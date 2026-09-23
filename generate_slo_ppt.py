from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.dml.color import RGBColor
from pptx.oxml.xmlchemy import OxmlElement
from pptx.oxml.ns import qn

# ── Presentation setup ───────────────────────────────────────────────────────
prs = Presentation()
prs.slide_width = Inches(13.333333)
prs.slide_height = Inches(7.5)
prs.core_properties.title = "Inference SLO：从延迟指标到 Goodput 优化"
prs.core_properties.subject = "LLM 推理系统 SLO 技术分享"
prs.core_properties.author = "Kiro"
prs.core_properties.keywords = "LLM, SLO, TTFT, TPOT, Goodput, PD, KV Cache"
BLANK = prs.slide_layouts[6]

# Canvas 13.333 × 7.5; units are inches
C = {
    "bg": "F8FAFC", "paper": "FFFFFF", "navy": "19324A", "ink": "27445F",
    "muted": "708297", "line": "D9E4EC", "mint": "DDF4ED", "teal": "20A38B",
    "teal_dark": "087A68", "sky": "E7F1FF", "blue": "3478C7", "coral": "FFE2D9",
    "orange": "ED7955", "yellow": "FFF4CC", "gold": "D59B22", "lav": "EFEAFF",
    "purple": "7257B8", "slate": "EDF2F6", "dark_bg": "132A3A",
}
FONT = "Noto Sans CJK SC"
FONT_FALLBACK = "Arial"


def rgb(key):
    v = C.get(key, key).replace('#','')
    return RGBColor.from_string(v)


def add_rect(slide, x, y, w, h, fill="paper", line=None, radius=True, transparency=0):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
                                 Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = rgb(fill)
    if transparency:
        shp.fill.transparency = transparency
    if line:
        shp.line.color.rgb = rgb(line); shp.line.width = Pt(0.8)
    else:
        shp.line.fill.background()
    # modest rounded corners look more editorial than pill shapes
    return shp


def add_line(slide, x1, y1, x2, y2, color="line", width=1.1, arrow=False):
    ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    ln.line.color.rgb = rgb(color); ln.line.width = Pt(width)
    if arrow:
        # add arrow tail through XML because python-pptx has no public API
        spPr = ln._element.spPr
        ln_el = spPr.find(qn('a:ln'))
        tail = OxmlElement('a:tailEnd')
        tail.set('type', 'triangle')
        ln_el.append(tail)
    return ln


def add_text(slide, text, x, y, w, h, size=16, color="ink", bold=False, align=PP_ALIGN.LEFT,
             valign=MSO_ANCHOR.TOP, font=FONT, margin=0.03, italic=False, bullet=False):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear(); tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(margin)
    tf.margin_top = tf.margin_bottom = Inches(margin)
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    p.alignment = align
    p.space_after = Pt(0)
    run = p.add_run(); run.text = text
    run.font.name = font; run.font.size = Pt(size); run.font.bold = bold; run.font.italic = italic
    run.font.color.rgb = rgb(color)
    if bullet:
        p.level = 0
    return box


def add_label(slide, text, x, y, w=None, fill="mint", color="teal_dark"):
    if w is None: w = max(0.75, len(text)*0.20+0.32)
    add_rect(slide, x, y, w, 0.31, fill=fill, radius=True)
    add_text(slide, text, x, y+0.028, w, 0.23, size=8.7, color=color, bold=True, align=PP_ALIGN.CENTER)


def title(slide, section, headline, kicker=None, dark=False):
    if dark:
        bg = add_rect(slide, 0, 0, 13.333, 7.5, "dark_bg", radius=False)
        sec_color, head_color, line_color = "mint", "paper", "teal"
    else:
        add_rect(slide, 0, 0, 13.333, 7.5, "bg", radius=False)
        sec_color, head_color, line_color = "teal_dark", "navy", "teal"
    add_text(slide, section.upper(), 0.62, 0.38, 2.5, 0.24, size=8.5, color=sec_color, bold=True)
    add_rect(slide, 0.62, 0.75, 0.44, 0.045, line_color, radius=False)
    add_text(slide, headline, 0.62, 0.93, 11.9, 0.58, size=27, color=head_color, bold=True)
    if kicker:
        add_text(slide, kicker, 0.64, 1.60, 11.5, 0.38, size=12, color="muted" if not dark else "D2DFE5")


def footer(slide, n, source=None, dark=False):
    color = "B5C3CD" if dark else "9AABB8"
    add_text(slide, "LLM INFERENCE SLO  /  INTERNAL EXPLAINER", 0.62, 7.12, 4.7, 0.16, size=6.8, color=color, bold=True)
    if source:
        add_text(slide, source, 5.0, 7.105, 6.7, 0.18, size=6.6, color=color, align=PP_ALIGN.RIGHT)
    add_text(slide, f"{n:02d}", 12.22, 7.07, 0.45, 0.2, size=8, color=color, bold=True, align=PP_ALIGN.RIGHT)


def circle(slide, x, y, d, fill, text=None, tcolor="navy", size=14):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    shp.fill.solid(); shp.fill.fore_color.rgb = rgb(fill); shp.line.fill.background()
    if text:
        add_text(slide, text, x, y+d*0.27, d, d*0.38, size=size, color=tcolor, bold=True, align=PP_ALIGN.CENTER)
    return shp


def icon_dot(slide, x, y, color="teal", d=0.11):
    circle(slide, x, y, d, color)


def metric_card(slide, x, y, w, h, value, unit, label, desc, accent="teal"):
    add_rect(slide, x, y, w, h, "paper", line="line")
    add_rect(slide, x, y, 0.06, h, accent, radius=False)
    add_text(slide, value, x+0.28, y+0.23, w-0.5, 0.43, size=26, color="navy", bold=True)
    add_text(slide, unit, x+0.31, y+0.70, w-0.55, 0.22, size=10, color=accent, bold=True)
    add_text(slide, label, x+0.28, y+1.10, w-0.5, 0.25, size=13, color="ink", bold=True)
    add_text(slide, desc, x+0.28, y+1.48, w-0.50, h-1.65, size=10.5, color="muted")


def process_box(slide, x, y, w, h, label, caption, fill="paper", accent="teal"):
    add_rect(slide, x, y, w, h, fill=fill, line="line")
    circle(slide, x+0.22, y+0.22, 0.32, accent)
    add_text(slide, label, x+0.67, y+0.21, w-0.88, 0.30, size=12.5, color="navy", bold=True)
    add_text(slide, caption, x+0.22, y+0.70, w-0.44, h-0.85, size=9.7, color="muted")


def arrow_between(slide, x1, y, x2, color="teal"):
    add_line(slide, x1, y, x2, y, color=color, width=1.6)
    # triangle head pointing right
    tri = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(x2-0.13), Inches(y-0.07), Inches(0.17), Inches(0.14))
    tri.fill.solid(); tri.fill.fore_color.rgb = rgb(color); tri.line.fill.background()


# ── 01 Cover ─────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
add_rect(s,0,0,13.333,7.5,"bg",radius=False)
# Architectural background composition
add_rect(s,8.72,0,4.61,7.5,"mint",radius=False)
add_rect(s,10.25,0,3.08,7.5,"sky",radius=False)
circle(s,9.18,1.02,2.18,"paper")
circle(s,10.50,2.52,2.80,"coral")
circle(s,8.08,4.65,2.05,"teal")
circle(s,11.44,5.27,1.18,"yellow")
add_line(s,8.22,1.15,11.66,5.75,"navy",1.1)
add_line(s,7.9,5.44,11.87,1.59,"teal",1.1)
add_label(s,"内部技术分享",0.70,0.72,1.25,fill="mint")
add_text(s,"Inference SLO",0.70,1.43,7.1,0.66,size=39,color="navy",bold=True)
add_text(s,"从延迟指标到\nGoodput 优化",0.70,2.18,7.2,1.32,size=33,color="navy",bold=True)
add_text(s,"用用户体验语言，建立对推理系统优化工作的共同理解",0.73,3.79,6.75,0.32,size=14,color="muted")
add_rect(s,0.70,4.46,6.52,0.02,"line",radius=False)
add_text(s,"TTFT  ·  TPOT  ·  队列  ·  KV Cache  ·  调度  ·  PD 架构",0.73,4.72,6.7,0.27,size=11,color="teal_dark",bold=True)
add_text(s,"面向：希望理解优化“为什么做、影响什么、如何取舍”的团队成员",0.73,6.58,6.5,0.27,size=9.6,color="muted")
footer(s,1)

# ── 02 Agenda ────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
title(s,"阅读路径","先建立同一张“推理体验地图”","不从术语出发，而从用户能感受到的等待与流畅出发。")
steps=[("01","为什么需要 SLO","从“机器跑得快”到“用户体验可承诺”","mint","teal_dark"),
       ("02","TTFT 与 TPOT","一次回答的两个关键体验时刻","sky","blue"),
       ("03","延迟从哪里来","队列、计算、KV、通信与干扰","coral","orange"),
       ("04","系统如何控制","架构、调度、执行、内存、网络","lav","purple"),
       ("05","最终优化目标","在约束下最大化 Goodput","yellow","gold")]
for i,(num,hd,ds,fill,ac) in enumerate(steps):
    x=0.75+i*2.50
    add_rect(s,x,2.42,2.12,2.62,fill=fill,line=None)
    add_text(s,num,x+0.18,2.68,0.5,0.3,size=10,color=ac,bold=True)
    add_text(s,hd,x+0.18,3.18,1.76,0.52,size=15,color="navy",bold=True)
    add_text(s,ds,x+0.18,4.06,1.70,0.60,size=9.6,color="ink")
    if i<4: arrow_between(s,x+2.17,3.72,x+2.42,"muted")
add_text(s,"这份分享的结论：所有底层优化，最终都应回到 TTFT / TPOT 以及 Goodput。",0.77,5.72,11.8,0.35,size=16,color="navy",bold=True,align=PP_ALIGN.CENTER)
footer(s,2)

# ── 03 Why SLO ───────────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
title(s,"01 / WHY SLO","真正要优化的，不只是“跑得更快”","在线服务的成功标准，是体验达标前提下能够稳定服务多少用户。")
# left throughput chart-ish
add_rect(s,0.72,2.18,5.73,3.95,"paper",line="line")
add_text(s,"传统性能视角",1.03,2.52,2.5,0.27,size=12,color="muted",bold=True)
for i,(lab,val,col) in enumerate([("Tokens/s",0.84,"teal"),("GPU 利用率",0.68,"blue"),("平均延迟",0.55,"orange")]):
    y=3.08+i*0.70
    add_text(s,lab,1.03,y,1.35,0.22,size=10.5,color="ink",bold=True)
    add_rect(s,2.57,y+0.02,2.80,0.22,"slate")
    add_rect(s,2.57,y+0.02,2.80*val,0.22,col)
    add_text(s,f"{int(val*100)}",5.55,y-0.03,0.42,0.24,size=9,color="muted",align=PP_ALIGN.RIGHT)
add_text(s,"这些指标很重要，但它们不直接回答：\n用户是否感觉“及时、连续、不卡顿”？",1.03,5.40,4.82,0.45,size=11,color="muted")
# right user value
add_rect(s,6.82,2.18,5.78,3.95,"navy",radius=True)
add_text(s,"SLO 视角",7.14,2.52,2.5,0.27,size=12,color="mint",bold=True)
add_text(s,"在体验约束下\n持续服务更多请求",7.14,3.06,4.85,0.86,size=23,color="paper",bold=True)
add_line(s,7.16,4.18,12.05,4.18,"teal",1.2)
for i,(lab,desc) in enumerate([("TTFT","第一次看到回答的等待"),("TPOT","后续内容出现的节奏"),("Goodput","两者都达标的实际服务量")]):
    y=4.48+i*0.45
    icon_dot(s,7.18,y+0.04,"teal",0.1)
    add_text(s,lab,7.43,y,0.86,0.22,size=10.3,color="paper",bold=True)
    add_text(s,desc,8.36,y,3.45,0.22,size=10.3,color="D2DFE5")
add_text(s,"从 Performance → SLO Attainment → Goodput",0.78,6.47,11.6,0.35,size=16,color="teal_dark",bold=True,align=PP_ALIGN.CENTER)
footer(s,3)

# ── 04 SLA SLO SLI ───────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
title(s,"01 / WHY SLO","SLA、SLO、SLI：三个词，一条闭环","把承诺、目标和实际测量分开，才能让性能讨论可执行。")
items=[("SLA","对外承诺","服务在什么范围内应达到怎样的体验","纸面上的服务等级协议","sky","blue"),
       ("SLO","内部目标","我们为用户体验设置的可衡量阈值","例如：TTFT、TPOT 的目标线","mint","teal_dark"),
       ("SLI","实际指标","系统真实运行时采集到的表现","例如：p95 TTFT、SLO 达成率","coral","orange")]
for i,(tag,hd,ds,ex,fill,ac) in enumerate(items):
    x=0.82+i*4.17
    add_rect(s,x,2.35,3.57,3.52,fill=fill)
    add_label(s,tag,x+0.24,2.66,0.63,fill="paper",color=ac)
    add_text(s,hd,x+0.24,3.18,2.8,0.36,size=19,color="navy",bold=True)
    add_text(s,ds,x+0.24,3.85,2.95,0.55,size=11,color="ink")
    add_rect(s,x+0.24,4.74,3.09,0.02,ac,radius=False)
    add_text(s,ex,x+0.24,4.98,2.95,0.45,size=10,color="muted")
    if i<2: arrow_between(s,x+3.61,4.1,x+3.95,"muted")
add_text(s,"共同语言的价值：每次优化，都可以明确回答“影响的是承诺、目标，还是实际测量？”",0.85,6.37,11.7,0.32,size=13,color="navy",bold=True,align=PP_ALIGN.CENTER)
footer(s,4)

# ── 05 Two SLOs ──────────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
title(s,"02 / THE TWO MOMENTS","一次 LLM 回答，用户会经历两个“等待时刻”","先看到第一个 token，再持续看到后续 token。两种体验由不同系统行为决定。")
# timeline
add_text(s,"用户发出请求",0.85,3.03,1.35,0.25,size=11,color="muted",bold=True)
circle(s,2.02,2.91,0.28,"navy")
add_line(s,2.30,3.05,11.2,3.05,"line",2.0)
# prefill zone
add_rect(s,2.55,2.54,3.27,1.03,"sky")
add_text(s,"PREFILL",2.79,2.73,1.05,0.22,size=9,color="blue",bold=True)
add_text(s,"理解整段 Prompt，生成 KV Cache",2.79,3.00,2.65,0.24,size=10.6,color="navy",bold=True)
# TTFT marker
circle(s,5.62,2.84,0.43,"teal")
add_text(s,"首 token",5.43,3.70,0.85,0.23,size=10,color="teal_dark",bold=True,align=PP_ALIGN.CENTER)
add_line(s,5.835,3.31,5.835,3.63,"teal",1.2)
# decode
add_rect(s,6.34,2.54,4.84,1.03,"mint")
add_text(s,"DECODE",6.60,2.73,1.05,0.22,size=9,color="teal_dark",bold=True)
for i in range(7):
    circle(s,7.02+i*0.51,3.04,0.16,"teal")
add_text(s,"一个 token 接一个 token 地生成",6.60,3.01,2.9,0.24,size=10.6,color="navy",bold=True)
# callouts
add_rect(s,1.05,4.63,5.28,1.26,"paper",line="line")
add_label(s,"TTFT",1.30,4.90,0.68,fill="sky",color="blue")
add_text(s,"Time To First Token",2.12,4.91,2.5,0.22,size=12,color="navy",bold=True)
add_text(s,"“我多久能看到系统开始回答？”",1.30,5.30,4.45,0.25,size=10.8,color="muted")
add_rect(s,6.83,4.63,5.28,1.26,"paper",line="line")
add_label(s,"TPOT",7.08,4.90,0.68,fill="mint",color="teal_dark")
add_text(s,"Time Per Output Token",7.90,4.91,2.5,0.22,size=12,color="navy",bold=True)
add_text(s,"“内容是否以稳定、流畅的节奏出现？”",7.08,5.30,4.48,0.25,size=10.8,color="muted")
footer(s,5)

# ── 06 Definitions ───────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
title(s,"02 / THE TWO MOMENTS","TTFT 与 TPOT：同一条回答里的两种度量","一个关注“开始得快不快”，一个关注“持续得顺不顺”。")
metric_card(s,0.79,2.22,5.65,3.55,"TTFT","时间","首 token 出现前的完整等待","从请求到达开始，包含排队、调度、KV 获取、Prefill、传输等步骤。","blue")
metric_card(s,6.88,2.22,5.65,3.55,"TPOT","每个 token 的时间","生成过程的平均步长","进入 Decode 后，相邻输出 token 之间的平均间隔；越稳定，阅读越流畅。","teal")
# bottom formulas conceptual
add_rect(s,0.79,6.17,11.74,0.46,"slate",radius=True)
add_text(s,"TTFT = 排队 + 调度 + KV 获取 + Prefill + 传输   ｜   TPOT ≈ Decode 总时间 ÷（输出 token 数 − 1）",1.02,6.29,11.25,0.20,size=10.5,color="ink",bold=True,align=PP_ALIGN.CENTER)
footer(s,6)

# ── 07 Tail Latency ──────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
title(s,"02 / THE TWO MOMENTS","平均值很好看，不代表体验真的达标","SLO 关注的是：有多少用户被“尾部延迟”拖慢。")
# Distribution histogram
add_rect(s,0.85,2.30,6.3,3.72,"paper",line="line")
add_text(s,"Latency distribution",1.15,2.58,2.2,0.22,size=10,color="muted",bold=True)
# axes
add_line(s,1.24,5.48,6.76,5.48,"muted",0.8)
add_line(s,1.24,3.06,1.24,5.48,"muted",0.8)
heights=[0.30,0.64,1.19,1.74,2.05,1.88,1.46,0.98,0.56,0.31,0.17,0.09]
for i,h in enumerate(heights):
    col = "teal" if i<9 else "orange"
    add_rect(s,1.52+i*0.40,5.46-h,0.26,h,col,radius=False)
# percentile lines
for x,lab,col in [(4.15,"p50","blue"),(5.55,"p95","orange"),(6.18,"p99","orange")]:
    add_line(s,x,3.06,x,5.48,col,1.0)
    add_text(s,lab,x-0.2,5.63,0.42,0.18,size=7.6,color=col,bold=True,align=PP_ALIGN.CENTER)
add_text(s,"少数慢请求，决定了用户对系统的“最坏印象”",1.14,5.72,5.4,0.20,size=9.4,color="muted")
# right
add_rect(s,7.55,2.30,4.98,3.72,"navy")
add_text(s,"SLO attainment",7.89,2.65,2.4,0.22,size=10,color="mint",bold=True)
add_text(s,"达标的请求数\n÷ 总请求数",7.89,3.20,3.4,0.70,size=22,color="paper",bold=True)
add_line(s,7.89,4.18,12.13,4.18,"teal",1.0)
for y,text in [(4.47,"观察 p50，知道典型体验"),(4.84,"观察 p95 / p99，发现尾部风险"),(5.21,"按上下文长度分桶，避免长请求被掩盖")]:
    icon_dot(s,7.91,y+0.04,"teal",0.10)
    add_text(s,text,8.17,y,3.73,0.22,size=9.4,color="DCE7EC")
add_text(s,"讨论 SLO 时，先问：“我们在看平均值，还是在看真正不达标的人数？”",0.92,6.44,11.5,0.28,size=13,color="navy",bold=True,align=PP_ALIGN.CENTER)
footer(s,7)

# ── 08 Goodput ───────────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
title(s,"02 / THE TWO MOMENTS","Goodput：满足体验约束后的“有效服务量”","吞吐最高，不一定等于用户体验最好；真正有效的是同时满足两个 SLO 的请求。")
# Formula center
add_rect(s,0.84,2.15,11.62,1.12,"navy")
add_text(s,"Goodput  =  在 TTFT 与 TPOT 都达标的前提下，单位时间内成功服务的请求数",1.10,2.52,11.08,0.33,size=17,color="paper",bold=True,align=PP_ALIGN.CENTER)
# Flow
nodes=[("吞吐提升","GPU 更忙","sky","blue"),("资源更满","排队 / 干扰增加","coral","orange"),("体验波动","SLO 达成率下降","yellow","gold"),("有效服务量","Goodput 可能下降","mint","teal_dark")]
for i,(hd,ds,fill,ac) in enumerate(nodes):
    x=0.78+i*3.10
    add_rect(s,x,4.08,2.55,1.35,fill)
    add_text(s,hd,x+0.18,4.34,2.17,0.24,size=12.6,color="navy",bold=True,align=PP_ALIGN.CENTER)
    add_text(s,ds,x+0.18,4.80,2.17,0.25,size=9.4,color="ink",align=PP_ALIGN.CENTER)
    if i<3: arrow_between(s,x+2.60,4.76,x+2.98,"muted")
add_text(s,"核心判断：不是“设备忙不忙”，而是“用户体验达标的请求有多少”。",0.94,6.15,11.4,0.31,size=14,color="teal_dark",bold=True,align=PP_ALIGN.CENTER)
footer(s,8)

# ── 09 TTFT breakdown ────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
title(s,"03 / WHERE DELAY COMES FROM","TTFT 不是单纯的 Prefill 时间","在第一个 token 出现前，系统已完成一条完整的服务链路。")
parts=[("1","Queue","请求在队列中等待","coral","orange"),("2","Schedule","挑选何时、与谁一起执行","yellow","gold"),("3","KV Retrieval","复用或恢复既有上下文","sky","blue"),("4","Prefill","理解输入并构建 KV","mint","teal_dark"),("5","Transfer","必要的数据搬运与通信","lav","purple")]
for i,(num,hd,ds,fill,ac) in enumerate(parts):
    x=0.78+i*2.48
    add_rect(s,x,2.66,2.05,2.40,fill)
    add_label(s,num,x+0.18,2.90,0.38,fill="paper",color=ac)
    add_text(s,hd,x+0.18,3.43,1.70,0.28,size=13,color="navy",bold=True)
    add_text(s,ds,x+0.18,3.93,1.65,0.60,size=9.3,color="ink")
    if i<4: arrow_between(s,x+2.09,3.86,x+2.38,"muted")
add_rect(s,1.12,5.62,11.10,0.53,"slate")
add_text(s,"优化 TTFT 的第一步：先判断时间到底消耗在“等待”、 “计算”，还是“取数据”。",1.32,5.78,10.7,0.21,size=11.5,color="navy",bold=True,align=PP_ALIGN.CENTER)
footer(s,9)

# ── 10 Queue ─────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
title(s,"03 / WHERE DELAY COMES FROM","TTFT 的最大敌人之一：排队","当请求抵达速度超过系统服务速度，等待会首先吞噬延迟预算。")
# left arrival/queue diagram
add_text(s,"请求到达",0.95,2.51,1.2,0.22,size=11,color="muted",bold=True)
for i in range(6):
    circle(s,1.00+i*0.30,3.05+(i%2)*0.28,0.16,"blue")
add_line(s,2.95,3.24,4.17,3.24,"blue",1.5)
add_rect(s,4.29,2.56,1.32,1.32,"coral")
add_text(s,"QUEUE",4.53,2.85,0.84,0.22,size=9,color="orange",bold=True,align=PP_ALIGN.CENTER)
add_text(s,"等待",4.53,3.22,0.84,0.24,size=12,color="navy",bold=True,align=PP_ALIGN.CENTER)
add_line(s,5.69,3.24,6.48,3.24,"orange",1.5)
add_rect(s,6.60,2.56,1.59,1.32,"mint")
add_text(s,"GPU",6.93,2.85,0.92,0.22,size=9,color="teal_dark",bold=True,align=PP_ALIGN.CENTER)
add_text(s,"执行",6.93,3.22,0.92,0.24,size=12,color="navy",bold=True,align=PP_ALIGN.CENTER)
# right cards
add_rect(s,8.75,2.28,3.63,3.38,"paper",line="line")
add_text(s,"当负载提升",9.04,2.62,2.3,0.24,size=13,color="navy",bold=True)
seq=[("QPS ↑","请求来的更快"),("Queue ↑","更多请求开始等待"),("TTFT ↑","首 token 变慢"),("Violation ↑","更多请求失去达标资格")]
for i,(a,b) in enumerate(seq):
    y=3.13+i*0.53
    add_text(s,a,9.04,y,0.95,0.21,size=10,color="orange",bold=True)
    add_text(s,b,10.10,y,1.88,0.21,size=9.6,color="muted")
    if i<3: add_line(s,9.45,y+0.23,9.45,y+0.43,"line",0.9)
add_rect(s,0.93,5.42,7.30,0.59,"navy")
add_text(s,"关键提醒：TTFT 优化不能只盯着 Prefill kernel。",1.22,5.60,6.72,0.22,size=13,color="paper",bold=True,align=PP_ALIGN.CENTER)
footer(s,10)

# ── 11 KV Cache ──────────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
title(s,"03 / WHERE DELAY COMES FROM","KV Cache：复用很重要，但“命中”不等于更快","缓存要考虑放在哪里、搬回来要多久，以及请求还剩多少延迟预算。")
# cache ladder
levels=[("HBM","最近","极低延迟","mint","teal_dark"),("DRAM","较远","需要搬运","sky","blue"),("NVMe","更远","恢复成本可能很高","coral","orange"),("Miss","无缓存","需要重新 Prefill","yellow","gold")]
for i,(hd,near,desc,fill,ac) in enumerate(levels):
    x=0.92+i*3.02
    add_rect(s,x,2.44,2.55,2.26,fill)
    add_text(s,hd,x+0.20,2.79,2.15,0.30,size=17,color="navy",bold=True,align=PP_ALIGN.CENTER)
    add_text(s,near,x+0.20,3.32,2.15,0.20,size=9,color=ac,bold=True,align=PP_ALIGN.CENTER)
    add_text(s,desc,x+0.20,3.78,2.15,0.35,size=9.5,color="ink",align=PP_ALIGN.CENTER)
    if i<3: arrow_between(s,x+2.60,3.56,x+2.91,"muted")
# conclusion
add_rect(s,0.92,5.28,11.60,0.85,"paper",line="line")
add_text(s,"Cache Hit  ≠  TTFT 一定更低",1.23,5.54,3.38,0.27,size=15,color="orange",bold=True)
add_text(s,"如果从深层存储恢复 KV 的传输时间，超过了节省下来的 Prefill 计算时间，用户仍会感觉“首字很慢”。",4.36,5.53,7.55,0.30,size=10.6,color="muted")
footer(s,11)

# ── 12 TPOT ──────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
title(s,"04 / SUSTAINED GENERATION","TPOT 描述的是“内容出现的节奏”","生成阶段每多一份等待，用户都会在阅读过程中感到卡顿。")
# circular decode loop
circle(s,1.05,2.45,2.45,"mint")
add_text(s,"Decode\nStep",1.30,3.13,1.95,0.60,size=18,color="teal_dark",bold=True,align=PP_ALIGN.CENTER)
# labels around
for x,y,txt in [(3.88,2.53,"Attention\n读取 KV"),(5.90,2.53,"Linear / MoE\n计算"),(7.92,2.53,"Communication\n协同"),(9.94,2.53,"Scheduling\n下一步")]:
    add_rect(s,x,y,1.62,1.20,"paper",line="line")
    add_text(s,txt,x+0.12,y+0.31,1.38,0.50,size=10.4,color="navy",bold=True,align=PP_ALIGN.CENTER)
    if x>4: arrow_between(s,x-0.36,y+0.60,x-0.08,"muted")
arrow_between(s,3.33,3.05,3.72,"teal")
# bottom
items=[("Batch size","同一轮服务更多请求，也可能拉长单步"),("Memory bandwidth","KV 访问是 Decode 的关键成本"),("Prefill interference","抢占资源会让每一步变长"),("TP / EP 通信","网络与通信会直接传导到 TPOT")]
for i,(a,b) in enumerate(items):
    x=0.91+(i%2)*5.95; y=4.72+(i//2)*0.68
    icon_dot(s,x,y+0.04,"teal",0.10)
    add_text(s,a,x+0.22,y,1.45,0.20,size=10,color="navy",bold=True)
    add_text(s,b,x+1.65,y,3.88,0.22,size=9.6,color="muted")
footer(s,12)

# ── 13 PD aggregation ────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
title(s,"04 / SUSTAINED GENERATION","Prefill 与 Decode 同处时：资源干扰会放大 TPOT","PD Aggregation 让资源利用更紧凑，也让两个不同节奏的任务相互影响。")
# GPU panel
add_rect(s,0.88,2.30,5.18,3.70,"navy")
add_text(s,"一块 GPU 内部",1.24,2.64,2.0,0.24,size=11,color="mint",bold=True)
add_rect(s,1.27,3.20,1.92,1.85,"coral")
add_text(s,"PREFILL",1.47,3.55,1.50,0.24,size=10,color="orange",bold=True,align=PP_ALIGN.CENTER)
add_text(s,"计算密集\n批量处理输入",1.47,3.95,1.50,0.50,size=10,color="navy",bold=True,align=PP_ALIGN.CENTER)
add_rect(s,3.67,3.20,1.92,1.85,"mint")
add_text(s,"DECODE",3.88,3.55,1.50,0.24,size=10,color="teal_dark",bold=True,align=PP_ALIGN.CENTER)
add_text(s,"单步敏感\n持续产生输出",3.88,3.95,1.50,0.50,size=10,color="navy",bold=True,align=PP_ALIGN.CENTER)
add_line(s,3.19,4.12,3.67,4.12,"orange",2.0)
# Right conclusion
add_rect(s,6.55,2.30,5.90,3.70,"paper",line="line")
add_text(s,"资源竞争链路",6.90,2.66,2.0,0.25,size=12,color="navy",bold=True)
steps=[("Prefill 工作量 ↑","占用更多计算 / 调度机会"),("Decode 等待 ↑","每个生成步变慢"),("TPOT ↑","用户感到输出不连续")]
for i,(a,b) in enumerate(steps):
    y=3.25+i*0.70
    circle(s,6.93,y,0.29,"coral",str(i+1),tcolor="navy",size=9)
    add_text(s,a,7.36,y-0.01,1.85,0.22,size=10.7,color="navy",bold=True)
    add_text(s,b,9.14,y-0.01,2.64,0.22,size=9.7,color="muted")
    if i<2: add_line(s,7.07,y+0.31,7.07,y+0.55,"line",0.9)
add_text(s,"Interference intensity：Decode 期间混入多少 Prefill 工作，是理解 TPOT 波动的直观指标。",0.93,6.38,11.5,0.25,size=11.4,color="teal_dark",bold=True,align=PP_ALIGN.CENTER)
footer(s,13)

# ── 14 Chunked prefill ───────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
title(s,"04 / SUSTAINED GENERATION","Chunked Prefill：一个典型的 TTFT ↔ TPOT 旋钮","切得更大或更小，都不是绝对更好，而是在两种体验之间重新分配资源。")
# two columns
for x,hd,tag,fill,ac,blocks,lines,concl in [
    (0.86,"大 Chunk","Prefill 更连续","coral","orange",[1.45,1.45,1.45],[0.18,0.18,0.18],"TTFT 通常更好\nTPOT 风险更高"),
    (6.90,"小 Chunk","更频繁让出资源","mint","teal_dark",[0.48]*7,[0.18]*7,"TPOT 通常更稳\nTTFT 风险更高")]:
    add_rect(s,x,2.34,5.54,3.74,"paper",line="line")
    add_label(s,tag,x+0.28,2.63,1.1,fill=fill,color=ac)
    add_text(s,hd,x+0.28,3.08,2.4,0.29,size=16,color="navy",bold=True)
    yy=3.78
    cx=x+0.32
    for j,bw in enumerate(blocks):
        add_rect(s,cx,yy,bw,0.30,fill,radius=False)
        cx += bw + 0.08
        if cx>x+4.92:
            cx=x+0.32; yy+=0.44
    # decode token line
    for j in range(11):
        circle(s,x+0.40+j*0.39,5.12,0.13,"teal")
    add_text(s,concl,x+3.35,3.14,1.70,0.74,size=11.3,color=ac,bold=True,align=PP_ALIGN.CENTER)
    add_text(s,"橙 / 绿块：Prefill 工作\n绿点：Decode token",x+0.32,5.48,2.15,0.35,size=8.5,color="muted")
add_text(s,"管理原则：根据当前 SLO 压力动态选择 Chunk，而不是固定一个“最优值”。",0.86,6.44,11.7,0.26,size=12.8,color="navy",bold=True,align=PP_ALIGN.CENTER)
footer(s,14)

# ── 15 PD comparison ─────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
title(s,"05 / SYSTEM CHOICES","PD Aggregation 还是 Disaggregation？答案取决于 SLO","不是谁“更先进”，而是不同约束下，哪种结构更贴近用户体验目标。")
# header cards
for x,hd,sub,fill,ac in [(0.81,"PD Aggregation","Prefill / Decode 同资源","sky","blue"),(6.88,"PD Disaggregation","Prefill / Decode 分离资源","mint","teal_dark")]:
    add_rect(s,x,2.28,5.63,0.90,fill)
    add_text(s,hd,x+0.29,2.53,2.75,0.25,size=15,color="navy",bold=True)
    add_text(s,sub,x+3.0,2.56,2.30,0.22,size=9.5,color=ac,bold=True,align=PP_ALIGN.RIGHT)
# rows
rows=[("Prefill capacity","通常更高","需要单独配置能力"),("TTFT","通常较低","容易受队列影响"),("TPOT","可能被 Prefill 干扰","通常更稳定"),("可独立扩展","较弱","较强"),("主要风险","Decode 体验波动","Prefill 排队 / KV 转移")]
for i,(r,a,b) in enumerate(rows):
    y=3.48+i*0.49
    if i%2==0: add_rect(s,0.81,y-0.05,11.70,0.42,"paper")
    add_text(s,r,1.08,y,2.10,0.20,size=9.8,color="muted",bold=True)
    add_text(s,a,3.42,y,2.63,0.20,size=10,color="navy",align=PP_ALIGN.CENTER)
    add_line(s,6.55,y-0.07,6.55,y+0.29,"line",0.7)
    add_text(s,b,7.05,y,4.80,0.20,size=10,color="navy",align=PP_ALIGN.CENTER)
add_text(s,"结论：SLO 更紧在哪一侧，架构就更需要为哪一侧留出“呼吸空间”。",0.86,6.37,11.6,0.25,size=12.5,color="teal_dark",bold=True,align=PP_ALIGN.CENTER)
footer(s,15)

# ── 16 5 layers ──────────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
title(s,"05 / SYSTEM CHOICES","SLO 优化，不是一把扳手，而是五层控制面","每层都有控制旋钮；组合使用，才可能把体验与资源效率同时拉上来。")
layers=[("Architecture","PD mode · PD ratio","mint","teal_dark"),("Scheduling","Queue · Batch · Priority","sky","blue"),("Execution","Chunk · Kernel · Batch size","coral","orange"),("Memory","KV · Prefix cache · Offload","lav","purple"),("Communication","TP / EP · NCCL · NVLink / PCIe","yellow","gold")]
for i,(hd,ds,fill,ac) in enumerate(layers):
    y=2.22+i*0.78
    add_rect(s,1.18,y,10.95,0.58,fill)
    add_rect(s,1.18,y,2.30,0.58,ac)
    add_text(s,hd,1.45,y+0.17,1.74,0.22,size=10.8,color="paper" if ac in ["teal_dark","blue","orange","purple","gold"] else "navy",bold=True,align=PP_ALIGN.CENTER)
    add_text(s,ds,3.85,y+0.16,7.65,0.22,size=11,color="navy",bold=True)
add_text(s,"共同目标：让每一个控制旋钮都能解释为“对 TTFT、TPOT 或 SLO 达成率的影响”。",1.18,6.36,10.95,0.25,size=12.5,color="navy",bold=True,align=PP_ALIGN.CENTER)
footer(s,16)

# ── 17 Scheduling ────────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
title(s,"05 / SYSTEM CHOICES","调度：谁先服务，决定谁还有机会达标","只看“先来后到”容易堵住短请求；只看“任务大小”又可能饿死长请求。")
policies=[("FCFS","先到先服务","简单，但可能出现 Head-of-Line Blocking","slate","muted"),("SJF","短任务优先","短请求更快，长上下文可能持续被推迟","sky","blue"),("EDF","最早截止时间优先","体现 deadline，但不充分理解执行成本","yellow","gold"),("Latency Budget","剩余预算优先","优先处理“最接近失约”的请求","mint","teal_dark")]
for i,(hd,sub,ds,fill,ac) in enumerate(policies):
    x=0.82+i*3.08
    add_rect(s,x,2.38,2.62,3.20,fill)
    add_text(s,hd,x+0.20,2.73,2.20,0.30,size=15,color="navy",bold=True,align=PP_ALIGN.CENTER)
    add_text(s,sub,x+0.20,3.27,2.20,0.22,size=9.5,color=ac,bold=True,align=PP_ALIGN.CENTER)
    add_rect(s,x+0.20,3.72,2.22,0.02,ac,radius=False)
    add_text(s,ds,x+0.20,4.10,2.22,0.68,size=9.7,color="ink",align=PP_ALIGN.CENTER)
add_rect(s,1.42,6.07,10.45,0.45,"navy")
add_text(s,"Latency Budget = SLO − 预测的剩余服务时间",1.70,6.20,9.92,0.20,size=12.5,color="paper",bold=True,align=PP_ALIGN.CENTER)
footer(s,17)

# ── 18 Latency budget ────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
title(s,"05 / SYSTEM CHOICES","Latency Budget：把“还有多少时间”变成系统共同语言","同一个 KV 搬运、同一次排队，对不同请求的风险完全不同。")
# Left two requests
requests=[("Request A","TTFT SLO 5.0s","已花 1.0s","剩余 4.0s","mint","teal_dark"),("Request B","TTFT SLO 5.0s","已花 4.5s","剩余 0.5s","coral","orange")]
for i,(hd,slo,used,rem,fill,ac) in enumerate(requests):
    y=2.36+i*1.74
    add_rect(s,0.88,y,5.65,1.33,"paper",line="line")
    add_label(s,hd,1.15,y+0.23,1.12,fill=fill,color=ac)
    add_text(s,slo,2.55,y+0.24,1.72,0.22,size=10,color="muted")
    add_text(s,used,1.15,y+0.73,1.48,0.22,size=10,color="ink",bold=True)
    add_text(s,rem,3.15,y+0.68,2.70,0.30,size=16,color=ac,bold=True)
# Right decision
add_rect(s,7.05,2.36,5.38,3.07,"navy")
add_text(s,"一个 300ms 的 KV transfer",7.38,2.75,4.70,0.26,size=13,color="mint",bold=True,align=PP_ALIGN.CENTER)
add_line(s,7.50,3.28,12.02,3.28,"teal",1.0)
add_text(s,"对 Request A",7.53,3.66,1.45,0.22,size=11,color="paper",bold=True)
add_text(s,"还有足够余量，可以接受",9.11,3.66,2.53,0.22,size=10,color="D5E4E9")
add_text(s,"对 Request B",7.53,4.21,1.45,0.22,size=11,color="paper",bold=True)
add_text(s,"会显著增加违约风险，应优先处理",9.11,4.21,2.73,0.22,size=10,color="FFD7CC")
add_text(s,"因此调度、KV movement、抢占等操作，应该共同消耗并参考这个预算。",0.92,6.22,11.45,0.25,size=12.2,color="navy",bold=True,align=PP_ALIGN.CENTER)
footer(s,18)

# ── 19 engineering link ──────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
title(s,"06 / OUR ENGINEERING MAP","把正在做的工程工作，放回同一条因果链","PD、Chunk、KV、通信、GPU 利用率不是零散项目；它们都在改变用户体验。")
# causal strip
top=[("PD ratio / PD mode","架构分配","TTFT / TPOT","purple"),("Chunk size","执行切分","TTFT ↔ TPOT","orange"),("KV cache / offload","内存路径","TTFT","blue"),("TP / EP / NCCL","通信路径","TPOT","teal_dark"),("GPU utilization","资源饱和","尾部延迟","gold")]
for i,(item,kind,impact,ac) in enumerate(top):
    x=0.72+i*2.51
    add_rect(s,x,2.36,2.12,2.78,"paper",line="line")
    add_rect(s,x,2.36,2.12,0.08,ac,radius=False)
    add_text(s,item,x+0.20,2.73,1.73,0.42,size=11.2,color="navy",bold=True,align=PP_ALIGN.CENTER)
    add_text(s,kind,x+0.20,3.51,1.73,0.20,size=9.4,color="muted",align=PP_ALIGN.CENTER)
    add_rect(s,x+0.25,4.05,1.62,0.38,ac)
    add_text(s,impact,x+0.28,4.15,1.56,0.18,size=8.4,color="paper",bold=True,align=PP_ALIGN.CENTER)
    if i<4: arrow_between(s,x+2.17,3.74,x+2.40,"line")
add_text(s,"工程问题的统一问法：这个改动会让哪种延迟变短？又会把压力转移到哪里？",0.80,5.92,11.7,0.28,size=13.7,color="teal_dark",bold=True,align=PP_ALIGN.CENTER)
footer(s,19)

# ── 20 Summary ───────────────────────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
title(s,"TAKEAWAY","从单点性能，走向系统级 Goodput","推理优化的最终目标：在给定 TTFT / TPOT SLO 下，让更多请求稳定达标。",dark=True)
# central system diagram
circle(s,5.38,2.12,2.48,"teal")
add_text(s,"SLO\nATTAINMENT",5.72,2.88,1.80,0.58,size=17,color="paper",bold=True,align=PP_ALIGN.CENTER)
# surrounding
sur=[(1.05,2.56,"TTFT","首字等待","sky","blue"),(9.47,2.56,"TPOT","生成节奏","mint","teal_dark"),(2.35,5.17,"控制旋钮","架构 · 调度 · 执行","coral","orange"),(8.13,5.17,"最终目标","Goodput","yellow","gold")]
for x,y,hd,ds,fill,ac in sur:
    add_rect(s,x,y,2.62,1.00,fill)
    add_text(s,hd,x+0.13,y+0.21,2.36,0.24,size=13,color="navy",bold=True,align=PP_ALIGN.CENTER)
    add_text(s,ds,x+0.13,y+0.59,2.36,0.19,size=9.0,color="ink",align=PP_ALIGN.CENTER)
# lines
add_line(s,3.69,3.05,5.36,3.05,"teal",1.2)
add_line(s,7.86,3.05,9.43,3.05,"teal",1.2)
add_line(s,4.85,5.00,5.67,4.33,"teal",1.2)
add_line(s,7.86,4.33,8.75,5.00,"teal",1.2)
add_text(s,"不是让某个 kernel 更快，而是让更多用户在等待与生成的全过程中，都获得可承诺的体验。",0.95,6.53,11.5,0.30,size=13.2,color="paper",bold=True,align=PP_ALIGN.CENTER)
footer(s,20,source="基于团队提供的 SLO / PD / KV / 调度研读材料整理",dark=True)

# Ensure every slide has unambiguous named title shape for accessibility (hidden-ish title footer isn't needed).
out = "/projects/sandbox/LLM_Inference_SLO_Goodput_技术分享.pptx"
prs.save(out)
print(out)
print(f"slides={len(prs.slides)}")
