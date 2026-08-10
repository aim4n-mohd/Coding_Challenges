import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 1150, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)

class Paddle:
    def __init__(self, x, y, color, velocity, side):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.score = 0
        self.side = side

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 12, 80), border_radius=5)
        self.text = font.render(str(self.score), True, self.color)
        screen.blit(self.text, (self.side, 50))

class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = WIDTH/2
        self.y = random.randint(25, HEIGHT-25)
        self.radius = 10
        self.angle = random.choice([random.randint(-45, 45), random.randint(135, 225)])
        self.velocity = 400

    def flipX(self):
        self.angle = 180-self.angle
        self.angle += random.randint(-5,5)
        self.angle %= 360

    def update(self, dt):
        if self.y<20 or self.y>HEIGHT-20:
            self.angle = -self.angle
        self.angle %= 360
        self.velocity += 10 * dt
        print(self.velocity)
        self.velocity = min(self.velocity, 900)
        self.x += math.cos(math.radians(self.angle)) * self.velocity * dt
        self.y += math.sin(math.radians(self.angle)) * self.velocity * dt

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)

        

def drawBox():
    pygame.draw.rect(screen, WHITE, (10, 10, WIDTH-20, HEIGHT-20), 2, 30)
    pygame.draw.line(screen, WHITE, (WIDTH/2, 10), (WIDTH/2, HEIGHT-10.5), 2)



def main():
    player = Paddle(25, HEIGHT/2, BLUE, 500, WIDTH/4)
    computer = Paddle(WIDTH-25-12, HEIGHT/2, RED, 250, 3*WIDTH/4)
    ball = Ball()
    lastTime = 0
    target = ball.y

    running = True
    while running:
        dt = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys =  pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.y > 20:
            player.y -= player.velocity * dt
        if keys[pygame.K_DOWN] and player.y+80 < HEIGHT-20:
            player.y += player.velocity * dt

        if ball.x<20:
            computer.score+=1
            ball.reset()
        if ball.x>WIDTH-20:
            ball.reset()
            player.score+=1

        if (ball.x-ball.radius<=player.x+12) and (player.y <= ball.y <= player.y+80) and math.cos(math.radians(ball.angle))<0:
            ball.flipX()
        if (ball.x+ball.radius>=computer.x) and (computer.y <= ball.y <= computer.y+80) and math.cos(math.radians(ball.angle))>0:
            ball.flipX()

        center = computer.y+40
        if (math.cos(math.radians(ball.angle))>0):
            nowTime = pygame.time.get_ticks()
            deltaTime = nowTime - lastTime
            if deltaTime>200:
                target = ball.y + random.randint(-10,10)
                lastTime = nowTime
            if target<center-25:
                computer.y -= computer.velocity*dt
            if target>center+25:
                computer.y += computer.velocity*dt
            computer.y = max(20, min(computer.y, HEIGHT-20-80))
        else:
            target = HEIGHT/2
            if target<center-25:
                computer.y -= computer.velocity*dt
            if target>center+25:
                computer.y += computer.velocity*dt
            computer.y = max(20, min(computer.y, HEIGHT-20-80))

        screen.fill(BLACK)
        drawBox()
        player.draw()
        computer.draw()
        ball.update(dt)
        ball.draw()
        pygame.display.update()

if __name__ == "__main__":
    main()
pygame.quit()