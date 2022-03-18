"""
A small game where youre flying a plane and astoroids come by trying to destroy youre ship
or enemy ships will appear that will try to kill you
"""

import pygame
import sys
from random import randint

pygame.init()
pygame.font.init()

# CONSTANT VARIABLES
screenSize = (700, 700)
# colors
colors = {
    "darkGrey": (50, 50, 50),
    "paleYellow": (203, 219, 29),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "neonGreen": (37, 247, 30),
    "lightBlue": (0, 255, 255),
    "green": (0, 255, 0),
}

explosionImages = [
    pygame.image.load("Explosion1.png"),
    pygame.image.load("Explosion2.png"),
    pygame.image.load("Explosion3.png"),
    pygame.image.load("Explosion4.png"),
    pygame.image.load("Explosion5.png"),
    pygame.image.load("Explosion6.png"),
]


smallMeteor = pygame.image.load("MeteorKlein.png")
mediumMeteor = pygame.image.load("MeteorMittel.png")
bigMeteor = pygame.image.load("MeteorGroß.png")


screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()
pygame.display.set_caption("Asteroids")


def showtext(text, x, y, fontSize):
    font = pygame.font.Font(None, fontSize)
    text_surface = font.render(text, True, colors["white"])
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


# Display the start of loading

showtext("Loading", screenSize[0] / 2, screenSize[1] / 2, 100)


class explosion:
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.counter = 0

    def update(self):
        self.counter += 1
        # Return determines if the explosion should be killed or not
        if self.counter >= 31:
            return True
        else:
            return False

    def draw(self):
        screen.blit(explosionImages[int(self.counter / 6)], (self.posX, self.posY))


class bullet:
    def __init__(self, posX, posY, direction, color):
        self.posX = posX
        self.posY = posY
        self.direction = direction
        self.rect = pygame.Rect(posX, posY, 10, 10)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.posX, self.posY, 10, 10))

    def update(self):
        self.posX += self.direction[0]
        self.posY += self.direction[1]
        self.rect = self.getRect()

    def getRect(self):
        rect = pygame.Rect(self.posX, self.posY, 10, 10)
        return rect


class plane:
    def __init__(self, posX, posY, lives, dmg, shotTicks, speed):
        # Position
        self.posX = posX
        self.posY = posY

        # Stats
        self.lives = lives
        self.dmg = dmg
        # Shots every x tick
        self.shotTicks = shotTicks
        self.speed = speed
        self.bullets = []
        self.gunSprayRange = [-4, 4]

        self.width = 30
        self.height = 60

        self.rect = pygame.Rect(posX, posY, self.width, self.height)

        self.jetImage = pygame.image.load("JetImage.png").convert_alpha()

    def draw(self):
        screen.blit(self.jetImage, (self.posX, self.posY))

    def getPressedKeys(self):
        pressedKeys = []
        # Getting the pressed key
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            pressedKeys.append([0, -1])
        elif pressed[pygame.K_DOWN]:
            pressedKeys.append([0, 1])
        if pressed[pygame.K_LEFT]:
            pressedKeys.append([-1, 0])
        elif pressed[pygame.K_RIGHT]:
            pressedKeys.append([1, 0])
        return pressedKeys

    def getRect(self):
        # + 15 to center the hitbox to the plane Image
        rect = pygame.Rect(self.posX + 15, self.posY, self.width, self.height)
        return rect

    def updatePlayerPosition(self):
        speed = self.speed
        playerX = self.posX
        playerY = self.posY
        pressedKeys = self.getPressedKeys()
        if pressedKeys != []:
            for pressedKey in pressedKeys:
                playerX += pressedKey[0] * speed
                playerY += pressedKey[1] * speed
            self.posX = playerX
            self.posY = playerY
            self.rect = self.getRect()

    def update(self):
        self.updatePlayerPosition()


class meteor:
    def __init__(self, posX, posY, lives, width, height):
        # Position
        self.posX = posX
        self.posY = posY

        # Stats
        self.defaultLives = lives
        self.lives = lives
        meteorValue = randint(30, 100)
        self.width = meteorValue
        self.height = meteorValue
        meteorImage = smallMeteor
        # 30 - 50
        # 50 - 70
        # 70 - 100
        if meteorValue >= 50 and meteorValue < 70:
            meteorImage = mediumMeteor
        elif meteorValue >= 70:
            meteorImage = bigMeteor
        self.meteorImage = meteorImage
        self.rect = pygame.Rect(posX, posY, self.width, self.height)
        # The direction will also be the speed i will just multiply the value of
        # the direction by 2 or something like that XD
        self.direction = [randint(-9, 9), randint(3, 9)]

    def draw(self):
        screen.blit(self.meteorImage, (self.posX, self.posY))
        # pygame.draw.rect(
        #     screen, colors["darkGrey"], (self.posX, self.posY, self.width, self.height)
        # )
        showtext(
            str(self.lives), self.posX + self.width / 2, self.posY + self.height / 2, 50
        )

    def update(self):
        self.posX += self.direction[0] * 0.6
        self.posY += self.direction[1] * 0.6
        self.rect = self.getRect()

    def getRect(self):
        rect = pygame.Rect(self.posX, self.posY, self.width, self.height)
        return rect


class enemy:
    def __init__(self, lives, shotTicks):
        # Position
        self.posX = 350
        self.posY = -50

        # Stats
        self.lives = lives
        # Shoots every x tick
        self.shotTicks = shotTicks
        self.direction = [5, 0]
        self.rect = pygame.Rect(self.posX, self.posY, 60, 60)
        self.image = pygame.image.load("EnemyJet.png")

    def update(self):
        if self.posY < 30:
            self.posY += 5
        else:
            self.posX += self.direction[0]
            self.posY += self.direction[1]
        if self.posX < 10:
            self.direction = [5, 0]
        if self.posX > 670:
            self.direction = [-5, 0]
        self.rect = pygame.Rect(self.posX, self.posY, 60, 60)

    def draw(self):
        screen.blit(self.image, (self.posX, self.posY))
        # pygame.draw.rect(screen, colors["green"], (self.posX, self.posY, 60, 60))
        showtext(str(self.lives), self.posX + 30, self.posY + 30, 50)


class interface:
    def __init__(self):
        self.score = 0
        self.heartImage = pygame.image.load("heart.png")
        self.backgroundPositions = [[0, 0]]

    def draw(self, lives):
        showtext("Score: " + str(self.score), screenSize[0] / 2, 20, 50)
        for x in range(0, lives):
            screen.blit(self.heartImage, (x * 50, 0))

    def drawGameOverScreen(self):
        while 1:
            clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked = True
            for position in self.backgroundPositions:
                screen.blit(backgroundImage, position)
                position[1] += 2
                if position[1] >= 700:
                    self.backgroundPositions.remove(position)
                if position[1] == 2:
                    self.backgroundPositions.append([0, -698])
            mousePos = pygame.mouse.get_pos()
            mouseRect = pygame.Rect(mousePos[0], mousePos[1], 20, 20)
            buttonRect = pygame.Rect(300, 470, 100, 60)
            buttonSelected = False
            if mouseRect.colliderect(buttonRect):
                buttonSelected = True
            if buttonSelected:
                buttonColor = colors["lightBlue"]
            else:
                buttonColor = colors["darkGrey"]
            if clicked and buttonSelected:
                gameLoop()
            pygame.draw.rect(screen, buttonColor, (300, 470, 100, 60))
            showtext("Play", 350, 500, 50)
            showtext("Game Over", screenSize[0] / 2, screenSize[1] * 0.3, 50)
            showtext(
                "Score " + str(self.score), screenSize[0] / 2, screenSize[1] * 0.5, 80
            )
            pygame.display.update()


backgroundImage = pygame.image.load("Background.png").convert_alpha()


def gameLoop():
    playerPlane = plane(250, 250, 3, 1, 5, 5)
    gameInterface = interface()
    enemies = []
    meteors = []
    bullets = []
    enemyBullets = []
    backgroundPositions = [[0, 0]]
    explosions = []
    counter = 1
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        for position in backgroundPositions:
            screen.blit(backgroundImage, position)
            position[1] += 2
            if position[1] >= 700:
                backgroundPositions.remove(position)
            if position[1] == 2:
                backgroundPositions.append([0, -698])

        for currentExplosion in explosions:
            endExplosion = currentExplosion.update()
            if endExplosion:
                explosions.remove(currentExplosion)
            else:
                currentExplosion.draw()

        playerPlane.update()
        playerPlane.draw()

        if counter % 10 == 0 and len(meteors) < 30:
            meteors.append(meteor(350, -180, randint(5, 10), 50, 50))

        if counter % 500 == 0:
            enemies.append(enemy(50, randint(20, 35)))

        if counter % playerPlane.shotTicks == 0:
            bullets.append(
                bullet(
                    playerPlane.posX + 23,
                    playerPlane.posY,
                    [
                        randint(
                            playerPlane.gunSprayRange[0], playerPlane.gunSprayRange[1]
                        ),
                        -10,
                    ],
                    colors["paleYellow"],
                )
            )

        for currentBullet in bullets:
            currentBullet.update()
            currentBullet.draw()
            destroyBullet = False
            for currentEnemy in enemies:
                if currentBullet.rect.colliderect(currentEnemy.rect):
                    destroyBullet = True
                    currentEnemy.lives -= 1
                    if currentEnemy.lives == 0:
                        enemies.remove(currentEnemy)
            for currentMeteor in meteors:
                if currentMeteor.rect.colliderect(currentBullet.rect):
                    destroyBullet = True
                    currentMeteor.lives -= playerPlane.dmg
                    if currentMeteor.lives == 0:
                        explosions.append(
                            explosion(currentMeteor.posX, currentMeteor.posY)
                        )
                        gameInterface.score += int(
                            currentMeteor.defaultLives * (currentMeteor.width / 10)
                        )
                        meteors.remove(currentMeteor)
            if currentBullet.posY < 0 or destroyBullet:
                bullets.remove(currentBullet)

        for currentMeteor in meteors:
            currentMeteor.update()
            currentMeteor.draw()
            if currentMeteor.rect.colliderect(playerPlane.rect):
                meteors.remove(currentMeteor)
                playerPlane.lives -= 1
                if playerPlane.lives == 0:
                    gameInterface.drawGameOverScreen()
            if (
                currentMeteor.posY > 700
                or currentMeteor.direction[0] > 0
                and currentMeteor.posX > 700
                or currentMeteor.direction[1] < 0
                and currentMeteor < 0
            ):
                meteors.remove(currentMeteor)

        for currentBullet in enemyBullets:
            currentBullet.update()
            currentBullet.draw()
            destroyBullet = False
            if currentBullet.rect.colliderect(playerPlane.rect):
                playerPlane.lives -= 1
                destroyBullet = True
                if playerPlane.lives == 0:
                    gameInterface.drawGameOverScreen()
            if currentBullet.posY > 700 or destroyBullet:
                enemyBullets.remove(currentBullet)

        for currentEnemy in enemies:
            if counter % currentEnemy.shotTicks == 0:
                enemyBullets.append(
                    bullet(
                        currentEnemy.posX,
                        currentEnemy.posY,
                        [
                            randint(-2, 2),
                            10,
                        ],
                        colors["green"],
                    )
                )
            currentEnemy.update()
            currentEnemy.draw()

        gameInterface.draw(playerPlane.lives)
        counter += 1
        pygame.display.update()
        clock.tick(60)


gameLoop()
