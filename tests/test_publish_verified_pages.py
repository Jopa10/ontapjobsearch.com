import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "pipeline" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
SCRIPT = SCRIPTS_DIR / "publish_verified_pages.py"
spec = importlib.util.spec_from_file_location("publish_verified_pages", SCRIPT)
publish = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = publish
spec.loader.exec_module(publish)


class PublishVerifiedPagesTests(unittest.TestCase):
    def write_json(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def mapping(self, source, dest):
        return publish.Mapping("Test", "Test Region", "admin_service", source, dest)

    def active(self):
        return {("Test Region", "admin_service")}

    def test_activated_slice_mappings_are_live(self):
        expected = {
            ("Hampshire", "support_worker"): (
                Path("pipeline/output-support-worker/hampshire-support-worker.json"),
                Path("app/hampshire/support-worker.json"),
            ),
            ("Surrey", "admin_service"): (
                Path("pipeline/output-admin-service/surrey-admin-service.json"),
                Path("app/surrey/service-administrator-jobs.json"),
            ),
            ("Kent", "admin_service"): (
                Path("pipeline/output-admin-service/kent-admin-service.json"),
                Path("app/kent/service-administrator-jobs.json"),
            ),
        }
        mappings = {
            (mapping.region, mapping.category): (mapping.source, mapping.destination)
            for mapping in publish.MAPPINGS
        }

        for slice_key, paths in expected.items():
            with self.subTest(slice_key=slice_key):
                self.assertEqual(paths, mappings[slice_key])
                self.assertIn(slice_key, publish.live_slices())

    def test_non_live_slice_is_skipped_before_reading_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dest = Path("live.json")
            live = [{"job_id": "existing", "title": "Existing", "apply_url": "https://example.com/existing"}]
            self.write_json(root / dest, live)

            result = publish.publish_one(
                self.mapping(Path("missing-source.json"), dest),
                write=True,
                active_slices=set(),
                root=root,
            )

            self.assertEqual(result["status"], "skipped")
            self.assertIn("not LIVE", result["reason"])
            self.assertEqual(json.loads((root / dest).read_text()), live)

    def test_duplicate_job_id_fails_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = Path("source.json")
            dest = Path("live.json")
            row = {"job_id": "1", "title": "Role", "apply_url": "https://example.com/apply"}
            self.write_json(root / source, [row, dict(row)])
            self.write_json(root / dest, [])

            result = publish.publish_one(self.mapping(source, dest), write=True, active_slices=self.active(), root=root)

            self.assertEqual(result["status"], "failed")
            self.assertIn("duplicate job_id", result["reason"])
            self.assertEqual(json.loads((root / dest).read_text()), [])

    def test_zero_job_source_clears_stale_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = Path("source.json")
            dest = Path("live.json")
            live = [{"job_id": "existing", "title": "Existing", "apply_url": "https://example.com/existing"}]
            self.write_json(root / source, [])
            self.write_json(root / dest, live)

            result = publish.publish_one(self.mapping(source, dest), write=True, active_slices=self.active(), root=root)

            self.assertEqual(result["status"], "published")
            self.assertIn("validated zero", result["reason"])
            self.assertEqual(json.loads((root / dest).read_text()), [])

    def test_zero_job_source_is_unchanged_when_destination_already_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = Path("source.json")
            dest = Path("live.json")
            self.write_json(root / source, [])
            self.write_json(root / dest, [])

            result = publish.publish_one(self.mapping(source, dest), write=True, active_slices=self.active(), root=root)

            self.assertEqual(result["status"], "unchanged")
            self.assertEqual(json.loads((root / dest).read_text()), [])

    def test_destination_file_must_already_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = Path("source.json")
            dest = Path("missing/live.json")
            self.write_json(root / source, [{"job_id": "1", "title": "Role", "apply_url": "https://example.com/apply"}])

            result = publish.publish_one(self.mapping(source, dest), write=True, active_slices=self.active(), root=root)

            self.assertEqual(result["status"], "failed")
            self.assertIn("destination parent directory does not exist", result["reason"])
            self.assertFalse((root / dest).exists())

    def test_first_ontap_publication_date_is_added_when_feed_date_is_blank(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = Path("source.json")
            dest = Path("live.json")
            self.write_json(root / source, [{"job_id": "1", "title": "Role", "apply_url": "https://example.com/apply", "posted_date": ""}])
            self.write_json(root / dest, [])

            result = publish.publish_one(
                self.mapping(source, dest),
                write=True,
                active_slices=self.active(),
                root=root,
                publication_date="2026-07-17",
            )

            self.assertEqual(result["status"], "published")
            row = json.loads((root / dest).read_text())[0]
            self.assertEqual(row["posted_date"], "2026-07-17")
            self.assertEqual(row["posted_date_basis"], "ontap_first_published")

    def test_first_ontap_publication_date_is_preserved_on_later_uploads(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = Path("source.json")
            dest = Path("live.json")
            row = {"job_id": "1", "title": "Role", "apply_url": "https://example.com/apply", "posted_date": ""}
            self.write_json(root / source, [row])
            self.write_json(root / dest, [{**row, "posted_date": "2026-07-15", "posted_date_basis": "ontap_first_published"}])

            result = publish.publish_one(
                self.mapping(source, dest),
                write=True,
                active_slices=self.active(),
                root=root,
                publication_date="2026-07-17",
            )

            self.assertEqual(result["status"], "unchanged")
            preserved = json.loads((root / dest).read_text())[0]
            self.assertEqual(preserved["posted_date"], "2026-07-15")
            self.assertEqual(preserved["posted_date_basis"], "ontap_first_published")

    def test_shared_first_publication_date_survives_a_slice_move(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = Path("new-slice-source.json")
            dest = Path("new-slice-live.json")
            row = {
                "job_id": "1",
                "title": "Role",
                "apply_url": "https://example.com/apply",
                "posted_date": "",
            }
            self.write_json(root / source, [row])
            self.write_json(root / dest, [])

            result = publish.publish_one(
                self.mapping(source, dest),
                write=True,
                active_slices=self.active(),
                root=root,
                publication_date="2026-07-20",
                shared_dates={
                    "1": ("2026-07-15", "ontap_first_published")
                },
            )

            self.assertEqual(result["status"], "published")
            preserved = json.loads((root / dest).read_text())[0]
            self.assertEqual(preserved["posted_date"], "2026-07-15")
            self.assertEqual(
                preserved["posted_date_basis"], "ontap_first_published"
            )

    def test_existing_source_date_is_not_refreshed_by_a_changed_feed_value(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = Path("source.json")
            dest = Path("live.json")
            self.write_json(
                root / source,
                [
                    {
                        "job_id": "1",
                        "title": "Role",
                        "apply_url": "https://example.com/apply",
                        "posted_date": "2026-07-16",
                        "posted_date_basis": "source",
                    }
                ],
            )
            self.write_json(
                root / dest,
                [
                    {
                        "job_id": "1",
                        "title": "Role",
                        "apply_url": "https://example.com/apply",
                        "posted_date": "2026-07-15",
                        "posted_date_basis": "source",
                    }
                ],
            )

            result = publish.publish_one(
                self.mapping(source, dest),
                write=True,
                active_slices=self.active(),
                root=root,
                publication_date="2026-07-20",
            )

            self.assertEqual(result["status"], "unchanged")
            preserved = json.loads((root / dest).read_text())[0]
            self.assertEqual(preserved["posted_date"], "2026-07-15")
            self.assertEqual(preserved["posted_date_basis"], "source")

    def test_first_reliable_source_date_replaces_ontap_fallback(self):
        source_rows = [
            {
                "job_id": "1",
                "title": "Role",
                "apply_url": "https://example.com/apply",
                "posted_date": "2026-07-10",
                "posted_date_basis": "jobg8_start_date",
            }
        ]
        destination_rows = [
            {
                "job_id": "1",
                "title": "Role",
                "apply_url": "https://example.com/apply",
                "posted_date": "2026-07-15",
                "posted_date_basis": "ontap_first_published",
            }
        ]

        result = publish.add_stable_posted_dates(
            source_rows,
            destination_rows,
            publication_date="2026-07-20",
        )

        self.assertEqual(result[0]["posted_date"], "2026-07-10")
        self.assertEqual(result[0]["posted_date_basis"], "jobg8_start_date")

    def test_shared_dates_use_earliest_ontap_date_across_destinations_and_ledger(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = self.mapping(Path("source-a.json"), Path("live-a.json"))
            second = self.mapping(Path("source-b.json"), Path("live-b.json"))
            self.write_json(
                root / first.destination,
                [
                    {
                        "job_id": "1",
                        "title": "Role",
                        "apply_url": "https://example.com/apply",
                        "posted_date": "2026-07-15",
                        "posted_date_basis": "ontap_first_published",
                    }
                ],
            )
            self.write_json(
                root / second.destination,
                [
                    {
                        "job_id": "1",
                        "title": "Role",
                        "apply_url": "https://example.com/apply",
                        "posted_date": "2026-07-18",
                        "posted_date_basis": "ontap_first_published",
                    }
                ],
            )
            ledger = root / publish.FIRST_SEEN_HISTORY
            ledger.parent.mkdir(parents=True, exist_ok=True)
            ledger.write_text(
                "first_seen_date,job_id\n2026-07-17,1\n",
                encoding="utf-8",
            )

            dates = publish.load_shared_posted_dates([first, second], root=root)

            self.assertEqual(
                dates["1"], ("2026-07-15", "ontap_first_published")
            )

    def test_legacy_first_publication_date_is_preserved_without_guessing_basis(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = Path("source.json")
            dest = Path("live.json")
            row = {"job_id": "1", "title": "Role", "apply_url": "https://example.com/apply", "posted_date": ""}
            self.write_json(root / source, [row])
            self.write_json(root / dest, [{**row, "posted_date": "2026-07-15"}])

            result = publish.publish_one(
                self.mapping(source, dest),
                write=True,
                active_slices=self.active(),
                root=root,
                publication_date="2026-07-17",
            )

            self.assertEqual(result["status"], "unchanged")
            self.assertNotIn("posted_date_basis", json.loads((root / dest).read_text())[0])

    def test_real_feed_posted_date_takes_precedence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = Path("source.json")
            dest = Path("live.json")
            self.write_json(root / source, [{"job_id": "1", "title": "Role", "apply_url": "https://example.com/apply", "posted_date": "2026-07-10", "posted_date_basis": "source"}])
            self.write_json(root / dest, [{"job_id": "1", "title": "Role", "apply_url": "https://example.com/apply", "posted_date": "2026-07-15", "posted_date_basis": "ontap_first_published"}])

            result = publish.publish_one(
                self.mapping(source, dest),
                write=True,
                active_slices=self.active(),
                root=root,
                publication_date="2026-07-17",
            )

            self.assertEqual(result["status"], "published")
            row = json.loads((root / dest).read_text())[0]
            self.assertEqual(row["posted_date"], "2026-07-10")
            self.assertEqual(row["posted_date_basis"], "source")

    def test_external_source_date_is_marked_as_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = Path("source.json")
            dest = Path("live.json")
            self.write_json(root / source, [{"job_id": "nejobs-1", "title": "Role", "apply_url": "https://example.com/apply", "posted_date": "10/07/2026", "source": "NEJobs"}])
            self.write_json(root / dest, [])

            result = publish.publish_one(
                self.mapping(source, dest),
                write=True,
                active_slices=self.active(),
                root=root,
            )

            self.assertEqual(result["status"], "published")
            row = json.loads((root / dest).read_text())[0]
            self.assertEqual(row["posted_date"], "2026-07-10")
            self.assertEqual(row["posted_date_basis"], "source")

    def test_post_write_mismatch_restores_previous_destination_and_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = Path("source.json")
            dest = Path("live.json")
            live = [{"job_id": "old", "title": "Old", "apply_url": "https://example.com/old"}]
            selected = [{"job_id": "new", "title": "New", "apply_url": "https://example.com/new"}]
            self.write_json(root / source, selected)
            self.write_json(root / dest, live)
            original_atomic_write = publish.atomic_write

            def tamper_once(path, content):
                if not hasattr(tamper_once, "called"):
                    tamper_once.called = True
                    original_atomic_write(path, json.dumps([{**selected[0], "title": "Tampered"}]) + "\n")
                else:
                    original_atomic_write(path, content)

            with mock.patch.object(publish, "atomic_write", side_effect=tamper_once):
                result = publish.publish_one(self.mapping(source, dest), write=True, active_slices=self.active(), root=root)

            self.assertEqual(result["status"], "failed")
            self.assertIn("restored previous destination", result["reason"])
            self.assertEqual(json.loads((root / dest).read_text()), live)


if __name__ == "__main__":
    unittest.main()
