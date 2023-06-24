import os
import random

def isLinux():
    print("IsLinux")
    from sys import platform
    global linuxMode
    if(platform == "linux" or platform == 'linux2'):    
        return 1
    else:
        return 0
    

def rename():
    if(isLinux() == 1):
            pth = 'vids/'
            app = ""
    else:
        pth = 'src/vids/'
        app = 'src/'

    names = os.listdir(path = pth)
    locations = ["lobby", 'atrium', 'foyer']
    for name in names:
        print(pth+name)
        locNum = random.randint(0,2)
        location = locations[locNum]
        yearNum = random.randint(2000, 2030)
        dayNum = random.randint(1,30)
        monthNum = random.randint(1,12)
        randHr = random.randint(0,23)
        randMin = random.randint(0,59)
        randSec = random.randint(0,59)
        os.rename(pth + name,pth + str(location + "&" + str(yearNum) + "-"+str(monthNum)+"-"+str(dayNum)+" "+str(randHr)+"-"+str(randMin)+"-"+str(randSec)+".mp4"))
        print(pth+name)

rename()

    