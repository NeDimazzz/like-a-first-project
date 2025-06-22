import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 15
PADDLE_SPEED = 7
INITIAL_BALL_SPEED = 5


class Paddle:
    """Класс для представления ракетки в игре Pong."""

    def __init__(self, x, y):
        self.rect = pygame.Rect(int(x), int(y), PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED
        self.score = 0

    def move(self, direction):
        """Перемещает ракетку в заданном направлении (1 - вниз, -1 - вверх)"""
        new_y = self.rect.y + direction * self.speed
        # Ограничение движения ракетки в пределах экрана
        self.rect.y = int(max(0, min(new_y, SCREEN_HEIGHT - PADDLE_HEIGHT)))

    def draw(self, surface):
        """Отрисовывает ракетку на поверхности"""
        pygame.draw.rect(surface, WHITE, self.rect)


class Ball:
    """Класс для представления мяча в игре Pong."""

    def __init__(self):
        self.reset()
        self.size = BALL_SIZE

    def move(self):
        """Перемещает мяч согласно его текущей скорости"""
        self.rect.x = int(self.rect.x + self.dx)
        self.rect.y = int(self.rect.y + self.dy)

        # Отскок от верхней и нижней границы
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.dy *= -1

    def collide_with_paddle(self, paddle):
        """Обрабатывает столкновение с ракеткой"""
        if self.rect.colliderect(paddle.rect):
            # Определяем точку удара относительно центра ракетки
            relative_intersect_y = (paddle.rect.centery - self.rect.centery)
            normalized_relative_intersect_y = relative_intersect_y / (PADDLE_HEIGHT / 2)

            # Угол отскока зависит от точки удара
            bounce_angle = normalized_relative_intersect_y * (math.pi / 4)

            # Увеличиваем скорость после каждого удара
            speed = max(INITIAL_BALL_SPEED, math.hypot(self.dx, self.dy) * 1.05)

            # Определяем направление (влево или вправо)
            direction = -1 if self.dx > 0 else 1

            self.dx = direction * speed * math.cos(bounce_angle)
            self.dy = -speed * math.sin(bounce_angle)

    def reset(self):
        """Сбрасывает мяч в центр экрана со случайным направлением"""
        self.rect = pygame.Rect(
            int(SCREEN_WIDTH // 2 - BALL_SIZE // 2),
            int(SCREEN_HEIGHT // 2 - BALL_SIZE // 2),
            BALL_SIZE,
            BALL_SIZE
        )
        self.dx = INITIAL_BALL_SPEED * random.choice((1, -1))
        self.dy = INITIAL_BALL_SPEED * random.choice((1, -1))

    def draw(self, surface):
        """Отрисовывает мяч на поверхности"""
        pygame.draw.rect(surface, WHITE, self.rect)


class Game:
    """Основной класс игры, управляющий всеми компонентами."""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong (ООП реализация)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

        # Создаем игровые объекты
        self.player = Paddle(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.opponent = Paddle(
            SCREEN_WIDTH - 30 - PADDLE_WIDTH,
            SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        )
        self.ball = Ball()

        # Настройки игры
        self.game_active = False
        self.winning_score = 5

    def handle_events(self):
        """Обрабатывает события игры"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_active:
                    self.game_active = True
                if event.key == pygame.K_ESCAPE:
                    self.game_active = False
                    self.reset_game()

        return True

    def reset_game(self):
        """Сбрасывает состояние игры к начальному"""
        self.player.score = 0
        self.opponent.score = 0
        self.ball.reset()
        self.player.rect.y = int(SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.opponent.rect.y = int(SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)

    def update(self):
        """Обновляет состояние игры"""
        if not self.game_active:
            return

        # Движение мяча
        self.ball.move()

        # Обработка столкновений с ракетками
        self.ball.collide_with_paddle(self.player)
        self.ball.collide_with_paddle(self.opponent)

        # Проверка выхода мяча за границы
        if self.ball.rect.left <= 0:
            self.opponent.score += 1
            self.ball.reset()
            self.game_active = False if self.opponent.score >= self.winning_score else True

        if self.ball.rect.right >= SCREEN_WIDTH:
            self.player.score += 1
            self.ball.reset()
            self.game_active = False if self.player.score >= self.winning_score else True

        # Простое ИИ для противника
        if self.ball.rect.centery < self.opponent.rect.centery:
            self.opponent.move(-1)
        elif self.ball.rect.centery > self.opponent.rect.centery:
            self.opponent.move(1)

        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player.move(-1)
        if keys[pygame.K_DOWN]:
            self.player.move(1)

    def draw(self):
        """Отрисовывает все игровые объекты"""
        self.screen.fill(BLACK)

        # Отрисовка центральной линии
        pygame.draw.aaline(
            self.screen, WHITE,
            (SCREEN_WIDTH // 2, 0),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT)
        )

        # Отрисовка ракеток и мяча
        self.player.draw(self.screen)
        self.opponent.draw(self.screen)
        self.ball.draw(self.screen)

        # Отрисовка счета
        player_score = self.font.render(str(self.player.score), True, WHITE)
        opponent_score = self.font.render(str(self.opponent.score), True, WHITE)
        self.screen.blit(player_score, (SCREEN_WIDTH // 4, 20))
        self.screen.blit(opponent_score, (3 * SCREEN_WIDTH // 4, 20))

        # Сообщения
        if not self.game_active:
            if self.player.score >= self.winning_score:
                message = self.font.render("You Win!", True, WHITE)
            elif self.opponent.score >= self.winning_score:
                message = self.font.render("You Lose!", True, WHITE)
            else:
                message = self.small_font.render("Press SPACE to start", True, WHITE)

            self.screen.blit(
                message,
                (SCREEN_WIDTH // 2 - message.get_width() // 2,
                 SCREEN_HEIGHT // 2 - message.get_height() // 2)
            )

        pygame.display.flip()

    def run(self):
        """Главный игровой цикл"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()