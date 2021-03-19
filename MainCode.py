######### Raging Racers Game // PyKart
######Import Statements
from math import sin, radians, degrees, copysign
import pygame
from pygame.math import Vector2
import time
pygame.init()
pygame.font.init()#####Declare global variables
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
window_width = 919
window_height = 447
GAMEEND = 0
GAMESTART = 0
#Loads all images needed - Caching - Improves loading times
backgroundMainMenu = pygame.image.load("MainMenu2Maybe.png")
instructionpagebackground = pygame.image.load("instructionPage.png")
KPbackground = pygame.image.load("rsz_kartpickerdesign.jpg")
WinningScreen = pygame.image.load("winningscreen3resize.png")
MainMap = pygame.image.load("mainmap.png")
MainMap2 = pygame.image.load("mainmap2.png")
Kart_Blue = pygame.image.load("Kart_BLUENEW.png")	
#Kart_Blue = pygame.transform.scale(Kart_Blue,(10,10))
Kart_Green = pygame.image.load("Kart_GREENNEW.png")
Kart_Orange = pygame.image.load("Kart_ORANGENEW.png")
Kart_Pink = pygame.image.load("Kart_PINKNEW.png")
Kart_Red = pygame.image.load("Kart_REDNEW.png")
Kart_Yellow = pygame.image.load("Kart_YELLOWNEW.png")
#Enters loaded karts into list to be accessed
karts = (Kart_Blue, Kart_Green, Kart_Orange, Kart_Pink, Kart_Red, Kart_Yellow)#puts all loaded kart images into a list
gameDisplay = pygame.display.set_mode((window_width, window_height))#sets the surface for images etc to be blitted onto
#sets game caption
pygame.display.set_caption("Road Runners Game")
#sets game clock
clock = pygame.time.Clock()
fps_menu = 30

####Classes
class car:
  def __init__(self, x, y, currentKart, angle=0.0, length=3, max_steering=30, max_acceleration=5.0):#sets neutral variables and class attributes
    self.image = currentKart
    self.rect = self.image.get_rect()
    self.position = Vector2(x, y)
    self.velocity = Vector2(0.0, 0.0)
    self.max_velocity = 40
    self.angle = angle
    self.length = length
    self.max_acceleration = max_acceleration
    self.max_steering = max_steering
    self.brake_deceleration = 10
    self.free_deceleration = 2
    self.acceleration = 0.0
    self.steering = 0.0
    self.angular_velocity = 0
    self.turning_radius = 0

  def update(self, dt):#update method
    self.velocity += (self.acceleration * dt, 0)# the velocity is the acceleration multipled overtime
    self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))# the max velocity can go to is the max_velocity attribute
    if self.steering:
      self.turning_radius = self.length / sin(radians(self.steering))#the turning radius is the steering attribute turned from degrees to radians which pygame uses which is then divided by length of the car
      self.angular_velocity = self.velocity.x / self.turning_radius#calculates angular  velocity
    else:
      self.angular_velocity = 0#otherwise set to 0 
    self.position += self.velocity.rotate(-self.angle) * dt
    self.angle += degrees(self.angular_velocity) * dt

class Timer(pygame.sprite.Sprite):#timer object
  def __init__(self,GAMEEND, GAMESTART):
    super().__init__()
    self.GAMEEND = GAMEEND
    self.GAMESTART = GAMESTART
    self.difference = self.GAMEEND - self.GAMESTART#calculates the time ticked from the game starting and when it is starting timer - required for calculating the difference
    self.font_name = pygame.font.match_font('arial')#sets the font type to arial
    self.font = pygame.font.Font(self.font_name, 100)
    self.UItext = pygame.font.Font(self.font_name,25)

  def update(self):
    self.loggedTime = pygame.time.get_ticks()
    self.timer = int(self.loggedTime/1000)
    self.displayTime = self.timer - self.difference#turns milliseconds into secords
    self.displayTime = round(self.displayTime,0)#rounds the number
    self.displayTime = int(self.displayTime)#turns into integer
    self.displayTime1 = str(self.displayTime)#turns int into string to be put onto screen
    
    self.timerText = self.UItext.render("RaceTimer: ",True, WHITE)
    self.timerTextRect = self.timerText.get_rect()
    self.timerTextRect.midtop = (60,5)
    
    self.text_surface = self.UItext.render(self.displayTime1, True, WHITE)
    self.text_rect = self.text_surface.get_rect()
    self.text_rect.midtop = (125,5)

    gameDisplay.blit(self.text_surface, self.text_rect)#blits text onto screen for timer
    gameDisplay.blit(self.timerText,self.timerTextRect)

class CountDown(pygame.sprite.Sprite):#countdown object
  def __init__(self,GAMEEND, GAMESTART):
    super().__init__()
    self.GAMEEND = GAMEEND
    self.GAMESTART = GAMESTART
    self.difference = self.GAMEEND - self.GAMESTART
    self.font_name = pygame.font.match_font('arial')
    self.font = pygame.font.Font(self.font_name, 100)

  def update(self):
    self.countDown = 5
    self.loggedTime = pygame.time.get_ticks()
    self.timer = int(self.loggedTime/1000)#turns milliseconds into secords
    self.countDown = self.countDown + self.difference
    self.countDown -= self.timer#takes countdown from timer 
    self.countDown = round(self.countDown,0)#rounds the number
    self.countDown = int(self.countDown)#turns into integer 
    self.displayCountDown = str(self.countDown)#turns int into string to be put onto screen
    
    self.text_surfaceTwo = self.font.render(self.displayCountDown, True, WHITE)
    self.text_rectTwo= self.text_surfaceTwo.get_rect()
    self.text_rectTwo.midtop = ((583/2), (584/2))
    
    if self.countDown < 1:#if countdown is less than 1
      self.text_rectTwo.midtop = (-100, -100)#more text out of view aka removing it
      self.text_surfaceTwo = self.font.render("GO!", True, WHITE)
      self.text_rectTwo= self.text_surfaceTwo.get_rect()
      self.text_rectTwo.midtop = ((583/2), (584/2))#replace with "go" text
      if self.countDown < 0:#if below 0
        self.text_rectTwo.midtop = (-100, -100)#remove "go"
 
    gameDisplay.blit(self.text_surfaceTwo, self.text_rectTwo)#blits to screen 

#class version main game
class Game:
  def __init__(self):
    width = 583
    height = 584
    self.screen = pygame.display.set_mode((width, height))
    self.clock = pygame.time.Clock()
    self.ticks = 60
    self.exit = False

  def run(self, currentKart,ts, GAMESTART):
    player = car(70, 22.5, currentKart)#creates car object
    GAMEEND = time.time()
    print(GAMEEND, "END")
    if ts == True:
      playerTimer = Timer(GAMEEND, GAMESTART)#creates timer object
      playerCountdown = CountDown(GAMEEND, GAMESTART)#creates countdown object
      
    while not self.exit:
      dt = self.clock.get_time() / 1000# gets the ticks of the game in while loop
      # Event queue
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.exit = True
          
        pressed = pygame.key.get_pressed()#get key presses
        if pressed[pygame.K_UP]:#if up arrow key
          if player.velocity.x < 0: #if velocity less than 0 
            player.acceleration = player.brake_deceleration
          else:
            player.acceleration += 1 * dt
        elif pressed[pygame.K_DOWN]:
          if player.velocity.x > 0:#if velocity greater than 0
            player.acceleration = -player.brake_deceleration#takes acceleration away from the deceleration acting like friction 
          else:
            player.acceleration -= 1 * dt

        elif pressed[pygame.K_SPACE]:#if space pressed
          if abs(player.velocity.x) > dt * player.brake_deceleration:#if the absolute velocity is greater than time * player brake deceleration
            player.acceleration = -copysign(player.brake_deceleration, player.velocity.x)
          else:
            player.acceleration = -player.velocity.x / dt

        else:
          if abs(player.velocity.x) > dt * player.free_deceleration:#if the absolute velocity is greater than free deceleration.
            player.acceleration = -copysign(player.free_deceleration, player.velocity.x)
          else:
            if dt != 0:
              player.acceleration = -player.velocity.x / dt
        player.acceleration = max(-player.max_acceleration, min(player.acceleration, player.max_acceleration))# acceleration is maxed to its variable max which stops any more than given.
          
        if pressed[pygame.K_RIGHT]:#if right key is pressed
          player.steering -= 1250 * dt#the steering is 1250 * time
        elif pressed[pygame.K_LEFT]:#if left key is presses
          player.steering += 1250 * dt#the steering is 1250 * time
        else:
          player.steering = 0#if no keys pressed it is 0 aka forward wherever it is facing
        player.steering = max(-player.max_steering, min(player.steering, player.max_steering))# steering is maxed to its variable max which stops any more than given.
        
      player.update(dt)#send the time (dt) to update method in car class
      gameDisplay.fill((0,0,0))#fills screen with black so the car image doesnt leave trail, bug fix
      gameDisplay.blit(MainMap2,(0,0))#puts main map onto screen
      playerTimer.update()#updates the timer each iteration aka whenever game fps refreshes
      playerCountdown.update()#updates the timer each iteration aka whenever game fps refreshes
      rotated = pygame.transform.rotate(currentKart, player.angle)#rotates image by angle of turn
      rect = rotated.get_rect()#gets the rect of the image
      ppu = 4
      gameDisplay.blit(rotated, player.position * ppu - (rect.width / 2, rect.height / 2))#blits rotated image to screen
      pygame.display.flip()#updates changes to screen

      self.clock.tick(self.ticks)
    pygame.quit()
  
#####Functions
def displayMenu(GAMESTART):
  GAMESTART = time.time()
  timerStart = False
  status = True
  while status:#Check for any key presses
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        status = False#if exit button pressed, end loop

      if event.type == pygame.MOUSEBUTTONDOWN:#when mousebutton clicked
        mouse_x, mouse_y = pygame.mouse.get_pos()
        print(mouse_x, mouse_y)#output coordinates
      if event.type == pygame.MOUSEBUTTONDOWN and mouse_x >= 557 and mouse_x <= 904 and mouse_y >= 231 and mouse_y <= 324:# sets coordinates for detecting button press
        KartPicker(timerStart,GAMESTART)#Starts the KartPicker Function with its own eventloop allowing it to be displayed on top
      if event.type == pygame.MOUSEBUTTONDOWN and mouse_x >= 555 and mouse_x <= 901 and mouse_y >= 335 and mouse_y <= 427:# sets coordinates for detecting button press
        instructionPage()#Starts the Instruction page function with its own eventloop allowing it to be displayed on top

      gameDisplay.blit(backgroundMainMenu,(0,0))#display background for Main Menu onto the screen
      pygame.display.flip()#update the screen every iteration of clock
      clock.tick(fps_menu)#sets iteration e.g. how many times to update
                           
def instructionPage():
    Instructionstatus = True
    while Instructionstatus:#instructionpage event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#if exit button pressed, end loop
                Instructionstatus = False

            if event.type == pygame.MOUSEBUTTONDOWN:#when mousebutton clicked
                mouse_x, mouse_y = pygame.mouse.get_pos()#when mousebutton clicked
                print(mouse_x, mouse_y)#output coordinates 
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_x >= 722 and mouse_x <= 896 and mouse_y >= 381 and mouse_y <= 435:
                time.sleep(0.125)#fixed bug
                Instructionstatus = False#ends the condition in while loop ending event loop
                                                                       
        gameDisplay.blit(instructionpagebackground,(5,5))#blits the instruction page ontop of main menu
        pygame.display.flip()#update the screen every iteration of clock
        clock.tick(fps_menu)#sets iteration e.g. how many times to update

def KartPicker(ts,GAMESTART):
  kartCounter = 0
  currentKart = karts[kartCounter]#index location of the kart in the list
  KPstatus = True
  while KPstatus:#kart picker eventloop
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        KPstatus = False

      mouse_x, mouse_y = pygame.mouse.get_pos()#gets the mouse location  x and y
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        print(mouse_x, mouse_y)
        
      if event.type == pygame.MOUSEBUTTONDOWN and mouse_x >= 8 and mouse_x <= 159  and mouse_y >= 391 and mouse_y <= 441:#checks for button presses within x and y coordinates
        time.sleep(0.125)#bug found here, used time.sleep to prevent it
        KPstatus = False #stops local eventloop   
      if event.type == pygame.MOUSEBUTTONDOWN and mouse_x >= 29 and mouse_x <= 239  and mouse_y >= 190 and mouse_y <= 261:#checks for button presses within x and y coordinates
        if kartCounter < 0:
          kartCounter = 5#sets max as 5
        else:
          kartCounter -= 1
          currentKart = karts[kartCounter]#current kart is whatever is selected at index location in kart list
      if event.type == pygame.MOUSEBUTTONDOWN and mouse_x >= 674 and mouse_x <= 885  and mouse_y >= 187 and mouse_y <= 261:#checks for button presses within x and y coordinates
        if kartCounter == 5:
          kartCounter = 0#if over boundary of 5, reset to 0
        else:
          kartCounter += 1
          currentKart = karts[kartCounter]              
      if event.type == pygame.MOUSEBUTTONDOWN and mouse_x >= 354 and mouse_x <=  566 and mouse_y >= 334 and mouse_y <= 406:#checks for button presses within x and y coordinate
        KPstatus = False#ends eventloop
        currentWidth = currentKart.get_width()
        currentHeight = currentKart.get_height()
        currentKart = pygame.transform.scale(currentKart,(int(currentWidth*0.5),int(currentHeight*0.5)))
        currentKart = pygame.transform.rotate(currentKart,-90)
        ts = True
        game = Game()#passes in the index location of the kart picked into class     
        game.run(currentKart, ts, GAMESTART)#creates object of main game class
               
      gameDisplay.blit(KPbackground,(0,0))#blits kart picker page onto screen
      gameDisplay.blit(currentKart, (440, 200))  #blits the index location kart in middle of screen
      pygame.display.flip()#updates any changes made
      #pygame.display.update()
      clock.tick(fps_menu)

def winningScreen():
  WSstatus = True
  while WSstatus:#kart picker eventloop
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        WSstatus = False

      if event.type == pygame.MOUSEBUTTONDOWN:#when mousebutton clicked
        mouse_x, mouse_y = pygame.mouse.get_pos()#gets the x and y of mouse position
        print(mouse_x, mouse_y)#output coordinates
      if event.type == pygame.MOUSEBUTTONDOWN and mouse_x >= 654  and mouse_x <= 910 and mouse_y >= 378 and mouse_y <= 445:# sets coordinates for detecting button press
        displayMenu(GAMESTART)#Starts the DisplayMenu Function with its own eventloop allowing it to be displayed on top
        WSstatus = False#end the game loop condition - ending game loop
    
      gameDisplay.blit(WinningScreen,(0,0))#blits winning screen
      pygame.display.flip()
      clock.tick(fps_menu)
displayMenu(GAMESTART)
