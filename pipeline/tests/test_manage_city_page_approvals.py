import tempfile
import unittest
from pathlib import Path

from scripts.manage_city_page_approvals import (
    build_config,
    candidate_from_parent,
    page_source,
    parse_review,
    public_slice,
    render_review,
    slugify,
)


class CityPageApprovalTests(unittest.TestCase):
    def test_slug_and_support_route_are_generic(self):
        self.assertEqual(slugify("Brighton & Hove"), "brighton-hove")
        self.assertEqual(public_slice("support-worker-jobs"), "support-worker")
        self.assertEqual(public_slice("service-administrator-jobs"), "service-administrator-jobs")

    def test_review_uses_one_human_action_field(self):
        rows = [
            {
                "region": "west-yorkshire",
                "slice": "service-administrator-jobs",
                "locality": "Leeds",
                "jobs": 6,
                "qualifying_runs": 3,
                "history": [6, 6, 6],
            }
        ]
        text = render_review(rows, [])
        self.assertIn("action: ", text)
        self.assertIn("status: READY FOR APPROVAL", text)
        self.assertIn("city: Leeds", text)
        self.assertIn("Edit only the `action:` line", text)

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "review.md"
            edited = text.replace(
                "\naction: \nstatus: READY FOR APPROVAL",
                "\naction: approve\nstatus: READY FOR APPROVAL",
                1,
            )
            path.write_text(edited, encoding="utf-8")
            blocks = parse_review(path)
        self.assertEqual(blocks[0]["action"], "approve")

    def test_dynamic_configured_slice_is_a_supported_city_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "app/_city-pages/configured-slices/lincolnshire/service-administrator-jobs.json"
            source.parent.mkdir(parents=True)
            source.write_text(
                '[{"location":"Lincoln"},{"location":"Boston"}]',
                encoding="utf-8",
            )
            market = {
                "region_key": "lincolnshire",
                "market_key": "lincoln",
                "display_name": "Lincoln",
                "include_patterns": ["lincoln"],
            }
            candidate = candidate_from_parent(root, "lincolnshire", "service-administrator-jobs", market)
            self.assertEqual(candidate["jobs"], 1)
            self.assertEqual(
                candidate["parent_json"],
                "app/_city-pages/configured-slices/lincolnshire/service-administrator-jobs.json",
            )
            config = build_config(
                region="lincolnshire",
                slice_key="service-administrator-jobs",
                locality="Lincoln",
                market=market,
                all_markets=[market],
                parent_page=candidate["parent_json"],
            )
            self.assertEqual(config["parent_page"], candidate["parent_json"])
            self.assertIn('href: "/job-search/lincolnshire/service-administrator-jobs"', page_source(config))

    def test_config_is_built_from_market_register_data_not_city_exceptions(self):
        leeds = {
            "region_key": "west-yorkshire",
            "market_key": "leeds",
            "display_name": "Leeds",
            "include_patterns": ["leeds", "pudsey"],
        }
        bradford = {
            "region_key": "west-yorkshire",
            "market_key": "bradford",
            "display_name": "Bradford",
            "include_patterns": ["bradford"],
        }
        config = build_config(
            region="west-yorkshire",
            slice_key="service-administrator-jobs",
            locality="Leeds",
            market=leeds,
            all_markets=[leeds, bradford],
        )
        self.assertEqual(config["route"], "/leeds/service-administrator-jobs")
        self.assertEqual(
            config["output_json"],
            "app/_city-pages/leeds/service-administrator-jobs.json",
        )
        self.assertEqual(
            [rule["pattern"] for rule in config["include_rules"]],
            ["leeds", "pudsey"],
        )
        self.assertIn("bradford", [rule["pattern"] for rule in config["exclude_rules"]])
        self.assertEqual(config["lifecycle_state"], "active")
        self.assertEqual(config["category_label"], "admin and office jobs")
        self.assertTrue(config["include_office_family_supplements"])
        self.assertEqual(config["exact_localities"], ["Leeds"])

        source = page_source(config)
        self.assertIn('const route = "/leeds/service-administrator-jobs";', source)
        self.assertIn("getCityPageDefinitionByRoute", source)
        self.assertIn("Admin and office jobs in Leeds", source)


if __name__ == "__main__":
    unittest.main()
