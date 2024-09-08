import bcrypt
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# 添加会话中间件
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# Jinja2模板目录
templates = Jinja2Templates(directory="templates")

# 模拟用户数据库，密码使用bcrypt哈希
fake_users_db = {}

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    if username in fake_users_db:
        return templates.TemplateResponse("register.html", {"request": request, "error": "用户名已存在"})
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    fake_users_db[username] = {
        "username": username,
        "email": username,
        "password": hashed_password,
    }
    return RedirectResponse(url="/", status_code=302)

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user_dict = fake_users_db.get(username)
    if not user_dict or not bcrypt.checkpw(password.encode('utf-8'), user_dict['password']):
        return templates.TemplateResponse("login.html", {"request": request, "error": "用户名或密码错误"})

    request.session['user_email'] = user_dict["email"]
    return RedirectResponse(url="/protected", status_code=302)

@app.get("/protected", response_class=HTMLResponse)
async def protected_page(request: Request):
    user_email = request.session.get("user_email")
    if user_email is None:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("protected.html", {"request": request, "user_email": user_email})

@app.post("/logout")
async def logout(request: Request):
    request.session.pop("user_email", None)
    return RedirectResponse(url="/")

# 运行应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
