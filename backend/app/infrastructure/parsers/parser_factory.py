from app.domain.interfaces.i_file_parser import IFileParser
from app.infrastructure.parsers.csv_parser import CsvParser
from app.infrastructure.parsers.json_parser import JsonParser
from app.infrastructure.parsers.excel_parser import ExcelParser


class ParserFactory:
    _MIME_MAP: dict[str, type] = {
        "text/csv": CsvParser,
        "application/csv": CsvParser,
        "text/plain": CsvParser,
        "application/json": JsonParser,
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ExcelParser,
        "application/vnd.ms-excel": ExcelParser,
    }
    _EXT_MAP: dict[str, type] = {
        ".csv": CsvParser,
        ".json": JsonParser,
        ".xlsx": ExcelParser,
        ".xls": ExcelParser,
    }

    def get_parser(self, content_type: str, file_name: str = "") -> IFileParser:
        # Try MIME type first
        cls = self._MIME_MAP.get(content_type.split(";")[0].strip().lower())
        if cls:
            return cls()

        # Fall back to file extension
        if file_name:
            for ext, parser_cls in self._EXT_MAP.items():
                if file_name.lower().endswith(ext):
                    return parser_cls()

        raise ValueError(
            f"Unsupported file type: content_type={content_type!r}, file_name={file_name!r}. "
            f"Supported: CSV, JSON, XLSX"
        )
