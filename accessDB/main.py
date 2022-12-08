from flask import Blueprint, current_app, flash, request, render_template, redirect, url_for
import random
import psycopg2

__version__ = '0.1.0'


def connect():
    conn = psycopg2.connect(dbname='arkea', user='postgres',
                            password='admin', host='bdd.harruis.fr', port='5432')
    cur = conn.cursor()
    return conn, cur


def close(conn, cur):
    cur.close()
    conn.close()


def addClient():
    try:
        conn, cur = connect()
        numcli = request.json.get("numcli", '')
        civilite = request.json.get("civilite", '')
        nomcli = request.json.get("nomcli", '')
        prenomcli = request.json.get("prenomcli", '')
        adrcli = request.json.get("adrcli", '')
        vilcli = request.json.get("vilcli", '')
        cur.execute("INSERT INTO arkea.\"Client\" (numcli, civilite, nomcli, prenomcli, adrcli, vilcli) VALUES (%s, '%s', '%s', '%s', '%s', '%s');" % (numcli, civilite, nomcli, prenomcli, adrcli, vilcli))
        conn.commit()
        close(conn, cur)
    except Exception as e:
        close(conn, cur)
        print(e)
        return {"Status": "Error", "Message": str(e)}, 400
    return {"Status": "Done"}

def addAccount():
    try:
        conn, cur = connect()

        numcli = request.json.get("numcli", '')
        numco = int(random.random()* 5000)
        typecompte = request.json.get("typecompte", '')
        soldecompte = request.json.get("soldecompte", '')
        cur.execute("INSERT INTO arkea.\"Compte\" (numco, numcli, typecompte, soldecompte) VALUES (%s, %s, %s, %s);" % (numco, numcli, typecompte, soldecompte))
        conn.commit()
        close(conn, cur)
    except Exception as e:
        close(conn, cur)
        print(e)
        return {"Status": "Error", "Message": str(e)}, 400
    return {"Status": "Done"}

def getAllClients():
    try:
        conn, cur = connect()
        cur.execute("Select civilite + ' ' + prenomcli + ' ' + nomcli, numcli from arkea.\"Client\";")
        result = cur.fetchone()
        close(conn, cur)
    except Exception as e:
        close(conn, cur)
        return {"Status": "Error", "Message": str(e)}
    return {"Status": "Done", "Value" : result}

def getTransactionsNumcli():
    try:
        conn, cur = connect()
        numcli = request.json.get("numcli", '')
        cur.execute("Select * from arkea.\"Operation\" where numcli=%s;" %numcli)
        result = cur.fetchone()
        close(conn, cur)
    except Exception as e:
        close(conn, cur)
        return {"Status": "Error", "Message": str(e)}
    return {"Status": "Done", "Value" : result}

def getTransactionsDate():
    try:
        conn, cur = connect()
        debut = request.json.get("debut", '')
        fin = request.json.get("fin", '')
        cur.execute("Select * from arkea.\"Operation\" where dateop BETWEEN '%s' AND '%s';" %(debut, fin))
        result = cur.fetchone()
        close(conn, cur)
    except Exception as e:
        close(conn, cur)
        return {"Status": "Error", "Message": str(e)}
    return {"Status": "Done", "Value" : result}


def getTransactionsDate():
    try:
        conn, cur = connect()
        debut = request.json.get("debut", '')
        fin = request.json.get("fin", '')
        cur.execute("Select * from arkea.\"Operation\" where dateop BETWEEN '%s' AND '%s';" %(debut, fin))
        result = cur.fetchone()
        close(conn, cur)
    except Exception as e:
        close(conn, cur)
        return {"Status": "Error", "Message": str(e)}
    return {"Status": "Done", "Value" : result}

def getTransactionsNumcar():
    try:
        conn, cur = connect()
        numcar = request.json.get("numcar", '')
        cur.execute("Select * from arkea.\"Operation\" where numcar='%s';" %numcar)
        result = cur.fetchone()
        close(conn, cur)
    except Exception as e:
        close(conn, cur)
        return {"Status": "Error", "Message": str(e)}
    return {"Status": "Done", "Value" : result}


def getStats():
    try:
        conn, cur = connect()
        cur.execute("Select sum(montant), count(*) from arkea.\"Operation\";")
        result = cur.fetchone()
        print(result)
        close(conn, cur)
    except Exception as e:
        close(conn, cur)
        return {"Status": "Error", "Message": str(e)}
    return {"Status": "Done", "Montant" : result[0], "TotalOp" : result[1]}



class AccessDB(Blueprint):

    def __init__(self, name='accessDB', import_name=__name__, *args, **kwargs):
        Blueprint.__init__(self, name, import_name,
                           template_folder='templates', *args, **kwargs)
        self.add_url_rule('/addClient', 'addClient', addClient, methods=['POST'])
        self.add_url_rule('/addAccount', 'addAccount', addAccount, methods=['POST'])
        self.add_url_rule('/getAllClients', 'getAllClients', getAllClients, methods=['GET'])
        self.add_url_rule('/getTransactionsNumcli', 'getTransactionsNumcli', getTransactionsNumcli, methods=['GET'])
        self.add_url_rule('/getTransactionsDate', 'getTransactionsDate', getTransactionsDate, methods=['GET'])
        self.add_url_rule('/getTransactionsNumcar', 'getTransactionsNumcar', getTransactionsNumcar, methods=['GET'])
        self.add_url_rule('/getStats', 'getStats', getStats, methods=['GET'])


    def register(self, app, options):
        try:
            Blueprint.register(self, app, options)
        except Exception:
            app.logger.error("init AccessDB on register is failed")
