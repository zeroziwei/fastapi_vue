from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import time  # 导入 time 模块
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可以根据需要修改允许的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def event_stream():
    while True:
        # 模拟数据生成
        await asyncio.sleep(1)  # 每隔 1 秒发送一次数据
        yield f"data: 当前时间戳是 {int(time.time())}\n\n"  # 使用 time 模块获取时间戳

@app.get("/sse")
async def sse():
    return StreamingResponse(event_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)