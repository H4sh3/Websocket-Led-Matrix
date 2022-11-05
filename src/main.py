from fastapi import FastAPI, WebSocket
from rgbmatrix import RGBMatrix,RGBMatrixOptions

def get_options():
    o = RGBMatrixOptions()
    o.gpio_slowdown = 4
    o.rows = 64
    o.cols = 64
    o.brightness = 60
    return o

matrix = RGBMatrix(options=get_options())

app = FastAPI()

def limit(v,low,high):
    if v < low:
        return low
    if v > high:
        return high
    return v

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    canvas = matrix.CreateFrameCanvas()
    while True:
        pixels = await websocket.receive_json()
        canvas.Clear()
        for pixel in pixels:
            r = limit(pixel[2],0,255)
            g = limit(pixel[3],0,255)
            b = limit(pixel[4],0,255)
            canvas.SetPixel(pixel[0],pixel[1],r,g,b)

        canvas = matrix.SwapOnVSync(canvas)
        await websocket.send_json({"message":"ok"})