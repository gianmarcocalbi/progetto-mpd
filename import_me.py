import re
import numpy
import scipy
import json
import time
import datetime
import math
import sys

ACT_DICT = {
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