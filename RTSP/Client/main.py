import socket
import uvicorn

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
    return {'Hello': 'World'}

@app.get('/DeviceInfo')
def device_info():
    return {
        'hostname': socket.gethostname()
    }

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
