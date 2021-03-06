# -*- coding: utf-8 -*-

import pygame
import sys
import random
import os
from functions import *
from color import *
from pygame.locals import *
from Card import Card
from Sound import Sound
from Hand import Hand
from Field import Field
from Score import Score
from Rules import adjacent
from listOfCards import allCards  # The list of all the cards
pygame.init()


class Application():
    """Main class of the game, manage the window"""
    def __init__(self, width, height, screen=None, soundInstance=None,
                  boss=None):
        # We create the window
        self.width = width
        self.height = height
        if screen == None:
            self.screen = pygame.display.set_mode((self.width, self.height))
        else:
            self.screen = screen

        if soundInstance == None:
            self.Sound = Sound()
        else:
            self.Sound = soundInstance
            print self.Sound.soundVolume

        self.background, self.backgroundRect = loadImage("background.jpg")

        # We keep the Menu instance if we are running TuxleTriad from Menu.py
        if boss != None:
            self.boss = boss
            self.boss.app = self
        else:
            self.boss = None

        # The Clock of the game, to manage the frame rate
        self.clock = pygame.time.Clock()
        self.fps = 60
        Cards1 = []
        Cards2 = []

        # We generate two  and draw 5 cards from each
        # to have an entire Hand of Card
        list1 = [i for i in range(len(allCards))]
        random.shuffle(list1)
        list2 = [i for i in range(len(allCards))]
        random.shuffle(list2)
        for i in range(5):
            number = list1[0]
            Cards1.append(Card(number, 1))
            list1.remove(number)
        for i in range(5):
            number = list2[0]
            Cards2.append(Card(number, -1))
            list2.remove(number)

        # We create the Hands to manage the lists of cards
        self.player1Hand = Hand(Cards1, 1)
        self.player2Hand = Hand(Cards2, -1)

        # We create the Score
        self.scorePlayer1 = Score("5", 1, self.width, self.height)
        self.scorePlayer2 = Score("5", -1, self.width, self.height)

        # With this variable, we cannot do anything until the animation
        #played is finished.
        self.animation = 0

        # If we have to play the animation in different directions
        self.sensAnimation = 0
        self.player = 1

        #self.Sound = Sound()
        self.position = None
        self.CARD = None

        # We create the field of the game, 3x3.
        sizeCard = self.player1Hand.cards[0].image.get_size()
        self.field = Field(self.width, self.height, sizeCard)
        self.alphaAnimation = 255
        self.emptyCase = 9

        # Manage the winner congratulations font
        self.winner = None
        self.winnerFont = pygame.font.Font(None, 60)

        # Manage the display of the name of the card selected
        self.cardFont = pygame.font.Font(None, 40)
        self.cardFontSurf = None

        # Manage the background for the name of the card selected
        self.backCard, self.backCardRect = loadImage("name.png")

        self.main()

    def update(self):
        self.screen.blit(self.background, self.background.get_rect())
        for card in self.player1Hand.cards:
            self.screen.blit(card.image, card.rect)
            if card == self.CARD:
                name = self.CARD.name
                self.cardFontSurf = self.cardFont.render(name, True, white)
                self.cardFontRect = self.cardFontSurf.get_rect()
                self.cardFontRect.midbottom = self.backgroundRect.midbottom
                self.cardFontRect.y -= 10
                self.backCardRect.center = self.cardFontRect.center
                self.backCardRect.centery -= 0

        for card in self.player2Hand.cards:
            if card == self.CARD:
                name = self.CARD.name
                self.cardFontSurf = self.cardFont.render(name, True, white)
                self.cardFontRect = self.cardFontSurf.get_rect()
                self.cardFontRect.midbottom = self.backgroundRect.midbottom
                self.cardFontRect.y -= 10
            self.screen.blit(card.image, card.rect)

        self.scorePlayer1.update()
        self.scorePlayer2.update()
        self.screen.blit(self.scorePlayer1.surface, self.scorePlayer1.rect)
        self.screen.blit(self.scorePlayer2.surface, self.scorePlayer2.rect)
        if self.winner != None:
            self.screen.blit(self.winnerSurface, self.winnerRect)

        if self.cardFontSurf != None:
            self.screen.blit(self.backCard, self.backCardRect)
            self.screen.blit(self.cardFontSurf, self.cardFontRect)
            self.cardFontSurf = None

        pygame.display.flip()
        self.clock.tick(self.fps)

    def main(self):
        self.cardsOwner()
        self.update()
        while 1:
            if self.animation == 1:
                # We continue the animation
                self.putCard()
                self.update()
            else:
                # We over the animation and now the next player have to play.
                if self.sensAnimation == 1:
                    self.player = self.player * -1
                    self.sensAnimation = 0

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP and self.animation == 0:
                    if self.winner == None:
                        self.playCard()
                elif event.type == QUIT:
                    audio = [self.Sound.soundVolume, self.Sound.musicVolume]
                    setConfig("config.txt", audio)
                    pygame.quit()
                    sys.exit()
                else:
                    # We get the status of all key on keyboard.
                    # Then we select the one at place 27: Escape.
                    # We can do this only if we ran the game
                    # with Menu.py and not directly from main.py
                    if pygame.key.get_pressed()[27] and self.boss != None:
                        self.boss.main()

            pygame.display.flip()
            self.clock.tick(self.fps)

    def playCard(self):
        """When player has to play a card"""

        coords = pygame.mouse.get_pos()

        if self.player == 1:
        # Player 1
            for card in self.player1Hand.cards:
                if card.rect.collidepoint(coords) and card.inHand:
                    self.CARD = card
                    self.selectedCard()
                    break
            if not self.CARD == None:
            # If we clicked on a card.
            # We wait for the event 'MOUSEBUTTONUP', so first we clean the
            #queue event. Then we deactivate the MOUSEMOTION event, because
            #it causes the card to be put randomly on the field!
            #We wait an event, for example a touch on the keyboard
            #pressed, or MOUSEBUTTONUP, but not only, and we reactivate
            #MOUSEMOTION, we could need it later.
                self.deactivate()
                if not self.animation:
                    pygame.event.wait()
                while pygame.event.peek(MOUSEBUTTONUP) and not self.animation:
                    pass
                self.reactivate()
                # If the player clicked on the field this time, we test
                #each cases of the Field.
                if self.field.rect.collidepoint(pygame.mouse.get_pos()):
                    for case in self.field.fieldRects:
                        if case.collidepoint(pygame.mouse.get_pos()):
                            self.position = case.topleft
                            if not self.caseFilled():
                                self.animation = 1
                                self.putCard()
                                self.cardsOwner()
                            return
                else:
                    self.deselectedCard()
                    self.CARD = None

        if self.player == -1:
        # Player -1...I mean Player 2
            for card in self.player2Hand.cards:
                if (card.rect.collidepoint(coords) and card.inHand):
                    self.CARD = card
                    self.selectedCard()
                    break
            if not self.CARD == None:
                # Same as before
                self.deactivate()
                if not self.animation:
                    pygame.event.wait()
                while pygame.event.peek(MOUSEBUTTONUP) and not self.animation:
                    pass
                self.reactivate()
                if self.field.rect.collidepoint(pygame.mouse.get_pos()):
                    for case in self.field.fieldRects:
                        if case.collidepoint(pygame.mouse.get_pos()):
                            self.position = case.topleft
                            if not self.caseFilled():
                                self.animation = 1
                                self.putCard()
                                self.cardsOwner()
                            return
                else:
                    self.deselectedCard()
                    self.CARD = None

    def putCard(self):
            """Animation of a card put on the field"""

            if self.CARD.inHand == 1:
            # We check if self..CARD is in the player's Hand
                self.Sound.playPutCard()

            # We drop the card off the Hand
            if self.CARD.inHand == 1:
                self.CARD.inHand = 0

            # Depending of the direction of the animation, we make the card
            # being invisible or visible again.
            if self.sensAnimation == 0:
                self.alphaAnimation -= 25
                self.CARD.image.set_alpha(self.alphaAnimation)
            elif self.sensAnimation == 1:
                self.alphaAnimation += 25
                self.CARD.image.set_alpha(self.alphaAnimation)

            # We change the position of the card and the animation's direction
            if self.CARD.image.get_alpha() == 5:
                self.CARD.rect.topleft = self.position
                self.sensAnimation = 1

            if self.CARD.image.get_alpha() == 255 and self.sensAnimation == 1:
                # We have put the card on the field and the animation is over
                #Now we have to look if that card captured some of the ennemy's
                self.animation = 0
                adjacentCards = self.getAdjacent()
                capturedCard = adjacent(self.CARD, adjacentCards)
                self.changeOwner(capturedCard)
                self.emptyCase -= 1
                self.CARD = None

            if self.emptyCase == 0:
                self.winAnimation()

    def selectedCard(self):
        """Player has selected a card
        But not yet a place on the field"""
        for i in range(5):
            self.CARD.rect.centerx += 4 * self.player
            self.update()

    def deselectedCard(self):
        """Finally, the player wants an other card"""
        for i in range(5):
            self.CARD.rect.centerx -= 4 * self.player
        self.CARD = None
        self.update()

    def deactivate(self):
        """Deactivate MOUSEMOTION event and clean the queue"""
        pygame.event.set_blocked(MOUSEMOTION)
        pygame.event.clear()

    def reactivate(self):
        """Get back MOUSEMOTION"""
        pygame.event.set_allowed(MOUSEMOTION)

    def caseFilled(self):
        """Say if there is already a card in the case"""
        for card in self.player1Hand.cards:
            if card.rect.topleft == self.position:
                return 1
        for card in self.player2Hand.cards:
            if card.rect.topleft == self.position:
                return 1
        return 0

    def cardsOwner(self):
        """Which cards is owned by who?"""
        cardPlayer = 0
        for card in self.player1Hand.cards:
            if card.owner == self.player:
                cardPlayer += 1
        for cards in self.player2Hand.cards:
            if cards.owner == self.player:
                cardPlayer += 1
        if self.player == 1:
            self.scorePlayer1.updateScore(cardPlayer)
            self.scorePlayer2.updateScore(10 - cardPlayer)
        elif self.player == -1:
            self.scorePlayer1.updateScore(10 - cardPlayer)
            self.scorePlayer2.updateScore(cardPlayer)

    def getAdjacent(self):
        """Get all the adjacent cards of the first one put"""
        posx, posy = self.CARD.rect.topleft
        adjacentCards = [None, None, None, None]
        if self.player == 1:
            for card in self.player2Hand.cards:
                if card.inHand == 0:
                    if card.rect.collidepoint((posx, posy - 144)):
                        # We first look at the card on the top
                        adjacentCards[0] = card

                    if card.rect.collidepoint((posx + 113, posy)):
                        # We look at the card on the right
                        adjacentCards[1] = card

                    if card.rect.collidepoint((posx, posy + 144)):
                        # We look at the card on the bottom
                        adjacentCards[2] = card

                    if card.rect.collidepoint((posx - 113, posy)):
                        # We look at the card on the left
                        adjacentCards[3] = card
        elif self.player == -1:
            for card in self.player1Hand.cards:
                if card.inHand == 0:
                    if card.rect.collidepoint((posx, posy - 144)):
                        # We first look at the card on the top
                        adjacentCards[0] = card

                    if card.rect.collidepoint((posx + 113, posy)):
                        # We look at the card on the right
                        adjacentCards[1] = card

                    if card.rect.collidepoint((posx, posy + 144)):
                        # We look at the card on the bottom
                        adjacentCards[2] = card

                    if card.rect.collidepoint((posx - 113, posy)):
                        # We look at the card on the left
                        adjacentCards[3] = card
        return adjacentCards

    def changeOwner(self, cards):
        for card in cards:
            if card.owner == 1:
                self.player1Hand.cards.remove(card)
                self.player2Hand.cards.append(card)
            if card.owner == -1:
                self.player2Hand.cards.remove(card)
                self.player1Hand.cards.append(card)
            self.capturedAnimation(card)
        self.cardsOwner()

    def capturedAnimation(self, card):
        # We want the sound of the card put played before doing anything more
        self.update()
        while (pygame.mixer.get_busy()):
            pass

        # self.Sound.capturedCard.play()
        width = card.rect.width  # we expect 113. If not please change format.
        height = card.image.get_rect().height  # Here we expect 139.
        topleft = list(card.rect.topleft)
        print height, "\t", topleft
        step = 16

        while(width != 1):
            width -= step
            topleft[0] += step / 2
            getCard(card)
            card.image = pygame.transform.scale(card.image, (width, height))
            card.rect = card.image.get_rect()
            card.rect.topleft = topleft
            self.update()

        card.owner *= -1
        card.changeOwner(card.rect.center)

        while (width != 113):
            width += step
            topleft[0] -= step / 2
            getCard(card)
            card.image = pygame.transform.scale(card.image, (width, height))
            card.rect = card.image.get_rect()
            card.rect.topleft = topleft
            self.update()

    def winAnimation(self):
        if self.scorePlayer1.score > self.scorePlayer2.score:
            self.winner = u"Blue win!"
        elif self.scorePlayer2.score > self.scorePlayer1.score:
            self.winner = u"Red win!"
        else:
            self.winner = u"Equality!"
        self.winnerSurface = self.winnerFont.render(self.winner, True, white)
        self.winnerRect = self.winnerSurface.get_rect()
        self.winnerRect.midtop = self.backgroundRect.midtop
        self.winnerRect.y += 10

if __name__ == '__main__':
    Application(800, 600)
