from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QRadioButton, QMessageBox, QLabel, QGridLayout, QApplication, QWidget, QGroupBox
from PyQt5.QtCore import Qt
import mysql.connector as mysql
import pyodbc
import os

class ConnectionChecker(QWidget):
    currentData = {}
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(800,300)
        self.setWindowTitle("Database Connection Checker")
        self.interface()
        self.show()


    def interface(self):
        self.loginOption = 1
        self.labelUser = QLabel("User:", self)
        self.labelPassword = QLabel("Password:", self)
        self.labelDatabase = QLabel("Database:", self)
        self.labelHost = QLabel("Server:", self)
        self.labelPort = QLabel("Port:", self)
        self.labelLoginType =QLabel("Connection method:",self)
        self.labelDatabaseType =QLabel("Database type:",self)
        self.labelString = QLabel("Insert connection string:")

        self.user = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.dbname = QLineEdit()
        self.host = QLineEdit()
        self.host.setPlaceholderText("localhost")
        self.port = QLineEdit()
        self.port.setPlaceholderText("3306")

        self.authString = QLineEdit()
        self.radioMysql =QRadioButton("MySQL")
        self.radioMssql = QRadioButton("MSSQL")
        self.buttonClassic = QPushButton("Classic method")
        self.buttonString = QPushButton("Connection string method")

        self.layoutS= QHBoxLayout()
        self.layoutS.addWidget(self.buttonClassic)
        self.layoutS.addWidget(self.buttonString)
        self.layoutS.itemAt(0).widget().setChecked(True)

        self.layoutR = QHBoxLayout()
        self.layoutR.addWidget(self.radioMysql)
        self.layoutR.addWidget(self.radioMssql)
        self.layoutR.itemAt(0).widget().setChecked(True)

        self.exitBtn = QPushButton("&Exit", self)
        self.checkBtn = QPushButton("&Check connection", self)
        self.exitBtn.resize(self.exitBtn.sizeHint())
        self.checkBtn.resize(self.checkBtn.sizeHint())

        self.layoutT = QGridLayout()
        self.layoutT.addWidget(self.labelLoginType, 6, 0, 1, 1)
        self.layoutT.addLayout(self.layoutS, 7, 0, 1, 3)
        self.layoutT.addWidget(self.labelDatabaseType, 8, 0, 1, 1)
        self.layoutT.addLayout(self.layoutR, 9, 0, 1, 3)
        self.layoutT.addWidget(self.labelHost, 10, 0, 1, 1)
        self.layoutT.addWidget(self.labelPort, 10, 2, 1, 1)
        self.layoutT.addWidget(self.host, 11, 0, 1, 2)
        self.layoutT.addWidget(self.port, 11, 2, 1, 1)
        self.layoutT.addWidget(self.labelUser, 12, 0, 1, 1)
        self.layoutT.addWidget(self.labelPassword, 12, 1, 1, 1)
        self.layoutT.addWidget(self.labelDatabase, 12, 2, 1, 1)
        self.layoutT.addWidget(self.user, 13, 0, 1, 1)
        self.layoutT.addWidget(self.password, 13, 1, 1, 1)
        self.layoutT.addWidget(self.dbname, 13, 2, 1, 1)
        self.layoutT.addWidget(self.checkBtn, 14, 0, 1, 3)
        self.layoutT.addWidget(self.exitBtn, 15, 0, 1, 3)

        #self.buttonClassic.clicked.connect(self.layoutClassic)
        self.buttonString.clicked.connect(self.layoutString)
        self.exitBtn.clicked.connect(self.end)
        self.checkBtn.clicked.connect(self.check)

        self.setLayout(self.layoutT)


    def layoutClassic(self):
        self.saveCurrentValues("string")
        self.switchLayout()
        self.interface()
        self.loadCurrentValues("classic")


    def layoutString(self):
        self.saveCurrentValues("classic")
        self.switchLayout()
        self.interfaceString()
        self.loadCurrentValues("string")

    def interfaceString(self):
        self.loginOption = 2
        self.labelLoginType =QLabel("Connection method:",self)
        self.labelDatabaseType =QLabel("Database type:",self)
        self.authString = QLineEdit()
        self.radioMysql =QRadioButton("MySQL")
        self.radioMssql = QRadioButton("MSSQL")
        self.buttonClassic = QPushButton("Classic method")
        self.buttonString = QPushButton("Connection string method")
        self.labelString = QLabel("Insert connection string:")

        self.layoutS= QHBoxLayout()
        self.layoutS.addWidget(self.buttonClassic)
        self.layoutS.addWidget(self.buttonString)
        self.layoutS.itemAt(0).widget().setChecked(True)

        self.layoutR = QHBoxLayout()
        self.layoutR.addWidget(self.radioMysql)
        self.layoutR.addWidget(self.radioMssql)
        self.layoutR.itemAt(0).widget().setChecked(True)

        self.exitBtn = QPushButton("&Exit", self)
        self.checkBtn = QPushButton("&Check connection", self)
        self.exitBtn.resize(self.exitBtn.sizeHint())
        self.checkBtn.resize(self.checkBtn.sizeHint())

        layoutX = QGridLayout()
        layoutX.addWidget(self.labelLoginType, 6, 0, 1, 3)
        layoutX.addLayout(self.layoutS, 7, 0, 1, 3)
        layoutX.addWidget(self.labelDatabaseType, 8, 0, 1, 1)
        layoutX.addLayout(self.layoutR, 9, 0, 1, 3)
        layoutX.addWidget(self.labelString, 10, 0, 1, 3)
        layoutX.addWidget(self.authString, 11, 0, 1, 3)
        layoutX.addWidget(self.checkBtn, 12, 0, 1, 3)
        layoutX.addWidget(self.exitBtn, 13, 0, 1, 3)

        self.buttonClassic.clicked.connect(self.layoutClassic)
        #self.buttonString.clicked.connect(self.layoutString)
        self.exitBtn.clicked.connect(self.end)
        self.checkBtn.clicked.connect(self.check)

        self.setLayout(layoutX)

    def switchLayout(self):
        QWidget().setLayout(self.layout())

    def end(self):
        self.close()

    def saveCurrentValues(self, window):
        if(self.radioMysql.isChecked()):
            self.currentData['radio'] = "MySql"
        else:
            self.currentData['radio'] = "MsSql"

        if window == "classic":
            self.currentData['host'] = self.host.text()
            self.currentData['port'] = self.port.text()
            self.currentData['user'] = self.user.text()
            self.currentData['password'] = self.password.text()
            self.currentData['dbname'] = self.dbname.text()
        else:
            self.currentData['authString'] = self.authString.text()

    def loadCurrentValues(self, window):
        if self.currentData['radio'] == "MySql":
            self.radioMysql.setChecked(True)
        else:
            self.radioMssql.setChecked(True)

        if window == "classic":
            self.host.setText(self.currentData['host'] if 'host' in self.currentData else "")
            self.password.setText(self.currentData['password'] if 'password' in self.currentData else "")
            self.port.setText(self.currentData['port'] if 'port' in self.currentData else "")
            self.dbname.setText(self.currentData['dbname'] if 'dbname' in self.currentData else "")
            self.user.setText(self.currentData['user'] if 'user' in self.currentData else "")
        else:
            self.authString.setText(self.currentData['authString'] if 'authString' in self.currentData else "")

    def check(self):
        nadawca = self.sender()
        if self.loginOption == 1:  # Połączenie klasyczne
            login = str(self.user.text())
            password = str(self.password.text())
            db_name = str(self.dbname.text())
            host = str(self.host.text())

            config = {
                'user': login,
                'password': password,
                'host': host,
                'database': db_name
            }

            allGood = True
            if(self.port.text() != ''):
                try:
                    port = int(self.port.text())
                except Exception as e:
                    allGood = False
                    QMessageBox.critical(self, "Error", "Port has to be a number!", QMessageBox.Ok)
                else:
                    config['port'] = port

            if(allGood):
                if(self.radioMysql.isChecked()):
                    self.Mysql(config)
                else:
                    self.Mssql(config)

        elif self.loginOption == 2: # Connection string
            string = str(self.authString.text())
            if string == '':
                QMessageBox.critical(self, "Error", "This field cannot be empty!", QMessageBox.Ok)
            else:
                if(self.radioMysql.isChecked()):
                    self.Mysql(string)
                else:
                    self.Mssql(string)

    def Mysql(self,connectionData):
        if self.loginOption == 1:
            try:
                db = mysql.connect(**connectionData)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"A connection to database could not be established! Error: {e}", QMessageBox.Ok)
            else:
                if not db.is_connected():
                    QMessageBox.critical(self, "Error", f"A connection to database could not be established! Error: {e}", QMessageBox.Ok)
                else:
                    QMessageBox.information(self,"Success","The connection to the database has been successfully established.")
        elif self.loginOption == 2:
            if connectionData[-1]==';':     # If there is ';' at the end of the string - delete it
                connectionData = connectionData[0:-1]
            try:
                connectionParams = dict(el.split('=') for el in connectionData.split(';'))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Format of the connection string is not valid!", QMessageBox.Ok)
            else:
                config = {
                        'user': connectionParams['Uid'] if "Uid" in connectionParams else None,
                        'password': connectionParams['Pwd'] if "Pwd" in connectionParams else None,
                        'host': connectionParams['Server'] if "Server" in connectionParams else None,
                        'database': connectionParams['Database'] if "Database" in connectionParams else None
                 }

                if 'Port' in connectionParams:
                    config['port'] = connectionParams['Port']

                try:
                    db = mysql.connect(**config)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"A connection to database could not be established! Error: {e}", QMessageBox.Ok)
                else:
                    if not db.is_connected():
                        QMessageBox.critical(self, "Error", f"A connection to database could not be established! Error: {e}", QMessageBox.Ok)
                    else:
                        QMessageBox.information(self,"Success","The connection to the database has been successfully established.")

    def Mssql(self, connectionData):
        if self.loginOption == 2:
            try:
                db = pyodbc.connect(connectionData)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"A connection to database could not be established! Error: {e}", QMessageBox.Ok)
            else:
                QMessageBox.information(self,"Success","The connection to the database has been successfully established.")
        elif self.loginOption == 1:
            if 'port' in connectionData:
                connectionString = f"Driver={{SQL Server}};Server={connectionData['host']},{connectionData['port']};Database={connectionData['database']};Uid={connectionData['user']};Pwd={connectionData['password']};"
            else:
                connectionString = f"Driver={{SQL Server}};Server={connectionData['host']};Database={connectionData['database']};Uid={connectionData['user']};Pwd={connectionData['password']};"

            try:
                db = pyodbc.connect(connectionString)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"A connection to database could not be established! Error: {e}", QMessageBox.Ok)
            else:
                QMessageBox.information(self,"Success","The connection to the database has been successfully established.")

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = ConnectionChecker()
    sys.exit(app.exec_())
