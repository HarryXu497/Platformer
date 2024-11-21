################################################################################
# ░██████╗░█████╗░██╗░░░██╗██████╗░░█████╗░███████╗░░░░░░░░░█████╗░░█████╗░██████╗░███████╗
# ██╔════╝██╔══██╗██║░░░██║██╔══██╗██╔══██╗██╔════╝░░░░░░░░██╔══██╗██╔══██╗██╔══██╗██╔════╝
# ╚█████╗░██║░░██║██║░░░██║██████╔╝██║░░╚═╝█████╗░░░░░░░░░░██║░░╚═╝██║░░██║██║░░██║█████╗░░
# ░╚═══██╗██║░░██║██║░░░██║██╔══██╗██║░░██╗██╔══╝░░░░░░░░░░██║░░██╗██║░░██║██║░░██║██╔══╝░░
# ██████╔╝╚█████╔╝╚██████╔╝██║░░██║╚█████╔╝███████╗░░░░░░░░╚█████╔╝╚█████╔╝██████╔╝███████╗
# ╚═════╝░░╚════╝░░╚═════╝░╚═╝░░╚═╝░╚════╝░╚══════╝░░░░░░░░░╚════╝░░╚════╝░╚═════╝░╚══════╝
###############################################################################
# Name: PlatformerTest.py
# Author:
#   Harry Xu
#
# Date:
#   Started: 12/21/21
#   Finished: 1/25/22
#
# Description:
#   A platformer shooter game with 1 or 2 players.
#   The players jump from platform to platform, finding new weapons and
#   fighting enemies. There are 3 stages, each with 5 levels, and capped with
#   a boss fight at the end of each stage.
#
###############################################################################
import pygame
from random import randint, uniform, choice
from typing import Union, Callable, Any

# Colours ---------------------------------------------------------------------
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (128, 0, 255)
LPURPLE = (148, 41, 255)
LRED = (255, 200, 200)
BLACK = (0, 0, 0)
GREY = (40, 40, 40)

# Player, Enemy and Coin *hitbox* sizes ---------------------------------------
# Player size
PLAYER_SIZE_X = 32
PLAYER_SIZE_Y = 40

# Enemy Size
ENEMY_SIZE_X = 38
ENEMY_SIZE_Y = 46

# Underworld enemy Size
UNDERWORLD_ENEMY_SIZE_X = 48
UNDERWORLD_ENEMY_SIZE_Y = 60

# Ice enemy Size
ICE_ENEMY_SIZE_X = 56
ICE_ENEMY_SIZE_Y = 60

# Coin size
COLLECTIBLE_SIZE = 16

# Speed constants--------------------------------------------------------------
MOVING_PLATFORM_SPEED = 12  # moving platform speed is inversely proportional to this

# Game Window Options ---------------------------------------------------------
pygame.init()
# WIDTH = 800
# HEIGHT = 600
# gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))

## the following code makes the game full screen and sets the width and height accordingly
gameWindow = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = gameWindow.get_size()


# Game icon and caption ----------------------------------------
icon = pygame.image.load("images/character/running/running2.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Source Code")

# Images not loaded with a class ----------------------------------------------
backgroundImage = pygame.image.load("images/backgrounds/background.jpg")
cloudsImage = pygame.image.load("images/backgrounds/clouds.png")

underworldBackgroundImage = pygame.image.load("images/backgrounds/underworld.png")
iceBackgroundImage = pygame.image.load("images/backgrounds/iceBackground.png")

# tile images needed for comparison
grassTile = pygame.image.load("images/tiles/grassTile/tile.png")
underworldTile = pygame.image.load("images/tiles/underworldTile/underworldTile.png")
iceTile = pygame.image.load("images/tiles/iceTile.jpg")

# resizing images
backgroundImage = pygame.transform.scale(backgroundImage, (WIDTH, HEIGHT))
cloudsImage = pygame.transform.scale(cloudsImage, (WIDTH, HEIGHT))
underworldBackgroundImage = pygame.transform.scale(underworldBackgroundImage, (WIDTH, HEIGHT))
iceBackgroundImage = pygame.transform.scale(iceBackgroundImage, (WIDTH, HEIGHT))

# a sized up coin icon for the GUI
coinIcon = pygame.image.load("images/coin/coinIcon.png")

# Bullet GUI images
bulletGUI = [
    pygame.image.load(f"images/gui/bullet/bullet{i}.png") for i in range(1, 6)
]

# menu animation images
menuBackgroundImage = pygame.image.load("images/backgrounds/background.jpg")
menuBackgroundImage = pygame.transform.scale(menuBackgroundImage, (WIDTH, HEIGHT))

# paused translucent image
pausedImage = pygame.image.load("images/backgrounds/paused.png")
pausedImage = pygame.transform.scale(pausedImage, (WIDTH, HEIGHT))
pausedImage.set_alpha(128)  # set opacity

# pause button
pauseButton = pygame.image.load("images/gui/button/pauseButton.png")
pauseButtonPressed = pygame.image.load("images/gui/button/pauseButtonPressed.png")

# Sounds ----------------------------------------------------------------------
# initializing the pygame.mixer module
pygame.mixer.init()

# menu button selection sound
menuSelect = pygame.mixer.Sound("sounds/menu/select.wav")
menuSelect.set_volume(0.25) # reducing volume

# player taking damage sound
playerHit = pygame.mixer.Sound("sounds/player/playerHit.wav")

# coin collection sound
coinCollected = pygame.mixer.Sound("sounds/collectibles/coinCollected.wav")

# potion collection sound
potionCollected = pygame.mixer.Sound("sounds/collectibles/potionCollected.wav")
potionCollected.set_volume(0.5) # reducing volume

# an error sound that plays when you try to unlock the upgrade chest without enough coins
notEnoughCoins = pygame.mixer.Sound("sounds/collectibles/notEnoughCoins.wav")
notEnoughCoins.set_volume(0.2) # reducing volume

## projectile sounds ##
# bullet
bulletFired = pygame.mixer.Sound("sounds/player/bullet/bulletFired.wav")
bulletFired.set_volume(0.4)

# shotgun
shotgunFired = pygame.mixer.Sound("sounds/player/bullet/shotgunFired.wav")

# flamethrower
flameSound = pygame.mixer.Sound("sounds/player/bullet/flame.wav")
flameSound.set_volume(0.05)

# lightning staff
thunderSound = pygame.mixer.Sound("sounds/player/staff/thunderSound.wav")
thunderSound.set_volume(0.6)

# grenade explosion
grenadeExplosion = pygame.mixer.Sound("sounds/player/grenade/explosion.mp3")
grenadeExplosion.set_volume(0.75)

# laser bullet sound
laserFiredSound = pygame.mixer.Sound("sounds/player/laser/laser.mp3")

# sniper laser bullet
sniperLaserFired = pygame.mixer.Sound("sounds/player/laser/sniperLaser.wav")

# picking up weapons
pickupWeapon = pygame.mixer.Sound("sounds/player/pickup/pickupWeapon.wav")
pickupWeapon.set_volume(0.35)

# enemy taking damage
enemyHitSound = pygame.mixer.Sound("sounds/enemy/EnemyHit.wav")
enemyHitSound.set_volume(0.1)

# boss taking damage
bossHitSound = pygame.mixer.Sound("sounds/enemy/BossHit.wav")
bossHitSound.set_volume(0.5)

# "missing" the boss - hitting a 'closed' missile channel
bossMissedSound = pygame.mixer.Sound("sounds/enemy/BossMissed.wav")
bossMissedSound.set_volume(0.5)

# entering a portal
portalEnter = pygame.mixer.Sound("sounds/portal/portal.wav")
portalEnter.set_volume(0.4)

# the player dies
playerDies = pygame.mixer.Sound("sounds/player/playerDeath.wav")
playerDies.set_volume(0.3)

# soundtrack
pygame.mixer.music.load("sounds/soundtrack.mp3")

# Fonts -----------------------------------------------------------------------
scoreFont = pygame.font.Font("fonts/ScoreFont.ttf", 50)
scoreFontSmall = pygame.font.Font("fonts/ScoreFont.ttf", 32)
titleFont = pygame.font.Font("fonts/TitleFontBold.ttf", (120 * WIDTH) // 800)
subTitleFont = pygame.font.Font("fonts/GravityBold8.ttf", (40 * WIDTH) // 800)
smallHeadingFont = pygame.font.Font("fonts/GravityBold8.ttf", (16 * WIDTH) // 800)
playerNameFont = pygame.font.Font("fonts/GravityBold8.ttf", (5 * WIDTH) // 800)
instructionFont = pygame.font.Font("fonts/GravityRegular5.ttf", (20 * WIDTH) // 800)
deathMessageFont = pygame.font.Font("fonts/GravityRegular5.ttf", (16 * WIDTH) // 800)


###############################################################################
#
# Classes
#
###############################################################################
#################################################################
#                                                               #
# Platforms                                                     #
#                                                               #
#################################################################
class Platform(object):
    """ An object representing a platform on which the player can move upon,
        enemies are spawned, and chests are generated.
        Base class for 'HorizontallyMovingPlatform' and 'VerticalMovingPlatform'

    Attributes:
        x: float
            The x position of the top left corner of the platform

        y: float
            The y position of the top left corner of the platform

        length: int
            The length of the platform

        width: int
            The width of the platform

        image: pygame.Surface
            The image of the tiled

        imageL: pygame.Surface
            The left image of the platform - a more 'rounded' verion of the normal 'image'
            
        imageR: pygame.Surface
            The right image of the platform - a more 'rounded' verion of the normal 'image'
    """

    def __init__(self, x: float, y: float, length: int, image: pygame.Surface = grassTile, width: int = 20) -> None:
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.image = image

        # loading the rounded grass images if the tile image is set to the grass type
        if self.image is grassTile:
            self.imageL = pygame.image.load("images/tiles/grassTile/tileL.png")
            self.imageR = pygame.image.load("images/tiles/grassTile/tileR.png")
            
        elif self.image is underworldTile:
            self.imageL = pygame.image.load("images/tiles/underworldTile/underworldTileLeft.png")
            self.imageR = pygame.image.load("images/tiles/underworldTile/underworldTileRight.png")
            
        else:
            self.imageL = self.image
            self.imageR = self.image

    def draw(self) -> None:
        """ Draws the platform, with square tiles, and using the left and right images if possible

        Parameters:


        Return => None
        """
        for x in range(int(self.x), int(self.x + self.length), 20):
            # this means that this is the first block - blit 'imageL'
            if x == int(self.x):
                gameWindow.blit(self.imageL, (x, self.y))

            # this means that this is the last block - blit 'imageR'
            elif x + 20 >= int(self.x + self.length):
                gameWindow.blit(self.imageR, (x, self.y))

            # blit the normal image
            else:
                gameWindow.blit(self.image, (x, self.y))


class VerticalMovingPlatform(Platform):
    """ An object representing a platform which moves vertically

    Attributes:
        x: float
            The x position of the top left corner of the platform

        y: float
            The y position of the top left corner of the platform

        length: int
            The length of the platform

        rangeOfMovement:
            The vertical range of the movement of the platform

        speed: float
            The speed at which the platform moves

        image: pygame.Surface
            The image of the tile

        moveDown: bool
            If the platform is moving down - True if moving down, False if moving up

        upperBound: float
            The highest point that the platform can go

        lowerBound: float
            The lowest point that the platform can go

    """

    def __init__(self, x: float, y: float, length: int, rangeOfMovement: float, speed: float = 0.5, image: pygame.Surface = grassTile) -> None:
        super().__init__(x, y, length, image)
        self.upperBound = y - rangeOfMovement
        self.lowerBound = y + rangeOfMovement
        self.moveDown = True
        self.speed = speed

    def draw(self) -> None:
        """ Draws the platform, with square tiles, and using the left and right images if possible.
            Also draws the line of movement in a gray line

        Parameters:


        Return => None
        """

        # draws the line of movement
        pygame.draw.line(gameWindow, GREY, (self.x + self.length / 2, self.upperBound),
                         (self.x + self.length / 2, self.lowerBound), 2)

        # drawing the platform at the correct location
        for xCoord in range(int(self.x), int(self.x + self.length), 20):
            # this means that this is the first block - blit 'imageL'
            if xCoord == int(self.x):
                gameWindow.blit(self.imageL, (xCoord, self.y))

            # this means that this is the last block - blit 'imageR'
            elif xCoord == int(self.x + self.length) - 20:
                gameWindow.blit(self.imageR, (xCoord, self.y))

            # blit the normal image
            else:
                gameWindow.blit(self.image, (xCoord, self.y))

        # Moving the platform
        if self.moveDown:
            # move platform down
            self.y += self.speed
            
        else:
            # move platform up
            self.y -= self.speed

        # flips the movement direction when it hits the edge
        if self.y <= self.upperBound:
            self.moveDown = True
            
        if self.y >= self.lowerBound:
            self.moveDown = False


class HorizontalMovingPlatform(Platform):
    """ An object representing a horizontally moving platform

    Attributes:
        x: float
            The x position of the top left corner of the platform

        y: float
            The y position of the top left corner of the platform

        length: int
            The length of the platform

        rangeOfMovement: float
            The horizontal range of the movement of the platform

        speed: float
            The speed at which the platform moves

        image: pygame.Surface
            The image of the tile

        moveRight: bool
            If the platform is moving right - True if moving right, False if moving left

        upperBound: float
            The highest point that the platform can go

        lowerBound: float
            The lowest point that the platform can go

    """

    def __init__(self, x: float, y: float, length: int, rangeOfMovement: float, speed: float = 0.5, image: pygame.Surface = grassTile) -> None:
        self.upperBound = x - rangeOfMovement
        self.lowerBound = x + rangeOfMovement
        self.rangeOfMovement = rangeOfMovement
        self.moveRight = True
        self.speed = speed
        super().__init__(x, y, length, image)

    def draw(self) -> None:
        """ Draws the platform, with square tiles, and using the left and right images if possible.
            Also draws the line of movement in a gray line

        Parameters:


        Return => None
        """
        # draws the line of movement
        pygame.draw.line(gameWindow, BLACK, (self.upperBound, self.y + self.width / 2), (self.lowerBound + self.length, self.y + self.width / 2), 2)

        # drawing the platform at the correct location
        for xCoord in range(int(self.x), int(self.x + self.length), 20):
            # this means that this is the first block - blit 'imageL'
            if xCoord == int(self.x):
                gameWindow.blit(self.imageL, (xCoord, self.y))

            # this means that this is the last block - blit 'imageR'
            elif xCoord == int(self.x + self.length) - 20:
                gameWindow.blit(self.imageR, (xCoord, self.y))

            # blit the normal image
            else:
                gameWindow.blit(self.image, (xCoord, self.y))

        # Moving the platform
        if self.moveRight:
            # move right
            self.x += self.speed
            
        else:
            # move left
            self.x -= self.speed

        # flips the movement direction when it hits the edge
        if self.x <= self.upperBound:
            self.moveRight = True
        if self.x >= self.lowerBound:
            self.moveRight = False


#################################################################
#                                                               #
# Enemies                                                       #
#                                                               #
#################################################################
class Enemy(object):
    """ The base class for the enemy

    Attributes:
        platform: Platform
            The platform the enemy spawns on

        enemySizeX:
            Width of the enemy's hitbox

        enemySizeY:
            Height of the enemy's hitbox

        speed: float
            The speed of the enemy

        health: int
            The health of the enemy

        x: float
            The x position of the enemy, initialized based on the platform's x position

        y: float
            The y position of the enemy, initialized based on the platform's y position

        hitbox: pygame.Rect
            The hitbox of the enemy.

        moveLeft: bool
            A boolean for if the enemy is moving left. It's used to flip the image accordingly

        damaged: bool
            A boolean for if the enemy is damaged. If it is, the enemy becomes invincible

        isDead: bool
            A boolean for if the enemy is dead, but not done the explosion death animation yet.

        moving, hurt, dead: list[pygame.Surface]
            List of images for when the enemy is moving, hurt or dead. Changes if 'underworldEnemy' is True

        timeHit:
            Time that the enemy was hit - used in collisions and invincibility cooldowns

    """

    def __init__(self, platform: Platform, speed: float, health: int = 100) -> None:
        self.platform = platform
        self.speed = speed
        self.health = health
        self.enemySizeX = ENEMY_SIZE_X
        self.enemySizeY = ENEMY_SIZE_Y
        self.x = platform.x + platform.length / 2
        self.y = platform.y - ENEMY_SIZE_Y / 2
        self.moveLeft = True
        self.damaged = False
        self.isDead = False
        self.timeHit = 0

        # Animation Images
        self.moving = [
            pygame.image.load(f"images/enemy/normal/moving/running/running{i}.png") for i in range(1, 4)
        ]

        self.hurt = [
            pygame.image.load("images/enemy/normal/moving/hurt/hurt1.png"),
        ]

        self.dead = [
            pygame.image.load(f"images/enemy/normal/dead/explosion{i}.png") for i in range(1, 11)
        ]

        # The current image
        self.currentImage = self.moving[0]

        # Keeps track of the animation stages
        self.movingStage = 0
        self.deadStage = 0

        # the current time when it takes damage. used for an invincibility delay
        self.damageTime = 0

        # Hitbox
        self.hitbox = pygame.Rect(self.x - self.enemySizeX / 2, self.y - self.enemySizeY / 2, self.enemySizeX, self.enemySizeY)

    def draw(self) -> None:
        """ Draws the enemy at the correct x and y location, with the appropriate images

        Parameters:


        Return => None
        """
        # if the enemy is hurt, but not dead, draw the enemy hurt image
        if self.damaged and self.health > 0:
            # flip the image if the enemy is facing left
            if self.moveLeft:
                gameWindow.blit(pygame.transform.flip(self.hurt[0], True, False), (self.x - self.enemySizeX / 2, self.y - self.enemySizeY / 2))

            else:
                gameWindow.blit(self.hurt[0], (self.x - self.enemySizeX / 2, self.y - self.enemySizeY / 2))

        else:
            # otherwise, blit the normal image
            gameWindow.blit(self.currentImage, (self.x - self.enemySizeX / 2, self.y - self.enemySizeY / 2))

        # draws the health bar if not dead ----------------------------------------------------------------------------
        if not self.isDead:
            # draw the border
            pygame.draw.rect(gameWindow, BLACK, (int(self.x - self.enemySizeX / 2 - 2), int(self.y - self.enemySizeX / 2 - 7), self.enemySizeX + 4, 9), 2, 1)

            # draws the health
            for j in range(self.health // 5):
                pygame.draw.rect(gameWindow, RED, (int(self.x - self.enemySizeX / 2 + (j * self.enemySizeX // 23)), int(self.y - self.enemySizeX / 2 - 5), self.enemySizeX // 5, 5))

    def move(self) -> None:
        """ Moves the enemy along its platform, and uses the appropriate images

        Parameters:


        Return => None
        """
        # checks to see if any of the 'animationStage' attributes will cause an error, and resets them to 0
        self.checkAnimation()

        # move the enemy if its not dead ------------------------------------------------------------------------------
        if not self.isDead:

            # if its going left, deduct speed ---------------------------------
            if self.moveLeft:
                self.x -= self.speed
                # blit a flipped image
                self.currentImage = pygame.transform.flip(self.moving[int(self.movingStage // 15)], True, False)

            # if its moving right, add speed ----------------------------------
            else:
                self.x += self.speed
                # blit the image
                self.currentImage = self.moving[int(self.movingStage // 15)]

            # if the enemy has reached the end of the platform, flip its direction
            if self.x < self.platform.x + self.enemySizeX / 4:
                self.moveLeft = False

            if self.x > self.platform.x + self.platform.length - self.enemySizeX / 4:
                self.moveLeft = True

            # increment animation
            self.movingStage += 1

        # -------------------------------------------------------------------------------------------------------------

        # The enemy is dead -------------------------------------------------------------------------------------------
        else:
            # generate collectible and spawn it at the enemy's x and y coordinate
            if self.deadStage == 0:
                collectibles.append(Coin(self.x, self.y))

            # draw the explosion images, flipping horizontally if necessary
            if self.moveLeft:
                self.currentImage = pygame.transform.flip(self.dead[int(self.deadStage // 8)], True, False)

            else:
                self.currentImage = self.dead[int(self.deadStage // 8)]

            # increment 'deadStage'
            self.deadStage += 1

        # -------------------------------------------------------------------------------------------------------------

        # if the platform is a vertical moving platform ---------------------------------------------------------------
        if isinstance(self.platform, VerticalMovingPlatform):
            # change the y depending on the platform
            if self.platform.moveDown:
                self.y += self.platform.speed

            else:
                self.y -= self.platform.speed

        # -------------------------------------------------------------------------------------------------------------

        # if the platform is a horizontal moving platform -------------------------------------------------------------
        if isinstance(self.platform, HorizontalMovingPlatform):
            # change the y depending on the platform
            if self.platform.moveRight:
                self.x += self.platform.speed
                
            else:
                self.x -= self.platform.speed
        # -------------------------------------------------------------------------------------------------------------

        # Rebuilds the hitbox -------------------------------------------------
        self.hitbox = pygame.Rect(self.x - self.enemySizeX / 2, self.y - self.enemySizeY / 2, self.enemySizeX, self.enemySizeY)

    def checkAlive(self) -> None:
        """ Checks if the enemies health is below 0, and sets the 'isDead' attribute to True if so

        Parameters:


        Return => None
        """

        if self.health <= 0:
            self.isDead = True

    def checkAnimation(self) -> None:
        """ Checks to see if any of the 'animationStage' attributes will cause an error, and resets them to 0

        Parameters:


        Return => None
        """

        if self.movingStage >= len(self.moving) * 15 - 1:
            self.movingStage = 0
            
        if self.deadStage >= len(self.dead) * 8 - 1:
            self.deadStage = 0

    def takeDamage(self, damage: int) -> None:
        """ If the enemy is alive and the enemy is not invincible, deduct health

        Parameters:
            damage: int -> the damage to be taken


        Return => None
        """
        if timeElapsed - self.damageTime >= 0.125 and self.health > 0:
            self.damageTime = timeElapsed
            enemyHitSound.stop()
            enemyHitSound.play()
            self.health -= int(damage // 1.5)


class UnderworldEnemy(Enemy):
    """ Class representing an 'Underworld Enemy', based on the Enemy class

    Attributes:
        platform: Platform
            The platform the enemy spawns on

        enemySizeX:
            Width of the enemy's hitbox

        enemySizeY:
            Height of the enemy's hitbox

        speed: float
            The speed of the enemy

        health: int
            The health of the enemy

        x: float
            The x position of the enemy, initialized based on the platform's x position

        y: float
            The y position of the enemy, initialized based on the platform's y position

        moveLeft: bool
            A boolean for if the enemy is moving left. It's used to flip the image accordingly

        damaged: bool
            A boolean for if the enemy is damaged. If it is, the enemy becomes invincible

        isDead: bool
            A boolean for if the enemy is dead, but not done the explosion death animation yet.

        moving: list[pygame.Surface]
            List of images for when the enemy is moving.

        hurt: list[pygame.Surface]
            List of images for when the enemy is hurt.

        dead: list[pygame.Surface]
            List of images for when the enemy is dead.
    """

    def __init__(self, platform: Platform, speed: float, health: int = 100) -> None:
        super().__init__(platform, speed, health)
        self.enemySizeX = UNDERWORLD_ENEMY_SIZE_X
        self.enemySizeY = UNDERWORLD_ENEMY_SIZE_Y

        ## lists of images for animation ##
        self.moving = [
            pygame.image.load(f"images/enemy/underworld/moving/running/running{i}.png") for i in range(1, 7)
        ]

        self.hurt = [
            pygame.image.load("images/enemy/underworld/moving/hurt/hurt1.png"),
        ]

        # Explosion animations are the same, but scaled up
        self.dead = [
            pygame.image.load(f"images/enemy/underworld/dead/explosion{i}.png") for i in range(1, 11)

        ]

        self.x = platform.x + platform.length / 2
        self.y = platform.y - ENEMY_SIZE_Y / 2

        # booleans
        self.moveLeft = True
        self.damaged = False
        self.isDead = False

    def takeDamage(self, damage: int) -> None:
        """ Delegates call to super class method - takes less damage

        Parameters:
            damage: int -> the damage to be taken


        Return => None
        """
        super().takeDamage(int(damage // 2))


class IceEnemy(Enemy):
    """ Class representing an 'Ice Enemy', based on the Enemy class

    Attributes:
        platform: Platform
            The platform the enemy spawns on

        enemySizeX:
            Width of the enemy's hitbox

        enemySizeY:
            Height of the enemy's hitbox

        speed: float
            The speed of the enemy

        health: int
            The health of the enemy

        x: float
            The x position of the enemy, initialized based on the platform's x position

        y: float
            The y position of the enemy, initialized based on the platform's y position

        hitbox: pygame.Rect
            The hitbox of the enemy. It becomes larger if 'underworldEnemy' is true

        moveLeft: bool
            A boolean for if the enemy is moving left. It's used to flip the image accordingly

        damaged: bool
            A boolean for if the enemy is damaged. If it is, the enemy becomes invincible

        isDead: bool
            A boolean for if the enemy is dead, but not done the explosion death animation yet.

        moving: list[pygame.Surface]
            List of images for when the enemy is moving.

        hurt: list[pygame.Surface]
            List of images for when the enemy is hurt.

        dead: list[pygame.Surface]
            List of images for when the enemy is dead.

    """

    def __init__(self, platform: Platform, speed: float, health: int = 100) -> None:
        super().__init__(platform, speed, health)
        self.enemySizeX = ICE_ENEMY_SIZE_X
        self.enemySizeY = ICE_ENEMY_SIZE_Y

        # lists of images for animation
        self.moving = [
            pygame.image.load(f"images/enemy/ice/moving/running/running{i}.png") for i in range(1, 7)
        ]
        self.hurt = [
            pygame.image.load(f"images/enemy/ice/moving/running/running{i}.png") for i in range(1, 2)
        ]
        self.dead = [
            pygame.image.load(f"images/enemy/ice/dead/explosion{i}.png") for i in range(1, 11)
        ]

        self.x = platform.x + platform.length / 2
        self.y = platform.y - ENEMY_SIZE_Y / 2

        # booleans
        self.moveLeft = True
        self.damaged = False
        self.isDead = False

    # overrides the 'move()' method because the ice enemy fires an icicle when it turns around
    def move(self) -> None:
        """ Moves the enemy along its platform

        Parameters:


        Return => None
        """
        # checks to see if any of the 'animationStage' attributes will cause an error, and resets them to 0
        self.checkAnimation()

        # move the enemy if its not dead ------------------------------------------------------------------------------
        if not self.isDead:

            # if its going left, deduct speed ---------------------------------
            if self.moveLeft:
                self.x -= self.speed
                # blit a flipped image
                self.currentImage = pygame.transform.flip(self.moving[int(self.movingStage // 15)], True, False)

            # if its moving right, add speed ----------------------------------
            else:
                self.x += self.speed
                # blit the image
                self.currentImage = self.moving[int(self.movingStage // 15)]

            # if the enemy has reached the end of the platform, flip its direction
            if self.x < self.platform.x + self.enemySizeX / 4:
                self.moveLeft = False

            # fires an icicle when it turns around
            if self.x > self.platform.x + self.platform.length - self.enemySizeX / 4:
                bullets.append(Icicle(self.x + 4, self.y + 5, 5))
                self.moveLeft = True

            # increment animation
            self.movingStage += 1

        # -------------------------------------------------------------------------------------------------------------

        # The enemy is dead -------------------------------------------------------------------------------------------
        else:
            # generate collectible and spawn it at the enemy's x and y coordinate
            if self.deadStage == 0:
                collectibles.append(Coin(self.x, self.y))

            # draw the explosion images, flipping if necessary
            if self.moveLeft:
                self.currentImage = pygame.transform.flip(self.dead[int(self.deadStage // 8)], True, False)

            else:
                self.currentImage = self.dead[int(self.deadStage // 8)]

            # increments 'deadStage'
            self.deadStage += 1

        # -------------------------------------------------------------------------------------------------------------

        # if the platform is a vertical moving platform ---------------------------------------------------------------
        if isinstance(self.platform, VerticalMovingPlatform):
            # change the y depending on the platform
            if self.platform.moveDown:
                self.y += self.platform.speed
            else:
                self.y -= self.platform.speed
        # -------------------------------------------------------------------------------------------------------------

        # if the platform is a horizontal moving platform -------------------------------------------------------------
        if isinstance(self.platform, HorizontalMovingPlatform):
            # change the y depending on the platform
            if self.platform.moveRight:
                self.x += self.platform.speed
            else:
                self.x -= self.platform.speed
        # -------------------------------------------------------------------------------------------------------------

        # Rebuilds the hitbox -------------------------------------------------
        self.hitbox = pygame.Rect(self.x - self.enemySizeX / 2, self.y - self.enemySizeY / 2, self.enemySizeX,
                                  self.enemySizeY)

    def takeDamage(self, damage: int) -> None:
        """ Delegates call to super class method

        Parameters:
            damage: int -> the damage to be taken


        Return => None
        """
        super().takeDamage(int(damage // 2.5))


#################################################################
#                                                               #
# Weapons                                                       #
#                                                               #
#################################################################
class Gun(object):
    """ Base class for all weapons

    Attributes:
        fireRate: float
            The delay between firing bullets

        damage: int
            The damage done per bullet

        name: str
            The name of the weapon in a string

        icon: pygame.Surface
            The icon of the weapon when a chest is opened

        timeSinceFire: float
            The time of the shot being fired. Used for the fire rate of the weapon

        clipSize: int
            The number of shots that can be fired before reloading. Stays constant

        bulletsInMagazine: int
            The bullets the gun has and can still fire before a reload is needed

        canFire: bool
            If the gun can be fired

    """

    def __init__(self, fireRate: float, damage: int, clipSize: int = 1) -> None:
        self.fireRate = fireRate
        self.damage = damage
        self.name = "Gun"
        self.icon = pygame.image.load("images/weaponIcons/default/pistol.png")
        self.timeSinceFire = 0
        self.clipSize = clipSize
        self.bulletsInMagazine = self.clipSize
        self.canFire = True

    def fire(self, x, y, facingLeft):
        # if canFire and the time since the previous shot is larger than the 'fireRate' attribute and there are bullets in the magazine
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine != 0:
            # plays sound
            bulletFired.play()

            # appends bullet to list
            bullets.append(Bullet(x + 4, y + 5, 5, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed

            # subtracts bullet from 'bulletsInMagazine'
            self.bulletsInMagazine -= 1

        # reload weapon
        elif timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine == 0:
            self.bulletsInMagazine = self.clipSize


class Pistol(Gun):
    """ Default weapon for the player, which fires a 'Bullet'

    Attributes:
        fireRate: float
            The delay between firing bullets

        damage: int
            The damage done per bullet

        name: str
            The name of the weapon in a string

        canFire: bool
            If the player can fire the weapon. Used if the weapon needs to be disabled

        icon: pygame.Surface
            The icon of the weapon when a chest is opened

        timeSinceFire:
            The time of the shot being fired. Used for the fire rate of the weapon

    """

    def __init__(self) -> None:
        super().__init__(PISTOL_FIRE_RATE, PISTOL_DAMAGE)
        self.canFire = True
        self.timeSinceFire = 0
        self.icon = pygame.image.load("images/weaponIcons/default/pistol.png")
        self.name = "Pistol"

    def fire(self, x: float, y: float, facingLeft: bool) -> None:
        """ 'Fires' the gun, appending bullet to the 'bullets' list

        Parameters:
            x: float
                The x position of the bullet to be appended
                
            y: float
                The y position of the bullet to be appended
                
            facingLeft: bool
                If the player if facing left of not, which determines the direction of the bullet


        Return => None
        """
        # if canFire and the time since the previous shot is larger than the 'fireRate' attribute and there are bullets in the magazine
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine != 0:
            # plays sound
            bulletFired.play()

            # appends bullet to list
            bullets.append(Bullet(x + 4, y + 5, 5, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed

            # subtracts bullet from 'bulletsInMagazine'
            self.bulletsInMagazine -= 1

        # reload weapon
        elif timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine == 0:
            self.bulletsInMagazine = self.clipSize


class AssaultRifle(Gun):
    """ Base weapon for the assault rifle, which fires a 'Bullet'

    Attributes:
        fireRate: float
            The delay between firing bullets

        damage: int
            The damage done per bullet

        name: str
            The name of the weapon in a string

        canFire: bool
            If the player can fire the weapon. Used if the weapon needs to be disabled

        icon: pygame.Surface
            The icon of the weapon when a chest is opened

        timeSinceFire:
            The time of the shot being fired. Used for the fire rate of the weapon
    """

    def __init__(self) -> None:
        super().__init__(ASSAULT_RIFLE_FIRE_RATE, ASSAULT_RIFLE_DAMAGE)
        self.canFire = True
        self.timeSinceFire = 0
        self.icon = pygame.image.load("images/weaponIcons/default/assaultRifle.png")
        self.name = "Assault Rifle"

    def fire(self, x: float, y: float, facingLeft: bool) -> None:
        """ 'Fires' the gun, appending bullet to the 'bullets' list

        Parameters:
            x: float
                The x position of the bullet to be appended
            y: float
                The y position of the bullet to be appended
            facingLeft: bool
                If the player if facing left of not, which determines the direction of the bullet


        Return => None
        """
        # if canFire and the time since the previous shot is larger than the 'fireRate' attribute and there are bullets in the magazine
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine != 0:
            # plays sound
            bulletFired.play()

            # appends bullet to list
            bullets.append(Bullet(x + 4, y + 5, 8, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed

            # subtracts bullet from 'bulletsInMagazine'
            self.bulletsInMagazine -= 1

        # reload weapon
        elif timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine == 0:
            self.bulletsInMagazine = self.clipSize

class SubMachineGun(Gun):
    """ Base weapon for the sub machine gun, which fires a 'Bullet'

    Attributes:
        fireRate: float
            The delay between firing bullets

        damage: int
            The damage done per bullet

        name: str
            The name of the weapon in a string

        canFire: bool
            If the player can fire the weapon. Used if the weapon needs to be disabled

        icon: pygame.Surface
            The icon of the weapon when a chest is opened

        timeSinceFire:
            The time of the shot being fired. Used for the fire rate of the weapon
    """

    def __init__(self) -> None:
        super().__init__(7, 18, 30)
        self.canFire = True
        self.reloadTime = 0.03
        self.timeSinceFire = 0
        self.icon = pygame.image.load("images/weaponIcons/default/submachineGun.png")
        self.name = "Sub-Machine Gun"

    def fire(self, x: float, y: float, facingLeft: bool) -> None:
        """ 'Fires' the gun, appending bullet to the 'bullets' list

        Parameters:
            x: float
                The x position of the bullet to be appended
            y: float
                The y position of the bullet to be appended
            facingLeft: bool
                If the player if facing left of not, which determines the direction of the bullet


        Return => None
        """
        # if canFire and the time since the previous shot is larger than the 'fireRate' attribute and there are bullets in the magazine
        if self.canFire and timeElapsed - self.timeSinceFire > self.reloadTime and self.bulletsInMagazine != 0:
            # changes volume as machine gun fire rate might lead to the sound being too loud
            bulletFired.set_volume(0.2)

            # plays sound
            bulletFired.play()
            bulletFired.set_volume(0.4)

            # appends bullet to list
            bullets.append(Bullet(x + 4, y + randint(-1, 9), 8, facingLeft, self.damage))


            # records time of shot
            self.timeSinceFire = timeElapsed

            # subtracts bullet from 'bulletsInMagazine'
            self.bulletsInMagazine -= 1

        # reload weapon
        elif timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine == 0:
            self.bulletsInMagazine = self.clipSize


class MachineGun(Gun):
    """ Base weapon for the machine gun, which fires a 'Bullet'

    Attributes:
        fireRate: float
            The delay between firing bullets

        damage: int
            The damage done per bullet

        name: str
            The name of the weapon in a string

        canFire: bool
            If the player can fire the weapon. Used if the weapon needs to be disabled

        icon: pygame.Surface
            The icon of the weapon when a chest is opened

        timeSinceFire:
            The time of the shot being fired. Used for the fire rate of the weapon
    """

    def __init__(self) -> None:
        super().__init__(MACHINE_GUN_FIRE_RATE, MACHINE_GUN_DAMAGE)
        self.canFire = True
        self.timeSinceFire = 0
        self.icon = pygame.image.load("images/weaponIcons/default/machineGun.png")
        self.name = "Machine Gun"

    def fire(self, x: float, y: float, facingLeft: bool) -> None:
        """ 'Fires' the gun, appending bullet to the 'bullets' list

        Parameters:
            x: float
                The x position of the bullet to be appended
            y: float
                The y position of the bullet to be appended
            facingLeft: bool
                If the player if facing left of not, which determines the direction of the bullet


        Return => None
        """
        # if canFire and the time since the previous shot is larger than the 'fireRate' attribute and there are bullets in the magazine
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine != 0:
            # changes volume as machine gun fire rate might lead to the sound being too loud
            bulletFired.set_volume(0.2)

            # plays sound
            bulletFired.play()
            bulletFired.set_volume(0.4)

            # appends bullet to list
            bullets.append(Bullet(x + 4, y + randint(-1, 9), 8, facingLeft, self.damage))


            # records time of shot
            self.timeSinceFire = timeElapsed

            # subtracts bullet from 'bulletsInMagazine'
            self.bulletsInMagazine -= 1

        # reload weapon
        elif timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine == 0:
            self.bulletsInMagazine = self.clipSize


class Shotgun(Gun):
    """ Base weapon for the shotgun, which fires a 'ShotgunBullet'

    ...
    Attributes:
        fireRate: float
            The delay between firing bullets

        damage: int
            The damage done per bullet

        name: str
            The name of the weapon in a string

        canFire: bool
            If the player can fire the weapon. Used if the weapon needs to be disabled

        icon: pygame.Surface
            The icon of the weapon when a chest is opened

        timeSinceFire:
            The time of the shot being fired. Used for the fire rate of the weapon

    """

    def __init__(self) -> None:
        super().__init__(SHOTGUN_FIRE_RATE, SHOTGUN_DAMAGE)
        self.canFire = True
        self.timeSinceFire = 0
        self.icon = pygame.image.load("images/weaponIcons/default/shotgun.png")
        self.name = "Shotgun"

    def fire(self, x: float, y: float, facingLeft: bool) -> None:
        """ 'Fires' the gun, appending bullet to the 'bullets' list

        Parameters:
            x: float
                The x position of the bullet to be appended
            y: float
                The y position of the bullet to be appended
            facingLeft: bool
                If the player if facing left of not, which determines the direction of the bullet


        Return => None
        """
        # if canFire and the time since the previous shot is larger than the 'fireRate' attribute and there are bullets in the magazine
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine != 0:

            # plays sound
            shotgunFired.play()

            # appends bullet to list
            bullets.append(ShotgunBullet(x + 12, y + 5, facingLeft, self.damage))

            # plays sound
            self.timeSinceFire = timeElapsed

            # subtracts bullet from 'bulletsInMagazine'
            self.bulletsInMagazine -= 1

        # reload weapon
        elif timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine == 0:
            self.bulletsInMagazine = self.clipSize


class SniperRifle(Gun):
    """ Base weapon for the Sniper, which fires a 'Bullet'

    Attributes:
        fireRate: float
            The delay between firing bullets

        damage: int
            The damage done per bullet

        name: str
            The name of the weapon in a string

        canFire: bool
            If the player can fire the weapon. Used if the weapon needs to be disabled

        icon: pygame.Surface
            The icon of the weapon when a chest is opened

        timeSinceFire:
            The time of the shot being fired. Used for the fire rate of the weapon

    """

    def __init__(self) -> None:
        super().__init__(SNIPER_FIRE_RATE, SNIPER_DAMAGE)
        self.canFire = True
        self.timeSinceFire = 0
        self.icon = pygame.image.load("images/weaponIcons/default/sniper.png")
        self.name = "Sniper Rifle"

    def fire(self, x: float, y: float, facingLeft: bool) -> None:
        """ 'Fires' the gun, appending bullet to the 'bullets' list

        Parameters:
            x: float
                The x position of the bullet to be appended
            y: float
                The y position of the bullet to be appended
            facingLeft: bool
                If the player if facing left of not, which determines the direction of the bullet


        Return => None
        """
        # if canFire and the time since the previous shot is larger than the 'fireRate' attribute and there are bullets in the magazine
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine != 0:
            # plays sound
            bulletFired.play()

            # appends bullet to list
            bullets.append(Bullet(x + 12, y + 5, 12, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed

            # subtracts bullet from 'bulletsInMagazine'
            self.bulletsInMagazine -= 1

        # reload weapon
        elif timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine == 0:
            self.bulletsInMagazine = self.clipSize


class GrenadeLauncher(Gun):
    """ Base weapon for the Grenade Launcher, which fires a 'Grenade'

    Attributes:
        fireRate: float
            The delay between firing bullets

        damage: int
            The damage done per bullet

        name: str
            The name of the weapon in a string

        canFire: bool
            If the player can fire the weapon. Used if the weapon needs to be disabled

        icon: pygame.Surface
            The icon of the weapon when a chest is opened

        timeSinceFire:
            The time of the shot being fired. Used for the fire rate of the weapon
    """

    def __init__(self) -> None:
        super().__init__(GRENADE_LAUNCHER_FIRE_RATE, GRENADE_LAUNCHER_DAMAGE)
        self.canFire = True
        self.timeSinceFire = 0
        self.icon = pygame.image.load("images/weaponIcons/default/grenadeLauncher.png")
        self.name = "Grenade Launcher"

    def fire(self, x: float, y: float, facingLeft: bool) -> None:
        """ 'Fires' the gun, appending bullet to the 'bullets' list

        Parameters:
            x: float
                The x position of the bullet to be appended
            y: float
                The y position of the bullet to be appended
            facingLeft: bool
                If the player if facing left of not, which determines the direction of the bullet


        Return => None
        """
        # if canFire and the time since the previous shot is larger than the 'fireRate' attribute and there are bullets in the magazine
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine != 0:
            # plays sound
            bulletFired.play()

            # appends grenade to list
            grenades.append(Grenade(x + 4, y - 8, 4, -8, 0.25, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed

            # subtracts bullet from 'bulletsInMagazine'
            self.bulletsInMagazine -= 1

        # reload weapon
        elif timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine == 0:
            self.bulletsInMagazine = self.clipSize


class MissileLauncher(Gun):
    """ Base weapon for the Missile Launcher, which fires a 'Missile'

    Attributes:
        fireRate: float
            The time for the magazine to reload

        reloadTime: float
            The delay between firing bullets

        damage: int
            The damage done per bullet

        name: str
            The name of the weapon in a string

        canFire: bool
            If the player can fire the weapon. Used if the weapon needs to be disabled

        icon: pygame.Surface
            The icon of the weapon when a chest is opened

        timeSinceFire:
            The time of the shot being fired. Used for the fire rate of the weapon
    """

    def __init__(self) -> None:
        super().__init__(7.5, 160, 4)
        self.reloadTime = 0.5
        self.canFire = True
        self.timeSinceFire = 0
        self.icon = pygame.image.load("images/weaponIcons/default/missileLauncher.png")
        self.name = "Missile Launcher"

    def fire(self, x: float, y: float, facingLeft: bool) -> None:
        """ 'Fires' the gun, appending bullet to the 'bullets' list

        Parameters:
            x: float
                The x position of the bullet to be appended
            y: float
                The y position of the bullet to be appended
            facingLeft: bool
                If the player if facing left of not, which determines the direction of the bullet


        Return => None
        """
        # if canFire and the time since the previous shot is larger than the 'fireRate' attribute and there are bullets in the magazine
        if self.canFire and timeElapsed - self.timeSinceFire > self.reloadTime and self.bulletsInMagazine != 0:
            # plays sound
            bulletFired.play()

            # appends bullet to list
            if facingLeft:
                grenades.append(Missile(x - 40, y - 8, 8, facingLeft, self.damage))
            else:
                grenades.append(Missile(x + 4, y - 8, 8, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed

            # subtracts bullet from 'bulletsInMagazine'
            self.bulletsInMagazine -= 1

        # reload weapon
        elif timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine == 0:
            self.bulletsInMagazine = self.clipSize


class FlameThrower(Gun):
    """ Base weapon for the flamethrower, which fires a 'Flame'

    ...
    Attributes:
        fireRate: float
            The delay between firing bullets

        damage: int
            The damage done per bullet

        name: str
            The name of the weapon in a string

        canFire: bool
            If the player can fire the weapon. Used if the weapon needs to be disabled

        icon: pygame.Surface
            The icon of the weapon when a chest is opened

        timeSinceFire:
            The time of the shot being fired. Used for the fire rate of the weapon

        playSound:
            If the previous sound played is over and a new one can be played

    """

    def __init__(self) -> None:
        super().__init__(0.015, 15)
        self.canFire = True
        self.timeSinceFire = 0
        self.clipSize = 100
        self.icon = pygame.image.load("images/weaponIcons/default/flameThrower.png")
        self.name = "Flamethrower"
        self.flameStage = 0
        self.playSound = True

    def fire(self, x: float, y: float, facingLeft: bool) -> None:
        """ 'Fires' the gun, appending bullet to the 'bullets' list

        Parameters:
            x: float
                The x position of the bullet to be appended
            y: float
                The y position of the bullet to be appended
            facingLeft: bool
                If the player if facing left of not, which determines the direction of the bullet


        Return => None
        """
        if self.flameStage >= 3:
            self.flameStage = 0

        # if canFire and the time since the previous shot is larger than the 'fireRate' attribute and there are bullets in the magazine
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine != 0:

            # plays sound
            flameSound.play()

            # appends bullet to list
            bullets.append(Flame(x + 12, y + 5, facingLeft, self.damage, int(self.flameStage)))

            # records time
            self.timeSinceFire = timeElapsed

            # increments 'flameStage'
            self.flameStage += 0.25

            # subtracts bullet from 'bulletsInMagazine'
            self.bulletsInMagazine -= 1

        # reload weapon
        elif timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine == 0:
            self.bulletsInMagazine = self.clipSize


class PlasmaCannon(Gun):
    """ Base weapon for the Plasma Cannon, which fires a 'PlasmaBall'

    Attributes:
        fireRate: float
            The time for the magazine to reload

        reloadTime: float
            The delay between firing bullets

        damage: int
            The damage done per bullet

        name: str
            The name of the weapon in a string

        canFire: bool
            If the player can fire the weapon. Used if the weapon needs to be disabled

        icon: pygame.Surface
            The icon of the weapon when a chest is opened

        timeSinceFire:
            The time of the shot being fired. Used for the fire rate of the weapon
    """

    def __init__(self) -> None:
        super().__init__(6.5, 600, 4)
        self.reloadTime = 0.5
        self.canFire = True
        self.timeSinceFire = 0
        self.icon = pygame.image.load("images/weaponIcons/laser/plasmaCannon.png")
        self.name = "Plasma Cannon"

    def fire(self, x: float, y: float, facingLeft: bool) -> None:
        """ 'Fires' the gun, appending bullet to the 'bullets' list

        Parameters:
            x: float
                The x position of the bullet to be appended
            y: float
                The y position of the bullet to be appended
            facingLeft: bool
                If the player if facing left of not, which determines the direction of the bullet


        Return => None
        """
        # if canFire and the time since the previous shot is larger than the 'fireRate' attribute and there are bullets in the magazine
        if self.canFire and timeElapsed - self.timeSinceFire > self.reloadTime and self.bulletsInMagazine != 0:
            # plays sound
            bulletFired.play()

            # appends bullet to list
            if facingLeft:
                grenades.append(PlasmaBall(x - 106, y - 8, 8, facingLeft, self.damage))
            else:
                grenades.append(PlasmaBall(x - 16, y - 8, 8, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed

            # subtracts bullet from 'bulletsInMagazine'
            self.bulletsInMagazine -= 1

        # reload weapon
        elif timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine == 0:
            self.bulletsInMagazine = self.clipSize




class LaserPistol(Gun):
    """ Class representing the Laser Pistol, which fires a 'LaserBullet'

    ...
    Attributes:
        fireRate: float
            The delay between firing bullets

        damage: int
            The damage done per bullet

        name: str
            The name of the weapon in a string

        canFire: bool
            If the player can fire the weapon. Used if the weapon needs to be disabled

        icon: pygame.Surface
            The icon of the weapon when a chest is opened

        timeSinceFire:
            The time of the shot being fired. Used for the fire rate of the weapon
    """

    def __init__(self) -> None:
        super().__init__(1.5, 60)
        self.canFire = True
        self.timeSinceFire = 0
        self.icon = pygame.image.load("images/weaponIcons/laser/pistol.png")
        self.name = "Laser Pistol"

    def fire(self, x: float, y: float, facingLeft: bool) -> None:
        """ 'Fires' the gun, appending bullet to the 'bullets' list

        Parameters:
            x: float
                The x position of the bullet to be appended
            y: float
                The y position of the bullet to be appended
            facingLeft: bool
                If the player if facing left of not, which determines the direction of the bullet


        Return => None
        """
        # if canFire and the time since the previous shot is larger than the 'fireRate' attribute and there are bullets in the magazine
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine != 0:
            # plays sound
            laserFiredSound.play()

            # appends bullet to list
            bullets.append(LaserBullet(x + 4, y + 5, 8, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed

            # subtracts bullet from 'bulletsInMagazine'
            self.bulletsInMagazine -= 1

        # reload weapon
        elif timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine == 0:
            self.bulletsInMagazine = self.clipSize


class LaserAssaultRifle(Gun):
    """ Class representing the laser assault rifle, which fires a 'LaserBullet'

    ...
    Attributes:
        fireRate: float
            The delay between firing bullets

        damage: int
            The damage done per bullet

        name: str
            The name of the weapon in a string

        canFire: bool
            If the player can fire the weapon. Used if the weapon needs to be disabled

        icon: pygame.Surface
            The icon of the weapon when a chest is opened

        timeSinceFire:
            The time of the shot being fired. Used for the fire rate of the weapon
    """

    def __init__(self) -> None:
        super().__init__(0.4, 35)
        self.canFire = True
        self.timeSinceFire = 0
        self.icon = pygame.image.load("images/weaponIcons/laser/assaultRifle.png")
        self.name = "Laser Assault Rifle"

    def fire(self, x: float, y: float, facingLeft: bool) -> None:
        """ 'Fires' the gun, appending bullet to the 'bullets' list

        Parameters:
            x: float
                The x position of the bullet to be appended
            y: float
                The y position of the bullet to be appended
            facingLeft: bool
                If the player if facing left of not, which determines the direction of the bullet


        Return => None
        """
        # if canFire and the time since the previous shot is larger than the 'fireRate' attribute and there are bullets in the magazine
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine != 0:
            # plays sound
            laserFiredSound.play()

            # appends bullet to list
            bullets.append(LaserBullet(x + 4, y + 5, 8, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed

            # subtracts bullet from 'bulletsInMagazine'
            self.bulletsInMagazine -= 1

        # reload weapon
        elif timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine == 0:
            self.bulletsInMagazine = self.clipSize


class LaserMachineGun(Gun):
    """ Class representing laser the machine gun, which fires a 'LaserBullet'

    Attributes:
        fireRate: float
            The delay between firing bullets

        damage: int
            The damage done per bullet

        name: str
            The name of the weapon in a string

        canFire: bool
            If the player can fire the weapon. Used if the weapon needs to be disabled

        icon: pygame.Surface
            The icon of the weapon when a chest is opened

        timeSinceFire:
            The time of the shot being fired. Used for the fire rate of the weapon
    """

    def __init__(self) -> None:
        super().__init__(0.1, 20)
        self.canFire = True
        self.timeSinceFire = 0
        self.icon = pygame.image.load("images/weaponIcons/laser/machineGun.png")
        self.name = "Laser Machine Gun"

    def fire(self, x: float, y: float, facingLeft: bool) -> None:
        """ 'Fires' the gun, appending bullet to the 'bullets' list

        Parameters:
            x: float
                The x position of the bullet to be appended
            y: float
                The y position of the bullet to be appended
            facingLeft: bool
                If the player if facing left of not, which determines the direction of the bullet


        Return => None
        """
        # if canFire and the time since the previous shot is larger than the 'fireRate' attribute and there are bullets in the magazine
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine != 0:
            # plays sound
            laserFiredSound.play()

            # appends bullet to list
            bullets.append(LaserBullet(x + 4, y + 5, 8, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed

            # subtracts bullet from 'bulletsInMagazine'
            self.bulletsInMagazine -= 1

        # reload weapon
        elif timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine == 0:
            self.bulletsInMagazine = self.clipSize


class LaserShotgun(Gun):
    """ Class representing the laser shotgun, which fires a 'LaserShotgunBullet'

    Attributes:
        fireRate: float
            The delay between firing bullets

        damage: int
            The damage done per bullet

        name: str
            The name of the weapon in a string

        canFire: bool
            If the player can fire the weapon. Used if the weapon needs to be disabled

        icon: pygame.Surface
            The icon of the weapon when a chest is opened

        timeSinceFire:
            The time of the shot being fired. Used for the fire rate of the weapon
    """

    def __init__(self) -> None:
        super().__init__(3.5, 450)
        self.canFire = True
        self.timeSinceFire = 0
        self.icon = pygame.image.load("images/weaponIcons/laser/shotgun.png")
        self.name = "Laser Shotgun"

    def fire(self, x: float, y: float, facingLeft: bool) -> None:
        """ 'Fires' the gun, appending bullet to the 'bullets' list

        Parameters:
            x: float
                The x position of the bullet to be appended
            y: float
                The y position of the bullet to be appended
            facingLeft: bool
                If the player if facing left of not, which determines the direction of the bullet


        Return => None
        """
        # if canFire and the time since the previous shot is larger than the 'fireRate' attribute and there are bullets in the magazine
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine != 0:
            # plays sound
            laserFiredSound.play()

            # appends bullet to list
            bullets.append(LaserShotgunBullet(x + 12, y + 5, 0, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed

            # subtracts bullet from 'bulletsInMagazine'
            self.bulletsInMagazine -= 1

        # reload weapon
        elif timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine == 0:
            self.bulletsInMagazine = self.clipSize


class LaserSniperRifle(Gun):
    """ Class representing the laser sniper rifle, which fires a 'Laser' projectile

    Attributes:
        fireRate: float
            The delay between firing bullets

        damage: int
            The damage done per bullet

        name: str
            The name of the weapon in a string

        canFire: bool
            If the player can fire the weapon. Used if the weapon needs to be disabled

        icon: pygame.Surface
            The icon of the weapon when a chest is opened

        timeSinceFire:
            The time of the shot being fired. Used for the fire rate of the weapon
    """

    def __init__(self) -> None:
        super().__init__(5, 320)
        self.canFire = True
        self.timeSinceFire = 0
        self.icon = pygame.image.load("images/weaponIcons/laser/sniperRifle.png")
        self.name = "Laser Sniper Rifle"

    def fire(self, x: float, y: float, facingLeft: bool) -> None:
        """ 'Fires' the gun, appending bullet to the 'bullets' list

        Parameters:
            x: float
                The x position of the bullet to be appended
            y: float
                The y position of the bullet to be appended
            facingLeft: bool
                If the player if facing left of not, which determines the direction of the bullet


        Return => None
        """
        # if canFire and the time since the previous shot is larger than the 'fireRate' attribute and there are bullets in the magazine
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine != 0:
            # plays sound
            sniperLaserFired.play()

            # appends bullet to list
            bullets.append(LaserBullet(x + 12, y + 5, 12, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed

            # subtracts bullet from 'bulletsInMagazine'
            self.bulletsInMagazine -= 1

        # reload weapon
        elif timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine == 0:
            self.bulletsInMagazine = self.clipSize


class LaserCannon(Gun):
    """ A class representing a Laser Cannon, which fires a 'LaserBeam'

    Attributes:
        fireRate: float
            The delay between firing bullets

        damage: int
            The damage done per bullet

        name: str
            The name of the weapon in a string

        canFire: bool
            If the player can fire the weapon. Used if the weapon needs to be disabled

        icon: pygame.Surface
            The icon of the weapon when a chest is opened

        timeSinceFire:
            The time of the shot being fired. Used for the fire rate of the weapon

    """

    def __init__(self) -> None:
        super().__init__(4, 240)
        self.canFire = True
        self.icon = pygame.image.load("images/weaponIcons/laser/cannon.png")
        self.name = "Laser Cannon"

    def fire(self, x: float, y: float, facingLeft: bool) -> None:
        """ 'Fires' the gun, appending bullet to the 'bullets' list

        Parameters:
            x: float
                The x position of the bullet to be appended
            y: float
                The y position of the bullet to be appended
            facingLeft: bool
                If the player if facing left of not, which determines the direction of the bullet


        Return => None
        """
        # if canFire and the time since the previous shot is larger than the 'fireRate' attribute and there are bullets in the magazine
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine != 0:
            # plays sound
            laserFiredSound.play()

            # appends bullet to list
            bullets.append(LaserBeam(x - 4, y - 10, facingLeft, self.damage, int(x - 10)))

            # records time of shot
            self.timeSinceFire = timeElapsed

            # subtracts bullet from 'bulletsInMagazine'
            self.bulletsInMagazine -= 1

        # reload weapon
        elif timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine == 0:
            self.bulletsInMagazine = self.clipSize


class LightningStaff(Gun):
    """ A class representing a Lightning Staff, which fires a 'Lightning' projectile

    Attributes:
        fireRate: float
            The delay between firing bullets

        damage: int
            The damage done per bullet

        name: str
            The name of the weapon in a string

        canFire: bool
            If the player can fire the weapon. Used if the weapon needs to be disabled

        icon: pygame.Surface
            The icon of the weapon when a chest is opened

        timeSinceFire:
            The time of the shot being fired. Used for the fire rate of the weapon

    """

    def __init__(self) -> None:
        super().__init__(4.5, 40)
        self.canFire = True
        self.icon = pygame.image.load("images/weaponIcons/staff/lightningStaff.png")
        self.name = "Lightning Staff"

    def fire(self, x: float, y: float, facingLeft: bool) -> None:
        """ 'Fires' the gun, appending bullet to the 'bullets' list

        Parameters:
            x: float
                The x position of the bullet to be appended
            y: float
                The y position of the bullet to be appended
            facingLeft: bool
                If the player if facing left of not, which determines the direction of the bullet


        Return => None
        """
        # if canFire and the time since the previous shot is larger than the 'fireRate' attribute and there are bullets in the magazine
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine != 0:

            # appends bullet to list
            bullets.append(Lightning(x + 4, y + 5, facingLeft, self.damage, int(y + 50)))

            # records time of shot
            self.timeSinceFire = timeElapsed

            # subtracts bullet from 'bulletsInMagazine'
            self.bulletsInMagazine -= 1

        # reload weapon
        elif timeElapsed - self.timeSinceFire > self.fireRate and self.bulletsInMagazine == 0:
            self.bulletsInMagazine = self.clipSize


#################################################################
#                                                               #
# Projectiles                                                   #
#                                                               #
#################################################################
class Projectile(object):
    """ The base class of a projectile

    Attributes:
        x: float
            The x position of the projectile

        y: float
            The y position of the projectile

        speedX: float
            The speed of the projectile in the x direction

        movingLeft: bool
            True if the projectile is moving left and False otherwise

        damage: int
            The damage caused upon collision of a projectile
    """

    def __init__(self, x: float, y: float, speedX: float, movingLeft: bool, damage: int) -> None:
        self.x = x
        self.y = y
        self.speedX = speedX
        self.movingLeft = movingLeft
        self.damage = damage

    def move(self) -> None:
        """ Moves the projectile depending on if the projectile is moving left or right

        Parameters:


        Return => None
        """
        if self.movingLeft:
            self.x -= self.speedX

        else:
            self.x += self.speedX


class Bullet(Projectile):
    """ A class representing a bullet, which travels across the screen

    Attributes:
        x: float
            The x position of the projectile

        y: float
            The y position of the projectile

        speedX: float
            The speed of the projectile in the x direction

        movingLeft: bool
            True if the projectile is moving left and False otherwise

        hitbox: pygame.Surface
            The hitbox of the bullet

        image: pygame.Surface
            The image of the bullet

        damage: int
            The damage caused upon collision of a projectile
    """

    def __init__(self, x: float, y: float, speedX: float, movingLeft: bool, damage: int) -> None:
        super().__init__(x, y, speedX, movingLeft, damage)
        self.hitbox = pygame.Rect(self.x, self.y, 10, 8)
        self.image = pygame.image.load("images/character/bullet/bullet.png")

    def move(self) -> None:
        """ Moves the projectile depending on if the projectile is moving left or right.
            Also rebuilds the hitbox of the bullet

        Parameters:


        Return => None
        """
        # moves the bullet left or right depending on the 'movingLeft' boolean
        if self.movingLeft:
            self.x -= self.speedX

        else:
            self.x += self.speedX

        # Rebuilds hit box
        self.hitbox = pygame.Rect(self.x, self.y, 10, 8)

    def draw(self) -> None:
        """ Draws the bullet at the x and y positions

        Parameters:


        Return => None
        """
        # draws the bullet left or right depending on the 'movingLeft' boolean
        if self.movingLeft:
            gameWindow.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))

        else:
            gameWindow.blit(self.image, (self.x, self.y))


class ShotgunBullet(Projectile):
    """ A class representing a shotgun bullet, which has has a stationary area of damage

    Attributes:
        x: float
            The x position of the projectile

        y: float
            The y position of the projectile

        movingLeft: bool
            True if the projectile is moving left and False otherwise

        hitbox: pygame.Surface
            The hitbox of the shotgun bullet

        muzzleFlash: list[pygame.Surface]
            The animation images of the shotgun bullet

        muzzleFlashStage: int
            Keeps track of which image in 'muzzleFlash' is being drawn

        damage: int
            The damage caused upon collision of a projectile
    """

    def __init__(self, x: float, y: float, movingLeft: bool, damage: int) -> None:
        super().__init__(x, y, 0, movingLeft, damage)
        self.muzzleFlash = [
            pygame.image.load(f"images/character/shotgun/shotgunMuzzle{i}.png") for i in range(1, 6)
        ]
        self.muzzleFlashStage = 0
        self.currentImage = self.muzzleFlash[0]
        self.hitbox = pygame.Rect((self.x, self.y - 10, 50, 50))

    def draw(self) -> None:
        """ Draws the bullet and bullet animation at the x and y positions

        Parameters:


        Return => None
        """
        # resets animation if 'muzzleFlashStage' will cause an error
        if self.muzzleFlashStage >= len(self.muzzleFlash) * 2 - 1:
            self.muzzleFlashStage = 0

        # Sets the rotation for the image based on if the player if facing left
        self.currentImage = self.muzzleFlash[int(self.muzzleFlashStage // 2)]

        # blits image depending on which way the player is facing
        if self.movingLeft:
            gameWindow.blit(pygame.transform.flip(self.currentImage, True, False), (self.x - 45, self.y - 10))

        else:
            gameWindow.blit(self.currentImage, (self.x, self.y - 10))

        # increments animation stage
        self.muzzleFlashStage += 1

        # Rebuilds hit box depending on the player's direction
        if self.movingLeft:
            self.hitbox = pygame.Rect(self.x - 85, self.y - 10, 50, 50)

        else:
            self.hitbox = pygame.Rect(self.x, self.y - 10, 50, 50)


class Flame(Projectile):
    """ A class representing a flame, which is shot from a flamethrower.
        It does not move on its own, but follows the flamethrower

    Attributes:
        x: float
            The x position of the projectile

        y: float
            The y position of the projectile

        movingLeft: bool
            True if the projectile is moving left and False otherwise

        hitbox: pygame.Surface
            The hitbox of the shotgun bullet

        flameImages: list[pygame.Surface]
            The animation images of the shotgun bullet

        flameImageStage: int
            Keeps track of which image in 'muzzleFlash' is being drawn

        fired: bool
            If the weapon is fired, as there is a closing animation when the weapon is no longer fired

        damage: int
            The damage caused upon collision of a projectile
    """

    def __init__(self, x: float, y: float, movingLeft: bool, damage: int, stage: int = 0) -> None:
        super().__init__(x, y, 0, movingLeft, damage)
        self.flameImages = [pygame.image.load(f"images/character/flamethrower/flame{i}.png") for i in range(1, 4)]
        self.flameImageStage = stage
        self.currentImage = self.flameImages[self.flameImageStage]
        self.fired = True
        self.hitbox = pygame.Rect((self.x, self.y - 10, 50, 50))

    def draw(self) -> None:
        """ Draws the flame and flame animation at the x and y positions

        Parameters:


        Return => None
        """
        # Sets the rotation for the image based on if the player if facing left
        self.currentImage = self.flameImages[int(self.flameImageStage)]

        # blits image depending on which way the player is facing
        if self.movingLeft:
            gameWindow.blit(pygame.transform.flip(self.currentImage, True, False), (self.x - 110, self.y - 18))

        else:
            gameWindow.blit(self.currentImage, (self.x - 10, self.y - 18))

        # Rebuilds hit box depending on the player's direction
        if self.movingLeft:
            self.hitbox = pygame.Rect(self.x - 85, self.y - 10, 50, 50)

        else:
            self.hitbox = pygame.Rect(self.x, self.y - 10, 50, 50)

        self.fired = False


class LaserBullet(Projectile):
    """ A class representing a laser bullet, whcih travels across the screen, but also pierces through enemies

    Attributes:
        x: float
            The x position of the projectile

        y: float
            The y position of the projectile

        speedX: float
            The speed of the projectile in the x direction

        movingLeft: bool
            True if the projectile is moving left and False otherwise

        hitbox: pygame.Surface
            The hitbox of the laser

        image: pygame.Surface
            The image of the laser

        damage: int
            The damage caused upon collision of a projectile
    """

    def __init__(self, x: float, y: float, speedX: float, movingLeft: bool, damage: int) -> None:
        super().__init__(x, y, speedX, movingLeft, damage)
        self.hitbox = pygame.Rect(self.x, self.y, 25, 8)
        self.image = pygame.image.load("images/character/laser/laser.png")

    def move(self) -> None:
        """ Moves the projectile depending on if the projectile is moving left or right.
            Also rebuilds the hitbox of the bullet

        Parameters:


        Return => None
        """
        # moves the bullet left or right depending on the 'movingLeft' boolean
        if self.movingLeft:
            self.x -= self.speedX

        else:
            self.x += self.speedX

        # Rebuilds hit box
        self.hitbox = pygame.Rect(self.x, self.y, 25, 8)

    def draw(self) -> None:
        # draws the bullet left or right depending on the 'movingLeft' boolean
        if self.movingLeft:
            gameWindow.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))

        else:
            gameWindow.blit(self.image, (self.x, self.y))


class LaserBeam(Projectile):
    """ A class representing a laser beam, which travels across the screen instantaneously

    Attributes:
        x: float
            The x position of the projectile

        y: float
            The y position of the projectile

        movingLeft: bool
            True if the projectile is moving left and False otherwise

        loopsSinceFire: int
            Incremented once every time the function is called. Used to delete bullet after a short time

        hitbox: pygame.Surface
            The hitbox of the laser

        images: pygame.Surface
            The image of the laser

        damage: int
            The damage caused upon collision of a projectile

        offset: int
            The starting point of the beam, used to scale the image appropriately
    """

    def __init__(self, x: float, y: float, movingLeft: bool, damage: int, offset: int) -> None:
        super().__init__(x, y, 0, movingLeft, damage)
        self.hitbox = pygame.Rect(self.x, self.y + 6, WIDTH, 20)
        self.loopsSinceFire = 0
        self.images = [pygame.image.load(f"images/character/laser/cannonLaser/cannonLaser{i}.png") for i in range(1, 7)]
        self.offset = offset
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i], (WIDTH - self.offset + 10, 32))

    def move(self) -> None:
        """ Rebuilds the hitbox of the laser beam and increments 'loopsSinceFire'

        Parameters:


        Return => None
        """
        # rebuilds the hitbox
        if self.movingLeft:
            self.hitbox = pygame.Rect(self.x - WIDTH, self.y + 6, WIDTH, 20)

        else:
            self.hitbox = pygame.Rect(self.x, self.y + 6, WIDTH, 20)

        self.loopsSinceFire += 1

    def draw(self) -> None:
        """ Draws the laser beam at the x and y positions

        Parameters:


        Return => None
        """
        # draws the beam left or right depending on the 'movingLeft' boolean
        if self.movingLeft:
            if self.loopsSinceFire < len(self.images) * 5 - 1:
                gameWindow.blit(pygame.transform.flip(self.images[self.loopsSinceFire // 5], True, False), (self.x - (WIDTH - self.offset + 10), self.y))
            else:
                gameWindow.blit(pygame.transform.flip(self.images[len(self.images) - 1], True, False), (self.x - (WIDTH - self.offset + 10), self.y))
        else:
            if self.loopsSinceFire < len(self.images) * 5 - 1:
                gameWindow.blit(self.images[self.loopsSinceFire // 5], (self.x, self.y))
            else:
                gameWindow.blit(self.images[len(self.images) - 1], (self.x, self.y))


class LaserShotgunBullet(Projectile):
    """ A class representing a laser shotgun bullet. Similar to a normal shotgun bullet, but the flash is blue

    Attributes:
        x: float
            The x position of the projectile

        y: float
            The y position of the projectile

        speedX: float
            The speed of the projectile in the x direction

        movingLeft: bool
            True if the projectile is moving left and False otherwise

        hitbox: pygame.Surface
            The hitbox of the shotgun bullet

        muzzleFlash: list[pygame.Surface]
            The animation images of the shotgun bullet

        muzzleFlashStage: int
            Keeps track of which image in 'muzzleFlash' is being drawn

        damage: int
            The damage caused upon collision of a projectile
    """

    def __init__(self, x: float, y: float, speedX: float, movingLeft: bool, damage: int) -> None:
        super().__init__(x, y, speedX, movingLeft, damage)
        self.muzzleFlash = [
            pygame.image.load(f"images/character/laser/shotgun/shotgunMuzzle{i}.png") for i in range(1, 6)
        ]
        self.muzzleFlashStage = 0
        self.currentImage = self.muzzleFlash[0]
        self.hitbox = pygame.Rect((self.x, self.y - 10, 50, 50))

    def draw(self) -> None:
        """ Draws the bullet at the x and y positions

        Parameters:


        Return => None
        """
        # draws the bullet left or right depending on the 'movingLeft' boolean
        if self.muzzleFlashStage >= len(self.muzzleFlash) * 2 - 1:
            self.muzzleFlashStage = 0

        # Sets the rotation for the image based on if the player if facing left
        self.currentImage = self.muzzleFlash[int(self.muzzleFlashStage // 2)]

        if self.movingLeft:
            gameWindow.blit(pygame.transform.flip(self.currentImage, True, False), (self.x - 45, self.y - 10))
        else:
            gameWindow.blit(self.currentImage, (self.x, self.y - 10))

        # increments animation stage
        self.muzzleFlashStage += 1

        # Rebuilds hit box depending on the player's direction
        if self.movingLeft:
            self.hitbox = pygame.Rect(self.x - 85, self.y - 10, 50, 50)
        else:
            self.hitbox = pygame.Rect(self.x, self.y - 10, 50, 50)


class Grenade(Projectile):
    """ A class representing a grenade, which follows a parabola until it collides with an enemy or a platform

    Attributes:
        x: float
            The x position of the projectile

        y: float
            The y position of the projectile

        speedX: float
            The speed of the projectile in the x direction

        speedY: float
            The speed of the projectile in the y direction

        accelerationY: float
            The acceleration of the grenade in the y axis

        explosionHitbox: pygame.Surface
            The box where enemies take damage. Larger than the grenade hitbox

        hitbox: pygame.Surface
            The hitbox of the grenade

        image: pygame.Surface
            The image of the grenade

        explosionAnimation: list[pygame.Surface]
            The animation images of the grenade explosion

        explosionAnimationStage: int
            The current animation image of the grenade explosion

        currentImage: pygame.Surface
            The current image to be blitted

        exploded: bool
            True if the grenade has exploded, False otherwise

        playSound: bool
            True if the sound can be played, False otherwise. Used to only play the sound once upon explosion

        damage: int
            The damage caused upon collision of a projectile

    """

    def __init__(self, x: float, y: float, speedX: float, speedY: float, accelerationY: float,
                 movingLeft: bool, damage: int) -> None:
        super().__init__(x, y, speedX, movingLeft, damage)
        self.speedY = speedY
        self.accelerationY = accelerationY
        self.hitbox = pygame.Rect(self.x - 10, self.y - 10, 26, 32)
        self.explosionHitbox = pygame.Rect(self.x - 20, self.y - 50, 66, 72)
        self.image = pygame.image.load("images/character/grenade/grenade.png")
        self.explosionAnimation = [
            pygame.image.load(f"images/character/grenade/explosion/explosion{i}.png") for i in range(1, 9)
        ]
        self.explosionAnimationStage = 0
        self.currentImage = self.image
        self.exploded = False
        self.playSound = False

    def move(self) -> None:
        """ Moves the projectile depending on if the projectile is moving left or right.
            Also rebuilds the hitbox of the grenade

        Parameters:


        Return => None
        """
        # resets 'explosionAnimationStage' if the current value will cause an error
        if self.explosionAnimationStage >= len(self.explosionAnimation) * 8 - 1 and self.exploded:
            self.explosionAnimationStage = 0

        # moves the grenade left or right depending on the 'movingLeft' boolean
        if self.movingLeft:
            self.x -= self.speedX

        else:
            self.x += self.speedX

        # Gravity
        self.speedY += self.accelerationY
        self.y += self.speedY

        # Rebuilds hit box
        self.hitbox = pygame.Rect(self.x, self.y - 20, 26, 32)
        self.explosionHitbox = pygame.Rect(self.x - 20, self.y - 50, 66, 72)

        # Animation
        if self.exploded:
            self.currentImage = self.explosionAnimation[int(self.explosionAnimationStage // 8)]
            self.explosionAnimationStage += 1
            self.speedX = 0
            self.speedY = 0
            self.accelerationY = 0
            if self.explosionAnimationStage == 1:
                grenadeExplosion.play()

        else:
            self.currentImage = self.image

    def draw(self):
        """ Draws the bullet at the x and y positions

        Parameters:


        Return => None
        """
        # draws the grenade left or right depending on the 'movingLeft' boolean
        if self.exploded:
            gameWindow.blit(self.currentImage, (self.x, self.y - 50))

        else:
            gameWindow.blit(self.currentImage, (self.x, self.y))


class Missile(Grenade):
    """ A class representing a missile - a grenade with no y velocity

    Attributes:
        x: float
            The x position of the projectile

        y: float
            The y position of the projectile

        speedX: float
            The speed of the projectile in the x direction

        speedY: float
            The speed of the projectile in the y direction

        accelerationY: float
            The acceleration of the grenade in the y axis

        explosionHitbox: pygame.Surface
            The box where enemies take damage. Larger than the grenade hitbox

        hitbox: pygame.Surface
            The hitbox of the grenade

        image: pygame.Surface
            The image of the grenade

        explosionAnimation: list[pygame.Surface]
            The animation images of the grenade explosion

        explosionAnimationStage: int
            The current animation image of the grenade explosion

        currentImage: pygame.Surface
            The current image to be blitted

        exploded: bool
            True if the grenade has exploded, False otherwise

        playSound: bool
            True if the sound can be played, False otherwise. Used to only play the sound once upon explosion

        damage: int
            The damage caused upon collision of a projectile

    """

    def __init__(self, x: float, y: float, speedX: float, movingLeft: bool, damage: int) -> None:
        super().__init__(x, y, speedX, 0, 0, movingLeft, damage)
        self.hitbox = pygame.Rect(self.x - 10, self.y - 10, 26, 32)
        self.explosionHitbox = pygame.Rect(self.x - 20, self.y - 50, 66, 72)
        self.image = pygame.image.load("images/character/missile/missile.png")
        self.explosionAnimation = [
            pygame.image.load(f"images/character/grenade/explosion/explosion{i}.png") for i in range(1, 9)
        ]
        self.explosionAnimationStage = 0
        self.currentImage = self.image
        self.exploded = False
        self.playSound = False

    def move(self) -> None:
        """ Moves the projectile depending on if the projectile is moving left or right.
            Also rebuilds the hitbox of the grenade

        Parameters:


        Return => None
        """
        # resets 'explosionAnimationStage' if the current value will cause an error
        if self.explosionAnimationStage >= len(self.explosionAnimation) * 8 - 1 and self.exploded:
            self.explosionAnimationStage = 0

        # moves the grenade left or right depending on the 'movingLeft' boolean
        if self.movingLeft:
            self.x -= self.speedX

        else:
            self.x += self.speedX

        # Gravity
        self.speedY += self.accelerationY
        self.y += self.speedY

        # Rebuilds hit box
        self.hitbox = pygame.Rect(self.x, self.y - 20, 26, 32)
        self.explosionHitbox = pygame.Rect(self.x - 20, self.y - 50, 66, 72)

        # Animation
        if self.exploded:
            self.currentImage = self.explosionAnimation[int(self.explosionAnimationStage // 8)]
            self.explosionAnimationStage += 1
            self.speedX = 0
            self.speedY = 0
            self.accelerationY = 0
            if self.explosionAnimationStage == 1:
                grenadeExplosion.play()

        else:
            self.currentImage = self.image

    def draw(self):
        """ Draws the bullet at the x and y positions

        Parameters:


        Return => None
        """
        # draws the grenade left or right depending on the 'movingLeft' boolean
        if self.exploded:
            gameWindow.blit(self.currentImage, (self.x, self.y - 50))

        else:
            if self.movingLeft:
                gameWindow.blit(pygame.transform.flip(self.currentImage, True, False), (self.x, self.y))
            else:
                gameWindow.blit(self.currentImage, (self.x, self.y))


class PlasmaBall(Grenade):
    """ A class representing a plasma ball - similar to a missile, but with a larger damage hitbox

    Attributes:
        x: float
            The x position of the projectile

        y: float
            The y position of the projectile

        speedX: float
            The speed of the projectile in the x direction

        speedY: float
            The speed of the projectile in the y direction

        accelerationY: float
            The acceleration of the grenade in the y axis

        explosionHitbox: pygame.Surface
            The box where enemies take damage. Larger than the grenade hitbox

        hitbox: pygame.Surface
            The hitbox of the grenade

        images: list[pygame.Surface]
            The image of the grenade

        explosionAnimation: list[pygame.Surface]
            The animation images of the grenade explosion

        explosionAnimationStage: int
            The current animation image of the grenade explosion

        imageStage: int
            The current animtion image of the plasma ball

        currentImage: pygame.Surface
            The current image to be blitted

        exploded: bool
            True if the grenade has exploded, False otherwise

        playSound: bool
            True if the sound can be played, False otherwise. Used to only play the sound once upon explosion

        damage: int
            The damage caused upon collision of a projectile

    """

    def __init__(self, x: float, y: float, speedX: float, movingLeft: bool, damage: int) -> None:
        super().__init__(x, y, speedX, 0, 0, movingLeft, damage)
        self.hitbox = pygame.Rect(self.x - 10, self.y - 10, 26, 32)
        self.explosionHitbox = pygame.Rect(self.x - 20, self.y - 50, 66, 72)
        self.images = [
            pygame.image.load(f"images/character/laser/plasma/ball/plasmaBall{i}.png") for i in range(1, 10)
        ]
        self.explosionAnimation = [
            pygame.image.load(f"images/character/laser/plasma/explosion/plasmaExplosion{i}.png") for i in range(1, 8)
        ]
        self.imageStage = 0
        self.explosionAnimationStage = 0
        self.currentImage = self.image
        self.exploded = False
        self.playSound = False

    def move(self) -> None:
        """ Moves the projectile depending on if the projectile is moving left or right.
            Also rebuilds the hitbox of the grenade

        Parameters:


        Return => None
        """
        # resets 'explosionAnimationStage' if the current value will cause an error
        if self.explosionAnimationStage >= len(self.explosionAnimation) * 8 - 1 and self.exploded:
            self.explosionAnimationStage = 0

        if self.imageStage >= len(self.images) * 8 - 1:
            self.imageStage = 0

        # moves the grenade left or right depending on the 'movingLeft' boolean
        if self.movingLeft:
            self.x -= self.speedX

        else:
            self.x += self.speedX

        # Gravity
        self.speedY += self.accelerationY
        self.y += self.speedY

        # Rebuilds hit box
        self.hitbox = pygame.Rect(self.x + 30, self.y - 10, 46, 34)
        self.explosionHitbox = pygame.Rect(self.x - 10, self.y - 30, 104, 84)

        # Animation
        if self.exploded:
            self.currentImage = self.explosionAnimation[int(self.explosionAnimationStage // 8)]
            self.explosionAnimationStage += 1
            self.speedX = 0
            self.speedY = 0
            self.accelerationY = 0
            if self.explosionAnimationStage == 1:
                grenadeExplosion.play()

        else:
            self.currentImage = self.images[int(self.imageStage // 8)]
            self.imageStage += 1
            

    def draw(self):
        """ Draws the bullet at the x and y positions

        Parameters:


        Return => None
        """
        # draws the grenade left or right depending on the 'movingLeft' boolean
        if self.exploded:
            gameWindow.blit(self.currentImage, (self.x, self.y - 50))

        else:
            if self.movingLeft:
                gameWindow.blit(pygame.transform.flip(self.currentImage, True, False), (self.x, self.y))
            else:
                gameWindow.blit(self.currentImage, (self.x, self.y))



class Lightning(Projectile):
    """ A class representing a beam of lightning - an "invisble" bullet that damages the
        enemy when it has the same X position as its hitbox

    Attributes:
        x: float
            The x position of the projectile

        y: float
            The y position of the projectile

        hitbox: pygame.Surface
            The hitbox of the beam

        explosionAnimation: list[pygame.Surface]
            The animation images of the beam

        explosionAnimationStage: int
            The current animation image of the beam

        collided: bool
            True if the beam has collided, False otherwise

        playSound: bool
            True if the sound can be played, False otherwise. Used to only play the sound once upon explosion

        damage: int
            The damage caused upon collision of a projectile

        offset: int
            The ending point of the lightning - used to scale the image appropriately

    """

    def __init__(self, x: float, y: float, movingLeft: bool, damage: int, offset: int) -> None:
        super().__init__(x, y, 12, movingLeft, damage)
        self.hitbox = pygame.Rect(self.x - 10, self.y - 10, 26, 32)
        self.explosionHitbox = pygame.Rect(self.x - 20, self.y - 50, 66, 72)
        self.explosionAnimation = [pygame.image.load(f"images/character/laser/lightning/lightning{i}.png") for i in range(1, 8)]
        self.offset = offset
        for i in range(len(self.explosionAnimation)):
            self.explosionAnimation[i] = pygame.transform.scale(self.explosionAnimation[i], (64, HEIGHT))

        self.explosionAnimationStage = 0
        self.collided = False
        self.playSound = False

    def move(self) -> None:
        """ Moves the projectile depending on if the projectile is moving left or right.
            Also rebuilds the hitbox of the bullet

        Parameters:


        Return => None
        """
        # resets 'explosionAnimationStage' if the current value will cause an error
        if self.explosionAnimationStage >= len(self.explosionAnimation) * 10 - 1 and self.collided:
            self.explosionAnimationStage = 0

        # moves the beam left or right depending on the 'movingLeft' boolean
        if self.movingLeft:
            self.x -= self.speedX

        else:
            self.x += self.speedX

        # Rebuilds hit box
        self.hitbox = pygame.Rect(self.x, self.y - 20, 26, 32)
        self.explosionHitbox = pygame.Rect(self.x - 20, self.y - 50, 66, 72)

    def draw(self):
        """ Draws the bullet at the x and y positions

        Parameters:


        Return => None
        """
        if self.collided:
            self.speedX = 0
            gameWindow.blit(self.explosionAnimation[int(self.explosionAnimationStage // 10)], (self.x, self.y - HEIGHT + 50))
            self.explosionAnimationStage += 1
            if self.explosionAnimationStage == 1:
                thunderSound.play()


class EnemyProjectile(Projectile):
    """ The base class of a projectile fired from an enemy, which always goes left

    Attributes:
        x: float
            The x position of the projectile

        y: float
            The y position of the projectile

        speedX: float
            The speed of the projectile in the x direction

        damage: int
            The damage caused upon collision of a projectile


    """

    def __init__(self, x: float, y: float, speedX: float, damage: int):
        super().__init__(x, y, speedX, True, damage)

    def move(self):
        """ Moves the projectile depending on if the projectile is moving left or right.

        Parameters:


        Return => None
        """
        # moves the bullet left or right depending on the 'movingLeft' boolean
        if self.movingLeft:
            self.x -= self.speedX

        else:
            self.x += self.speedX


class Icicle(EnemyProjectile):
    """ A class representing an icicle, based upon 'EnemyProjectile'. It is fired from an 'IceEnemy'

    Attributes:
        x: float
            The x position of the projectile

        y: float
            The y position of the projectile

        speedX: float
            The speed of the projectile in the x direction

        hitbox: pygame.Surface
            The hitbox of the icicle

        damage: int
            The damage caused upon collision of a projectile
    """

    def __init__(self, x, y, speedX) -> None:
        # always going left
        super().__init__(x, y, speedX, 10)
        self.image = pygame.image.load("images/enemy/ice/weapon/icicle1.png")
        self.hitbox = pygame.Rect(self.x, self.y, 16, 10)

    def move(self):
        """ Moves the projectile depending on if the projectile is moving left or right.
            Also rebuilds the hitbox of the bullet

        Parameters:


        Return => None
        """
        # moves the bullet left or right depending on the 'movingLeft' boolean
        super().move()

        # Rebuilds hit box
        self.hitbox = pygame.Rect(self.x, self.y, 13, 8)

    def draw(self):
        """ Draws the bullet at the x and y positions

        Parameters:


        Return => None
        """
        # draws the bullet left or right depending on the 'movingLeft' boolean
        if self.movingLeft:
            gameWindow.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))

        else:
            gameWindow.blit(self.image, (self.x, self.y))


class EnemyBullet(EnemyProjectile):
    """ A class representing an enemy fired bullet

    Attributes:
        x: float
            The x position of the projectile

        y: float
            The y position of the projectile

        speedX: float
            The speed of the projectile in the x direction

        hitbox: pygame.Surface
            The hitbox of the icicle

        damage: int
            The damage caused upon collision of a projectile
    """

    def __init__(self, x, y, speedX) -> None:
        # always going left
        super().__init__(x, y, speedX, 10)
        self.image = pygame.image.load("images/enemy/boss/weapon/bullet.png")
        self.image = pygame.transform.scale(self.image, (32, 16))
        self.hitbox = pygame.Rect(self.x, self.y, 32, 16)

    def move(self):
        """ Moves the projectile depending on if the projectile is moving left or right.
            Also rebuilds the hitbox of the bullet

        Parameters:


        Return => None
        """
        # moves the bullet left or right depending on the 'movingLeft' boolean
        super().move()

        # Rebuilds hit box
        self.hitbox = pygame.Rect(self.x, self.y, 32, 16)

    def draw(self):
        """ Draws the bullet at the x and y positions

        Parameters:


        Return => None
        """
        # draws the bullet left or right depending on the 'movingLeft' boolean
        if self.movingLeft:
            gameWindow.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))

        else:
            gameWindow.blit(self.image, (self.x, self.y))


class EnemyLaser(Projectile):
    """ A class representing a laser, which is fired by the enemy

    Attributes:
        x: float
            The x position of the projectile

        hitbox: pygame.Surface
            The hitbox of the beam

        explosionAnimation: list[pygame.Surface]
            The animation images of the beam

        explosionAnimationStage: int
            The current animation image of the beam

        ended: bool
            True if the beam has ended, False otherwise

        playSound: bool
            True if the sound can be played, False otherwise. Used to only play the sound once upon explosion

        damage: int
            The damage caused upon collision of a projectile

        end: float
            the ending position of the laser

    """

    def __init__(self, x: float, end: float, damage: int) -> None:
        super().__init__(x, HEIGHT, 2, False, damage)
        self.end = end
        self.hitbox = pygame.Rect(self.x - 10, 0, 27, HEIGHT)
        self.explosionAnimation = [
            pygame.image.load(f"images/character/laser/lightning/lightning{i}.png") for i in range(1, 6)
        ]

        for i in range(len(self.explosionAnimation)):
            self.explosionAnimation[i] = pygame.transform.scale(self.explosionAnimation[i], (27, HEIGHT))

        self.explosionAnimationStage = 0
        self.ended = False
        self.playSound = False

    def move(self) -> None:
        """ Moves the projectile depending on if the projectile is moving left or right.
            Also rebuilds the hitbox of the bullet

        Parameters:


        Return => None
        """
        # resets 'explosionAnimationStage' if the current value will cause an error
        if self.explosionAnimationStage < len(self.explosionAnimation) * 10 - 1 and not self.ended:
            self.explosionAnimationStage += 1

        if self.explosionAnimationStage == len(self.explosionAnimation) * 10 - 1 and not self.ended:
            self.explosionAnimationStage -= 10

        # moves the beam left or right depending on the 'movingLeft' boolean
        if self.x - self.speedX > self.end:
            self.x -= self.speedX

        elif self.x + self.speedX < self.end:
            self.x += self.speedX

        else:
            self.ended = True

        # Rebuilds hit box
        self.hitbox = pygame.Rect(self.x, 0, 27, HEIGHT)

    def draw(self):
        """ Draws the bullet at the x and y positions

        Parameters:


        Return => None
        """
        # draws the beam left or right depending on the 'movingLeft' boolean
        gameWindow.blit(self.explosionAnimation[int(self.explosionAnimationStage // 10)], (self.x, self.y - HEIGHT))


#################################################################
#                                                               #
# Player                                                        #
#                                                               #
#################################################################
class Player(object):
    """ A class that represents a player

    Attributes:
        x: float
            the x position of the player. Represents the middle point of the player.

        y: float
            the y position of the player. Represents the middle point of the player.

        health: int
            the health of the player.

        accelerationX: float
            the acceleration of the Player on the horizontal plane.

        accelerationY: float
            the acceleration of the Player on the vertical plane.

        maxSpeedX: float
            the maximum speed of the player on the horizontal plane.

        maxSpeedY: float
            the maximum speed of the player on the vertical plane.

        speedX: float
            the speed of the player on the horizontal plane.

        speedY: float
            the speed of the player on the vertical plane.

        touchingBlock: bool
            True if the player is touching a platform

        invincible: bool
            True if the player is invincible, (i.e player has just been hit by an enemy)

        facingLeft: bool
            True if the player is facing left. Used for blitting images the correct way.

        hurt, idle, jumpOrFall, running: list[pygame.Surface]
            these lists contain the images for the player animations

        hurtStage, idleStage, jumpOrFallStage, runningStage: int
            tracks the animation stage of each of the lists above

        currentImage: pygame.Surface
            the current image to be blitted

        currentWeapon: Gun
            the current weapon of the player

        damageMultiplier: float
            The increase in damage from a player; "strength"

        hitbox: pygame.Surface
            The hitbox of the player

        timeHit: float
            The time that the player is hit by an enemy - used for tracking invincibility period

        WASD: bool
            Use WASD or Arrow keys

        name: str
            The player name displayed

        nameRender: str
            The name rendered as a font
    """

    def __init__(self, health: int, accelerationX: float, accelerationY: float, maxSpeedX: float, maxSpeedY: float,
                 x: float, y: float, currentWeapon: Gun, WASD: bool, name: str) -> None:
        self.x = x
        self.y = y
        self.health = health
        self.accelerationX = accelerationX
        self.accelerationY = accelerationY
        self.maxSpeedX = maxSpeedX
        self.maxSpeedY = maxSpeedY
        self.speedX = 0
        self.speedY = 0
        self.touchingBlock = False
        self.invincible = False
        self.facingLeft = False
        self.canThrowGrenade = True
        self.currentWeapon = currentWeapon
        self.WASD = WASD
        self.name = name
        self.nameRender = playerNameFont.render(self.name, False, BLACK)
        self.timeHit = timeElapsed

        # Animation images
        self.hurt = [
            pygame.image.load("images/character/hurt/hurt1.png"),
        ]

        self.idle = [
            pygame.image.load(f"images/character/idle/idle{i}.png") for i in range(1, 3)
        ]

        self.jumpOrFall = [
            pygame.image.load("images/character/jump/jump.png"),
            pygame.image.load("images/character/jump/fall.png"),
        ]

        self.running = [
            pygame.image.load(f"images/character/running/running{i}.png") for i in range(1, 7)
        ]

        # Current image
        self.currentImage = self.idle[0]

        # Tracks the current stage of each animation
        self.hurtStage = 0
        self.idleStage = 0
        self.jumpOrFallStage = 0
        self.runningStage = 0

        # damage multiplier
        self.damageMultiplier = 1

        self.hitbox = pygame.Rect(self.x - PLAYER_SIZE_X / 2, self.y - PLAYER_SIZE_Y / 2, PLAYER_SIZE_X, PLAYER_SIZE_Y)

    def move(self) -> None:
        """ Responsible for getting keyboard input and moving the player.
            Also controls a lot of the animation images.

        Parameters:


        Return => None
        """
        # Checks to see if any current stage of any animations will cause an error and resets them if so
        self.checkAnimation()

        # If 'd' is pressed and the max speed has not exceeded the maximum speed --------------------------------------
        if (keys[pygame.K_d] and self.WASD) or (keys[pygame.K_RIGHT] and not self.WASD):
            # Sets the current image of the player depending on how long 'd' has been pressed
            self.currentImage = self.running[int(self.runningStage // 10)]

            # sets the 'facingLeft' attribute to False
            self.facingLeft = False

            # Increases speed going right -------------------------------------
            if self.speedX < self.maxSpeedX - self.accelerationX:
                if self.touchingBlock:
                    self.speedX += self.accelerationX

                else:
                    # Makes acceleration slower if the player is in the air
                    self.speedX += self.accelerationX / 4

            # Increments the running animation stage and sets the idle stage to 0
            self.runningStage += 1
            self.idleStage = 0

        # If 'a' is pressed and the max speed has not exceeded the maximum speed --------------------------------------
        elif (keys[pygame.K_a] and self.WASD) or (keys[pygame.K_LEFT] and not self.WASD):

            # Sets the current image of the player depending on how long 'a' has been pressed
            self.currentImage = pygame.transform.flip(self.running[int(self.runningStage // 10)], True, False)

            # sets the 'facingLeft' attribute to True
            self.facingLeft = True

            # Increases speed going left --------------------------------------
            if self.speedX > -self.maxSpeedX + self.accelerationX:
                if self.touchingBlock:
                    self.speedX -= self.accelerationX

                else:
                    # Makes acceleration slower if the player is in the air
                    self.speedX -= self.accelerationX / 4

            # Increments the running animation stage and sets the idle stage to 0
            self.runningStage += 1
            self.idleStage = 0


        # If neither 'a' or 'd' are pressed, slowly decreases/increase speed to 0
        else:
            # decelerate by half of the set accelerationX
            if self.speedX < 0:
                # if the current level is the ice level, decrease deceleration
                if level.background is iceBackgroundImage and self.touchingBlock:
                    self.speedX += self.accelerationX / 6
                else:
                    self.speedX += self.accelerationX / 2

            # decelerate by half of the set accelerationX
            elif self.speedX > 0:
                # if the current level is the ice level, decrease deceleration
                if level.background is iceBackgroundImage and self.touchingBlock:
                    self.speedX -= self.accelerationX / 6
                else:
                    self.speedX -= self.accelerationX / 2

            # if speed is close to 0, set the speed to 0
            if self.accelerationX * 5 > self.speedX > -self.accelerationX * 5:
                self.speedX = 0

        # If 'space' is pressed and the player is touching a block, decrease the speedY ------------------------------
        if ((keys[pygame.K_w] and self.WASD) or (keys[pygame.K_UP] and not self.WASD)) and self.touchingBlock:
            # Sets the current image to the 'jump' image
            self.currentImage = self.jumpOrFall[0]

            # Decreases the speedY
            self.speedY -= self.accelerationY

            # Sets 'touchingBlock' to False
            self.touchingBlock = False

        # If the current speed is lower or equal to the max speed and touchingBlock, increase the speed (gravity) -----
        if not self.touchingBlock and self.speedY <= self.maxSpeedY:
            self.speedY += 0.10
        else:
            self.speedY = 0

        # If idle, use the idle imaging facing right ------------------------------------------------------------------
        if 0.25 > self.speedX > -0.25 and 0.25 > self.speedY > -0.25 and not self.facingLeft:
            # The majority of the 'idle' animation is the first image
            if self.idleStage < 80:
                self.currentImage = self.idle[0]

            else:
                # 1/5 of the idle time is the second image
                self.currentImage = self.idle[1]

            # Increments 'idleStage'
            self.idleStage += 1

        # If idle, use the idle imaging facing left ------------------------------------------------------------------
        if 0.25 > self.speedX > -0.25 and 0.25 > self.speedY > -0.25 and self.facingLeft:
            # The majority of the 'idle' animation is the first image
            if self.idleStage < 80:
                self.currentImage = pygame.transform.flip(self.idle[0], True, False)
            else:
                # 1/5 of the idle time is the second image
                self.currentImage = pygame.transform.flip(self.idle[1], True, False)

            # Increments 'idleStage'
            self.idleStage += 1

        # If falling, use the falling image facing right --------------------------------------------------------------
        if self.speedY < 0.1 and not self.touchingBlock and not self.facingLeft:
            self.currentImage = self.jumpOrFall[1]


        # If jumping, use the jumping image facing right --------------------------------------------------------------
        elif self.speedY > 1.2 and not self.touchingBlock and not self.facingLeft:
            self.currentImage = self.jumpOrFall[0]

        # If falling, use the falling image facing left ---------------------------------------------------------------
        if self.speedY < 0 and not self.touchingBlock and self.facingLeft:
            self.currentImage = pygame.transform.flip(self.jumpOrFall[1], True, False)


        # If jumping, use the jumping image facing right --------------------------------------------------------------
        elif self.speedY > 1.2 and not self.touchingBlock and self.facingLeft:
            self.currentImage = pygame.transform.flip(self.jumpOrFall[0], True, False)

        # If invincible, use the 'hurt' image -------------------------------------------------------------------------
        if self.invincible:
            # flip the image if facing left
            if self.facingLeft:
                self.currentImage = pygame.transform.flip(self.hurt[0], True, False)

            else:
                self.currentImage = self.hurt[0]

        # Increase the x and y by the x and y speed
        self.y += self.speedY
        self.x += self.speedX

        # rebuilds hitbox
        self.hitbox = pygame.Rect(self.x - PLAYER_SIZE_X / 2, self.y - PLAYER_SIZE_Y / 2, PLAYER_SIZE_X, PLAYER_SIZE_Y)

    def draw(self) -> None:
        """ Draws the player with the 'x' and 'y' coordinates at the center

        Parameters:


        Return => None
        """
        # gets the width of the name
        playerNameTextWidth = playerNameFont.size(self.name)[0]

        # blits the name above the player
        gameWindow.blit(self.nameRender, (self.x - playerNameTextWidth / 2, self.y - PLAYER_SIZE_Y / 2 - 10))

        # uses 'x' and 'y' as the center
        gameWindow.blit(self.currentImage, (self.x - PLAYER_SIZE_X / 2, self.y - PLAYER_SIZE_Y / 2))

    def checkCollision(self):
        """ Kills the player if they leave the screen area

        Parameters:


        Return => None
        """
        if WIDTH - PLAYER_SIZE_X / 2 < self.x or self.x < 0:
            # Does 10 damages at a time
            self.health -= 10

        if self.y > HEIGHT - PLAYER_SIZE_Y / 2:
            # Does 10 damages at a time
            self.health -= 10

    def checkLife(self) -> bool:
        """ Returns true if the player's health is lower than 100

        Parameters:


        Return => bool: if the player's health is lower than 0 or now
        """
        if self.health <= 0:
            return True

        return False

    def takeDamage(self, amount):
        """ Returns true if the player's health is lower than 100

        Parameters:


        Return => bool: if the player's health is lower than 0 or now
        """
        playerHit.play()
        self.health -= amount

    def fireWeapon(self):
        """ Returns true if the player can fire the weapon and is holding the 'w' key.
            Also plays the sound and appends the bullet to the list

        Parameters:


        Return => bool: if the player's has fired the gun
        """

        # If 'w' is pressed and can fire ------------------------------------------------------------------------------
        if (keys[pygame.K_SPACE] and self.WASD) or (keys[pygame.K_SLASH] and not self.WASD):
            # records original damage
            originalDamage = self.currentWeapon.damage

            # applying damage multiplier
            if self.currentWeapon.damage * self.damageMultiplier > 20:
                # maximum of +20 damage
                self.currentWeapon.damage += 20

            else:
                self.currentWeapon.damage = round(self.currentWeapon.damage * self.damageMultiplier)

            # fires the weapon
            self.currentWeapon.fire(self.x + 4, self.y - 4, self.facingLeft)

            # resets the damage to the original
            self.currentWeapon.damage = originalDamage

            return True

        # -------------------------------------------------------------------------------------------------------------

        return False

    def checkAnimation(self):
        """ Resets the animation stage trackers if they will cause an IndexError

        Parameters:


        Return => bool: if the player's has fired the gun
        """
        if self.hurtStage >= len(self.hurt):
            self.hurtStage = 0

        if self.idleStage >= len(self.idle) * 50 - 1:
            self.idleStage = 0

        if self.jumpOrFallStage >= len(self.jumpOrFall):
            self.runningStage = 0

        if self.runningStage >= len(self.running) * 10 - 1:
            self.runningStage = 0

    ###################################################################################################################
    #
    # Player Collision methods
    #
    ###################################################################################################################

    def checkCollectibleCollision(self, collectibleToCheck) -> None:
        """ Checks if the player has collided with any collectibles

        Parameters:
            collectibleToCheck: Collectible
                Collectible to check collision for

        Return => None
        """
        global coinsCollected
        # creating hitbox
        collectibleHitbox = pygame.Rect(collectibleToCheck.x - COLLECTIBLE_SIZE / 2,
                                        collectibleToCheck.y - COLLECTIBLE_SIZE / 2, COLLECTIBLE_SIZE, COLLECTIBLE_SIZE)

        # If the collectible is an instance of a Coin, increment the score and collect the collectible
        if isinstance(collectibleToCheck, Coin):
            if collectibleHitbox.colliderect(self.hitbox):
                collectibleToCheck.collect()
                collectibles.pop(collectibles.index(collectibleToCheck))
                coinsCollected += 1

    def checkEnemyCollision(self, enemy) -> bool:
        """ Checks if the player has collided with an enemy

        Parameters:
            enemy: Enemy
                The enemy to check collision for


        Return => bool: whether there is a collision or not
        """
        # Gets the enemy hitboxes -------------------------------------------------------------------------------------
        enemyHitboxL = pygame.Rect(enemy.x - enemy.enemySizeX / 2, enemy.y - enemy.enemySizeY / 2, enemy.enemySizeX / 2,
                                   enemy.enemySizeY)
        enemyHitboxR = pygame.Rect(enemy.x, enemy.y - enemy.enemySizeY / 2, enemy.enemySizeX / 2, enemy.enemySizeY)
        enemyHitboxTop = pygame.Rect(enemy.x - enemy.enemySizeX / 2 + 15, enemy.y - enemy.enemySizeY / 2 - 5,
                                     enemy.enemySizeX - 30, 2)

        # -------------------------------------------------------------------------------------------------------------

        # Checks if the player has hit the left side of the enemy -----------------------------------------------------
        if self.hitbox.colliderect(enemyHitboxL) and not self.invincible and not enemy.isDead:
            # sets damage based on enemy type
            if isinstance(enemy, UnderworldEnemy):
                damage = 15
            elif isinstance(enemy, IceEnemy):
                damage = 20
            else:
                damage = 10

            self.takeDamage(damage)
            self.invincible = True
            self.x = enemy.x - enemy.enemySizeX
            self.y = enemy.y - PLAYER_SIZE_Y - 4
            # sets knockback based on enemy type
            if isinstance(enemy, UnderworldEnemy) or isinstance(enemy, IceEnemy):
                knockback = -4
            else:
                knockback = -3

            self.speedX = knockback
            self.speedY = -0.05
            self.touchingBlock = False
            return True

        # -------------------------------------------------------------------------------------------------------------

        # Checks if the player has hit the right side of the enemy ----------------------------------------------------
        elif self.hitbox.colliderect(enemyHitboxR) and not self.invincible and not enemy.isDead:
            # sets damage based on enemy type
            if isinstance(enemy, UnderworldEnemy):
                damage = 15
            elif isinstance(enemy, IceEnemy):
                damage = 20
            else:
                damage = 10

            self.takeDamage(damage)
            self.invincible = True
            self.x = enemy.x + enemy.enemySizeX
            self.y = enemy.y - PLAYER_SIZE_Y - 4

            # sets knockback based on enemy type
            if isinstance(enemy, UnderworldEnemy) or isinstance(enemy, IceEnemy):
                knockback = 4
            else:
                knockback = 3

            self.speedX = knockback
            self.speedY = -0.05
            self.touchingBlock = False
            return True

        # -------------------------------------------------------------------------------------------------------------

        # Checks if the player has hit the top side of the enemy, which damages the enemy and may damage the player ---
        elif self.hitbox.colliderect(enemyHitboxTop) and not enemy.isDead:
            enemy.takeDamage(25)
            self.speedY = -4
            self.y -= 3
            enemy.damaged = True
            self.invincle = False
            return True

        # -------------------------------------------------------------------------------------------------------------

        return False

    def checkPlatformCollision(self, levelToCheck) -> None:
        """ Checks if the player has collided with an enemy

        Parameters:
            levelToCheck: the level whose platforms to check
                The enemy to check collision for

        Return => None
        """
        onGround = False
        for platform in levelToCheck.platforms:
            groundHitbox = pygame.Rect(platform.x + 4, platform.y - 3, platform.length - 8, 2)
            # if platform.x + platform.length + PLAYER_SIZE_X / 2 > self.x > platform.x - PLAYER_SIZE_X / 2 and platform.y + 10 > self.y + PLAYER_SIZE_Y / 2 > platform.y:
            if self.hitbox.colliderect(groundHitbox):
                self.y = platform.y - PLAYER_SIZE_Y / 2
                self.speedY = 0
                onGround = True

                # If the player is on the ground and on a moving platform, it moves with the platform
                if onGround and isinstance(platform, VerticalMovingPlatform):
                    if platform.moveDown:
                        self.y += platform.speed
                    else:
                        self.y -= platform.speed

                if onGround and isinstance(platform, HorizontalMovingPlatform):
                    if platform.moveRight:
                        self.x += platform.speed
                    else:
                        self.x -= platform.speed

            # Side collisions
            platformLeftHitbox = pygame.Rect(platform.x, platform.y + 2, 1, platform.width - 4)
            platformRightHitbox = pygame.Rect(platform.x + platform.length - 1, platform.y + 2, 1, platform.width - 4)

            if self.hitbox.colliderect(platformLeftHitbox) or self.hitbox.colliderect(platformRightHitbox):
                self.speedX = 0

        self.touchingBlock = onGround

        # if self.x >= 200:
        #     moveBackground(1)

    def checkChestCollision(self, chestToCheck):
        """ Checks if the player has collided with any chests

        Parameters:
            chestToCheck: chest to check for collision

        Return => None
        """
        global coinsCollected, timeOpened

        # setting colour based on background images
        colour = BLACK if level.background is iceBackgroundImage else WHITE

        if chestToCheck.hitbox.colliderect(self.hitbox):
            # Displaying name of weapon if the chest is an instance of 'Chest' ----------------------------------------
            if isinstance(chestToCheck, WeaponChest):
                chestToCheck.opening = True
                weaponName = scoreFontSmall.render(chestToCheck.weapon.name, True, colour)
                weaponNameLength = weaponName.get_size()[0]

                # draw the '[s]' if the level is the tutorial level ---------------------------
                if levelNumber == 0 and not chestToCheck.collected:
                    pressX = scoreFontSmall.render("[s]/[.]", True, colour)
                    gameWindow.blit(pressX, ((chestToCheck.platform.x + chestToCheck.platform.length / 2 - 20), chestToCheck.platform.y + 16))

                # blitting name to screen -----------------------------------------------------
                if not chestToCheck.collected:
                    gameWindow.blit(weaponName, ((chestToCheck.platform.x + chestToCheck.platform.length / 2) - weaponNameLength / 2, chestToCheck.platform.y - 43))

                # picking up the weapon -------------------------------------------------------
                if (keys[pygame.K_s] and self.WASD) or (keys[pygame.K_PERIOD] and not self.WASD):
                    self.currentWeapon = chestToCheck.weapon
                    if not chestToCheck.collected:
                        pickupWeapon.play()
                    chestToCheck.collected = True

            # Displaying name of upgrade if the chest is an instance of 'UpgradeChest' --------------------------------
            if isinstance(chestToCheck, UpgradeChest):
                if not chestToCheck.opening:
                    costRender = scoreFontSmall.render(f"{POTION_COST} coins", True, colour)
                    costRenderLength = costRender.get_size()[0]
                    gameWindow.blit(costRender, (chestToCheck.platform.x + chestToCheck.platform.length / 2 - costRenderLength / 2, chestToCheck.platform.y - 48))

                if ((keys[pygame.K_s] and self.WASD) or (
                        keys[pygame.K_PERIOD] and not self.WASD)) and not chestToCheck.opening:
                    timeOpened = timeElapsed
                    if coinsCollected >= POTION_COST:
                        coinsCollected -= POTION_COST
                        chestToCheck.opening = True
                    else:
                        notEnoughCoins.stop()
                        notEnoughCoins.play()

                else:
                    upgradeName = scoreFontSmall.render(chestToCheck.upgrade.name, True, colour)
                    upgradeNameLength = upgradeName.get_size()[0]

                    if not chestToCheck.collected and chestToCheck.opening:
                        gameWindow.blit(upgradeName, ((chestToCheck.platform.x + chestToCheck.platform.length / 2) - upgradeNameLength / 2, chestToCheck.platform.y - 48))

                    if ((keys[pygame.K_s] and self.WASD) or (keys[
                                                                 pygame.K_PERIOD] and not self.WASD)) and not chestToCheck.collected and timeElapsed - timeOpened >= 0.25:
                        if isinstance(chestToCheck.upgrade, StrengthPotion):
                            if self.damageMultiplier < 1.7:
                                self.damageMultiplier += round(chestToCheck.upgrade.strength / 100, 2)
                            else:
                                self.damageMultiplier = 1.7

                        if isinstance(chestToCheck.upgrade, HealthPotion):
                            if self.health + chestToCheck.upgrade.health > 100:
                                self.health = 100
                            else:
                                self.health += chestToCheck.upgrade.health

                        if not chestToCheck.collected:
                            potionCollected.play()
                        chestToCheck.collected = True

        if chestToCheck.opening:
            chestToCheck.open()


    def checkPortalEnter(self, portalList):
        """ Checks if the player has entered the portal

        Parameters:
            portalList: list[Portal]
                The list of portals that is checked by this function

        Return => Level: The newly generated level
        """
        # the colour changes depending on background of the level
        colour = BLACK if level.background is iceBackgroundImage else WHITE
        for portal in portalList:
            # display text if portal and player hitbox collide
            if portal.hitbox.colliderect(self.hitbox):
                # renders text
                portalText = scoreFontSmall.render("[s]/[.] Next Level?", True, colour)

                # blits text
                gameWindow.blit(portalText, (portal.platform.x + portal.platform.length / 2 - 96, portal.platform.y - 118))

                # resets level - clears lists, resets positions, etc ------------------------------------------------------
                if (keys[pygame.K_s] and self.WASD) or (keys[pygame.K_PERIOD] and not self.WASD):
                    return True


#################################################################
#                                                               #
# Collectibles                                                  #
#                                                               #
#################################################################
class Collectible(object):
    """ A class representing a collectible

    Attributes:
        x: float
            The x position of the collectible

        y: float
            The y position of the collectible

        collected: bool
            If the collectible is collected or not

    """

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.collected = False

    def collect(self) -> None:
        """ sets 'collected' to True

        Parameters:


        Return => None
        """
        # sets 'collected' to True
        self.collected = True


class Coin(Collectible):
    """ A class representing a coin, inheriting from a collectible

    Attributes:
        x: float
            The x position of the collectible

        y: float
            The y position of the collectible

        coinImages: list[pygame.Surface]
            The images for the animation coin

        animationStage: int
            The current image's index number

        collected: bool
            If the collectible is collected or not

        offset: float
            The offset of the coin relative to the left of the platform. Used to move the coin with the platform

    """

    def __init__(self, x, y) -> None:
        self.coinImages = [
            pygame.image.load(f"images/coin/coinStage{i}.png") for i in range(1, 5)
        ]
        self.animationStage = 0
        super().__init__(x, y)
        for platform in level.platforms:
            if platform.x < self.x < platform.x + platform.length:
                self.offset = self.x - platform.x

    def draw(self) -> None:
        """ Draws and animates the collectible at the x and y positions

        Parameters:


        Return => None
        """
        # resets the animation stage if the index will cause an error ---------
        if self.animationStage >= (len(self.coinImages) * 10) - 1:
            self.animationStage = 0

        # Resets the x and y position - for moving platforms ------------------
        for platform in level.platforms:
            if platform.x < self.x < platform.x + platform.length:
                self.y = platform.y - 10
                self.x = platform.x + self.offset

        # blits the image to the screen ---------------------------------------
        gameWindow.blit(self.coinImages[int(self.animationStage // 10)],
                        (self.x - COLLECTIBLE_SIZE / 2, self.y - COLLECTIBLE_SIZE / 2))

        # increments animation stage ------------------------------------------
        self.animationStage += 1

    def collect(self) -> None:
        """ Collects the coin and plays a sound

        Parameters:


        Return => None
        """
        # plays the 'coinCollected' sound
        coinCollected.stop()
        coinCollected.play()
        self.collected = True


class UpgradePotion(Collectible):
    """ A class representing an upgrade potion, inheriting from a collectible, and is extended by other potions

        Attributes:
            x: float
                The x position of the collectible

            y: float
                The y position of the collectible

            image: pygame.Surface
                The images for the potion, based on the strength of the potion

            offset: float
                The offset of the potion relative to the left of the platform. Used to move the potion with the platform

            name: str
                The name of the upgrade, which is displayed

        """

    def __init__(self, x: float, y: float, image: pygame.Surface, name: str):
        super().__init__(x, y)
        self.image = image
        self.name = name
        for platform in level.platforms:
            if platform.x < self.x < platform.x + platform.length:
                self.offset = self.x - platform.x

    def draw(self):
        """ Draws and animates the collectible at the x and y positions

        Parameters:


        Return => None
        """
        # Resets the y position - for moving platforms ------------------------
        for platform in level.platforms:
            if platform.x < self.x < platform.x + platform.length:
                self.y = platform.y - 10
                self.x = platform.x + self.offset

        # blits the image to the screen ---------------------------------------
        gameWindow.blit(self.image, (self.x - COLLECTIBLE_SIZE / 2, self.y - COLLECTIBLE_SIZE / 2))

    def collect(self):
        """ Collects the potion and plays a sound

        Parameters:


        Return => None
        """
        # plays the 'potionCollected' sound
        potionCollected.play()
        self.collected = True


class StrengthPotion(UpgradePotion):
    """ A class representing a strength potion, inheriting from a upgrade potion

    Attributes:
        x: float
            The x position of the collectible

        y: float
            The y position of the collectible

    """

    def __init__(self, x: float, y: float, strength: int) -> None:
        self.strength = strength
        if self.strength <= 3:
            image = pygame.image.load("images/potion/strengthPotion/emptyPotion.png")

        elif self.strength <= 5:
            image = pygame.image.load("images/potion/strengthPotion/halfPotion.png")

        else:
            image = pygame.image.load("images/potion/strengthPotion/fullPotion.png")

        super().__init__(x, y, image, f"+{self.strength}% strength")


class HealthPotion(UpgradePotion):
    """ A class representing a health potion, inheriting from a upgrade potion

    Attributes:
        x: float
            The x position of the collectible

        y: float
            The y position of the collectible

    """

    def __init__(self, x, y, health):
        self.health = health
        if self.health <= 10:
            image = pygame.image.load("images/potion/healthPotion/emptyPotion.png")

        elif self.health <= 20:
            image = pygame.image.load("images/potion/healthPotion/halfPotion.png")

        else:
            image = pygame.image.load("images/potion/healthPotion/fullPotion.png")
        super().__init__(x, y, image, f"+{self.health} health")


#################################################################
#                                                               #
# Chests                                                        #
#                                                               #
#################################################################
class Chest(object):
    """ A class representing a chest, which holds a weapon

        Attributes:
            platform: Platform
                The platform the chest spawns on

            hitbox: pygame.Rect
                The hitbox of the chest. If a player is inside this  hitbox, the chest opens

            collected: bool
                If the chest is collected or not

            opening: bool
                If the chest if opening or not. Used to play the chet open sound only once

    """

    def __init__(self, platform: Platform) -> None:
        self.platform = platform
        self.hitbox = pygame.Rect((self.platform.x + self.platform.length / 2) - 32, self.platform.y - 43, 64, 64)
        self.opening = False
        self.collected = False


class WeaponChest(Chest):
    """ A class representing a weapon chest, which holds a weapon

    Attributes:
        platform: Platform
            The platform the chest spawns on

        images: list[pygame.Surface]
            The images for the animated chest opening

        animationStage: int
            The current image's index number

        currentImage: pygame.Surface
            The current image to be blitted at the correct location

        hitbox: pygame.Rect
            The hitbox of the chest. If a player is inside this  hitbox, the chest opens

        weapon: Gun
            The gun the chest holds, which is given to the player if they choose

        collected: bool
            If the chest is collected or not

        opening: bool
            If the chest if opening or not. Used to play the chet open sound only once

    """

    def __init__(self, platform: Platform, weapon: Gun) -> None:
        super().__init__(platform)
        self.images = [
            pygame.image.load(f"images/chest/weaponChest/chest{i}.png") for i in range(1, 7)
        ]
        self.animationStage = 0
        self.currentImage = self.images[0]
        self.hitbox = pygame.Rect((self.platform.x + self.platform.length / 2) - 32, self.platform.y - 43, 64, 64)
        self.weapon = weapon
        self.collected = False
        self.opening = False

    def draw(self) -> None:
        """ Draws the chest at the middle of the platform. Draws the weapon's icon if the chest is opened

        Parameters:


        Return => None
        """
        # draw chest
        gameWindow.blit(self.currentImage, (self.platform.x + self.platform.length / 2 - 32, self.platform.y - 43))

        # if the chest has not been collected[x] and the chest is finished opening
        if self.animationStage == len(self.images) * 8 - 1 and not self.collected:
            gameWindow.blit(self.weapon.icon, (self.platform.x + self.platform.length / 2 - 32, self.platform.y - 43))

        # Rebuilds the hitbox
        self.hitbox = pygame.Rect((self.platform.x + self.platform.length / 2) - 32, self.platform.y - 43, 64, 64)

    def open(self) -> None:
        """ Sets the current image and increments 'Animation Stage'

        Parameters:


        Return => None
        """
        # sets current image
        self.currentImage = self.images[int(self.animationStage // 8)]

        # increments 'animationStage' if possible
        if self.animationStage <= len(self.images) * 8 - 2:
            self.animationStage += 1


class UpgradeChest(Chest):
    """ A class representing an upgrade chest, which holds an upgrade

    Attributes:
        platform: Platform
            The platform the chest spawns on

        images: list[pygame.Surface]
            The images for the animated chest opening

        animationStage: int
            The current image's index number

        currentImage: pygame.Surface
            The current image to be blitted at the correct location

        hitbox: pygame.Rect
            The hitbox of the chest. If a player is inside this  hitbox, the chest opens

        collected: bool
            If the chest is collected or not

        opening: bool
            If the chest if opening or not. Used to play the chet open sound only once

    """

    def __init__(self, platform: Platform, upgrade: UpgradePotion) -> None:
        super().__init__(platform)
        self.images = [pygame.image.load(f"images/chest/upgradeChest/chest{i}.png") for i in range(1, 7)]
        self.animationStage = 0
        self.currentImage = self.images[self.animationStage]
        self.hitbox = pygame.Rect((self.platform.x + self.platform.length / 2) - 32, self.platform.y - 43, 64, 64)
        self.upgrade = upgrade
        self.collected = False
        self.opening = False

    def draw(self) -> None:
        """ Draws the chest at the middle of the platform. Draws the weapon's icon if the chest is opened

        Parameters:


        Return => None
        """
        # draw chest
        gameWindow.blit(self.currentImage, (self.platform.x + self.platform.length / 2 - 32, self.platform.y - 43))

        # if the chest has not been collected[x] and the chest is finished opening
        if self.animationStage == len(self.images) * 8 - 1 and not self.collected:
            gameWindow.blit(self.upgrade.image, (self.platform.x + self.platform.length / 2 - COLLECTIBLE_SIZE / 2, self.platform.y - COLLECTIBLE_SIZE))

        # Rebuilds the hitbox
        self.hitbox = pygame.Rect((self.platform.x + self.platform.length / 2) - 32, self.platform.y - 43, 64, 64)

    def open(self) -> None:
        """ Sets the current image and increments 'Animation Stage'

        Parameters:


        Return => None
        """
        # sets current image
        self.currentImage = self.images[int(self.animationStage // 8)]

        # increments 'animationStage' if possible
        if self.animationStage <= len(self.images) * 8 - 2:
            self.animationStage += 1


#################################################################
#                                                               #
# Portal                                                        #
#                                                               #
#################################################################
class Portal(object):
    """ A class representing a portal, which sends you to the next level

    Attributes:
        platform: Platform
            The platform the portal spawns on

        hitbox: pygame.Rect
            The hitbox of the portal

        images: list[pygame.Surface]
            The images for the animated portal

        animationStage: int
            The current image's index number

        currentImage: pygame.Surface
            The current image to be blitted at the correct location

    """

    def __init__(self, platform: Platform) -> None:
        self.platform = platform
        self.hitbox = pygame.Rect(self.platform.x + self.platform.length / 2 - 64, self.platform.y - 118, 128, 128)
        self.images = [
            pygame.image.load(f"images/portal/portal{i}.png") for i in range(1, 9)
        ]
        self.animationStage = 0
        self.currentImage = self.images[self.animationStage]

    def draw(self) -> None:
        """ Draws the portal at the midpoint of its platform

        Parameters:


        Return => None
        """
        # resets 'animationStage' if the current value will cause an IndexError
        if self.animationStage >= len(self.images) * 5 - 1:
            self.animationStage = 0

        # sets the current image and blits it
        self.currentImage = self.images[int(self.animationStage // 5)]
        gameWindow.blit(self.currentImage, (self.platform.x + self.platform.length / 2 - 64, self.platform.y - 118))

        # rebuilds hitbox
        self.hitbox = pygame.Rect(self.platform.x + self.platform.length / 2 - 64, self.platform.y - 118, 128, 128)

        # increments animation stage
        self.animationStage += 1


#################################################################
#                                                               #
# Level                                                         #
#                                                               #
#################################################################
class Level(object):
    """ An object representing an in-game level

    Attributes:
        platforms: list[Platforms]
            The lists of platforms for the level. The list is constantly updated

        numOfPlatforms: int
            The number of platforms generated

        maxPlatforms: int
            The maximum number of platforms in the level excluding the last 2 platforms. The second last platform has a
            upgrade chest and the last platform has a portal to the next level

        background: pygame.Surface
            The background of the level



    """

    def __init__(self, maxPlatforms: int, background: pygame.Surface = backgroundImage) -> None:
        if background is underworldBackgroundImage:
            self.startPlatform = Platform(200, HEIGHT // 2 - 100, 100, underworldTile)

        elif background is iceBackgroundImage:
            self.startPlatform = Platform(200, HEIGHT // 2 - 100, 100, iceTile)

        else:
            self.startPlatform = Platform(200, HEIGHT // 2 - 100, 100)

        self.platforms: list[Union[Platform, HorizontalMovingPlatform, VerticalMovingPlatform]] = [self.startPlatform]
        self.maxPlatforms = maxPlatforms
        self.numOfPlatforms = len(self.platforms)
        self.background = background

    # Platform-related functions
    def drawPlatforms(self) -> None:
        """ Draws every platform in the 'platforms' list

        Parameters:


        Return => None
        """
        for platform in self.platforms:
            platform.draw()

    def deletePlatforms(self) -> None:
        # gets first element because first element is closes to the border --------------------------------------------
        if len(self.platforms) >= 1:

            # if the platform is out of the screen, remove it -----------------
            if self.platforms[0].x + self.platforms[0].length < -30:
                # pops the platform from the list -----------------------------
                self.platforms.pop(0)

        # -------------------------------------------------------------------------------------------------------------

        # removes enemies it they are off the screen ------------------------------------------------------------------
        for enemy in enemies:
            if enemy.platform.x + enemy.platform.length < -5:
                enemies.pop(0)

        # -------------------------------------------------------------------------------------------------------------

        # removes chests if they are off the screen -------------------------------------------------------------------
        for chest in chests:
            if chest.platform.x + chest.platform.length < -5:
                chests.pop(0)

        # -------------------------------------------------------------------------------------------------------------

    def generatePlatforms(self) -> None:
        """ Generates platforms based on the type and location of the previous platform

        Parameters:


        Return => None
        """
        # generates platform depending on the level background
        if self.background is underworldBackgroundImage:
            image = underworldTile

        elif self.background is iceBackgroundImage:
            image = iceTile

        else:
            image = grassTile

        # if there is no new platform, generate one -------------------------------------------------------------------
        if self.platforms[-1].x <= WIDTH - 60 and self.numOfPlatforms < self.maxPlatforms and len(self.platforms) != 0:
            # chance of a moving platform
            movingPlatformChance = randint(1, 4)

            # if the platform is higher or lower than the current one ---------
            higherOrLower = randint(0, 1)

            # force the platform to be lower if current platform is too high --
            if self.platforms[-1].y <= 150:
                higherOrLower = 1

            # force the platform to be high if current platform is too low ----
            elif self.platforms[-1].y >= HEIGHT - 150:
                higherOrLower = 0

            # if 'higherOrLower' is 1, make the platform lower than the current one -----------------------
            if higherOrLower == 1:

                # if 'movingPlatformChance' is 1, make a moving Platform ----------------------
                if movingPlatformChance == 1 and not isinstance(self.platforms[-1], HorizontalMovingPlatform):
                    self.platforms.append(
                        VerticalMovingPlatform(self.platforms[-1].x + self.platforms[-1].length + (randint(3, 6) * 20),
                                               self.platforms[-1].y + (randint(2, 4) * 20), (randint(7, 10) * 20),
                                               (randint(3, 6) * 10),
                                               choice([i / MOVING_PLATFORM_SPEED for i in range(5, 20)]), image)
                    )

                elif movingPlatformChance == 2 and not (
                        isinstance(self.platforms[-1], VerticalMovingPlatform) or isinstance(self.platforms[-1],
                                                                                             HorizontalMovingPlatform)):
                    self.platforms.append(
                        HorizontalMovingPlatform(
                            self.platforms[-1].x + self.platforms[-1].length + (randint(8, 10) * 20),
                            self.platforms[-1].y + (randint(2, 4) * 20), (randint(7, 10) * 20),
                            (randint(4, 7) * 10), choice([i / MOVING_PLATFORM_SPEED for i in range(5, 20)]), image)
                    )
                # else make a normal platform -------------------------------------------------
                else:
                    # make new platform a random distance from the left most point of horizontally moving platform
                    if isinstance(self.platforms[-1], HorizontalMovingPlatform):
                        self.platforms.append(
                            Platform(self.platforms[-1].lowerBound + self.platforms[-1].length + (randint(5, 8) * 20),
                                     self.platforms[-1].y + (randint(2, 4) * 20), (randint(7, 10) * 20), image)
                        )

                    # make new platform a random distance from the lowest point of vertically moving platform
                    elif isinstance(self.platforms[-1], VerticalMovingPlatform):
                        self.platforms.append(
                            Platform(self.platforms[-1].x + self.platforms[-1].length + (randint(5, 8) * 20),
                                     self.platforms[-1].lowerBound + (randint(2, 4) * 20), (randint(7, 10) * 20), image)
                        )
                    else:
                        self.platforms.append(
                            Platform(self.platforms[-1].x + self.platforms[-1].length + (randint(3, 6) * 20),
                                     self.platforms[-1].y + (randint(2, 4) * 20), (randint(7, 10) * 20), image)
                        )

            # if 'higherOrLower' is 0, make the platform higher than the current one ----------------------
            else:

                # if 'movingPlatformChance' is 1, make a moving Platform ----------------------
                if movingPlatformChance == 1 and not isinstance(self.platforms[-1], HorizontalMovingPlatform):
                    self.platforms.append(
                        VerticalMovingPlatform(self.platforms[-1].x + self.platforms[-1].length + (randint(3, 7) * 20),
                                               self.platforms[-1].y - (randint(2, 3) * 20), (randint(7, 10) * 20),
                                               (randint(3, 6) * 10),
                                               choice([i / MOVING_PLATFORM_SPEED for i in range(5, 20)]), image)
                    )

                elif movingPlatformChance == 2 and not (
                        isinstance(self.platforms[-1], VerticalMovingPlatform) or isinstance(self.platforms[-1],
                                                                                             HorizontalMovingPlatform)):
                    self.platforms.append(
                        HorizontalMovingPlatform(
                            self.platforms[-1].x + self.platforms[-1].length + (randint(9, 10) * 20),
                            self.platforms[-1].y - (randint(2, 4) * 20), (randint(7, 10) * 20),
                            (randint(4, 7) * 10), choice([i / MOVING_PLATFORM_SPEED for i in range(5, 20)]), image)
                    )
                # else make a normal platform -------------------------------------------------
                else:
                    # make new platform a random distance from the left most point of horizontally moving platform
                    if isinstance(self.platforms[-1], HorizontalMovingPlatform):
                        self.platforms.append(
                            Platform(self.platforms[-1].lowerBound + self.platforms[-1].length + (randint(5, 8) * 20),
                                     self.platforms[-1].y - (randint(2, 4) * 20), (randint(7, 10) * 20), image)
                        )

                    # make new platform a random distance from the highest point of vertically moving platform
                    elif isinstance(self.platforms[-1], VerticalMovingPlatform):
                        self.platforms.append(
                            Platform(self.platforms[-1].x + self.platforms[-1].length + (randint(5, 8) * 20),
                                     self.platforms[-1].upperBound - (randint(1, 3) * 20), (randint(7, 10) * 20), image)
                        )
                    else:
                        self.platforms.append(
                            Platform(self.platforms[-1].x + self.platforms[-1].length + (randint(3, 6) * 20),
                                     self.platforms[-1].y - (randint(2, 4) * 20), (randint(7, 10) * 20), image)
                        )

            # increments 'numOfPlatforms' ---------------------------------
            self.numOfPlatforms += 1

            # the chance that an enemy spawns on the platform ---------------------------------------------
            chanceOfEnemy = randint(1, 4)

            # if the last platform is not the spawn platform and 'chanceOfEnemy' is 1 ---------
            if chanceOfEnemy in [1, 2] and self.platforms[-1] is not self.startPlatform:
                # number of enemies and speed of each enemy
                numberOfEnemies = int(randint(2, 4) // 2)
                speed = uniform(0.2, 0.4)

                # generate the 'numberOfEnemies' number of enemies, depending on background --
                for j in range(numberOfEnemies):
                    # ice enemy
                    if level.background is iceBackgroundImage:
                        enemies.append(
                            IceEnemy(self.platforms[-1], speed, 100)
                        )

                    # underworld enemy
                    elif level.background is underworldBackgroundImage:
                        enemies.append(
                            UnderworldEnemy(self.platforms[-1], speed, 100)
                        )

                    # normal enemy
                    else:
                        enemies.append(
                            Enemy(self.platforms[-1], speed, 100)
                        )

                    # makes the speed of the second enemy 0.2 larger than the speed of the first
                    speed += 0.2

            # Removing enemies if they are on the first platform ------------------------------------------
            for enemy in enemies:
                if enemy.platform is self.startPlatform:
                    if enemy in enemies:
                        enemies.remove(enemy)

            # chance of a chest to spawn ------------------------------------------------------------------
            chanceOfChest = randint(1, 3)

            # if levelNumber == 0(tutorial level), make every possible chest spawn ------------------------
            if levelNumber == 0:
                chanceOfChest = 1

            if chanceOfChest == 1 and chanceOfEnemy not in [1, 2]:
                # Weapon generation
                weapon = generateWeapon()

                # Append the new chest
                chests.append(
                    WeaponChest(self.platforms[-1], weapon)
                )

        # -------------------------------------------------------------------------------------------------------------

        # Append new platform with the upgrade chest ------------------------------------------------------------------
        if self.numOfPlatforms == self.maxPlatforms:
            if isinstance(self.platforms[-1], HorizontalMovingPlatform):

                # appending platform based on the right most position
                self.platforms.append(
                    Platform(self.platforms[-1].lowerBound + self.platforms[-1].length + 60,
                             self.platforms[-1].y, 180, image)
                )

            else:
                # append platform normally
                self.platforms.append(
                    Platform(self.platforms[-1].x + self.platforms[-1].length + 60,
                             self.platforms[-1].y, 180, image)
                )

            # generate potions ----------------------------------------------------------------
            potionChoice = randint(1, 2)

            # defaults to '+ 10' health
            potion = HealthPotion(self.platforms[-1].x + self.platforms[-1].length / 2, self.platforms[-1].y, 10)

            # generate potion
            if potionChoice == 1:
                potion = StrengthPotion(self.platforms[-1].x + self.platforms[-1].length / 2, self.platforms[-1].y,
                                        choice([3, 5, 10]))

            elif potionChoice == 2:
                potion = HealthPotion(self.platforms[-1].x + self.platforms[-1].length / 2, self.platforms[-1].y,
                                      choice([10, 20, 25]))

            # appends upgrade chest to list ---------------------------------------------------
            chests.append(UpgradeChest(self.platforms[-1], potion))

            self.numOfPlatforms += 1

        # -------------------------------------------------------------------------------------------------------------

        # Append new platform with the 'next level' portal ------------------------------------------------------------
        if self.numOfPlatforms == self.maxPlatforms + 1:
            self.platforms.append(
                Platform(self.platforms[-1].x + self.platforms[-1].length + 60,
                         self.platforms[-1].y, 180, image)
            )

            # appends portal to list
            portals.append(Portal(self.platforms[-1]))

            self.numOfPlatforms += 1

        # -------------------------------------------------------------------------------------------------------------

    def checkPlayerCollision(self, playerToCheck: Player) -> None:
        """ Responsible for checking for collision between the platforms and the player

        Parameters:
            playerToCheck: Player
                The player whose weapon damages the enemy


        Return => None
        """
        playerToCheck.checkPlatformCollision(self)
    
    def redrawPlatforms(self) -> None:
        """ Responsible for drawing, generating, and deleting the platforms, as well has the weapon cooldown

        Parameters:
            playerToCheck: Player
                The player whose weapon damages the enemy


        Return => None
        """
        self.generatePlatforms()
        self.deletePlatforms()
        self.drawPlatforms()


class MissileChannel(object):
    """ A channel which fires a missile. The primary way to damage the boss in a 'BossLevel'

    Attributes:
        hitbox: pygame.Rect
            The hitbox of the channel

        isOpened: bool
            If the channel is opened or not, which allows the player to damage the boss

        timeSinceOpen: float
            Used to close the channel after a certain amount of time

        colour: tuple[int, int, int]
            The colour of the channels when closed

        timeSinceOpen: float
            Used to flash the channel for a certain amount of time

    """

    def __init__(self, y: float, height: float, colour: tuple[int, int, int]) -> None:
        self.hitbox = pygame.Rect(WIDTH - 2, y, 2, height)

        # if the channel is open, the boss can be hit from there
        self.isOpened = False

        self.timeSinceOpen = 0

        self.originalColour = colour
        self.colour = self.originalColour

        self.timeSinceFlash = 0

    def open(self) -> None:
        """ opens the channel and records the time

        Parameters:


        Return => None
        """
        if not self.isOpened:
            self.timeSinceOpen = timeElapsed
            self.isOpened = True

    def draw(self) -> None:
        """ draws the channel when its opened

        Parameters:


        Return => None
        """
        if self.isOpened:
            pygame.draw.rect(gameWindow, RED, (WIDTH - 5, self.hitbox.y, 5, self.hitbox.height))
            pygame.draw.rect(gameWindow, BLACK, (WIDTH - 6, self.hitbox.y - 1, 7, self.hitbox.height + 2), 1)

        else:
            pygame.draw.rect(gameWindow, self.colour, (WIDTH - 5, self.hitbox.y, 5, self.hitbox.height))
            pygame.draw.rect(gameWindow, BLACK, (WIDTH - 6, self.hitbox.y - 1, 7, self.hitbox.height + 2), 1)

    def flash(self) -> None:
        """ Flashes the channels red

        Parameters:


        Return => None
        """
        if self.colour == self.originalColour:
            self.colour = RED
            self.timeSinceFlash = timeElapsed

    def unFlash(self):
        """ Resets the channel's colour

        Parameters:


        Return => None
        """
        if timeElapsed - self.timeSinceFlash >= 0.25 and self.colour == RED and not self.isOpened:
            self.colour = self.originalColour


class BossLevel(Level):
    """ An object representing an in-game level with a boss fight

    Attributes:
        maxPlatforms: int
            The maximum number of platforms in the level. The last platform has a portal to the next level

        background: pygame.Surface
            The background of the level

        generatePlatform: bool
            In the boss level, platforms are generated infinitely until the boss is defeated. This booleans controls
            platform generation

        canFireLaser: bool
            In the boss level, there is a stage where the boss fires vertical lasers toward the player
            This controls the firing of the lasers, as we do not want 2 lasers at the same time

        hitboxes: list[MissileChannel]
            A list of 'MissileChannel', which are the the only way to damage the boss.
            When a missile is fired from a channel, that channel is temporarily opened, which then can be hit with
            a bullet

        health: int
            The health of the boss

        MISSILE_STAGE, ENEMY_STAGE, LASER_STAGE: int
            Constants for the 3 boss stages

        stage: int
            The current stage of the boss fight

        healthBreakpoint: int
            The point at which to cycle to the next stage

        instructionAnimationStage: int
            The animation stage of the instructions, which has a "typed-out" animation

    """

    def __init__(self, maxPlatforms: int, background: pygame.Surface = backgroundImage) -> None:
        super().__init__(maxPlatforms, background)

        # booleans
        self.generatePlatform = True
        self.canFireLaser = False
        self.levelOver = False

        # hitboxes
        self.hitboxes = [MissileChannel(y, 50, WHITE) for y in range(0, HEIGHT, 50)]

        # health
        self.health = 750

        # stages
        self.MISSILE_STAGE = 1
        self.ENEMY_STAGE = 2
        self.LASER_STAGE = 3

        # current stage
        self.stage = self.MISSILE_STAGE

        # when to cycle to next stage
        self.healthBreakpoint = self.health - 250
        self.enemiesToGenerate = 0

        # animation
        self.instructionAnimationStage = 0

    def generatePlatforms(self) -> None:
        """ Generates platforms based on the type and location of the previous platform

        Parameters:


        Return => None
        """
        # generates platform depending on the level background
        if self.background is underworldBackgroundImage:
            image = underworldTile

        elif self.background is iceBackgroundImage:
            image = iceTile

        else:
            image = grassTile

        # if there is no new platform, generate one -------------------------------------------------------------------
        if self.platforms[-1].x <= WIDTH - 60 and self.generatePlatform:
            # chance of a moving platform
            movingPlatformChance = randint(1, 4)

            # if the platform is higher or lower than the current one ---------
            higherOrLower = randint(0, 1)

            # force the platform to be lower if current platform is too high --
            if self.platforms[-1].y <= 300:
                higherOrLower = 1

            # force the platform to be high if current platform is too low ----
            elif self.platforms[-1].y >= HEIGHT - 300:
                higherOrLower = 0

            # if 'higherOrLower' is 1, make the platform lower than the current one -----------------------
            if higherOrLower == 1:

                # if 'movingPlatformChance' is 1, make a moving Platform ----------------------
                if movingPlatformChance == 1 and not isinstance(self.platforms[-1], HorizontalMovingPlatform):
                    self.platforms.append(
                        VerticalMovingPlatform(self.platforms[-1].x + self.platforms[-1].length + (randint(3, 6) * 20),
                                               self.platforms[-1].y + (randint(2, 4) * 20), (randint(7, 10) * 20),
                                               (randint(3, 6) * 10), choice([i / MOVING_PLATFORM_SPEED for i in range(5, 20)]), image)
                    )

                elif movingPlatformChance == 2 and not (
                        isinstance(self.platforms[-1], VerticalMovingPlatform) or isinstance(self.platforms[-1],
                                                                                             HorizontalMovingPlatform)):
                    self.platforms.append(
                        HorizontalMovingPlatform(
                            self.platforms[-1].x + self.platforms[-1].length + (randint(8, 10) * 20),
                            self.platforms[-1].y + (randint(2, 4) * 20), (randint(7, 10) * 20),
                            (randint(4, 7) * 10), choice([i / MOVING_PLATFORM_SPEED for i in range(5, 20)]), image)
                    )
                # else make a normal platform -------------------------------------------------
                else:
                    # make new platform a random distance from the left most point of horizontally moving platform
                    if isinstance(self.platforms[-1], HorizontalMovingPlatform):
                        self.platforms.append(
                            Platform(self.platforms[-1].lowerBound + self.platforms[-1].length + (randint(5, 8) * 20),
                                     self.platforms[-1].y + (randint(2, 4) * 20), (randint(7, 10) * 20), image)
                        )

                    # make new platform a random distance from the lowest point of vertically moving platform
                    elif isinstance(self.platforms[-1], VerticalMovingPlatform):
                        self.platforms.append(
                            Platform(self.platforms[-1].x + self.platforms[-1].length + (randint(5, 8) * 20),
                                     self.platforms[-1].lowerBound + (randint(2, 4) * 20), (randint(7, 10) * 20), image)
                        )
                    else:
                        self.platforms.append(
                            Platform(self.platforms[-1].x + self.platforms[-1].length + (randint(3, 6) * 20),
                                     self.platforms[-1].y + (randint(2, 4) * 20), (randint(7, 10) * 20), image)
                        )

            # if 'higherOrLower' is 0, make the platform higher than the current one ----------------------
            else:

                # if 'movingPlatformChance' is 1, make a moving Platform ----------------------
                if movingPlatformChance == 1 and not isinstance(self.platforms[-1], HorizontalMovingPlatform):
                    self.platforms.append(
                        VerticalMovingPlatform(self.platforms[-1].x + self.platforms[-1].length + (randint(3, 7) * 20),
                                               self.platforms[-1].y - (randint(2, 3) * 20), (randint(7, 10) * 20),
                                               (randint(3, 6) * 10), choice([i / MOVING_PLATFORM_SPEED for i in range(5, 20)]), image)
                    )

                elif movingPlatformChance == 2 and not (
                        isinstance(self.platforms[-1], VerticalMovingPlatform) or isinstance(self.platforms[-1],
                                                                                             HorizontalMovingPlatform)):
                    self.platforms.append(
                        HorizontalMovingPlatform(
                            self.platforms[-1].x + self.platforms[-1].length + (randint(9, 10) * 20),
                            self.platforms[-1].y - (randint(2, 4) * 20), (randint(7, 10) * 20),
                            (randint(4, 7) * 10), choice([i / MOVING_PLATFORM_SPEED for i in range(5, 20)]), image)
                    )
                # else make a normal platform -------------------------------------------------
                else:
                    # make new platform a random distance from the left most point of horizontally moving platform
                    if isinstance(self.platforms[-1], HorizontalMovingPlatform):
                        self.platforms.append(
                            Platform(self.platforms[-1].lowerBound + self.platforms[-1].length + (randint(5, 8) * 20),
                                     self.platforms[-1].y - (randint(2, 4) * 20), (randint(7, 10) * 20), image)
                        )

                    # make new platform a random distance from the highest point of vertically moving platform
                    elif isinstance(self.platforms[-1], VerticalMovingPlatform):
                        self.platforms.append(
                            Platform(self.platforms[-1].x + self.platforms[-1].length + (randint(5, 8) * 20),
                                     self.platforms[-1].upperBound - (randint(1, 3) * 20), (randint(7, 10) * 20), image)
                        )
                    else:
                        self.platforms.append(
                            Platform(self.platforms[-1].x + self.platforms[-1].length + (randint(3, 6) * 20),
                                     self.platforms[-1].y - (randint(2, 4) * 20), (randint(7, 10) * 20), image)
                        )

            # if the last platform is not the spawn platform and 'chanceOfEnemy' is 1 ---------
            if self.stage == self.ENEMY_STAGE and self.platforms[-1] is not self.startPlatform and self.enemiesToGenerate > 0:

                # speed
                speed = uniform(0.3, 0.7)

                typeOfEnemy = randint(1, 8)

                # ice enemy
                if typeOfEnemy == 1 and self.background is iceBackgroundImage:
                    enemies.append(
                        IceEnemy(self.platforms[-1], speed, 100)
                    )

                # underworld enemy
                elif typeOfEnemy == 2 and (
                        self.background is iceBackgroundImage or self.background is underworldBackgroundImage):
                    enemies.append(
                        UnderworldEnemy(self.platforms[-1], speed, 100)
                    )

                # normal enemy
                else:
                    enemies.append(
                        Enemy(self.platforms[-1], speed, 100)
                    )

                self.enemiesToGenerate -= 1

            # Removing enemies if they are on the first platform ------------------------------------------
            for enemy in enemies:
                if enemy.platform is self.startPlatform:
                    if enemy in enemies:
                        enemies.remove(enemy)

            # chance of a chest to spawn ------------------------------------------------------------------
            chanceOfChest = randint(1, 3)

            if chanceOfChest == 1:
                # Weapon generation
                weapon = generateWeapon()

                # Append the new chest
                chests.append(
                    WeaponChest(self.platforms[-1], weapon)
                )

        # -------------------------------------------------------------------------------------------------------------

        # Append new platform with the upgrade chest ------------------------------------------------------------------
        if self.generatePlatform and self.levelOver:
            if isinstance(self.platforms[-1], HorizontalMovingPlatform):

                # appending platform based on the right most position
                self.platforms.append(
                    Platform(self.platforms[-1].lowerBound + self.platforms[-1].length + 60,
                             self.platforms[-1].y, 180, image)
                )

            else:
                # append platform normally
                self.platforms.append(
                    Platform(self.platforms[-1].x + self.platforms[-1].length + 60,
                             self.platforms[-1].y, 180, image)
                )

            # generate potions ----------------------------------------------------------------
            potionChoice = randint(1, 2)

            # defaults to '+ 10' health
            potion = HealthPotion(self.platforms[-1].x + self.platforms[-1].length / 2, self.platforms[-1].y, 10)

            # generate potion
            if potionChoice == 1:
                potion = StrengthPotion(self.platforms[-1].x + self.platforms[-1].length / 2, self.platforms[-1].y,
                                        choice([3, 5, 10]))

            elif potionChoice == 2:
                potion = HealthPotion(self.platforms[-1].x + self.platforms[-1].length / 2, self.platforms[-1].y,
                                      choice([10, 20, 25]))

            # appends upgrade chest to list ---------------------------------------------------
            chests.append(UpgradeChest(self.platforms[-1], potion))

        # -------------------------------------------------------------------------------------------------------------

        # Append new platform with the 'next level' portal ------------------------------------------------------------
        if self.generatePlatform and self.levelOver:
            self.platforms.append(
                Platform(self.platforms[-1].x + self.platforms[-1].length + 60,
                         self.platforms[-1].y, 180, image)
            )

            # appends portal to list
            portals.append(Portal(self.platforms[-1]))

            self.numOfPlatforms += 1

            self.generatePlatform = False

        # -------------------------------------------------------------------------------------------------------------

    def drawHealthBar(self, y: int) -> None:
        """ Draws a health bar for the boss

        Parameters:
            y: int
                The Y location of the health bar

        Return => None
        """
        # drawing player health in chunks of 25 -------------------------------
        for j in range(int(self.health // 25)):
            # health
            pygame.draw.rect(gameWindow, PURPLE, (200 + (j * 14), y + 3, 14, 30), 0, 0)
            pygame.draw.rect(gameWindow, LPURPLE, (200 + (j * 14), y + 8, 14, 6), 0, 0)

            # drawing over edges of health bar
            if j == 0:
                pygame.draw.rect(gameWindow, PURPLE, (200, y + 3, 6, 30), 0, 0)
            if j == (self.health // 25) - 1:
                pygame.draw.rect(gameWindow, PURPLE, (200 + (j * 14) + 8, y + 3, 6, 30), 0, 0)

        # ---------------------------------------------------------------------

        # border --------------------------------------------------------------
        pygame.draw.rect(gameWindow, BLACK, (196, y, 422, 36), 5, 8)
        pygame.draw.rect(gameWindow, (64, 64, 64), (196, y - 2, 424, 40), 3, 8)

        # ---------------------------------------------------------------------

    def checkPlayerCollision(self, playerToCheck: Player) -> None:
        """ Responsible for checking for collision between the platforms and the player

        Parameters:
            playerToCheck: Player
                The player whose weapon damages the enemy


        Return => None
        """
        playerToCheck.checkPlatformCollision(self)

    def redrawPlatforms(self) -> None:
        """ Responsible for drawing, moving, generating, and deleting the platforms

        Parameters:


        Return => None
        """
        self.generatePlatforms()
        self.deletePlatforms()
        self.checkAlive()
        super().drawPlatforms()
        self.checkCollision()
        self.drawHealthBar(25)

        if not self.levelOver:
            self.changeStage()
            self.drawInstructions()
            self.fireWeapon()
            self.drawChannels()

    def fireMissile(self) -> None:
        """ Fires a missile and opens the respective channel at a random location

        Parameters:


        Return => None
        """
        randomChannel = randint(0, HEIGHT // 50 - 1)

        self.hitboxes[randomChannel].open()

        bullets.append(EnemyBullet(WIDTH - 10, randomChannel * 50 + 17, 8))

    def fireLaser(self, start, end) -> None:
        laserFired = True
        for bullet in bullets:
            if isinstance(bullet, EnemyLaser):
                laserFired = False

        self.canFireLaser = laserFired

        if self.canFireLaser:
            bullets.append(EnemyLaser(start, end, 12))

    def drawChannels(self) -> None:
        """ Draws the channels and also closes them after a period of time

        Parameters:


        Return => None
        """
        for channel in self.hitboxes:
            if channel.isOpened and timeElapsed - channel.timeSinceOpen >= 6:
                channel.isOpened = False

            channel.draw()

    def checkCollision(self) -> None:
        """ Checks for collision between the bullets and the open channels

        Parameters:


        Return => None
        """
        for channel in self.hitboxes:
            for bullet in bullets:
                if bullet.hitbox.colliderect(channel.hitbox) and channel.isOpened and not isinstance(bullet, EnemyProjectile):
                    bossHitSound.stop()
                    bossHitSound.play()
                    self.health -= int(bullet.damage // 3)

                    for hitbox in self.hitboxes:
                        hitbox.flash()

                    # removing bullet
                    if bullet in bullets:
                        bullets.remove(bullet)

                # plays sound if the channel is not open
                elif bullet.hitbox.colliderect(channel.hitbox) and not (isinstance(bullet, EnemyProjectile) or isinstance(bullet, EnemyLaser)):
                    bossMissedSound.stop()
                    bossMissedSound.play()

            for grenade in grenades:
                if grenade.hitbox.colliderect(channel.hitbox):
                    if channel.isOpened and not grenade.exploded:
                        self.health -= int(grenade.damage // 3)

                        for hitbox in self.hitboxes:
                            hitbox.flash()

                    grenade.exploded = True


            channel.unFlash()

    def drawInstructions(self) -> None:
        """ Draws the instructions "aim for the red targets" with a typed-out animation

        Parameters:


        Return => None
        """
        instructionStr = "aim for the red targets"
        if self.numOfPlatforms <= 8:
            if self.instructionAnimationStage < len(instructionStr) * 2:
                self.instructionAnimationStage += 1

            bossInstructions = instructionFont.render(instructionStr[:self.instructionAnimationStage // 2], False,
                                                      WHITE)
            instructionsWidth, instructionsHeight = instructionFont.size(
                instructionStr[:self.instructionAnimationStage // 2])
            gameWindow.blit(bossInstructions, (WIDTH / 2 - instructionsWidth / 2, HEIGHT - 40 - instructionsHeight))

    def fireWeapon(self) -> None:
        """ Draws the platforms

        Parameters:


        Return => None
        """
        # firing missile randomly
        if randint(1, 50) == 1 and self.stage == self.MISSILE_STAGE:
            self.fireMissile()

        # firing laser randomly
        if randint(1, 50) == 1 and self.stage == self.LASER_STAGE:
            start = choice([-27, WIDTH])
            end = (WIDTH / 2 - randint(0, int(WIDTH / 8))) if start == -27 else (WIDTH / 2 + randint(0, int(WIDTH / 8)))
            self.fireLaser(start, end)

    def checkAlive(self) -> None:
        """ Checks if the boss is alive, and sets the level over if the boss is not alive

        Parameters:


        Return => None
        """
        if self.health <= 0:
            self.levelOver = True

    def changeStage(self) -> None:
        """ Cycles through the stages

        Parameters:


        Return => None
        """
        if self.stage == self.MISSILE_STAGE and self.health <= self.healthBreakpoint:
            self.healthBreakpoint -= 250
            self.stage = self.ENEMY_STAGE
            self.enemiesToGenerate = randint(8, 16)

        if self.stage == self.ENEMY_STAGE and self.enemiesToGenerate <= 0:
            self.stage = self.LASER_STAGE

        if self.stage == self.LASER_STAGE and randint(1, 10) == 1 and self.canFireLaser:
            self.stage = self.MISSILE_STAGE


###############################################################################
#
# Functions
#
###############################################################################
## Move background ############################################
def moveBackground(rate: float) -> None:
    """ Moves the background to give the illusion of the player moving forward

    Parameters:
        rate: float -> the rate of which the backgrounds moves


    Return => None
    """
    # moves player
    for play in players:
        play.x -= rate

    # moves platforms
    for pf in level.platforms:
        pf.x -= rate
        if isinstance(pf, HorizontalMovingPlatform):
            pf.upperBound -= rate
            pf.lowerBound -= rate

    # moves enemies
    for en in enemies:
        en.x -= rate

    # moves collectibles
    for co in collectibles:
        co.x -= rate

    # moves bullets
    for bu in bullets:
        bu.x -= rate

    # moves grenades
    for gr in grenades:
        gr.x -= rate


## Enemy-related functions ####################################
def drawEnemies() -> None:
    """ Draws all the enemies

    Parameters:


    Return => None
    """
    for enemy in enemies:
        enemy.draw()


def moveEnemies() -> None:
    """ Moves all the enemies

    Parameters:


    Return => None
    """
    for enemy in enemies:
        enemy.move()


def deleteEnemies() -> None:
    """ Deletes enemies if their health is <= 0 and their death animation is over

    Parameters:


    Return => None
    """
    for enemy in enemies:
        if enemy.health <= 0 and enemy.deadStage == (len(enemy.dead) * 8) - 1:
            if enemy in enemies:
                enemies.remove(enemy)


def checkEnemyAlive() -> None:
    """ Checks if the enemy is alive or not

    Parameters:


    Return => None
    """
    for enemy in enemies:
        enemy.checkAlive()


## Bullet-related functions ###################################
def moveBullets() -> None:
    """ Moves all bullets according to their speed

    Parameters:


    Return => None
    """
    for bullet in bullets:
        bullet.move()


def drawBullets() -> None:
    """ Draws bullets

    Parameters:


    Return => None
    """
    for bullet in bullets:
        bullet.draw()


## Grenade-related functions ##################################
def drawGrenades() -> None:
    """ Draws grenade

    Parameters:


    Return => None
    """
    for grenade in grenades:
        grenade.draw()


def moveGrenades() -> None:
    """ Draws grenades

    Parameters:


    Return => None
    """
    for grenade in grenades:
        grenade.move()


## Chest-related functions ####################################
def drawChests() -> None:
    """ Draws chests

    Parameters:


    Return => None
    """
    for chest in chests:
        chest.draw()


## Collectible-related functions ##############################
def drawCollectibles() -> None:
    """ Draws collectibles

    Parameters:


    Return => None
    """
    for collectible in collectibles:
        collectible.draw()


## Portal-related functions ###################################
def drawPortals() -> None:
    """ Draws portals

    Parameters:


    Return => None
    """
    for portal in portals:
        portal.draw()


## Level generation ###########################################
def generateLevel(playerList: list[Player]) -> Level:
    """ Generates a new level

    Parameters:
        playerList: Player
            The list of players that is checked by this function

    Return => Level: The newly generated level
    """

    global levelNumber, levelTransition

    for playerToCheck in playerList:
        if playerToCheck.checkPortalEnter(portals) and levelNumber == 5:
            levelTransition = True

        if playerToCheck.checkPortalEnter(portals) and not levelTransition:

            portalEnter.play()
            chests.clear()
            portals.clear()
            enemies.clear()
            grenades.clear()
            bullets.clear()
            collectibles.clear()

            # resets player location
            for play in playerList:
                play.x = 250
                play.y = 200 - PLAYER_SIZE_X

                # resets player speed
                play.speedX = 0
                play.speedY = 1

                # resets acceleration
                play.accelerationX = 0.25


            # increments level number
            levelNumber += 1
            levelTransition = False

            # reset player health and weapon after they finish the tutorial ---------------
            if levelNumber == 1:
                for play in playerList:
                    play.currentWeapon = Pistol()
                    play.health = 100

            levelBackgroundImage = backgroundImage


            # sets background based on level number
            if 6 <= levelNumber <= 10:
                levelBackgroundImage = underworldBackgroundImage

            if 11 <= levelNumber <= 15:
                # acceleration as the level has 'ice'
                playerToCheck.accelerationX = 0.15
                levelBackgroundImage = iceBackgroundImage

            platformNum = levelNumber * 5 + 5
            if platformNum > MAX_PLATFORMS:
                platformNum = MAX_PLATFORMS

            if levelNumber == 5 or levelNumber == 10 or levelNumber == 15:
                return BossLevel(platformNum, levelBackgroundImage)

            return Level(platformNum, levelBackgroundImage)

        # Going into the underworld transition ----------------------------------------------------------------------------
        if levelTransition:
            # remove the portal and its platform
            for portal in portals:
                if portal.platform in level.platforms:
                    level.platforms.remove(portal.platform)

                portals.clear()

            # resets level if player has left the screen
            if playerToCheck.y >= HEIGHT + PLAYER_SIZE_Y + 500:
                levelTransition = False
                # resets lists
                portalEnter.play()
                chests.clear()
                portals.clear()
                enemies.clear()
                grenades.clear()
                bullets.clear()
                collectibles.clear()

                # resets player location
                for play in playerList:
                    play.x = 250
                    play.y = 200 - PLAYER_SIZE_X

                    # resets player speed
                    play.speedX = 0
                    play.speedY = 1

                    # resets acceleration
                    play.accelerationX = 0.25

                # increments level number
                levelNumber += 1

                platformNum = levelNumber * 5 + 5
                if platformNum > MAX_PLATFORMS:
                    platformNum = MAX_PLATFORMS

                return Level(platformNum, underworldBackgroundImage)

    return level



## Weapon generation ##########################################
def generateWeapon() -> Gun:
    """ Generates a weapon using the choice() function from the random module.

    Parameters:


    Return => Gun: returns the randomly generated gun
    """
    # generating weapon -------------------------------------------------------
    # picking a type of weapon
    weaponType = choice(list(weapons.keys()))

    # forcing the 'default' type if 'levelNumber' is smaller than 6
    if levelNumber < 6:
        weaponType = list(weapons.keys())[0]
    elif levelNumber < 11:
        weaponType = choice([list(weapons.keys())[0], list(weapons.keys())[1]])
    elif levelNumber < 16:
        weaponType = choice([list(weapons.keys())[1], list(weapons.keys())[2]])

    weapon = choice(weapons[weaponType])

    return SubMachineGun()


###############################################################################
#
# Collision functions
#
###############################################################################
## Bullet and grenade collision functions #####################
def checkBulletCollision(playerToCheck: Player) -> None:
    """ Checks if any bullets in the 'bullets' list has collided with any enemies

    Parameters:
        playerToCheck: Player
            The player whose weapon damages the enemy

    Return => None
    """
    # nested loop to check every bullet and enemy ---------------------------------------------------------------------
    for bullet in bullets:
        for enemy in enemies:
            # for staffs, which target the closest enemy
            enemyLargeHitbox = pygame.Rect(enemy.x, 0, enemy.enemySizeX, HEIGHT)
            if enemy.hitbox.colliderect(bullet.hitbox) and not enemy.damaged and not enemy.isDead and not isinstance(bullet, Icicle) and not isinstance(bullet, Lightning) and not isinstance(bullet, EnemyLaser):
                # damages enemy if the enemy is not already damaged(invincible) and the bullet is not an icicle

                if isinstance(bullet, Flame):
                    enemyHitSound.set_volume(0.05)
                else:
                    enemyHitSound.set_volume(0.5)

                enemy.takeDamage(bullet.damage)
                enemy.damaged = True

                # remove the bullet if possible -------------------------------
                if bullet in bullets and not isinstance(bullet, LaserBullet) and not isinstance(bullet, LaserBeam) and not enemy.isDead:
                    bullets.remove(bullet)

            if enemyLargeHitbox.colliderect(bullet.hitbox) and isinstance(bullet, Lightning):
                bullet.y = enemy.y + enemy.enemySizeY / 2
                enemy.takeDamage(bullet.damage)
                enemy.damaged = True
                bullet.collided = True

        # removes bullet if it has left the screen ----------------------------
        if (bullet.x > WIDTH + 10 or bullet.x < -10 or bullet.y > HEIGHT + 10) and not isinstance(bullet, EnemyLaser):
            if bullet in bullets:
                bullets.remove(bullet)

        # removes shotgun bullets whose animation is over----------------------
        if isinstance(bullet, ShotgunBullet) and bullet.muzzleFlashStage == len(bullet.muzzleFlash) * 2 - 1:
            if bullet in bullets:
                bullets.remove(bullet)

        # removes shotgun bullets whose animation is over ---------------------
        if isinstance(bullet, LaserShotgunBullet) and bullet.muzzleFlashStage == len(bullet.muzzleFlash) * 2 - 1:
            if bullet in bullets:
                bullets.remove(bullet)

        # removes flames ------------------------------------------------------
        if isinstance(bullet, Flame) and not bullet.fired:
            if bullet in bullets:
                bullets.remove(bullet)

        # removes laser beams -------------------------------------------------
        if isinstance(bullet, LaserBeam) and bullet.loopsSinceFire == 30:
            if bullet in bullets:
                bullets.remove(bullet)

        # removes beams -------------------------------------------------------
        if isinstance(bullet, Lightning) and bullet.explosionAnimationStage == len(bullet.explosionAnimation) * 10 - 1:
            if bullet in bullets:
                bullets.remove(bullet)

        # removes beams -------------------------------------------------------
        if isinstance(bullet, EnemyLaser) and bullet.ended:
            if bullet in bullets:
                bullets.remove(bullet)

        # enemy-fired bullets which get deleted after collision ----------------
        if isinstance(bullet, Icicle) or isinstance(bullet, EnemyBullet) or isinstance(bullet, EnemyLaser):
            if bullet.hitbox.colliderect(playerToCheck.hitbox):
                # damages player upon collision
                playerToCheck.takeDamage(bullet.damage)

                # removes bullet if possible
                if bullet in bullets:
                    bullets.remove(bullet)


def checkGrenadeCollision() -> None:
    """ Checks if any grenade in the 'grenades' list has collided with any enemies or platforms

    Parameters:


    Return => None
    """
    # Checks if the bullet is in any platforms or enemies ---------------------
    for grenade in grenades:
        for platform in level.platforms:
            # Builds platform hitbox
            platformHitbox = pygame.Rect(platform.x, platform.y, platform.length, platform.width)

            # explodes grenade if grenade hits a platform -------------
            if grenade.hitbox.colliderect(platformHitbox):
                grenade.exploded = True

            # Checks every enemy for collision ------------------------
            for enemy in enemies:

                # explodes if grenade hits an enemy -------------------
                if grenade.hitbox.colliderect(enemy.hitbox):
                    grenade.exploded = True

                # Deduct health ---------------------------------------
                if grenade.exploded and grenade.explosionHitbox.colliderect(enemy.hitbox) and grenade.explosionAnimationStage == 0:
                    enemy.takeDamage(GRENADE_LAUNCHER_DAMAGE)

        # Remove grenade when explosion animation ends ----------------
        if grenade.explosionAnimationStage >= len(grenade.explosionAnimation) * 8 - 1:
            grenades.pop(grenades.index(grenade))

        # removes grenade if it falls out of the screen ---------------
        if grenade.y > HEIGHT + 10:
            grenades.pop(grenades.index(grenade))

    # -------------------------------------------------------------------------


## redraw functions - combines other functions ################
def redrawPlayer(playerToDraw: Player) -> None:
    """ Responsible for drawing and moving the player, as well has the weapon cooldown

    Parameters:
        playerToDraw: Player
            The player to draw and move


    Return => None
    """
    playerToDraw.move()
    playerToDraw.draw()
    # Fire weapon if possible
    playerToDraw.fireWeapon()

    # Draw the bullet GUI with the time
    drawMagazineDisplay(playerToDraw, timeElapsed - playerToDraw.currentWeapon.timeSinceFire,
                        playerToDraw.currentWeapon.fireRate,
                        HEIGHT - 50 * (len(players) - (players.index(playerToDraw))))

    # Invincible delay --------------------------------------------------------
    enemyHit = False
    for enemy in enemies:
        enemyHit = playerToDraw.checkEnemyCollision(enemy)
    # get the current time
    if enemyHit:
        playerToDraw.timeHit = timeElapsed

    if (timeElapsed - playerToDraw.timeHit) >= INVINCIBLE_DELAY:
        playerToDraw.invincible = False

    # -------------------------------------------------------------------------

    # Checks for player collision with the edges of the screen -----------------
    if not levelTransition:
        playerToDraw.checkCollision()

    if playerToDraw.checkLife():
        players.remove(playerToDraw)


def redrawEnemies() -> None:
    """ Draws and move the enemies

    Parameters:



    Return => None
    """
    # checks if enemy is alive
    checkEnemyAlive()

    # draws and move enemy
    drawEnemies()
    moveEnemies()

    # delete enemies that are finished their death animation
    deleteEnemies()
    


def checkEnemyInvincibilityCooldown(playerToCheck: Player) -> None:
    """ Makes sure that the collision cooldown is used - makes the enmy invicible for a short duration

    Parameters:
        playerToCheck: Player
            The player to check collision for


    Return => None
    """
    # records time when hit - for invincibility
    for enemy in enemies:
        enemyHit = playerToCheck.checkEnemyCollision(enemy)
        if enemyHit and enemy.damaged:
            enemy.timeHit = timeElapsed

        if (timeElapsed - enemy.timeHit) >= 0.25:
            enemy.damaged = False




def redrawBullets() -> None:
    """ Draws and move bullets

    Parameters:


    Return => None
    """
    moveBullets()
    drawBullets()


def redrawGrenades() -> None:
    """ Draws and move grenades

    Parameters:


    Return => None
    """
    moveGrenades()
    drawGrenades()


def redrawCollectibles(playerToCheck: Player) -> None:
    """ Draws and checks collisions for collectibles

    Parameters:
        playerToCheck: Player
            The player whom to check collision for

    Return => None
    """
    drawCollectibles()
    for collectible in collectibles:
        playerToCheck.checkCollectibleCollision(collectible)


def redrawChest(playerToCheck: Player) -> None:
    """ Draws and checks collisions for chests

    Parameters:
        playerToCheck: Player
            The player whom to check collision for

    Return => None
    """
    drawChests()
    for chest in chests:
        playerToCheck.checkChestCollision(chest)


def drawHealthBar(playerToCheck: Player, y: int) -> None:
    """ Draws health bar

    Parameters:
        playerToCheck: Player
            The player whose health to draw

        y: float
            the y position where the health bar is draw


    Return => None
    """
    # drawing player health in chunks of 5 ------------------------------------
    for j in range(int(playerToCheck.health // 5)):
        # health
        pygame.draw.rect(gameWindow, RED, (WIDTH - 366 + (j * 14), y + 3, 14, 30), 0, 0)
        pygame.draw.rect(gameWindow, LRED, (WIDTH - 366 + (j * 14), y + 8, 14, 6), 0, 0)

        # drawing over edges of health bar
        if j == 0:
            pygame.draw.rect(gameWindow, RED, (WIDTH - 366, y + 3, 6, 30), 0, 0)
        if j == (playerToCheck.health // 5) - 1:
            pygame.draw.rect(gameWindow, RED, (WIDTH - 366 + (j * 14) + 8, y + 3, 6, 30), 0, 0)

    # -------------------------------------------------------------------------

    # border ------------------------------------------------------------------
    pygame.draw.rect(gameWindow, BLACK, (WIDTH - 370, y, 286, 36), 5, 8)
    pygame.draw.rect(gameWindow, (64, 64, 64), (WIDTH - 370, y - 2, 288, 40), 3, 8)

    # -------------------------------------------------------------------------


def drawCoinDisplay() -> None:
    """ Draws coin display at the top left corner

    Parameters:


    Return => None
    """

    # changes colour based on background ------------------------------
    colour = BLACK if level.background is iceBackgroundImage else WHITE

    # rendering text, with antialias off ------------------------------
    xRender = scoreFontSmall.render("x", False, colour)
    scoreRender = scoreFont.render(f"{coinsCollected}", False, colour)

    # blitting text and images ----------------------------------------
    # gameWindow.blit(coinIcon, (WIDTH - 470, 16))
    # gameWindow.blit(xRender, (WIDTH - 495, 30))
    # gameWindow.blit(scoreRender, (WIDTH - 500 - scoreWidth, 20))
    gameWindow.blit(coinIcon, (30, 16))
    gameWindow.blit(xRender, (85, 30))
    gameWindow.blit(scoreRender, (100, 20))


def drawBulletDisplay(timeSinceFire: float, fireRate: float, y: float) -> None:
    """ draws bullet display at bottom right corner - time until you can fire again.
        The bullet is "greyed out" and slowly "reloads"

    Parameters:
        timeSinceFire: float
            The time since firing

        fireRate: float
            fire rate of the weapon

        y: float
            The y position of the bullet


    Return => None
    """
    # draws different versions of the bullet depending on 'timeSinceFire'
    if round(timeSinceFire, 2) <= round(fireRate / 6, 2):
        gameWindow.blit(bulletGUI[0], (WIDTH - 80, y))

    elif round(timeSinceFire, 2) <= round(fireRate / 3, 2):
        gameWindow.blit(bulletGUI[1], (WIDTH - 80, y))

    elif round(timeSinceFire, 2) <= round(fireRate / 2, 2):
        gameWindow.blit(bulletGUI[2], (WIDTH - 80, y))

    elif round(timeSinceFire, 2) <= round(fireRate / 1.25, 2):
        gameWindow.blit(bulletGUI[3], (WIDTH - 80, y))

    else:
        gameWindow.blit(bulletGUI[4], (WIDTH - 80, y))


def drawMagazineDisplay(playerToCheck: Player, timeSinceFire: float, fireRate: float, y: float) -> None:
    """ draws bullet display at bottom right corner - time until you can fire again.
        The bullet is "greyed out" and slowly "reloads"

    Parameters:
        playerToCheck: Player
            The player to display

        timeSinceFire: float
            The time since firing

        fireRate: float
            Fire rate of the weapon

        y: float
            Where to display the magazine

    Return => None
    """
    # draws different versions of the bullet depending on 'timeSinceFire'
    if playerToCheck.currentWeapon.bulletsInMagazine == 0:
        drawBulletDisplay(timeSinceFire, fireRate, y)

    elif playerToCheck.currentWeapon.bulletsInMagazine == playerToCheck.currentWeapon.clipSize // 4:
        gameWindow.blit(bulletGUI[1], (WIDTH - 80, y))

    elif playerToCheck.currentWeapon.bulletsInMagazine == playerToCheck.currentWeapon.clipSize // 4 * 2:
        gameWindow.blit(bulletGUI[2], (WIDTH - 80, y))

    elif playerToCheck.currentWeapon.bulletsInMagazine == playerToCheck.currentWeapon.clipSize // 4 * 3:
        gameWindow.blit(bulletGUI[3], (WIDTH - 80, y))

    else:
        gameWindow.blit(bulletGUI[4], (WIDTH - 80, y))
    # displays the player name in middle of the bullet
    gameWindow.blit(playerToCheck.nameRender, (WIDTH - 80 + bulletGUI[0].get_size()[0] / 2,
                                               y + bulletGUI[0].get_size()[1] / 2 - playerToCheck.nameRender.get_size()[
                                                   1] / 2))


def drawWeaponDisplay(playerToCheck: Player, y) -> None:
    """ Draws weapon display under the health bar

    Parameters:
        playerToCheck: Player
            The player whose weapon is displayed

        y: float
            the y position where the weapon is displayed



    Return => None
    """
    # changing colour if the background is the underworld one
    colour = (32, 32, 32) if level.background is iceBackgroundImage else WHITE

    # rendering name
    weaponName = scoreFontSmall.render(playerToCheck.currentWeapon.name, True, colour)
    weaponNameLength = weaponName.get_size()[0]

    # blits name based on width of weapon name
    gameWindow.blit(weaponName, (WIDTH - 226 - weaponNameLength / 2, y))


def drawInstructions() -> None:
    """ Draws the instructions for moving, jumping, and shooting

    Parameters:


    Return => None
    """
    global tutorialLettersToRender, instructionNum, timeOfFinishedWriting

    # rendering
    drawInstruction(instructions[instructionNum], tutorialLettersToRender // 2, WHITE)

    # typed-out animation
    if tutorialLettersToRender < len(instructions[instructionNum]) * 2:
        tutorialLettersToRender += 1
        timeOfFinishedWriting = timeElapsed

    # flipping to next instructions
    elif timeElapsed - timeOfFinishedWriting >= 2:
        instructionNum += 1
        tutorialLettersToRender = 0
    
        


def drawWeaponUnlock():
    global weaponUnlockLettersToRender, weaponUnlockMessage, timeOfFinishedWriting

    drawInstruction(weaponUnlockMessage, weaponUnlockLettersToRender // 2, WHITE)

    # typed-out animation
    if weaponUnlockLettersToRender < len(weaponUnlockMessage) * 2:
        weaponUnlockLettersToRender += 1
        timeOfFinishedWriting = timeElapsed

def drawMiscWeaponUnlock():
    global weaponUnlockMiscLettersToRender, weaponUnlockMessageMisc, timeOfFinishedWriting

    drawInstruction(weaponUnlockMessageMisc, weaponUnlockMiscLettersToRender // 2, BLACK)

    # typed-out animation
    if weaponUnlockMiscLettersToRender < len(weaponUnlockMessageMisc) * 2:
        weaponUnlockMiscLettersToRender += 1
        timeOfFinishedWriting = timeElapsed


def drawInstruction(messageToWrite: str, lettersToRender: int, colour: tuple[int, int, int]) -> None:
    """ Draws an instruction with the 'typed-out' animation

    Parameters:
        messageToWrite: str
            The str to write

        lettersToRender: int
            The number of letters in the string to render

        colour: tuple[int, int, int]
            The colour to draw the instructions of


    Return => None
    """
    instruction = instructionFont.render(messageToWrite[:lettersToRender], False, colour)
    instructionWidth = instructionFont.size(messageToWrite[:lettersToRender])[0]
    gameWindow.blit(instruction, (WIDTH / 2 - instructionWidth / 2, HEIGHT - 100))


def drawGUI(playerList: list[Player]) -> None:
    """ Draws GUI by combining the drawHealthBar(), drawCoinDisplay(), and drawWeaponDisplay() functions

    Parameters:
        playerList: list[Player]
            The list of players on which to draw the GUI for


    Return => None
    """
    yPos = 25
    for play in playerList:
        drawHealthBar(play, yPos)
        drawWeaponDisplay(play, yPos + 35)
        yPos += 70

    drawCoinDisplay()
    # only draws instructions if the level is the tutorial level and its not finished drawing
    if instructionNum < len(instructions):
        drawInstructions()

    # only draws weapon unlock message if the level is 6 and total amount of platforms generated is less than 8
    if levelNumber == 6 and level.numOfPlatforms < 8:
        drawWeaponUnlock()

    if levelNumber == 11 and level.numOfPlatforms < 8:
        drawMiscWeaponUnlock()

def checkQuit() -> bool:
    """ Checks if the ESCAPE or QUIT button has been pressed, and returns True if so

    Parameters:


    Return => bool: if the quit event has been detected
    """
    # ESC key and QUIT button
    if keys[pygame.K_ESCAPE]:
        return True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False


def forEachPlayer(playerList: list[Player], func: Callable[[Player, ...], Any], *args) -> None:
    """ Calls 'func' with each player as the argument individually

    Parameters:
        playerList: list[Player]
            A list of players, which are passed into the function one by one

        func: Callable[[Player, ...], Any]
            A function that takes a player, and any number or type of arguments after than, and returns Any.
            This function will be called on each player in 'playerList'

        *args:
            optional arguments that are passed if 'func' needs arguments


    Return => bool: if the quit event has been detected
    """
    for playerToCheck in playerList:
        func(playerToCheck, *args)


def everyPlayer(playerList: list[Player], func: Callable[[Player], bool]) -> bool:
    """ returns if every player in 'playerList' passes the implemented test function('func')

    Parameters:
        playerList: list[Player]
            A list of players, which are passed into the function one by one

        func: Callable[[Player, ...], Any]
            A function that takes a player as an argument and returns a boolean.
            This function will be called on each player in 'playerList'


    Return => bool: if the quit event has been detected
    """
    every = True
    for playerToCheck in playerList:
        if not func(playerToCheck):
            every = False
    return every


def anyPlayer(playerList: list[Player], func: Callable[[Player], bool]) -> bool:
    """ returns if any player in 'playerList' passes the implemented test function('func')

    Parameters:
        playerList: list[Player]
            A list of players, which are passed into the function one by one

        func: Callable[..., Any]
            A function that takes a player as an argument and returns a boolean.
            This function will be called on each player in 'playerList'


    Return => bool: if the quit event has been detected
    """
    for playerToCheck in playerList:
        if func(playerToCheck):
            return True
    return False


# Timer
FPS = 60
fpsClock = pygame.time.Clock()
timeElapsed = 0


###############################################################################
#
# Weapon Info
#
###############################################################################

# pistol
PISTOL_FIRE_RATE = 1
PISTOL_DAMAGE = 40

# machine gun
ASSAULT_RIFLE_FIRE_RATE = 0.4
ASSAULT_RIFLE_DAMAGE = 30

# shotgun
SHOTGUN_FIRE_RATE = 2.5
SHOTGUN_DAMAGE = 200

# sniper
SNIPER_FIRE_RATE = 4
SNIPER_DAMAGE = 180

# machine gun
MACHINE_GUN_FIRE_RATE = 0.08
MACHINE_GUN_DAMAGE = 20

# grenade launcher
GRENADE_LAUNCHER_FIRE_RATE = 6
GRENADE_LAUNCHER_DAMAGE = 160

# delay constants
INVINCIBLE_DELAY = 0.35

# menu variables
menuImagesX = 0

###############################################################################
#
# Initialization of game variables
#
###############################################################################
# num of players
numOfPlayers = 1

# Player and spawn platform
players = [
    Player(100, 0.25, 5, 2.75, 15, 250, HEIGHT // 2 - 120, Pistol(), True, "p1"),
    Player(100, 0.25, 5, 2.75, 15, 250, HEIGHT // 2 - 120, Pistol(), False, "p2"),
]

# lists
enemies = []
collectibles = []
bullets = []
grenades = []
chests = []
portals = []

# coins collected
coinsCollected = 0

# initial level
level = Level(8)

# Level number - 0 is tutorial
levelNumber = 0
# if the player if transitioning between levels
levelTransition = False

# maximum platforms
MAX_PLATFORMS = 100

# cost of a potion from an upgrade chest
POTION_COST = 10

# the time that a chest is opened - allows a cooldown
timeOpened = 0

# all weapons - used for weapon generation
weapons = {
    # available any level
    "default": [
        Pistol(),
        AssaultRifle(),
        SubMachineGun(),
        MachineGun(),
        SniperRifle(),
        Shotgun(),
        GrenadeLauncher(),
        FlameThrower(),
        MissileLauncher(),
    ],

    # after level 5
    "laser": [
        LaserPistol(),
        LaserAssaultRifle(),
        LaserMachineGun(),
        LaserSniperRifle(),
        LaserShotgun(),
    ],

    # after level 10
    "misc": [
        LaserCannon(),
        LightningStaff(),
        PlasmaCannon(),
    ]
}

## Menu Variables ##
titleStr = "Source Code"
titleLettersToRender = 0
timeSelected = 0

## Instructions Variables ##
tutorialLettersToRender = 0
instructionNum = 0
timeOfFinishedWriting = 0
instructions = ["press [a] and [d]/[<] and [>] to move", "press [w]/[^] to jump", "press [space]/[/] to shoot",
                "press [s]/[.] to pick up weapons"]
# laser weapon unlock
weaponUnlockLettersToRender = 0
weaponUnlockMessage = "laser weapons unlocked"
weaponUnlockMiscLettersToRender = 0
weaponUnlockMessageMisc = "more weapons unlocked"

## Pausing Variables ##
timeOfPause = 0

###############################################################################
#
# Loop control variables and music
#
###############################################################################
# loop control variables
inPlay = True
inMenu = True
inGame = True
endScreen = False
paused = False
drawPausedImage = False

# loading menu soundtrack
pygame.mixer.music.unload()
pygame.mixer.music.load("sounds/menuSoundtrack.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

###############################################################################
#
# Menu Loop
#
###############################################################################
while inMenu:
    # resetting 'menuImagesX' to restart the animation loop -----------
    if menuImagesX <= -WIDTH:
        menuImagesX = 0

    # getting all keys ------------------------------------------------
    keys = pygame.key.get_pressed()

    # clearing events -------------------------------------------------
    pygame.event.clear()

    # blitting background ---------------------------------------------
    gameWindow.blit(menuBackgroundImage, (0, 0))
    gameWindow.blit(cloudsImage, (menuImagesX, 0))
    gameWindow.blit(cloudsImage, (menuImagesX + WIDTH, 0))

    # mouse position and button status --------------------------------
    mousePos = pygame.mouse.get_pos()
    mouseClicked = pygame.mouse.get_pressed(3)[0]

    # rendering text --------------------------------------------------
    title = titleFont.render(titleStr[:titleLettersToRender // 3], False, WHITE)
    titleShadow = titleFont.render(titleStr[:titleLettersToRender // 3], False, BLACK)
    playText = subTitleFont.render("Play", False, BLACK)
    playTextShadow = subTitleFont.render("Play", False, WHITE)
    singlePlayerText = smallHeadingFont.render("1 player", False, BLACK)
    singlePlayerTextShadow = smallHeadingFont.render("1 player", False, WHITE)
    multiplayerText = smallHeadingFont.render("2 players", False, BLACK)
    multiplayerTextShadow = smallHeadingFont.render("2 players", False, WHITE)

    # getting the width and height of the title and play text ---------
    titleWidth, titleHeight = titleFont.size(titleStr)
    playTextWidth, playTextHeight = subTitleFont.size("Play")
    singlePlayerTextWidth, singlePlayerTextHeight = smallHeadingFont.size("1 player")
    multiplayerTextWidth, multiplayerTextHeight = smallHeadingFont.size("2 players")

    # setting hitbox for play button ----------------------------------
    playHoverHitbox = pygame.Rect(WIDTH / 2 - playTextWidth / 2, titleHeight + HEIGHT * 41 / 108, playTextWidth, playTextHeight + singlePlayerTextHeight + multiplayerTextHeight + 60)
    playHitbox = pygame.Rect(WIDTH / 2 - playTextWidth / 2, titleHeight + HEIGHT * 41 / 108, playTextWidth, playTextHeight)
    singlePlayerHitbox = pygame.Rect(WIDTH / 2 - playTextWidth / 2, titleHeight + HEIGHT * 41 / 108 + playTextHeight + 30, singlePlayerTextWidth, singlePlayerTextHeight)
    multiplayerHitbox = pygame.Rect(WIDTH / 2 - playTextWidth / 2, titleHeight + HEIGHT * 41 / 108 + playTextHeight + singlePlayerTextHeight + 50, multiplayerTextWidth, multiplayerTextHeight)

    if numOfPlayers == 1:
        singlePlayerText = smallHeadingFont.render(">1 player", False, WHITE)
        singlePlayerTextShadow = smallHeadingFont.render(">1 player", False, BLACK)
        singlePlayerTextWidth, singlePlayerTextHeight = smallHeadingFont.size(">1 player")

    elif numOfPlayers == 2:
        multiplayerText = smallHeadingFont.render(">2 players", False, WHITE)
        multiplayerTextShadow = smallHeadingFont.render(">2 players", False, BLACK)
        multiplayerTextWidth, multiplayerTextHeight = smallHeadingFont.size(">2 players")

    # makes the text white upon hover ---------------------------------
    if playHoverHitbox.collidepoint(mousePos):

        if singlePlayerHitbox.collidepoint(mousePos) and mouseClicked and timeElapsed - timeSelected >= 0.25:
            numOfPlayers = 1
            menuSelect.play()
            timeSelected = timeElapsed


        if multiplayerHitbox.collidepoint(mousePos) and mouseClicked and timeElapsed - timeSelected >= 0.25:
            numOfPlayers = 2
            menuSelect.play()
            timeSelected = timeElapsed

        # inverting colours
        playText = subTitleFont.render("Play", True, WHITE)
        playTextShadow = subTitleFont.render("Play", False, BLACK)
        gameWindow.blit(singlePlayerTextShadow, (WIDTH / 2 - singlePlayerTextWidth / 2 + 2, titleHeight + HEIGHT * 41 / 108 + playTextHeight + 2 + 30))
        gameWindow.blit(singlePlayerText, (WIDTH / 2 - singlePlayerTextWidth / 2, titleHeight + HEIGHT * 41 / 108 + playTextHeight + 30))
        gameWindow.blit(multiplayerTextShadow, (WIDTH / 2 - multiplayerTextWidth / 2 + 2, titleHeight + HEIGHT * 41 / 108 + playTextHeight + 2 + 50 + singlePlayerTextHeight))
        gameWindow.blit(multiplayerText, (WIDTH / 2 - multiplayerTextWidth / 2, titleHeight + HEIGHT * 41 / 108 + playTextHeight + 50 + singlePlayerTextHeight))

    # starts the game upon hover and click ----------------------------
    if playHitbox.collidepoint(mousePos) and mouseClicked:
        menuSelect.play()
        inMenu = False

    # line decorations ------------------------------------------------
    pygame.draw.line(gameWindow, WHITE, (WIDTH / 2 - titleWidth / 2, 40), (WIDTH / 2 + titleWidth / 2, 40))
    pygame.draw.line(gameWindow, WHITE, (WIDTH / 2 - titleWidth / 2, 36), (WIDTH / 2 + titleWidth / 2, 36))
    pygame.draw.line(gameWindow, WHITE, (WIDTH / 2 - titleWidth / 2, 40 + titleHeight + 8),
                     (WIDTH / 2 + titleWidth / 2, 40 + titleHeight + 8))
    pygame.draw.line(gameWindow, WHITE, (WIDTH / 2 - titleWidth / 2, 40 + titleHeight + 12),
                     (WIDTH / 2 + titleWidth / 2, 40 + titleHeight + 12))

    # blitting text ---------------------------------------------------
    gameWindow.blit(titleShadow, (WIDTH / 2 - titleWidth / 2 + 12, 52))
    gameWindow.blit(title, (WIDTH / 2 - titleWidth / 2, 40))

    gameWindow.blit(playTextShadow, (WIDTH / 2 - playTextWidth / 2 + 4, titleHeight + (HEIGHT * 41 / 108) + 4))
    gameWindow.blit(playText, (WIDTH / 2 - playTextWidth / 2, titleHeight + HEIGHT * 41 / 108))

    # check for quit events -------------------------------------------
    if checkQuit():
        inMenu = False
        inPlay = False
        inGame = False

    # decrementing 'menuImagesX' to move the background ---------------
    menuImagesX -= 1

    # incrementing 'lettersToRender' for a typed-out animation
    if titleLettersToRender < (len(titleStr) + 1) * 3:
        titleLettersToRender += 1

    # accumulates time  ---------------------------------------------------
    time = fpsClock.tick(FPS)
    timeElapsed += time / 1000

    # updating screen -------------------------------------------------
    pygame.display.update()

# -----------------------------------------------------------------------------

# generates the correct number of players
players = [
    Player(100, 0.25, 5, 2.75, 15, 250, HEIGHT // 2 - 120, Pistol(), i % 2 == 1, f"p{i}") for i in range(1, numOfPlayers + 1)
]

timeElapsed = 0

#######################################################################################################################
#
# Main Loop: Game Loop + Restart Menu
#
#######################################################################################################################
while inGame:
    # clearing events -------------------------------------------------
    pygame.event.clear()

    # getting all keys ------------------------------------------------
    keys = pygame.key.get_pressed()

    # mouse position and button status --------------------------------
    mousePos = pygame.mouse.get_pos()
    mouseClicked = pygame.mouse.get_pressed(3)[0]

    # restarts music --------------------------------------------------
    if not endScreen and not paused and inPlay and not drawPausedImage:
        pygame.time.delay(300)
        pygame.mixer.music.unload()
        pygame.mixer.music.load("sounds/soundtrack.mp3")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)

    ###########################################################################################
    #
    # Game Loop
    #
    ###########################################################################################
    while inPlay and not paused:
        # getting all keys ----------------------------------------------------
        keys = pygame.key.get_pressed()

        # mouse position and button status ------------------------------------
        mousePos = pygame.mouse.get_pos()
        mouseClicked = pygame.mouse.get_pressed(3)[0]

        # clearing events -----------------------------------------------------
        pygame.event.clear()

        # Adding background ---------------------------------------------------
        gameWindow.blit(level.background, (0, 0))

        # Redraws chests ------------------------------------------------------
        forEachPlayer(players, redrawChest)

        # drawing player, and ending game if collision occurs -----------------
        forEachPlayer(players, redrawPlayer)

        if everyPlayer(players, lambda playerToCheck: playerToCheck.checkLife()) or levelNumber >= 16:
            inPlay = False
            endScreen = True

        # platforms-player collision ------------------------------------------
        forEachPlayer(players, level.checkPlayerCollision)

        # drawing platforms ---------------------------------------------------
        level.redrawPlatforms()

        # draws portals -------------------------------------------------------
        drawPortals()

        # player-enemies ------------------------------------------------------
        forEachPlayer(players, checkEnemyInvincibilityCooldown)

        # drawing enemies -----------------------------------------------------
        redrawEnemies()

        # draws GUI -----------------------------------------------------------
        drawGUI(players)

        # redraws bullets -----------------------------------------------------
        redrawBullets()

        # redraws grenades ----------------------------------------------------
        redrawGrenades()

        # checks for bullet collision -----------------------------------------
        forEachPlayer(players, checkBulletCollision)

        # checks for grenade collision ----------------------------------------
        checkGrenadeCollision()

        # draws collectibles and detects collision ----------------------------
        forEachPlayer(players, redrawCollectibles)

        # checks if new level has to be generated -----------------------------
        level = generateLevel(players)

        # moves background  ---------------------------------------------------
        if anyPlayer(players, lambda playerCheck: playerCheck.x >= 200):
            moveBackground(1)

        elif levelNumber == 0 and timeElapsed - timeOfFinishedWriting < 4:
            moveBackground(0)
            
        else:
            moveBackground(0.5)

        # accumulates time  ---------------------------------------------------
        time = fpsClock.tick(FPS)
        timeElapsed += time / 1000

        # Checking for quit events  -------------------------------------------
        if checkQuit():
            inPlay = False
            inGame = False

        # gets the width and height of the buttons ----------------------------
        pauseButtonWidth, pauseButtonHeight = pauseButton.get_size()
        pauseButtonPressedWidth, pauseButtonPressedHeight = pauseButtonPressed.get_size()

        # makes the hitbox ----------------------------------------------------
        pauseButtonHitbox = pygame.Rect(WIDTH - 10 - pauseButtonWidth, 22, pauseButtonWidth, pauseButtonHeight)

        # Checking for pause events with the pause button ---------------------
        if pauseButtonHitbox.collidepoint(mousePos) and mouseClicked and not paused and timeElapsed - timeOfPause >= 0.4:
            paused = True
            drawPausedImage = True
            timeOfPause = timeElapsed
            gameWindow.blit(pauseButtonPressed, (WIDTH - 10 - pauseButtonWidth, 86 - pauseButtonPressedHeight))
        else:
            gameWindow.blit(pauseButton, (WIDTH - 10 - pauseButtonWidth, 86 - pauseButtonHeight))

        # updating screen  ----------------------------------------------------
        pygame.display.update()

    # End of game loop ------------------------------------------------------------------------

    ###########################################################################################
    #
    # Resetting game and pause functionality
    #
    ###########################################################################################

    # plays death sound and stops soundtrack --------------------------
    if not inPlay:
        playerDies.play()
        pygame.mixer.music.pause()

    # resets menu animation -------------------------------------------
    menuImagesX = 0

    # initializing 'showExit' for the arrow button
    showExit = False

    # adds a delay between arrow presses
    timeSinceArrowPress = 0

    # death message
    if levelNumber >= 16:
        deathMessage = "you have beat the game!"
    elif levelNumber == 0:
        deathMessage = "congrats! you died in the tutorial level!"
    else:
        deathMessage = f"You made it to level {levelNumber}!"

    # animation control -----------------------------------------------
    deathMessageLetters = 0

    # gets the width and height of the button -------------------------
    pauseButtonWidth, pauseButtonHeight = pauseButton.get_size()

    # makes the hitbox ------------------------------------------------
    pauseButtonHitbox = pygame.Rect(WIDTH - 10 - pauseButtonWidth, 22, pauseButtonWidth, pauseButtonHeight)

    # Allows for unpausing --------------------------------------------
    # draws translucent image when paused
    if paused and drawPausedImage:
        gameWindow.blit(pausedImage, (0, 0))
        pygame.display.update()
        drawPausedImage = False

    # Checking for quit events  ---------------------------------------
    if checkQuit():
        inPlay = False
        inGame = False

    # Checking for pause events - click event -------------------------
    if pauseButtonHitbox.collidepoint(mousePos) and mouseClicked and paused and timeElapsed - timeOfPause >= 0.4:
        paused = False
        timeOfPause = timeElapsed

    # accumulates time  -----------------------------------------------
    time = fpsClock.tick(FPS)
    timeElapsed += time / 1000

    # -------------------------------------------------------------------------

    ###########################################################################################
    #
    # Restart Loop
    #
    ###########################################################################################
    while endScreen:
        # resetting 'menuImagesX' to restart the animation loop ---------------
        if menuImagesX <= -WIDTH:
            menuImagesX = 0

        # getting all keys ----------------------------------------------------
        keys = pygame.key.get_pressed()

        # clearing events -----------------------------------------------------
        pygame.event.clear()

        # blitting background -------------------------------------------------
        gameWindow.blit(menuBackgroundImage, (0, 0))
        gameWindow.blit(cloudsImage, (menuImagesX, 0))
        gameWindow.blit(cloudsImage, (menuImagesX + WIDTH, 0))

        # mouse position and button status ------------------------------------
        mousePos = pygame.mouse.get_pos()
        mouseClicked = pygame.mouse.get_pressed(3)[0]

        # rendering text and its shadows --------------------------------------
        # title
        title = titleFont.render(titleStr, False, WHITE)
        titleShadow = titleFont.render(titleStr, False, BLACK)

        # restart text
        restartText = subTitleFont.render("Play Again", False, BLACK)
        restartTextShadow = subTitleFont.render("Play Again", False, WHITE)

        # exit text
        exitText = subTitleFont.render("Exit", False, BLACK)
        exitTextShadow = subTitleFont.render("Exit", False, WHITE)

        # arrows
        rightArrowText = subTitleFont.render(">", False, BLACK)
        rightArrowTextShadow = subTitleFont.render(">", False, WHITE)

        leftArrowText = subTitleFont.render("<", False, BLACK)
        leftArrowTextShadow = subTitleFont.render("<", False, WHITE)

        # death messages
        deathMessageText = deathMessageFont.render(deathMessage[:deathMessageLetters // 3], False, WHITE)
        deathMessageTextShadow = deathMessageFont.render(deathMessage[:deathMessageLetters // 3], False, BLACK)

        # getting the width and height of the title and restart text ----------
        titleWidth, titleHeight = titleFont.size(titleStr)

        restartTextWidth, restartTextHeight = subTitleFont.size("Play Again")

        exitTextWidth, exitTextHeight = subTitleFont.size("Exit")

        rightArrowTextWidth, rightArrowTextHeight = subTitleFont.size(">")

        leftArrowTextWidth, leftArrowTextHeight = subTitleFont.size("<")

        deathMessageTextWidth, deathMessageTextHeight = deathMessageFont.size(deathMessage[:deathMessageLetters // 3])

        # setting hitbox for restart button -----------------------------------
        restartHitbox = pygame.Rect(WIDTH / 2 - restartTextWidth / 2, titleHeight + HEIGHT * 41 / 108, restartTextWidth, restartTextHeight)

        # setting hitbox for exit button --------------------------------------
        exitHitbox = pygame.Rect(WIDTH / 2 - exitTextWidth / 2, titleHeight + HEIGHT * 41 / 108, exitTextWidth, exitTextHeight)

        # setting hitbox for exit button --------------------------------------
        if showExit:
            rightArrowHitbox = pygame.Rect(WIDTH / 2 + exitTextWidth / 2, titleHeight + HEIGHT * 41 / 108,
                                           rightArrowTextWidth, rightArrowTextHeight)
            leftArrowHitbox = pygame.Rect(WIDTH / 2 - exitTextWidth / 2 - leftArrowTextWidth,
                                          titleHeight + HEIGHT * 41 / 108, leftArrowTextWidth, leftArrowTextHeight)

        else:
            rightArrowHitbox = pygame.Rect(WIDTH / 2 + restartTextWidth / 2, titleHeight + HEIGHT * 41 / 108,
                                           rightArrowTextWidth, rightArrowTextHeight)
            leftArrowHitbox = pygame.Rect(WIDTH / 2 - restartTextWidth / 2 - leftArrowTextWidth,
                                          titleHeight + HEIGHT * 41 / 108, leftArrowTextWidth, leftArrowTextWidth)

        # makes the 'play again' text white upon hover ------------------------
        if restartHitbox.collidepoint(mousePos) and not showExit:
            restartText = subTitleFont.render("Play Again", True, WHITE)
            restartTextShadow = subTitleFont.render("Play Again", True, BLACK)

        # makes the 'exit' text white upon hover ------------------------------
        if exitHitbox.collidepoint(mousePos) and showExit:
            exitText = subTitleFont.render("Exit", True, WHITE)
            exitTextShadow = subTitleFont.render("Exit", True, BLACK)

        # makes the '>' text white upon hover ---------------------------------
        if rightArrowHitbox.collidepoint(mousePos):
            rightArrowText = subTitleFont.render(">", True, WHITE)
            rightArrowTextShadow = subTitleFont.render(">", True, BLACK)

        # makes the '<' text white upon hover ---------------------------------
        if leftArrowHitbox.collidepoint(mousePos):
            leftArrowText = subTitleFont.render("<", True, WHITE)
            leftArrowTextShadow = subTitleFont.render("<", True, BLACK)

        # switching from 'exit' to 'play again' upon click
        if (rightArrowHitbox.collidepoint(mousePos) or leftArrowHitbox.collidepoint(mousePos)) and mouseClicked:
            showExit = not showExit
            timeSinceArrowPress = timeElapsed

        # resets and restarts the game upon hover and click -------------------
        if restartHitbox.collidepoint(mousePos) and mouseClicked and not showExit and timeElapsed - timeSinceArrowPress >= 0.25:
            inPlay = True
            endScreen = False

            # resetting game ------------------------------------------
            players = [
                Player(100, 0.25, 5, 2.75, 15, 250, HEIGHT // 2 - 120, Pistol(), i % 2 == 1, f"p{i}") for i in range(1, numOfPlayers + 1)
            ]

            # clearing lists ------------------------------------------
            enemies.clear()
            collectibles.clear()
            coinsCollected = 0
            for player in players:
                player.damageMultiplier = 1
            bullets.clear()
            grenades.clear()
            chests.clear()
            portals.clear()

            # reset level ---------------------------------------------
            level = Level(8)
            levelNumber = 0

            # if the player if transitioning between levels -----------
            levelTransition = False

        # ---------------------------------------------------------------------

        # exits the game upon hover and click ---------------------------------
        if exitHitbox.collidepoint(mousePos) and mouseClicked and showExit and timeElapsed - timeSinceArrowPress >= 0.25:
            inMenu = False
            inGame = False
            inPlay = False
            endScreen = False

        # line decorations ------------------------------------------------
        pygame.draw.line(gameWindow, WHITE, (WIDTH / 2 - titleWidth / 2, 40), (WIDTH / 2 + titleWidth / 2, 40))
        pygame.draw.line(gameWindow, WHITE, (WIDTH / 2 - titleWidth / 2, 36), (WIDTH / 2 + titleWidth / 2, 36))
        pygame.draw.line(gameWindow, WHITE, (WIDTH / 2 - titleWidth / 2, 40 + titleHeight + 8), (WIDTH / 2 + titleWidth / 2, 40 + titleHeight + 8))
        pygame.draw.line(gameWindow, WHITE, (WIDTH / 2 - titleWidth / 2, 40 + titleHeight + 12), (WIDTH / 2 + titleWidth / 2, 40 + titleHeight + 12))

        # blitting text -------------------------------------------------------
        gameWindow.blit(titleShadow, (WIDTH / 2 - titleWidth / 2 + 12, 52))
        gameWindow.blit(title, (WIDTH / 2 - titleWidth / 2, 40))

        gameWindow.blit(deathMessageTextShadow, (WIDTH / 2 - deathMessageTextWidth / 2 + 4, titleHeight + HEIGHT * 52 / 108 + 4))
        gameWindow.blit(deathMessageText, (WIDTH / 2 - deathMessageTextWidth / 2, titleHeight + HEIGHT * 52 / 108))

        # drawing different buttons based on the 'showExit' flag
        if not showExit:
            # restart text
            gameWindow.blit(restartTextShadow, (WIDTH / 2 - restartTextWidth / 2 + 4, titleHeight + HEIGHT * 41 / 108 + 4))
            gameWindow.blit(restartText, (WIDTH / 2 - restartTextWidth / 2, titleHeight + HEIGHT * 41 / 108))

            # right arrow text
            gameWindow.blit(rightArrowTextShadow, (WIDTH / 2 + restartTextWidth / 2 + 4, titleHeight + HEIGHT * 41 / 108 + 4))
            gameWindow.blit(rightArrowText, (WIDTH / 2 + restartTextWidth / 2, titleHeight + HEIGHT * 41 / 108))

            # left arrow text
            gameWindow.blit(leftArrowTextShadow, (WIDTH / 2 - restartTextWidth / 2 - leftArrowTextWidth + 4, titleHeight + HEIGHT * 41 / 108 + 4))
            gameWindow.blit(leftArrowText, (WIDTH / 2 - restartTextWidth / 2 - leftArrowTextWidth, titleHeight + HEIGHT * 41 / 108))

        else:
            # exit text
            gameWindow.blit(exitTextShadow, (WIDTH / 2 - exitTextWidth / 2 + 4, titleHeight + HEIGHT * 41 / 108 + 4))
            gameWindow.blit(exitText, (WIDTH / 2 - exitTextWidth / 2, titleHeight + HEIGHT * 41 / 108))

            # right arrow text
            gameWindow.blit(rightArrowTextShadow, (WIDTH / 2 + exitTextWidth / 2 + 4, titleHeight + HEIGHT * 41 / 108 + 4))
            gameWindow.blit(rightArrowText, (WIDTH / 2 + exitTextWidth / 2, titleHeight + HEIGHT * 41 / 108))

            # left arrow text
            gameWindow.blit(leftArrowTextShadow, (WIDTH / 2 - exitTextWidth / 2 - leftArrowTextWidth + 4, titleHeight + HEIGHT * 41 / 108 + 4))
            gameWindow.blit(leftArrowText, (WIDTH / 2 - exitTextWidth / 2 - leftArrowTextWidth, titleHeight + HEIGHT * 41 / 108))

        # check for quit events -----------------------------------------------
        if checkQuit():
            inMenu = False
            inGame = False
            inPlay = False
            endScreen = False

        # decrementing 'menuImagesX' to move the background -------------------
        menuImagesX -= 1

        if deathMessageLetters < len(deathMessage) * 3:
            deathMessageLetters += 1

        # accumulates the time ------------------------------------------------
        time = fpsClock.tick(FPS)
        timeElapsed += time / 1000

        # updating screen -----------------------------------------------------
        pygame.display.update()

# quitting pygame
pygame.quit()
