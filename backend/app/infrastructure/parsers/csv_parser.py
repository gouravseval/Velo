import csv
import io
from typing import Any
from app.domain.interfaces.i_file_parser import IFileParser


class CsvParser(IFileParser):
    def parse(self, data: bytes) -> list[dict[str, Any]]:
        text = data.decode("utf-8-sig", errors="replace")
        reader = csv.DictReader(io.StringIO(text))
        return [dict(row) for row in reader]
