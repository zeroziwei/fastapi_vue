from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# 定义表单数据的模型
class FormData(BaseModel):
    name: str
    email: str

# 创建 FastAPI 实例
app = FastAPI()

# 允许跨域请求的来源
origins = [
    "http://localhost:8080",  # Vue 前端运行的地址
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义接收表单数据的 POST 端点
@app.post("/api/form")
async def submit_form(data: FormData):
    # 在这里处理接收到的数据，比如保存到数据库等
    # 这里只是返回数据作为示例
    if not data.name or not data.email:
        raise HTTPException(status_code=400, detail="Name and email are required")
    print(f'data:{data.name}')
    return {"message": "Form submitted successfully", "data": data}
    


