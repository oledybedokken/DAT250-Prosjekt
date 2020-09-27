import os
import sys, datetime
from sqlalchemy import DateTime
from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Bruker(Base):
    __tablename__ = "bruker"
    id = Column(String, primary_key=True)
    navn = Column(String(50), nullable=False)
    bruker_type = Column(String(50), nullable=False)
    passord = Column(String(32))
    
class Kunder(Base):
    __tablename__="kunder"
    kunde_id = Column(Integer, primary_key=True, autoincrement=True)
    ssn_kunde_id = Column(Integer, unique=True)
    navn = Column(String(50), nullable=False)
    adresse = Column(String(64), nullable=False)
    fylke = Column(String(32), nullable=False)
    by = Column(String(32), nullable=False)
    status = Column(String(250), nullable=False)

class KundeLog(Base):
    __tablename__="kundelog"
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    kunde_id = Column(Integer, ForeignKey("kunder.kunde_id"))
    melding_log = Column(String(250), nullable=False)
    time_stamp = Column(DateTime(timezone=False), default=datetime.datetime.utcnow)

class Konto(Base):
    __tablename__="konto"
    bruker_id = Column(Integer,primary_key=True,autoincrement=True)
    bruker_type = Column(String(64),nullable=False)
    saldo = Column(Integer, nullable=False)
    kunde_id = Column(Integer, ForeignKey("kunder.kunde_id"))
    kunder = relationship(Kunder)
    status = Column(String(64), nullable=False)
    melding =  Column(String(64))
    last_update = Column(DateTime)

class Transaksjoner(Base):
    __tablename__="Transaksjoner"
    trans_id = Column(Integer, primary_key=True, autoincrement=True)
    bruker_id = Column(Integer, ForeignKey("konto.bruker_id"))
    trans_melding = Column(String(64), nullable=False)
    belop = Column(Integer, nullable=False)
    time_stamp = Column(DateTime(timezone=False), default=datetime.datetime.utcnow)
    
engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(engine)