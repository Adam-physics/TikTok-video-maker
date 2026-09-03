"""Brand constants for Trick Trivia shorts.

Colours are lifted from the book's own printed pages so the videos and the
book read as one product. Anything that can be cropped out of a real page
(the title lockup, the halftone background) is taken from the page itself
rather than re-created here.
"""

# TikTok-native canvas
WIDTH, HEIGHT, FPS = 1080, 1920, 30

# Safe area: TikTok's own UI eats the bottom ~18% and the right ~14%.
# Nothing that must be read goes inside these margins.
SAFE_TOP = 220
SAFE_BOTTOM = 420
SAFE_SIDE = 48

# Palette sampled from the book pages
ORANGE = (247, 148, 29)
ORANGE_DEEP = (238, 108, 17)
BLUE = (26, 106, 200)
BLUE_DEEP = (17, 74, 150)
GREEN = (60, 158, 46)
RED = (208, 42, 34)
YELLOW = (255, 199, 26)
INK = (16, 16, 20)
PAPER = (250, 248, 240)

# The guess timer sits in a fixed slot under the title, so its position
# does not drift when an answer panel is taller than a claim panel.
TIMER_X, TIMER_Y = 90, 384
TIMER_W, TIMER_H = 900, 22

# Panel presentation
PANEL_WIDTH = 1004          # leaves a 38px brand border either side
PANEL_RADIUS = 26
PANEL_SHADOW = 18

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

# Beat sheet (seconds). Tuned for a ~32s round: long enough to actually
# guess, short enough that the loop still counts as a full watch.
T_CLAIM = 4.4               # per claim, while the guess timer runs
T_LOCK = 1.3                # "lock in your guess" beat
T_ANSWER = 3.6              # per reveal
T_ENDCARD = 2.6
