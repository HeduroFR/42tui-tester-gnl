#!/usr/bin/env python3
"""Run the mandatory suite and write a fresh 42TUI version-1 result report."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--report', required=True)
args = parser.parse_args()
report = Path(args.report)
if report.exists() or report.is_symlink():
    sys.exit('Report destination already exists')
fd, events = tempfile.mkstemp(prefix='gnl-report-')
os.close(fd)
try:
    env = dict(os.environ, GNL_REPORT_EVENTS=events)
    result = subprocess.run(['make', '-o', 'update', 'm'], env=env, check=False)
    if result.returncode:
        sys.exit(2)
    raw = Path(events).read_bytes()
    if not raw or set(raw) - set(b'PF EBC'.replace(b' ', b'')) or not raw.count(b'B') or raw.count(b'C') > raw.count(b'B'):
        sys.exit('Tester did not produce a valid result stream')
    counts = {'passed': raw.count(b'P'), 'failed': raw.count(b'F'),
              'errors': max(raw.count(b'E'), raw.count(b'B') - raw.count(b'C')), 'skipped': 0}
    counts['total'] = sum(counts.values())
    with report.open('x', encoding='utf-8') as output:
        json.dump({'version': 1, **counts}, output)
        output.write('\n')
    print('\nSummary:', counts, flush=True)
    sys.exit(1 if counts['failed'] or counts['errors'] else 0)
finally:
    os.unlink(events)
