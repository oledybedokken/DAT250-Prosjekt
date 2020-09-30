import os
import sys ,datetime
from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()

class Bruker(Base):
    __tablename__ = "bruker"
    id = Column(String, primary_key=True)
    name = Column(String(250),nullable=False)
    bruker_type = Column(String(250), nullable=False)
    passord = Column(String(250))
    
class Kunder(Base):
    __tablename__="kunder"
    kunde_id = Column(Integer, primary_key=True, autoincrement=True)
    cust_ssn_id = Column(Integer, unique=True)
    name = Column(String(250),nullable=False)
    adresse = Column(String(250), nullable=False)
    age = Column(Integer)
    fylke = Column(String(250), nullable=False)
    by = Column(String(250), nullable=False)
    status = Column(String(250), nullable=False)

class KundeLog(Base):
    __tablename__="kundelog"
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    kunde_id = Column(Integer, ForeignKey("kunder.kunde_id"))
    melding_log = Column(String(250), nullable=False)
    time_stamp = Column(DateTime(timezone=False), default=datetime.datetime.utcnow)

class Konto(Base):
    __tablename__="konto"
    konto_id = Column(Integer,primary_key=True,autoincrement=True)
    konto_type = Column(String(250),nullable=False)
    saldo = Column(Integer, nullable=False)
    kunde_id = Column(Integer, ForeignKey("kunder.kunde_id"))
    kunder = relationship(Kunder)
    status = Column(String(250), nullable=False)
    message =  Column(String(250))
    last_update = Column(DateTime)

class Transaksjoner(Base):
    __tablename__="transaksjoner"
    trans_id = Column(Integer, primary_key=True, autoincrement=True)
    konto_id = Column(Integer, ForeignKey("konto.konto_id"))
    trans_melding = Column(String(250), nullable=False)
    belop = Column(Integer, nullable=False)
    time_stamp = Column(DateTime(timezone=False), default=datetime.datetime.utcnow)
    
engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(engine)