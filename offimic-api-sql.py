#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from flask import Flask, Response
import csv, datetime
import mysql.connector

app = Flask(__name__)
conn=mysql.connector.connect(host="localhost", user="offi", password="offi", database="offi")
cursor=conn.cursor()

@app.route("/")
def accueil():
    # lire views/index.html
    # retourner le fichier avec un mimetype="text/html"
    return "Pour voir l'historique des connections sur le réseau d'Officience, veuillez visiter la page:http://localhost:5000/history"

#retourne l’historique des mesures collectées dans la base de données
@app.route("/history/")
def read():
    cursor.execute("""SELECT entry_date, count FROM history;""")
    data=""
    rows=cursor.fetchall()
    for row in rows:
        entry_date=row[0].strftime("%d/%m/%Y")
        entry_time=row[0].strftime("%H:%M:%S")
        count=str(row[1])
        data+="Le "+entry_date+ " à "+entry_time+", il y avait "+count+" personne(s) présente(s)."+"\n"
    return Response(data, mimetype='text/plain')

 #enregistre la valeur :value pour la date/heure correspondant à celle de la requête
 #retourne “OK” ou “ERROR”, selon que l’enregistrement est réussi ou non.
@app.route("/count/<value>/")
def count(value):
    now=datetime.datetime.now()
    nowStr="%04d-%02d-%02d %02d:%02d:%02d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    try:
        cursor.execute("""INSERT INTO history(entry_date, count) VALUES(%s, %s)""", (nowStr, value))
        conn.commit()
        return Response("OK", mimetype='text/plain')
    except:
        return Response("ERROR", mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)