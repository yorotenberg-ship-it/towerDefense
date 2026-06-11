import pygame, sys, os, time, math
clock = pygame.time.Clock()
pygame.display.set_caption("Tower Defense Game")
pygame.init()
screen = pygame.display.set_mode((1219, 814))
background = pygame.image.load("map.png")
background = pygame.transform.scale(background, (1219, 814))
running = True
placing = False
down = False
collide=False
cash = 500
towersWidth = 50
towersHeight = 50

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
    def __init__(Enemy, health, enemyType, speed, x, y):
        Enemy.health = health
        Enemy.type = enemyType
        Enemy.speed = speed
        Enemy.x = x
        Enemy.y = y
        Enemy.rect = pygame.Rect(x, y, 40, 40)
        Enemy.wayPointIndex = 0

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

        Enemy.rect.x = Enemy.x-20
        Enemy.rect.y = Enemy.y-20


closest = None
closestDist = 'inf'
towers = [Tower(100, 100, towersWidth, towersHeight, "seller", "range", 200), Tower(100, 250, towersWidth, towersHeight, "seller", "short", 100), Tower(100, 400, towersWidth, towersHeight ,"seller", "area", 50)]
weapons = []
enemies = []
font = pygame.font.Font(None, 36)
cash_content = f'Cash: {cash}$'
cash_surface = font.render(cash_content, True, (255, 255, 255))
cash_rect = cash_surface.get_rect(topleft=(1060, 10))
placingType = None

tick=0
while running:

    tick += 1
    tick = tick % 60
    mouseX, mouseY = pygame.mouse.get_pos()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    enemies.append(Enemy(1, "normal", 10, 0, 170))
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
                        temp_tower = Tower(mouseX - towersWidth  //  2, mouseY - towersHeight // 2, towersWidth, towersHeight)
                        for tower in towers: 
                            if not tower.rect == temp_tower.rect:
                                collide = temp_tower.rect.colliderect(tower.rect)
                                if collide == True: break
                            
                        if collide == False: 
                            
                            placing = False
    #print(placing)
    

    if placing == True:
        towers[-1] = Tower(mouseX- towersWidth // 2, mouseY - towersHeight // 2, towersWidth, towersHeight, placingType)
    cash_content = f'Cash: {cash}$'
    cash_surface = font.render(cash_content, True, (255, 255, 255))

    GREEN = (82, 130, 37)
    BROWN = (180, 130, 20)
    PATH_WIDTH = 110
    LOOP_CENTER = (600, 405)
    LOOP_OUTER = 265
    LOOP_INNER = 155

# grass background
    pygame.draw.rect(screen, GREEN, (0, 0, 1200, 800))

# entry straight (top left)
    pygame.draw.rect(screen, BROWN, (0, 140, 620, PATH_WIDTH))

# the loop ring
    pygame.draw.circle(screen, BROWN, LOOP_CENTER, LOOP_OUTER)
    pygame.draw.circle(screen, GREEN, LOOP_CENTER, LOOP_INNER)

# exit straight (bottom right)
    pygame.draw.rect(screen, BROWN, (600, 560, 600, PATH_WIDTH))
    for tower in towers:
        if tower.type == "seller":
            if tower.sellerType == "range":
                pygame.draw.rect(screen, (255, 0, 0), tower.rect)
            elif tower.sellerType == "short":
                pygame.draw.rect(screen, (255, 255, 0), tower.rect)
            elif tower.sellerType == "seller":
                pygame.draw.rect(screen, (0, 255, 255), tower.rect)
            elif tower.sellerType == "area":
                pygame.draw.rect(screen, (255, 255, 255), tower.rect)
        else: 
            if tower.type == "range":
                pygame.draw.rect(screen, (255, 0, 0), tower.rect)
                if tick == 30 and (not tower.rect == towers[-1].rect or placing == False):
                    closest = None
                    closestDist = 9999999999999
                    for enemy in enemies:
                        xDiff = abs(tower.x - enemy.x)
                        yDiff = abs(tower.y - enemy.y)
                        if math.hypot(xDiff, yDiff) < closestDist:
                            closest = enemy
                            closestDist = math.hypot(xDiff, yDiff)
                    
                    for enemy in enemies:
                            if enemy == closest:
                                enemy.health -= 5
                                

                    #weapons.append(Weapon(tower.x + (tower.w - 20) // 2, tower.y + (tower.w - 20) // 2, 0, 0, 50, "range"))
            elif tower.type == "short":
                pygame.draw.rect(screen, (255, 255, 0), tower.rect)
            elif tower.type == "area":
                pygame.draw.rect(screen, (255, 255, 255), tower.rect)
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
            cash += 100
        enemy.move()
        
        pygame.draw.rect(screen, (0, 255, 0), enemy.rect)

    screen.blit(cash_surface, cash_rect)
    pygame.display.flip()
    

    clock.tick(60)
    