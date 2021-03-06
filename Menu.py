# -*- coding: utf-8 -*-

import pygame
import os
import sys
from functions import *
from color import *
from pygame.locals import *
from game import Application
from Sound import Sound
from Buttons import Button
pygame.init()


class Menu(pygame.sprite.Sprite):
    def __init__(self, width, height):
        # We create the window
        self.width = width
        self.height = height
        FULLSCREEN = 0
        self.dimension = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.dimension,  FULLSCREEN, 32)
        pygame.display.set_caption("TuxleTriad")

        elemText = ["Play", "Options", "Rules", "About", "Quit Game"]
        self.menu = []
        for elem in elemText:
            self.menu.append(Button(elem, "Dearest.ttf", white))

        posx = 400
        posy = 400 - (60 * len(elemText))

        for elem in self.menu:
            elem.rect.center = ((posx, posy))
            posy += 100

        self.bkgrnd, self.bkgrndRect = loadImage("background.jpg")
        self.bkgrndRect = self.bkgrnd.get_rect()

        # The Clock of the game, to manage the frame-rate
        self.clock = pygame.time.Clock()
        self.fps = 60

        # We start the Sound object, playing music and sounds.
        self.sound = Sound()

        # Needed to keep track of the game if we do a pause during the game.
        self.app = None

        self.main()

    def main(self):
        pygame.event.clear()
        while 1:
            self.screen.blit(self.bkgrnd, self.bkgrndRect)
            for i in range(len(self.menu)):
                self.screen.blit(self.menu[i].surface, self.menu[i].rect)

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    self.clicked()
                elif event.type == QUIT:
                    self.quitGame()

            pygame.display.flip()
            self.clock.tick(self.fps)

    def play(self):
        """User clicked on "Play" """
        if self.app != None:
            self.app.main()
        else:
            Application(800, 600, self.screen, self.sound, self)

    def options(self):
        pygame.event.clear()
        texts = ["Audio", "Sounds", "Music", "Back"]
        length = len(texts)
        textsPos = [(320, 100), (100, 200), (100, 300), (500, 450)]
        elements = []

        for i in range(length):
            elements.append(Button(texts[i], "Dearest.ttf", white))
            elements[i].rect.topleft = textsPos[i]

        bar1, bar1Rect = loadImage("barSound.jpg")
        bar2, bar2Rect = loadImage("barSound.jpg")
        bar1Rect.topleft = (300, 220)
        bar2Rect.topleft = (300, 320)
        bars = [bar1Rect, bar2Rect]

        # X coordinates, relative to the bar's, of beginning and ending
        # of each volume cursor.
        MIN_VOLUME = 15
        MAX_VOLUME = 240

        # X absolute coordinates of the volume cursor.
        MIN = bars[0].x + MIN_VOLUME
        MAX = bars[0].x + MAX_VOLUME

        cursor1, cursor1Rect = loadImage("cursorSound.png")
        cursor2, cursor2Rect = loadImage("cursorSound.png")
        cursor1Rect.topleft = \
          (bar1Rect.x + 225 * self.sound.soundVolume, bar1Rect.y - 23)
        cursor2Rect.topleft = \
          (bar2Rect.x + 225 * self.sound.musicVolume, bar2Rect.y - 23)
        cursors = [cursor1Rect, cursor2Rect]

        while 1:
            self.screen.blit(self.bkgrnd, self.bkgrndRect)
            self.screen.blit(bar1, bar1Rect)
            self.screen.blit(bar2, bar2Rect)
            self.screen.blit(cursor1, cursors[0])
            self.screen.blit(cursor2, cursors[1])
            for i in range(length):
                self.screen.blit(elements[i].surface, elements[i].rect)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quitGame()
                elif event.type == MOUSEBUTTONDOWN:
                    mousex, mousey = pygame.mouse.get_pos()
                    for i in range(len(cursors)):
                        if cursors[i].collidepoint((mousex, mousey)):
                            while pygame.event.poll().type != MOUSEBUTTONUP:
                                mousex, mousey = pygame.mouse.get_pos()
                                if MIN <= mousex <= MAX:
                                    cursors[i].centerx = mousex
                                elif mousex > bars[i].x + MAX_VOLUME:
                                    cursors[i].centerx = bars[i].x + MAX_VOLUME
                                else:
                                    cursors[i].centerx = bars[i].x + MIN_VOLUME
                                volume = cursors[i].centerx - MIN
                                if volume != 0:
                                    volume = (volume / 2.25) / 100.0
                                assert (0.0 <= volume <= 1.0)

                                if i == 0:
                                    self.sound.soundVolume = volume
                                    self.sound.playPutCard()
                                elif i == 1:
                                    self.sound.musicVolume = volume
                                self.sound.update()

                                self.screen.blit(self.bkgrnd, self.bkgrndRect)
                                self.screen.blit(bar1, bar1Rect)
                                self.screen.blit(bar2, bar2Rect)
                                self.screen.blit(cursor1, cursors[0])
                                self.screen.blit(cursor2, cursors[1])
                                for j in range(4):
                                    self.screen.blit(elements[j].surface,\
                                                      elements[j].rect)
                                pygame.display.flip()

                    if elements[3].rect.collidepoint((mousex, mousey)):
                        self.main()

            pygame.display.update()

    def quitGame(self):
        setConfig("config.txt", self.sound.volume)
        pygame.quit()
        sys.exit()

    def clicked(self):
        for button in self.menu:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                if button.text == "Play":
                    self.play()
                elif button.text == "Options":
                    self.options()
                elif button.text == "Rules":
                    print "Rules!"
                elif button.text == "About":
                    print "About !"
                elif button.text == "Quit Game":
                    self.quitGame()

    def __repr__(self):
        return "<Menu>"

Menu(800, 600)
