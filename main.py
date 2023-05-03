import uuid
from datetime import datetime
from fastapi import FastAPI, Depends, Header
from passlib.context import CryptContext
from app.database import User, InvestRecord, InvestDetail, get_db #engine 
from app.model import UserList, UserRegisterEntry, UserLoginEntry, InvestRecordEntry, InvestDetailEntry, InvestDetailList
from sqlalchemy.orm import Session
from app.auth.auth_bearer import JWTBearer
from app.auth.jwt_handler import generate_access_token, generate_refresh_token, decode_for_refresh
from starlette.responses import JSONResponse


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # password hashing

app = FastAPI()


def is_email_exist(email, db: Session = Depends(get_db)): # 이메일 중복 확인
    result = db.query(User).filter(email==User.email).first()
    # session.close()
    if result is not None:
        return True
    return False

def user_email_with_token(authorization):
    token = authorization[7:]
    email = decode_for_refresh(token)
    return email

@app.post("/user/signup", response_model=UserList, tags=["user"])
def register_user(user: UserRegisterEntry, db: Session = Depends(get_db)):
    if not user.email or not user.password: # 이메일 혹은 password는 반드시 기입했는지 확인
            return JSONResponse(status_code=400, content=dict(msg="Email and PW must be provided'"))
    
    is_exist = is_email_exist(user.email, db)
    if is_exist:
        return JSONResponse(status_code=400, content=dict(message="EMAIL_EXISTS"))
    
    user_uuid = str(uuid.uuid1())
    user_date = str(datetime.now())
    query = User(
        id          = user_uuid,
        email       = user.email,
        password    = pwd_context.hash(user.password),
        name        = user.name,
        created_at  = user_date,
    )
    db.add(query)
    db.commit()
    return {
        "id"        : user_uuid,
        "email"     : user.email,
        "name"      : user.name,
        "created_at": user_date,
    }

@app.post("/user/login",tags=["user"])
def user_login(user: UserLoginEntry, db: Session = Depends(get_db)):
    if not user.email or not user.password: # 이메일 혹은 password는 반드시 기입했는지 확인
        return JSONResponse(status_code=400, content=dict(msg="Email and PW must be provided'"))
    
    is_exist = is_email_exist(user.email, db)
    if not is_exist:
        return JSONResponse(status_code=400, content=dict(message="NO_MATCH_EMAIL"))
    
    result = db.query(User).filter(user.email==User.email).first()
    password_match = pwd_context.verify(user.password, result.password)

    if not password_match:
        return JSONResponse(status_code=400, content=dict(msg='WRONG_PASSWORD'))
    
    access_token = generate_access_token({"email": user.email})
    refresh_token = generate_refresh_token({"email": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token}

@app.post("/user/refresh", dependencies=[Depends(JWTBearer())], tags=["user"])
def refresh_to_access(authorization = Header(None)):
    result = user_email_with_token(authorization)
    new_access_token = generate_access_token({"email": result['email']})
    return {"access_token": new_access_token}

# server process with JWT
@app.post("/invest/record/post", dependencies=[Depends(JWTBearer())], tags=["Invest_Diary"])
def add_investing_record(record: InvestRecordEntry, db: Session = Depends(get_db), authorization = Header(None)):
    result = user_email_with_token(authorization)
    user = db.query(User).filter(result['email']==User.email).first()
    record_user_id = user.id
    record_uuid = str(uuid.uuid1())
    record_date = datetime.now().strftime('%Y-%m-%d')

    query = InvestRecord(
        id         = record_uuid,
        user_id    = record_user_id,
        title      = record.title,
        context    = record.context,
        created_at = record_date,
    )
    db.add(query)
    db.commit()
    # session.close()
    return {
        "id"         : record_uuid, # invest_detail에서 관련 값을 찾기 위한 데이터 전송
        "user_id"    : record_user_id,
        "title"      : record.title,
        "context"    : record.context,
        "created_at" : record_date
    }

@app.get("/invest/record/get", dependencies=[Depends(JWTBearer())], tags=["Invest_Diary"])
def find_invest_record(authorization = Header(None), db: Session = Depends(get_db)):
    result = user_email_with_token(authorization)
    user = db.query(User).filter(result['email']==User.email).first()
    invest_record = db.query(InvestRecord).filter(user.id==InvestRecord.user_id).all() # all data according to one user as LIST
    # session.close()
    return {
        "invest_record": invest_record
    }

@app.post("/invest/detail/add", dependencies=[Depends(JWTBearer())], tags=["Invest_Diary"])
def add_investing_detail(detail: InvestDetailEntry, db: Session = Depends(get_db)):
    # invest_detail = session.query(InvestDetail).filter(detail.invest_record_id==InvestDetail.invest_record_id).all()
    detail_uuid = str(uuid.uuid1())

    query = InvestDetail(
        id               = detail_uuid,
        invest_record_id = detail.invest_record_id,
        category         = detail.category,
        buying_price     = detail.buying_price,
        quantity         = detail.quantity
    )
    db.add(query)
    db.commit()
    # session.close()
    return {
        "id"            : detail_uuid,
        "category"      : detail.category,
        "buying_price"  : detail.buying_price,
        "quantity"      : detail.quantity
    }

@app.post("/invest/detail/info", dependencies=[Depends(JWTBearer())], tags=["Invest_Diary"])
def find_invest_detail(detail: InvestDetailList, db: Session = Depends(get_db)):
    invest_detail = db.query(InvestDetail).filter(detail.invest_record_id==InvestDetail.invest_record_id).all()
    invest_detail_list = []
    for i in list(invest_detail):
        detail_value = {"category":"", "buying_price":"", "current_price":"", "profit_rate":""}
        detail_value["category"] = i.category
        detail_value["buying_price"] = i.buying_price
        detail_value["current_price"] = 10 # temporary mock data, will be differ depends on how to get 'current_price'
        detail_value["profit_rate"] = (10 - i.buying_price) / i.buying_price # profit_rate Formula
        invest_detail_list.append(detail_value)
        
    return {
        "invest_detail_list": invest_detail_list
    }

# #### To Show all the user ####
# @app.get("/users", tags=["user"])
# def find_all_users(db: Session = Depends(get_db)):
#     all_users = []
#     users = db.query(User)
#     for user in users:
#         user_lst = {"email":"", "name":""}
#         user_lst['email'] = user.email
#         user_lst['name'] = user.name
#         all_users.append(user_lst)
#     # session.close()
#     return all_users