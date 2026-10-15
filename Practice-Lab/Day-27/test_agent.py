import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from main import (
    create_test_files,
    execute_action,
    run_workflow,
    validate_action,
)


class HumanApprovalAgentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        self.root = Path(self.temp.name) / "workspace"
        self.root.mkdir()

        create_test_files(self.root)
        self.log_path = Path(self.temp.name) / "actions.jsonl"

        self.action = {
            "source": "notes.txt",
            "destination": "Documents/notes.txt",
            "reason": "Text files belong in Documents.",
        }

    def planner(self, goal, filenames):
        return [self.action]

    def read_log(self):
        if not self.log_path.exists():
            return []

        return [
            json.loads(line)
            for line in self.log_path.read_text(encoding="utf-8").splitlines()
        ]

    def test_approved_action_moves_file(self):
        run_workflow(
            "Organize files",
            self.root,
            self.log_path,
            input_fn=lambda prompt: "a",
            planner=self.planner,
        )

        self.assertFalse((self.root / "notes.txt").exists())
        self.assertTrue(
            (self.root / "Documents" / "notes.txt").is_file()
        )

        records = self.read_log()
        self.assertEqual(records[-1]["decision"], "approved")
        self.assertEqual(records[-1]["result"], "executed")

    def test_rejected_action_is_never_executed(self):
        with patch("main.execute_action") as mocked_execute:
            run_workflow(
                "Organize files",
                self.root,
                self.log_path,
                input_fn=lambda prompt: "r",
                planner=self.planner,
            )

            mocked_execute.assert_not_called()

        self.assertTrue((self.root / "notes.txt").is_file())
        self.assertFalse(
            (self.root / "Documents" / "notes.txt").exists()
        )

        records = self.read_log()
        self.assertEqual(records[-1]["decision"], "rejected")
        self.assertEqual(records[-1]["result"], "Not executed.")

    def test_cancel_stops_remaining_actions(self):
        second_action = {
            "source": "report.pdf",
            "destination": "Reports/report.pdf",
            "reason": "PDF files belong in Reports.",
        }

        def two_action_planner(goal, filenames):
            return [self.action, second_action]

        with patch("main.execute_action") as mocked_execute:
            run_workflow(
                "Organize files",
                self.root,
                self.log_path,
                input_fn=lambda prompt: "c",
                planner=two_action_planner,
            )

            mocked_execute.assert_not_called()

        self.assertTrue((self.root / "notes.txt").exists())
        self.assertTrue((self.root / "report.pdf").exists())

        records = self.read_log()
        self.assertEqual(records[-1]["decision"], "cancelled")
        self.assertEqual(len(records), 1)

    def test_path_traversal_is_rejected(self):
        unsafe = {
            "source": "../notes.txt",
            "destination": "Documents/notes.txt",
            "reason": "Unsafe test.",
        }

        valid, message = validate_action(unsafe, self.root)

        self.assertFalse(valid)
        self.assertIn("Unsafe source", message)

    def test_outside_destination_is_rejected(self):
        unsafe = {
            "source": "notes.txt",
            "destination": "../../outside.txt",
            "reason": "Unsafe test.",
        }

        valid, message = validate_action(unsafe, self.root)

        self.assertFalse(valid)
        self.assertIn("Destination must be", message)

    def test_existing_destination_is_not_overwritten(self):
        destination_dir = self.root / "Documents"
        destination_dir.mkdir()
        destination_file = destination_dir / "notes.txt"
        destination_file.write_text("Keep this content.", encoding="utf-8")

        valid, message = validate_action(self.action, self.root)

        self.assertFalse(valid)
        self.assertIn("overwrite blocked", message)

        with self.assertRaises(ValueError):
            execute_action(self.action, self.root)

        self.assertEqual(
            destination_file.read_text(encoding="utf-8"),
            "Keep this content.",
        )
        self.assertTrue((self.root / "notes.txt").exists())

    def test_malformed_model_plan_does_not_execute(self):
        def broken_planner(goal, filenames):
            raise json.JSONDecodeError("Invalid JSON", "not json", 0)

        with patch("main.execute_action") as mocked_execute:
            run_workflow(
                "Organize files",
                self.root,
                self.log_path,
                input_fn=lambda prompt: "a",
                planner=broken_planner,
            )

            mocked_execute.assert_not_called()

        self.assertTrue((self.root / "notes.txt").exists())

        records = self.read_log()
        self.assertEqual(records[-1]["decision"], "error")
        self.assertIn("Planning failed", records[-1]["result"])


if __name__ == "__main__":
    unittest.main()