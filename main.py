import pygame
import os
import random

pygame.init()

screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.mixer.music.load(os.path.join("Other", "background_music.mp3"))


# Importing images
running = [pygame.image.load(os.path.join("Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Dino", "DinoRun2.png"))]
jumping = pygame.image.load(os.path.join("Dino", "DinoJump.png"))
ducking = [pygame.image.load(os.path.join("Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Dino", "DinoDuck2.png"))]
small_cactus = [pygame.image.load(os.path.join("Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Cactus", "SmallCactus3.png"))]
large_cactus = [pygame.image.load(os.path.join("Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Cactus", "LargeCactus3.png"))]
bird = [pygame.image.load(os.path.join("Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Bird", "Bird2.png"))]
cloud = pygame.image.load(os.path.join("Other", "Cloud.png"))
BG = pygame.image.load(os.path.join("Other", "Track.png"))


class Dinosaur:
    x_pos = 80
    y_pos = 380
    y_pos_duck = 410
    JUMP_VEL = 9.5

    def __init__(self):
        self.duck_img = ducking
        self.run_img = running
        self.jump_img = jumping

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_jump = True
            self.dino_duck = False
            self.dino_run = False
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos_duck
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
class Cloud:
    def __init__(self):
        self.x = screen_width + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = cloud
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(self.width * 1.5), int(self.height * 1.5)))

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = screen_width + random.randint(500, 1000)
            self.y = random.randint(50, 100)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = screen_width

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 395

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 370

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 320
        self.index = 0

    def draw(self, screen):
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index // 5], self.rect)
        self.index += 1

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    clouds = Cloud()
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 450
    points = 0
    font = pygame.font.Font("myFont.ttf", 15)
    obstacles = []
    death_count = 0

    pygame.mixer.music.play(-1)

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 2

        text = font.render("Score: " + str(points), True, (83, 83, 83))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        screen.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        screen.blit(BG, (x_pos_bg, y_pos_bg))
        screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill("white")
        userInput = pygame.key.get_pressed()

        player.draw(screen)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(small_cactus))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(large_cactus))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(bird))

        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                death_count += 1
                menu(death_count)

        background()

        score()

        clouds.draw(screen)
        clouds.update()

        clock.tick(30)
        pygame.display.update()

def menu(death_count):
    global points
    start_button_img = pygame.image.load(os.path.join("Other", "start.png"))
    restart_button_img = pygame.image.load(os.path.join("Other", "reset.png"))
    font = pygame.font.Font("myFont.ttf", 30)
    pygame.mixer.music.stop()

    run = True
    while run:
        screen.fill((255, 255, 255))

        if death_count > 0:
            game_over_text = font.render("G A M E  O V E R", True, (83, 83, 83))
            game_over_rect = game_over_text.get_rect()
            game_over_rect.center = (screen_width // 2, screen_height // 2 - 100)
            screen.blit(game_over_text, game_over_rect)

            score = font.render("Your Score: " + str(points), True, (83, 83, 83))
            score_rect = score.get_rect()
            score_rect.center = (screen_width // 2, screen_height // 2)
            screen.blit(score, score_rect)

            button_img = restart_button_img
            button_y = screen_height // 2 + 50
        else:
            button_img = start_button_img
            button_y = (screen_height - button_img.get_height()) // 3

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                button_width = button_img.get_width()
                button_height = button_img.get_height()
                button_x = (screen_width - button_width) // 2
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    main()
        screen.blit(button_img, ((screen_width - button_img.get_width()) // 2, button_y))
        pygame.display.update()


menu(death_count=0)
