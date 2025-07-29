import time
from typing import Optional, Union

import pygame
import random

pygame.init()

#loading sfx and fonts
p1_hit = pygame.mixer.Sound('sound2.wav')
p2_hit = pygame.mixer.Sound('sound1.wav')
ball_out = pygame.mixer.Sound('sound6.wav')
font_78 = pygame.font.Font('PressStart2P-vaV7.ttf', 78)
font_36 = pygame.font.Font('PressStart2P-vaV7.ttf', 36)
font_28 = pygame.font.Font('PressStart2P-vaV7.ttf', 28)

#constants
WIDTH = 1280
HEIGHT = 720
BG_COLOUR = (0, 0, 0)
OBJ_COLOUR = (255, 255, 255)
SELECT_COLOUR = (225, 225, 225)

class Ball:
    """
    A ball within a game of Pong.

    Attributes:
    radius: the radius of this <Ball>
    hitbpx: the hitbox of this <Ball>
    speed_factor: the factor <speed> is multiplied by
    speed: the speed of this <Ball>
    """
    radius: int
    hitbox: pygame.Rect
    speed_factor = float
    speed: list[float]

    def __init__(self, radius: int) -> None:
        self.hitbox = pygame.Rect((WIDTH - radius * 2) / 2, (HEIGHT - radius * 2) / 2, radius * 2, radius * 2)
        self.radius = radius
        self.speed = [8.0, 8.0]

    def draw(self, colour) -> None:
        pygame.draw.circle(screen, colour, self.hitbox.center, self.radius)

    def inc_speed(self) -> None:
        self.speed[0] *= 1.03
        self.speed[1] *= 1.03

    def move(self) -> None:
        self.hitbox.x += self.speed[0]
        self.hitbox.y += self.speed[1]

    def reset(self) -> None:
        self.hitbox.x = (WIDTH - self.radius * 2) / 2
        self.hitbox.y = (HEIGHT - self.radius * 2) / 2
        new_speed = 8 * random.choice((1, -1))
        self.speed[0], self.speed[1] = new_speed, new_speed

class Player:
    """
    A general class for a <Player> object within Pong.
    This class is not meant to be accessed directly.

    Attributes:
    hitbpx: the hitbox of this player's paddle
    score: this player's score
    """

    hitbox: Optional[pygame.Rect]
    score: int

    def __init__(self, width, height) -> None:
        """
        Creates a new <Player> with a score of 0.
        """
        self.score = 0
        self.hitbox = None


    def draw_paddle(self, screen, colour) -> None:
        """
        Visually draws this <Player> object's paddle
        onto <screen>
        """
        pygame.draw.rect(screen, colour, self.hitbox)

    def move(self) -> None:
        """
        Defines the movement for the movement for the
        paddle of this <Player>.
        """
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

class Player1(Player):
    """
    Player 1 of this game. This class is a subclass
    of <Player>, sharing the same attributes.
    """

    def __init__(self, width, height) -> None:
        """
        Creates a new <Player> with a score of 0, and
        a hitbox with <width> and <height> both adjusted
        according to the paddle's initial position on the
        screen.
        """
        Player.__init__(self, width, height)
        self.hitbox = pygame.Rect(0, (HEIGHT - height) / 2, width, height)

    def move(self) -> None:
        """
        Defines the movement for the movement for the
        paddle of this <Player>.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.hitbox.top > -self.hitbox.height:
            self.hitbox.y -= 15
        if keys[pygame.K_s] and self.hitbox.bottom < HEIGHT + self.hitbox.height:
            self.hitbox.y += 15

    def reset(self) -> None:
        self.hitbox.x = 0
        self.hitbox.y = (HEIGHT - self.hitbox.height) / 2

class Player2(Player):
    """
    Player 2 of this game. This class is a subclass
    of <Player>, sharing the same attributes.
    """

    def __init__(self, width, height) -> None:
        """
        Creates a new <Player> with a score of 0, and
        a hitbox with <width> and <height> both adjusted
        according to the paddle's initial position on the
        screen.
        """
        Player.__init__(self, width, height)
        self.hitbox = pygame.Rect(WIDTH - width, (HEIGHT - height) / 2, width, height)

    def move(self) -> None:
        """
        Defines the movement for the movement for the
        paddle of this <Player>.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.hitbox.top > -self.hitbox.height:
            self.hitbox.y -= 15
        if keys[pygame.K_DOWN] and self.hitbox.bottom < HEIGHT + self.hitbox.height:
            self.hitbox.y += 15

    def reset(self) -> None:
        self.hitbox.x = WIDTH - self.hitbox.width
        self.hitbox.y = (HEIGHT - self.hitbox.height) / 2

class AIPlayer(Player2):
    """
    A second AI player within this game. This class is a subclass
    of <Player2>, sharing the same attributes.

    Attributes:
    speed: the speed that the paddle of this <Player> moves at
    """
    speed: float

    def __init__(self, width, height) -> None:
        """
        Creates a new <Player> with a score of 0, and
        a hitbox with <width> and <height> both adjusted
        according to the paddle's initial position on the
        screen.
        """
        Player2.__init__(self, width, height)
        self.speed = 8

    def move(self, ball: Ball) -> None:
        """
        Defines the movement for the movement for the
        paddle of this <Player>.
        """
        self.speed = random.uniform(7.0, 8.0)

        if ball.speed[0] > 0:
            if self.hitbox.bottom and self.hitbox.top < ball.hitbox.top:
                self.hitbox.y += self.speed
            elif self.hitbox.top and self.hitbox.bottom > ball.hitbox.bottom:
                self.hitbox.y -= self.speed

        elif ball.speed[0] < 0:
            if self.hitbox.y < (HEIGHT - self.hitbox.height) / 2:
                self.hitbox.y += self.speed
            if self.hitbox.y > (HEIGHT - self.hitbox.height) / 2:
                self.hitbox.y -= self.speed

    def inc_speed(self):
        self.speed *= 1.03


def menu_select() -> None:
    global start_1, start_2, menu

    click = pygame.mouse.get_pressed()

    p1_colour = OBJ_COLOUR
    p2_colour = OBJ_COLOUR
    p1_select = font_28.render('1 Player', True, p1_colour)
    p2_select = font_28.render('2 Player', True, p2_colour)
    p1_pos = ((WIDTH - p1_select.get_rect().width) / 2, 500)
    p2_pos = ((WIDTH - p2_select.get_rect().width) / 2, 600)

    if p1_select.get_rect(topleft = p1_pos).collidepoint((pygame.mouse.get_pos())):
        p1_colour = SELECT_COLOUR
        if click[0]:
            start_1 = True
            menu = False
    if p2_select.get_rect(topleft = p2_pos).collidepoint(pygame.mouse.get_pos()):
        p2_colour = SELECT_COLOUR
        if click[0]:
            start_2 = True
            menu = False

    title = font_78.render('PONG', True, OBJ_COLOUR)
    p1_select = font_28.render('1 Player', True, p1_colour)
    p2_select = font_28.render('2 Player', True, p2_colour)
    screen.blit(title, ((WIDTH - title.get_rect().width) / 2, 250))
    screen.blit(p1_select, (p1_pos))
    screen.blit(p2_select, (p2_pos))


def scoreboard(screen: pygame.display, p1: Player1, p2: Union[Player2, AIPlayer]) -> None:
    p1_score_board = font_36.render(str(p1.score), True, OBJ_COLOUR)
    screen.blit(p1_score_board, (0, 0))
    p2_score_board = font_36.render(str(p2.score), True, OBJ_COLOUR)
    screen.blit(p2_score_board, (WIDTH - p2_score_board.get_rect().width, 0))


def draw(screen: pygame.display, p1: Player1, p2: Union[Player2, AIPlayer], ball: Ball) -> None:
    count = 0
    for i in range(36):
        if i % 2 == 0:
            pygame.draw.rect(screen, OBJ_COLOUR, ((WIDTH - 15)/2, 9 + count, 15, 20))
        count += 20
    p1.draw_paddle(screen, OBJ_COLOUR)
    p2.draw_paddle(screen, OBJ_COLOUR)
    ball.draw(OBJ_COLOUR)


def check_collision(p1: Player1, p2: Union[Player2, AIPlayer], ball: Ball) -> str:
    last_touched = ''

    if ball.speed[0] > 0:
        last_touched = 'p1'
        if p2.hitbox.colliderect(ball.hitbox):
            p2_hit.play()
            ball.speed[0] *= -1
            ball.inc_speed()
            if isinstance(p2, AIPlayer):
                p2.inc_speed()
    elif ball.speed[0] < 0:
        last_touched = 'p2'
        if p1.hitbox.colliderect(ball.hitbox):
            p1_hit.play()
            ball.speed[0] *= -1
            ball.inc_speed()
            if isinstance(p2, AIPlayer):
                p2.inc_speed()

    return last_touched

def update_score(p1: Player1, p2: Union[Player2], last_touched: str) -> None:
    if last_touched == 'p1':
        p1.score += 1
    elif last_touched == 'p2':
        p2.score += 1

def reset(p1: Player1, p2: Union[Player2, AIPlayer], ball: Ball, last_touched: str) -> None:
    p1.reset()
    p2.reset()
    ball.reset()
    clock.tick(6)
    update_score(p1, p2, last_touched)

def ball_animation(ball) -> None:
    last_touched = check_collision(p1, p2, ball)

    if ball.hitbox.top <= 0 or ball.hitbox.bottom >= HEIGHT:
        ball.speed[1] *= -1
    if ball.hitbox.left < 0 - ball.hitbox.width or ball.hitbox.right > WIDTH + ball.hitbox.width:
        reset(p1, p2, ball, last_touched)

def pause_menu(screen: pygame.display) -> None:
    global menu, start_1, start_2, paused

    pygame.mouse.set_visible(True)
    blur_layer = pygame.Surface((WIDTH, HEIGHT))
    blur_layer.set_alpha(128)
    blur_layer.fill(BG_COLOUR)
    screen.blit(blur_layer, (0, 0))

    click = pygame.mouse.get_pressed()

    p1_colour = OBJ_COLOUR
    p2_colour = OBJ_COLOUR
    p1_select = font_28.render('Return To Menu', True, p1_colour)
    p2_select = font_28.render('Continue', True, p2_colour)
    p1_pos = ((WIDTH - p1_select.get_rect().width) / 2, 500)
    p2_pos = ((WIDTH - p2_select.get_rect().width) / 2, 600)

    if p1_select.get_rect(topleft=p1_pos).collidepoint((pygame.mouse.get_pos())):
        p1_colour = SELECT_COLOUR
        if click[0]:
            start_1 = False
            start_2 = False
            paused = False
            menu = True
            time.sleep(0.25)

    if p2_select.get_rect(topleft=p2_pos).collidepoint(pygame.mouse.get_pos()):
        p2_colour = SELECT_COLOUR
        if click[0]:
            paused = False

    title = font_78.render('PAUSED', True, OBJ_COLOUR)
    p1_select = font_28.render('Return To Menu', True, p1_colour)
    p2_select = font_28.render('Continue', True, p2_colour)
    screen.blit(title, ((WIDTH - title.get_rect().width) / 2, 250))
    screen.blit(p1_select, (p1_pos))
    screen.blit(p2_select, (p2_pos))

if __name__ == '__main__':
    running = True
    menu = True
    start_1 = False
    start_2 = False
    paused = False
    while running:

        #Quitting the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        pygame.mouse.set_visible(True)
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('PONG')
        screen.fill(BG_COLOUR)
        clock = pygame.time.Clock()
        pygame.display.flip()
        clock.tick(60)

        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

            screen.fill(BG_COLOUR)
            menu_select()

            pygame.display.flip()
            clock.tick(60)

        if start_1:
            p1 = Player1(50, 250)
            p2 = AIPlayer(50, 250)
            ball = Ball(30)

            while start_1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            freeze_frame = screen.copy()
                            paused = not paused

                if paused:
                    screen.blit(freeze_frame, (0, 0))
                    pause_menu(screen)

                else:
                    screen.fill(BG_COLOUR)
                    pygame.mouse.set_visible(False)
                    p1.move()
                    p2.move(ball)
                    ball_animation(ball)
                    ball.move()

                    scoreboard(screen, p1, p2)
                    draw(screen, p1, p2, ball)

                pygame.display.flip()
                clock.tick(60)

        if start_2:
            p1 = Player1(50, 250)
            p2 = Player2(50, 250)
            ball = Ball(30)

            while start_2:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            freeze_frame = screen.copy()
                            paused = not paused

                if paused:
                    screen.blit(freeze_frame, (0, 0))
                    pause_menu(screen)

                else:
                    screen.fill(BG_COLOUR)
                    pygame.mouse.set_visible(False)
                    p1.move()
                    p2.move()
                    ball_animation(ball)
                    ball.move()

                    scoreboard(screen, p1, p2)
                    draw(screen, p1, p2, ball)

                pygame.display.flip()
                clock.tick(60)

    pygame.quit()
