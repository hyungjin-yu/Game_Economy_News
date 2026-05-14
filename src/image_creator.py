import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

_GRADIENTS = {
    'general':  ((10, 18, 40),  (20, 50, 120)),
    'economy':  ((10, 25, 15),  (15, 70, 40)),
    'world_it': ((25, 10, 40),  (70, 20, 110)),
}

_BADGE_LABELS = {
    'general':  'GAME DEV',
    'economy':  'ECONOMY',
    'world_it': 'WORLD IT',
}

_FONT_CANDIDATES = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-{weight}.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-{weight}.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJKkr-{weight}.otf',
]


def _load_font(bold: bool, size: int) -> ImageFont.FreeTypeFont:
    weight = 'Bold' if bold else 'Regular'
    for tmpl in _FONT_CANDIDATES:
        path = tmpl.format(weight=weight)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _draw_gradient(img: Image.Image, top: tuple, bot: tuple):
    draw = ImageDraw.Draw(img)
    H = img.height
    for y in range(H):
        t = y / H
        color = tuple(int(top[c] + (bot[c] - top[c]) * t) for c in range(3))
        draw.line([(0, y), (img.width, y)], fill=color)


def create_instagram_card(
    title: str, summary: str, source: str, category: str, output_path: str
) -> str:
    W, H, PAD = 1080, 1080, 80

    top, bot = _GRADIENTS.get(category, _GRADIENTS['general'])
    img = Image.new('RGB', (W, H))
    _draw_gradient(img, top, bot)
    draw = ImageDraw.Draw(img)

    f_badge   = _load_font(bold=True,  size=30)
    f_title   = _load_font(bold=True,  size=52)
    f_summary = _load_font(bold=False, size=34)
    f_source  = _load_font(bold=False, size=26)

    # 카테고리 배지
    badge = _BADGE_LABELS.get(category, category.upper())
    draw.text((PAD, PAD + 10), badge, font=f_badge, fill=(148, 163, 184))

    # 강조 라인
    draw.rectangle([(PAD, PAD + 58), (PAD + 56, PAD + 64)], fill=(99, 102, 241))

    # 제목 (최대 4줄)
    y = PAD + 110
    for line in textwrap.wrap(title, width=20)[:4]:
        draw.text((PAD, y), line, font=f_title, fill=(255, 255, 255))
        y += 68

    # 구분선
    y += 24
    draw.rectangle([(PAD, y), (W - PAD, y + 2)], fill=(51, 65, 85))
    y += 32

    # 요약 (최대 8줄)
    lines: list[str] = []
    for sentence in summary.replace('\n', ' ').split('. '):
        lines += textwrap.wrap(sentence.strip(), width=28)
        if len(lines) >= 8:
            break
    for line in lines[:8]:
        draw.text((PAD, y), line, font=f_summary, fill=(203, 213, 225))
        y += 50

    # 출처 푸터
    draw.text((PAD, H - PAD - 10), source, font=f_source, fill=(71, 85, 105))

    img.save(output_path, 'PNG', optimize=True)
    return output_path
