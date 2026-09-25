from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"모듈을 불러올 수 없습니다: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    "relative_path,module_name",
    [
        ("chapter04/starter/rag.py", "chapter04_rag"),
        ("chapter05/starter/rag.py", "chapter05_rag"),
    ],
)
def test_split_into_chunks(relative_path: str, module_name: str) -> None:
    module = load_module(ROOT / relative_path, module_name)

    text = "첫 번째 규정\n\n두 번째 규정\n\n\n세 번째 규정"
    chunks = module.split_into_chunks(text)

    assert chunks == ["첫 번째 규정", "두 번째 규정", "세 번째 규정"]


@pytest.mark.parametrize(
    "relative_path,module_name",
    [
        ("chapter04/starter/rag.py", "chapter04_rag_cosine"),
        ("chapter05/starter/rag.py", "chapter05_rag_cosine"),
    ],
)
def test_cosine_similarity_identity(relative_path: str, module_name: str) -> None:
    module = load_module(ROOT / relative_path, module_name)

    assert module.cosine_similarity([1.0, 0.0], [1.0, 0.0]) == pytest.approx(1.0)


@pytest.mark.parametrize(
    "relative_path,module_name",
    [
        ("chapter04/starter/rag.py", "chapter04_rag_zero"),
        ("chapter05/starter/rag.py", "chapter05_rag_zero"),
    ],
)
def test_cosine_similarity_zero_vector(relative_path: str, module_name: str) -> None:
    module = load_module(ROOT / relative_path, module_name)

    assert module.cosine_similarity([0.0, 0.0], [1.0, 0.0]) == 0.0


def test_sample_policy_exists_and_has_expected_content() -> None:
    sample = ROOT / "data" / "sample" / "company_policy.txt"
    assert sample.is_file()

    text = sample.read_text(encoding="utf-8")
    assert "출장" in text
    assert "휴가" in text
