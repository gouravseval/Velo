import re
import json
import shlex
from app.domain.entities.api_spec import ApiSpec, HttpMethod


class CurlParser:
    """
    Parses a curl command string into an ApiSpec.

    Supports:
      -X / --request      HTTP method
      -H / --header        headers
      -d / --data          body (JSON)
      --url / positional   URL
    """

    def parse(self, curl_str: str) -> ApiSpec:
        # Normalise line continuations
        curl_str = curl_str.replace("\\\n", " ").strip()
        tokens = shlex.split(curl_str)

        method = HttpMethod.GET
        url = ""
        headers: dict[str, str] = {}
        body_raw: str | None = None

        i = 1  # skip "curl"
        while i < len(tokens):
            tok = tokens[i]
            if tok in ("-X", "--request"):
                method = HttpMethod(tokens[i + 1].upper())
                i += 2
            elif tok in ("-H", "--header"):
                key, _, val = tokens[i + 1].partition(":")
                headers[key.strip()] = val.strip()
                i += 2
            elif tok in ("-d", "--data", "--data-raw"):
                body_raw = tokens[i + 1]
                if method == HttpMethod.GET:
                    method = HttpMethod.POST
                i += 2
            elif tok.startswith("http"):
                url = tok
                i += 1
            elif tok == "--url":
                url = tokens[i + 1]
                i += 2
            else:
                i += 1

        body_template = None
        if body_raw:
            try:
                body_template = json.loads(body_raw)
            except json.JSONDecodeError:
                body_template = {"_raw": body_raw}

        return ApiSpec(
            method=method,
            url=url,
            headers=headers,
            body_template=body_template,
        )
