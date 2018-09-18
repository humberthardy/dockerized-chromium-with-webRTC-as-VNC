#!/usr/bin/env python

# WS server example that synchronizes state across clients

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
ch.setLevel(logging.DEBUG)
root.addHandler(ch)

pyautogui.FAILSAFE = False

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
    else:
        return key


def mapperX(ratio):
    return math.floor(ratio * width)

def mapperY(ratio):
    return math.floor(ratio * height)

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



def extractMouseParameter(data):
    kwargs = dict()
    kwargs["button"] = mapperButton(data["parameter"]["button"])
    kwargs["x"] = mapperX(data["parameter"]["x"])
    kwargs["y"] = mapperY(data["parameter"]["y"])
    logging.info("mouse event {}".format(kwargs))
    return kwargs


async def control(websocket, path):
    # register(websocket) sends user_event() to websocket
    try:
        async for message in websocket:
            data = json.loads(message)
            if data['action'] == 'onmouseup':
                pyautogui.mouseDown(**extractMouseParameter(data))
                logging.info(data['action'])
            elif data['action'] == 'onmousedown':
                pyautogui.mouseDown(**extractMouseParameter(data))
                logging.info(data['action'])
            elif data['action'] == 'onclick':
                pyautogui.click(**extractMouseParameter(data))
                logging.info(data['action'])
            elif data['action'] == 'onkeyup':
                key = extractKey(data)
                pyautogui.keyUp(key)
                logging.info(data['action'])
            elif data['action'] == 'onkeydown':
                key = extractKey(data)
                pyautogui.keyDown(key)
                logging.info(data['action'])
            else:
                logging.error("unsupported event: {}", data)
    finally:
        pass

asyncio.get_event_loop().run_until_complete(
    websockets.serve(control, '0.0.0.0', 6789))
asyncio.get_event_loop().run_forever()