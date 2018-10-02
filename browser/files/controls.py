#!/usr/bin/env python3


import asyncio
import json
import logging
import websockets
import sys
import pyautogui
import math
# config handler

root = logging.getLogger()
root.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
root.addHandler(ch)

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.0

width, height = pyautogui.size()

def mapper(key):

    if key == 'Control':
        return 'ctrl'
    elif key == 'Shift':
        return 'shift'
    elif key == '\n':
        return 'enter'
    elif key == 'Alt':
        return 'alt'
    elif key == 'F11':
        return 'f11'
    elif key == 'Escape':
        return 'esc'
    elif key == 'ArrowRight':
        return 'right'
    elif key == 'ArrowLeft':
        return 'left'
    elif key == 'ArrowUp':
        return 'up'
    elif key == 'ArrowDown':
        return 'down'
    else:
        return key

def mapperX(ratio):
    return round(ratio * width)

def mapperY(ratio):
    return round(ratio * height)

def mapperButton(button):
    if button == 0:
        return 'left'
    elif button == 1:
        return "middle"
    elif button == 2:
        return "right"

def extractKey(data):
    try:
        key = mapper(data["parameter"]["key"])
        logging.info("key {} was pressed".format(key))
        return key
    except:
        logging.error("can not extract key from {}".format(data))

def convertScroll(delta):
    if delta == 0:
        return 0
    elif delta > 0:
        return -1
    else:
        return 1



def extractMouseParameter(data, button=True):
    kwargs = dict()
    if button:
        kwargs["button"] = mapperButton(data["parameter"]["button"])
    kwargs["x"] = mapperX(data["parameter"]["x"])
    kwargs["y"] = mapperY(data["parameter"]["y"])

    logging.debug("mouse event {}".format(kwargs))
    return kwargs


async def control(websocket, path):
    try:
        async for message in websocket:
            data = json.loads(message)
            logging.debug(data)

            if data['action'] == 'onmouseup':
                pyautogui.mouseDown(**extractMouseParameter(data))
            elif data['action'] == 'onmousedown':
                pyautogui.mouseDown(**extractMouseParameter(data))
            elif data['action'] == 'onmousemove':
                pyautogui.moveTo(duration=0, **extractMouseParameter(data, button=False))
            elif data['action'] == 'onmousewheel':
                deltax = convertScroll(data['parameter']['deltaX'])
                deltay = convertScroll(data['parameter']['deltaY'])
                if deltax != 0:
                    pyautogui.hscroll(deltax, **extractMouseParameter(data, button=False))
                if deltay != 0:
                    pyautogui.vscroll(deltay, **extractMouseParameter(data, button=False))
            elif data['action'] == 'onclick':
                pyautogui.click(**extractMouseParameter(data))
            elif data['action'] == 'onkeyup':
                key = extractKey(data)
                pyautogui.keyUp(key)
            elif data['action'] == 'onkeydown':
                key = extractKey(data)
                pyautogui.keyDown(key)
            else:
                logging.error("unsupported event: {}", data)
    finally:
        pass

asyncio.get_event_loop().run_until_complete(
    websockets.serve(control, '0.0.0.0', 6789))
asyncio.get_event_loop().run_forever()