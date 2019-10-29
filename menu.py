import pygame


class Main:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()

    def on_cleanup(self):
        pass


class InGame(Main):
    def __init__(self, screen):
        super(InGame, self).__init__(screen)

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_q:
                return 1

    def on_loop(self):
        pass

    def on_render(self):
        pygame.display.flip()

    def init(self):
        background = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        background.fill((100, 100, 100, 128))
        self.screen.blit(background, (0, 0))

        while self.running:
            for event in pygame.event.get():
                if self.on_event(event) == 1:
                    return 1
            self.on_loop()
            self.on_render()
            self.clock.tick(60)
        self.on_cleanup()
