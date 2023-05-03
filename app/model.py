from pydantic import BaseModel, Field, EmailStr

class UserList(BaseModel):
    id          : str
    email       : str
    name        : str
    created_at  : str

class UserRegisterEntry(BaseModel):
    email       : str = Field(..., example="cjkim@gmail.com")
    password    : str = Field(..., example="somethings")
    name        : str = Field(..., example="Paul")

class UserLoginEntry(BaseModel):
    email       : EmailStr = Field(..., example="cjkim@gmail.com")
    password    : str = Field(..., example="somethings")

class InvestRecordEntry(BaseModel):
    title    : str = Field(..., example="Big enterprise companies")
    context  : str = Field(..., example="To analyze how it works")

class InvestDetailEntry(BaseModel):
    invest_record_id : str = Field(..., example="98eb3fd4-e33a-11ed-a7ce-b208a00092a0")
    category         : str = Field(..., example="Google")
    buying_price     : float = Field(..., example="11.02") # DECIMAL range is also considered with Crypto
    quantity         : float = Field(..., example="0.02")

class InvestDetailList(BaseModel):
    invest_record_id : str = Field(..., example="98eb3fd4-e33a-11ed-a7ce-b208a00092a0")

##### JWT Web token schema
# class UserLoginSchema(BaseModel):
#     email    : EmailStr = Field(default=None)
#     password : str = Field(default=None)
#     class Config:
#         the_schema = {
#             "user_demo": {
#                 "email": "help@billionaire.com",  
#                 "password": "123"
#             }
#         }





# class UsersRepo(BaseRepo):
    
#     @staticmethod
#     def find_by_username(db:Session, model: Generic[T], username: str):
#         return db.query(model).filter(model.username == username).first()
    

# _user = UsersRepo.find_by_username(
#             db, Users, request.parameter.data["username"])