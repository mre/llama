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

        # And, just like last time, we make our sprite and have it do the action we define
        self.sprite = Sprite(pyglet.image.load_animation("assets/img/lama_jump.gif"))
        self.sprite.position = 150, 100
        self.add(self.sprite)
        self.sprite.do(GameAction())


class Block(ScrollableLayer):
    def __init__(self):
        super(Block, self).__init__()

        # And, just like last time, we make our sprite and have it do the action we define
        self.sprite = Sprite("assets/img/block.png")
        self.sprite.position = 150, 150
        self.sprite.scale = 0.4
        self.add(self.sprite)


class Level(ScrollableLayer):
    def __init__(self):
        super(Level, self).__init__()

        # And, just like last time, we make our sprite and have it do the action we define
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

        # Check for collisions
        # Figure out new dx and dy values and set the target's velocity equal to those new dx and dy values
        # self.target.velocity = self.collide_map(map_layer, last_rect, new_rect, dy, dx)

        # If the y position hasn't changed, we know that we have not moved off the ground!
        # self.on_ground = bool(new_rect.y == last_rect.y)

        # Now we need to anchor the position of the target to the middle of the bounding rectangle (or else the target won't move)
        self.target.position = new_rect.center

        # Set focus of the scroller to center of player (which is the center of the rect)
        # The * sets the argument passed in as all of the required parameters
        # scroller.set_focus(*new_rect.center)



def main():
    director.init(caption="LAMA", width=WIDTH, height=HEIGHT, autoscale=False, resizable=False)

    director.window.push_handlers(keyboard)

    # The first thing we do in our "main" code is make the layer we just defined
    player = Lama()

    # Now here's some more code we haven't done before
    # Essentially, we need to find the cell where I marked for the player to start, and set the sprite as starting there
    # We do this by first finding that cell I marked (check the source code of the map to see how it's done)
    # start = map_layer.find_cells(player_start=True)[0]

    # Then I get that bounded rectangle we talked about earlier from the sprite
    player_rect = player.sprite.get_rect()

    # After that I set the middle bottom of the sprite's bounded rectangle equal to the middle bottom of the start cell
    # player_rect.midbottom = start.midbottom

    # And lastly I set the position of the sprite to the center of the rectangle
    player.sprite.position = player_rect.center

    # From here it's pretty easy sailing
    # First I add the map, and set the "z" to 0
    # The z is the vertical axis, so the highest z value layer will always show on top of the others

    scene = Scene()
    scene.add(player, z=1)

    block = Block()
    scene.add(block, z=1)

    level = Level()
    scene.add(level, z=0)

    director.run(scene)


if __name__ == "__main__":
    main()
