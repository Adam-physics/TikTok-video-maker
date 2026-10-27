"""Full-screen comic video from book page 9 (crows / elephants / shrimp), parent voice.

Claims and answers follow the printed pages (q05.png, a05.png). The page says
elephants are the only land mammal that can't jump; others can't either, so
the narration keeps to the part that is true: elephants can't jump at all.
"""
ID = "comic9"
Q, A = "q05.png", "a05.png"

SCRIPT = [
    ("Okay, this is the game my kid begs to play at dinner. Three facts, one is fake.",
     {"view": "page", "page": "q", "box": "Do crows really hold grudges against people??"}),
    ("One: Crows recognize faces and hold grudges against people who upset them.",
     {"view": "panel", "page": "q", "panel": 0}),
    ("Two: Elephants can jump one inch off the ground.",
     {"view": "panel", "page": "q", "panel": 1}),
    ("Three: A shrimp's heart is located in its head.",
     {"view": "panel", "page": "q", "panel": 2}),
    ("Lock in your guess. Three, two, one.",
     {"view": "lock", "page": "q", "box": "LOCK IN YOUR GUESS", "count": ["three", "two", "one"]}),
    ("Crows? Real. They remember faces for years, and they warn other crows about you.",
     {"view": "panel", "page": "a", "panel": 0, "stamp": ("REAL!", "real")}),
    ("Elephants? Fake! Elephants can't jump at all.",
     {"view": "panel", "page": "a", "panel": 1, "stamp": ("FAKE!", "fake")}),
    ("Shrimp? Real. A shrimp's heart sits in the head region.",
     {"view": "panel", "page": "a", "panel": 2, "stamp": ("REAL!", "real")}),
    ("It's a book called Trick Trivia, and every page is like this. It's on Amazon.",
     {"view": "end", "box": "search “Trick Trivia” on Amazon"}),
]

CAPTION = (
    "This is the game my kid begs to play at dinner. Three facts, one is fake: crows recognize "
    "faces and hold grudges, elephants can jump one inch off the ground, and a shrimp's heart is "
    "in its head. Which one got you? It's a book called Trick Trivia, every page is like this, "
    "and it's on Amazon if you want it for your own dinner table."
)
HASHTAGS = ["#realorfake", "#funfacts", "#familygame", "#dinnertable", "#momtok", "#dadtok",
            "#animalfacts"]
