#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, Response
import csv, datetime

app = Flask(__name__)

#retourne l’historique des mesures collectées, au format CSV
@app.route("/history/")
def read():
    data = open("./history.csv", "r")
    return Response(data, mimetype='text/plain')

 #enregistre la valeur :value pour la date/heure correspondant à celle de la requête
 #retourne “OK” ou “ERROR”, selon que l’enregistrement est réussi ou non.
@app.route("/count/<value>/")
def count(value):
    now=datetime.datetime.now()
    nowStr="%02d/%02d/%02d" % (now.day, now.month, now.year)
    data=[nowStr, value]
    try:
        with open('./history.csv', 'a') as f:
            writer=csv.writer(f)
            writer.writerow(data)
        return Response("OK", mimetype='text/plain')
    except:
        return Response("ERROR", mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)