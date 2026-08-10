
import json
import os
import urllib.parse
import urllib.request

BASE = "https://api.stlouisfed.org/fred/series/observations"

def fetch_series(series_id: str, api_key: str | None = None, observation_start: str = "1990-01-01"):
    """
    Fetch one FRED series using the official FRED API.
    API key is read from argument or FRED_API_KEY env var.
    """
    key = api_key or os.getenv("FRED_API_KEY")
    if not key:
        raise RuntimeError(
            "Missing FRED_API_KEY. Create a free FRED API key and store it as "
            "a GitHub Actions repository secret named FRED_API_KEY."
        )

    params = {
        "series_id": series_id,
        "api_key": key,
        "file_type": "json",
        "observation_start": observation_start,
        "sort_order": "asc",
    }
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "investment-research-terminal/3.1"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    data = []
    for row in payload.get("observations", []):
        v = row.get("value")
        if v in (None, ".", ""):
            continue
        try:
            value = float(v)
        except ValueError:
            continue
        data.append([row["date"], value])
    if not data:
        raise RuntimeError(f"No observations returned for FRED series {series_id}")
    return data
