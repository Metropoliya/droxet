
import urllib.request
import urllib.error
import json
import os
import ssl
from datetime import datetime

API_URL = "https://catfact.ninja/fact"
OUTPUT  = "facts.txt"
TIMEOUT = 5


def fetch_fact(url: str, timeout: int = TIMEOUT) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
            "Accept": "application/json",
        }
    )
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
        raw = response.read().decode("utf-8")

    data = json.loads(raw)
    fact = data.get("fact", "").strip()
    if not fact:
        raise ValueError("API вернул пустой факт.")
    return fact


def save_fact(fact: str, filepath: str = OUTPUT) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {fact}\n"
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(line)


def main() -> None:
    print("Запрашиваю факт о котах...")

    try:
        fact = fetch_fact(API_URL)
    except urllib.error.URLError:
        print("Не удалось получить факт")
        return
    except (json.JSONDecodeError, ValueError, KeyError):
        print("Не удалось получить факт")
        return
    except Exception:
        print("Не удалось получить факт")
        return

    save_fact(fact)

    print(f"\nФакт: {fact}")
    print(f"\nСохранено в {OUTPUT}")

    try:
        with open(OUTPUT, encoding="utf-8") as f:
            total = sum(1 for _ in f)
        print(f"Всего фактов в файле: {total}")
    except OSError:
        pass


if __name__ == "__main__":
    main()
