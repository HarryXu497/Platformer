import pygame
from random import randint, uniform

# Colours ---------------------------------------------------------------------
WHITE = (255, 255, 255)
RED = (255, 0, 0)
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

# Game Window Options ---------------------------------------------------------
pygame.init()
WIDTH = 800
HEIGHT = 600
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))

# Game icon and caption ----------------------------------------
icon = pygame.image.load("images/character/running/running2.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Players, Platforms, and Enemies")

# Images not associated with a class ------------------------------------------
backgroundImage = pygame.image.load("images/backgrounds/background.jpg")
underworldBackgroundImage = pygame.image.load("images/backgrounds/underworld.png")
iceBackgroundImage = pygame.image.load("images/backgrounds/iceBackground.png")

# tile images needed for comparison
grassTile = pygame.image.load("images/tiles/grassTile/tile.png")
underworldTile = pygame.image.load("images/tiles/underworldTile.png")
iceTile = pygame.image.load("images/tiles/iceTile.jpg")

# resizing images
backgroundImage = pygame.transform.scale(backgroundImage, (WIDTH, HEIGHT))
underworldBackgroundImage = pygame.transform.scale(underworldBackgroundImage, (WIDTH, HEIGHT))
iceBackgroundImage = pygame.transform.scale(iceBackgroundImage, (WIDTH, HEIGHT))

coinIcon = pygame.image.load("images/coin/coinIcon.png")

# Bullet GUI images
bulletGUI = [
    pygame.image.load("images/gui/bullet/bullet1.png"),
    pygame.image.load("images/gui/bullet/bullet2.png"),
    pygame.image.load("images/gui/bullet/bullet3.png"),
    pygame.image.load("images/gui/bullet/bullet4.png"),
    pygame.image.load("images/gui/bullet/bullet5.png"),
]

grenadeGUI = [
    pygame.image.load("images/gui/grenade/grenade.png"),
]

# menu animation images
menuBackgroundImage = pygame.image.load("images/backgrounds/background.jpg")
menuBackgroundImage = pygame.transform.scale(menuBackgroundImage, (WIDTH, HEIGHT))

# Sounds ----------------------------------------------------------------------
pygame.mixer.init()

playerHit = pygame.mixer.Sound("sounds/player/playerHit.wav")
coinCollected = pygame.mixer.Sound("sounds/collectibles/coinCollected.wav")
potionCollected = pygame.mixer.Sound("sounds/collectibles/potionCollected.wav")

bulletFired = pygame.mixer.Sound("sounds/player/bullet/bulletFired.wav")
shotgunFired = pygame.mixer.Sound("sounds/player/bullet/shotgunFired.wav")
grenadeExplosion = pygame.mixer.Sound("sounds/player/grenade/explosion.mp3")
pickupWeapon = pygame.mixer.Sound("sounds/player/pickup/pickupWeapon.mp3")

enemyHitSound = pygame.mixer.Sound("sounds/enemy/enemyHit.wav")
enemyHitSound.set_volume(0.75)

laserFired = pygame.mixer.Sound("sounds/player/laser/laser.mp3")
sniperLaserFired = pygame.mixer.Sound("sounds/player/laser/sniperLaser.wav")

portalEnter = pygame.mixer.Sound("sounds/portal/portal.wav")

playerDies = pygame.mixer.Sound("sounds/player/playerDeath.wav")

# soundtrack
pygame.mixer.music.load("sounds/soundtrack.mp3")

# Fonts -----------------------------------------------------------------------
scoreFont = pygame.font.Font("fonts/ScoreFont.ttf", 50)
scoreFontSmall = pygame.font.Font("fonts/ScoreFont.ttf", 32)
titleFont = pygame.font.Font("fonts/TitleFontBold.ttf", (120 * WIDTH)//800)
subTitleFont = pygame.font.Font("fonts/TitleFontBold.ttf", (70 * WIDTH)//800)


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
    """

    def __init__(self, health: int, accelerationX: float, accelerationY: float, maxSpeedX: float, maxSpeedY: float,
                 x: float, y: float, currentWeapon) -> None:
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

        # Animation images
        self.hurt = [
            pygame.image.load("images/character/hurt/hurt1.png"),
        ]

        self.idle = [
            pygame.image.load("images/character/idle/idle1.png"),
            pygame.image.load("images/character/idle/idle2.png"),
        ]

        self.jumpOrFall = [
            pygame.image.load("images/character/jump/jump.png"),
            pygame.image.load("images/character/jump/fall.png"),
        ]

        self.running = [
            pygame.image.load("images/character/running/running1.png"),
            pygame.image.load("images/character/running/running2.png"),
            pygame.image.load("images/character/running/running3.png"),
            pygame.image.load("images/character/running/running4.png"),
            pygame.image.load("images/character/running/running5.png"),
            pygame.image.load("images/character/running/running6.png"),
        ]

        # Current image
        self.currentImage = self.idle[0]

        # Tracks the current stage of each animation
        self.hurtStage = 0
        self.idleStage = 0
        self.jumpOrFallStage = 0
        self.runningStage = 0


    def move(self) -> None:
        """ Responsible for getting keyboard input and moving the player.
            Also controls a lot of the animation images.

        Parameters:


        Return => None
        """
        # Checks to see if any current stage of any animations will cause an error and resets them if so
        self.checkAnimation()

        # gets all pressed keys
        keys = pygame.key.get_pressed()

        # If 'a' is pressed and the max speed has not exceeded the maximum speed --------------------------------------
        if keys[pygame.K_a] and self.speedX > -self.maxSpeedX + self.accelerationX:

            # Sets the current image of the player depending on how long 'a' has been pressed
            self.currentImage = pygame.transform.flip(self.running[int(self.runningStage // 10)], True, False)

            # sets the 'facingLeft' attribute to True
            self.facingLeft = True

            # Increases speed going left --------------------------------------
            if self.touchingBlock:
                self.speedX -= self.accelerationX

            else:
                # Makes acceleration slower if the player is in the air
                self.speedX -= self.accelerationX / 4

            # Increments the running animation stage and sets the idle stage to 0
            self.runningStage += 1
            self.idleStage = 0


        # If 'd' is pressed and the max speed has not exceeded the maximum speed --------------------------------------
        elif keys[pygame.K_d] and self.speedX < self.maxSpeedX - self.accelerationX:

            # Sets the current image of the player depending on how long 'd' has been pressed
            self.currentImage = self.running[int(self.runningStage // 10)]

            # sets the 'facingLeft' attribute to False
            self.facingLeft = False

            # Increases speed going right -------------------------------------
            if self.touchingBlock:
                self.speedX += self.accelerationX

            else:
                # Makes acceleration slower if the player is in the air
                self.speedX += self.accelerationX / 4

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
        if keys[pygame.K_SPACE] and self.touchingBlock:
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
        if self.speedY < 0 and not self.touchingBlock and not self.facingLeft:
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

    def draw(self) -> None:
        """ Draws the player with the 'x' and 'y' coordinates at the center

        Parameters:


        Return => None
        """

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
        # Get keys pressed
        keys = pygame.key.get_pressed()

        # If 'w' is pressed and can fire
        if keys[pygame.K_w]:
            # Play sound and append bullet to list
            self.currentWeapon.fire(self.x + 4, self.y - 4, self.facingLeft)

            return True

        return False

    def checkAnimation(self):
        """ Resets the animation stage trackers if they will cause an error

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
        playerHitbox = pygame.Rect(self.x - PLAYER_SIZE_X / 2, self.y - PLAYER_SIZE_Y / 2, PLAYER_SIZE_X, PLAYER_SIZE_Y)
        collectibleHitbox = pygame.Rect(collectibleToCheck.x - COLLECTIBLE_SIZE / 2, collectibleToCheck.y - COLLECTIBLE_SIZE / 2, COLLECTIBLE_SIZE, COLLECTIBLE_SIZE)

        # If the collectible is an instance of a Coin, increment the score and collect the collectible
        if isinstance(collectibleToCheck, Coin):
            if collectibleHitbox.colliderect(playerHitbox):
                collectibleToCheck.collect()
                collectibles.pop(collectibles.index(collectibleToCheck))
                coinsCollected += 1

        # If the collectible is an instance of a HealthPotion, increase the player's health if possible and collect the collectible
        elif isinstance(collectibleToCheck, HealthPotion):
            if collectibleHitbox.colliderect(playerHitbox):
                collectibleToCheck.collect()
                collectibles.pop(collectibles.index(collectibleToCheck))
                # If possible, increase health
                player.health += 25
                if player.health > 100:
                    player.health = 100

    def checkEnemyCollision(self, enemy) -> bool:
        """ Checks if the player has collided with an enemy

        Parameters:
            enemy: Enemy
                The enemy to check collision for


        Return => bool: whether there is a collision or not
        """
        # creating hitbox
        playerHitbox = pygame.Rect(self.x - PLAYER_SIZE_X / 2, self.y - PLAYER_SIZE_Y / 2, PLAYER_SIZE_X, PLAYER_SIZE_Y)
        # Gets the enemy hitboxes -------------------------------------------------------------------------------------
        enemyHitboxL = pygame.Rect(enemy.x - enemy.enemySizeX / 2, enemy.y - enemy.enemySizeY / 2,
                                   enemy.enemySizeX / 2, enemy.enemySizeY)
        enemyHitboxR = pygame.Rect(enemy.x, enemy.y - enemy.enemySizeY / 2, enemy.enemySizeX / 2, enemy.enemySizeY)
        enemyHitboxTop = pygame.Rect(enemy.x - enemy.enemySizeX / 2 + 15, enemy.y - enemy.enemySizeY / 2 - 5,
                                     enemy.enemySizeX - 30, 2)

        # -------------------------------------------------------------------------------------------------------------

        # Checks if the player has hit the left side of the enemy -----------------------------------------------------
        if playerHitbox.colliderect(enemyHitboxL) and not self.invincible and not enemy.isDead:
            # sets damage based on enemy type
            if isinstance(enemy, UnderworldEnemy):
                damage = 15
            elif isinstance(enemy, IceEnemy):
                damage = 20
            else:
                damage = 10

            self.takeDamage(damage)
            self.invincible = True
            self.x = enemy.x - PLAYER_SIZE_X - 5
            self.y = enemy.y - PLAYER_SIZE_Y
            # sets knockback based on enemy type
            if isinstance(enemy, UnderworldEnemy) or isinstance(enemy, IceEnemy):
                knockback = -3.5
            else:
                knockback = -3

            self.speedX = knockback
            self.speedY = -0.05
            self.touchingBlock = False
            return True

        # -------------------------------------------------------------------------------------------------------------

        # Checks if the player has hit the right side of the enemy ----------------------------------------------------
        elif playerHitbox.colliderect(enemyHitboxR) and not self.invincible and not enemy.isDead:
            # sets damage based on enemy type
            if isinstance(enemy, UnderworldEnemy):
                damage = 15
            elif isinstance(enemy, IceEnemy):
                damage = 20
            else:
                damage = 10

            self.takeDamage(damage)
            self.invincible = True
            self.x = enemy.x + (PLAYER_SIZE_X * 2) - 5
            self.y = enemy.y - PLAYER_SIZE_Y

            # sets knockback based on enemy type
            if isinstance(enemy, UnderworldEnemy) or isinstance(enemy, IceEnemy):
                knockback = 3.5
            else:
                knockback = 3

            self.speedX = knockback
            self.speedY = -0.05
            self.touchingBlock = False
            return True

        # -------------------------------------------------------------------------------------------------------------

        # Checks if the player has hit the top side of the enemy, which damages the enemy and may damage the player ---
        elif playerHitbox.colliderect(enemyHitboxTop) and not enemy.isDead:
            # chance fo damaging player
            if randint(1, 2) == 1:
                self.takeDamage(5)
            enemy.takeDamage(25)
            self.speedY = -4
            self.y -= 3
            enemy.damaged = True
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
        currentPlatformX = levelToCheck.platforms[-1].x
        onGround = False
        for platform in levelToCheck.platforms:
            if platform.x + platform.length + PLAYER_SIZE_X / 2 > self.x > platform.x - PLAYER_SIZE_X / 2 and platform.y + 10 > self.y + PLAYER_SIZE_Y / 2 > platform.y:
                self.y = platform.y - PLAYER_SIZE_Y / 2
                self.speedY = 0
                onGround = True
                currentPlatformX = platform.x

                # If the player is on the ground and on a moving platform, it moves with the platform
                if onGround and isinstance(platform, VerticalMovingPlatform):
                    if platform.moveDown:
                        self.y += 0.5
                    else:
                        self.y -= 0.5

                if onGround and isinstance(platform, HorizontalMovingPlatform):
                    if platform.moveRight:
                        self.x += 1
                    else:
                        self.x -= 1

            # Side collisions
            if platform.y - PLAYER_SIZE_Y / 2 < self.y < platform.y + platform.width and (platform.x - PLAYER_SIZE_X / 2 <= self.x < platform.x or platform.x + platform.length + PLAYER_SIZE_X / 2 <= self.x < platform.x + platform.length):
                self.speedX = 0

        self.touchingBlock = onGround

        if currentPlatformX >= 150:
            moveBackground(1)

    def checkChestCollision(self, chestToCheck):
        """ Checks if any player has collided with any chests

        Parameters:
            chestToCheck: chest to check for collision

        Return => None
        """
        keys = pygame.key.get_pressed()
        colour = BLACK if level.background is iceBackgroundImage else WHITE
        playerHitbox = pygame.Rect(self.x - PLAYER_SIZE_X / 2, self.y - PLAYER_SIZE_Y / 2,
                                   PLAYER_SIZE_X,
                                   PLAYER_SIZE_Y)
        if chestToCheck.hitbox.colliderect(playerHitbox):
            chestToCheck.opening = True
            weaponName = scoreFontSmall.render(chestToCheck.weapon.name, True, colour)
            if levelNumber == 0 and not chestToCheck.collected:
                pressX = scoreFontSmall.render("[x]", True, colour)
                gameWindow.blit(pressX,
                                ((chestToCheck.platform.x + chestToCheck.platform.length / 2 - 20), chestToCheck.platform.y + 16))

            if not chestToCheck.collected:
                if isinstance(chestToCheck.weapon, Pistol):
                    gameWindow.blit(weaponName,
                                    ((chestToCheck.platform.x + chestToCheck.platform.length / 2) - 35, chestToCheck.platform.y - 43))

                elif isinstance(chestToCheck.weapon, AssaultRifle):
                    gameWindow.blit(weaponName,
                                    ((chestToCheck.platform.x + chestToCheck.platform.length / 2) - 90, chestToCheck.platform.y - 43))

                elif isinstance(chestToCheck.weapon, MachineGun):
                    gameWindow.blit(weaponName,
                                    ((chestToCheck.platform.x + chestToCheck.platform.length / 2) - 80, chestToCheck.platform.y - 43))

                elif isinstance(chestToCheck.weapon, SniperRifle):
                    gameWindow.blit(weaponName,
                                    ((chestToCheck.platform.x + chestToCheck.platform.length / 2) - 80, chestToCheck.platform.y - 43))

                elif isinstance(chestToCheck.weapon, Shotgun):
                    gameWindow.blit(weaponName,
                                    ((chestToCheck.platform.x + chestToCheck.platform.length / 2) - 55, chestToCheck.platform.y - 43))

                elif isinstance(chestToCheck.weapon, GrenadeLauncher):
                    gameWindow.blit(weaponName,
                                    ((chestToCheck.platform.x + chestToCheck.platform.length / 2) - 120, chestToCheck.platform.y - 43))

                elif isinstance(chestToCheck.weapon, LaserPistol):
                    gameWindow.blit(weaponName,
                                    ((chestToCheck.platform.x + chestToCheck.platform.length / 2) - 85, chestToCheck.platform.y - 43))

                elif isinstance(chestToCheck.weapon, LaserAssaultRifle):
                    gameWindow.blit(weaponName,
                                    ((chestToCheck.platform.x + chestToCheck.platform.length / 2) - 140, chestToCheck.platform.y - 43))

                elif isinstance(chestToCheck.weapon, LaserMachineGun):
                    gameWindow.blit(weaponName,
                                    ((chestToCheck.platform.x + chestToCheck.platform.length / 2) - 120, chestToCheck.platform.y - 43))

                elif isinstance(chestToCheck.weapon, LaserSniperRifle):
                    gameWindow.blit(weaponName,
                                    ((chestToCheck.platform.x + chestToCheck.platform.length / 2) - 130, chestToCheck.platform.y - 43))

                elif isinstance(chestToCheck.weapon, LaserShotgun):
                    gameWindow.blit(weaponName,
                                    ((chestToCheck.platform.x + chestToCheck.platform.length / 2) - 100, chestToCheck.platform.y - 43))

            if keys[pygame.K_x]:
                player.currentWeapon = chestToCheck.weapon
                if not chestToCheck.collected:
                    pickupWeapon.play()
                chestToCheck.collected = True

        if chestToCheck.opening:
            chestToCheck.open()


class Platform(object):
    """ An object representing a platform

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

    """

    def __init__(self, x: float, y: float, length: int, image: pygame.Surface = grassTile, width: int = 20) -> None:
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.image = image
        if self.image is grassTile:
            self.imageL = pygame.image.load("images/tiles/grassTile/tileL.png")
            self.imageR = pygame.image.load("images/tiles/grassTile/tileR.png")
        else:
            self.imageL = self.image
            self.imageR = self.image

    def draw(self) -> None:
        """ Draws the platform, with square tiles

        Parameters:


        Return => None
        """
        for x in range(int(self.x), int(self.x + self.length), 20):
            if x == int(self.x):
                gameWindow.blit(self.imageL, (x, self.y))

            # this means that this is the last block
            elif x + 20 >= int(self.x + self.length):
                gameWindow.blit(self.imageR, (x, self.y))

            else:
                gameWindow.blit(self.image, (x, self.y))


class VerticalMovingPlatform(Platform):
    """ An object representing a platform

    Attributes:
        x: float
            The x position of the top left corner of the platform

        y: float
            The y position of the top left corner of the platform

        length: int
            The length of the platform

        rangeOfMovement:
            The vertical range of the movement of the platform

        image: pygame.Surface
            The image of the tile

    """

    def __init__(self, x, y, length, rangeOfMovement, image=pygame.image.load("images/tiles/grassTile/tile.png")) -> None:
        self.upperBound = y - rangeOfMovement
        self.lowerBound = y + rangeOfMovement
        self.moveDown = True
        super().__init__(x, y, length, image)

    def draw(self) -> None:
        """ Draws the platform, with square tiles

        Parameters:


        Return => None
        """

        # draws the line of movement
        pygame.draw.line(gameWindow, GREY, (self.x + self.length / 2, self.upperBound), (self.x + self.length / 2, self.lowerBound), 2)

        # drawing the platform at the correct location
        for xCoord in range(int(self.x), int(self.x + self.length), 20):
            if xCoord == int(self.x):
                gameWindow.blit(self.imageL, (xCoord, self.y))
            elif xCoord == int(self.x + self.length) - 20:
                gameWindow.blit(self.imageR, (xCoord, self.y))
            else:
                gameWindow.blit(self.image, (xCoord, self.y))

        # Moving the platform
        if self.moveDown:
            self.y += 0.5
        else:
            self.y -= 0.5

        # flips the movement direction when it hits the edge
        if self.y <= self.upperBound:
            self.moveDown = True
        if self.y >= self.lowerBound:
            self.moveDown = False


class HorizontalMovingPlatform(Platform):
    """ An object representing a platform

    Attributes:
        x: float
            The x position of the top left corner of the platform

        y: float
            The y position of the top left corner of the platform

        length: int
            The length of the platform

        rangeOfMovement:
            The vertical range of the movement of the platform

        image: pygame.Surface
            The image of the tile

    """

    def __init__(self, x, y, length, rangeOfMovement, image=pygame.image.load("images/tiles/grassTile/tile.png")) -> None:
        self.originalX = x
        self.upperBound = x - rangeOfMovement
        self.lowerBound = x + rangeOfMovement
        self.rangeOfMovement = rangeOfMovement
        self.moveRight = True
        super().__init__(x, y, length, image)

    def draw(self) -> None:
        """ Draws the platform, with square tiles

        Parameters:


        Return => None
        """
        # draws the line of movement
        pygame.draw.line(gameWindow, BLACK, (self.upperBound, self.y + self.width/2), (self.lowerBound + self.length, self.y + self.width/2), 2)

        # drawing the platform at the correct location
        for xCoord in range(int(self.x), int(self.x + self.length), 20):
            if xCoord == int(self.x):
                gameWindow.blit(self.imageL, (xCoord, self.y))
            elif xCoord == int(self.x + self.length) - 20:
                gameWindow.blit(self.imageR, (xCoord, self.y))
            else:
                gameWindow.blit(self.image, (xCoord, self.y))

        # Moving the platform
        if self.moveRight:
            self.x += 0.5
        else:
            self.x -= 0.5

        # flips the movement direction when it hits the edge
        if self.x <= self.upperBound:
            self.moveRight = True
        if self.x >= self.lowerBound:
            self.moveRight = False



class Enemy(object):
    """ The base class for the enemy, as well as the underworld enemy, as their
        behaviours are very similar

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

        moving, hurt, dead: list[pygame.Surface]
            List of images for when the enemy is moving, hurt or dead. Changes if 'underworldEnemy' is True

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

        # Animation Images
        self.moving = [
            pygame.image.load("images/enemy/normal/moving/running/running1.png"),
            pygame.image.load("images/enemy/normal/moving/running/running2.png"),
            pygame.image.load("images/enemy/normal/moving/running/running3.png"),
        ]

        self.hurt = [
            pygame.image.load("images/enemy/normal/moving/hurt/hurt1.png"),
        ]

        self.dead = [
            pygame.image.load("images/enemy/normal/dead/explosion1.png"),
            pygame.image.load("images/enemy/normal/dead/explosion2.png"),
            pygame.image.load("images/enemy/normal/dead/explosion3.png"),
            pygame.image.load("images/enemy/normal/dead/explosion4.png"),
            pygame.image.load("images/enemy/normal/dead/explosion5.png"),
            pygame.image.load("images/enemy/normal/dead/explosion6.png"),
            pygame.image.load("images/enemy/normal/dead/explosion7.png"),
            pygame.image.load("images/enemy/normal/dead/explosion8.png"),
            pygame.image.load("images/enemy/normal/dead/explosion9.png"),
            pygame.image.load("images/enemy/normal/dead/explosion10.png"),
        ]

        # Hitbox
        self.hitbox = pygame.Rect(self.x - self.enemySizeX / 2, self.y - self.enemySizeY / 2, self.enemySizeX, self.enemySizeY)

        # The current image
        self.currentImage = self.moving[0]

        # Keeps track of the animation stages
        self.movingStage = 0
        self.deadStage = 0

        # the current time when it takes damage. used for an invincibility delay
        self.damageTime = 0

    def draw(self) -> None:
        """ Draws the enemy at the correct x and y location

        Parameters:


        Return => None
        """
        # if the enemy is hurt, but not dead, draw the enemy hurt image
        if self.damaged and self.health > 0:
            # flip the image if the enemy is facing left
            if self.moveLeft:
                gameWindow.blit(pygame.transform.flip(self.hurt[0], True, False),
                                (self.x - self.enemySizeX / 2, self.y - self.enemySizeY / 2))

            else:
                gameWindow.blit(self.hurt[0], (self.x - self.enemySizeX / 2, self.y - self.enemySizeY / 2))

        else:
            # otherwise, blit the normal image
            gameWindow.blit(self.currentImage, (self.x - self.enemySizeX / 2, self.y - self.enemySizeY / 2))

        # draws the health bar if not dead ----------------------------------------------------------------------------
        if not self.isDead:
            # draw the border
            pygame.draw.rect(gameWindow, GREY, (int(self.x - self.enemySizeX / 2 - 2), int(self.y - self.enemySizeX / 2 - 7), self.enemySizeX + 4, 9), 2, 1)

            # draws the health
            for j in range(self.health // 5):
                pygame.draw.rect(gameWindow, RED, (int(self.x - self.enemySizeX / 2 + (j * self.enemySizeX // 23)), int(self.y - self.enemySizeX / 2 - 5), self.enemySizeX // 5, 5))

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

            if self.x > self.platform.x + self.platform.length - self.enemySizeX / 4:
                self.moveLeft = True

            # increment animation
            self.movingStage += 1

        # -------------------------------------------------------------------------------------------------------------



        # The enemy is dead -------------------------------------------------------------------------------------------
        else:
            # generate collectible and spawn it at the enemy's x and y coordinate
            if self.deadStage == 0:
                collectibleType = randint(1, 16)
                # if 'collectibleType' is between 1 - 4, spawn a health potion
                if 1 <= collectibleType <= 4:
                    collectibles.append(HealthPotion(self.x, self.y))

                else:
                    collectibles.append(Coin(self.x, self.y))

            # draw the explosion images, flipping if necessary
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
                self.y += 0.5

            else:
                self.y -= 0.5

        # -------------------------------------------------------------------------------------------------------------



        # if the platform is a horizontal moving platform -------------------------------------------------------------
        if isinstance(self.platform, HorizontalMovingPlatform):
            # change the y depending on the platform
            if self.platform.moveRight:
                self.x += 0.5
            else:
                self.x -= 0.5
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
            self.health -= damage


class UnderworldEnemy(Enemy):
    """ Class representing an 'Underworld Enemy'

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

        moving, hurt, dead: list[pygame.Surface]
            List of images for when the enemy is moving, hurt or dead. Changes if 'underworldEnemy' is True

    """

    def __init__(self, platform: Platform, speed: float, health: int = 100) -> None:
        super().__init__(platform, speed, health)
        self.enemySizeX = UNDERWORLD_ENEMY_SIZE_X
        self.enemySizeY = UNDERWORLD_ENEMY_SIZE_Y
        self.moving = [
            pygame.image.load("images/enemy/underworld/moving/running/running1.png"),
            pygame.image.load("images/enemy/underworld/moving/running/running2.png"),
            pygame.image.load("images/enemy/underworld/moving/running/running3.png"),
            pygame.image.load("images/enemy/underworld/moving/running/running4.png"),
            pygame.image.load("images/enemy/underworld/moving/running/running5.png"),
            pygame.image.load("images/enemy/underworld/moving/running/running6.png"),
        ]

        self.hurt = [
            pygame.image.load("images/enemy/underworld/moving/hurt/hurt1.png"),
        ]

        # Explosion animations are the same, but scaled up
        self.dead = [
            pygame.image.load("images/enemy/underworld/dead/explosion1.png"),
            pygame.image.load("images/enemy/underworld/dead/explosion2.png"),
            pygame.image.load("images/enemy/underworld/dead/explosion3.png"),
            pygame.image.load("images/enemy/underworld/dead/explosion4.png"),
            pygame.image.load("images/enemy/underworld/dead/explosion5.png"),
            pygame.image.load("images/enemy/underworld/dead/explosion6.png"),
            pygame.image.load("images/enemy/underworld/dead/explosion7.png"),
            pygame.image.load("images/enemy/underworld/dead/explosion8.png"),
            pygame.image.load("images/enemy/underworld/dead/explosion9.png"),
            pygame.image.load("images/enemy/underworld/dead/explosion10.png"),
        ]

        self.x = platform.x + platform.length / 2
        self.y = platform.y - ENEMY_SIZE_Y / 2
        self.moveLeft = True
        self.damaged = False
        self.isDead = False

    def takeDamage(self, damage: int) -> None:
        """ Delegates call to super class method

        Parameters:
            damage: int -> the damage to be taken


        Return => None
        """
        super().takeDamage(int(damage // 2))


class IceEnemy(Enemy):
    """ Class representing an 'Ice Enemy'

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

        moving, hurt, dead: list[pygame.Surface]
            List of images for when the enemy is moving, hurt or dead. Changes if 'underworldEnemy' is True

    """

    def __init__(self, platform: Platform, speed: float, health: int = 100) -> None:
        super().__init__(platform, speed, health)
        self.enemySizeX = ICE_ENEMY_SIZE_X
        self.enemySizeY = ICE_ENEMY_SIZE_Y
        self.moving = [
            pygame.image.load(f"images/enemy/ice/moving/running/running{j}.png") for j in range(1, 7)
        ]
        self.hurt = [
            pygame.image.load(f"images/enemy/ice/moving/running/running{j}.png") for j in range(1, 2)
        ]
        self.dead = [
            pygame.image.load(f"images/enemy/ice/dead/explosion{j}.png") for j in range(1, 11)
        ]

        self.x = platform.x + platform.length / 2
        self.y = platform.y - ENEMY_SIZE_Y / 2
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
                collectibleType = randint(1, 16)
                # if 'collectibleType' is between 1 - 4, spawn a health potion
                if 1 <= collectibleType <= 4:
                    collectibles.append(HealthPotion(self.x, self.y))

                else:
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
                self.y += 0.5
            else:
                self.y -= 0.5
        # -------------------------------------------------------------------------------------------------------------

        # if the platform is a horizontal moving platform -------------------------------------------------------------
        if isinstance(self.platform, HorizontalMovingPlatform):
            # change the y depending on the platform
            if self.platform.moveRight:
                self.x += 0.5
            else:
                self.x -= 0.5
        # -------------------------------------------------------------------------------------------------------------



        # Rebuilds the hitbox -------------------------------------------------
        self.hitbox = pygame.Rect(self.x - self.enemySizeX / 2, self.y - self.enemySizeY / 2, self.enemySizeX, self.enemySizeY)

    def takeDamage(self, damage: int) -> None:
        """ Delegates call to super class method

        Parameters:
            damage: int -> the damage to be taken


        Return => None
        """
        super().takeDamage(int(damage // 3))


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

        timeSinceFire:
            The time of the shot being fired. Used for the fire rate of the weapon

    """

    def __init__(self, fireRate: float, damage: int) -> None:
        self.fireRate = fireRate
        self.damage = damage
        self.name = "Gun"
        self.icon = pygame.image.load("images/weaponIcons/default/pistol.png")
        self.timeSinceFire = 0


class Pistol(Gun):
    """ Default weapon for the player

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

    def __init__(self, fireRate: float, damage: int) -> None:
        super().__init__(fireRate, damage)
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
        # if canFire and the time since the previous shot is larger than the 'foreRate' attribute
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate:
            # plays sound
            bulletFired.play()

            # appends bullet to list
            bullets.append(Bullet(x + 4, y + 5, 5, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed


class AssaultRifle(Gun):
    """ Base weapon for the assault rifle

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

    def __init__(self, fireRate: float, damage: int) -> None:
        super().__init__(fireRate, damage)
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
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate:
            # plays sound
            bulletFired.play()

            # appends bullet to list
            bullets.append(Bullet(x + 4, y + 5, 8, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed


class MachineGun(Gun):
    """ Base weapon for the machine gun

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

    def __init__(self, fireRate: float, damage: int) -> None:
        super().__init__(fireRate, damage)
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
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate:
            # changes volume as machine gun fire rate might lead to the sound being too loud
            bulletFired.set_volume(0.75)

            # plays sound
            bulletFired.play()
            bulletFired.set_volume(1)

            # appends bullet to list
            bullets.append(Bullet(x + 4, y + 5, 8, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed


class Shotgun(Gun):
    """ Base weapon for the shotgun

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

    def __init__(self, fireRate: float, damage: int) -> None:
        super().__init__(fireRate, damage)
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
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate:
            # plays sound
            shotgunFired.play()

            # appends bullet to list
            bullets.append(ShotgunBullet(x + 12, y + 5, 0, facingLeft, self.damage))

            # plays sound
            self.timeSinceFire = timeElapsed


class SniperRifle(Gun):
    """ Base weapon for the Sniper

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

    def __init__(self, fireRate: float, damage: int) -> None:
        super().__init__(fireRate, damage)
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
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate:
            # plays sound
            bulletFired.play()

            # appends bullet to list
            bullets.append(Bullet(x + 12, y + 5, 12, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed


class GrenadeLauncher(Gun):
    """ Base weapon for the Grenade Launcher

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

    def __init__(self, fireRate: float, damage: int) -> None:
        super().__init__(fireRate, damage)
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
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate:
            # plays sound
            bulletFired.play()

            # appends bullet to list
            grenades.append(Grenade(x + 4, y - 8, 4, -8, 0.25, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed


class LaserPistol(Gun):
    """ Class representing the Laser Pistol

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
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate:
            # plays sound
            laserFired.play()

            # appends bullet to list
            bullets.append(LaserBullet(x + 4, y + 5, 7, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed


class LaserAssaultRifle(Gun):
    """ Class representing the laser assault rifle

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
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate:
            # plays sound
            laserFired.play()

            # appends bullet to list
            bullets.append(LaserBullet(x + 4, y + 5, 8, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed


class LaserMachineGun(Gun):
    """ Class representing laser the machine gun

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
        super().__init__(0.15, 20)
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
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate:
            # plays sound
            laserFired.play()

            # appends bullet to list
            bullets.append(LaserBullet(x + 4, y + 5, 8, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed


class LaserShotgun(Gun):
    """ Class representing the laser shotgun

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
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate:
            # plays sound
            laserFired.play()

            # appends bullet to list
            bullets.append(LaserShotgunBullet(x + 12, y + 5, 0, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed


class LaserSniperRifle(Gun):
    """ Class representing the laser sniper rifle

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
        if self.canFire and timeElapsed - self.timeSinceFire > self.fireRate:
            # plays sound
            sniperLaserFired.play()

            # appends bullet to list
            bullets.append(LaserBullet(x + 12, y + 5, 12, facingLeft, self.damage))

            # records time of shot
            self.timeSinceFire = timeElapsed


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
    """ A class representing a bullet

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
            Also rebuild the hitbox of the bullet

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
    """ A class representing a shotgun bullet

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
            pygame.image.load("images/character/shotgun/shotgunMuzzle1.png"),
            pygame.image.load("images/character/shotgun/shotgunMuzzle2.png"),
            pygame.image.load("images/character/shotgun/shotgunMuzzle3.png"),
            pygame.image.load("images/character/shotgun/shotgunMuzzle4.png"),
            pygame.image.load("images/character/shotgun/shotgunMuzzle5.png"),
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


class LaserBullet(Projectile):
    """ A class representing a laser bullet

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
            pygame.image.load("images/character/laser/shotgun/shotgunMuzzle1.png"),
            pygame.image.load("images/character/laser/shotgun/shotgunMuzzle2.png"),
            pygame.image.load("images/character/laser/shotgun/shotgunMuzzle3.png"),
            pygame.image.load("images/character/laser/shotgun/shotgunMuzzle4.png"),
            pygame.image.load("images/character/laser/shotgun/shotgunMuzzle5.png"),
        ]
        self.muzzleFlashStage = 0
        self.currentImage = self.muzzleFlash[0]
        self.hitbox = pygame.Rect((self.x, self.y - 10, 50, 50))

    def draw(self) -> None:
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


class Icicle(Projectile):
    """ A class representing a laser bullet

    Attributes:
        x: float
            The x position of the projectile

        y: float
            The y position of the projectile

        speedX: float
            The speed of the projectile in the x direction

        hitbox: pygame.Surface
            The hitbox of the icicle

        image: pygame.Surface
            The image of the icicle

        damage: int
            The damage caused upon collision of a projectile
    """

    def __init__(self, x, y, speedX) -> None:
        # always going left
        super().__init__(x, y, speedX, True, 10)
        self.hitbox = pygame.Rect(self.x, self.y, 16, 10)
        self.image = pygame.image.load("images/enemy/ice/weapon/icicle1.png")

    def move(self):
        # moves the bullet left or right depending on the 'movingLeft' boolean
        if self.movingLeft:
            self.x -= self.speedX

        else:
            self.x += self.speedX

        # Rebuilds hit box
        self.hitbox = pygame.Rect(self.x, self.y, 13, 8)

    def draw(self):
        # draws the bullet left or right depending on the 'movingLeft' boolean
        if self.movingLeft:
            gameWindow.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))

        else:
            gameWindow.blit(self.image, (self.x, self.y))


class Grenade(Projectile):
    """ A class representing a grenade

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
            pygame.image.load("images/character/grenade/explosion/explosion1.png"),
            pygame.image.load("images/character/grenade/explosion/explosion2.png"),
            pygame.image.load("images/character/grenade/explosion/explosion3.png"),
            pygame.image.load("images/character/grenade/explosion/explosion4.png"),
            pygame.image.load("images/character/grenade/explosion/explosion5.png"),
            pygame.image.load("images/character/grenade/explosion/explosion6.png"),
            pygame.image.load("images/character/grenade/explosion/explosion7.png"),
            pygame.image.load("images/character/grenade/explosion/explosion8.png"),
        ]
        self.explosionAnimationStage = 0
        self.currentImage = self.image
        self.exploded = False
        self.playSound = False

    def move(self) -> None:

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
        # draws the grenade left or right depending on the 'movingLeft' boolean
        if self.exploded:
            gameWindow.blit(self.currentImage, (self.x, self.y - 50))

        else:
            gameWindow.blit(self.currentImage, (self.x, self.y))


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

    """

    def __init__(self, x, y) -> None:
        self.coinImages = [
            pygame.image.load("images/coin/coinStage1.png"),
            pygame.image.load("images/coin/coinStage2.png"),
            pygame.image.load("images/coin/coinStage3.png"),
            pygame.image.load("images/coin/coinStage4.png"),
        ]
        self.animationStage = 0
        super().__init__(x, y)
        for platform in level.platforms:
            if platform.x < self.x < platform.x + platform.length:
                self.offset = self.x - platform.x

    def draw(self) -> None:
        # resets the animation stage if the index will cause an error ---------
        if self.animationStage >= (len(self.coinImages) * 10) - 1:
            self.animationStage = 0

        # Resets the y position - for moving platforms ------------------------
        for platform in level.platforms:
            if platform.x < self.x < platform.x + platform.length:
                self.y = platform.y - 10
                self.x = platform.x + self.offset


        # blits the image to the screen ---------------------------------------
        gameWindow.blit(self.coinImages[int(self.animationStage // 10)], (self.x - COLLECTIBLE_SIZE / 2, self.y - COLLECTIBLE_SIZE / 2))

        # increments animation stage ------------------------------------------
        self.animationStage += 1

    def collect(self) -> None:
        # plays the 'coinCollected' sound
        coinCollected.play()
        self.collected = True


class HealthPotion(Collectible):
    """ A class representing a health potion, inheriting from a collectible

    Attributes:
        x: float
            The x position of the collectible

        y: float
            The y position of the collectible

        potionImages: list[pygame.Surface]
            The images for the animated potion

        animationStage: int
            The current image's index number

        collected: bool
            If the collectible is collected or not

    """

    def __init__(self, x, y) -> None:
        self.potionImages = [
            pygame.image.load("images/potion/potion1.png"),
            pygame.image.load("images/potion/potion2.png"),
            pygame.image.load("images/potion/potion3.png"),
            pygame.image.load("images/potion/potion4.png"),
            pygame.image.load("images/potion/potion5.png"),
            pygame.image.load("images/potion/potion6.png"),
            pygame.image.load("images/potion/potion7.png"),
            pygame.image.load("images/potion/potion8.png"),
        ]
        self.animationStage = 0
        super().__init__(x, y)

    def draw(self):
        # resets the animation stage if the index will cause an error ---------
        if self.animationStage >= (len(self.potionImages) * 10) - 1:
            self.animationStage = 0

        # Resets the y position - for moving platforms ------------------------
        for platform in level.platforms:
            if platform.x < self.x < platform.x + platform.length:
                self.y = platform.y - 10

        # blits the image to the screen ---------------------------------------
        gameWindow.blit(self.potionImages[int(self.animationStage // 10)], (self.x - COLLECTIBLE_SIZE / 2, self.y - COLLECTIBLE_SIZE / 2))

        # increments animation stage ------------------------------------------
        self.animationStage += 1

    def collect(self):
        # plays the 'potionCollected' sound
        potionCollected.play()
        self.collected = True


class Chest(object):
    """ A class representing a chest, which holds a weapon

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
        self.platform = platform
        self.images = [
            pygame.image.load("images/chest/chest1.png"),
            pygame.image.load("images/chest/chest2.png"),
            pygame.image.load("images/chest/chest3.png"),
            pygame.image.load("images/chest/chest4.png"),
            pygame.image.load("images/chest/chest5.png"),
            pygame.image.load("images/chest/chest6.png"),
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

    def open(self):
        """ Sets the current image and increments 'Animation Stage'

        Parameters:


        Return => None
        """
        # sets current image
        self.currentImage = self.images[int(self.animationStage // 8)]

        # increments 'animationStage' if possible
        if self.animationStage <= len(self.images) * 8 - 2:
            self.animationStage += 1


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
            pygame.image.load("images/portal/portal1.png"),
            pygame.image.load("images/portal/portal2.png"),
            pygame.image.load("images/portal/portal3.png"),
            pygame.image.load("images/portal/portal4.png"),
            pygame.image.load("images/portal/portal5.png"),
            pygame.image.load("images/portal/portal6.png"),
            pygame.image.load("images/portal/portal7.png"),
            pygame.image.load("images/portal/portal8.png"),
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


class Level(object):
    """ An object representing an in-game level

    Attributes:
        platforms: list[Platforms]
            The lists of platforms for the level. The list is constantly updated

        maxPlatforms: int
            The maximum number of platforms in the level. The last platform has a portal to the next level

    """

    def __init__(self, maxPlatforms: int, background: pygame.Surface = backgroundImage) -> None:
        if background is underworldBackgroundImage:
            self.startPlatform = Platform(100, HEIGHT // 2 - 100, 100, underworldTile)

        elif background is iceBackgroundImage:
            self.startPlatform = Platform(100, HEIGHT // 2 - 100, 100, iceTile)

        else:
            self.startPlatform = Platform(100, HEIGHT//2 - 100, 100)

        self.platforms = [self.startPlatform]
        self.maxPlatforms = maxPlatforms
        self.numOfPlatforms = 0
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

                # increments 'numOfPlatforms' ---------------------------------
                self.numOfPlatforms += 1

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
        # generates platform depending on the level background
        if self.background is underworldBackgroundImage:
            image = underworldTile

        elif self.background is iceBackgroundImage:
            image = iceTile

        else:
            image = grassTile

        # if there is no new platform, generate one -------------------------------------------------------------------
        if self.platforms[-1].x <= WIDTH - 60 and self.numOfPlatforms < self.maxPlatforms:
            # chance of a moving platform
            movingPlatformChance = randint(1, 4)

            # if the platform is higher or lower than the current one ---------
            higherOrLower = randint(0, 1)

            # force the platform to be lower if current platform is too high --
            if self.platforms[-1].y <= 200:
                higherOrLower = 1

            # force the platform to be high if current platform is too low ----
            elif self.platforms[-1].y >= HEIGHT - 200:
                higherOrLower = 0

            # if 'higherOrLower' is 1, make the platform lower than the current one -----------------------
            if higherOrLower == 1:

                # if 'movingPlatformChance' is 1, make a moving Platform ----------------------
                if movingPlatformChance == 1 and not isinstance(self.platforms[-1], HorizontalMovingPlatform):
                    self.platforms.append(
                        VerticalMovingPlatform(self.platforms[-1].x + self.platforms[-1].length + (randint(3, 6) * 20),
                                               self.platforms[-1].y + (randint(2, 4) * 20), (randint(7, 10) * 20),
                                               (randint(3, 6) * 10), image)
                    )

                elif movingPlatformChance == 2 and not (isinstance(self.platforms[-1], VerticalMovingPlatform) or isinstance(self.platforms[-1], HorizontalMovingPlatform)):
                    self.platforms.append(
                        HorizontalMovingPlatform(self.platforms[-1].x + self.platforms[-1].length + (randint(8, 10) * 20),
                                                 self.platforms[-1].y + (randint(2, 4) * 20), (randint(7, 10) * 20),
                                                 (randint(4, 7) * 10), image)
                    )
                # else make a normal platform -------------------------------------------------
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
                                               (randint(3, 6) * 10), image)
                    )

                elif movingPlatformChance == 2 and not (isinstance(self.platforms[-1], VerticalMovingPlatform) or isinstance(self.platforms[-1], HorizontalMovingPlatform)):
                    self.platforms.append(
                        HorizontalMovingPlatform(self.platforms[-1].x + self.platforms[-1].length + (randint(9, 10) * 20),
                                                 self.platforms[-1].y + (randint(2, 4) * 20), (randint(7, 10) * 20),
                                                 (randint(4, 7) * 10), image)
                    )
                # else make a normal platform -------------------------------------------------
                else:
                    self.platforms.append(
                        Platform(self.platforms[-1].x + self.platforms[-1].length + (randint(3, 7) * 20),
                                 self.platforms[-1].y - (randint(2, 3) * 20), (randint(7, 10) * 20), image)
                    )

            # the chance that an enemy spawns on the platform ---------------------------------------------
            chanceOfEnemy = randint(1, 4)

            # if the last platform is not the spawn platform and 'chanceOfEnemy' is 1 ---------
            if chanceOfEnemy == 1 and self.platforms[-1] is not self.startPlatform:
                # number of enemies and speed of each enemy
                numberOfEnemies = randint(1, 2)
                speed = uniform(0.3, 0.5)

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
                if enemy.platform is spawnPlatform:
                    if enemy in enemies:
                        enemies.remove(enemy)

            # chance of a chest to spawn ------------------------------------------------------------------
            chanceOfChest = randint(1, 5)

            # if levelNumber == 0(tutorial level), make every possible chest spawn ------------------------
            if levelNumber == 0:
                chanceOfChest = 1

            if chanceOfChest == 1 and chanceOfEnemy != 1:
                # Weapon generation
                weapon = generateWeapon()

                # Append the new chest
                chests.append(
                    Chest(self.platforms[-1], weapon)
                )

        # -------------------------------------------------------------------------------------------------------------



        # Append new platform with the 'next level' portal ------------------------------------------------------------
        if self.numOfPlatforms == self.maxPlatforms:
            self.platforms.append(
                Platform(self.platforms[-1].x + self.platforms[-1].length + 60,
                         self.platforms[-1].y, 180, image)
            )

            # appends portal to list
            portals.append(Portal(self.platforms[-1]))

            self.numOfPlatforms += 1

        # -------------------------------------------------------------------------------------------------------------

    def redrawPlatforms(self, playerToCheck: Player) -> None:
        """ Responsible for drawing and moving the player, as well has the weapon cooldown

        Parameters:
            playerToCheck: Player
                The player whose weapon damages the enemy

            self: Level
                The level whose platforms are

        Return => None
        """
        self.generatePlatforms()
        self.deletePlatforms()
        playerToCheck.checkPlatformCollision(self)
        self.drawPlatforms()


## Move background ##
def moveBackground(rate: float) -> None:
    """ Moves the background to give the illusion of the player moving forward

    Parameters:
        rate: float -> the rate of which the backgrounds moves


    Return => None
    """
    # moves player
    player.x -= rate

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


## Enemy-related functions ##
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


## Bullet-related functions ##
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


## Grenade-related functions ##
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


## Chest-related functions ##
def drawChests() -> None:
    """ Draws chests

    Parameters:


    Return => None
    """
    for chest in chests:
        chest.draw()


## Collectible-related functions ##
def drawCollectibles() -> None:
    """ Draws collectibles

    Parameters:


    Return => None
    """
    for collectible in collectibles:
        collectible.draw()


## Portal-related functions ##
def drawPortals() -> None:
    """ Draws portals

    Parameters:


    Return => None
    """
    for portal in portals:
        portal.draw()


## Level generation ##
def generateLevel(playerToCheck: Player) -> Level:
    """ Generates a new level

    Parameters:
        playerToCheck: Player
            The player that is checked by this function

    Return => Level: The newly generated level
    """

    global levelNumber, levelTransition
    # gets all keys
    keys = pygame.key.get_pressed()

    # generates player hitbox
    playerHitbox = pygame.Rect(playerToCheck.x - PLAYER_SIZE_X / 2, playerToCheck.y - PLAYER_SIZE_Y / 2, PLAYER_SIZE_X, PLAYER_SIZE_Y)

    # the colour changes depending on background of the level
    colour = BLACK if level.background is iceBackgroundImage else WHITE

    for portal in portals:

        # display text if portal and player hitbox collide
        if portal.hitbox.colliderect(playerHitbox):

            # renders text
            portalText = scoreFontSmall.render("[x] Next Level?", True, colour)

            # blits text
            gameWindow.blit(portalText, (portal.platform.x + portal.platform.length / 2 - 96, portal.platform.y - 118))

            # starts the transition to underworld level ---------------------------------------------------------------
            if keys[pygame.K_x] and levelNumber == 5:
                levelTransition = True

            # resets level - clears lists, resets positions, etc ------------------------------------------------------
            if keys[pygame.K_x] and not levelTransition:
                portalEnter.play()
                chests.clear()
                portals.clear()
                enemies.clear()
                grenades.clear()
                bullets.clear()
                collectibles.clear()

                # resets player location
                player.x = 150
                player.y = 200 - PLAYER_SIZE_X

                # increments level number
                levelNumber += 1
                levelTransition = False

                # reset player health and weapon after they finish the tutorial ---------------
                if levelNumber == 1:
                    playerToCheck.currentWeapon = Pistol(PISTOL_FIRE_RATE, PISTOL_DAMAGE)
                    playerToCheck.health = 100

                levelBackgroundImage = backgroundImage

                # acceleration
                player.accelerationX = 0.25

                # resets speed
                playerToCheck.speedY = 1

                # sets background based on level number
                if 6 <= levelNumber <= 10:
                    levelBackgroundImage = underworldBackgroundImage
                    # return Level(round(level.maxPlatforms + (int(level.maxPlatforms // 2))), underworldBackgroundImage)

                if 11 <= levelNumber <= 15:
                    # acceleration as the level has 'ice'
                    player.accelerationX = 0.15
                    levelBackgroundImage = iceBackgroundImage

                platformNum = round(level.maxPlatforms * 1.25)
                if platformNum > MAX_PLATFORMS:
                    platformNum = MAX_PLATFORMS

                return Level(platformNum, levelBackgroundImage)

            # ---------------------------------------------------------------------------------------------------------



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
            chests.clear()
            portals.clear()
            enemies.clear()
            grenades.clear()
            bullets.clear()
            collectibles.clear()

            # resets speed
            playerToCheck.speedY = 1

            # reset player location
            player.x = 150
            player.y = 5

            # increments 'levelNumber'
            levelNumber += 1

            platformNum = round(level.maxPlatforms * 1.25)
            if platformNum > MAX_PLATFORMS:
                platformNum = MAX_PLATFORMS

            return Level(platformNum, underworldBackgroundImage)

    return level


## Weapon generation ##
def generateWeapon() -> Gun:
    """ Generates a weapon using the randint() function.

    Parameters:


    Return => Gun: returns the randomly generated gun
    """
    weapon = Gun(0, 0)
    weaponGenerated = False
    while not weaponGenerated:
        weaponType = randint(1, 11)
        if weaponType == 1:
            weapon = Pistol(PISTOL_FIRE_RATE, PISTOL_DAMAGE)
            weaponGenerated = True

        elif weaponType == 2:
            weapon = AssaultRifle(ASSAULT_RIFLE_FIRE_RATE, ASSAULT_RIFLE_DAMAGE)
            weaponGenerated = True

        elif weaponType == 3:
            weapon = MachineGun(MACHINE_GUN_FIRE_RATE, MACHINE_GUN_DAMAGE)
            weaponGenerated = True

        elif weaponType == 4:
            weapon = SniperRifle(SNIPER_FIRE_RATE, SNIPER_FIRE_DAMAGE)
            weaponGenerated = True

        elif weaponType == 5:
            weapon = Shotgun(SHOTGUN_FIRE_RATE, SHOTGUN_DAMAGE)
            weaponGenerated = True

        elif weaponType == 6:
            weapon = GrenadeLauncher(GRENADE_LAUNCHER_FIRE_RATE, GRENADE_LAUNCHER_DAMAGE)
            weaponGenerated = True

        elif weaponType == 7 and levelNumber >= 3:
            weapon = LaserPistol()
            weaponGenerated = True

        elif weaponType == 8 and levelNumber >= 3:
            weapon = LaserShotgun()
            weaponGenerated = True

        elif weaponType == 9 and levelNumber >= 3:
            weapon = LaserMachineGun()
            weaponGenerated = True

        elif weaponType == 10 and levelNumber >= 3:
            weapon = LaserAssaultRifle()
            weaponGenerated = True

        elif weaponType == 11 and levelNumber >= 3:
            weapon = LaserSniperRifle()
            weaponGenerated = True
    return weapon


###############################################################################
#
# Collision functions
#
###############################################################################
# Bullet and grenade collision functions #
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
            if enemy.hitbox.colliderect(bullet.hitbox) and not enemy.damaged and not isinstance(bullet, Icicle):
                # damages enemy if the enemy is not already damaged(invincible) and the bullet is not an icicle
                enemy.takeDamage(bullet.damage)
                enemy.damaged = True

                # remove the bullet if possible -------------------------------
                if bullet in bullets and not isinstance(bullet, LaserBullet) and not enemy.isDead:
                    bullets.remove(bullet)


        # removes bullet if it has left the screen ----------------------------
        if bullet.x > WIDTH + 10 or bullet.x < -10 or bullet.y > HEIGHT + 10:
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

        # enemy-fired bullet --------------------------------------------------
        if isinstance(bullet, Icicle):
            # player hitbox
            playerHitbox = pygame.Rect(playerToCheck.x - PLAYER_SIZE_X / 2, playerToCheck.y - PLAYER_SIZE_Y / 2, PLAYER_SIZE_X, PLAYER_SIZE_Y)
            if bullet.hitbox.colliderect(playerHitbox):
                # damages player upon collision
                player.takeDamage(bullet.damage)

                # removes bullet if possible
                if bullet in bullets:
                    bullets.remove(bullet)


def checkGrenadeCollision() -> None:
    """ Checks if any grenade in the 'grenades' list has collided with any enemies or platforms

    Parameters:

    Return => None
    """
    # Checks if the bullet is in any platforms or enemies
    for grenade in grenades:
        for platform in level.platforms:
            # Builds platform hitbox
            platformHitbox = pygame.Rect(platform.x, platform.y, platform.length, platform.width)

            # explodes grenade if grenade hits a platform
            if grenade.hitbox.colliderect(platformHitbox):
                grenade.exploded = True

            # Checks every enemy for collision
            for enemy in enemies:

                # explodes if grenade hits an enemy
                if grenade.hitbox.colliderect(enemy.hitbox):
                    grenade.exploded = True

                # Deduct health
                if grenade.exploded and grenade.explosionHitbox.colliderect(
                        enemy.hitbox) and grenade.explosionAnimationStage == 0:
                    enemy.takeDamage(GRENADE_LAUNCHER_DAMAGE)

        # Remove grenade when explosion animation ends
        if grenade.explosionAnimationStage >= len(grenade.explosionAnimation) * 8 - 1:
            grenades.pop(grenades.index(grenade))

        # removes grenade if it falls out of the screen
        if grenade.y > HEIGHT + 10:
            grenades.pop(grenades.index(grenade))


# redraw functions - combines other functions
def redrawPlayer(playerToDraw: Player) -> None:
    """ Responsible for drawing and moving the player, as well has the weapon cooldown

    Parameters:
        playerToDraw: Player
            The player to draw and move

    Return => None
    """
    global timeFired, timeHit, timeThrown
    playerToDraw.move()
    playerToDraw.draw()
    # Fire weapon if possible
    playerToDraw.fireWeapon()

    # Draw the bullet GUI with the time
    drawBulletDisplay(timeElapsed - playerToDraw.currentWeapon.timeSinceFire, playerToDraw.currentWeapon.fireRate)

    # Invincible delay --------------------------------------------------------
    enemyHit = False
    for enemy in enemies:
        enemyHit = playerToDraw.checkEnemyCollision(enemy)
    # get the current time
    if enemyHit:
        timeHit = timeElapsed

    if (timeElapsed - timeHit) >= INVINCIBLE_DELAY:
        playerToDraw.invincible = False

    # Checks for player collision with the edges of the screen
    if not levelTransition:
        playerToDraw.checkCollision()


def redrawEnemies(playerToCheck: Player) -> None:
    """ Draws and move the enemies, as well as collision and deletion

    Parameters:
        playerToCheck: Player
            The player to check collision for

    Return => None
    """

    global enemyTimeHit
    # checks if enemy is alive
    checkEnemyAlive()

    # draws and move enemy
    drawEnemies()
    moveEnemies()

    # records time when hit - for invincibility
    for enemy in enemies:
        enemyHit = playerToCheck.checkEnemyCollision(enemy)
        if enemyHit and enemy.damaged:
            enemyTimeHit = timeElapsed

        if (timeElapsed - timeHit) >= 0.25:
            enemy.damaged = False

    # delete enemies that are finished their death animation
    deleteEnemies()


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


def drawHealthBar() -> None:
    """ Draws health bar

    Parameters:


    Return => None
    """
    # drawing player health in chunks of 5
    for j in range(int(player.health // 5)):
        # health
        pygame.draw.rect(gameWindow, RED, (WIDTH - 326 + (j * 14), 28, 14, 30), 0, 0)
        pygame.draw.rect(gameWindow, LRED, (WIDTH - 326 + (j * 14), 33, 14, 6), 0, 0)

        # drawing over edges of health bar
        if j == 0:
            pygame.draw.rect(gameWindow, RED, (WIDTH - 326, 28, 6, 30), 0, 0)
        if j == (player.health // 5) - 1:
            pygame.draw.rect(gameWindow, RED, (WIDTH - 326 + (j * 14) + 8, 28, 6, 30), 0, 0)

    # border
    pygame.draw.rect(gameWindow, BLACK, (WIDTH - 330, 25, 286, 36), 5, 8)
    pygame.draw.rect(gameWindow, (64, 64, 64), (WIDTH - 330, 23, 288, 40), 3, 8)


def drawCoinDisplay() -> None:
    """ Draws coin display at the top left corner

    Parameters:


    Return => None
    """
    # changes colour based on background
    colour = BLACK if level.background is iceBackgroundImage else WHITE

    # rendering text, with antialias off
    xRender = scoreFontSmall.render("x", False, colour)
    scoreRender = scoreFont.render(f"{coinsCollected}", False, colour)

    # blitting text and images
    gameWindow.blit(coinIcon, (25, 15))
    gameWindow.blit(xRender, (80, 30))
    gameWindow.blit(scoreRender, (100, 20))


def drawBulletDisplay(timeSinceFire: float, fireRate: float) -> None:
    """ draws bullet display at bottom right corner - time until you can fire again.
        The bullet is "greyed out" and slowly "reloads"

    Parameters:
        timeSinceFire: float
            The time since firing

        fireRate: float
            fire rate of the weapon


    Return => None
    """
    # draws different versions of the bullet depending on 'timeSinceFire'
    if round(timeSinceFire, 2) <= round(fireRate / 6, 2):
        gameWindow.blit(bulletGUI[0], (WIDTH - 80, HEIGHT - 50))

    elif round(timeSinceFire, 2) <= round(fireRate / 3, 2):
        gameWindow.blit(bulletGUI[1], (WIDTH - 80, HEIGHT - 50))

    elif round(timeSinceFire, 2) <= round(fireRate / 2, 2):
        gameWindow.blit(bulletGUI[2], (WIDTH - 80, HEIGHT - 50))

    elif round(timeSinceFire, 2) <= round(fireRate / 1.25, 2):
        gameWindow.blit(bulletGUI[3], (WIDTH - 80, HEIGHT - 50))

    else:
        gameWindow.blit(bulletGUI[4], (WIDTH - 80, HEIGHT - 50))


def drawWeaponDisplay() -> None:
    """ Draws weapon display under the health bar

    Parameters:


    Return => None
    """
    # changing colour if the background is the underworld one
    colour = (32, 32, 32) if level.background is iceBackgroundImage else WHITE

    # rendering name
    weaponName = scoreFontSmall.render(player.currentWeapon.name, True, colour)
    weaponNameLength = weaponName.get_size()[0]

    # blits name based on width of weapon name
    gameWindow.blit(weaponName, (WIDTH - 186 - weaponNameLength / 2, 60))


def drawGUI() -> None:
    """ Draws GUI by combining the drawHealthBar(), drawCoinDisplay(), and drawWeaponDisplay() functions

    Parameters:


    Return => None
    """
    drawHealthBar()
    drawCoinDisplay()
    drawWeaponDisplay()


def checkQuit() -> bool:
    """ Checks if the ESCAPE or QUIT button has been pressed, and returns True if so

    Parameters:


    Return => bool
    """
    keys = pygame.key.get_pressed()
    # ESC key and QUIT button
    if keys[pygame.K_ESCAPE]:
        return True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False


# Timer
FPS = 60
fpsClock = pygame.time.Clock()
timeElapsed = 0

# Time when 'something' hit
timeHit = 0
enemyTimeHit = 0
timeFired = 0
timeThrown = 0

###############################################################################
#
# Weapon Info
#
###############################################################################

# pistol
PISTOL_FIRE_RATE = 1.5
PISTOL_DAMAGE = 40

# machine gun
ASSAULT_RIFLE_FIRE_RATE = 0.4
ASSAULT_RIFLE_DAMAGE = 20

# shotgun
SHOTGUN_FIRE_RATE = 2.5
SHOTGUN_DAMAGE = 160

# sniper
SNIPER_FIRE_RATE = 4
SNIPER_FIRE_DAMAGE = 120

# machine gun
MACHINE_GUN_FIRE_RATE = 0.1
MACHINE_GUN_DAMAGE = 15

# grenade launcher
GRENADE_LAUNCHER_FIRE_RATE = 6
GRENADE_LAUNCHER_DAMAGE = 120

# delay constants
GRENADE_DELAY = 5
INVINCIBLE_DELAY = 0.35

###############################################################################
#
# Initialization of game variables
#
###############################################################################
# Player and spawn platform
player = Player(100, 0.25, 5, 2.5, 15, 150, HEIGHT//2 - 120, Pistol(PISTOL_FIRE_RATE, PISTOL_DAMAGE))
spawnPlatform = Platform(100, HEIGHT//2 - 100, 100)

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
level = Level(15)

# Level number - 0 is tutorial
levelNumber = 0

# if the player if transitioning between levels
levelTransition = False

# maximum platforms
MAX_PLATFORMS = 100

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

# loading menu soundtrack
pygame.mixer.music.unload()
pygame.mixer.music.load("sounds/menuSoundtrack.mp3")
pygame.mixer.music.play(-1)

###############################################################################
#
# Menu Loop
#
###############################################################################
while inMenu:
    # clearing events -------------------------------------------------
    pygame.event.clear()

    # blitting background ---------------------------------------------
    gameWindow.blit(menuBackgroundImage, (0, 0))

    # mouse position and button status --------------------------------
    mousePos = pygame.mouse.get_pos()
    mouseClicked = pygame.mouse.get_pressed(3)[0]

    # rendering text --------------------------------------------------
    title = titleFont.render("Bit by Bit", False, BLACK)
    playText = subTitleFont.render("Play", False, BLACK)

    # getting the width and height of the title and play text ---------
    titleWidth, titleHeight = titleFont.size("Bit by Bit")
    playTextWidth, playTextHeight = subTitleFont.size("Play")

    # setting hitbox for play button ----------------------------------
    playHitbox = pygame.Rect(WIDTH / 2 - playTextWidth / 2, titleHeight + WIDTH*17/54, playTextWidth, playTextHeight)

    # makes the text white upon hover ---------------------------------
    if playHitbox.collidepoint(mousePos):
        playText = subTitleFont.render("Play", True, WHITE)

    # starts the game upon hover and click ----------------------------
    if playHitbox.collidepoint(mousePos) and mouseClicked:
        inMenu = False

    # line decorations ------------------------------------------------
    pygame.draw.line(gameWindow, WHITE, (WIDTH/2 - titleWidth/2, 40), (WIDTH/2 + titleWidth/2, 40))
    pygame.draw.line(gameWindow, WHITE, (WIDTH / 2 - titleWidth / 2, 36), (WIDTH / 2 + titleWidth / 2, 36))
    pygame.draw.line(gameWindow, WHITE, (WIDTH/2 - titleWidth/2, 40 + titleHeight + 4), (WIDTH/2 + titleWidth/2, 40 + titleHeight + 4))
    pygame.draw.line(gameWindow, WHITE, (WIDTH / 2 - titleWidth / 2, 40 + titleHeight + 8), (WIDTH / 2 + titleWidth / 2, 40 + titleHeight + 8))

    # blitting text ---------------------------------------------------
    gameWindow.blit(title, (WIDTH/2 - titleWidth/2, 40))
    gameWindow.blit(playText, (WIDTH/2 - playTextWidth/2, titleHeight + WIDTH*17/54))


    # check for quit events -------------------------------------------
    if checkQuit():
        inMenu = False
        inPlay = False
        inGame = False

    # updating screen -------------------------------------------------
    pygame.display.update()

# -----------------------------------------------------------------------------



#######################################################################################################################
#
# Main Loop: Game Loop + Restart Menu
#
#######################################################################################################################
while inGame:
    # clearing events -------------------------------------------------
    pygame.event.clear()

    # restarts music --------------------------------------------------
    if not endScreen:
        pygame.time.delay(300)
        pygame.mixer.music.unload()
        pygame.mixer.music.load("sounds/soundtrack.mp3")
        pygame.mixer.music.play(-1)

    ###########################################################################################
    #
    # Game Loop
    #
    ###########################################################################################
    while inPlay:
        # clearing events -----------------------------------------------------
        pygame.event.clear()

        # Adding background ---------------------------------------------------
        gameWindow.blit(level.background, (0, 0))

        # Redraws chests ------------------------------------------------------
        redrawChest(player)

        # drawing player, and ending game if collision occurs -----------------
        redrawPlayer(player)
        if player.checkLife():
            inPlay = False
            endScreen = True

        # drawing platforms ---------------------------------------------------
        level.redrawPlatforms(player)

        # draws portals -------------------------------------------------------
        drawPortals()

        # drawing enemies -----------------------------------------------------
        redrawEnemies(player)

        # draws GUI -----------------------------------------------------------
        drawGUI()

        # redraws bullets -----------------------------------------------------
        redrawBullets()

        # redraws grenades ----------------------------------------------------
        redrawGrenades()

        # checks for bullet collision -----------------------------------------
        checkBulletCollision(player)

        # checks for grenade collision ----------------------------------------
        checkGrenadeCollision()

        # draws collectibles and detects collision ----------------------------
        redrawCollectibles(player)

        # checks if new level has to be generated -----------------------------
        level = generateLevel(player)

        # moves background  ---------------------------------------------------
        moveBackground(0.125)

        # accumulates time  ---------------------------------------------------
        time = fpsClock.tick(FPS)
        timeElapsed += time / 1000

        # Checking for quit events  -------------------------------------------
        if checkQuit():
            inPlay = False
            inGame = False

        # updating screen  ----------------------------------------------------
        pygame.display.update()

    # -----------------------------------------------------------------------------------------


    # stops soundtrack ------------------------------------------------
    pygame.mixer.music.pause()

    # plays death sound -----------------------------------------------
    playerDies.play()


    ###########################################################################################
    #
    # Restart Loop
    #
    ###########################################################################################
    while endScreen:
        # clearing events -----------------------------------------------------
        pygame.event.clear()

        # blitting background -------------------------------------------------
        gameWindow.blit(menuBackgroundImage, (0, 0))

        # mouse position and button status ------------------------------------
        mousePos = pygame.mouse.get_pos()
        mouseClicked = pygame.mouse.get_pressed(3)[0]

        # rendering text ------------------------------------------------------
        title = titleFont.render("Bit by Bit", True, BLACK)
        restartText = subTitleFont.render("Restart", True, BLACK)

        # getting the width and height of the title and restart text ----------
        titleWidth, titleHeight = titleFont.size("Bit by Bit")
        restartTextWidth, restartTextHeight = subTitleFont.size("Restart")

        # setting hitbox for restart button -----------------------------------
        restartHitbox = pygame.Rect(WIDTH / 2 - restartTextWidth / 2, titleHeight + WIDTH*17/54, restartTextWidth, restartTextHeight)

        # makes the text white upon hover -------------------------------------
        if restartHitbox.collidepoint(mousePos):
            restartText = subTitleFont.render("Restart", True, WHITE)

        # resets and restarts the game upon hover and click -------------------
        if restartHitbox.collidepoint(mousePos) and mouseClicked:
            inPlay = True
            endScreen = False

            # resetting game ------------------------------------------
            player = Player(100, 0.25, 5, 2.5, 15, 150,  HEIGHT//2 - 120, Pistol(PISTOL_FIRE_RATE, PISTOL_DAMAGE))
            spawnPlatform = Platform(100, HEIGHT//2 - 100, 100)

            # clearing lists ------------------------------------------
            enemies.clear()
            collectibles.clear()
            coinsCollected = 0
            bullets.clear()
            grenades.clear()
            chests.clear()
            portals.clear()

            # reset level ---------------------------------------------
            level = Level(15)
            levelNumber = 0

            # if the player if transitioning between levels -----------
            levelTransition = False

        # ---------------------------------------------------------------------



        # blitting text -------------------------------------------------------
        gameWindow.blit(title, (WIDTH / 2 - titleWidth / 2, 40))
        gameWindow.blit(restartText, (WIDTH / 2 - restartTextWidth / 2, titleHeight + WIDTH*17/54))

        # check for quit events -----------------------------------------------
        if checkQuit():
            inMenu = False
            inGame = False
            inPlay = False
            endScreen = False

        # updating screen -----------------------------------------------------
        pygame.display.update()

# quitting pygame
pygame.quit()
