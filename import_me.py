import re
import numpy
import scipy
import json
import time
import datetime
import math
import sys

OBS_DICT = {
    'Basin' : 0,
    'Bed' : 1,
    'Cabinet' : 2,
    'Cooktop' : 3,
    'Cupboard' : 4,
    'Fridge' : 5,
    'Maindoor' : 6,
    'Microwave' : 7,
    'Seat' : 8,
    'Shower' : 9,
    'Toaster' : 10,
    'Toilet' : 11
}

ACT_DICT = {
    'Breakfast' : 0,
    'Dinner' : 1,
    'Grooming' : 2,
    'Leaving' : 3,
    'Lunch' : 4,
    'Showering' : 5,
    'Sleeping' : 6,
    'Snack' : 7,
    "Spare_Time/TV" : 8,
    'Toileting' : 9
}