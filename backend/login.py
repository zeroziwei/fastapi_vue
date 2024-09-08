from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

app = FastAPI()

# Jinja2模板目录
templates = Jinja2Templates(directory="templates")

# 模拟用户数据库
fake_users_db = {
    "user@example.com": {
        "username": "user",
        "email": "user@example.com",
        "password": "password",  # 明文密码
    }
}

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    user_dict = fake_users_db.get(username)
    if not user_dict or user_dict['password'] != password:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    response = RedirectResponse(url="/protected", status_code=302)
    response.set_cookie(key="user_email", value=user_dict["email"])
    return response

@app.get("/protected")
async def protected_page(request: Request):
    user_email = request.cookies.get("user_email")
    if user_email is None:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("protected.html", {"request": request, "user_email": user_email})

@app.post("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie(key="user_email")
    return response

# 运行应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
