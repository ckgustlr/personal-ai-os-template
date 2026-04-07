import xlwings as xw
import pandas as pd
import json


class ExcelParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.app = xw.App(visible=False)
        self.wb = self.app.books.open(file_path)

    def close(self):
        self.wb.close()
        self.app.quit()

    # ---------------------------
    # Sheet Loop
    # ---------------------------
    def extract_sheets(self):
        results = []

        for sheet in self.wb.sheets:
            sheet_data = {
                "sheet_name": sheet.name,
                "tables": self.extract_tables(sheet),
                "formulas": self.extract_formulas(sheet),
                "notes": self.extract_notes(sheet)
            }

            results.append(sheet_data)

        return results

    # ---------------------------
    # Table Extraction
    # ---------------------------
    def extract_tables(self, sheet):
        tables = []

        used_range = sheet.used_range
        values = used_range.value

        if not values or len(values) < 2:
            return tables

        df = pd.DataFrame(values[1:], columns=values[0])

        # 데이터 클린
        df = df.dropna(how='all')

        if df.empty:
            return tables

        table_info = {
            "name": f"{sheet.name}_table",
            "columns": list(df.columns),
            "sample_rows": df.head(5).values.tolist(),
            "stats": self._get_stats(df)
        }

        tables.append(table_info)
        return tables

    # ---------------------------
    # Stats Summary
    # ---------------------------
    def _get_stats(self, df):
        stats = {}
        numeric_df = df.select_dtypes(include='number')

        if not numeric_df.empty:
            stats = {
                col: {
                    "mean": float(numeric_df[col].mean()),
                    "min": float(numeric_df[col].min()),
                    "max": float(numeric_df[col].max())
                }
                for col in numeric_df.columns
            }

        return stats

    # ---------------------------
    # Formula Extraction
    # ---------------------------
    def extract_formulas(self, sheet):
        formulas = []

        used_range = sheet.api.UsedRange

        for row in range(1, used_range.Rows.Count + 1):
            for col in range(1, used_range.Columns.Count + 1):
                cell = used_range.Cells(row, col)

                if cell.HasFormula:
                    formulas.append({
                        "cell": cell.Address,
                        "formula": cell.Formula
                    })

        return formulas[:50]  # 토큰 제한 대비

    # ---------------------------
    # Notes / Text Extraction
    # ---------------------------
    def extract_notes(self, sheet):
        notes = []

        used_range = sheet.used_range.value

        if not used_range:
            return notes

        for row in used_range:
            for cell in row:
                if isinstance(cell, str) and len(cell) > 20:
                    notes.append(cell)

        return notes[:20]

    # ---------------------------
    # Final JSON Builder
    # ---------------------------
    def build_llm_input(self):
        data = {
            "file_name": self.file_path,
            "sheets": self.extract_sheets()
        }

        return data


# ---------------------------
# 실행
# ---------------------------
if __name__ == "__main__":
    parser = ExcelParser("your_file.xlsx")

    try:
        result = parser.build_llm_input()

        with open("llm_input.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print("✅ JSON 생성 완료")

    finally:
        parser.close()