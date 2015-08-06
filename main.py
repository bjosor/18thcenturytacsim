import pygame, math, sys

pygame.init()

class Config(object):

    width = 800
    height = 600
    fps = 40

class unit(pygame.sprite.Sprite):
    count = 0

    def __init__(self,pos,groups):
        pygame.sprite.Sprite.__init__(self, groups)
        self.image = pygame.image.load("blue_dot.png")
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.name = unit.count
        unit.count += 1

class MenuItem(pygame.font.Font):
    def __init__(self, text, font=None, font_size=30, font_color=(255, 255, 255), pos= (0,0)):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.position = pos
        self.posx = self.position[0]
        self.posy = self.position[1]
 
    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def is_mouse_selection(self, pos):
        if (pos[0] >= self.pos_x and pos[0] <= self.pos_x + self.width) and \
            (pos[1] >= self.pos_y and pos[1] <= self.pos_y + self.height):
                return True
        return False

    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)
        
class GameMenu():
    def __init__(self, screen, items, bg_color=(0,0,0), font=None, font_size=30,
                    font_color=(255, 255, 255)):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
 
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
 
        self.items = items
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
 
        self.items = []
        for index, item in enumerate(items):
            menu_item = MenuItem(item)
 
            # t_h: total height of text block
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            pos_y = (self.scr_height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height)
         
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
 
    def run(self):
        menuloop = True
        while menuloop:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    menuloop = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mpos = pygame.mouse.get_pos()
                    for item in self.items:
                        if item.is_mouse_selection(mpos):
                            if item.text == "Quit":
                                pygame.quit()
                            if item.text == "Start":
                                main()
                            menuloop = False
                            
 
            # Redraw the background
            self.screen.fill(self.bg_color)
 
            for item in self.items:
                if item.is_mouse_selection(pygame.mouse.get_pos()):
                    item.set_font_color((255, 0, 0))
                    item.set_italic(True)
                else:
                    item.set_font_color((255, 255, 255))
                    item.set_italic(False)
                self.screen.blit(item.label, item.position)
 
            pygame.display.flip()
    
    
def terminate():
    pygame.quit()
    sys.exit()

def main():

    screen=pygame.display.set_mode((Config.width,Config.height))
    background = screen.copy()
    clock = pygame.time.Clock()
    playtime = 0
    spritegroup = pygame.sprite.Group()
    unitdict = {}

    background.fill((255,255,255))
    screen.blit(background,(0,0))

    mainloop = True
    while mainloop == True:
        milliseconds = clock.tick(Config.fps)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
        playtime += seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame window closed by user
                mainloop = False
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                    mainloop = False # exit game
                if event.key == pygame.K_p:
                    unitdict[unit.count] = unit(pygame.mouse.get_pos(),spritegroup)
                    

        spritegroup.clear(screen,background)
        spritegroup.draw(screen)
        pygame.display.flip()
        
        

if __name__ == "__main__":
    # Creating the screen
    screen = pygame.display.set_mode((640, 480), 0, 32)
 
    menu_items = ('Start', 'Quit')
 
    pygame.display.set_caption('Game Menu')
    gm = GameMenu(screen, menu_items)
    gm.run()
