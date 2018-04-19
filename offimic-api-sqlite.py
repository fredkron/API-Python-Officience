#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from flask import Flask, Response
import datetime, sqlite3, sys
from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

app = Flask(__name__) 

engine = create_engine('sqlite:///api_python.db')
Base = declarative_base()

class Parent(Base):
    __tablename__ = 'CAPTURE'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime(timezone=True), server_default=func.current_timestamp())
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

@app.route("/history/")
def read():
    conn = sqlite3.connect("api_python.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT time, count FROM CAPTURE;""")
    data=''
    rows=cursor.fetchall()
    for row in rows:
        captureDate=datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
        entry_date=captureDate.strftime("%d/%m/%Y")
        entry_time=captureDate.strftime("%H:%M:%S")
        count=str(row[1])
        data+="Le "+entry_date+" à "+entry_time+", il y avait "+count+" personne(s) présente(s).\n"
    return Response(data, mimetype='text/plain')

@app.route("/count/<value>")
def count(value):
    conn = sqlite3.connect("api_python.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO CAPTURE(count) VALUES("+str(value)+")")
    conn.commit()
    lastid=cursor.lastrowid
    return Response(str(lastid)+"\n", mimetype='text/plain')

@app.route("/presence/<captureid>/<machash>")
def presence(captureid, machash):
    conn = sqlite3.connect("api_python.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO PRESENCE(hash,parent_id) VALUES('"+machash+"',"+str(captureid)+")")
    conn.commit()
    return Response("OK", mimetype='text/plain')

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)