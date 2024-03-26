from sense_hat import SenseHat
from time import sleep
from random import choice

sense = SenseHat()

w = (255,255,255)
g = (0,160,0)
r = (255,0,0)
b = (0,0,0)

w_arrow = [
b,b,b,w,w,b,b,b,
b,b,w,w,w,w,b,b,
b,w,w,w,w,w,w,b,
w,w,w,w,w,w,w,w,
b,b,b,w,w,b,b,b,
b,b,b,w,w,b,b,b,
b,b,b,w,w,b,b,b,
b,b,b,w,w,b,b,b
]

g_arrow = [
b,b,b,g,g,b,b,b,
b,b,g,g,g,g,b,b,
b,g,g,g,g,g,g,b,
g,g,g,g,g,g,g,g,
b,b,b,g,g,b,b,b,
b,b,b,g,g,b,b,b,
b,b,b,g,g,b,b,b,
b,b,b,g,g,b,b,b
]

r_arrow = [
b,b,b,r,r,b,b,b,
b,b,r,r,r,r,b,b,
b,r,r,r,r,r,r,b,
r,r,r,r,r,r,r,r,
b,b,b,r,r,b,b,b,
b,b,b,r,r,b,b,b,
b,b,b,r,r,b,b,b,
b,b,b,r,r,b,b,b
]

pause = 3
score = 0
angle = 0
play = True
UserIn = True
level = 1

angles = []
user_in = []
ctr = 0


while play :
    for i in range(level):
        #Generate angle
        last_angle = angle
        while angle == last_angle:
            angle = choice([0,90,180,270])
        #Store angle to be compared with user input
        angles.append(angle)
        #Show arrow and wait to show next one (if level>1)
        sense.set_rotation(angle)
        sense.set_pixels(w_arrow)
        sleep(pause)
        sense.clear()
    
    #Down=0,Left=90,Up=180,Right=270,Middle:Done with sequence
    while UserIn:
        for event in sense.stick.get_events():
            if event.direction == "up":
                print("UP")
                sense.set_rotation(0)
                sense.set_pixels(w_arrow)
                #Check to make sure arrow before isn't the same
                #Sense hat is finicky, usually reads in double input
                if (len(user_in) == 0) or (user_in[ctr-1] != 0):
                    user_in.append(0)
                    ctr += 1
            elif event.direction == "down":
                print("DOWN")
                sense.set_rotation(180)
                sense.set_pixels(w_arrow)
                if (len(user_in) == 0) or (user_in[ctr-1] != 180):
                    user_in.append(180)
                    ctr += 1
            elif event.direction == "left":
                print("LEFT")
                sense.set_rotation(270)
                sense.set_pixels(w_arrow)
                if (len(user_in) == 0) or (user_in[ctr-1] != 270):
                    user_in.append(270)
                    ctr += 1
            elif event.direction == "right":
                print("RIGHT")
                sense.set_rotation(90)
                sense.set_pixels(w_arrow)
                if (len(user_in) == 0) or (user_in[ctr-1] != 90):
                    user_in.append(90)
                    ctr += 1
            #End user input
            elif event.direction == "middle":
                print("M")
                UserIn = False
                break
            
        sleep(0.5)
        sense.clear()
            
    #Round over, time to compare
    if len(user_in) != level:
        play = False
#       sense.clear(255,0,0)
    else:
        for i in range(level):
            sense.clear()
            if angles[i] == user_in[i]:
                sense.set_rotation(user_in[i])
                sense.set_pixels(g_arrow)
                sleep(1)
            else:
                sense.set_rotation(user_in[i])
                sense.set_pixels(r_arrow)
                sleep(1)
                play = False
                break
    
    if play:
        #Shorten the pause duration slightly  
        pause = pause * 0.95
        #Update score and level
        score += 1
        level += 1
        #Reset boolean and counter
        UserIn = True
        ctr = 0
        #Remove all elements of both arrays
        angles.clear()
        user_in.clear()
        #Notify user next round is coming
        sense.set_rotation(0)
        won_msg = "Great Job! Level: %d" % level
        sense.show_message(won_msg,scroll_speed=0.05)
        #Pause before the next round 
        sleep(1)
            
#Score after loss
sense.set_rotation(0)
l_msg = "Sorry, you lost"
sense.show_message(l_msg)
msg = "Your score: %s" % score
sense.show_message(msg, scroll_speed=0.05, text_colour=[100, 100, 100])