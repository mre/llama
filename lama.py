from cocos.sprite import Sprite
from cocos.tiles import load
from cocos.mapcolliders import RectMapCollider
from cocos.layer import ScrollingManager, ScrollableLayer, ColorLayer
from cocos.director import director
from cocos.scene import Scene
from cocos.actions import Action
from pyglet.window import key
import pyglet

WIDTH = 700
HEIGHT = 500

director.init(width=WIDTH, height=HEIGHT, autoscale=False, resizable=False)

scroller = ScrollingManager()
keyboard = key.KeyStateHandler()
director.window.push_handlers(keyboard)

class GameAction(Action, RectMapCollider):
    # Use the start function instead of  __init__
    # because of the way the Action parent class is structured
    def start(self):
        self.target.velocity = 0, 0

    def on_ground(self):
        rect = self.target.get_rect()
        return rect.y <=  -200

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
        #self.on_ground = bool(new_rect.y == last_rect.y)

        # Now we need to anchor the position of the target to the middle of the bounding rectangle (or else the target won't move)
        self.target.position = new_rect.center

        # Set focus of the scroller to center of player (which is the center of the rect)
        # The * sets the argument passed in as all of the required parameters
        #scroller.set_focus(*new_rect.center)


# Now, once again, we make another class for the sprite's layer
# Remember that it must be a ScrollableLayer
class Lama(ScrollableLayer):
    def __init__(self):
        super(Lama, self).__init__()

        # And, just like last time, we make our sprite and have it do the action we define
        self.sprite = Sprite(pyglet.image.load_animation("assets/img/lama_jump.gif"))
        self.add(self.sprite)
        self.sprite.do(GameAction())

class Level1(ScrollableLayer):
    def __init__(self):
        super(Level1, self).__init__()

        # And, just like last time, we make our sprite and have it do the action we define
        self.sprite = Sprite(pyglet.image.load_animation("assets/img/level1.gif"))
        self.sprite.position = 300, 300
        self.add(self.sprite)
        #self.sprite.do(GameAction())


# The first thing we do in our "main" code is make the layer we just defined
player = Lama()

# Now here's some more code we haven't done before
# Essentially, we need to find the cell where I marked for the player to start, and set the sprite as starting there
# We do this by first finding that cell I marked (check the source code of the map to see how it's done)
# start = map_layer.find_cells(player_start=True)[0]

# Then I get that bounded rectangle we talked about earlier from the sprite
player_rect = player.sprite.get_rect()

# After that I set the middle bottom of the sprite's bounded rectangle equal to the middle bottom of the start cell
#player_rect.midbottom = start.midbottom

# And lastly I set the position of the sprite to the center of the rectangle
player.sprite.position = player_rect.center

# From here it's pretty easy sailing
# First I add the map, and set the "z" to 0
# The z is the vertical axis, so the highest z value layer will always show on top of the others

# Then I add the sprite, and set the z to 1 so that it shows on top of the map layer
scroller.add(player, z=1)


# Same for level
level = Level1()
#level_rect = level.sprite.get_rect()
#level.sprite.position = level_rect.center
#scroller.add(level, z=0)

# Then I make a scene
scene = Scene()
# And I add the scroller to it and put it on top of the stack of layers
scene.add(scroller, z=1)
scene.add(level, z=0)

# And I add the background color (I don't need to define a z because by default it's 0)

director.run(scene)
