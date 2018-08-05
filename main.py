# import modules
import pygame
import math
import time
import os

# initialize the display
os.environ["SDL_FBDEV"] = "/dev/fb1"

# initialize pygame
pygame.init()

# some basic color definitions
white=(255,255,255)
black=(0,0,0)
lightGrey=(192,192,192)
darkGrey=(64,64,64)
grey=(128,128,128)
red=(0,0,255)
green=(0,255,0)
blue=(0,0,255)

# some basic day and month definitions
daysOfTheWeek=('Mon','Tue','Wed','Thu','Fri','Sat','Sun')
monthsOfTheYear=('ErrMonth','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')

# setup the display
displayWidth = 160
displayHeight = 128
uiDisplay = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('ui')

# update the display
#pygame.display.flip() can also be used but is less common
pygame.display.update()

#hide the mouse
pygame.mouse.set_visible(False)

#pixAr=pygame.PixelArray(uiDisplay)
#pixAr[10][20] = green

# set the default font
smallFont=pygame.font.SysFont(None,15)
mediumFont=pygame.font.SysFont(None,20)
defaultFont=pygame.font.SysFont(None,25)
largeFont=pygame.font.SysFont(None,30)
analogClockFont=pygame.font.SysFont(None,22)

# setup the fps clock
clock = pygame.time.Clock()

def polarLine(uiDisplay,color,angleDegrees,radius,centerpoint,nullspace,lineWidth):
    angleRadians=math.radians(angleDegrees+270)
    xfarcord=((math.cos(angleRadians)*radius)+(centerpoint[0]))
    yfarcord=((math.sin(angleRadians)*radius)+(centerpoint[1]))
    xnearcord=((math.cos(angleRadians)*nullspace)+(centerpoint[0]))
    ynearcord=((math.sin(angleRadians)*nullspace)+(centerpoint[1]))
    nearCoordinates=(xnearcord,ynearcord)
    farCoordinates=(xfarcord,yfarcord)
    pygame.draw.line(uiDisplay,color,nearCoordinates,farCoordinates,lineWidth)

def centeredPolarLine(uiDisplay,color,angleDegrees,radius,centerPoint,lineWidth):
    angleRadians=math.radians(angleDegrees+270)
    coords=(((math.cos(angleRadians)*radius)+(centerPoint[0])),((math.sin(angleRadians)*radius)+(centerPoint[1])))
    pygame.draw.line(uiDisplay,color,centerPoint,coords,lineWidth)

def postTextSimple(msg,color,location,font):
    if font=="analogClockFont":
        screen_text=analogClockFont.render(msg, True, color)
    else:
        screen_text=defaultFont.render(msg, True, color)
    uiDisplay.blit(screen_text,location)


def text_objects(text,color,font):
    if font=="analogClockFont":
        textSurface=analogClockFont.render(text, True, color)
    else:
        textSurface=defaultFont.render(text, True, color)
    return textSurface, textSurface.get_rect()


def postTextCentered(msg,color,xDisplace=0,yDisplace=0,font="defaultFont"):
    textSurf, textRect = text_objects(msg,color,font)
    #screen_text=font.render(msg, True, color)
    #uiDisplay.blit(screen_text,location)
    textRect.center = (displayWidth/2)+xDisplace,(displayHeight/2)+yDisplace
    uiDisplay.blit(textSurf, textRect)


def uiDScheduleLoop():
    # setup the uiExit variable
    uiExit = False
    while not uiExit:        
        # event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                uiExit = True
            if event.type == pygame.KEYDOWN:
                print(event)
                if event.key == 27:
                    uiExit = True
            #print(event)
        
        uiDisplay.fill(black)
        postTextCentered("hello",white,0,0)
        pygame.display.update()
        # set the frames per second to 30, the correctnumber for the clock
        clock.tick(30)

    # close out the display
    pygame.quit()

    
def uiAnalogClockLoop():    
    # setup the uiExit variable
    uiExit = False
    
    # setup the clock data
    clockTime=time.localtime(None)
    rotationSecondHand=clockTime.tm_sec*6
    rotationMinuteHand=clockTime.tm_min*6
    rotationHourHand=clockTime.tm_hour*30
    currentMonth=monthsOfTheYear[clockTime.tm_mon]
    currentNumday=str(clockTime.tm_mday)
    currentWeekday=daysOfTheWeek[clockTime.tm_wday]
    currentYear=str(clockTime.tm_year)
    selectionColor=(160,0,255)
    # create clock testing data ( activate for debugging purposes )
    #digitalTime=(clockTime.tm_hour,clockTime.tm_min,clockTime.tm_sec)
    #dateTime=(daysOfTheWeek[clockTime.tm_wday],clockTime.tm_mday,monthsOfTheYear[clockTime.tm_mon],clockTime.tm_year)
    
    while not uiExit:        
        # event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                uiExit = True
            if event.type == pygame.KEYDOWN:
                print(event)
                if event.key == 27:
                    uiExit = True
            #print(event)
                    
        # The actual graphics code

        # Clear the display
        uiDisplay.fill(black)
        
        # Incriment second hand rotation
        if rotationSecondHand<=360.4:
            rotationSecondHand+=0.58
        else:
            # Update the time
            clockTime=time.localtime(None)
            rotationSecondHand=(clockTime.tm_sec*6)
            rotationMinuteHand=int(clockTime.tm_min*6)
            rotationHourHand=int(clockTime.tm_hour*30)
            # Update the date
            currentMonth=monthsOfTheYear[clockTime.tm_mon]
            currentNumday=str(clockTime.tm_mday)
            currentWeekday=daysOfTheWeek[clockTime.tm_wday]
            currentYear=str(clockTime.tm_year)
        
        # add the date data to the screen
        postTextSimple(currentMonth,lightGrey,[4,24],"analogClockFont")
        postTextSimple(currentNumday,lightGrey,[12,40],"analogClockFont")
        postTextSimple(currentWeekday,lightGrey,[4,95],"analogClockFont")
        postTextSimple(currentYear,lightGrey,[4,110],"analogClockFont")
        
        # Draw the circle for the watch face
        pygame.draw.circle(uiDisplay,grey,(96,64),64,4)
        
        # Draw the watch face deliniations
        #12 Big Marks
        for i in range(12):
            polarLine(uiDisplay,grey,int(i*30),60,(96,64),52,4)
            #Create 4 small marks for each big mark
            for n in range(4):
                polarLine(uiDisplay,grey,int(i*30)+n*6+6,60,(96,64),56,2)
                
        # Draw the hands
        # Second hand
        centeredPolarLine(uiDisplay,red,rotationSecondHand,54,(96,64),4)
        # Minute hand
        centeredPolarLine(uiDisplay,lightGrey,rotationMinuteHand,54,(96,64),4)
        # Hour hand
        centeredPolarLine(uiDisplay,lightGrey,rotationHourHand,30,(96,64),4)
        # Draw the center bubble of the watch hands
        pygame.draw.circle(uiDisplay,darkGrey,(96,64),6,0)

        # Draw the selector
        pygame.draw.rect(uiDisplay,darkGrey,[5,5,14,14])
        pygame.draw.rect(uiDisplay,lightGrey,[9,9,6,6])
        pygame.draw.rect(uiDisplay,selectionColor,[10,10,4,4])
        
        # update our display
        pygame.display.update()
        # set the frames per second to 30, the correctnumber for the clock
        clock.tick(15)

    # close out the display
    pygame.quit()

uiAnalogClockLoop()
#uiDScheduleLoop()
#quit()
