import pygame

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_WIDTH, PLAYER_HEIGHT = 10, 10

# Window and background
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 60
BACKGROUND_IMAGE = pygame.image.load("Assets/png/BG.png").convert()
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_x, bg_y = 0, 0
pygame.init()
pygame.display.set_caption("Platformer")

# Player
PLAYER_STANDING_IMAGE = [pygame.image.load("Assets/player/standing/frame-1.png").convert_alpha(), pygame.image.load("Assets/player/standing/frame-2.png").convert_alpha()]
PLAYER_STANDING = [pygame.transform.scale(PLAYER_STANDING_IMAGE[0], (PLAYER_STANDING_IMAGE[0].get_width()/PLAYER_WIDTH, PLAYER_STANDING_IMAGE[0].get_height()/PLAYER_HEIGHT)), pygame.transform.scale(PLAYER_STANDING_IMAGE[1], (PLAYER_STANDING_IMAGE[1].get_width()/PLAYER_WIDTH, PLAYER_STANDING_IMAGE[1].get_height()/PLAYER_HEIGHT))]

PLAYER_RUNNING_IMAGE = [pygame.image.load("Assets/player/running/frame-1.png").convert_alpha(), pygame.image.load("Assets/player/running/frame-2.png").convert_alpha(), pygame.image.load("Assets/player/running/frame-3.png").convert_alpha(), pygame.image.load("Assets/player/running/frame-4.png").convert_alpha(), pygame.image.load("Assets/player/running/frame-5.png").convert_alpha(), pygame.image.load("Assets/player/running/frame-6.png").convert_alpha()]
PLAYER_RUNNING = [pygame.transform.scale(PLAYER_RUNNING_IMAGE[0], (PLAYER_RUNNING_IMAGE[0].get_width()/PLAYER_WIDTH, PLAYER_RUNNING_IMAGE[0].get_height()/PLAYER_HEIGHT)), pygame.transform.scale(PLAYER_RUNNING_IMAGE[1], (PLAYER_RUNNING_IMAGE[1].get_width()/PLAYER_WIDTH, PLAYER_RUNNING_IMAGE[1].get_height()/PLAYER_HEIGHT)), pygame.transform.scale(PLAYER_RUNNING_IMAGE[2], (PLAYER_RUNNING_IMAGE[2].get_width()/PLAYER_WIDTH, PLAYER_RUNNING_IMAGE[2].get_height()/PLAYER_HEIGHT)), pygame.transform.scale(PLAYER_RUNNING_IMAGE[3], (PLAYER_RUNNING_IMAGE[3].get_width()/PLAYER_WIDTH, PLAYER_RUNNING_IMAGE[3].get_height()/PLAYER_HEIGHT)), pygame.transform.scale(PLAYER_RUNNING_IMAGE[4], (PLAYER_RUNNING_IMAGE[4].get_width()/PLAYER_WIDTH, PLAYER_RUNNING_IMAGE[4].get_height()/PLAYER_HEIGHT)), pygame.transform.scale(PLAYER_RUNNING_IMAGE[5], (PLAYER_RUNNING_IMAGE[5].get_width()/PLAYER_WIDTH, PLAYER_RUNNING_IMAGE[5].get_height()/PLAYER_HEIGHT))]

PLAYER_JUMPING_IMAGE = [pygame.image.load("Assets/player/jump/jump_up.png").convert_alpha(), pygame.image.load("Assets/player/jump/jump_fall.png").convert_alpha()]
PLAYER_JUMPING = [pygame.transform.scale(PLAYER_JUMPING_IMAGE[0], (PLAYER_JUMPING_IMAGE[0].get_width()/PLAYER_WIDTH, PLAYER_JUMPING_IMAGE[0].get_height()/PLAYER_HEIGHT)), pygame.transform.scale(PLAYER_JUMPING_IMAGE[1], (PLAYER_JUMPING_IMAGE[1].get_width()/PLAYER_WIDTH, PLAYER_JUMPING_IMAGE[1].get_height()/PLAYER_HEIGHT))]

class Player(pygame.sprite.Sprite):
    def __init__(self, frames_stand, frames_run, frames_jump, x, y):
        super().__init__()
        self.frames_stand = frames_stand
        self.frames_run = frames_run
        self.frames_jump = frames_jump
        self.image = self.frames_stand[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.frame_index = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
        self.moving_speed = 2
        self.gravity = 1
        self.is_jumping = False
        self.is_falling = False
        self.jump_speed = 13
        self.current_jump_height = 0
        self.y_velocity = 0

    def move_background_left(self):
        global bg_x
        bg_x -= 2
        if bg_x <= -BACKGROUND_IMAGE.get_width():
            bg_x = 0

    def move_background_right(self):
        global bg_x
        bg_x += 2
        if bg_x >= 0:
            bg_x = -BACKGROUND_IMAGE.get_width()

    def update(self):
        # Handle input
        anything_pressed = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            anything_pressed = True
            self.move_right()
            self.move_background_left()
        elif keys[pygame.K_LEFT]:
            anything_pressed = True
            self.move_left()
            self.move_background_right()
        if not anything_pressed:
            self.stand()

        # Handle jumping and falling
        if not self.is_jumping and not self.is_falling:
            if keys[pygame.K_UP]:
                self.is_jumping = True
                self.y_velocity = -self.jump_speed
        elif self.is_jumping:
            self.jump()
        elif self.is_falling:
            self.fall()

    def stand(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed * 60:
            self.animation_timer = 0
            self.frame_index += 1
            if self.frame_index >= len(self.frames_stand):
                self.frame_index = 0
            self.image = self.frames_stand[self.frame_index]
    def run(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed * 60:
            self.animation_timer = 0
            self.frame_index += 1
            if self.frame_index >= len(self.frames_run):
                self.frame_index = 0
            self.image = self.frames_run[self.frame_index]
    def jump(self):
        self.y_velocity += self.gravity
        self.rect.y += self.y_velocity
        self.current_jump_height += abs(self.y_velocity)
        self.image = self.frames_jump[0]
        if self.y_velocity >= 0:
            self.is_jumping = False
            self.is_falling = True
            self.y_velocity = 0
    def fall(self):
        self.y_velocity += self.gravity
        self.rect.y += self.y_velocity
        self.image = self.frames_jump[1]
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.is_falling = False
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.stand()
            self.current_jump_height = 0
            self.y_velocity = 0
    def move_left(self):
        if self.rect.x > 0:
            self.rect.x -= self.moving_speed
        self.run()
    def move_right(self):
        if self.rect.x < (SCREEN_WIDTH - self.rect.width) / 2:
            self.rect.x += self.moving_speed
        self.run()

def main():
    player = Player(PLAYER_STANDING, PLAYER_RUNNING, PLAYER_JUMPING, 50, SCREEN_HEIGHT - PLAYER_STANDING[0].get_height())
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        player.update()
        WINDOW.blit(BACKGROUND_IMAGE, (bg_x, bg_y))
        WINDOW.blit(BACKGROUND_IMAGE, (bg_x + BACKGROUND_IMAGE.get_width(), bg_y))
        WINDOW.blit(player.image, (player.rect.x, player.rect.y))
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()

