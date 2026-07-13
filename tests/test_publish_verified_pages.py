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

    def test_zero_job_source_is_skipped_without_changing_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = Path("source.json")
            dest = Path("live.json")
            live = [{"job_id": "existing", "title": "Existing", "apply_url": "https://example.com/existing"}]
            self.write_json(root / source, [])
            self.write_json(root / dest, live)

            result = publish.publish_one(self.mapping(source, dest), write=True, active_slices=self.active(), root=root)

            self.assertEqual(result["status"], "skipped")
            self.assertEqual(json.loads((root / dest).read_text()), live)

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
