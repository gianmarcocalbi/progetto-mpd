# -*- coding: utf-8 -*-
import re
import numpy
import scipy
import json
import time
import datetime
import math
import sys
from sklearn import preprocessing 
from sklearn.metrics import confusion_matrix

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

OBS_DICT_REV = {
    0 : 'Basin',
    1 : 'Bed',
    2 : 'Cabinet',
    3 : 'Cooktop',
    4 : 'Cupboard',
    5 : 'Fridge',
    6 : 'Maindoor',
    7 : 'Microwave',
    8 : 'Seat',
    9 : 'Shower',
    10 : 'Toaster',
    11 : 'Toilet'
}

ACT_DICT = {
    'Breakfast' : 0,
    'Dinner' : 1,
    'Drink' : 2,
    'Grooming' : 3,
    "Idle/Unlabeled" : 4,
    'Leaving' : 5,
    'Lunch' : 6,
    'Showering' : 7,
    'Sleeping' : 8,
    'Snack' : 9,
    "Spare_Time/TV" : 10,
    'Toileting' : 11
}

ACT_DICT_REV = {
    0 : 'Breakfast',
    1 : 'Dinner',
    2 : 'Drink',
    3 : 'Grooming',
    4 : "Idle/Unlabeled",
    5 : 'Leaving',
    6 : 'Lunch',
    7 : 'Showering',
    8 : 'Sleeping',
    9 : 'Snack',
    10 : "Spare_Time/TV",
    11 : 'Toileting'
}

    
def DecimalTo12bitArray(dec):
    return list(map(int, list(bin(dec)[2:].zfill(12))))