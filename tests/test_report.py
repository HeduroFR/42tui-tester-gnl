"""Contract checks for fresh reports and incomplete test groups."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

REPORTER = Path(__file__).resolve().parents[1] / 'report.py'

class ReportTests(unittest.TestCase):
    def test_outcomes_and_missing_report_on_build_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make = root / 'make'
            make.write_text('#!/bin/sh\nprintf %s "$TEST_EVENTS" >> "$GNL_REPORT_EVENTS"\nexit "$TEST_EXIT"\n')
            make.chmod(0o755)
            for events, exit_code, expected, counts in (
                ('BPPC', 0, 0, (2, 0, 0)), ('BFC', 0, 1, (0, 1, 0)),
                ('BE', 0, 1, (0, 0, 1)), ('BP', 0, 1, (1, 0, 1)),
                ('BPPC', 2, 2, None), ('BAD', 0, 1, None),
            ):
                with self.subTest(events=events, exit_code=exit_code):
                    report = root / f'result-{events}-{exit_code}.json'
                    env = dict(os.environ, PATH=str(root) + os.pathsep + os.environ['PATH'],
                               TEST_EVENTS=events, TEST_EXIT=str(exit_code))
                    run = subprocess.run([sys.executable, str(REPORTER), '--report', str(report)],
                                         cwd=root, env=env, capture_output=True)
                    self.assertEqual(run.returncode, expected, run.stderr)
                    if counts is None:
                        self.assertFalse(report.exists())
                    else:
                        result = json.loads(report.read_text())
                        self.assertEqual(tuple(result[k] for k in ('passed', 'failed', 'errors')), counts)
                        self.assertEqual(result['total'], sum(counts))
                        again = subprocess.run([sys.executable, str(REPORTER), '--report', str(report)],
                                               cwd=root, env=env, capture_output=True)
                        self.assertNotEqual(again.returncode, 0)
                        self.assertEqual(json.loads(report.read_text()), result)

if __name__ == '__main__':
    unittest.main()
