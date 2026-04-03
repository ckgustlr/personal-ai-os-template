Step-by-step logic:
1. Initialize xlwings app in background mode.
2. Open the specified Excel file "Raw.xlsx".
3. Access the worksheet named "GMES_DB".
4. Iterate through all rows in the worksheet.
5. Extract the value from the second column of each row.
6. Concatenate these values into a single CSV formatted string, separated by commas.
7. Print the resulting one-line string.
8. Properly close the workbook and quit the app.

Input specification:
- File: Raw.xlsx
- Worksheet name: GMES_DB
- Data type: xlsx

Output specification:
- A single CSV-formatted line containing all second-column values from the sheet, like: 2026,1,DA,,,,,
- Printed to stdout.

Edge cases:
- Empty rows or empty cells in the second column should be treated as empty strings.
- The worksheet might contain merged cells or hidden rows; treat them as normal and read their values.
- Handle the case where the worksheet "GMES_DB" does not exist.

Error handling:
- Capture and handle file not found errors.
- Handle inability to open the Excel application.
- Handle missing worksheet errors.
- Ensure that the app and workbook are cleanly closed on error.
- Print meaningful error messages to stderr and exit gracefully.

Final instruction:
Generate clean, production-grade Python code that uses xlwings to open Excel in background mode, read the second column of the "GMES_DB" sheet from "Raw.xlsx", print one CSV line of all values, handle errors gracefully, and close resources properly.

