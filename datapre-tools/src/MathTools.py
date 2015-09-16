"""
This file contains general math functions for assisting calculations
"""
import math

def degreeToRadian(degree):
    return degree * math.pi / 180.0 

def radianToDegree(radian):
    return radian * 180.0 / math.pi

def bound(val, valMin, valMax):
    res = max(val, valMin)
    res = min(res, valMax)
    return res

class MathTools:
    TILE_SIZE = 256.0
    ORIGIN_X = TILE_SIZE / 2.0
    ORIGIN_Y = TILE_SIZE / 2.0
    PIXELS_PER_LONGITUDE_DEGREE = TILE_SIZE / 360.0
    PIXELS_PER_LONGITUDE_RADIAN = TILE_SIZE / (2.0 * math.pi)
