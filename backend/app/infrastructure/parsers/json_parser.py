import json
from typing import Any
from app.domain.interfaces.i_file_parser import IFileParser


class JsonParser(IFileParser):
    def parse(self, data: bytes) -> list[dict[str, Any]]:
        parsed = json.loads(data.decode("utf-8"))
        if isinstance(parsed, list):
            return parsed
        if isinstance(parsed, dict):
            # Try common wrapper keys
            for key in ("data", "records", "items", "results"):
                if key in parsed and isinstance(parsed[key], list):
                    return parsed[key]
            return [parsed]
        raise ValueError("JSON root must be an array or object")
