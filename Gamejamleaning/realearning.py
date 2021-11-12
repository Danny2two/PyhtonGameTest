
import arcade
import random
import math

# --- Constants ---
Player_scale = 0.3
Floor_scale = 0.5
Overlay_scale = 0.5

Tourch_Particle_num = 15

TEXTURE_LEFT = 1
TEXTURE_RIGHT = 0

SW = 1200
SH = 800



class Backround_layer_0(arcade.Sprite):
    def __init__(self,row,collum):
        super().__init__("assets/backrounds/floor.png", Floor_scale)
        self.row = row
        self.collum = collum
        self.center_x = (100 + (self.collum * 200))
        self.center_y = (100 + (self.row * 200))


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

        self.jump= False
        self.jump_timer = 0

        self.torch_particle_offset_x = -30
        self.torch_particle_offset_y = 20


    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
            self.torch_particle_offset_x = -30
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_RIGHT]
            self.torch_particle_offset_x = 30



#this is the code for the jump animation and it sucks
        if self.jump_timer > 0:
            self.jump_timer -= 1
        #elif self.jump_timer == 0:

        if self.scale > Player_scale:
            self.scale -= 0.02
            self.jump = False
        else:
            self.scale = Player_scale

        if self.jump:
            #print(self.jump)
            self.scale += (0.05 * self.jump_timer)




class Overlay(arcade.Sprite):
    def __init__(self,x,y,scale,flicker):
        super().__init__("assets/overlays/torch_overlay.png")
        self.center_x = x
        self.center_y = y
        self.scale = scale
        self.flicker = flicker

    def update(self):
        if self.flicker:
            self.scale = (Overlay_scale + (.005 * random.randint(-5,5)))

class Torchparticle(arcade.Sprite):
    def __init__(self,x,y):
        super().__init__("assets/player/torch_particle.png")
        self.center_x = x
        self.center_y = y
        self.change_x = (0.1 * random.randrange(-20,20,1))
        self.change_y = (0.1 * random.randrange(-50, 50, 1))
        self.scale = (0.1 * random.randrange(1,6,1))
        self.change_rot = random.randint(-30,30)
        self.change_alpha = random.randint(-2,-1)

    def update(self):
        self.change_y -= 0.2
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += self.change_rot
        self.alpha += self.change_alpha











# ------MyGame Class--------------
class MyGame(arcade.Window):
    _vsync = True
    def __init__(self, SW, SH, title):
        super().__init__(SW, SH, title)
        self.set_mouse_visible(False)

        #Make Player
        self.player = Player()

        #Make Overlay
        self.overlay = Overlay(SW/2, SH/2,Overlay_scale,True)
        self.overlay2 = Overlay(SW/2, SH/2,1.5,False)

#generates background tiles, does math for determining how many are needed in x and y
        self.background_tile_list = []
        y = -1
        for i in range(0, SH, 200):
            y += 1
            x = -1
            for i in range(0, SW, 200):
                x += 1
                background = Backround_layer_0(y,x)
                self.background_tile_list.append(background)

        self.particle_list = []
        for i in range(Tourch_Particle_num):
            particle = Torchparticle(SW/2,SH/2)
            self.particle_list.append(particle)




    def reset(self):
        pass

    def on_draw(self):
        #draws background tiles
        for i in self.background_tile_list:
            i.draw()

        self.player.draw()

        self.overlay.draw()

        for i in self.particle_list:
            i.draw()

        self.overlay2.draw()



    def on_update(self, dt):

        self.player.update()

        self.overlay.update()

        for i in self.particle_list:
            i.update()
            if i .center_y < -5:
                i.change_y = (0.1 * random.randrange(0, 50, 1))
                i.center_y = self.player.center_y + self.player.torch_particle_offset_y
                i.center_x = self.player.center_x + self.player.torch_particle_offset_x
                i.alpha = 255



        self.overlay.center_y = self.player.center_y + self.player.torch_particle_offset_y
        self.overlay.center_x = self.player.center_x + self.player.torch_particle_offset_x
        self.overlay2.center_y = self.player.center_y
        self.overlay2.center_x = self.player.center_x




    def on_key_press(self, symbol, modifiers: int):
        #print(symbol)
        if symbol == 119:
            self.player.change_y = 5
        elif symbol == 97:
            self.player.change_x = -5
        elif symbol == 115:
            self.player.change_y = -5
        elif symbol == 100:
            self.player.change_x = 5
        elif symbol == 32:
            if not self.player.jump:
                #print("set")
                self.player.jump = True
                self.player.jump_timer = 5

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == 119:
            self.player.change_y = 0
        elif symbol == 97:
            self.player.change_x = 0
        elif symbol == 115:
            self.player.change_y = 0
        elif symbol == 100:
            self.player.change_x = 0



# -----Main Function--------
def main():
    window = MyGame(SW, SH, "Darkroom")
    window.reset()
    arcade.run()


# ------Run Main Function-----
if __name__ == "__main__":
    main()
