import pygame, sys, os, time, math
clock = pygame.time.Clock()
pygame.display.set_caption("Tower Defense Game")
pygame.init()
screen = pygame.display.set_mode((1400, 800))
running = True
placing = False
down = False
collide=False
on_path = False
cash = 500
health = 100
towersWidth = 80
towersHeight = 80
titan = pygame.image.load('graphics/titan.png')
titan = pygame.transform.scale(titan, (80, 80))
bonerDragon = pygame.image.load('graphics/bonerDragon.png')
bonerDragon = pygame.transform.scale(bonerDragon, (80, 80))
skeleton = pygame.image.load('graphics/skeleton.png')
skeleton = pygame.transform.scale(skeleton, (80, 80))
necromancer = pygame.image.load('graphics/necromancer.png')
necromancer = pygame.transform.scale(necromancer, (110, 80))
wizard = pygame.image.load('graphics/wizard.png')
wizard = pygame.transform.scale(wizard, (towersWidth, towersHeight))
dragon = pygame.image.load('graphics/dragon.png')
dragon = pygame.transform.scale(dragon, (towersWidth, towersHeight))
archer = pygame.image.load('graphics/archer.png')
archer = pygame.transform.scale(archer, (towersWidth, towersHeight))
knight = pygame.image.load('graphics/knight.png')
knight = pygame.transform.scale(knight, (towersWidth, towersHeight))
LOOP_CENTER = (600, 405) 
LOOP_RADIUS = 210  



loop_points = []
for i in range(100):
    angle = math.radians(-90 + i * 5.1)

    x = LOOP_CENTER[0] + math.cos(angle) * LOOP_RADIUS
    y = LOOP_CENTER[1] + math.sin(angle) * LOOP_RADIUS

    loop_points.append((x, y))

wayPoints = ([(0, 195), (400, 195)] + loop_points + [(800, 620), (1200, 620)])

class Tower:
    def __init__ (Tower, towerX, towerY, width, height, towerType = None, sellerType = False, sellerCost = 0):
        Tower.x = towerX
        Tower.y = towerY
        Tower.type = towerType
        Tower.cost = sellerCost
        Tower.sellerType = sellerType
        Tower.w = width
        Tower.h = height
        Tower.rect = (pygame.Rect(towerX, towerY, width, height))

class Weapon:
    def __init__(Weapon, startX, startY, goalX, goalY, damage, weaponType, radius = 0):
        Weapon.goalX = goalX
        Weapon.goalY = goalY
        Weapon.damage = damage
        Weapon.type = weaponType
        Weapon.startX = startX
        Weapon.startY = startY
        Weapon.radius = radius
        if not weaponType == 'area':
            Weapon.rect = (pygame.Rect(startX, startY, 20, 20))

class Enemy:
    def __init__(Enemy, health, enemyType, speed, x, y, damage):
        Enemy.health = health
        Enemy.type = enemyType
        Enemy.speed = speed
        Enemy.x = x
        Enemy.y = y
        Enemy.rect = pygame.Rect(x, y, 40, 40)
        Enemy.wayPointIndex = 0
        Enemy.damage = damage


    def move(Enemy):
        if Enemy.wayPointIndex >= len(wayPoints):
            return

        targetX, targetY = wayPoints[Enemy.wayPointIndex]
        dx = targetX - Enemy.x
        dy = targetY - Enemy.y
        dist = math.hypot(dx, dy)

        if dist < Enemy.speed:
            Enemy.x = targetX
            Enemy.y = targetY
            Enemy.wayPointIndex += 1
        else:
            Enemy.x += (dx / dist) * Enemy.speed
            Enemy.y += (dy / dist) * Enemy.speed

        Enemy.rect.x = Enemy.x-40
        Enemy.rect.y = Enemy.y-40


closest = None
closestDist = 'inf'
towers = [Tower(1250, 350, towersWidth, towersHeight, "seller", "range", 200), Tower(1250, 425, towersWidth, towersHeight, "seller", "short", 100), Tower(1250, 500, towersWidth, towersHeight ,"seller", "area", 50)]
weapons = []
enemies = []
font = pygame.font.Font(None, 36)
cash_content = f'Cash: {cash}$'
cash_surface = font.render(cash_content, True, (255, 255, 255))
cash_rect = cash_surface.get_rect(topleft=(1060, 10))

health_content = f'health: {health}$'
health_surface = font.render(health_content, True, (255, 255, 255))
health_rect = health_surface.get_rect(topleft=(1060, 50))
placingType = None

enemyQueue = []
spawnTimer = 0

wave1 = [['titan', 5]]
wave2 = [['titan', 10]]
wave3 = [['titan', 5], ['skeleton', 3]]
wave4 = [['skeleton', 3], ['titan', 5], ['skeleton', 3]]
wave5 = [['titan', 20]]
wave6 = [['skeleton',5], ['bonerDragon', 1]]
wave7 = [['bonerDragon', 3]]
wave8 = [['titan', 10], ['skeleton', 5], ['bonerDragon', 2]]
wave9 = [['necromancer', 1]]
wave10 = [['bonerDragon', 3], ['necromancer', 1]]

waveQueue = [wave1, wave2, wave3, wave4, wave5, wave6, wave7, wave8, wave9, wave10]


def waveStart(wave):
    for enemy in wave:
        if enemy[0] == 'titan':
            for x in range(enemy[1]):
                enemyQueue.append(Enemy(5, "titan", 3, 0, 195, 1))
        elif enemy[0] == 'skeleton':
            for x in range(enemy[1]):
                enemyQueue.append(Enemy(10, "skeleton", 7, 0, 195, 2))
        elif enemy[0] == 'bonerDragon':
            for x in range(enemy[1]):
                enemyQueue.append(Enemy(40, "bonerDragon", 12, 0, 195, 3))
        elif enemy[0] == 'necromancer':
            for x in range(enemy[1]):
                enemyQueue.append(Enemy(85, "necromancer", 3, 0, 195, 4))


tick=0
while running:
    tick += 1
    tick = tick % 60
    mouseX, mouseY = pygame.mouse.get_pos()

    GREEN = (82, 130, 37)
    BROWN = (180, 130, 20)
    GREY = (128, 128, 128)

    PATH_WIDTH = 110
    LOOP_CENTER = (600, 405)
    LOOP_OUTER = 265
    LOOP_INNER = 155

    pygame.draw.rect(screen, GREEN, (0, 0, 1200, 800))
    pygame.draw.rect(screen, BROWN, (0, 140, 620, PATH_WIDTH))
    pygame.draw.circle(screen, BROWN, LOOP_CENTER, LOOP_OUTER)
    pygame.draw.circle(screen, GREEN, LOOP_CENTER, LOOP_INNER)
    pygame.draw.rect(screen, BROWN, (600, 560, 600, PATH_WIDTH))
    pygame.draw.rect(screen, GREY, (1200, 0, 200, 800))

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    enemies.append(Enemy(1, "titan", 5, 0, 195, 5))
                elif event.button == 2:
                    waveStart(waveQueue.pop(0))
                else:
                    if placing == False:
                        for tower in towers:
                            if tower.rect.collidepoint(mouseX, mouseY):
                                if tower.type == "seller" and cash - tower.cost >= 0: 
                                    placing = True
                                    towers.append(Tower(mouseX - tower.w  //  2, mouseY - tower.h  //  2, towersWidth, towersHeight, tower.sellerType))
                                    cash -= tower.cost
                                    placingType = tower.sellerType
                                    break
                    elif placing == True: 
                        temp_tower = Tower(mouseX - towersWidth // 2, mouseY - towersHeight // 2, towersWidth, towersHeight)
                        collide = False
                        on_path = False
                        for tower in towers:
                            if not tower.rect == temp_tower.rect:
                                if temp_tower.rect.colliderect(tower.rect):
                                    collide = True
                                    break
                        corners = [(temp_tower.rect.left+20, temp_tower.rect.top+20),(temp_tower.rect.right-20, temp_tower.rect.top+20),(temp_tower.rect.left+20, temp_tower.rect.bottom-20),(temp_tower.rect.right-20, temp_tower.rect.bottom-20)]
                        on_path = any(screen.get_at(corner)[:3] == BROWN for corner in corners)
                        if collide == False and on_path == False:
                            placing = False
                            

    if len(enemyQueue) > 0:
        spawnTimer += 1
    if spawnTimer >= 30:
        enemies.append(enemyQueue.pop(0))
        spawnTimer = 0

    if placing == True:
        towers[-1] = Tower(mouseX- towersWidth // 2, mouseY - towersHeight // 2, towersWidth, towersHeight, placingType)
    cash_content = f'Cash: {cash}$'
    cash_surface = font.render(cash_content, True, (255, 255, 255))
    health_content = f'Health: {health}'
    health_surface = font.render(health_content, True, (255, 255, 255))


    for tower in towers:
        if tower.type == "seller":
            if tower.sellerType == "range":
                screen.blit(archer, tower.rect)
            elif tower.sellerType == "short":
                screen.blit(knight, tower.rect)
                #pygame.draw.rect(screen, (255, 255, 0), tower.rect)
            elif tower.sellerType == "seller":
                pygame.draw.rect(screen, (0, 255, 255), tower.rect)
            elif tower.sellerType == "area":
                screen.blit(dragon, tower.rect)
                #pygame.draw.rect(screen, (255, 255, 255), tower.rect)
        else: 
            if tower.type == "range":
                #pygame.draw.rect(screen, (255, 0, 0), tower.rect)
                screen.blit(archer, tower.rect)
                if tick == 30 and (not tower.rect == towers[-1].rect or placing == False):
                    closest = None
                    closestDist = 9999999999999
                    for enemy in enemies:
                        xDiff = abs(tower.x - enemy.x)
                        yDiff = abs(tower.y - enemy.y)
                        if math.hypot(xDiff, yDiff) < closestDist and not enemy.health <= 0:
                            closest = enemy
                            closestDist = math.hypot(xDiff, yDiff)
                    for enemy in enemies:
                            if enemy == closest and not enemy.health <= 0:
                                enemy.health -= 5
                                break
            elif tower.type == "short":
                screen.blit(knight, tower.rect)
                #pygame.draw.rect(screen, (255, 255, 0), tower.rect)
            elif tower.type == "area":
                screen.blit(dragon, tower.rect)
                #pygame.draw.rect(screen, (255, 255, 255), tower.rect)
                if not tower.rect == towers[-1].rect or placing == False:
                    weapons.append(Weapon(tower.x + tower.w // 2, tower.y + tower.h // 2, 0, 0, 20, "area", 2))
    for weapon in weapons:
        if weapon.type == 'range':
            pygame.draw.rect(screen, (255, 255, 255), weapon.rect)
        elif weapon.type == 'area':
            pygame.draw.circle(screen, (0, 0, 255), (weapon.startX, weapon.startY), weapon.radius)
    
    for enemy in enemies:
        if enemy.health <= 0:
            enemies.pop(enemies.index(enemy))
            cash += 15
        enemy.move()

        if enemy.x == 1200 and enemy.y == 620:
            enemies.pop(enemies.index(enemy))
            health -= enemy.damage
        if enemy.type == 'titan':
            screen.blit(titan, enemy.rect)
        elif enemy.type == 'bonerDragon':
            screen.blit(bonerDragon, enemy.rect)
        elif enemy.type == 'skeleton':
            screen.blit(skeleton, enemy.rect)
        elif enemy.type == 'necromancer':
            screen.blit(necromancer, enemy.rect)
    screen.blit(cash_surface, cash_rect)
    screen.blit(health_surface, health_rect)
    pygame.display.flip()
    clock.tick(60)