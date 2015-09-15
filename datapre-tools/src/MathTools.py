"""
This file contains general math functions for assisting calculations
"""
import math

def degreeToRadian(degree):
    return degree * math.pi / 180.0 

def radianToDegree(radian):
    return radian / 180.0 * math.pi

def bound(val, valMin, valMax):
    res = max(val, valMin)
    res = min(res, valMax)
    return res
