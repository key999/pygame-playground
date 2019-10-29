#!/usr/bin/env python3

# A simple game without purpose (yet)
# version 0.1.1
# author: key999
# exit codes:
# 0 - correct exit
# anything else i will add here, i.e. -1 something

import pygame
import objects as obj
import menu


class Game:
    def __init__(self):
        self.running = True
        self.screen = None
        self.size = self.width, self.height = 1024, 768
        self.clock = pygame.time.Clock()

        self.objects = pygame.sprite.Group()
        self.player = None
        self.screen_rect = None

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.screen_rect = self.screen.get_rect()

        self.player = obj.Car(self.screen, "car1.png", self.screen_rect.center)
        self.objects.add(self.player)

        self.running = True
        self.screen.fill((50, 50, 50))
        pygame.display.flip()

        for i in self.objects:
            i.image.convert_alpha()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            print("quit")
            self.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("esc down")
            if menu.InGame(self.screen).init() == 1:
                return 1

    def on_loop(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.drive("forward")
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player.drive("backward")
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.drive("left")
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.drive("right")
        if keys[pygame.K_SPACE]:
            self.player.handbrake()
        if keys[pygame.K_r]:
            self.player.reset_position()

        self.player.move()

        # restrict to board
        if not self.screen_rect.contains(self.player.rect):
            self.player.rect.center = self.screen_rect.center

    def on_render(self):
        # screen background
        self.screen.fill((50, 50, 50))

        # draw objects
        self.objects.draw(self.screen)

        # refresh screen
        pygame.display.flip()

    @staticmethod
    def on_cleanup():
        pygame.quit()

    def on_execute(self):
        if self.on_init() is False:
            self.running = False

        while self.running:
            print(self.player.rect.center, self.player.movement_vector, sep=";")
            for event in pygame.event.get():
                if self.on_event(event) == 1:
                    self.on_cleanup()
                    exit(0)
            self.on_loop()
            self.on_render()
            self.clock.tick(60)
        self.on_cleanup()


if __name__ == "__main__":
    a = Game()
    a.on_execute()
