import pygame, math, sys

pygame.init()

class Config(object):
    
    gridsquare_size = 32
    mapsize = (2048,2048)
    width = 800
    height = 600
    screensize = (width,height)
    cornerpoint = [0,0]
    fps = 40
    scrollstepx = 1
    scrollstepy = 1

class Formation(object):

    def __init__(self,units):
        self.units = units
        

class Unit(pygame.sprite.Sprite):
    count = 0
    selected = []
    ## Contains the base information of the instance
    def __init__(self,pos,groups,graphics):
        pygame.sprite.Sprite.__init__(self,groups)
        Unit.count += 1
        self.image = graphics[0]
        self.rect = self.image.get_rect()
        self.trueX = pos[0]
        self.trueY = pos[1]
        self.rect.center = (self.trueX,self.trueY)
        self.moveto = None
        self.speed = 0
        self.speedimpulse = 0
        self.angle = 0
        self.radius = 0.1
        self.mass = 0.01



    def target(self,target):
        self.moveto = target
        x = self.trueX - self.moveto[0]
        y = self.trueY - self.moveto[1]
        self.angle = math.atan2(y,x) - 0.5*math.pi
        self.speed = 0.5

    def move(self,seconds):
        self.trueX += math.sin(self.angle) * self.speed * seconds
        self.trueY -= math.cos(self.angle) * self.speed * seconds

    ##used each frame to update the state of the instance
    def update(self,seconds,impulse=0):
        self.rect.center = array_to_screen((self.trueX,self.trueY))
       

        #if a target has been set, move towards it and stop when reached
        if  self.moveto != None:
            x = self.trueX - self.moveto[0]
            y = self.trueY - self.moveto[1]
            self.angle = math.atan2(y,x) - 0.5*math.pi
            self.speedimpulse *= self.mass
            self.speed = self.speed
            self.move(seconds)
            array_rectcoords = screen_to_array(self.rect.center)
            if array_rectcoords[0]-0.1 <= self.moveto[0] < array_rectcoords[0]+0.1:
                    if array_rectcoords[1]-0.1 <= self.moveto[1] < array_rectcoords[1]+0.1:
                        target = array_to_screen(self.moveto)
                        trueX = target[0]
                        trueY = target[1]
                        self.moveto = None


            

    ## marks a unit as selected if clicked on, and deselects it if you click elsewhere
    def selection(self,graphics):
        if self.rect.collidepoint((pygame.mouse.get_pos())):
            if not self in Unit.selected:
                Unit.selected.append(self)
                self.image = graphics[1]
                print(Unit.selected)
            

        elif not self.rect.collidepoint((pygame.mouse.get_pos())):
            if self in Unit.selected:
                Unit.selected.remove(self)
                self.image = graphics[0]
                print(Unit.selected)

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

def collide(p1, p2,elasticity = 1):
    dx = p1.trueX - p2.trueX
    dy = p1.trueY - p2.trueY
    
    dist = math.hypot(dx, dy)
    if dist < p1.radius + p2.radius:
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent

        angle1 = 2*tangent - p1.angle
        angle2 = 2*tangent - p2.angle
        speed1 = p2.speed*elasticity
        speed2 = p1.speed*elasticity

        (p1.angle, p1.speedimpulse) = (angle1, speed1)
        (p2.angle, p2.speedimpulse) = (angle2, speed2)

        coords = screen_to_array((math.sin(angle),math.cos(angle)))


        p1.trueX += coords[0]
        p1.trueY -= coords[1]
        p2.trueX -= coords[0]
        p2.trueY += coords[1]
   

def screen_to_array(screen_coords):
    #takes a coordinate tuple and converts it from screen coords to array coords
    screen_coords = list(screen_coords)
    screen_coords[0] = (screen_coords[0]/Config.gridsquare_size) + Config.cornerpoint[0]
    screen_coords[1] = (screen_coords[1]/Config.gridsquare_size) + Config.cornerpoint[1]
    return tuple(screen_coords)

def array_to_screen(array_coords):
    #takes a coordinate tuple and converts it from array coords to screen coords
    array_coords = list(array_coords)
    array_coords[0] = array_coords[0]*Config.gridsquare_size - Config.cornerpoint[0]*Config.gridsquare_size
    array_coords[1] = array_coords[1]*Config.gridsquare_size - Config.cornerpoint[1]*Config.gridsquare_size
    return tuple(array_coords)

def scroll(background):
    scrollx = 0
    scrolly = 0
    pressedkeys = pygame.key.get_pressed()
    # --- handle Cursor keys to scroll map ----
    if pressedkeys[pygame.K_LEFT]:
        scrollx -= Config.scrollstepx
    if pressedkeys[pygame.K_RIGHT]:
        scrollx += Config.scrollstepx
    if pressedkeys[pygame.K_UP]:
        scrolly -= Config.scrollstepy
    if pressedkeys[pygame.K_DOWN]:
        scrolly += Config.scrollstepy
        # -------- scroll the visible part of the map ------
    Config.cornerpoint[0] += scrollx
    Config.cornerpoint[1] += scrolly
    #--------- do not scroll out of bigmap edge -----
    if Config.cornerpoint[0] < 0:
        Config.cornerpoint[0] = 0
        scrollx = 0
    elif Config.cornerpoint[0] > Config.mapsize[0] - int(Config.screensize[0]/Config.gridsquare_size+1):
        Config.cornerpoint[0] = Config.mapsize[0] - int(Config.screensize[0]/Config.gridsquare_size+1)
        scrollx = 0
    if Config.cornerpoint[1] < 0:
        Config.cornerpoint[1] = 0
        scrolly = 0
    elif Config.cornerpoint[1] > Config.mapsize[1] - int(Config.screensize[1]/Config.gridsquare_size+2):
        Config.cornerpoint[1] = Config.mapsize[1] - int(Config.screensize[1]/Config.gridsquare_size+2)
        scrolly = 0

    snapshot = background.subsurface((Config.cornerpoint[0],Config.cornerpoint[1],Config.width,Config.height))
    return snapshot

def drawgrid(background):
    for x in range(0,Config.mapsize[0],Config.gridsquare_size): #start, stop, step
        pygame.draw.line(background, (200,200,200), (x,0), (x,Config.mapsize[1]))
    for y in range(0,Config.mapsize[1],Config.gridsquare_size): #start, stop, step
        pygame.draw.line(background, (200,200,200), (0,y), (Config.mapsize[0],y))

def circle_collision(a,b):
    r = a.radius + b.radius
    r*=r
    return r < (a.trueX+b.trueX)^2+(a.trueY+b.trueY)^2


def terminate():
    pygame.quit()
    sys.exit()

def main():
    
    gridsize = 200
    screen=pygame.display.set_mode((Config.width,Config.height))
    background = pygame.Surface(Config.mapsize)
    clock = pygame.time.Clock()
    playtime = 0
    spritegroup = pygame.sprite.Group()
    unitlist = []

    mapgrid = [[0 for i in range(gridsize)]for j in range(gridsize)]

    graphics = [pygame.image.load('blue_dot.png').convert(),
                pygame.image.load('blue_dot_sel.png').convert()]
    for i in graphics:
        i.set_colorkey((255,0,255))

    background.fill((255,255,255))
    drawgrid(background)
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
                    unitlist.append(Unit(screen_to_array(pygame.mouse.get_pos()),spritegroup,graphics))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for unit in unitlist:
                        unit.selection(graphics)
                if event.button == 3:
                    for i in Unit.selected:
                        target = screen_to_array(pygame.mouse.get_pos())
                        i.target(target)

                    
                    

        snapshot = scroll(background)
                
        for i, unit in enumerate(unitlist):
            unit.update(seconds)
            for unit2 in unitlist[i+1:]:
                collide(unit,unit2)
            
            
        spritegroup.clear(screen,snapshot)
        spritegroup.draw(screen)
        pygame.display.flip()
        
        

if __name__ == "__main__":
    # Creating the screen
    screen = pygame.display.set_mode((640, 480), 0, 32)
 
    menu_items = ('Start', 'Quit')
 
    pygame.display.set_caption('Game Menu')
    gm = GameMenu(screen, menu_items)
    gm.run()
