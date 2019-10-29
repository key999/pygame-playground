import pygame
from math import sin, cos, radians, ceil


class Object(pygame.sprite.DirtySprite):
    def __init__(self, screen, file, pos):
        super(Object, self).__init__()
        # self.pos = pos
        self.blocking = False
        self.original_image = pygame.image.load(file)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.screen = screen


class NPC(Object):
    def __init__(self, screen, file, pos):
        super().__init__(screen, file, pos)
        self.blocking = True
        self.step = 5

    # def move(self, direction, screen_size):
    #     if direction.lower() == "up":
    #         if self.pos[1] > 0:
    #             self.pos[1] -= self.step
    #     elif direction.lower() == "down":
    #         if self.pos[1] + self.image.get_height() < screen_size[1]:
    #             self.pos[1] += self.step
    #     elif direction.lower() == "left":
    #         if self.pos[0] > 0:
    #             self.pos[0] -= self.step
    #     elif direction.lower() == "right":
    #         if self.pos[0] + self.image.get_width() <= screen_size[0]:
    #             self.pos[0] += self.step


class Car(Object):
    def __init__(self, screen, file, pos):
        super().__init__(screen, file, pos)
        self.blocking = True
        self.max_speed = 10
        self.acceleration = 0.5
        self.turn_rate = 7

        # [speed, angle]
        self.movement_vector = [0, 0]
        self.car_angle = self.movement_vector[0]

    def move(self):
        # if not moving skip calculations
        if self.movement_vector[0] == 0:
            # self.car_angle = self.movement_vector[1]
            return

        # calculate movement
        c, fi = self.movement_vector[0], self.movement_vector[1]
        y = ceil(c * cos(radians(fi)))
        x = ceil(c * sin(radians(fi)))
        print(x, y)

        self.rect.move_ip(x, y)

        self.apply_friction()

    def apply_friction(self):
        # if abs(self.movement_vector[0]) < 0.5:
        #     self.movement_vector[0] = 0
        self.movement_vector[0] /= 1.005

    def drive(self, direction):
        # get acceleration
        if direction == "forward":
            self.movement_vector[0] -= self.acceleration
        elif direction == "backward":
            self.movement_vector[0] += self.acceleration / 2

        # get turns and drifts
        # restrict turning to speed
        actual_turn = 0
        if abs(self.movement_vector[0]) > self.max_speed / 10:
            actual_turn = self.turn_rate * (self.movement_vector[0] / self.max_speed)

        # determine turning direction and apply car angle
        # get car angle
        if direction == "left":
            self.car_angle -= actual_turn
        elif direction == "right":
            self.car_angle += actual_turn

        # drifting mechanics will go here (maybe)
        if abs(self.movement_vector[0]) <= self.max_speed / 5:
            self.movement_vector[1] = self.car_angle
        else:
            self.movement_vector[1] = self.car_angle

        # restrict maximum speed
        if self.movement_vector[0] > self.max_speed:
            self.movement_vector[0] = self.max_speed
        elif self.movement_vector[0] < -self.max_speed:
            self.movement_vector[0] = -self.max_speed

        # restrict angle
        # probably not needed but maybe useful in case of big numbers
        self.movement_vector[1] %= 360
        self.car_angle %= 360

        # rotate sprite according to angle
        # also control "axis of rotation" by moving rotated image back into place
        # so that is stays on top of actual object at all times
        self.rect = self.image.get_rect(
            center=(self.rect.x + self.image.get_width() / 2, self.rect.y + self.image.get_height() / 2))
        self.image = pygame.transform.rotate(self.original_image, self.car_angle)

        new_pos = self.image.get_rect()
        new_pos.center = self.rect.center
        self.rect = new_pos

    def handbrake(self):
        self.movement_vector[0] /= 1.07
        if abs(self.movement_vector[0]) <= 2:
            self.movement_vector[0] = 0

    def reset_position(self):
        self.rect.center = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.movement_vector[0] = 0
