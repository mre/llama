import cocos
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import ColorLayer
from cocos.sprite import Sprite

import cocos.collision_model as cm
import cocos.euclid as eu

from collections import defaultdict
from pyglet.window import key
import pyglet

WIDTH = 700
HEIGHT = 500


class Background(Sprite):
    def __init__(self):
        super(Background, self).__init__(pyglet.image.load_animation("assets/img/level1.gif"))
        self.position = 350, 250
        self.scale = 2.3


class Block(Sprite):
    def __init__(self, x, y, pic):
        super(Block, self).__init__(pic)
        self.position = pos = eu.Vector2(x, y)
        self.cshape = cm.CircleShape(pos, self.width / 2 - 10)


class Lama(Sprite):
    def __init__(self, x, y):
        super(Lama, self).__init__(pyglet.image.load_animation("assets/img/lama_jump.gif"))
        self.position = pos = eu.Vector2(x, y)
        self.cshape = cm.CircleShape(pos, self.width / 2 - 10)
        self.speed = 1.0
        self.strength = 1.0

    def move(self, dx, dy):
        x, y = self.position
        self.position = (x + self.speed * dx, y + self.strength * dy)
        self.cshape.center = self.position

    def powerup(self):
        self.speed += self.speed * 0.3
        self.strength += self.strength * 0.3

    def on_ground(self):
        x, y = self.position
        return y <= 80


class Game(ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(Game, self).__init__(0, 80, 125, 0)

        self.block_pic = "assets/img/block.png"
        for pos in [(100, 100), (540, 380), (540, 100), (100, 380)]:
            self.add(Block(pos[0], pos[1], self.block_pic))
        self.lama = Lama(120, 100)
        self.add(self.lama)

        cell = self.lama.width * 1.25
        self.collman = cm.CollisionManagerGrid(0, 640, 0, 480, cell, cell)

        self.pressed = defaultdict(int)
        self.schedule(self.update)

    def on_key_press(self, k, m):
        self.pressed[k] = 1

    def on_key_release(self, k, m):
        self.pressed[k] = 0

    def update(self, dt):
        self.collman.clear()
        for _, node in self.children:
            self.collman.add(node)
        for other in self.collman.iter_colliding(self.lama):
            self.remove(other)
            self.lama.powerup()

        dx = (self.pressed[key.RIGHT] - self.pressed[key.LEFT]) * 250 * dt
        dy = 0
        if self.lama.on_ground():
            if self.pressed[key.SPACE]:
                dy = 150
        else:
            dy -= 300 * dt
        self.lama.move(dx, dy)


def main():
    director.init(caption="Lama!!!", width=WIDTH, height=HEIGHT)
    scene = Scene()
    scene.add(Background(), z=0)
    scene.add(Game(), z=1)
    director.run(scene)


if __name__ == "__main__":
    main()
