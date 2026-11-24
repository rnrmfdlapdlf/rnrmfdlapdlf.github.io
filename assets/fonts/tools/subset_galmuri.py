"""갈무리11(Galmuri11) 공용 웹 글꼴 서브셋 생성 스크립트.

사용법:
    python -I subset_galmuri.py <Galmuri11.ttf> <출력 폴더>

글자 범위는 subset_noto.py 와 같습니다.
    - 기본 라틴(U+0020~U+007E), 라틴-1 보충
    - KS X 1001 비한자 전체 (기호, 전각 문자, 한글 자모, 한글 2,350자, 가나 등)
    - EXTRA_CHARS 에 적은 글자

갈무리11은 1200 유닛 = 12px 격자로 그린 픽셀 글꼴입니다.
12px의 정수배(12·24·36·48px)로 써야 픽셀이 뭉개지지 않습니다.
fontTools, brotli 가 필요합니다.
"""
import sys
from pathlib import Path

from fontTools import subset

# 2,350자 밖에서 페이지에 필요한 글자를 여기에 추가합니다.
EXTRA_CHARS = "·…‥『』「」《》〈〉【】※★☆♪→←↑↓○●◎◇◆□■△▲▽▼▶◀～〜、。—–‘’“”•×÷°℃™©®"


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
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["*"]
    options.name_IDs = ["*"]
    options.name_languages = ["*"]
    options.notdef_outline = True
    options.hinting = False
    font = subset.load_font(str(src), options)
    subsetter = subset.Subsetter(options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    target = out / f"{src.stem}.woff2"
    subset.save_font(font, str(target), options)
    print(f"{target.name}\t{target.stat().st_size // 1024} KB")
    print(f"글자 수: {len(text)}")


if __name__ == "__main__":
    main()
