import pygame

class Player():
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius # 원의 반경
        self.color = color # 원의 색상
        self.center = (x,y) #원의 중심
        self.vel = 3 #이동 증분

    def draw(self, win):
        # 원을 그린다
        pygame.draw.circle(win, self.color, self.center, self.radius)

    def move(self):
        # 방향키에 따라 원의 중심을 이동한다
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.center = (self.x, self.y)