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
HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇游戏")

# 时钟
clock = pygame.time.Clock()

# 蛇类
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # 向右移动
        self.grow = False
    
    def move(self):
        # 计算新的头部位置
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x) % GRID_WIDTH, (head_y + dir_y) % GRID_HEIGHT)
        
        # 检查是否撞到自己
        if new_head in self.body:
            return False
        
        # 移动蛇
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        
        return True
    
    def change_direction(self, new_direction):
        # 不能反向移动
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def draw(self):
        for segment in self.body:
            rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, GREEN, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
    
    def check_collision(self, food):
        return self.body[0] == food.position
    
    def eat(self):
        self.grow = True

# 食物类
class Food:
    def __init__(self):
        self.position = self.random_position()
    
    def random_position(self):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return (x, y)
    
    def draw(self):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, RED, rect)

# 游戏类
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                else:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
        return True
    
    def update(self):
        if not self.game_over:
            if not self.snake.move():
                self.game_over = True
            
            if self.snake.check_collision(self.food):
                self.snake.eat()
                self.score += 1
                self.food = Food()
                # 确保食物不会生成在蛇身上
                while self.food.position in self.snake.body:
                    self.food = Food()
    
    def draw(self):
        screen.fill(BLACK)
        
        # 绘制网格（可选）
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (20, 20, 20), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, (20, 20, 20), (0, y), (WIDTH, y))
        
        # 绘制食物和蛇
        self.food.draw()
        self.snake.draw()
        
        # 显示分数
        score_text = self.small_font.render(f"分数: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # 游戏结束提示
        if self.game_over:
            game_over_text = self.font.render("游戏结束!", True, RED)
            restart_text = self.small_font.render("按空格键重新开始，ESC退出", True, WHITE)
            
            game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            
            screen.blit(game_over_text, game_over_rect)
            screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def reset(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
    
    def run(self):
        while True:
            if not self.handle_events():
                break
            
            self.update()
            self.draw()
            clock.tick(10)  # 控制游戏速度
        
        pygame.quit()
        sys.exit()

# 主程序
if __name__ == "__main__":
    game = Game()
    game.run()
