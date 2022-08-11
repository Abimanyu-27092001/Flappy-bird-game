from math import fabs, trunc
import pygame
import sys
import random

from pygame.constants import K_SPACE
from pygame.version import PygameVersion
# All variables
bg_x_position = 0
floor_x_position = 0
gravity = 0.2
bird_y_move = 0
score = 0
scoreplay = 0
high_score = 0
# All functions


def bg_move():
    screen.blit(bg_surface, (bg_x_position, 0))
    screen.blit(bg_surface, (bg_x_position+288, 0))


def floor_move():
    screen.blit(floor, (floor_x_position, 450))
    screen.blit(floor, (floor_x_position+288, 450))


def create_pipe():
    random_height = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(288, random_height))
    top_pipe = pipe_surface.get_rect(midbottom=(288, random_height-150))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit.play()
            return False
    if bird_rect.top <= 0:
        hit  .play()
        return False
    elif bird_rect.bottom <= 450:
        return True
    die.play()
    return False


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_y_move*3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(65, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == "main-game":
        score_surface = game_font.render(
            f"Score::{str(int(score))}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)
    if game_state == "game-over":
        score_surface = game_font.render(
            f"Score::{str(int(score))}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(
            f"HighScore::{str(int(high_score))}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(144, 430))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, highscore):
    if score > highscore:
        highscore = score
    return highscore


pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
game_font = pygame.font.Font("HeadlinerNo.45 DEMO.ttf", 40)
game_active = True


bg_surface = pygame.image.load('assets/background-night.png').convert()
floor = pygame.image.load('assets/base.png').convert()
bird_downflap = pygame.image.load(
    'assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird = bird_frames[bird_index]
bird_rect = bird.get_rect(center=(65, 256))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_list = []
SPWANPIPE = pygame.USEREVENT
pygame.time.set_timer(SPWANPIPE, 1300)
pipe_height = [195, 200, 210, 220, 230, 240, 250, 260, 270, 280,
               290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410]
game_over_screen = pygame.image.load('assets/message.png').convert_alpha()
game_over_screen_rect = game_over_screen.get_rect(center=(144, 256))
flap = pygame.mixer.Sound("sound/sfx_wing.wav")
hit = pygame.mixer.Sound("sound/sfx_hit.wav")
point = pygame.mixer.Sound("sound/sfx_point.wav")
die = pygame.mixer.Sound("sound/sfx_die.wav")
pygame.display.set_caption("By Abimanyu")


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and game_active:
                bird_y_move = 0
                bird_y_move = -5
                flap.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (65, 256)
                bird_y_move = 0
                score = 0
        if event.type == SPWANPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index = bird_index+1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    floor_x_position = floor_x_position-1
    bg_x_position = bg_x_position-1

    bg_move()
    if bg_x_position <= -288:
        bg_x_position = 0

    if game_active:
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        bird_y_move += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_y_move
        screen.blit(rotated_bird, bird_rect)

        game_active = check_collision(pipe_list)
        score += 0.01
        scoreplay += 0.01
        if scoreplay >= 1.0:
            point.play()
            scoreplay = 0

        score_display("main-game")
    else:
        screen.blit(game_over_screen, game_over_screen_rect)
        high_score = update_score(score, high_score)
        score_display("game-over")

    floor_move()

    if floor_x_position <= -288:
        floor_x_position = 0

    pygame.display.update()
    clock.tick(120)
