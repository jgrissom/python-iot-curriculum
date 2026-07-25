# ============================================================
# songs.py  --  the class songbook (RTTTL strings)
# Python IoT on the TinyPICO : Session 5 (Sound & Light)
#
# Upload to the board like a library, next to rtttl.py.
#
# Everything here is public domain (long-dead composers, folk
# tunes, US bugle calls) or original jingles written for this
# course. The internet holds thousands more RTTTL strings --
# e.g. the PICAXE archive
# (https://picaxe.com/rtttl-ringtones-for-tune-command/, ~11,000
# songs) or just search "RTTTL <song name>". Paste any of them in
# as a new constant and rtttl.play() will play it. (If you publish
# your copy, keep it to public-domain melodies -- most famous
# themes are under copyright until roughly a century after
# publication.)
#
# Longer classical pieces are opening-phrase transcriptions, not
# complete works -- enough to be unmistakable on a piezo.
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

# --- Game-show cues (short, functional) -------------------------

# US Army bugle call -- "you've got to get up" (round-start cue)
REVEILLE = ("reveille:d=8,o=5,b=140:c,e,c,g4,c,e,c,g4,c,e,c,e,4g,"
            "e,c,e,c,g4,c,e,c,g4,4c")

# The dignified loss -- same register as SAD_TROMBONE, opposite mood
TAPS = ("taps:d=4,o=5,b=60:8g4.,16g4,2c,8g4.,16c,2e,8g4.,16c,e,"
        "8g4.,16c,e,8g4.,16c,2e.,8c.,16e,2g,8e.,16c,2g4,8g4.,16g4,2c.")

# Chopin, Piano Sonata No. 2 -- the cartoon game-over
FUNERAL_MARCH = ("funeralmarch:d=4,o=5,b=70:c,8c.,16c,c,d#,8d.,16d,"
                 "8d,8c,8c.,16b4,2c")

# R. Strauss, Also sprach Zarathustra -- maximal victory (match point!)
ZARATHUSTRA = ("zarathustra:d=4,o=5,b=100:2c,2g,2c.6,8p,1e6,8p,"
               "8c,8g4,8c,8g4,8c,8g4,4c")

# --- Classics that shine on a piezo -----------------------------

ODE_TO_JOY = ("odetojoy:d=4,o=5,b=100:e,e,f,g,g,f,e,d,c,c,d,e,e.,8d,2d,"
              "e,e,f,g,g,f,e,d,c,c,d,e,d.,8c,2c")

FUR_ELISE = ("furelise:d=8,o=5,b=125:e6,d#6,e6,d#6,e6,b,d6,c6,4a,p,c,e,a,"
             "4b,p,e,g#,b,4c6")

ENTERTAINER = ("entertainer:d=8,o=5,b=140:d,d#,e,4c6,e,4c6,e,2c6,c6,d6,d#6,"
               "e6,c6,d6,4e6,b,4d6,2c6")

# Grieg -- try it, then double b= and run it again; it WANTS to accelerate
MOUNTAIN_KING = ("mountainking:d=8,o=5,b=120:a4,b4,c,d,e,c,4e,d#,b4,4d#,"
                 "d,b4,4d,a4,b4,c,d,e,c,e,a,4g,e,c,e,2g")

# Mozart, Rondo alla Turca -- fast, high, and shockingly good on a piezo
TURKISH_MARCH = ("turkishmarch:d=16,o=5,b=120:b,a,g#,a,8c6,p,d6,c6,b,c6,"
                 "8e6,p,f6,e6,d#6,e6,b6,a6,g#6,a6,b6,a6,g#6,a6,4c7")

# Bach, Toccata in D minor -- the organ flourish, two octaves of drama
TOCCATA = ("toccata:d=16,o=6,b=90:a,g,2a,4p,g,f,e,d,8c#,2d,4p,"
           "a5,g5,2a5,4p,g5,f5,e5,d5,8c#5,2d5")

# Beethoven's Fifth -- starts on a REST: the canonical test of 'p' handling
BEETHOVEN5 = "beethoven5:d=8,o=5,b=100:p,g,g,g,2d#,p,f,f,f,2d"

# Rossini, William Tell finale -- the gallop ("...and they're off!")
WILLIAM_TELL = ("williamtell:d=16,o=5,b=180:c,c,8c,c,c,8c,c,c,8e,8g,8g,8e,"
                "8c,8e,8g,8e,4c6,8p,c,c,8c,c,c,8c,c,c,8e,8g,8g,8e,"
                "8c,8e,8d,8d,4c")

# Bizet, Carmen -- the chromatic descent; a workout for sharps
HABANERA = "habanera:d=8,o=5,b=100:4d.6,c#6,c6,4b,16b,16b,c6,b,a,2g#"

# --- Singalong tier (debug by ear -- everyone knows these) ------

JINGLE_BELLS = ("jinglebells:d=8,o=5,b=140:e,e,4e,e,e,4e,e,g,c,d,2e,"
                "f,f,f,f,f,e,e,16e,16e,e,d,d,e,4d,4g,"
                "e,e,4e,e,e,4e,e,g,c,d,2e,"
                "f,f,f,f,f,e,e,16e,16e,g,g,f,d,2c")

FRERE_JACQUES = ("frerejacques:d=4,o=5,b=125:c,d,e,c,c,d,e,c,e,f,2g,e,f,2g,"
                 "8g,8a,8g,8f,e,c,8g,8a,8g,8f,e,c,c,g4,2c,c,g4,2c")

MARY_LAMB = ("marylamb:d=4,o=5,b=125:e,d,c,d,e,e,2e,d,d,2d,e,g,2g,"
             "e,d,c,d,e,e,e,e,d,d,e,d,2c")

YANKEE_DOODLE = ("yankeedoodle:d=8,o=5,b=140:c,c,d,e,c,e,4d,g4,"
                 "c,c,d,e,2c,4b4,c,c,d,e,f,e,d,c,b4,g4,a4,b4,4c,4c")

OH_SUSANNA = ("ohsusanna:d=8,o=5,b=140:c,d,e,g,4g.,a,4g,4e,4c,d,e,e,4d,4c,2d,"
              "c,d,e,g,4g.,a,4g,4e,4c,d,e,e,4d,4d,2c")

SAINTS = ("saints:d=4,o=5,b=125:8c,8e,8f,2g,8p,8c,8e,8f,2g,8p,"
          "8c,8e,8f,g,e,c,e,2d,8p,e,d,c,2c,e,g,2g.,f,e,f,g,e,c,d,2c")

BALLGAME = "ballgame:d=4,o=5,b=170:c,c6,a,g,e,2g.,2d.,c,c6,a,g,e,2g."

BIRTHDAY = ("birthday:d=4,o=5,b=125:8g.,16g,a,g,c6,2b,8g.,16g,a,g,d6,2c6,"
            "8g.,16g,g6,e6,c6,b,a,8f6.,16f6,e6,c6,d6,2c6")

TWINKLE = ("twinkle:d=4,o=5,b=100:c,c,g,g,a,a,2g,f,f,e,e,d,d,2c,"
           "g,g,f,f,e,e,2d,g,g,f,f,e,e,2d")

# --- The sly one ------------------------------------------------

# 19th-century Russian folk song. Everyone will call it something else.
KOROBEINIKI = ("korobeiniki:d=8,o=5,b=140:4e,b4,c,4d,c,b4,4a4,a4,c,4e,d,c,"
               "4b4,c,4d,4e,4c,4a4,4a4,4p,"
               "4d,f,4a,g,f,4e,c,4e,d,c,4b4,b4,c,4d,4e,4c,4a4,4a4")

# --- Stress test ------------------------------------------------

# Rimsky-Korsakov -- a chromatic phrase; the parser-and-timing torture test
BUMBLEBEE = ("bumblebee:d=16,o=6,b=140:e,d#,d,c#,c,b5,a#5,a5,g#5,a5,a#5,b5,"
             "c,c#,d,d#,e,d#,d,c#,c,b5,a#5,a5,g#5,g5,f#5,f5,e5,"
             "f5,f#5,g5,g#5,a5,a#5,b5")

# The jukebox's records (Part B) and the light organ's setlist (Part D)
ALL = [SCALE, VICTORY, CHARGE, SAD_TROMBONE, REVEILLE, TAPS, FUNERAL_MARCH,
       ZARATHUSTRA, ODE_TO_JOY, FUR_ELISE, ENTERTAINER, MOUNTAIN_KING,
       TURKISH_MARCH, TOCCATA, BEETHOVEN5, WILLIAM_TELL, HABANERA,
       JINGLE_BELLS, FRERE_JACQUES, MARY_LAMB, YANKEE_DOODLE, OH_SUSANNA,
       SAINTS, BALLGAME, BIRTHDAY, TWINKLE, KOROBEINIKI, BUMBLEBEE]
