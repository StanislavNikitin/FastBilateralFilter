# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
import numpy as np
import cv2

def readImage(path):
    inputImage = Image.open(path)
    grayImage = inputImage.convert('L') # 0 - 255
    grayImage.save("gray.jpg")
    #
    pix = grayImage.load() # Выгружаем значения пикселей.
    width = grayImage.size[0]
    height = grayImage.size[1]
    intMatrix = np.zeros((height, width))
    minInt = 255
    for i in range(height):
         for j in range(width):
             intensity = pix[j,i]
             intMatrix[i,j] = intensity
             if (intensity < minInt):
                 minInt = intensity
    return intMatrix, minInt


def makeImage(intMatrix, path):
    im = Image.fromarray(intMatrix)
    print im.mode
    im.convert("RGB").save(path, "PNG")


#readImage("input.jpg")

