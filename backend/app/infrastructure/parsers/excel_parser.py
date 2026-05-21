import io
from typing import Any
from app.domain.interfaces.i_file_parser import IFileParser

try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False


class ExcelParser(IFileParser):
    def parse(self, data: bytes) -> list[dict[str, Any]]:
        if not HAS_OPENPYXL:
            raise RuntimeError("openpyxl is required to parse Excel files")
        wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True)
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            return []
        headers = [str(h) if h is not None else f"col_{i}" for i, h in enumerate(rows[0])]
        result = []
        for row in rows[1:]:
            result.append({headers[i]: row[i] for i in range(len(headers))})
        return result
