##from serial import serial
import pygame, math, time, traceback, serial
import logging
logging.basicConfig(level=logging.WARNING, format=' %(asctime)s - %(levelname)s- %(message)s')

ser = serial.Serial('COM6',9600)
pygame.init()
#Define font
pygame.font.init()
fontsize = 18
font=pygame.font.SysFont('Comic Sans MS',fontsize)

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
#Colours
axiscolour=GREEN
pingcolour=RED
textcolour=WHITE
#Define Size
size = (1000, 600)
xsize = size[0]
xmid=xsize/2
ysize = size[1]
ymid=ysize/2
Footerheight = 50
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Robot Sonar")

#Create Sonar list
ping = []
for i in range(1,180):
    ping.append([i,0])

time.sleep(2)
# Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

    # --- Drawing code should go here
    # First, clear the screen to Black. Don't put other drawing commands
    # above this, or they will be erased with this command.
    try:
        logging.info('Screen drawn')
        screen.fill(BLACK)
        pygame.draw.line(screen, axiscolour, [0,ysize-Footerheight],[xsize,ysize-Footerheight])
        pygame.draw.circle(screen, axiscolour,(int(xmid),int(ysize-Footerheight)),int(xmid),1) #Large circle
        pygame.draw.circle(screen, axiscolour,(int(xmid),int(ysize-Footerheight)),int(xmid*0.75),1)  #3/4 Circle
        pygame.draw.circle(screen, axiscolour,(int(xmid),int(ysize-Footerheight)),int(xmid*0.5),1)  #1/2 Circle
        pygame.draw.circle(screen, axiscolour,(int(xmid),int(ysize-Footerheight)),int(xmid*0.25),1)  #1/4 Circle
        pygame.draw.rect(screen, BLACK, [0,ysize,xsize,-(Footerheight-2)],0)
        m1 = font.render('1m', False, (WHITE))
        m2 = font.render('2m', False, (WHITE))
        m3 = font.render('3m', False, (WHITE))
        m4 = font.render('4m', False, (WHITE))
        textoffset = 2
        screen.blit(m1,(xmid-xmid*0.25,ysize-Footerheight+textoffset))
        screen.blit(m2,(xmid-xmid*0.5,ysize-Footerheight+textoffset))
        screen.blit(m3,(xmid-xmid*0.75,ysize-Footerheight+textoffset))
        screen.blit(m4,(xmid-xmid,ysize-Footerheight+textoffset))
        pygame.display.flip()
        linesdrawn=0

        while linesdrawn <180:
            if event.type == pygame.QUIT:
                pygame.quit
                break
            if ser.in_waiting > 7:
                data=ser.readline()
                if len(data) <6:
                    logging.warning('bad data recieved: '+ str(data))
                    break
                logging.debug('into read loop')
                #logging.info(data)
                deg =[]
                i=0
                dist = []
                while data[i] != 44:  #44 is ASCII code for ,
                    deg.append(int(chr(data[i])))
                    i=i+1
                if len(deg) ==1:
                    deg = int(deg[0])
                elif len(deg) ==2:
                    deg=int((str(deg[0]))+str(deg[1]))
                elif len(deg) ==3:
                    deg=int((str(deg[0]))+str(deg[1])+str(deg[2]))
                logging.info('deg = '+str(deg))
                i = i+1
                while data[i] != 13: #ACII code for \r
                    #logging.debug('i = '+ str(i))
                    dist.append(int(chr(data[i])))
                    i=i+1
                if len(dist) ==1:
                    dist = int(dist[0])
                elif len(dist) ==2:
                    dist=int((str(dist[0]))+str(dist[1]))
                elif len(dist) ==3:
                    dist=int((str(dist[0]))+str(dist[1])+str(dist[2]))
                elif len (dist) >3:
                    logging.warning('suspect distance reading' + str(dist))
                    dist = 400
                if dist > 400:
                    dist = 400
                logging.info('dist =' +str(dist))
                scaleRatio = 400/xmid    #400cm is max range of sensor
                scaleDist = scaleRatio * dist
                linesdrawn = linesdrawn +1
                            
                pingx = xmid-(scaleDist*math.cos(math.radians(deg)))
                pingy = ysize-Footerheight-(scaleDist*math.sin(math.radians(deg)))
                pygame.draw.line(screen,axiscolour,[xmid,ysize-Footerheight],[pingx,pingy])
                pygame.draw.line(screen,pingcolour,[pingx,pingy],[pingx-((xmid-scaleDist)*math.cos(math.radians(deg))),(pingy-(((xmid-scaleDist)*math.sin(math.radians(deg)))))])          
                pygame.display.flip()
                deg=[]
                dist=[]    
    except TypeError:
        print("Type error")
        traceback.print_exc()
        ser.close()
        break
    pygame.display.flip()
    clock.tick(20)
pygame.quit()

ser.close()

#
