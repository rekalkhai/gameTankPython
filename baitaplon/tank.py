import random
from pgzero.builtins import Actor, music, keyboard
import pgzrun

WIDTH = 800
HEIGHT = 600
SIZE_TANK = 25
walls = []
bullets = []
enemy_bullets = []
enemy_direction = []
enemies = []
bullets_holdoff = 0
enemy_bullets_holdoff = 0
enemy_move_count = 0
game_over = False

tank = Actor('tank_blue')
tank.pos = (WIDTH / 2, HEIGHT - SIZE_TANK)
tank.angle = 90

for i in range(5):
    enemy = Actor('tank_red')
    enemy.x = i * 100 + 100
    enemy.y = SIZE_TANK
    enemy.angle = 270
    enemies.append(enemy)
    enemy_direction.append(0)

background = Actor('grass')
lose = Actor('lose')
win = Actor('win')

for x in range(16):
    for y in range(10):
        if random.randint(0, 100) < 50:
            wall = Actor('wall')
            wall.x = x * 50 + SIZE_TANK
            wall.y = y * 50 + SIZE_TANK * 3
            walls.append(wall)


def tank_set(): 
    original_x = tank.x 
    original_y = tank.y
    if keyboard.left:
        tank.x = tank.x - 2
        tank.angle = 180
    elif keyboard.right:
        tank.x = tank.x + 2
        tank.angle = 0
    elif keyboard.up:
        tank.y = tank.y - 2
        tank.angle = 90
    elif keyboard.down:
        tank.y = tank.y + 2
        tank.angle = 270
    if tank.collidelist(walls) != -1:
        tank.x = original_x
        tank.y = original_y

    if tank.x < SIZE_TANK or tank.x > (WIDTH - SIZE_TANK) or tank.y < SIZE_TANK or tank.y > (HEIGHT - SIZE_TANK):
        tank.x = original_x
        tank.y = original_y
    
def tank_bullets_set(): 
    global bullets_holdoff
    if bullets_holdoff == 0:
        if keyboard.space:
            bullet = Actor("bulletblue2")
            bullet.angle = tank.angle
            if bullet.angle == 0:
                bullet.pos = (tank.x + SIZE_TANK, tank.y)
            elif bullet.angle == 180:
                bullet.pos = (tank.x - SIZE_TANK, tank.y)
            elif bullet.angle == 90:
                bullet.pos = (tank.x, tank.y - SIZE_TANK)
            else:
                bullet.pos = (tank.x, tank.y - SIZE_TANK)
            bullets.append(bullet)
            bullets_holdoff = 20
    else:
        bullets_holdoff = bullets_holdoff - 1

    for bullet in bullets:
        if bullet.angle == 0:
            bullet.x += 5
        elif bullet.angle == 180:
            bullet.x -= 5
        elif bullet.angle == 90:
            bullet.y -= 5
        else:
            bullet.y += 5

    for bullet in bullets:
        wall_index =  bullet.collidelist(walls)
        if wall_index != -1:
            new_enemy = Actor('tank_red')
            new_enemy.pos = walls[wall_index].pos
            enemies.append(new_enemy)
            enemy_direction.append(1)
            del walls[wall_index]
            bullets.remove(bullet)
            sounds.gun9.play()
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)

        enemy_index = bullet.collidelist(enemies)
        if enemy_index != -1:
            bullets.remove(bullet)
            del enemies[enemy_index]
            sounds.exp.play()


def enemy_set(): 
    global enemy_move_count, enemy_direction
    global enemy_bullets_holdoff

    for i in range(0, len(enemies)):
        enemy = enemies[i]   
        choice = random.randint(0, 2)
        original_x = enemy.x
        original_y = enemy.y

        if enemy_move_count > 0:
            enemy_move_count -= 1
            if enemy.angle == 0:
                enemy.x += 2
            elif enemy.angle == 180:
                enemy.x -= 2
            elif enemy.angle == 90:
                enemy.y -= 2
            else:
                enemy.y += 2 
            if enemy.x < SIZE_TANK or enemy.x > WIDTH - SIZE_TANK or enemy.y < SIZE_TANK or enemy.y > HEIGHT - SIZE_TANK:
                enemy.x = original_x
                enemy.y = original_y
                enemy_move_count = 0
                enemy_direction[i] = 1
            elif enemy.collidelist(walls) != -1:
                enemy.x = original_x
                enemy.y = original_y
                enemy_move_count = 0
                enemy_direction[i] = 1
                choice = 2
            else:
                for other_enemy in enemies:
                    if other_enemy == enemy:
                        continue
                    else:
                        if enemy.colliderect(other_enemy):
                            enemy.x = original_x
                            enemy.y = original_y
                            enemy_move_count = 0
                            enemy_direction[i] = 1

        if choice == 0:
            enemy_move_count = 30
        elif choice == 1 and enemy_direction[i] == 1:
            enemy.angle = random.randint(0, 3) * 90
            enemy_direction[i] = 0 
        if choice == 2:
            if enemy_bullets_holdoff == 0:
                bullet = Actor('bulletred2')
                bullet.angle = enemy.angle
                if bullet.angle == 0:
                    bullet.pos = (enemy.x + SIZE_TANK, enemy.y)
                elif bullet.angle == 180:
                    bullet.pos = (enemy.x - SIZE_TANK, enemy.y)
                elif bullet.angle == 90:
                    bullet.pos = (enemy.x, enemy.y - SIZE_TANK)
                else:
                    bullet.pos = (enemy.x, enemy.y - SIZE_TANK)
                enemy_bullets.append(bullet)
                enemy_bullets_holdoff = 70
            else:
                enemy_bullets_holdoff -= 1
  
def enemy_bullets_set(): 
    global game_over,enemies
    for bullet in enemy_bullets:
        if bullet.angle == 0:
            bullet.x += 5
        elif bullet.angle == 180:
            bullet.x -= 5
        elif bullet.angle == 90:
            bullet.y -= 5
        else:
            bullet.y += 5
    for bullet in enemy_bullets:
        wall_index =  bullet.collidelist(walls)
        if wall_index != -1:
            del walls[wall_index]
            enemy_bullets.remove(bullet)
            sounds.gun10.play()
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            enemy_bullets.remove(bullet)
        if bullet.colliderect(tank):
            game_over = True
            enemies = []

def  collide():
    global game_over, enemies
    if tank.collidelist(enemies) != -1:
        game_over = True
        enemies = []

def update():
    tank_set()
    tank_bullets_set()
    enemy_set()
    enemy_bullets_set()
    collide()

def draw():
    if game_over:
        lose.draw()
    elif len(enemies) == 0:
        win.draw()
    else:    
        background.draw()
        tank.draw()
        for wall in walls:
            wall.draw()
        for bullet in bullets:
            bullet.draw()
        for enemy in enemies:
            enemy.draw()
        for bullet in enemy_bullets:
            bullet.draw()
pgzrun.go()