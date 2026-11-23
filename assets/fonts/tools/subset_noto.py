"""Noto Sans KR 공용 웹 글꼴 서브셋 생성 스크립트.

사용법:
    python -I subset_noto.py <Noto_Sans_KR/static 폴더> <출력 폴더>

글자 범위:
    - 기본 라틴(U+0020~U+007E), 라틴-1 보충 문장부호 일부
    - KS X 1001 비한자 전체 (기호, 전각 문자, 한글 자모, 한글 2,350자, 가나 등)
    - EXTRA_CHARS 에 적은 글자 (2,350자 밖의 글자가 필요하면 여기에 추가)

9개 굵기(Thin~Black)를 각각 woff2 로 만듭니다. fontTools, brotli 가 필요합니다.
"""
import sys
from pathlib import Path

from fontTools import subset

WEIGHTS = ["Thin", "ExtraLight", "Light", "Regular", "Medium",
           "SemiBold", "Bold", "ExtraBold", "Black"]

# 2,350자 밖에서 페이지에 필요한 글자를 여기에 추가합니다.
EXTRA_CHARS = "·…‥『』「」《》〈〉【】※★☆♪→←↑↓○●◎◇◆□■△▲▽▼～〜、。—–‘’“”•×÷°℃™©®"


def ksx1001_chars():
    chars = set()
    for lead in range(0xA1, 0xC9):          # A1~C8: 기호·자모·한글 (C9 이후는 사용자 정의·한자)
        for trail in range(0xA1, 0xFF):
            try:
                chars.add(bytes([lead, trail]).decode("euc-kr"))
            except UnicodeDecodeError:
                pass
    return chars


def build_text():
    chars = ksx1001_chars()
    chars.update(chr(c) for c in range(0x20, 0x7F))
    chars.update(chr(c) for c in range(0xA0, 0x100))
    chars.update(EXTRA_CHARS)
    return "".join(sorted(chars))


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    text = build_text()
    for weight in WEIGHTS:
        options = subset.Options()
        options.flavor = "woff2"
        options.layout_features = ["*"]
        options.name_IDs = ["*"]
        options.name_languages = ["*"]
        options.notdef_outline = True
        options.hinting = False
        font = subset.load_font(str(src / f"NotoSansKR-{weight}.ttf"), options)
        subsetter = subset.Subsetter(options)
        subsetter.populate(text=text)
        subsetter.subset(font)
        target = out / f"NotoSansKR-{weight}.woff2"
        subset.save_font(font, str(target), options)
        print(f"{target.name}\t{target.stat().st_size // 1024} KB")
    print(f"글자 수: {len(text)}")


if __name__ == "__main__":
    main()
