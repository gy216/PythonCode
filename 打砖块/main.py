import pygame
import random
import sys
import os

# 隐藏 Pygame 欢迎消息
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

# 初始化 pygame
pygame.init()

# 游戏配置
WIDTH = 600
HEIGHT = 500
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_RADIUS = 8
BRICK_ROWS = 5
BRICK_COLS = 8
BRICK_WIDTH = (WIDTH - 100) // BRICK_COLS
BRICK_HEIGHT = 25

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (255, 80, 80)
GREEN = (80, 255, 80)
YELLOW = (255, 255, 80)
ORANGE = (255, 165, 80)
PURPLE = (180, 80, 255)

# 砖块颜色列表
BRICK_COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE]

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("打砖块游戏")

# 时钟
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# 挡板类
class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = (WIDTH - self.width) // 2
        self.y = HEIGHT - 40
        self.speed = 8
    
    def move(self, direction):
        if direction == 'left' and self.x > 0:
            self.x -= self.speed
        elif direction == 'right' and self.x < WIDTH - self.width:
            self.x += self.speed
    
    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 2)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# 球类
class Ball:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 60
        self.radius = BALL_RADIUS
        self.speed_x = random.choice([-4, -3, 3, 4])
        self.speed_y = -5
    
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        # 墙壁碰撞
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.speed_x *= -1
        if self.y - self.radius < 0:
            self.speed_y *= -1
    
    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

# 砖块类
class Brick:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.color = color
        self.alive = True
    
    def draw(self):
        if self.alive:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 1)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# 游戏类
class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = []
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.win = False
        self.create_bricks()
    
    def create_bricks(self):
        self.bricks = []
        start_x = 50
        start_y = 60
        
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = start_x + col * (BRICK_WIDTH + 5)
                y = start_y + row * (BRICK_HEIGHT + 5)
                color = BRICK_COLORS[row % len(BRICK_COLORS)]
                self.bricks.append(Brick(x, y, color))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_over or self.win:
                    if event.key == pygame.K_SPACE:
                        self.reset()
                    elif event.key == pygame.K_ESCAPE:
                        return False
        
        # 持续按键检测
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.move('left')
        if keys[pygame.K_RIGHT]:
            self.paddle.move('right')
        
        return True
    
    def check_collisions(self):
        ball_rect = self.ball.get_rect()
        paddle_rect = self.paddle.get_rect()
        
        # 球与挡板碰撞
        if ball_rect.colliderect(paddle_rect) and self.ball.speed_y > 0:
            # 根据击打位置改变角度
            hit_pos = (self.ball.x - self.paddle.x) / self.paddle.width
            self.ball.speed_x = 8 * (hit_pos - 0.5)
            self.ball.speed_y *= -1
        
        # 球与砖块碰撞
        for brick in self.bricks:
            if brick.alive and ball_rect.colliderect(brick.get_rect()):
                brick.alive = False
                self.ball.speed_y *= -1
                self.score += 10
                break
        
        # 球掉落
        if self.ball.y > HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.ball.reset()
        
        # 检查胜利
        if all(not brick.alive for brick in self.bricks):
            self.win = True
    
    def update(self):
        if not self.game_over and not self.win:
            self.ball.move()
            self.check_collisions()
    
    def draw(self):
        screen.fill(BLACK)
        
        # 绘制游戏元素
        for brick in self.bricks:
            brick.draw()
        
        self.paddle.draw()
        self.ball.draw()
        
        # 绘制分数和生命
        score_text = small_font.render(f"分数: {self.score}", True, WHITE)
        lives_text = small_font.render(f"生命: {self.lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 100, 10))
        
        # 游戏结束或胜利提示
        if self.game_over:
            game_over_text = font.render("游戏结束!", True, RED)
            restart_text = small_font.render("按空格键重新开始，ESC退出", True, WHITE)
            
            game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            
            screen.blit(game_over_text, game_over_rect)
            screen.blit(restart_text, restart_rect)
        elif self.win:
            win_text = font.render("恭喜通关!", True, GREEN)
            restart_text = small_font.render("按空格键重新开始，ESC退出", True, WHITE)
            
            win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            
            screen.blit(win_text, win_rect)
            screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def reset(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.win = False
        self.create_bricks()
    
    def run(self):
        while True:
            if not self.handle_events():
                break
            
            self.update()
            self.draw()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

# 主程序
if __name__ == "__main__":
    game = Game()
    game.run()
