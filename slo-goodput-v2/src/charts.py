# -*- coding: utf-8 -*-
"""图表绘制工具：坐标轴、折线、柱状、堆叠条、散点、矩阵。全部用原生形状绘制，可在 PPT 中直接编辑。"""
from deckkit import *
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR


def axes(slide, x, y, w, h, ylab=None, xlab=None, color=FAINT, lw=1.5,
         ylab_size=13, xlab_size=13):
    """L 形坐标轴，返回基线 y 坐标。"""
    hline(slide, x, y + h, w, color, lw)
    vline(slide, x, y, h, color, lw)
    if ylab:
        txt(slide, x - 1.55, y - 0.06, 1.42, 0.6, ylab, ylab_size, True, MUTED, "r", line=1.2)
    if xlab:
        txt(slide, x, y + h + 0.14, w, 0.3, xlab, xlab_size, True, MUTED, "c", line=1.0)
    return y + h


def polyline(slide, pts, color=BLUE, lw=2.75, dash=False):
    for i in range(len(pts) - 1):
        c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                                       Inches(pts[i][0]), Inches(pts[i][1]),
                                       Inches(pts[i + 1][0]), Inches(pts[i + 1][1]))
        c.line.color.rgb = RGBColor.from_string(color)
        c.line.width = Pt(lw)
        if dash:
            from pptx.oxml import parse_xml
            ln = c.line._get_or_add_ln()
            ln.append(parse_xml('<a:prstDash xmlns:a="http://schemas.openxmlformats.org/'
                                'drawingml/2006/main" val="dash"/>'))
        c.shadow.inherit = False


def curve(slide, x, y, w, h, pts01, color=BLUE, lw=2.75, dash=False):
    """pts01: [(fx, fy)]，fx 左→右 0..1，fy 0=底部 1=顶部。"""
    p = [(x + fx * w, y + h - fy * h) for fx, fy in pts01]
    polyline(slide, p, color, lw, dash)
    return p


def dot(slide, cx, cy, r=0.09, fill=WHITE, line=BLUE, lw=2.25):
    return shape(slide, MSO_SHAPE.OVAL, cx - r, cy - r, r * 2, r * 2, fill, line, lw)


def vbar_chart(slide, x, y, w, h, items, maxv=None, gapr=0.42,
               val_size=20, lab_size=15, sub_size=12, baseline=True):
    """items: [(标签, 数值, 颜色, 数值文字, 副标签)]"""
    maxv = maxv or max(i[1] for i in items) * 1.18
    n = len(items)
    bw = w / (n + (n - 1) * gapr)
    gap = bw * gapr
    if baseline:
        hline(slide, x, y + h, w, FAINT, 1.5)
    for i, it in enumerate(items):
        lab, val, col = it[0], it[1], it[2]
        vtext = it[3] if len(it) > 3 else str(val)
        sub = it[4] if len(it) > 4 else None
        bh = max(0.12, h * val / maxv)
        bx = x + i * (bw + gap)
        shape(slide, MSO_SHAPE.ROUND_2_SAME_RECTANGLE, bx, y + h - bh, bw, bh, col, None)
        txt(slide, bx - 0.2, y + h - bh - 0.44, bw + 0.4, 0.4, vtext, val_size, True, col, "c", line=1.0)
        txt(slide, bx - 0.2, y + h + 0.16, bw + 0.4, 0.34, lab, lab_size, True, INK, "c", line=1.0)
        if sub:
            txt(slide, bx - 0.3, y + h + 0.52, bw + 0.6, 0.32, sub, sub_size, False, MUTED, "c", line=1.1)
    return bw, gap


def hbar_stacked(slide, x, y, w, rows, maxv, row_h=0.5, gap=0.26, lab_w=1.75,
                 lab_size=15, seg_size=12, total_fmt=None, total_size=14):
    """rows: [(标签, [(数值, 颜色, 段内文字)], 右侧文字, 右侧颜色)]"""
    bx = x + lab_w
    bw = w - lab_w - 1.9
    yy = y
    for row in rows:
        lab, segs = row[0], row[1]
        right = row[2] if len(row) > 2 else None
        rcol = row[3] if len(row) > 3 else BODY
        txt(slide, x, yy + (row_h - 0.28) / 2, lab_w - 0.16, 0.32, lab, lab_size, True, INK, "r", line=1.0)
        cx = bx
        for seg in segs:
            v, col = seg[0], seg[1]
            stext = seg[2] if len(seg) > 2 else None
            sw = bw * v / maxv
            rect(slide, cx, yy, sw, row_h, col)
            if stext and sw > 0.55:
                txt(slide, cx, yy + (row_h - 0.24) / 2, sw, 0.28, stext, seg_size, True, WHITE, "c", line=1.0)
            cx += sw
        if right:
            txt(slide, cx + 0.16, yy + (row_h - 0.28) / 2, 1.7, 0.32, right, total_size, True, rcol, line=1.0)
        yy += row_h + gap
    return bx, bw, yy


def legend(slide, x, y, items, size=13, gap=0.22, box=0.18):
    """items: [(文字, 颜色)]，横向排列"""
    cx = x
    for t, col in items:
        rect(slide, cx, y + 0.04, box, box, col)
        tb, tf = textbox(slide, cx + box + 0.1, y - 0.02, 3.0, 0.3)
        para(tf, t, size, False, BODY, first=True, line=1.0)
        cx += box + 0.1 + _textw(t, size) + gap
    return cx


def _textw(t, size):
    """粗略估算文字宽度（英寸）：中文约 1em，西文约 0.55em。"""
    em = size / 72.0
    w = 0.0
    for ch in t:
        w += em * (1.0 if ord(ch) > 0x2000 else 0.55)
    return w


def matrix(slide, x, y, w, h, cols, rows, cells, col_size=13, row_size=15,
           cell_size=17, sub_size=11, head_h=0.72, lab_w=2.0):
    """cells[r][c] = (文字, 副文字, 底色, 字色)"""
    cw = (w - lab_w) / len(cols)
    rh = (h - head_h) / len(rows)
    for c, ct in enumerate(cols):
        txt(slide, x + lab_w + c * cw + 0.08, y, cw - 0.16, head_h - 0.1, ct,
            col_size, True, INK, "c", line=1.2)
    for r, rt in enumerate(rows):
        yy = y + head_h + r * rh
        txt(slide, x, yy + (rh - 0.3) / 2, lab_w - 0.18, 0.34, rt, row_size, True, INK, "r", line=1.0)
        for c in range(len(cols)):
            t, sub, bg, fc = cells[r][c]
            sh = card(slide, x + lab_w + c * cw + 0.06, yy + 0.05, cw - 0.12, rh - 0.1,
                      bg, None, radius=0.1)
            lines = [(t, cell_size, True, fc)]
            if sub:
                lines.append((sub, sub_size, False, fc))
            box_text(sh, lines)
    return cw, rh


def band(slide, x, y, w, h, fill=PANEL, radius=0.06):
    """图表背景板"""
    return card(slide, x, y, w, h, fill, None, radius=radius)


def tag(slide, x, y, text, size=11, fc=FAINT, fill=None):
    """图注 / 示意标记"""
    wd = _textw(text, size) + 0.3
    if fill:
        pill(slide, x, y, wd, 0.3, text, size, True, fill, fc)
    else:
        txt(slide, x, y, wd + 0.4, 0.28, text, size, False, fc, line=1.0)
    return wd
