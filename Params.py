# -*- coding: utf-8 -*-

# FILEINFO: for downloading data from kff
# OPSTART: for history size, unit: day
FILEINFO = {
    "TEXT": {"wx": "", "file": "ad_text.txt"},
    "OTHER": {"wx": "", "file": "user_other.txt"},
    "VIEW": {"wx": "", "file": "user_view.txt"}
}

OPTSTART = {
    "TEXT": -150,
    "OTHER": -120,
    "VIEW": -90
}

TAG = "tag.txt"

ADTAG = "ad_tag.txt"

USERTAG = "user_tag.txt"

DATA_SOURCE_DAYGAP = -7

TAGRELATION_AD = 1
TAGRELATION_USER = 0.5


wordNum = 200

tagNum = 3000

ad_Tag = 4

user_Tag = 20
