#!/usr/bin/env python3
"""news-23 b114 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"

def font(size, bold=False, serif=False):
    path = SERIF_B if serif else (SANS_B if bold else SANS)
    return ImageFont.truetype(path, size)

# palette
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (179, 0, 27)
GOLD = (212, 175, 55)
NAVY = (26, 47, 90)
TEAL = (14, 122, 107)
PURPLE = (91, 58, 142)
GREEN = (46, 125, 50)
GRAY = (102, 102, 102)
LGRAY = (238, 238, 238)
CREAM = (245, 240, 225)
DARKGREEN = (30, 107, 52)
MAPGREEN = (198, 220, 178)

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

def wrap(text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def chip(x, y, text, color):
    f = font(8, bold=True)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x, y, x + tw + 10, y + 12], radius=2, fill=color)
    d.text((x + 5, y + 1), text, font=f, fill=WHITE)
    return tw + 10

# ---------- masthead ----------
d.rectangle([0, 0, W, 56], fill=BLACK)
d.text((16, 4), "THE WORLD TODAY", font=font(44, serif=True, bold=True), fill=WHITE)
dt = "MONDAY 23 NOVEMBER 2026"
d.text((W - 16 - d.textlength(dt, font=font(15, bold=True)), 20), dt,
       font=font(15, bold=True), fill=GOLD)

# ---------- kicker ----------
d.rectangle([0, 56, W, 76], fill=RED)
kick = "AI rout hits Asia  ·  UN chief urges AI rules  ·  US lead over China at record low  ·  Anthropic IPO $107.3B"
d.text(((W - d.textlength(kick, font=font(12, bold=True))) / 2, 61), kick,
       font=font(12, bold=True), fill=WHITE)

# ---------- number strip ----------
nums = [
    ("-3.3%", "KOSPI"), ("5.3", "US-CHINA POWER GAP"), ("11,762", "EBOLA CASES, DRC"),
    ("10T won", "SEOUL STABILISATION FUND"), ("2%", "BILLIONAIRE TAX IN PARIS"),
    ("$450M", "SKUBAL DEAL"), ("165", "RUSSIAN MISSILES/WEEK"), ("12,000", "CLEARED IN MANCHESTER"),
    ("264 kg", "EXPLOSIVES SEIZED"), ("$107.3B", "ANTHROPIC IPO"),
]
for i, (v, lab) in enumerate(nums):
    col, row = i % 5, i // 5
    x = 8 + col * 204
    y = 78 + row * 26
    d.text((x, y), v, font=font(19, bold=True), fill=RED if row == 0 and col == 0 else BLACK)
    d.text((x, y + 19), lab, font=font(8), fill=GRAY)

# ---------- region bar ----------
regions = [("ASIA-PACIFIC 7", NAVY, 7), ("AMERICAS 8", RED, 8), ("MIDDLE EAST 6", TEAL, 6),
           ("EUROPE 5", PURPLE, 5), ("AFRICA 3", GREEN, 3), ("WORLD 2", (90, 90, 90), 2)]
x = 8
for label, color, cnt in regions:
    w = round(1008 * cnt / 31)
    d.rectangle([x, 132, x + w - 1, 150], fill=color)
    tw = d.textlength(label, font=font(11, bold=True))
    d.text((x + (w - tw) / 2, 136), label, font=font(11, bold=True), fill=WHITE)
    x += w

# ---------- UTC strip ----------
d.rectangle([0, 150, W, 166], fill=LGRAY)
utc = "THE DAY IN UTC  ·  ~00:00 Kospi dives  ·  ~05:30 Guterres opens  ·  ~09:00 Power Index  ·  ~12:00 Paris 2% tax  ·  ~15:00 Kyiv missiles"
d.text((10, 154), utc, font=font(10), fill=GRAY)
ap = "~ APPROX"
d.text((W - 10 - d.textlength(ap, font=font(10)), 154), ap, font=font(10), fill=GRAY)

# ---------- hero scenes ----------
SX = [8, 350, 692]
SW = 324
SY, SH = 166, 124

# scene 1: Kospi
x0 = SX[0]
d.rectangle([x0, SY, x0 + SW, SY + SH], fill=(11, 31, 58))
d.text((x0 + 10, SY + 6), "-3.3%", font=font(32, bold=True), fill=WHITE)
# buildings with lit windows, right side only (keep clear of the big number)
import random
random.seed(114)
for bx in range(x0 + 175, x0 + SW - 14, 26):
    bh = random.randint(38, 78)
    by = SY + 96 - bh
    d.rectangle([bx, by, bx + 20, SY + 96], fill=(20, 48, 84))
    for wy in range(by + 5, SY + 92, 11):
        for wx in (bx + 4, bx + 12):
            if random.random() < 0.6:
                d.rectangle([wx, wy, wx + 5, wy + 5], fill=(255, 214, 90))
# orange chart line, lower right, clear of the big number
pts = [(x0 + 150, SY + 78), (x0 + 185, SY + 70), (x0 + 215, SY + 76),
       (x0 + 245, SY + 66), (x0 + 275, SY + 72), (x0 + 305, SY + 60)]
d.line(pts, fill=(255, 140, 40), width=3)
for px, py in pts:
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=WHITE)
d.rectangle([x0, SY + SH - 18, x0 + SW, SY + SH], fill=BLACK)
d.text((x0 + 8, SY + SH - 15), "KOSPI 4,708.54  ·  -161 PTS", font=font(10, bold=True), fill=WHITE)

# scene 2: Guterres
x0 = SX[1]
d.rectangle([x0, SY, x0 + SW, SY + SH], fill=DARKGREEN)
d.text((x0 + 12, SY + 6), "150", font=font(38, bold=True), fill=GOLD)
for i, line in enumerate(["DELEGATES", "BACK A RISK", "FRAMEWORK"]):
    d.text((x0 + 12, SY + 50 + i * 20), line, font=font(18, bold=True), fill=GOLD)
# globe, right side
cx, cy, r = x0 + 262, SY + 52, 38
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 214, 168))
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(90, 160, 90), width=2)
d.ellipse([cx - 14, cy - r, cx + 14, cy + r], outline=(90, 160, 90), width=1)
d.line([cx - r, cy, cx + r, cy], fill=(90, 160, 90), width=1)
d.arc([cx - r, cy - 18, cx + r, cy + 18], 0, 360, fill=(90, 160, 90), width=1)
d.rectangle([x0, SY + SH - 18, x0 + SW, SY + SH], fill=BLACK)
d.text((x0 + 8, SY + SH - 15), "UN  ·  BRIDGETOWN", font=font(10, bold=True), fill=WHITE)

# scene 3: Power Index bars
x0 = SX[2]
d.rectangle([x0, SY, x0 + SW, SY + SH], fill=CREAM)
d.text((x0 + 10, SY + 6), "NARROWEST SINCE 2018", font=font(10, bold=True), fill=BLACK)
gap = "GAP 5.3"
d.text((x0 + SW - 10 - d.textlength(gap, font=font(12, bold=True)), SY + 5), gap,
       font=font(12, bold=True), fill=RED)
bars = [("78.9", "US", NAVY, 78.9), ("73.6", "CHINA", RED, 73.6), ("40.5", "INDIA", (176, 141, 30), 40.5)]
base = SY + 90
for i, (val, name, color, v) in enumerate(bars):
    bx = x0 + 28 + i * 104
    bh = v / 80 * 52
    d.text((bx + 28 - d.textlength(val, font=font(13, bold=True)) / 2, base - bh - 17),
           val, font=font(13, bold=True), fill=BLACK)
    d.rectangle([bx, base - bh, bx + 56, base], fill=color)
    d.text((bx + 28 - d.textlength(name, font=font(10, bold=True)) / 2, base + 3),
           name, font=font(10, bold=True), fill=BLACK)
d.rectangle([x0, SY + SH - 18, x0 + SW, SY + SH], fill=BLACK)
d.text((x0 + 8, SY + SH - 15), "ASIA POWER INDEX 2026", font=font(10, bold=True), fill=WHITE)

# ---------- hero headlines ----------
heroes = [
    ("AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE"),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS"),
    ("US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 - gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE"),
]
for i, (head, body, src) in enumerate(heroes):
    x0 = SX[i]
    hl = wrap(head, font(14, bold=True), SW - 4)
    for j, line in enumerate(hl[:2]):
        d.text((x0, 292 + j * 16), line, font=font(14, bold=True), fill=BLACK)
    bl = wrap(body, font(11), SW - 4)
    for j, line in enumerate(bl[:2]):
        d.text((x0, 322 + j * 13), line, font=font(11), fill=BLACK)
    d.text((x0, 346), src, font=font(9), fill=GRAY)
    chip(x0 + SW - 62, 344, "REPORTED", NAVY)

# ---------- MORE OF THE DAY strip ----------
d.rectangle([0, 356, W, 372], fill=BLACK)
d.text((10, 360), "MORE OF THE DAY  —  10 STORIES", font=font(12, bold=True), fill=WHITE)

# ---------- cards ----------
cards = [
    ("AMERICAS", RED, "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "WSJ", "REPORTED", NAVY),
    ("AMERICAS", RED, "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED", NAVY),
    ("WHITE HOUSE", (150, 90, 20), "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED", NAVY),
    ("MARKETS", NAVY, "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED", NAVY),
    ("SPORT", (150, 120, 20), "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED", NAVY),
    ("SPORT", (150, 120, 20), "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED", NAVY),
    ("LEGAL", PURPLE, "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED", NAVY),
    ("TECH", TEAL, "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED", NAVY),
    ("EUROPE", PURPLE, "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM", RED),
    ("SPACE", NAVY, "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM", RED),
]
for i, (cat, catc, head, body, src, chip_t, chip_c) in enumerate(cards):
    col, row = i % 5, i // 5
    x0 = 8 + col * 204
    y0 = 372 + row * 64
    d.text((x0, y0 + 4), cat, font=font(8, bold=True), fill=catc)
    num = str(i + 1)
    d.text((x0 + 198 - 8 - d.textlength(num, font=font(10, bold=True)), y0 + 3),
           num, font=font(10, bold=True), fill=RED)
    hl = wrap(head, font(11, bold=True), 192)
    for j, line in enumerate(hl[:2]):
        d.text((x0, y0 + 15 + j * 12), line, font=font(11, bold=True), fill=BLACK)
    d.text((x0, y0 + 41), body, font=font(10), fill=BLACK)
    d.text((x0, y0 + 53), src, font=font(8), fill=GRAY)
    chip(x0 + 198 - 62, y0 + 51, chip_t, chip_c)

# ---------- WHERE IT HAPPENED strip ----------
d.rectangle([0, 500, W, 518], fill=BLACK)
d.text((10, 504), "WHERE IT HAPPENED", font=font(12, bold=True), fill=WHITE)

# ---------- map ----------
def blob(points):
    d.polygon(points, fill=MAPGREEN)

blob([(20, 560), (120, 540), (160, 600), (150, 700), (110, 800), (60, 810), (25, 720), (15, 620)])
blob([(180, 560), (260, 545), (285, 580), (270, 620), (210, 630), (185, 600)])
blob([(200, 640), (260, 640), (275, 700), (250, 780), (215, 780), (195, 700)])
blob([(285, 560), (335, 555), (340, 640), (320, 700), (290, 690), (275, 620)])
blob([(285, 730), (330, 725), (335, 760), (300, 775), (282, 755)])
pins = [(315, 600), (55, 790), (325, 585), (95, 640), (120, 610), (245, 592),
        (212, 600), (195, 568), (258, 568), (185, 592), (270, 615), (255, 625), (235, 720)]
for i, (px, py) in enumerate(pins, 1):
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
    t = str(i)
    d.text((px - d.textlength(t, font=font(8, bold=True)) / 2, py - 5), t,
           font=font(8, bold=True), fill=WHITE)
legend = ["Pins 1-13:  1 Seoul  ·  2 Bridgetown  ·  3 Beijing  ·  4 Washington  ·  5 New York",
          "6 Kyiv  ·  7 Paris  ·  8 London  ·  9 Warsaw  ·  10 Manchester  ·  11 Beirut",
          "12 Gaza  ·  13 Khartoum"]
for i, line in enumerate(legend):
    d.text((16, 814 + i * 12), line, font=font(9), fill=BLACK)

# ---------- ALSO ----------
d.text((348, 522), "ALSO ON MONDAY", font=font(12, bold=True), fill=BLACK)
also_l = [
    "14. Paris: 100+ back 2% billionaire tax",
    "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week",
    "17. COP31: the day after Antalya pact rejected",
    "18. Israel unity talks resume",
    "19. Gaza: two killed in Israeli strike",
    "20. West Bank settler attacks",
    "21. Iran war: no deal in sight",
    "22. Lebanon seizes 264 kg explosives",
]
also_r = [
    "23. Bahrain: strike hits plant, 2 hurt",
    "24. Benghazi: UN demands probe [CLAIM]",
    "25. Sudan: defences down drones [CLAIM]",
    "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits in exam row",
    "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules",
    "31. Seoul readies 10T-won fund",
]
for i, line in enumerate(also_l):
    d.text((348, 542 + i * 18), line, font=font(10), fill=BLACK)
for i, line in enumerate(also_r):
    d.text((682, 542 + i * 18), line, font=font(10), fill=BLACK)
# red CLAIM markers
for (cx, cy) in [(682 + d.textlength("24. Benghazi: UN demands probe ", font=font(10)),
                  542 + 1 * 18),
                 (682 + d.textlength("25. Sudan: defences down drones ", font=font(10)),
                  542 + 2 * 18)]:
    pass  # [CLAIM] already in text; keep plain to avoid overlap

# ---------- DATE CHECK ----------
d.rectangle([8, 852, 1016, 920], outline=RED, width=2)
d.text((16, 859), "DATE CHECK  —  READ 23 NOV 2026, 23:59 UTC  —  STORIES DATED 23 NOV ONLY",
       font=font(11, bold=True), fill=RED)
d.text((16, 877), "LEFT OUT — NOT 23 NOV: Dems reach 258 (22 Nov) · Sparta II fire (22 Nov) · El Chapo Isidro captured (22 Nov) · EU–Indonesia pact (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov)",
       font=font(10), fill=BLACK)
d.text((16, 893), "NOT YET — Dymer search continues (14 missing)  ·  4 House races uncalled  ·  COP32 venue not set  ·  WHO evacuating trapped Ebola staff",
       font=font(10), fill=BLACK)

# ---------- footer ----------
d.text((16, 928), "Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · ESPN · Lowy Institute (Asia Power Index 2026).",
       font=font(9), fill=GRAY)
d.text((16, 942), "CHIPS: REPORTED = confirmed by wires · CLAIM = one side's claim, not independently confirmed · ONGOING = still developing.",
       font=font(9), fill=GRAY)
d.text((16, 956), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
       font=font(9), fill=GRAY)
foot = "THE WORLD TODAY  ·  Monday 23 November 2026  ·  31 stories  ·  6 regions"
d.text(((W - d.textlength(foot, font=font(11, bold=True))) / 2, 992), foot,
       font=font(11, bold=True), fill=(150, 110, 20))

img.save(OUT, optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
