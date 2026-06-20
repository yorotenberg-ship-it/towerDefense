import pygame, sys, os, time, math
os.chdir(os.path.dirname(os.path.abspath(__file__)))
clock = pygame.time.Clock()
pygame.display.set_caption("Tower Defense Game")
pygame.init()
screen = pygame.display.set_mode((1400, 800))
placing, down, collide, on_path, placingType, running = False, False, False, False, None, True
cash, health, tick = 500, 100, 0
towersWidth, towersHeight = 80, 80
if True:
    titan = pygame.image.load('graphics/titan.png')
    titan = pygame.transform.scale(titan, (80, 80))
    bonerDragon = pygame.image.load('graphics/bonerDragon.png')
    bonerDragon = pygame.transform.scale(bonerDragon, (80, 80))
    skeleton = pygame.image.load('graphics/skeleton.png')
    skeleton = pygame.transform.scale(skeleton, (80, 80))
    necromancer = pygame.image.load('graphics/necromancer.png')
    necromancer = pygame.transform.scale(necromancer, (110, 80))
    skeletonKing = pygame.image.load('graphics/skeletonKing.png')
    skeletonKing = pygame.transform.scale(skeletonKing, (130, 130))
    wizard = pygame.image.load('graphics/wizard.png')
    wizard = pygame.transform.scale(wizard, (towersWidth, towersHeight))
    wizardArea = pygame.image.load('graphics/wizardArea.png')
    wizardArea = pygame.transform.scale(wizardArea, (300, 300))
    dragon = pygame.image.load('graphics/dragon.png')
    dragon = pygame.transform.scale(dragon, (towersWidth, towersHeight))
    archer = pygame.image.load('graphics/archer.png')
    archer = pygame.transform.scale(archer, (towersWidth, towersHeight))
    knight = pygame.image.load('graphics/knight.png')
    knight = pygame.transform.scale(knight, (towersWidth, towersHeight))
    iceWarrior = pygame.image.load('graphics/iceWarrior.png')
    iceWarrior = pygame.transform.scale(iceWarrior, (towersWidth + 20, towersHeight))
    death = pygame.image.load('graphics/death.png')
    death = pygame.transform.scale(death, (1400, 800))
LOOP_CENTER, LOOP_RADIUS = (600, 405), 210  

loop_points = []
for i in range(100):
    angle = math.radians(-90 + i * 5.1)

    x = LOOP_CENTER[0] + math.cos(angle) * LOOP_RADIUS
    y = LOOP_CENTER[1] + math.sin(angle) * LOOP_RADIUS

    loop_points.append((x, y))

wayPoints = ([(0, 195), (400, 195)] + loop_points + [(800, 620), (1200, 620)])

class Tower:
    def __init__ (Tower, damage, area, baseCooldown, towerX, towerY, width, height, towerType = None, sellerType = False, sellerCost = 0, angle = 0, cooldown = 0, attacks = 0):
        Tower.x = towerX
        Tower.y = towerY
        Tower.type = towerType
        Tower.cost = sellerCost
        Tower.sellerType = sellerType
        Tower.w = width
        Tower.h = height
        Tower.angle = angle
        Tower.cooldown = cooldown
        Tower.damageDealt = attacks
        Tower.damage = damage
        Tower.baseCooldown = baseCooldown
        Tower.range = area

        Tower.rect = (pygame.Rect(towerX, towerY, width, height))

class Enemy:
    def __init__(Enemy, health, enemyType, speed, x, y, damage, wait, frozen = 0):
        Enemy.health = health
        Enemy.type = enemyType
        Enemy.speed = speed
        Enemy.x = x
        Enemy.y = y
        Enemy.rect = pygame.Rect(x, y, 40, 40)
        Enemy.wayPointIndex = 0
        Enemy.damage = damage
        Enemy.wait = wait
        Enemy.frozen = frozen


    def move(Enemy, King):
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
        
        if King == True:
            Enemy.rect.x = Enemy.x-70
            Enemy.rect.y = Enemy.y-70
        else:
            Enemy.rect.x = Enemy.x-40
            Enemy.rect.y = Enemy.y-40

towers = [Tower(8, 999999, 120, 1250, 60, towersWidth, towersHeight, "seller", 'archer', 325), Tower(0, 200, 120, 1250, 260, towersWidth, towersHeight, "seller", "short", 400), Tower(1, 150, 4, 1250, 460, towersWidth, towersHeight ,"seller", "area", 550), Tower(2, 200, 60, 1250, 660, towersWidth, towersHeight ,"seller", "knight", 100)]
weapons, enemies, enemyQueue = [], [], []
font = pygame.font.Font(None, 36)
cash_content = f'Cash: {cash}$'
cash_surface = font.render(cash_content, True, (255, 255, 255))
cash_rect = cash_surface.get_rect(topleft=(1060, 10))

health_content = f'health: {health}$'
health_surface = font.render(health_content, True, (255, 255, 255))
health_rect = health_surface.get_rect(topleft=(1060, 50))

spawnTimer = 0

wave1 = [['titan', 5, 0]]
wave2 = [['titan', 10, 0]]
wave3 = [['titan', 5, 0], ['skeleton', 3, 0]]
wave4 = [['skeleton', 3, 0], ['titan', 5, 0], ['skeleton', 3, 0]]
wave5 = [['titan', 20, 0]]
wave6 = [['skeleton', 5, 0], ['bonerDragon', 1, 0]]
wave7 = [['bonerDragon', 3, 0]]
wave8 = [['titan', 10, 0], ['skeleton', 5, 0], ['bonerDragon', 2, 0]]
wave9 = [['necromancer', 1, 0]]
wave10 = [['bonerDragon', 3, 0], ['necromancer', 1, 0]]
wave11 = [['bonerDragon', 4, 0], ['air', 7, 0], ['bonerDragon', 3, 0]]
wave12 = [['bonerDragon', 5, 0], ['air', 7, 0], ['necromancer', 2, 0]]
wave13 = [['skeleton', 25, 29], ['air', 7, 0], ['bonerDragon', 4, 0]]
wave14 = [['necromancer', 3, 0]]
wave15 = [['bonerDragon', 7, 0], ['air', 7, 0], ['necromancer', 2, 0]]
wave16 = [['bonerDragon', 5, 0], ['air', 7, 0], ['necromancer', 2, 0]]
wave17 = [['bonerDragon', 4, 29], ['air', 7, 0], ['bonerDragon', 4, 29]]
wave18 = [['necromancer', 4, 0]]
wave19 = [['bonerDragon', 10, 10]]
wave20 = [['skeletonKing', 1, 0]]
wave21 = [['skeleton', 50, 29], ['necromancer', 1,0]]
wave22 = [['necromancer', 6, 10], ['bonerDragon', 5, 15]]
wave23 = [['skeleton', 35, 29], ['air', 7, 0], ['bonerDragon', 5, 15], ['air', 7, 0], ['skeleton', 35, 29], ['air', 7, 0], ['bonerDragon', 5, 15]]
wave24 = [['bonerDragon', 7, 15], ['air', 7, 0], ['skeletonKing', 1, 0]]
wave25 = [['skeletonKing', 2, 0]]
wave26 = [['skeletonKing', 1, 0], ['air', 7, 0], ['bonerDragon', 7, 29], ['skeletonKing', 1, 0]]
wave27 = [['bonerDragon', 1, 29], ['skeleton', 3, 29], ['bonerDragon', 1, 29], ['bonerDragon', 1, 29], ['skeleton', 3, 29], ['bonerDragon', 1, 29], ['skeleton', 3, 29], ['bonerDragon', 1, 29], ['skeleton', 3, 29], ['bonerDragon', 1, 29], ['skeleton', 3, 29], ['bonerDragon', 1, 29], ['skeleton', 3, 29]]
wave28 = [['bonerDragon', 20, 20]]
wave29 = [['titan', 7, 15], ['skeleton', 7, 15], ['bonerDragon', 7, 15], ['air', 7, 0], ['bonerDragon', 30, 15]]
wave30 = [['skeletonKing', 5, 0]]
waveQueue = [wave1, wave2, wave3, wave4, wave5, wave6, wave7, wave8, wave9, wave10, wave11, wave12, wave13, wave14, wave15, wave16, wave17, wave18, wave19, wave20, wave21, wave22, wave23, wave24, wave25, wave26, wave27, wave28, wave29, wave30]
GREEN = (82, 130, 37)
BROWN = (180, 130, 20)
GREY = (128, 128, 128)
PATH_WIDTH = 110
LOOP_CENTER = (600, 405)
LOOP_OUTER = 265
LOOP_INNER = 155
waves = len(waveQueue)
def waveStart(wave):
    global cash, enemies, enemyQueue
    for enemy in wave:
        if enemy[0] == 'titan':
            for x in range(enemy[1]):
                enemyQueue.append(Enemy(4, "titan", 3, 0, 195, 5, enemy[2]))
        elif enemy[0] == 'skeleton':
            for x in range(enemy[1]):
                enemyQueue.append(Enemy(10, "skeleton", 7, 0, 195, 10, enemy[2]))
        elif enemy[0] == 'bonerDragon':
            for x in range(enemy[1]):
                enemyQueue.append(Enemy(40, "bonerDragon", 12, 0, 195, 40, enemy[2]))
        elif enemy[0] == 'necromancer':
            for x in range(enemy[1]):
                enemyQueue.append(Enemy(200, "necromancer", 3, 0, 195, 200, enemy[2]))
        elif enemy[0] == 'skeletonKing':
            for x in range(enemy[1]):
                enemyQueue.append(Enemy(500, "skeletonKing", 2.2, 0, 195, 500, enemy[2]))
        elif enemy[0] == 'air':
            for x in range(enemy[1]):
                enemyQueue.append("air")

def draw ():
    pygame.draw.rect(screen, GREEN, (0, 0, 1200, 800))
    pygame.draw.rect(screen, BROWN, (0, 140, 620, PATH_WIDTH))
    pygame.draw.circle(screen, BROWN, LOOP_CENTER, LOOP_OUTER)
    pygame.draw.circle(screen, GREEN, LOOP_CENTER, LOOP_INNER)
    pygame.draw.rect(screen, BROWN, (600, 560, 600, PATH_WIDTH))
    pygame.draw.rect(screen, GREY, (1200, 0, 200, 800))

    name_surface = font.render('Archer', True, (0, 0, 0))
    desc_surface = font.render('Fires Arrows', True, (0, 0, 0))
    cost_surface = font.render(f'${325}', True, (0, 0, 0))
    screen.blit(name_surface, (1260, 20))
    screen.blit(desc_surface, (1230, 40))
    screen.blit(cost_surface, (1260, 130))

    name_surface = font.render('Ice Knight', True, (0, 0, 0))
    desc_surface = font.render('Slows Enemies', True, (0, 0, 0))
    cost_surface = font.render(f'${400}', True, (0, 0, 0))
    screen.blit(name_surface, (1240, 220))
    screen.blit(desc_surface, (1215, 240))
    screen.blit(cost_surface, (1260, 330))

    name_surface = font.render('Wizard', True, (0, 0, 0))
    desc_surface = font.render('Casts Spells', True, (0, 0, 0)) 
    cost_surface = font.render(f'${550}', True, (0, 0, 0))
    screen.blit(name_surface, (1250, 410))
    screen.blit(desc_surface, (1220, 440))
    screen.blit(cost_surface, (1260, 530))

    name_surface = font.render('Knight', True, (0, 0, 0))
    desc_surface = font.render('Stabs Enemies', True, (0, 0, 0)) 
    cost_surface = font.render(f'${100}', True, (0, 0, 0))
    screen.blit(name_surface, (1250, 620))
    screen.blit(desc_surface, (1210, 640))
    screen.blit(cost_surface, (1260, 730))

round_ended = False

while running:
    if health > 0:
        tick += 1
        mouseX, mouseY = pygame.mouse.get_pos()

        
        draw()

<<<<<<< HEAD
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
                    if not enemies == []:
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
=======
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    for x, tower in enumerate(towers):
                        if not tower.type == 'seller':
                            print(f'Num: {x - 3}, Type: {tower.type}, Damage: {tower.damageDealt}')
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not waveQueue == [] and enemies == [] and enemyQueue == []:
                        waveStart(waveQueue.pop(0))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    for x, tower in enumerate(towers):
                        if not tower.type == 'seller':
                            print(f'Num: {x - 3}, Type: {tower.type}, Damage: {tower.damageDealt}')
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        enemyQueue.append(Enemy(40, "bonerDragon", 12, 0, 195, 40, 30))
                    else:
                        if placing == False:
                            for tower in towers:
                                if tower.rect.collidepoint(mouseX, mouseY):
                                    if tower.type == "seller" and cash - tower.cost >= 0: 
                                        placing = True
                                        towers.append(Tower(tower.damage, tower.range, tower.baseCooldown, mouseX - tower.w  //  2, mouseY - tower.h  //  2, towersWidth, towersHeight, tower.sellerType))
                                        cash -= tower.cost
                                        placingType = tower.sellerType
                                        break
                        elif placing == True: 
                            temp_tower = Tower(0, 0, 0, mouseX - towersWidth // 2, mouseY - towersHeight // 2, towersWidth, towersHeight)
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
>>>>>>> 087855e2ec5641d9cd3ed063e673fcf76c6f7084
                    

        if len(enemyQueue) > 0:
            spawnTimer += 1
        if spawnTimer >= 30 and not enemyQueue == []:
            if not enemyQueue[0] == 'air':
                spawnTimer = int(enemyQueue[0].wait)
                enemies.append(enemyQueue.pop(0))
                
            else:
                spawnTimer = 0
                enemyQueue.pop(0)
            if enemyQueue == []:
                round_ended = True
        if enemies == [] and round_ended == True:
            round_ended = False
            cash += 100
        if placing == True:
            towers[-1] = Tower(towers[-1].damage, towers[-1].range, towers[-1].baseCooldown, mouseX- towersWidth // 2, mouseY - towersHeight // 2, towersWidth, towersHeight, placingType)
        currentWave = waves - len(waveQueue)
    
        wave_content = f'Wave: {currentWave}'
        wave_surface = font.render(wave_content, True, (255, 255, 255))
        wave_rect = wave_surface.get_rect(topleft=(10, 10)) 

        fps_content = f'FPS: {int(clock.get_fps())}'
        fps_surface = font.render(fps_content, True, (255, 255, 255))
        fps_rect = fps_surface.get_rect(topleft=(10, 30)) 

        cash_content = f'Cash: {cash}$'
        cash_surface = font.render(cash_content, True, (255, 255, 255))

        health_content = f'Health: {health}'
        health_surface = font.render(health_content, True, (255, 255, 255))

        for tower in towers:
            if tower.type == "seller":
                if tower.sellerType == 'archer':
                    screen.blit(archer, tower.rect)
                elif tower.sellerType == "short":
                    screen.blit(iceWarrior, tower.rect)
                elif tower.sellerType == "seller":
                    pygame.draw.rect(screen, (0, 255, 255), tower.rect)
                elif tower.sellerType == "area":
                    screen.blit(wizard, tower.rect)
                elif tower.sellerType == "knight":
                    screen.blit(knight, tower.rect)
            else: 
                if tower.type == 'archer':
                    if tower.cooldown > 0:
                        tower.cooldown -= 1
                    elif tower.cooldown == 0 and (not tower.rect == towers[-1].rect or placing == False):
                        first_enemy = None
                        best_progress = -1
                        for enemy in enemies:
                            if not enemy.health <= 0:
                                targetX, targetY = wayPoints[enemy.wayPointIndex]
                                dist_to_next = math.hypot(targetX - enemy.x, targetY - enemy.y)
                                progress = enemy.wayPointIndex * 10000 - dist_to_next
                                if progress > best_progress:
                                    best_progress = progress
                                    first_enemy = enemy
                        
                        for enemy in enemies:
                                if enemy == first_enemy and not enemy.health <= 0:
                                    enemy.health -= 8
                                    tower.damageDealt += 8
                                    tower.cooldown = 120
                                    targetX = enemy.x
                                    targetY = enemy.y
                                    dx = targetX - tower.rect.centerx
                                    dy = targetY - tower.rect.centery
                                    angle = math.degrees(math.atan2(-dy, dx))
                                    tower.angle = angle
                                    pygame.draw.line(screen, (255, 255, 255), (tower.rect.centerx, tower.rect.centery), (targetX, targetY), 5)

                elif tower.type == "short":
                    if tower.cooldown > 0:
                        tower.cooldown -= 1
                    elif not tower.rect == towers[-1].rect or placing == False:
                        first_enemy = None
                        best_progress = -1
                        for enemy in enemies:
                            if math.hypot(tower.x - enemy.x, tower.y - enemy.y) < 200:
                                if not enemy.health <= 0 and not enemy.type == "skeletonKing":
                                    if not enemy.frozen > 20:
                                        enemy.frozen = 20
                                    targetX, targetY = wayPoints[enemy.wayPointIndex]
                                    dist_to_next = math.hypot(targetX - enemy.x, targetY - enemy.y)
                                    progress = enemy.wayPointIndex * 10000 - dist_to_next
                                    if progress > best_progress:
                                        best_progress = progress
                                        first_enemy = enemy
                                
                        for enemy in enemies:
                                if enemy == first_enemy and not enemy.health <= 0:
                                    enemy.frozen = 110
                                    tower.cooldown = 120
                                    targetX = enemy.x
                                    targetY = enemy.y
                                    dx = targetX - tower.rect.centerx
                                    dy = targetY - tower.rect.centery
                                    angle = math.degrees(math.atan2(-dy, dx))
                                    tower.angle = angle
                elif tower.type == "area":
                    if not tower.rect == towers[-1].rect or placing == False:
                        area_rect = wizardArea.get_rect(center=tower.rect.center)
                        screen.blit(wizardArea, area_rect)
                        for enemy in enemies:
                            if math.hypot(tower.x - enemy.x, tower.y - enemy.y) < 150 and tick % 4 == 0:
                                enemy.health -= 1
                                tower.damageDealt += 1

                elif tower.type == "knight":
                    if tower.cooldown > 0:
                        tower.cooldown -= 1
                    elif not tower.rect == towers[-1].rect or placing == False:
                        first_enemy = None
                        best_progress = -1
                        for enemy in enemies:
                            if math.hypot(tower.x - enemy.x, tower.y - enemy.y) < 200:
                                if not enemy.health <= 0:
                                    targetX, targetY = wayPoints[enemy.wayPointIndex]
                                    dist_to_next = math.hypot(targetX - enemy.x, targetY - enemy.y)
                                    progress = enemy.wayPointIndex * 10000 - dist_to_next
                                    if progress > best_progress:
                                        best_progress = progress
                                        first_enemy = enemy
                                
                        for enemy in enemies:
                                if enemy == first_enemy and not enemy.health <= 0:
                                    enemy.health -= tower.damage
                                    tower.damageDealt += tower.damage
                                    tower.cooldown = 60
                                    targetX = enemy.x
                                    targetY = enemy.y
                                    dx = targetX - tower.rect.centerx
                                    dy = targetY - tower.rect.centery
                                    angle = math.degrees(math.atan2(-dy, dx))
                                    tower.angle = angle

                
        for tower in towers:
            if tower.type == 'area':
                screen.blit(wizard, tower.rect)
            elif tower.type == 'archer':
                rotated_image = pygame.transform.rotate(archer, tower.angle)
                rotated_rect = rotated_image.get_rect(center=tower.rect.center)
                screen.blit(rotated_image, rotated_rect)
            elif tower.type == 'short':
                rotated_image = pygame.transform.rotate(iceWarrior, tower.angle)
                rotated_rect = rotated_image.get_rect(center=tower.rect.center)
                screen.blit(rotated_image, rotated_rect)
            elif tower.type == 'knight':
                rotated_image = pygame.transform.rotate(knight, tower.angle)
                rotated_rect = rotated_image.get_rect(center=tower.rect.center)
                screen.blit(rotated_image, rotated_rect)
        weapons = []
        for enemy in enemies:
            if enemy.health <= 0:
                enemies.pop(enemies.index(enemy))
                cash += 15
            if enemy.frozen > 0:
                enemy.frozen -= 1
            else:
                if enemy.type != 'skeletonKing':
                    King = False
                else:
                    King = True
                enemy.move(King)
        
            if enemy.x == 1200 and enemy.y == 620:
                print(f'Health Left: {enemy.health}')
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
            elif enemy.type == 'skeletonKing':
                screen.blit(skeletonKing, enemy.rect)

        if len(enemies) == 0 and enemyQueue == []:
            help_content = 'press space to start next wave'
            help_surface = font.render(help_content, True, (255, 255, 255))
            help_rect = help_surface.get_rect(topleft=(400, 10))
        else:
            help_content = ''
            help_surface = font.render(help_content, True, (255, 255, 255))
            help_rect = help_surface.get_rect(topleft=(400, 10))

        screen.blit(cash_surface, cash_rect)
        screen.blit(health_surface, health_rect)
        screen.blit(wave_surface, wave_rect)
        screen.blit(help_surface, help_rect)
        screen.blit(fps_surface, fps_rect)
        pygame.display.flip()
        clock.tick(120)
    else:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        screen.blit(death, (0, 0))
        pygame.display.flip()