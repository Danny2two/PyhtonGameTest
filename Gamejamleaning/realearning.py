import arcade
import random
import math

# --- Constants ---
Player_scale = 0.3
Floor_scale = 0.75
Overlay_scale = 0.5

Torch_Particle_num = 15
Weather_Particle_num = 100
Dust_particle_num = 60

TEXTURE_LEFT = 1
TEXTURE_RIGHT = 0

SW = 1200
SH = 800


class Backround_layer_0(arcade.Sprite):
    def __init__(self, row, collum):
        super().__init__("assets/backrounds/city_background.png", Floor_scale)
        self.row = row
        self.collum = collum
        self.center_x = (self.width/2 + (self.collum * self.width))
        self.center_y = (self.height/2 + (self.row * self.height))

    def update(self):
        pass


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/player/guy.png", Player_scale)

        self.textures = []

        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        texture = arcade.load_texture("assets/player/guy.png")
        self.textures.append(texture)
        texture = arcade.load_texture("assets/player/guy.png", flipped_horizontally=True)
        self.textures.append(texture)

        self.texture = texture

        self.center_x = SW / 2
        self.center_y = SH / 2
        self.change_x = 0
        self.change_y = 0

        self.slowingdown = False
        self.grounded = False

        self.jump = False
        self.jump_timer = 0

        self.dash_timer = 0

        self.torch_particle_offset_x = -30
        self.torch_particle_offset_y = 15

    def dash(self):
        if self.dash_timer == 0:
            self.dash_timer = 60
            #self.slowingdown = True
            if self.change_x > 0:
                self.change_x = 100
            elif self.change_x < 0:
                self.change_x = -100

    def update(self,delta_time):

        #print("DashTime" + str(self.dash_timer))
        if self.dash_timer > 0:
            self.dash_timer -= 1
            self.center_x += ((self.change_x * delta_time) * (0.1 * self.dash_timer))
            if self.change_x > 0:
                self.angle = 90
            elif self.change_x < 0:
                self.angle = -90
        else:
            self.center_x += self.change_x * delta_time
            self.angle = 0

        if self.center_y > 100:
            self.change_y -= (9.8 * delta_time)
            self.center_y += self.change_y
        elif self.center_y < 100:
            self.grounded = True
            self.change_y = 0
            self.center_y = 100
        else:
            self.center_y += self.change_y

        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
            self.torch_particle_offset_x = -30
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_RIGHT]
            self.torch_particle_offset_x = 30

        if self.slowingdown and self.grounded:
            if abs(self.change_x) > 0.1:
                self.change_x = self.change_x * 0.8
            else:
                self.change_x = 0


class Overlay(arcade.Sprite):
    def __init__(self, x, y, scale, flicker):
        super().__init__("assets/overlays/torch_overlay.png")
        self.center_x = x
        self.center_y = y
        self.scale = scale
        self.flicker = flicker

    def update(self):
        if self.flicker:
            self.scale = (Overlay_scale + (.005 * random.randint(-5, 5)))


class Torchparticle(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("assets/player/torch_particle.png")
        self.center_x = x
        self.center_y = y
        self.change_x = (0.1 * random.randrange(-20, 20, 1))
        self.change_y = (0.1 * random.randrange(-50, 50, 1))
        self.scale = (0.1 * random.randrange(1, 3, 1))
        self.change_rot = random.randint(-30, 30)
        self.change_alpha = (0.1 * random.randint(-100, -10))

    def update(self):
        self.change_y += (0.2 * random.randint(-2,2))
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += self.change_rot

        if self.alpha > abs(self.change_alpha):
            self.alpha += self.change_alpha
        else:
            self.alpha = 0


class Rain(arcade.Sprite):
    def __init__(self,x,y):
        super().__init__("assets/overlays/rain_particle.png")
        self.center_x = x
        self.center_y = y
        speed_seed = 0.1 * random.randint(10,50)
        self.change_x = -6 * speed_seed
        self.change_y = -10 * speed_seed
        self.angle = -math.degrees(math.tan(self.change_x/self.change_y))
        self.scale = 2
        self.splat_time = 0
        self.textures =[]
        texture = arcade.load_texture("assets/overlays/rain_splat.png")
        self.textures.append(texture)
        texture = arcade.load_texture("assets/overlays/rain_particle.png")
        self.textures.append(texture)
        self.texture = texture

    def update(self):
        if self.splat_time > 0:
            self.splat_time -= 1
            if self.splat_time == 1:
                self.texture = self.textures[1]
                self.bottom = SH + random.randint(5, 500)
                self.center_x = random.randint(50, SW + 400)
        elif self.splat_time == 0:
            self.center_x += self.change_x
            self.center_y += self.change_y
            if self.bottom <= (100 + random.randint(-20, 20)):
                self.texture = self.textures[0]
                self.splat_time = random.randint(20,60)

class Playerdust(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("assets/player/dust_particle.png")
        self.center_x = x
        self.center_y = y
        self.change_x = (0.1 * random.randrange(-20, 20, 1))
        self.change_y = (0.1 * random.randrange(-30, 30, 1))
        self.scale = (0.1 * random.randrange(10, 20, 1))
        self.change_rot = random.randint(-30, 30)
        self.change_alpha = (0.1 * random.randint(-100, -50))

    def update(self):
        self.change_y += (0.2 * random.randint(-2,2))
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += self.change_rot

        if self.alpha > abs(self.change_alpha):
            self.alpha += self.change_alpha
        else:
            self.alpha = 0

# ------MyGame Class--------------
class MyGame(arcade.Window):

    def __init__(self, SW, SH, title):
        super().__init__(SW, SH, title)
        self.set_mouse_visible(False)
        self.is_dark = False


        # Make Player
        self.player = Player()

        # Make Overlay
        self.overlay = Overlay(SW / 2, SH / 2, Overlay_scale, True)
        self.overlay2 = Overlay(SW / 2, SH / 2, 1.5, False)

        self.weather_particle_list = arcade.SpriteList()
        for i in range(Weather_Particle_num):
            i = Rain(random.randint(0,SW +200), SH + random.randint(10,500))
            self.weather_particle_list.append(i)

        # generates background tiles, does math for determining how many are needed in x and y
        self.background_tile_list = arcade.SpriteList()
        self.background_tile_list.is_static = True
        y = -1
        for i in range(0, SH, 1600):
            y += 1
            x = -1
            for i in range(0, SW, 1200):
                x += 1
                background = Backround_layer_0(y, x)
                self.background_tile_list.append(background)

        #generates torch particles
        self.particle_list = arcade.SpriteList()
        for i in range(Torch_Particle_num):
            particle = Torchparticle(SW / 2, SH / 2)
            self.particle_list.append(particle)

        self.dust_particle_list = arcade.SpriteList()

    def reset(self):
        pass

    def on_draw(self):
        # draws background tiles

        self.background_tile_list.draw()
        #arcade.draw_rectangle_filled(SW / 2, SH / 2, SW, SH, arcade.color.WHITE)
        self.player.draw()
        self.dust_particle_list.draw()

        if self.is_dark:
            self.overlay.draw()
            self.weather_particle_list.draw()
            self.overlay2.draw()
        else:
            self.weather_particle_list.draw()
        self.particle_list.draw()



    def on_update(self,dt):

        self.player.update(dt)

        self.overlay.update()

        self.weather_particle_list.update()

        self.dust_particle_list.update()

        for i in self.dust_particle_list:
            if i.alpha == 0:
                i.kill()


        for i in self.particle_list:
            i.update()
            if i.center_y < -5 or i.alpha == 0:
                i.change_y = (0.1 * random.randrange(0, 50, 1))
                i.center_y = self.player.center_y + self.player.torch_particle_offset_y
                i.center_x = self.player.center_x + self.player.torch_particle_offset_x
                i.alpha = 255


        self.overlay.center_y = self.player.center_y + self.player.torch_particle_offset_y
        self.overlay.center_x = self.player.center_x + self.player.torch_particle_offset_x
        self.overlay2.center_y = self.player.center_y
        self.overlay2.center_x = self.player.center_x

        if self.player.dash_timer > 0:
            if self.player.change_x > 0:
                dust = Playerdust(self.player.right, self.player.center_y - 15)
            else:
                dust = Playerdust(self.player.left, self.player.center_y - 15)
            self.dust_particle_list.append(dust)


    def on_key_press(self, symbol, modifiers: int):
        print(symbol)
        print(modifiers)

        if symbol == 97:
            self.player.slowingdown = False
            if modifiers == 1:
                self.player.change_x = -300
            else:
                self.player.change_x = -200

        elif symbol == 100:
            self.player.slowingdown = False
            if modifiers == 1:
                self.player.change_x = 300
            else:
                self.player.change_x = 200

        elif modifiers == 1:
            if self.player.change_x > 0:
                self.player.change_x = 300
            elif self.player.change_x < 0:
                self.player.change_x = -300

        if symbol == 32:
            if self.player.grounded:
                self.player.change_y = 10
                self.player.grounded = False

        elif symbol == 111:
            self.is_dark = not self.is_dark

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == 97 and self.player.change_x < 0:
            self.player.slowingdown = True

        elif symbol == 100 and self.player.change_x > 0:
            self.player.slowingdown = True

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        print("Mouse button" + str(button))
        if button == 4:
            self.player.dash()




# -----Main Function--------
def main():
    window = MyGame(SW, SH, "Darkroom")
    window.reset()
    arcade.run()


# ------Run Main Function-----
if __name__ == "__main__":
    main()
