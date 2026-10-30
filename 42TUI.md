# 42TUI report fork

Based on Tripouille/gnlTester. `python3 report.py --report PATH` runs the mandatory suite without self-updating and writes a fresh version-1 JSON report. Checks increment passed/failed, leaks increment failed, and crashed/timed-out children increment errors. Allocation-size checks remain in the console but are not included in the report. A failed build or incomplete suite does not write a report. Existing output is preserved.

The reporter uses an event file inherited by forked tests. The report is intended for ordinary student projects and is not a security boundary against deliberately hostile code. The upstream test suite and Valgrind behavior remain platform-dependent.
