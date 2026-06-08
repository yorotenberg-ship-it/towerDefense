import pygame, sys, os, time, math

#This is a comment for testing if github works!

clock = pygame.time.Clock()
pygame.display.set_caption("Tower Defense Game")
pygame.init()
screen = pygame.display.set_mode((1200, 600))
running = True
BLACK = (0, 0, 0)
placing = False
down = False
collide=False
cash = 500
towersWidth = 50
towersHeight = 50

x = 200

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
    tick = tick % 60
    mouseX, mouseY = pygame.mouse.get_pos()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
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
                        towers.append(Tower(mouseX - towersWidth // 2, mouseY - towersHeight // 2, towersWidth, towersHeight, placingType))
                        placing = False
    #print(placing)
    

    if placing == True:
        towers[-1] = Tower(mouseX- towersWidth // 2, mouseY - towersHeight // 2, towersWidth, towersHeight, placingType)
    cash_content = f'Cash: {cash}$'
    cash_surface = font.render(cash_content, True, (255, 255, 255))

    screen.fill(BLACK)
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
                if tick == 0 and (not tower.rect == towers[-1].rect or placing == False):
                    if not enemies == []
                        closest = None
                        closestDist = 'inf'
                        for enemy in enemies:
                            xDiff = abs(tower.x - enemy.x)
                            yDiff = abs(tower.y - enemy.y)
                            if math.hypot(xDiff, yDiff) < closestDist:
                                closest = enemy
                                closestDist = math.hypot(xDiff, yDiff)
                        for enemy in enemies:
                            if enemy == closest:
                                enemy = Enemy(enemy.health - 50, enemy.type, enemy.speed, enemy.x, enemy.y)
                                break
                    
            
                    #weapons.append(Weapon(tower.x + (tower.w - 20) // 2, tower.y + (tower.w - 20) // 2, 0, 0, 50, "range"))
            elif tower.type == "short":
                pygame.draw.rect(screen, (255, 255, 0), tower.rect)
            elif tower.type == "area":
                pygame.draw.rect(screen, (255, 255, 255), tower.rect)
                if not tower.rect == towers[-1].rect or placing == False:
                    weapons.append(Weapon(tower.x + tower.w // 2, tower.y + tower.h // 2, 0, 0, 20, "area", 80))
    for weapon in weapons:
        if weapon.type == 'range':
            pygame.draw.rect(screen, (255, 255, 255), weapon.rect)
        elif weapon.type == 'area':
            pygame.draw.circle(screen, (0, 0, 255), (weapon.startX, weapon.startY), weapon.radius)
    screen.blit(cash_surface, cash_rect)
    pygame.display.flip()
    tick += 1

    clock.tick(60)
    