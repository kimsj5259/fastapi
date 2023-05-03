import sqlalchemy
from sqlalchemy import create_engine, Column, DateTime, String, ForeignKey, Date, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://sjair:password@127.0.0.1:5432/bill"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = 'user'

    id         = Column(String(500), primary_key=True, nullable=False)
    email      = Column(String, nullable=False)
    password   = Column(String(500), nullable=False)
    name       = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)

class InvestRecord(Base):
    __tablename__ = "invest_record"

    id         = Column(String(500), primary_key=True, nullable=False)
    user_id    = Column(String(500), ForeignKey('user.id'), nullable=False)
    title      = Column(String, nullable=False)
    context    = Column(String, nullable=True)
    created_at = Column(Date, nullable=False)

class InvestDetail(Base):
    __tablename__ = "invest_detail"

    id               = Column(String(500), primary_key=True, nullable=False)
    invest_record_id = Column(String(500), ForeignKey('invest_record.id'), nullable=False)
    category         = Column(String, nullable=False)
    buying_price     = Column(Float, nullable=False) # DECIMAL range is also considered with Crypto
    quantity         = Column(Float, nullable=False)
    # current_price    = Column(DECIMAL(10, 10), nullable=False) # 아래 두가지 컬럼은 매도 완료 했을시 저장하고 싶다면 필요, 물론 profit 테이블을 따로 빼는 것이 효율적일 것.
    # profit_rate      = Column(Numeric(10, 10, asdecimal=True), nullable=False)


Base.metadata.create_all(engine)
    

# import databases, sqlalchemy

# DATABASE_URL = "postgresql://sjair:password@127.0.0.1:5432/bill"
# database = databases.Database(DATABASE_URL)
# metadata = sqlalchemy.MetaData()

# users = sqlalchemy.Table(
#     "user",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
#     sqlalchemy.Column("email" , sqlalchemy.String, unique=True, nullable=False),
#     sqlalchemy.Column("password" , sqlalchemy.String),
#     sqlalchemy.Column("name" , sqlalchemy.String),
#     sqlalchemy.Column("gender" , sqlalchemy.CHAR),
#     sqlalchemy.Column("created_at" , sqlalchemy.String),
# )

# invest_record = sqlalchemy.Table(
#     "invest_record",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
#     sqlalchemy.Column("user_id" , sqlalchemy.String, foreign_key="user.id", nullable=False),
#     sqlalchemy.Column("category" , sqlalchemy.String),
#     sqlalchemy.Column("buying_price" , sqlalchemy.FLOAT),
#     sqlalchemy.Column("current_price" , sqlalchemy.FLOAT),
#     sqlalchemy.Column("profit_rate" , sqlalchemy.Float),
# )


# engine = sqlalchemy.create_engine(
#     DATABASE_URL
# )
# metadata.create_all(engine)