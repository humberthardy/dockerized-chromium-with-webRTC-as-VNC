String.prototype.format = function() {
    a = this;
    for (k in arguments) {
        a = a.replace("{" + k + "}", arguments[k])
    }
    return a
}

function getScreen() {
    return document.getElementById("screen");
}
function getVideo() {
    return document.getElementById("stream");
}


var ws = null;
var attempt = 0;
function onControlServerClose(event) {
    setTimeout(connectToServer, 1000)
}

function connectToServer() {
    attempt++;
    var ws_server;
    var ws_port = "6789";
    if (window.location.protocol.startsWith ("http")) {
        ws_server = ws_server || window.location.hostname;
    } else {
        throw new Error ("Don't know how to connect to the signalling server with uri" + window.location);
    }
    var ws_url = 'ws://' + ws_server + ':' + ws_port

    console.log("Connected to server {0} attempt #{1} ".format(ws_url, attempt));
    ws = new WebSocket(ws_url);
    ws.addEventListener('close', onControlServerClose);
}
connectToServer();

function scaleToScreen() {
    var currentWindowWidth = window.innerWidth;
    var currentWindowHeight = window.innerHeight;

    console.log("resizing to {0}px,{1}px".format(currentWindowWidth, currentWindowHeight));
    getScreen().style.width = currentWindowWidth  + "px";
    getScreen().style.height = currentWindowHeight + "px";
    getScreen().focus();

}

window.onresize = scaleToScreen;


function onmouseEvent (name, event) {
    var x = getXRatio(event);
    var y = getYRatio(event);
    var button = event.button;
    console.info("Event {0} ({1}, {2}) button={3}".format(name,x, y, button));
    var body = {
        action: name,
        parameter: {
            x: x,
            y: y,
            button: button
        }
    }

    if (event.constructor.name == "WheelEvent") {
        body["parameter"]["deltaX"] = event.deltaX;
        body["parameter"]["deltaY"] = event.deltaY;
    }

    event.stopImmediatePropagation();
    event.stopPropagation();
    event.preventDefault();

    ws.send(JSON.stringify(body));
}

function onKeyEvent(name, event) {
    var key = event.key;
    console.info("Event {0} on ({1})".format(name, key));
    body = {
        action: name,
        parameter: {
            key: key,
        }
    }

    event.stopImmediatePropagation();
    event.stopPropagation();
    event.preventDefault();

    ws.send(JSON.stringify(body));
}


function getHorizontalMargin() {
    var displayWidth = getVideo().offsetWidth;
    var displayHeight = getVideo().offsetHeight;
    var videoWidth = getVideo().videoWidth;
    var videoHeight = getVideo().videoHeight;
    var videoRatio = videoHeight / videoWidth;
    var displayRatio = displayHeight / displayWidth;

    if (displayRatio < videoRatio) {
        var widthMargin = Math.round((displayWidth - (displayHeight/ videoRatio))/2);
        console.log("computed width margin {0}".format(widthMargin));
        return widthMargin;
    } else {
        return 0;
    }
}

function getVerticalMargin() {
    var displayWidth = getVideo().offsetWidth;
    var displayHeight = getVideo().offsetHeight;
    var videoWidth = getVideo().videoWidth;
    var videoHeight = getVideo().videoHeight;
    var videoRatio = videoWidth / videoHeight;
    var displayRatio = displayWidth / displayHeight;

    if (displayRatio < videoRatio) {
        var heightMargin = Math.round((displayHeight - (displayWidth/ videoRatio))/2);
        console.log("computed height margin {0}".format(heightMargin));
        return heightMargin;
    } else {
        return 0;
    }
}

function getXRatio(event) {
    var x = event.offsetX;
    var width = getVideo().offsetWidth;
    var offset = getHorizontalMargin();
    return ((x - offset)/(width - (offset * 2)));
}

function getYRatio(event) {
    var y = event.offsetY;
    var height = getVideo().offsetHeight;
    var offset = getVerticalMargin();
    return ((y - offset ) / (height - (offset * 2)));
}
window.onload = function(e) {
    scaleToScreen(); // quick hack for now

    document.addEventListener("contextmenu", function(e){
        e.preventDefault();
    }, false);

    websocketServerConnect(e);

    var screen = getScreen();
    var video  = getVideo();

    video.onclick = function(event) {
        onmouseEvent("onclick", event);
    }
    video.onmousedown = function(event) {
        onmouseEvent("onmousedown", event);
    }
    video.onmouseup = function(event) {
        onmouseEvent("onmouseup", event);
    }
    video.onmousemove = function(event) {
        onmouseEvent("onmousemove", event);
    }
    video.onmousewheel = function(event) {
        onmouseEvent("onmousewheel", event);
    }
    screen.onkeydown = function(event) {
        onKeyEvent("onkeydown", event)
    }
    screen.onkeyup = function(event) {
        onKeyEvent("onkeyup", event);
    }
}
