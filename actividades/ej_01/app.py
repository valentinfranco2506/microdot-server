import asyncio
from microdot import Microdot
from microdot import send_file

app = Microdot()

@app.get('/')
async def index(request):
    return send_file('index.html')

@app.get('/styles/base.css')
async def index(request):
    return send_file('styles/base.css')

@app.get('/scripts/base.js')
async def index(request):
    return send_file('scripts/base.js')

@app.get('/')
async def image(request):
    return send_file('/static/image.jpg', max_age=3600)  # in seconds

app.run()

async def main():
    # start the server in a background task
    server = asyncio.create_task(app.start_server())

    # ... do other asynchronous work here ...

    # cleanup before ending the application
    await server

asyncio.run(main())

