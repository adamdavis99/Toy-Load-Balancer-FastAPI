from fastapi import FastAPI
import httpx
import uvicorn
import asyncio
import Load_Balancer

app = FastAPI()

backend_servers = [
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003"
]

balancer = Load_Balancer.LoadBalancer(backend_servers, 2, 1)

@app.get("/")
async def root():
    backend_server = balancer.get_server()
    async with httpx.AsyncClient() as client:
        response = await client.get(backend_server)
    return response.text

app2 = FastAPI()
@app2.get("/")
async def root():
    return {"message": "Hello from 8001"}

app3 = FastAPI()
@app3.get("/")
async def root():
    return {"message": "Hello from 8002"}

app4 = FastAPI()
@app4.get("/")
async def root():
    return {"message": "Hello from 8003"}

async def start_app(app, port):
    uvicorn_config = uvicorn.Config(app, host="0.0.0.0", port=port)
    server = uvicorn.Server(uvicorn_config)
    await server.serve()

async def run():
    app1_task = asyncio.create_task(start_app(app, 8000))
    app2_task = asyncio.create_task(start_app(app2, 8001))
    app3_task = asyncio.create_task(start_app(app3, 8002))
    app4_task = asyncio.create_task(start_app(app3, 8003))
    await asyncio.gather(app1_task, app2_task, app3_task, app4_task)

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("Shutting down servers...")
        tasks = [task for task in asyncio.all_tasks()]
        [task.cancel() for task in tasks]
        asyncio.run(asyncio.gather(*tasks, return_exceptions=True))
