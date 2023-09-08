import random
import board
import digitalio
import time
import usb_hid
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

kbd = Keyboard(usb_hid.devices)

mouse = Mouse(usb_hid.devices)

layout = KeyboardLayoutUS(kbd)


led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

time.sleep(1)


def blinkLed():

    for i in range(0,6):
        led.value = not led.value
        time.sleep(0.2)

    led.value = False


def sleepRnd():
    if test:
        secs = random.randint(1,5)
    else:
        secs = random.randint(60,200)

    print("sleep: ", secs)
    time.sleep(secs)

def sleepShort():
    time.sleep(random.randint(1,8)/10)

def runCommand():
    print("running command")
    kbd.send(Keycode.WINDOWS)
    time.sleep(5)
    layout.write("cmd")
    time.sleep(5)
    kbd.send(Keycode.ENTER)
    time.sleep(1)
    layout.write("dir\n")
    sleepRnd()
    layout.write("exit\n")

def wheel():
    print("moving mouse wheel")
    for i in range(1, random.randint(5,25)):
        mouse.move(wheel=-1)
        print("moved 1... ", i)
        time.sleep(random.randint(10,80) / 100)

def mouseMove():
    print("moving mouse")
    for i in range(1, random.randint(5,25)):
        mouse.move(x=i)
        print("moved x... ", i)
        time.sleep(random.randint(10,80) / 100)

def altTab():
    print("altTab")
    kbd.send(Keycode.ALT, Keycode.TAB)
    sleepRnd()
    kbd.send(Keycode.ALT, Keycode.TAB)

def rightClick():
    print("right click mouse")
    sleepRnd()
    mouse.click(Mouse.RIGHT_BUTTON)
    sleepRnd()
    kbd.send(Keycode.ESCAPE)


def openShortCut():
    index = random.randint(1,5)
    print("open shortcut", index)
    kbd.send(Keycode.CONTROL, Keycode.WINDOWS, layout.keycodes(str(index))[0])
    sleepRnd()
    kbd.send(Keycode.ALT, Keycode.F4)

def changeVirtualDesktop():
    print("change virtual desktop")
    kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.RIGHT_ARROW)
    kbd.send(Keycode.CONTROL, Keycode.WINDOWS, Keycode.RIGHT_ARROW)
    sleepRnd()
    kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.LEFT_ARROW)
    kbd.send(Keycode.CONTROL, Keycode.WINDOWS, Keycode.LEFT_ARROW)


def capsLockOff():
    print("caps off")
    if kbd.led_on(Keyboard.LED_CAPS_LOCK):
        kbd.send(Keycode.CAPS_LOCK)

def capsLockOn():
    print("caps on")
    if not kbd.led_on(Keyboard.LED_CAPS_LOCK):
        kbd.send(Keycode.CAPS_LOCK)
        
def openUrl():
    print("opening url")
    kbd.send(Keycode.WINDOWS)
    time.sleep(1)
    layout.write("cmd")
    time.sleep(1)
    kbd.send(Keycode.ENTER)
    time.sleep(1)
    layout.write("alias start=xdg-open\n")
    time.sleep(1)
    url = urls[random.randrange(len(urls))];
    layout.write("start " + url + "\n")
    sleepRnd()
    kbd.send(Keycode.CONTROL, Keycode.W)
    sleepRnd()
    kbd.send(Keycode.ALT, Keycode.TAB)
    sleepRnd()
    layout.write("exit\n")
    
def openChrome():
    print("open chrome and read page")
    kbd.send(Keycode.WINDOWS)
    sleepShort()
    layout.write("chrome\n")
    sleepRnd()
    kbd.send(Keycode.CONTROL, Keycode.T)
    sleepRnd()
    url = urls[random.randrange(len(urls))];
    layout.write(url)
    sleepShort()
    kbd.send(Keycode.ENTER)
    sleepRnd()
    readPage()
    
    kbd.send(Keycode.CONTROL, Keycode.A)
    sleepShort()
    kbd.send(Keycode.CONTROL, Keycode.C)
    sleepShort()
    kbd.send(Keycode.CONTROL, Keycode.W)
    sleepRnd()
    
def copyChromeContent():
    print("copy chrome content")
    kbd.send(Keycode.WINDOWS)
    sleepShort()
    layout.write("chrome")
    sleepShort()
    kbd.send(Keycode.ENTER)
    sleepRnd()
    kbd.send(Keycode.CONTROL, Keycode.T)
    sleepShort()
    sleepShort()
    url = urls[random.randrange(len(urls))];
    layout.write(url)
    sleepShort()
    sleepShort()
    kbd.send(Keycode.ENTER)
    time.sleep(5) #wait for page to load
    kbd.send(Keycode.CONTROL, Keycode.A)
    sleepShort()
    sleepShort()
    kbd.send(Keycode.CONTROL, Keycode.C)
    sleepShort()
    sleepShort()
    kbd.send(Keycode.CONTROL, Keycode.C)
    sleepShort()
    kbd.send(Keycode.CONTROL, Keycode.W)
    sleepShort()
    sleepShort()
    sleepShort()
    sleepShort()
    
def vsCodeFind():
    print("find text vs code")
    kbd.send(Keycode.HOME)
    text = [chr(i) for i in range(97,123)]
    kbd.send(Keycode.CONTROL, Keycode.F)
    sleepShort()
    layout.write(text[random.randrange(len(text))])
    for x in range(0,random.randint(0,20)):
        kbd.send(Keycode.ENTER)
        sleepRnd()
    kbd.send(Keycode.ESCAPE)
    sleepShort()

def copyWord():
    print("copy word")
    kbd.send(Keycode.CONTROL,Keycode.SHIFT, Keycode.RIGHT_ARROW)
    sleepShort()
    kbd.send(Keycode.CONTROL,Keycode.C)
    sleepShort()
    kbd.send(Keycode.ESCAPE)
    sleepRnd()

def paste():
    print("paste")
    newLine()
    kbd.send(Keycode.CONTROL, Keycode.V)
    sleepShort()    

def newLine():
    print("newLine")
    kbd.send(Keycode.ENTER)
    kbd.send(Keycode.ENTER)
    kbd.send(Keycode.UP_ARROW)
    sleepShort()


def execShellCommands():
    print("exec shell commands")
    shellCommands = ["ls", "ls -a", "df", "df -h", "echo $(date)", "du","df", "uname","uname -a",
    "ls | awk '{sum += 1 } END { print sum }'", "date | grep 'M'", "history", "history --help", 
    "grep --help","printenv"]
    
    for n in range(0,random.randrange(4)):
        shellCommand = shellCommands[random.randrange(len(shellCommands))]
        layout.write(shellCommand)
        sleepShort()
        kbd.send(Keycode.ENTER)
        sleepShort()
    

def vsOpenTerminal():
    print("open terminal")
    kbd.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.P)
    sleepShort()
    layout.write("new terminal profile")
    sleepShort()
    kbd.send(Keycode.ENTER)
    sleepShort()
    layout.write("bash")
    sleepShort()
    kbd.send(Keycode.ENTER)
    sleepShort()
    execShellCommands()
    sleepRnd()
    layout.write("exit 0") # close this terminal window
    sleepShort()
    kbd.send(Keycode.ENTER)
    sleepShort()
    # return to editor
    # show explorer
    kbd.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.E)
    sleepShort()
    kbd.send(Keycode.CONTROL, Keycode.ONE) # go to editor 1
    
def randomVsCommands():
    print("random vs code commands")
    vscommands = [readPage, vsCodeFind, copyWord, paste, newLine, vsOpenTerminal]
    #vscommands = [vsOpenTerminal] # test single command
    for k in range(0,random.randrange(10)):
        vscommands[random.randrange(len(vscommands))]()
    
def openVsCode():
    print("open vs code")
    copyChromeContent()
    
    kbd.send(Keycode.WINDOWS)
    sleepShort()
    layout.write("code")
    sleepShort()
    kbd.send(Keycode.ENTER)
    sleepShort()
    sleepRnd()
    kbd.send(Keycode.ESCAPE)
    sleepShort()
    sleepShort()
    # show explorer
    kbd.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.E)
    # new text file
    kbd.send(Keycode.CONTROL, Keycode.N)
    sleepShort()
    kbd.send(Keycode.CONTROL, Keycode.V)
    sleepRnd()
    
    randomVsCommands()
    
    sleepRnd()
    kbd.send(Keycode.CONTROL, Keycode.W)
    sleepShort()
    kbd.send(Keycode.ALT, Keycode.N)
    sleepShort()
    
def pageUpOrDown():
    print("pageUpOrDown")
    if random.randint(0,1):
        key = Keycode.PAGE_DOWN
    else:
        key = Keycode.PAGE_UP
            
    for i in range(0,random.randint(0,10)):
        kbd.send(key)
        sleepRnd()
        
def arrowUpOrDown():
    print("arrowUpOrDown")
    if random.randint(0,1):
        key = Keycode.UP_ARROW
    else:
        key = Keycode.DOWN_ARROW
            
    for i in range(0,random.randint(0,10)):
        kbd.send(key)
        sleepRnd()
        
    
def readPage():
    print("read page")
    for i in range(0,random.randint(0,5)):
        readType = random.choice([pageUpOrDown, arrowUpOrDown, wheel])
        readType() 
 
def runLastCommand():
    print("running last command")
    kbd.send(Keycode.WINDOWS)
    sleepShort()
    layout.write("cmd")
    sleepShort()
    kbd.send(Keycode.ENTER)
    sleepRnd()
    layout.write("echo run for ")
    sleepShort()
    layout.write(str((time.time() - startTime)/60))
    sleepShort()
    layout.write(" minutes")
    sleepShort()
    kbd.send(Keycode.ENTER)
    sleepShort()
    layout.write("echo The end")
    kbd.send(Keycode.ENTER)
    sleepShort() 
    
    
urls = ["https://github.com/features/issues","https://harness.io/blog","https://aws.amazon.com","https://learn.microsoft.com/en-us/azure/",
"https://finact.britive-app.com/login","https://maven.apache.org/","https://www.java.com/en/download/help/index.html"]

commands = [ openVsCode, openVsCode, openVsCode, openVsCode, openChrome, openUrl, rightClick, altTab, wheel, mouseMove, runCommand, openShortCut, changeVirtualDesktop ]
commands = [ openVsCode ] # test single command

startTime = time.time()

#if started with capsLock on then we are testing
kbd.send(Keycode.CAPS_LOCK)
time.sleep(.3)
kbd.send(Keycode.CAPS_LOCK)
time.sleep(.2)
test = kbd.led_on(Keyboard.LED_CAPS_LOCK)


print("-------------------------")
print("Starting autonomous robot")
print("test: ", kbd.led_on(Keyboard.LED_CAPS_LOCK))


capsLockOn()
sleepRnd()
capsLockOff()
sleepRnd()

#for j in range(0,len(commands) * 2):
for j in range(len(commands)):
    if kbd.led_on(Keyboard.LED_CAPS_LOCK):
        print("CapsLock is ON. Stopping robot")
        break

    blinkLed()
    print("running %s minutes" % ((time.time() - startTime)/60) )
    cmdindex = random.randrange(len(commands))
    print("index: ", cmdindex)
    print(str(commands[cmdindex]) + " - " + str(cmdindex))
    commands[cmdindex]()
    
    sleepRnd()

runLastCommand()
print("run for %s minutes" % ((time.time() - startTime)/60) )
print("End autonomous robot")
capsLockOn()

#while True:
    #led.value = True
    #print("on")
    #time.sleep(10)
    #led.value = False
    #print("off")
    #time.sleep(2)
