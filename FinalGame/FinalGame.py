# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 21:54:53 2019

@author: Jacky
"""

import tkinter as Tk
import random as rd
import winsound as ws
from PIL import Image, ImageTk
import threading as thd

WIDTH = 816 #width of the area that birds move in
HEIGHT = 550 #height of area that birds move in (at the grasslines)
WINWIDTH = 816 #width of game windows
WINHEIGHT = 768 #height of game window
MAXSPEED = 12 #max speed of birds, should be more than 40% higher than minimum speed
MINSPEED = 7 #minimum speed of birds
rd.seed()

'''
Create a regular bird, travels in a predictable direction and set speed
'''
class Bird(object):
    #canvas is where the bird is drawn in
    #posX and posY will be where the bird is spawned
    def __init__(self, canvas,posX, posY):
        self.speed = [rd.randrange(-1,2,2) * rd.uniform(MINSPEED,MAXSPEED), -rd.uniform(MINSPEED,MAXSPEED)]
        self.canvas = canvas
        self.frame = 0 #used to play different frames of the animation
        '''
        The gif is composed of several parts:
            Frame|
            1-4  | Flapping motion facing right
            5-8  | Flapping motion facing left
            9    | Bird is hit
            10-11| Bird is spinning as it falls down
        '''
        self.photo = Tk.PhotoImage(file="BirdAnim.gif", format="gif -index %s" %(self.frame))
        #places the bird on canvas at initial position
        self.shape = self.canvas.create_image(posX, posY, image=self.photo, anchor='nw')
        self.pos = self.canvas.coords(self.shape) #grabs coordinates of the bird
        self.points = 100 #points rewarded for hitting it
        '''
        'status' tracks the state the bird is currently in:
            0 | Not dead, still flying around
            1 | Got hit, freezes in place for a brief moment
            2 | Dying, slowly falls to the ground
            3 | Bird has reached the ground, gets marked for deletion
            4 | Bird has lived for too long, starts flying away
            5 | Bird has flown away, gets marked for deletion as a 'fly away'
        '''
        self.status = 0 #starts the bird off in state 0
        self.dFrame = 0 #separate number to track how long the bird has been in "death frames"

    #the game automatically runs 'update' in short intervals
    #'update' animates the birds, moving them to the new position and updating their status if it changes
    def update(self):
        self.pos = self.canvas.coords(self.shape)
        if self.status == 0: #Bird is alive and flying      
            if self.speed[0] < 0: #Bird is facing left (moving in -x direction)
                #loops frames 5-8
                self.photo = Tk.PhotoImage(file="BirdAnim.gif", format="gif -index %s" %(self.frame%4 + 4))
            else: #Bird is facing right
                #loops frames 1-4
                self.photo = Tk.PhotoImage(file="BirdAnim.gif", format="gif -index %s" %(self.frame%4))
            #updates the image on canvas
            self.shape = self.canvas.create_image(self.pos[0], self.pos[1], image=self.photo, anchor='nw')
            if self.pos[0]+70 >= WIDTH or self.pos[0] <= 0: #Bird has reached the left or right edge
                self.speed[0] *= -1 #flips horizontal direction
            if self.pos[1]+62 >= HEIGHT or self.pos[1] <= 0: #Bird has reached the top or bottom edge
                self.speed[1] *= -1 #flips vertical direction
            self.canvas.move(self.shape, self.speed[0], self.speed[1]) #moves bird to new position
            self.frame += 1 #makes bird display the next frame on next update
            if self.frame > 300: #Bird stayed alive for too long
                self.status = 4 #changes state to 'flying away'
        elif self.status == 1: #Bird got hit
            #like the original Duck Hunt, birds freeze in place briefly after getting hit
            #displays frame 9
            self.photo = Tk.PhotoImage(file="BirdAnim.gif", format="gif -index 8")
            self.shape = self.shape = self.canvas.create_image(self.pos[0], self.pos[1], image=self.photo, anchor='nw')
            self.dFrame += 1 #increments timer of how long it has been dead
            if self.dFrame > 15: #bird has been frozen in place for a while
                self.status = 2 #changes state to 2
        elif self.status == 2: #Bird is dying and falling down
            #loops frames 10 & 11 (spinning as it falls down)
            self.photo = Tk.PhotoImage(file="BirdAnim.gif", format="gif -index %s" %(self.dFrame%2 + 9))
            self.shape = self.canvas.create_image(self.pos[0], self.pos[1], image=self.photo, anchor='nw')
            self.canvas.move(self.shape, 0, 14) #bird is falling straight down
            self.dFrame += 1
            if self.pos[1] > 470: #reached the ground
                self.status = 3
        elif self.status == 3: #Bird is dead
            #doesn't do anything on update in this state
            return #game should detect that the bird is in state 3 and delete this bird
        elif self.status == 4: #Bird is flying away
            #plays the normal flying animation
            if self.speed[0] < 0:
                self.photo = Tk.PhotoImage(file="BirdAnim.gif", format="gif -index %s" %(self.frame%4 + 4))
            else:
                self.photo = Tk.PhotoImage(file="BirdAnim.gif", format="gif -index %s" %(self.frame%4))
            self.shape = self.canvas.create_image(self.pos[0], self.pos[1], image=self.photo, anchor='nw')
            #bird now flies straight up very quickly
            self.speed[0] = 0
            self.speed[1] = -20
            self.canvas.move(self.shape, self.speed[0], self.speed[1])
            self.frame += 1
            if self.pos[1] < -10: #bird has exited the screen
                self.status = 5 #move to state 5
        else: #status == 5, bird has flown away
            #doesn't do anything upon update
            return #game should detect this state, delete the bird, and make player lose a life

'''
create a 'tricky bird', similar to regular bird but randomly changes direction
functions and comments exactly the same as the normal bird except where commented
'''     
class trickyBird(Bird):
    def __init__(self, canvas,posX, posY):
        #minimum speed is 20% higher so it moves faster on average
        self.speed = [rd.randrange(-1,2,2) * rd.uniform(MINSPEED * 1.2,MAXSPEED), -rd.uniform(MINSPEED * 1.2,MAXSPEED)]
        self.canvas = canvas
        self.frame = 0
        #gif is in the same format as regular bird, just recolored
        self.photo = Tk.PhotoImage(file="TrickyBirdAnim.gif", format="gif -index %s" %(self.frame))
        self.shape = self.canvas.create_image(posX, posY, image=self.photo, anchor='nw')
        self.pos = self.canvas.coords(self.shape)
        self.points = 250 #rewards 250 points instead
        self.status = 0
        self.dFrame = 0
        
    def update(self):
        self.pos = self.canvas.coords(self.shape)
        if self.status == 0:           
            if self.speed[0] < 0:
                self.photo = Tk.PhotoImage(file="TrickyBirdAnim.gif", format="gif -index %s" %(self.frame%4 + 4))
            else:
                self.photo = Tk.PhotoImage(file="TrickyBirdAnim.gif", format="gif -index %s" %(self.frame%4))
            self.shape = self.canvas.create_image(self.pos[0], self.pos[1], image=self.photo, anchor='nw')
            if self.pos[0]+70 >= WIDTH or self.pos[0] <= 0:
                self.speed[0] *= -1
            if self.pos[1]+62 >= HEIGHT or self.pos[1] <= 0:
                self.speed[1] *= -1
            
            #randomly changes directions
            if (rd.random() < 0.07): #chance to trigger on each update
                for i in range(2):
                    #if not at an edge
                    if self.pos[0]+70 <= WIDTH and self.pos[0] >= 10 and self.pos[1]+62 <= HEIGHT or self.pos[1] >= 10:
                        #rd.randrange(-1,2,2) generates either -1 or 1
                        #it has a 50% chance of flipping directions for horizontal and vertical movement
                        self.speed[i] *= rd.randrange(-1,2,2)
            self.canvas.move(self.shape, self.speed[0], self.speed[1])
            self.frame += 1
            if self.frame > 300:
                self.status = 4
        elif self.status == 1:
            self.photo = Tk.PhotoImage(file="TrickyBirdAnim.gif", format="gif -index 8")
            self.shape = self.shape = self.canvas.create_image(self.pos[0], self.pos[1], image=self.photo, anchor='nw')
            self.dFrame += 1
            if self.dFrame > 15:
                self.status = 2
        elif self.status == 2:
            self.photo = Tk.PhotoImage(file="TrickyBirdAnim.gif", format="gif -index %s" %(self.dFrame%2 + 9))
            self.shape = self.canvas.create_image(self.pos[0], self.pos[1], image=self.photo, anchor='nw')
            self.canvas.move(self.shape, 0, 14)
            self.dFrame += 1
            if self.pos[1] > 470:
                self.status = 3
        elif self.status == 3:
            return
        elif self.status == 4:
            if self.speed[0] < 0:
                self.photo = Tk.PhotoImage(file="TrickyBirdAnim.gif", format="gif -index %s" %(self.frame%4 + 4))
            else:
                self.photo = Tk.PhotoImage(file="TrickyBirdAnim.gif", format="gif -index %s" %(self.frame%4))
            self.shape = self.canvas.create_image(self.pos[0], self.pos[1], image=self.photo, anchor='nw')
            self.speed[0] = 0
            self.speed[1] = -20
            self.canvas.move(self.shape, self.speed[0], self.speed[1])
            self.frame += 1
            if self.pos[1] < -10:
                self.status = 5
        else:
            return
  
'''      
creates an 'MLG bird', frequently changes directions and fluctuates in speed
also the same as a regular bird except where it's commented 
'''
class MLGBird(Bird):
    def __init__(self, canvas,posX, posY):
        #minimum speed is 40% higher, resulting in a higher average speed
        self.speed = [rd.randrange(-1,2,2) * rd.uniform(MINSPEED * 1.4,MAXSPEED), -rd.uniform(MINSPEED * 1.4,MAXSPEED)]
        self.canvas = canvas
        self.frame = 0
        #gif is in same format, just recolored
        self.photo = Tk.PhotoImage(file="MLGBirdAnim.gif", format="gif -index %s" %(self.frame))
        self.shape = self.canvas.create_image(posX, posY, image=self.photo, anchor='nw')
        self.pos = self.canvas.coords(self.shape)
        self.points = 600 #rewards 600 points instead
        self.status = 0
        self.dFrame = 0
        
    def update(self):
        self.pos = self.canvas.coords(self.shape)
        if self.status == 0:   
            if self.speed[0] < 0:
                self.photo = Tk.PhotoImage(file="MLGBirdAnim.gif", format="gif -index %s" %(self.frame%4 + 4))
            else:
                self.photo = Tk.PhotoImage(file="MLGBirdAnim.gif", format="gif -index %s" %(self.frame%4))
            self.shape = self.canvas.create_image(self.pos[0], self.pos[1], image=self.photo, anchor='nw')
            if self.pos[0]+70+MAXSPEED >= WIDTH or self.pos[0]+MAXSPEED <= 0:
                self.speed[0] *= -1
            if self.pos[1]+62+MAXSPEED >= HEIGHT or self.pos[1]+MAXSPEED <= 0:
                self.speed[1] *= -1
            
            #randomly changes direction and speed
            if (rd.random() < 0.13): #has a chance to proc on each update 
                for i in range(2): #for horizontal and vertical movement
                    #not at an edge
                    if self.pos[0]+70 <= WIDTH and self.pos[0] >= 10 and self.pos[1]+62 <= HEIGHT or self.pos[1] >= 10:
                        #50% chance to flip direction
                        self.speed[i] *= rd.randrange(-1,2,2)
            for i in range(2): #for vertical and horizontal movement
                if abs(self.speed[i]) < MAXSPEED: #not already moving at max speed
                    self.speed[i] *= rd.uniform(1.03,1.2) #makes it move 3-20% faster
                if abs(self.speed[i]) > MAXSPEED: #exceeded max speed
                    self.speed[i] *= rd.uniform(0.5,0.83) #drops it to 50-83% of current speed
            self.canvas.move(self.shape, self.speed[0], self.speed[1])
            self.frame += 1
            if self.frame > 300:
                self.status = 4
        elif self.status == 1:
            self.photo = Tk.PhotoImage(file="MLGBirdAnim.gif", format="gif -index 8")
            self.shape = self.shape = self.canvas.create_image(self.pos[0], self.pos[1], image=self.photo, anchor='nw')
            self.dFrame += 1
            if self.dFrame > 15:
                self.status = 2
        elif self.status == 2:
            self.photo = Tk.PhotoImage(file="MLGBirdAnim.gif", format="gif -index %s" %(self.dFrame%2 + 9))
            self.shape = self.canvas.create_image(self.pos[0], self.pos[1], image=self.photo, anchor='nw')
            self.canvas.move(self.shape, 0, 14)
            self.dFrame += 1
            if self.pos[1] > 470:
                self.status = 3
        elif self.status == 3:
            #self.photo = Tk.PhotoImage(file="blank.gif", format="gif")
            return
        elif self.status == 4:
            if self.speed[0] < 0:
                self.photo = Tk.PhotoImage(file="MLGBirdAnim.gif", format="gif -index %s" %(self.frame%4 + 4))
            else:
                self.photo = Tk.PhotoImage(file="MLGBirdAnim.gif", format="gif -index %s" %(self.frame%4))
            self.shape = self.canvas.create_image(self.pos[0], self.pos[1], image=self.photo, anchor='nw')
            self.speed[0] = 0
            self.speed[1] = -20
            self.canvas.move(self.shape, self.speed[0], self.speed[1])
            self.frame += 1
            if self.pos[1] < -10:
                self.status = 5
        else:
            return

#This object displays an ammo counter in the game
class ammoCount(object):
    def __init__(self, canvas):
        self.canvas = canvas
        self.photo = ImageTk.PhotoImage(Image.open('shot5.png')) #starts ammo at 5 shots
        #place counter on screen
        self.shape = self.canvas.create_image(70, WINHEIGHT - 110, image = self.photo, anchor='nw')
    
    def update(self, count): #update is ran when the ammo count changes, takes 'count' as the new count
        #images are named as 'shotX.png' where X is the number of shots to display (0-5)
        self.photo = ImageTk.PhotoImage(Image.open("shot%s.png" %(count))) #updates graphic
        self.shape = self.canvas.create_image(70, WINHEIGHT - 110, image = self.photo, anchor='nw')

class GIF(object): #a gif object
    #name is the name of file
    #xPos and yPos is the location to place it
    #frames is the total frames the gif has to allow looping and prevent out of range errors
    def __init__(self, canvas, name, xPos, yPos, frames):
        self.canvas = canvas
        self.name = name
        self.img = Tk.PhotoImage(file=name, format="gif -index 0") #starts at frame 1
        self.pos = [xPos, yPos]
        #displays gif at specified location
        self.shape = self.canvas.create_image(self.pos[0], self.pos[1], image = self.img, anchor='nw')
        self.frames = frames #total frames of gifs
        self.frame = 0 #tracks the current frame the gif is in
        self.loops = 0 #number of times it has looped
    
    def update(self):
        if self.frame < self.frames - 1: #if it has not reached the last frame of gif
            self.frame += 1 #increment frame
        else: #has reached last frame of gif
            self.frame = 0 #sets current frame back to 0
        #displays the current frame the gif should be in
        self.img = Tk.PhotoImage(file=self.name, format="gif -index %s" %self.frame)
        self.shape = self.canvas.create_image(self.pos[0], self.pos[1], image = self.img, anchor='nw')
        if (self.frame%self.frames) == 0: #gif has looped back to beginning (displayed frame 1)
            self.loops += 1 #increment loops counter
            
'''
Main game
'''     
class DankHunt(object):
    def __init__(self, root):
        #sets up the root and canvas
        self.root = root
        self.canvas = Tk.Canvas(root, width=WINWIDTH, height=WINHEIGHT, bg="white")
        self.canvas.pack()
        #opens background image and displays it
        self.BGIMG = ImageTk.PhotoImage(Image.open('BG.png'))
        self.canvas.create_image(0,0, image=self.BGIMG, anchor='nw')
        self.points = 0 #counter for player score
        #displays score counter on screen
        self.score = Tk.Label(root, text="Score: %d" % self.points)
        self.score.pack()
        self.score.place(x=570, y=WINHEIGHT-90)
        
        #commands for the game
        #left click to shoot and right click to reload
        #pressing p can pause the game
        self.canvas.bind("<Button-1>", self.fire)
        self.canvas.bind("<Button-3>", self.reloadCycle)
        self.canvas.focus_set() #allows pausing to function
        self.canvas.bind("<p>", self.pause)
        self.Birds = [] #keeps track of birds in game
        self.gifs = [] #keeps track of gifs being displayed in game
        self.active = True #game is currently running
        self.update() #start the update loop
        self.hitmarks = [] #keeps track of hitmarks being displayed
        self.update_hitmark() #loop to remove hitmarks after enough time
        self.hitmark = ImageTk.PhotoImage(Image.open('hitmarker.png')) #image file for hitmarker
        self.shots = 5 #shots player currently has, starts at 5
        self.ammoCounter = ammoCount(self.canvas) #displays ammo counter on screen
        self.lives = 3 #lives player currently has, starts at 3
        self.hits = 0 #how many birds the player has hit
        self.root.after(2000, self.spawnLoop) #waits 1 second before spawning birds
        ws.PlaySound('airhorn.wav', ws.SND_ASYNC)
    
    #function to spawn a bird
    def spawnBird(self):
        rng = rd.random() #generates a random number between 0 and 1
        if (rng <= 0.15): #15% chance to be an MLG Bird
            #spawns a bird randomly along the grass
            #rd.uniform(70, WIDTH - 70) keeps bird inside left and right edge of the game
            #470 is approximately where the grass height is and spawns them there
            bird = MLGBird(self.canvas, rd.uniform(70,WIDTH - 70),470)
        elif (rng <= 0.5): #35% chance to be a Tricky Bird
            bird = trickyBird(self.canvas, rd.uniform(70,WIDTH - 70),470)
        else: #50% chance to spawn a regular bird
            bird = Bird(self.canvas, rd.uniform(70,WIDTH - 70),470)
        self.Birds.append(bird) #adds the bird to list of birds
    
    #loop to continuously spawn birds
    def spawnLoop(self):
        interval = int(rd.uniform(400, 2400)) #interval to wait before spawning another bird
        self.spawnBird() #spawn a bird
        self.root.after(interval, self.spawnLoop) #loops function
    
    #updates current score of player when called
    def updateScore(self):
        self.score["text"] = "%d points" % self.points
    
    #loop to remove hitmarks after some time
    def update_hitmark(self):
        if len(self.hitmarks) > 0: #there are currently hitmarks on the screen
            self.canvas.delete(self.hitmarks[0]) #deletes oldest one from canvas
            del self.hitmarks[0] #removes it from table
        self.root.after(750, self.update_hitmark) #waits 750ms before running again
    
    #fires a shot at the mouse location
    def fire(self, event):
        if self.shots > 0: #player has a shot available
            self.shots -= 1 #subtracts the shot
            self.ammoCounter.update(self.shots) #updats ammo counter
            clickedBirds = [bird for bird in self.Birds #checks each bird in the game
                            if event.x <= bird.pos[0]+70 and event.x >= bird.pos[0] #click lines up horizontally with bird
                            and event.y <= bird.pos[1]+62 and event.y >= bird.pos[1] #click lines up vertically with bird
                            and bird.status == 0] #bird is still alive and not flying away/dying
            if len(clickedBirds): #at least 1 bird was clicked
                #create a hitmark where player clicked
                hitmark = self.canvas.create_image(event.x, event.y, image=self.hitmark)
                self.hitmarks.append(hitmark)
                #plays sound upon successful hit
                ws.PlaySound('hitsound.wav', ws.SND_ASYNC)
                
                clicked = self.Birds.index(clickedBirds[0]) #gets index of oldest clicked bird
                self.Birds[clicked].status = 1 #sets status to 1 (dying, freeze in place)
                self.points += self.Birds[clicked].points #adds the respective point value of bird to score
                self.updateScore() #update score count
                self.hits += 1 #increment hit count
                if (self.hits == 10): #every 10 hits show a rainbow frog on screen
                    self.showFrog()
            else: #player has missed
                #play sound for missing
                ws.PlaySound('bulletMiss.wav', ws.SND_ASYNC)    
        else: #player does not have a shot available or is currently reloading
            #does nothing, only plays sound
            ws.PlaySound('noAmmo.wav', ws.SND_ASYNC)

    #loop to update the game
    def update(self):
        if self.active: #game is currently unpaused
            for bird in self.Birds: #for each bird currently in game
                bird.update() #update each bird
                if bird.status == 3 or bird.status == 5: #bird has either died or flown away
                    if bird.status == 5: #if flown away
                        self.flyAway() #run function when a bird has flown away
                        ws.PlaySound('oof.wav', ws.SND_ASYNC) #play sound
                        if self.lives == 0: #player has run out of lives
                            self.gameOver() #move to game over screen
                    dead = self.Birds.index(bird) #gets index of dead bird
                    del self.Birds[dead] #delete bird from table
            for gif in self.gifs: #for each gif currently in game
                gif.update() #update it for animation
                if gif.loops > 8: #gif has looped 10 times
                    end = self.gifs.index(gif) #gets index of gif to remove
                    del self.gifs[end] #delete it
            self.root.after(20, self.update) #updates every 20ms
      
    #called when player has finished reloading ammo
    def reloadAmmo(self):
        self.shots = 5 #set shots to 5
        self.ammoCounter.update(self.shots) #update ammo counter
    
    #player has right clicked to start reloading
    def reloadCycle(self, event):
        self.shots = 0 #sets shots to 0 so player can't shoot while reloading
        ws.PlaySound('reload.wav', ws.SND_ASYNC) #plays reloading sound
        thd.Thread(target=self.startReload).start() #starts the wait for reload
        #thd.Thread is used to run it in a separate thread so it doesn't stop the rest of the game from running
    
    #called when reload starts        
    def startReload(self):
        #after 1000ms, finish the reload
        self.root.after(1000, self.reloadAmmo) 
    
    #called when a bird has flown away
    def flyAway(self):
        self.lives -= 1 #reduces the lives a player has
        print ('You have', self.lives, 'lives left.') #tell how many lives left
    
    #pauses/unpauses the game
    def pause(self, event):
        print ("pausing/ unpausing")
        if self.active == True: #game is currently unpause
            self.active = False #sets it to inactive, stopping the update loop
        else: #game is currently paused
            self.active = True #set it back to active
            self.update() #starts update loop again
    
    #plays a gif at a specified location
    #img is the file name
    #xPos yPos is locationt to place the gif
    #frames is the total # of frames in gif
    def playGIF(self, img, xPos, yPos, frames):
        gif = GIF(self.canvas, img, xPos, yPos, frames) #create gif object
        self.gifs.append(gif) #add it to list of gifs
    
    #displays a rainbow frog on screen when called (every 10 hits)   
    def showFrog(self):
        frog = GIF(self.canvas, 'MLGFrog.gif', 340 , WINHEIGHT - 150, 10)
        self.gifs.append(frog)
        self.hits = 0 #set hitcounter back to 0
    
    #called when player loses all lives, moves to game over screen
    def gameOver(self):
        self.active = 0 #sets it to inactive
        self.canvas.pack_forget() #wipes the canvas
        game = GameOver(self.root, self.points) #creates game over screen
        print ("You have lost :(")

'''
Menu Screen
'''

class Menu(object):
     def __init__(self, root):
        #set up root and canvas
        self.root = root
        self.canvas = Tk.Canvas(root, width=WINWIDTH, height=WINHEIGHT, bg="white")
        self.canvas.pack()
        #import menu screen and displays it
        self.BGIMG = ImageTk.PhotoImage(Image.open('menu.png'))
        self.canvas.create_image(0,0, image=self.BGIMG, anchor='nw')
        #starts the game once the player inputs any key
        self.canvas.focus_set()
        self.canvas.bind("<Key>", self.startGame)
    
     def startGame(self, event):
        self.canvas.pack_forget() #wipes canvas
        game = DankHunt(self.root) #starts the game

'''
Game Over Screen
'''
class GameOver(object):
    #'score' is how much the player has scored in the game
    def __init__(self, root, score):
        #set up canvas
        self.root = root
        self.canvas = Tk.Canvas(root, width=WINWIDTH, height=WINHEIGHT, bg="white")
        self.canvas.pack()
        #import game over screen and displays it
        self.img = ImageTk.PhotoImage(Image.open('GameOver.png'))
        self.canvas.create_image(0,0, image=self.img, anchor='nw')
        ws.PlaySound('SadViolin.wav', ws.SND_ASYNC|ws.SND_LOOP) #plays game over music on a loop
        #label to display score of player
        self.score = Tk.Label(root, text="%d" % score, font=("Arial", 34), height=1, width = 10)
        self.score.pack()
        self.score.place(x=230, y=WINHEIGHT-230)
        #button player can click to restart the game
        self.restart = Tk.Button(root, text="Retry", command = self.startGame, height = 2, width = 7)
        self.restart.pack()
        self.restart.place(x=370, y=WINHEIGHT-130)
        self.restart.bind("<Enter>", self.buttonHover) #player hovers over button
        self.restart.bind("<Leave>", self.buttonLeave) #stops hovering over button
   
    #starting a new game     
    def startGame(self):
        self.canvas.pack_forget() #clears canvas
        ws.PlaySound(None, ws.SND_FILENAME) #stops game over music
        game = DankHunt(self.root) #starts the game
    
    #hovering over restart button
    def buttonHover(self, event):
        self.restart['background'] = 'green' #changes color to green
    
    #stops hovering over restart button    
    def buttonLeave(self, event):
        self.restart['background'] = 'white' #changes color to white
      
def main(): 
    root = Tk.Tk()
    start = Menu(root)
    root.mainloop()

if __name__ == '__main__':
    main()