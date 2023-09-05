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
        secs = random.randint(60,300)

    print("sleep: ", secs)
    time.sleep(secs)

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
        
    
commands = [ rightClick, altTab, wheel, mouseMove, runCommand, openShortCut, changeVirtualDesktop ]

startTime = time.time()

#if started with capsLock on then we are testing
kbd.send(Keycode.CAPS_LOCK)
time.sleep(.3)
kbd.send(Keycode.CAPS_LOCK)
time.sleep(.2)
test = kbd.led_on(Keyboard.LED_CAPS_LOCK)

print("test: ", kbd.led_on(Keyboard.LED_CAPS_LOCK))

print("-------------------------")
print("Starting autonomous robot")


capsLockOn()
sleepRnd()
capsLockOff()
sleepRnd()

for cmd in commands:
    if kbd.led_on(Keyboard.LED_CAPS_LOCK):
        print("CapsLock is ON. Stopping robot")
        break
        
    blinkLed()
    print("running %s minutes" % ((time.time() - startTime)/60) )
    print(str(cmd))
    cmd()
    sleepRnd()

capsLockOn()
print("run for %s minutes" % ((time.time() - startTime)/60) )
print("End autonomous robot")

#while True:
    #led.value = True
    #print("on")
    #time.sleep(10)
    #led.value = False
    #print("off")
    #time.sleep(2)
