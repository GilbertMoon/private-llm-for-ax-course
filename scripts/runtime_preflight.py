from __future__ import annotations

import platform
import sys
from urllib.error import URLError
from urllib.request import urlopen


MODELS_URL = "http://localhost:1234/v1/models"


def print_environment() -> None:
    print("=== Environment ===")
    print(f"OS: {platform.platform()}")
    print(f"Python: {sys.version.split()[0]}")


def check_lm_studio() -> None:
    print("\n=== LM Studio Server ===")

    try:
        with urlopen(MODELS_URL, timeout=5) as response:
            body = response.read().decode("utf-8")
    except URLError as exc:
        print("FAIL: LM Studio Local Server에 연결할 수 없습니다.")
        print("확인 순서:")
        print("1. LM Studio가 실행 중인지 확인")
        print("2. Local Server가 시작되었는지 확인")
        print("3. Port가 1234인지 확인")
        print(f"Error: {exc}")
        raise SystemExit(1)

    print("PASS: LM Studio Local Server 응답 확인")
    print("\n=== /v1/models raw response ===")
    print(body)
    print("\n위 응답의 model id를 Chapter 03~05 코드에서 사용하세요.")


def main() -> None:
    print_environment()
    check_lm_studio()


if __name__ == "__main__":
    main()
