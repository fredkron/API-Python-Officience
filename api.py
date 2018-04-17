#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from flask import Flask, Response
import datetime, sqlite3
from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, String, datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from base import Base

app = Flask(__name__) 

Base = declarative_base()
engine = create_engine('sqlite:///api_python.db')
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

class Parent(Base):
    __tablename__ = 'CAPTURE'
    id = Column(Integer, primary_key=True)
    time = Column(datetime)
    count = Column(Integer)
    children = relationship("PRESENCE")

class Child(Base):
    __tablename__ = 'PRESENCE'
    id = Column(Integer, primary_key=True)
    hash = Column(String(20))
    parent_id = Column(Integer, ForeignKey('CAPTURE.id'))

@app.route("/")
def accueil():
    return "Accueil"

if __name__ == '__main__':
    app.run(debug=True)