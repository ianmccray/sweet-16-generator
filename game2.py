#Some notes: after collecting 50 coins, the game gets faster. Collect 100 and 130, and the game gets even faster.
#Try to get a 'Flawless' game -- getting 130 coins without going below 100 health!

import pygame
import gamebox
import random
camera = gamebox.Camera(400, 400)

randsize = random.randrange(30,60)
print(randsize)
platforms = [
    gamebox.from_color(camera.x, camera.bottom, 'dark green', camera.right+10, 40)
]

rain = [
    gamebox.from_color(camera.left + 100, camera.top, 'red', 10, 10),
    gamebox.from_color(camera.left + 200, camera.top, 'red', 10, 10),
    gamebox.from_color(camera.left + 300, camera.top, 'red', 10, 10)
]

healthplus = [gamebox.from_image(camera.right + 1000, camera.top + 300, 'plus.png')]
healthplus[0].size = 15, 15
music = gamebox.load_sound("savantsplinter.wav")

box = gamebox.from_text(40, 200, "HE", "Arial", 35, "red")

lava = gamebox.from_color(camera.x, camera.bottom, 'red', randsize, 40)
coins = [
    gamebox.from_image(random.randrange(camera.right+100, camera.right+300), random.randrange(220, 300), "coin.png"),
    gamebox.from_image(random.randrange(camera.right+100, camera.right+300), random.randrange(220, 300), "coin.png"),
    gamebox.from_image(random.randrange(camera.right+100, camera.right+300), random.randrange(220, 300), "coin.png")
]

sheet = gamebox.load_sprite_sheet("https://highergroundz.files.wordpress.com/2012/07/runningman2.png", 2, 5)
print(sheet)

coins_got = 0

show_splash = True
ticks = 0

musicplayer0 = music.play(-1)
def splash(keys):
    global show_splash, ticks
    camera.clear('red')
    text = gamebox.from_text(camera.x, camera.y, "ACID RAIN RUN", "Arial", 20, 'black')
    camera.draw(text)
    directions = gamebox.from_text(camera.x, camera.y, "Press space to continue", "Arial", 10, 'black')
    controls = gamebox.from_text(camera.x, camera.y, 'Up arrow to jump; Right arrow to run forward; Left to run backward', 'Arial', 10, 'black')
    instructions = gamebox.from_text(camera.x, camera.y, 'Avoid the rain and puddles, keep running and collect coins!', 'Arial', 10, 'black')
    names = gamebox.from_text(camera.x, camera.y,
                                 'Made by Ian McCray (im3vy) and Lata Goudel (lg3dy)', 'Arial', 10,
                                 'black')
    instructions.top = text.bottom + 20
    controls.top = instructions.bottom + 10
    directions.top = controls.bottom + 20
    names.top = directions.bottom + 10
    camera.draw(controls)
    camera.draw(directions)
    camera.draw(instructions)
    camera.draw(names)


    if pygame.K_SPACE in keys:
        show_splash = False
    if ticks > 600:
        show_splash = False
    camera.display()



def tick(keys):

    global ticks, coins_got,coins, lives
    on_ground = False
    ticks += 1

    if show_splash:
        splash(keys)
        return

    if lava.right < camera.left:
        lava.x = camera.right+50
        lava.size = [random.randrange(30,100), 40]

    camera.clear('grey')

    for coin in coins:
        coin.size = 20, 20
        camera.draw(coin)
        if coin.right < camera.left:
            coin.x = random.randrange(camera.right+100, camera.right+300)
            coin.y = random.randrange(220, 300)
        if coin.touches(box):
            coins.remove(coin)
            x = gamebox.from_image(random.randrange(camera.right+100, camera.right+300), random.randrange(220, 300), "coin.png")
            x.size = 20, 20
            coins.append(x)
            coins_got += 1

    time = gamebox.from_text(0,0, str(ticks//60), 'Arial', 24, 'black')
    num_coins = gamebox.from_text(camera.left + 60, 10, 'Coins: '+ str(coins_got), 'Arial', 24, 'black')
    time.top = camera.top
    time.right = camera.right
    camera.draw(time)

    health = gamebox.from_text(5, 0, 'Health: ' + str(lives), 'Arial', 24, 'black')
    health.top = time.bottom
    health.left = camera.left
    camera.draw(health)

    for healths in healthplus:
        camera.draw(healths)
        if healths.right < camera.left:
            healths.x = camera.right + 3000
            healths.y = random.randint(200, 350)
        if box.touches(healths):
            healthplus.remove(healths)
            newhealth = gamebox.from_image(camera.right + 3000, random.randrange(220, 300), "plus.png")
            newhealth.size = 15, 15
            healthplus.append(newhealth)
            lives += 10

    for platform in platforms:
        camera.draw(platform)
        camera.draw(lava)
        if box.touches(platform):
            box.move_to_stop_overlapping(platform)
        if box.bottom_touches(platform):
            on_ground = True
        if platform.right < camera.right+10:
            platform.right += 10


    for rains in rain:
        camera.draw(rains)
        if(coins_got < 100):
            rains.y += 6
        else:
            rains.y += 8
        if rains.y > 500:
            rains.y = -random.randint(50,150)
            rains.x = random.randint(camera.left + 200, camera.right + 200)
            camera.draw(rains)
        if box.touches(rains):
            lives -= 1
            if lives <= 0:
                text3 = gamebox.from_text(camera.x, camera.y, "You died", "Arial", 20, 'black')
                text4 = gamebox.from_text(camera.x, camera.y,
                                      "You lasted: " + str(ticks//60) + " seconds with " + str(coins_got) + " coins!",
                                      "Arial", 20, 'black')
                text4.top = text3.bottom
                camera.draw(text3)
                camera.draw(text4)
                gamebox.pause()
                camera.display()

    box.image = sheet[0]
    
    if pygame.K_UP in keys and on_ground:
        box.speedy = -28
    if pygame.K_RIGHT in keys:
        #box.x += 8
        box.image = sheet[(ticks // 3) % len(sheet)]
        box.x += 8
    if pygame.K_LEFT in keys:
        #box.x -= 5
        box.image = sheet[(ticks // 3) % len(sheet)]
        box.x -= 5

    box.speedy += 1


    box.speedx *= 0.95
    box.speedy *= 0.95

    box.speedy += 1

    box.move_speed()
    if(coins_got < 50):
        camera.move(3, 0)
    if(coins_got < 100 and coins_got >= 50):
        camera.move(5, 0)
    if (coins_got >= 100 and coins_got < 130):
        camera.move(6, 0)
    if (coins_got >= 130):
        camera.move(7, 0)

    camera.draw(box)
    camera.draw(num_coins)
    camera.display()

    if box.touches(lava):
        lives -= 1
        if lives <= 0:
            text3 = gamebox.from_text(camera.x, camera.y, "You died", "Arial", 20, 'black')
            text4 = gamebox.from_text(camera.x, camera.y,
                                      "You lasted: " + str(ticks//60) + " seconds with " + str(coins_got) + " coins!",
                                      "Arial", 20, 'black')
            text4.top = text3.bottom
            camera.draw(text3)
            camera.draw(text4)
            gamebox.pause()
            camera.display()

    if box.right < camera.left or box.left > camera.right:
        text3 = gamebox.from_text(camera.x, camera.y, "You died", "Arial", 20, 'black')
        text4 = gamebox.from_text(camera.x, camera.y,
                                  "You lasted: " + str(ticks // 60) + " seconds with " + str(coins_got) + " coins!",
                                  "Arial", 20, 'black')
        text4.top = text3.bottom
        camera.draw(text3)
        camera.draw(text4)
        gamebox.pause()
        camera.display()

lives = 100
gamebox.timer_loop(60, tick)