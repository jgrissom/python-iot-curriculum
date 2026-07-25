# ============================================================
# songs.py  --  the class songbook (RTTTL strings)
# Python IoT on the TinyPICO : Session 5 (Sound & Light)
#
# Upload to the board like a library, next to rtttl.py.
#
# Everything here is public domain (long-dead composers) or
# original jingles written for this course. The internet holds
# thousands more RTTTL strings -- paste any of them in as a new
# constant and rtttl.play() will play it. (If you publish your
# copy, keep it to public-domain melodies.)
# ============================================================

# --- Course jingles (original) ----------------------------------

# The winner's fanfare -- bright rising arpeggio, lands on a high C
VICTORY = "victory:d=8,o=5,b=160:c,e,g,4c6,p,g,4c6"

# The classic "Charge!" bugle call
CHARGE = "charge:d=8,o=5,b=180:g,c6,e6,4g.6,8e6,2g6"

# Wah, wah, wah, waaah...
SAD_TROMBONE = "sadtrombone:d=4,o=5,b=90:8d#,8d,8c#,2c"

# An octave up and back -- the parser test
SCALE = "scale:d=8,o=5,b=125:c,d,e,f,g,a,b,c6"

# --- The classics (public domain) -------------------------------

ODE_TO_JOY = ("odetojoy:d=4,o=5,b=100:e,e,f,g,g,f,e,d,c,c,d,e,e.,8d,2d,"
              "e,e,f,g,g,f,e,d,c,c,d,e,d.,8c,2c")

FUR_ELISE = ("furelise:d=8,o=5,b=125:e6,d#6,e6,d#6,e6,b,d6,c6,4a,p,c,e,a,"
             "4b,p,e,g#,b,4c6")

TWINKLE = ("twinkle:d=4,o=5,b=100:c,c,g,g,a,a,2g,f,f,e,e,d,d,2c,"
           "g,g,f,f,e,e,2d,g,g,f,f,e,e,2d")

BIRTHDAY = ("birthday:d=4,o=5,b=125:8g.,16g,a,g,c6,2b,8g.,16g,a,g,d6,2c6,"
            "8g.,16g,g6,e6,c6,b,a,8f6.,16f6,e6,c6,d6,2c6")

ENTERTAINER = ("entertainer:d=8,o=5,b=140:d,d#,e,4c6,e,4c6,e,2c6,c6,d6,d#6,"
               "e6,c6,d6,4e6,b,4d6,2c6")

# The jukebox's records (Part B) and the light organ's setlist (Part D)
ALL = [SCALE, VICTORY, CHARGE, SAD_TROMBONE, ODE_TO_JOY, FUR_ELISE,
       TWINKLE, BIRTHDAY, ENTERTAINER]
