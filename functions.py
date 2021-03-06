﻿# -*-  coding: utf-8  -*-

import pygame
import os


def loadImage(name):
    """Example:
    image, rect = loadImage("myPic.png") """

    image = pygame.image.load(os.path.join(os.getcwd(), name)).convert_alpha()
    rect = image.get_rect()
    return image, rect


def getFont(fontName, size):
    """ Example:
    fontName = getFont("font.ttf") """

    font = pygame.font.Font(os.path.join(os.getcwd(), "fonts", fontName), size)
    return font


def readFile(fileName):
    """Example:
    file = readFile("myFile.txt") """

    pathName = os.path.join(os.getcwd(), fileName)
    fileObject = open(pathName, "r")
    return fileObject.read()


def getConfig(fileContent):
    """Example:
    sound, music = getConfig(file)"""

    index = fileContent.find("=")
    index += 2
    print fileContent[index:index + 3]
    soundVolume = float(fileContent[index:index + 4])
    # From the first digit of the value to the last digit.

    index = fileContent.find("=", index + 4)
    index += 2
    musicVolume = float(fileContent[index:index + 4])

    return soundVolume, musicVolume


def setConfig(fileName, parameters):
    """Example:
    setConfig("config.txt", (sound,music)) """

    pathName = os.path.join(os.getcwd(), fileName)
    sound = parameters[0]
    music = parameters[1]
    if len(str(sound)) <= 4:
        if sound == 0:
            sound = str(sound) + ".0"
        elif sound == 1.0:
            pass
        param = str(sound)
        param = param[0:2] + "0"
        sound = param

    if len(str(music)) <= 4:
        if music == 0:
            music = str(music) + ".0"
        elif music == 1.0:
            pass
        param = str(music)
        param = param[0:2] + "0"
        music = param

    print "Sound : ", sound
    print "Music : ", music

    fileObject = open(pathName, "w")
    soundContent = "sound = " + str(sound) +\
                    "\nmusic = " + str(music)

    fileObject.write(soundContent)
    
def getCard(card):
    if card.owner == 1:
        File = os.path.join(os.getcwd(), "cards/" + card.name + "B.jpg")
        card.image = pygame.image.load(File)
    if card.owner == -1:
        File = os.path.join(os.getcwd(), "cards/" + card.name + "R.jpg")
        card.image = pygame.image.load(File)
