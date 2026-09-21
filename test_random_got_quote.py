import requests
import time
import json


def get_quote():
    url = "https://api.gameofthronesquotes.xyz/v1/random"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://api.gameofthronesquotes.xyz/",
    }

    max_retries = 4
    backoff = 1

    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 429:
                print(f"Attempt {attempt}: 429 Too Many Requests")
                if attempt == max_retries:
                    return {
                        "error": "429 Too Many Requests",
                        "status_code": 429,
                        "response_text": resp.text[:500],
                    }
                time.sleep(backoff)
                backoff *= 2
                continue

            resp.raise_for_status()

            content_type = resp.headers.get("Content-Type", "")
            if "application/json" in content_type or "json" in content_type:
                try:
                    return resp.json()
                except Exception as e:
                    return {
                        "error": "Invalid JSON in response",
                        "exception": str(e),
                        "status_code": resp.status_code,
                        "response_text": resp.text[:500],
                    }

            try:
                return resp.json()
            except Exception as e:
                return {
                    "error": "Non-JSON response",
                    "exception": str(e),
                    "status_code": resp.status_code,
                    "response_text": resp.text[:500],
                }

        except requests.RequestException as e:
            print(f"Attempt {attempt}: RequestException: {e}")
            if attempt == max_retries:
                return {"error": "RequestException", "exception": str(e)}
            time.sleep(backoff)
            backoff *= 2

    return {"error": "max_retries_exhausted"}


if __name__ == "__main__":
    result = get_quote()
    print(json.dumps(result, indent=2, ensure_ascii=False))
