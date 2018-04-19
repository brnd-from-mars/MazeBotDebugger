import pygame as gui
import numpy as np
import serial
import _thread

pos = (0, 0, 3)

map = {}

vic = []

minX = 0
maxY = 0

lockM = False


def serialRead():
    global map, minX, maxY, lockM, pos
    
    ser = serial.Serial("/dev/cu.Mazebot-DevB", 38400, timeout=0.1)
    ser.reset_input_buffer()
    
    
    while True:
        line = str(ser.readline()).replace("b","").replace("\\r\\n","").replace("'","").split(" ")[:-1]
        
        flag = True
        
        try:
    
            for element in line:
                if element=="":
                    flag = False
                try:
                    int(element)
                    break
                except:
                    flag = False
        
            if(int(line[0])==255):
                while lockM:
                    pass
                lockM = True
                map = {}
                minX = 0
                maxY = 0
                vic = []
                lockM = False
                pos = (0, 0, 0)
        
            if (len(line)==3) and flag:
                pos = (int(line[0]), int(line[1]), int(line[2]))

            if (len(line)==8) and flag:
                if int(line[0])<minX:
                    minX = int(line[0])
                if int(line[1])>maxY:
                    maxY = int(line[1])
                while lockM:
                    pass
                lockM = True
                map[(int(line[0]),int(line[1]))] = [int(line[4]), int(line[5]), int(line[6]), int(line[7]), int(line[2]), int(line[3])]
                lockM = False

        except:
            pass


_thread.start_new_thread(serialRead, ())


gui.init()
gui.font.init()
screen = gui.display.set_mode((700, 700))
font = gui.font.SysFont("Helvetica", 18)

running = True

while running:
    screen.fill((0,64,0))
    
    for event in gui.event.get():
        if event.type == gui.KEYDOWN:
            if event.key == gui.K_ESCAPE:
                running = False
            if event.key == gui.K_r:
                while lockM:
                    pass
                lockM = True
                map = {}
                minX = 0
                maxY = 0
                pos = (0, 0, 0)
                lockM = False

    while lockM:
        pass
    lockM = True

    for key,value in map.items():
        nX = 100*(key[0]-minX)+50
        nY = 100*(maxY-key[1])+50
        
        if value[4]==0:
            gui.draw.rect(screen, (64, 64, 64), gui.Rect(nX, nY, 100, 100), 0)
        if value[4]==1:
            gui.draw.rect(screen, (192, 192, 192), gui.Rect(nX, nY, 100, 100), 0)
        if value[4]==2:
            gui.draw.rect(screen, (8, 8, 8), gui.Rect(nX, nY, 100, 100), 0)
        if value[4]==3:
            gui.draw.rect(screen, (0, 0, 255), gui.Rect(nX, nY, 100, 100), 0)
        if value[4]==4:
            gui.draw.rect(screen, (255, 255, 0), gui.Rect(nX, nY, 100, 100), 0)
        
        if value[0]==1:
            gui.draw.line(screen, (0,128,128), (nX+98, nY), (nX+98, nY+100), 5)
        if value[1]==1:
            gui.draw.line(screen, (0,128,128), (nX, nY+98), (nX+100, nY+98), 5)
        if value[2]==1:
            gui.draw.line(screen, (0,128,128), (nX+2, nY), (nX+2, nY+100), 5)
        if value[3]==1:
            gui.draw.line(screen, (0,128,128), (nX+100, nY+2), (nX, nY+2), 5)
        
        text = font.render(str(value[5]), True, (128, 128, 0))
        screen.blit(text, (nX+10, nY+10))

    for value in vic:
        nX = 100*(value[0]-minX)+50
        nY = 100*(maxY-value[1])+50
        if(value[3] == 0):
            gui.draw.rect(screen, (128,0,0), gui.Rect(nX+40, nY, nX+60, nY+20), 0)
        if(value[3] == 1):
            gui.draw.rect(screen, (128,0,0), gui.Rect(nX+80, nY+40, nX+100, nY+60), 0)
        if(value[3] == 2):
            gui.draw.rect(screen, (128,0,0), gui.Rect(nX+40, nY+80, nX+60, nY+100), 0)
        if(value[3] == 3):
            gui.draw.rect(screen, (128,0,0), gui.Rect(nX, nY+40, nX+20, nY+60), 0)

    # text = font.render(str(pos[3]), True, (255,255,255))
    # screen.blit(text, (10,10))
    

    lockM = False

    nX = 100*(pos[0]-minX)+90
    nY = 100*(maxY-pos[1])+90

    gui.draw.rect(screen, (255, 0, 0), gui.Rect(nX, nY, 20, 20), 0)

    if pos[2]==0:
        gui.draw.polygon(screen, (255,0,0), [(nX+20, nY), (nX+20, nY+20), (nX+30, nY+10)], 0)
    if pos[2]==1:
        gui.draw.polygon(screen, (255,0,0), [(nX, nY+20), (nX+20, nY+20), (nX+10, nY+30)], 0)
    if pos[2]==2:
        gui.draw.polygon(screen, (255,0,0), [(nX, nY), (nX, nY+20), (nX-10, nY+10)], 0)
    if pos[2]==3:
        gui.draw.polygon(screen, (255,0,0), [(nX, nY), (nX+20, nY), (nX+10, nY-10)])

    gui.display.flip()
