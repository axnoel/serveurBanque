from flask import Blueprint, request
import random
import psycopg2

__version__ = '0.1.0'

dbname = 'arkea'
user = 'postgres'
password = 'admin'
host = 'bdd.harruis.fr'
port = '5432'


def connect():
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cur = conn.cursor()
    print(conn)
    print(cur)
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
        cur.execute("INSERT INTO arkea.\"Client\" (numcli, civilite, nomcli, prenomcli, adrcli, vilcli) VALUES (%s, '%s', '%s', '%s', '%s', '%s');" % (
            numcli, civilite, nomcli, prenomcli, adrcli, vilcli))
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
        numco = int(random.random() * 5000)
        typecompte = request.json.get("typecompte", '')
        soldecompte = request.json.get("soldecompte", '')
        cur.execute("INSERT INTO arkea.\"Compte\" (numco,typecompte, soldecompte) VALUES (%s, %s, %s);" % (
            numco, typecompte, soldecompte))
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
        cur.execute(
            "Select concat(civilite, ' ', prenomcli, ' ', nomcli), numcli from arkea.\"Client\";")
        result = cur.fetchall()
        close(conn, cur)
    except Exception as e:
        close(conn, cur)
        return {"Status": "Error", "Message": str(e)}
    return {"Status": "Done", "Value": result}


def getTransactionsNumcli():
    try:
        conn, cur = connect()
        numcli = request.json.get("numcli", '')
        cur.execute(
            "Select * from arkea.\"Operation\" where numco=(Select numco from arkea.\"Compte\" where numcli='%s');" % numcli)
        result = cur.fetchall()
        value = []
        for res in result:
            value.append({"numop" : res[0], "numco" : res[4], "dateop" : res[5], "montantop" : res[6]})
        close(conn, cur)
    except Exception as e:
        close(conn, cur)
        return {"Status": "Error", "Message": str(e)}
    return {"Status": "Done", "Value": value}


def getTransactionsDate():
    try:
        conn, cur = connect()
        debut = request.json.get("debut", '')
        fin = request.json.get("fin", '')
        cur.execute(
            "Select * from arkea.\"Operation\" where dateop BETWEEN '%s' AND '%s';" % (debut, fin))
        result = cur.fetchall()
        value = []
        for res in result:
            value.append({"numop" : res[0], "numco" : res[4], "dateop" : res[5], "montantop" : res[6]})
        print("Hello")
        print(value)
        close(conn, cur)
    except Exception as e:
        print(str(e))
        close(conn, cur)
        return {"Status": "Error", "Message": str(e)}
    return {"Status": "Done", "Value": value}


def getTransactionsNumcar():
    try:
        conn, cur = connect()
        numcar = request.json.get("numcar", '')
        cur.execute(
            "Select * from arkea.\"Operation\" where numcar='%s';" % numcar)
        result = cur.fetchall()
        value = []
        for res in result:
            value.append({"numop" : res[0], "numco" : res[4], "dateop" : res[5], "montantop" : res[6]})
        close(conn, cur)
    except Exception as e:
        close(conn, cur)
        return {"Status": "Error", "Message": str(e)}
    return {"Status": "Done", "Value": value}


def getStats():
    try:
        conn, cur = connect()
        cur.execute("Select sum(montantop), count(*) from arkea.\"Operation\";")
        result = cur.fetchone()
        liste_annee = []
        cur.execute("Select EXTRACT(YEAR FROM dateop) ,sum(montantop), count(*) from arkea.\"Operation\" group by EXTRACT(YEAR FROM dateop) order by EXTRACT(YEAR FROM dateop) desc;")
        for res_ann in cur.fetchall():
            liste_annee.append(
                {"Annee": int(res_ann[0]), "Montant": res_ann[1], "TotalOp": res_ann[2]})
        cur.execute("Select sum(montantop), count(*), CAST(avg(montantop) as NUMERIC(7,2)), min(montantop), max(montantop) from arkea.\"Operation\" where numgab is not NULL;")
        res = cur.fetchone()
        op_gab = {"Montant_Total": res[0], "Nbr_Operations": res[1],
                  "Moyenne_OP": res[2], "Min_OP": res[3], "Max_OP": res[4]}
        cur.execute("Select o.numgab, CONCAT(g.adrgab, ', ', g.villegab, ', ', g.codep), sum(montantop), count(*), CAST(avg(montantop) as NUMERIC(7,2)), min(montantop), max(montantop) from arkea.\"Operation\" o join arkea.\"GAB\" g on o.numgab = g.numgab where o.numgab is not NULL group by o.numgab, g.adrgab,g.villegab, g.codep;")
        op_gab_par_gab = []
        for res in cur.fetchall():
            op_gab_par_gab.append({"Num_Gab": res[0], "Adr_Gab": res[1], "Montant_Total": res[2],
                                  "Nbr_Operations": res[3], "Moyenne_OP": res[4], "Min_OP": res[5], "Max_OP": res[6]})
        cur.execute("Select sum(montantop), count(*), CAST(avg(montantop) as NUMERIC(7,2)), min(montantop), max(montantop) from arkea.\"Operation\" where numcome is not NULL;")
        res = cur.fetchone()
        op_com = {"Montant_Total": res[0], "Nbr_Operations": res[1],
                  "Moyenne_OP": res[2], "Min_OP": res[3], "Max_OP": res[4]}

        cur.execute("Select EXTRACT(MONTH FROM dateop), EXTRACT(YEAR FROM dateop) ,sum(montantop), CAST(avg(montantop) as NUMERIC(7,2)) from arkea.\"Operation\" group by EXTRACT(YEAR FROM dateop), EXTRACT(MONTH FROM dateop) order by EXTRACT(YEAR FROM dateop) desc, EXTRACT(MONTH FROM dateop) desc;")

        liste_mois = []
        for res in cur.fetchall():
            liste_mois.append({"Mois": res[0], "Annee": int(
                res[1]), "Montant_Total": res[2], "Moyenne_OP": res[3]})
        close(conn, cur)
    except Exception as e:
        close(conn, cur)
        print(e)
        return {"Status": "Error", "Message": str(e)}
    return {"Status": "Done", "Montant_total": result[0], "Nbr_Operations": result[1], "Annuelle": liste_annee, "OP_GAB": op_gab, "OP_GAB_Par_GAB": op_gab_par_gab, "OP_Commercants": op_com, "Mensuelle": liste_mois}


class AccessDB(Blueprint):

    def __init__(self, name='accessDB', import_name=__name__, *args, **kwargs):
        Blueprint.__init__(self, name, import_name,
                           template_folder='templates', *args, **kwargs)
        self.add_url_rule('/addClient', 'addClient',
                          addClient, methods=['POST'])
        self.add_url_rule('/addAccount', 'addAccount',
                          addAccount, methods=['POST'])
        self.add_url_rule('/getAllClients', 'getAllClients',
                          getAllClients, methods=['GET'])
        self.add_url_rule('/getTransactionsNumcli', 'getTransactionsNumcli',
                          getTransactionsNumcli, methods=['GET'])
        self.add_url_rule('/getTransactionsDate', 'getTransactionsDate',
                          getTransactionsDate, methods=['GET'])
        self.add_url_rule('/getTransactionsNumcar', 'getTransactionsNumcar',
                          getTransactionsNumcar, methods=['GET'])
        self.add_url_rule('/getStats', 'getStats', getStats, methods=['GET'])

    def register(self, app, options):
        try:
            Blueprint.register(self, app, options)
        except Exception:
            app.logger.error("init AccessDB on register is failed")
