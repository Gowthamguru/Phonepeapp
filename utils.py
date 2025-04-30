# import important libraries
from sqlalchemy import Column, Integer, String, create_engine,DateTime,Float,BigInteger
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from dotenv import find_dotenv, load_dotenv
import os
from urllib.parse import quote_plus
from git import Repo
import pandas as pd


# Base class for ORM models
Base = declarative_base()

# Validate the path
dotenv_path = find_dotenv()
# load the path
env_val = load_dotenv(dotenv_path)


# Define Aggregated Tables:

#Aggregated_user
class Agguser(Base):
    __tablename__ = 'aggregated_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reg_users = Column(Integer)
    app_opens = Column(BigInteger)
    brand = Column(String(250))
    count = Column(Integer)
    percentage = Column(Float)
    agg_year = Column(Integer)
    state = Column(String(250))
    quarter = Column(Integer)
    ingestion_date = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Agguser(reg_users='{self.registered_users}',app_opens='{self.app_opens}',brand='{self.brand}',count='{self.count}',percentage='{self.percentage}',agg_year='{self.agg_year}',state={self.state},quarter='{self.quarter}')>"

#Aggregated_transaction
class Aggtrans(Base):
    __tablename__='aggregated_transaction'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    count = Column(BigInteger)
    amount = Column(Float)
    agg_year = Column(Integer)
    state = Column(String(250))
    quarter = Column(Integer)
    ingestion_date = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return  f"Aggtrans(name='{self.name}',count='{self.count}',amount='{self.amount}',agg_year='{self.agg_year}',state={self.state},quarter='{self.quarter}')>"

#Aggregated Insurance
class Agginsurance(Base):
    __tablename__='aggregated_insurance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    count = Column(BigInteger)
    amount = Column(Float)
    agg_year = Column(Integer)
    state = Column(String(250))
    quarter = Column(Integer)
    ingestion_date = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return  f"Agginsurance(name='{self.name}',count='{self.count}',amount='{self.amount}',agg_year='{self.agg_year}',state={self.state},quarter='{self.quarter}')>"

#Map Tables:

#Map_user:
class Mapuser(Base):
    __tablename__='map_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reg_users = Column(Integer)
    app_opens = Column(BigInteger)
    agg_year = Column(Integer)
    state = Column(String(250))
    district = Column(String(250))
    quarter = Column(Integer)
    ingestion_date = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return  f"<Mapuser(reg_users='{self.reg_users}',app_opens='{self.app_opens}',agg_year='{self.agg_year}',state='{self.state}',district='{self.district}',quarter='{self.quarter}')>"

#Map_map
class Mapmap(Base):
    __tablename__ ='map_map'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    count = Column(BigInteger)
    amount = Column(Float)
    agg_year = Column(Integer)
    state = Column(String(250))
    district = Column(String(250))
    quarter = Column(Integer)
    ingestion_date = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return  f"<Mapmap(name='{self.name}',count='{self.count}',amount='{self.amount}',agg_year='{self.agg_year}',state={self.state},district='{self.district}',quarter='{self.quarter}')>"

#Map_insurance
class Mapinsurance(Base):
    __tablename__ ='map_insurance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    count = Column(BigInteger)
    amount = Column(Float)
    agg_year = Column(Integer)
    state = Column(String(250))
    district = Column(String(250))
    quarter = Column(Integer)
    ingestion_date = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return  f"<Mapinsurance(name='{self.name}',count='{self.count}',amount='{self.amount}',agg_year='{self.agg_year}',state={self.state},district='{self.district}',quarter='{self.quarter}')>"

#Top Tables

#Top_user
class Topuser(Base):
    __tablename__='top_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reg_users = Column(Integer)
    agg_year = Column(Integer)
    state = Column(String(250))
    district = Column(String(250))
    quarter = Column(Integer)
    pincode = Column(Integer)
    ingestion_date = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return  f"<Topuser(reg_users='{self.reg_users}',agg_year='{self.agg_year}',state='{self.state}',district='{self.district}',quarter='{self.quarter}',pincode='{self.pincode}')>"

#Top Map
class Topmap(Base):
    __tablename__='top_map'

    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_name = Column(String(250))
    count = Column(BigInteger)
    amount = Column(Float)
    agg_year = Column(Integer)
    state = Column(String(250))
    district = Column(String(250))
    quarter = Column(Integer)
    pincode = Column(Integer)
    ingestion_date = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"Topmap(entity_name='{self.entity_name}',count='{self.count}',amount='{self.amount}',agg_year='{self.agg_year}',state={self.state},district='{self.district}',quarter='{self.quarter}',pincode='{self.pincode}')>"

#Top Insurance
class Topinsurance(Base):
    __tablename__='top_insurance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_name = Column(String(250))
    count = Column(BigInteger)
    amount = Column(Float)
    agg_year = Column(Integer)
    state = Column(String(250))
    district = Column(String(250))
    quarter = Column(Integer)
    pincode = Column(Integer)
    ingestion_date = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"Topinsurance(entity_name='{self.entity_name}',count='{self.count}',amount='{self.amount}',agg_year='{self.agg_year}',state={self.state},district='{self.district}',quarter='{self.quarter}',pincode='{self.pincode}')>"

# Table creation function using sqlalchemy
def table_creation():
    if env_val:
        _host = os.getenv("HOST")
        _userid = os.getenv("USER_ID")
        _password = quote_plus(os.getenv("PASSWORD"))
        _database = os.getenv("DATABASE")
        engine = create_engine(f'mysql+mysqlconnector://{_userid}:{_password}@{_host}/{_database}')
        Base.metadata.create_all(engine)

# Copy the data from dataframe to SQL tables
def copytomysql(df,tablename):
    if env_val:
        _host = os.getenv("HOST")
        _userid = os.getenv("USER_ID")
        _password = quote_plus(os.getenv("PASSWORD"))
        _database = os.getenv("DATABASE")
        engine = create_engine(f'mysql+mysqlconnector://{_userid}:{_password}@{_host}/{_database}')
        df.to_sql(tablename, con=engine, if_exists='append', index=False)

# to Fetch the data from SQL tables to Data frame
def fetchfrommysql(query):
    if env_val:
        _host = os.getenv("HOST")
        _userid = os.getenv("USER_ID")
        _password = quote_plus(os.getenv("PASSWORD"))
        _database = os.getenv("DATABASE")
        engine = create_engine(f'mysql+mysqlconnector://{_userid}:{_password}@{_host}/{_database}')
        df = pd.read_sql(query, engine)
        return df

# Repository clone function
def clone_repo():
    git_url=os.getenv("GIT_URL")
    destination = "./data"
    if os.path.exists(destination):
        print('Path already exists')
    else:
        try:
            Repo.clone_from(git_url,destination)
            print('Repository Cloned')
        except:
            print('Clone Failed')
