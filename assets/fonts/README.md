# 공용 웹 글꼴

여러 프로젝트 페이지에서 함께 쓰는 글꼴입니다.

| 파일 | 글꼴 | 글자 범위 |
|---|---|---|
| `GyeonggiTitle-Medium.woff` | 경기천년제목 Medium | KS X 1001 한글 2,350자, 한글 자모, 영문·숫자, 주요 문장부호 |
| `gyeonggi-title.css` | 위 글꼴의 `@font-face` (`font-family: "GyeonggiTitle"`) | |
| `noto-sans-kr/NotoSansKR-*.woff2` | Noto Sans KR 9개 굵기 (Thin 100 ~ Black 900) | KS X 1001 비한자 전체(한글 2,350자·자모·기호), 영문·숫자, 주요 문장부호 |
| `noto-sans-kr.css` | 위 글꼴의 `@font-face` (`font-family: "Noto Sans KR"`, `font-weight` 100~900) | |
| `tools/subset_noto.py` | Noto Sans KR 서브셋 재생성 스크립트 (fontTools, brotli 필요) | |

## 사용법

```html
<link rel="stylesheet" href="/assets/fonts/gyeonggi-title.css">
<style>
  h1 { font-family: "GyeonggiTitle", "Malgun Gothic", sans-serif; }
</style>
```

```html
<link rel="stylesheet" href="/assets/fonts/noto-sans-kr.css">
<style>
  body { font-family: "Noto Sans KR", "Malgun Gothic", sans-serif; font-weight: 500; }
</style>
```

Noto Sans KR 서브셋을 다시 만들 때 (2,350자 밖의 글자가 필요하면 스크립트의 `EXTRA_CHARS`에 추가):

```
python assets/fonts/tools/subset_noto.py <Noto_Sans_KR/static 폴더> assets/fonts/noto-sans-kr
```

## 라이선스

경기천년체 © GYEONGGI PROVINCE. All Rights Reserved.

경기도 서체는 특별한 허가 절차 없이 누구나 무료로 다운로드 받아 자유롭게 사용할 수 있습니다.
영상, 인쇄, 웹, 로고, 간판 등 다양한 매체에 자유롭게 사용이 가능하며, 프로그램에 탑재하여 배포하는 것도 가능합니다.
단, 경기천년체 폰트 자체를 그대로 판매하거나 유료로 양도하는 행위는 허용되지 않습니다.

Noto Sans KR © The Noto Project Authors. SIL Open Font License 1.1 (`noto-sans-kr/OFL.txt`).
서브셋으로 다시 만든 파일도 같은 라이선스를 따르며, 글꼴 자체만 따로 판매할 수 없습니다.
