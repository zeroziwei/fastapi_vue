from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://zero:zc991012@localhost/test"
Base = declarative_base()

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)

    # 定义与 Address 的关系
    addresses = relationship("Address", back_populates="owner", cascade="all, delete-orphan")

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String(100), nullable=False)
    city = Column(String(50), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # 定义与 User 的关系
    owner = relationship("User", back_populates="addresses")
    
    # 定义与 Order 的关系
    myorder = relationship("Order", back_populates="myaddress", cascade="all, delete-orphan")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_info = Column(String(50), nullable=False)
    address_id = Column(Integer, ForeignKey("addresses.id"))

    # 定义与 Address 的关系
    myaddress = relationship("Address", back_populates="myorder")
    # 定义与 User 的关系

# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 创建表
Base.metadata.create_all(bind=engine)

##########################################################################

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app = FastAPI()
# Pydantic 数据模型
class UserCreate(BaseModel):
    name: str
    email: str

class AddressCreate(BaseModel):
    street: str
    city: str
    owner_id: int

class OrderCreate(BaseModel):
    order_info: str
    address_id: int
# 依赖 - 获取数据库 session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 创建新用户
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 创建新地址
@app.post("/addresses/")
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    db_address = Address(street=address.street, city=address.city, owner_id=address.owner_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

@app.post("/order/")
def create_address(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(order_info = order.order_info, address_id = order.address_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.delete("/delete/{user_name}")
def delete(username,db:Session = Depends(get_db)):
    user = db.query(User).filter(User.name == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 删除用户
    db.delete(user)
    db.commit()

    return {"message": f"User '{username}' has been deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)