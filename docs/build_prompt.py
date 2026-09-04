"""AGENTS.md에서 웹 UI(ChatGPT/Claude Projects)용 프롬프트를 생성한다.

WHY: 지침을 두 벌로 관리하면 반드시 어긋난다. AGENTS.md를 단일 원본으로 두고,
     웹 UI에는 저장소 파일 구조처럼 의미 없는 섹션만 걷어낸 사본을 붙여넣는다.
사용법: python docs/build_prompt.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "AGENTS.md"
DST = ROOT / "docs" / "PROMPT.md"

# 웹 UI에서는 로컬 파일 경로가 무의미하므로 제외할 섹션 제목
EXCLUDE_SECTIONS = ("## 4. 저장소 구조",)

HEADER = """# 웹 UI 붙여넣기용 프롬프트

> 이 파일은 `AGENTS.md`에서 자동 생성됩니다. 직접 수정하지 마십시오.
> 갱신: `python docs/build_prompt.py`
>
> ChatGPT Projects 또는 Claude Projects의 인스트럭션 칸에
> 아래 구분선부터 끝까지 붙여넣으십시오.

---

"""


def build(text: str) -> str:
    """`## ` 단위로 잘라 제외 섹션을 걷어내고, 파일 안내 서두를 제거한다."""
    lines = text.splitlines()

    # 첫 `## ` 이전(파일 자체에 대한 안내)은 웹 UI에 불필요하므로 버린다
    start = next(i for i, line in enumerate(lines) if line.startswith("## "))

    kept, skipping = [], False
    for line in lines[start:]:
        if line.startswith("## "):
            skipping = line.strip() in EXCLUDE_SECTIONS
        if not skipping:
            kept.append(line)

    body = "\n".join(kept).strip()
    return HEADER + "# 이력서·커리어 어드바이저\n\n" + body + "\n"


def main() -> None:
    DST.write_text(build(SRC.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"생성 완료: {DST.relative_to(ROOT)} ({DST.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
