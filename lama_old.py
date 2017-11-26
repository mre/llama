from cocos.sprite import Sprite
from cocos.mapcolliders import RectMapCollider
from cocos.layer import ScrollingManager, ScrollableLayer
from cocos.director import director
from cocos.scene import Scene
from cocos.actions import Action
from pyglet.window import key
import pyglet

WIDTH = 700
HEIGHT = 500
keyboard = key.KeyStateHandler()

class Lama(ScrollableLayer):
    def __init__(self):
        super(Lama, self).__init__()

        self.sprite = Sprite(pyglet.image.load_animation("assets/img/lama_jump.gif"))
        self.sprite.position = 150, 100
        self.add(self.sprite)
        self.sprite.do(GameAction())


class Block(ScrollableLayer):
    def __init__(self):
        super(Block, self).__init__()

        self.sprite = Sprite("assets/img/block.png")
        self.sprite.position = 150, 150
        self.sprite.scale = 0.4
        self.add(self.sprite)


class Level(ScrollableLayer):
    def __init__(self):
        super(Level, self).__init__()

        self.sprite = Sprite(pyglet.image.load_animation("assets/img/level1.gif"))
        self.sprite.position = 350, 250
        self.sprite.scale = 2.3
        self.add(self.sprite)


class GameAction(Action, RectMapCollider):
    # Use the start function instead of  __init__
    # because of the way the Action parent class is structured
    def start(self):
        self.target.velocity = 0, 0

    def on_ground(self):
        rect = self.target.get_rect()
        return rect.y <= 0

    def on_bump_handler(self, vx, vy):
        return vx, vy

    def step(self, dt):
        dx = self.target.velocity[0]
        dy = self.target.velocity[1]

        # Combine the left and right values and amplify them so it's visible
        dx = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 250 * dt

        if self.on_ground() and keyboard[key.SPACE]:
            dy = 4500

        # What we do here may seem a bit odd, but it essentially acts as gravity for the target
        if not self.on_ground():
            dy -= 7500 * dt

        # Collision code
        # Get bounding rectangle for last frame
        last_rect = self.target.get_rect()

        # Create new rect for modification
        new_rect = last_rect.copy()
        new_rect.x += dx
        new_rect.y += dy * dt

        # Now we need to anchor the position of the target to the middle of the bounding rectangle (or else the target won't move)
        self.target.position = new_rect.center



def main():
    director.init(caption="LAMA", width=WIDTH, height=HEIGHT, autoscale=False, resizable=False)
    director.window.push_handlers(keyboard)

    scene = Scene()

    player = Lama()
    block = Block()
    level = Level()

    scene.add(player, z=1)
    scene.add(block, z=1)
    scene.add(level, z=0)

    director.run(scene)


if __name__ == "__main__":
    main()
