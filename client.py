import pygame
from pygame import *
from network import Network
pygame.font.init()
pygame.init()
import pickle

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

class Button:
    def __init__(self, text, x, y, color, width, height):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("candara", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):

    win.fill((255, 182, 193))

    if not (game.connected()):
        backgroundImage = pygame.image.load("flower.jpg")
        win.blit(backgroundImage, [-70, -90])
        font = pygame.font.SysFont("candara", 60)
        text = font.render("Waiting for Player...", 1, (231, 84, 128), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:

        font = pygame.font.SysFont("candara", 50)
        text = font.render("Your Move", 1, (231, 84, 128))
        win.blit(text, (60, 160))

        text = font.render("Opponent", 1, (231, 84, 128))
        win.blit(text, (380, 160))

        move1 = game.getPlayerMove(0)
        move2 = game.getPlayerMove(1)

        if game.bothWent():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))

        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))
        for btn in btns:
            btn.draw(win)
    pygame.display.update()

btns = [Button("Rock", 50, 500, (102, 2, 60), 170, 100), Button("Scissors", 250, 500, (80,200,120), 170, 100), Button("Paper", 450, 500, (0,191,255), 170, 100)]
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are Player: ", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break


            font = pygame.font.SysFont("candara", 90)
            if(game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):

                text = font.render("You Won!", 1, (255, 0, 0))

            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255, 0, 0))
            else:

                text = font.render("You Lost...", 1, (255, 0, 0))


            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)


def menuScreen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((0,0,0))
        backgroundImage = pygame.image.load("background.jpg")
        win.blit(backgroundImage, [0, 0])

        menuButton = Button("Click here to play!", 180, 250, (231, 84, 128), 350, 150)
        menuButton.draw(win)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menuScreen()


