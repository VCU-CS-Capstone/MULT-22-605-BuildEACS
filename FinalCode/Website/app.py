from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "hello"

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'CapstonePassword'
app.config['MYSQL_DB'] = 'sys'

mysql = MySQL(app)

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        table = request.form["tables"]
        action = request.form["actions"]
        if table == "users":
            if action == "add":
                return redirect(url_for("addUser"))
            elif action == "modify":
                return redirect(url_for("findUser"))
            elif action == "delete":
                return redirect(url_for("deleteUser"))
        elif table == "equip":
            if action == "add":
                return redirect(url_for("addEquip"))
            elif action == "modify":
                return redirect(url_for("findEquip"))
            elif action == "delete":
                return redirect(url_for("deleteEquip"))
        elif table == "cert":
            if action == "add":
                return redirect(url_for("addCert"))
            elif action == "modify":
                return redirect(url_for("findCert"))
            elif action == "delete":
                return redirect(url_for("deleteCert"))
    else:
        return render_template('index.html')

@app.route("/addUser", methods=["POST", "GET"])
def addUser():
    cur = mysql.connection.cursor()
    cur.execute("select * from Certifications")
    data = cur.fetchall()
    cur.execute("select * from CertUser")
    numUserCerts = cur.fetchall()

    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        userid = int(request.form["userid"])
        phonenum = request.form["phonenum"]
        admin = int(request.form["admin"])
        emailaddress = request.form["emailaddress"]

        certsSelected = request.form.getlist("certs")
        index = len(numUserCerts)

        cur.execute("SET foreign_key_checks = 0")
        for cert in certsSelected:
            index = index + 1
            cur.execute("INSERT INTO CertUser(userID, certID, indexID) VALUES(%s, %s, %s)", (userid, cert, index))
        cur.execute("INSERT INTO Users(fName, lName, userID, phone, isAdmin, email) VALUES(%s, %s, %s, %s, %s, %s)", (fname, lname, userid, phonenum, admin, emailaddress))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("index"))

    else:
        return render_template('addUser.html', values=data)

@app.route("/addEquip", methods=["POST", "GET"])
def addEquip():
    if request.method == "POST":
        eName = request.form["ename"]
        equipID = request.form["eid"]
        eType = request.form["etype"]
        boxNum = request.form["boxnum"]
        wifi_Address = request.form["wifiadd"]
        modelNo = request.form["model"]
        serialNo = request.form["serial"]
        certNeeded = request.form["certneeded"]
        lastMain = request.form["lastmain"]
        surgeLevel = request.form["surge"]

        if lastMain == '':
            lastMain = None
        if eType == '':
            eType = None
        if serialNo == '':
            serialNo = None
        if surgeLevel == '':
            surgeLevel = None

        cur = mysql.connection.cursor()

        cur.execute("SET foreign_key_checks = 0")
        cur.execute("INSERT INTO Equipment(eName, equipID, eType, boxNum, wifi_Address, modelNo, serialNo, powerState, lastUsed, certNeeded, lastMaint, needMaint, eSchedule, surgeLevel) VALUES(%s, %s, %s, %s, %s, %s, %s, 0, NULL, %s, %s, NULL, NULL, %s)", (eName, equipID, eType, boxNum, wifi_Address, modelNo, serialNo, certNeeded, lastMain, surgeLevel))
        cur.execute("INSERT INTO EqCert(equipID, certID) VALUES(%s, %s)", (equipID, certNeeded))

        mysql.connection.commit()
        cur.close()
        return redirect(url_for("index"))
    else:
        return render_template('addEquip.html')

@app.route("/addCert", methods=["POST", "GET"])
def addCert():
    if request.method == "POST":
        cname = request.form["cname"]
        certid = request.form["certid"]
        certtype = request.form["certtype"]
        equipid = int(request.form["equipid"])

        if certtype == '':
            certtype = None

        cur = mysql.connection.cursor()
        cur.execute("SET foreign_key_checks = 0")
        cur.execute("INSERT INTO Certifications(cName, certID, cType, equipID) VALUES(%s, %s, %s, %s)", (cname, certid, certtype, equipid))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("index"))

    else:
        return render_template('addCert.html')


@app.route("/modifyUser<values>", methods=["POST", "GET"])
def modifyUser(values):
    cur = mysql.connection.cursor()
    cur.execute("select * from Users where userID = %s", (values,))
    data = cur.fetchall()
    cur.execute("select * from Certifications")
    certifications = cur.fetchall()
    cur.execute("select * from CertUser")
    numUserCerts = cur.fetchall()

    cur.execute("select certID from CertUser where userID = %s", (values,))
    selectedItems = cur.fetchall()
    a_tuple = ()
    for item in selectedItems:
        a_tuple = a_tuple + item

    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        userid = int(request.form["userid"])
        phonenum = request.form["phonenum"]
        admin = int(request.form["admin"])
        emailaddress = request.form["emailaddress"]

        certsSelected = request.form.getlist("certs")
        index = len(numUserCerts)

        cur.execute("SET foreign_key_checks = 0")
        for cert in a_tuple:
            if cert not in certsSelected:
                cur.execute("DELETE FROM CertUser WHERE userID = %s AND certID = %s", (userid, cert))
        for cert in certsSelected:
            if cert not in a_tuple:
                index = index + 1
                cur.execute("INSERT INTO CertUser(userID, certID, indexID) VALUES(%s, %s, %s)", (userid, cert, index))

        cur.execute("select indexID from CertUser")
        indexes = cur.fetchall()
        val = 0

        for ind in indexes:
            val = val + 1
            cur.execute("UPDATE CertUser SET indexID = %s WHERE indexID = %s", (val, ind))
        cur.execute("UPDATE Users SET fName = %s, lName = %s, userID = %s, phone = %s, isAdmin = %s, email = %s WHERE userID = %s", (fname, lname, userid, phonenum, admin, emailaddress, values))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("index"))
    return render_template('modifyUser.html', values = data, certs=certifications, selectedCerts=a_tuple)

@app.route("/modifyEquip<values>", methods=["POST", "GET"])
def modifyEquip(values):
    cur = mysql.connection.cursor()
    cur.execute("select * from Equipment where equipID = %s", (values,))
    data = cur.fetchall()
    if request.method == "POST":
        eName = request.form["ename"]
        equipID = request.form["eid"]
        eType = request.form["etype"]
        boxNum = request.form["boxnum"]
        wifi_Address = request.form["wifiadd"]
        modelNo = request.form["model"]
        serialNo = request.form["serial"]
        powerState = request.form["power"]
        lastUsed = request.form["lastused"]
        certNeeded = request.form["certneeded"]
        lastMaint = request.form["lastmain"]
        needMaint = request.form["needmain"]
        eSchedule = request.form["schedule"]
        surgeLevel = request.form["surge"]

        if lastMaint == '':
            lastMaint = None
        if eType == '':
            eType = None
        if serialNo == '':
            serialNo = None
        if surgeLevel == '':
            surgeLevel = None
        if lastUsed == '':
            lastUsed = None
        if needMaint == '':
            needMaint = None
        if eSchedule == '':
            eSchedule = None

        cur.execute("SET foreign_key_checks = 0")
        cur.execute("UPDATE Equipment SET eName = %s, equipID = %s, eType = %s, boxNum = %s, wifi_Address = %s, modelNo = %s, serialNo = %s, powerState = %s, lastUsed = %s, certNeeded = %s, lastMaint = %s, needMaint = %s, eSchedule = %s, surgeLevel = %s WHERE equipID = %s", (eName, equipID, eType, boxNum, wifi_Address, modelNo, serialNo, powerState, lastUsed, certNeeded, lastMaint, needMaint, eSchedule, surgeLevel, values))
        cur.execute("UPDATE EqCert SET equipID = %s, certID = %s WHERE equipID = %s", (equipID, certNeeded))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for("index"))

    return render_template('modifyEquip.html', values = data)

@app.route("/modifyCert<values>", methods=["POST", "GET"])
def modifyCert(values):
    cur = mysql.connection.cursor()
    cur.execute("select * from Certifications where certID = %s", (values,))
    data = cur.fetchall()
    if request.method == "POST":
        cname = request.form["cname"]
        certid = request.form["certid"]
        certtype = request.form["certtype"]
        equipid = int(request.form["equipid"])

        if certtype == '':
            certtype = None

        cur.execute("SET foreign_key_checks = 0")
        cur.execute("UPDATE Certifications SET cName = %s, certID = %s, cType = %s, equipID = %s WHERE certID = %s", (cname, certid, certtype, equipid, values))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for("index"))
    return render_template('modifyCert.html', values = data)

@app.route("/deleteUser", methods=["POST", "GET"])
def deleteUser():
    cur = mysql.connection.cursor()
    cur.execute("select * from Users")
    data = cur.fetchall()
    if request.method == "POST":
        userid = request.form["fname"]
        cur.execute("SET foreign_key_checks = 0")
        cur.execute("DELETE FROM Users WHERE userID = %s", (userid,))
        cur.execute("DELETE FROM CertUser WHERE userID = %s", (userid,))

        mysql.connection.commit()
        cur.close()
        return redirect(url_for("index"))
    return render_template('deleteUser.html', values=data)

@app.route("/deleteEquip", methods=["POST", "GET"])
def deleteEquip():
    cur = mysql.connection.cursor()
    cur.execute("select * from Equipment")
    data = cur.fetchall()
    if request.method == "POST":
        equipid = request.form["equipid"]
        cur.execute("DELETE FROM EqCert WHERE equipID = %s", (equipid,))
        cur.execute("DELETE FROM Equipment WHERE equipID = %s", (equipid,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("index"))
    return render_template('deleteEquip.html', values=data)


@app.route("/deleteCert", methods=["POST", "GET"])
def deleteCert():
    cur = mysql.connection.cursor()
    cur.execute("select * from Certifications")
    data = cur.fetchall()
    if request.method == "POST":
        certId = request.form["certId"]
        cur.execute("DELETE FROM Certifications WHERE certID = %s", (certId,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("index"))
    return render_template('deleteCert.html', values=data)


@app.route("/findUser", methods=["POST", "GET"])
def findUser():
    cur = mysql.connection.cursor()
    cur.execute("select * from Users")
    data = cur.fetchall()
    if request.method == "POST":
        userid = request.form["userId"]
        return redirect(url_for("modifyUser", values=userid))
    return render_template('findUser.html', values=data)

@app.route("/findEquip", methods=["POST", "GET"])
def findEquip():
    cur = mysql.connection.cursor()
    cur.execute("select * from Equipment")
    data = cur.fetchall()
    if request.method == "POST":
        equipid = request.form["equipId"]
        return redirect(url_for("modifyEquip", values=equipid))
    return render_template('findEquip.html', values=data)

@app.route("/findCert", methods=["POST", "GET"])
def findCert():
    cur = mysql.connection.cursor()
    cur.execute("select * from Certifications")
    data = cur.fetchall()
    if request.method == "POST":
        certid = request.form["certId"]
        return redirect(url_for("modifyCert", values=certid))
    return render_template('findCert.html', values=data)


if __name__ == "__main__":
    app.run()
