
To validate the correctness of the Excel reading script:

1. Prepare test files:
   - "Raw.xlsx" containing sheet "GMES_DB" with known data in the second column.
   - Include cases with empty cells, formula cells, mixed data types.
2. Run the script and verify output:
   - Output is a single CSV string.
   - Values correctly correspond to the second column data.
   - Empty cells represented by empty fields (consecutive commas).
3. Test error handling:
   - Rename or remove "Raw.xlsx" and expect clear error message.
   - Change or remove "GMES_DB" sheet and verify error.
4. Confirm cleanup:
   - Excel process is closed after script runs, no lingering processes.
5. Edge cases:
   - Entire second column empty -> output should be an empty line.
   - Cells with formulas return calculated values.
6. Mark test as SUCCESS only if all conditions above are met and script performs smoothly without crashes.
7. Otherwise, mark as FAIL and report issues.

Provide a concise testing report template capturing these checks and results.
