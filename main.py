import sqlite3
import sys
from PyQt5 import uic

from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem



TITLE = ['СОРТ', 'ЗЁРНА/МОЛОТЫЙ', 'ОБЪЁМ в гр', 'ЦЕНА, руб.', 'СТЕПЕНЬ ОБЖАРКИ', 'ВКУС']
TITLE0 = list(map(lambda x: str(x), range(1, 7)))
SIZE = [1200, 600]

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('coffee.sqlite')
        uic.loadUi('main.ui', self)
        self.initUi()

    def initUi(self):
        self.setGeometry(300, 300, *SIZE)
        self.setWindowTitle('Эспрессо')
        self.statusBar().showMessage("This is status bar")
        cur = self.con.cursor()
        result = cur.execute("SELECT degree FROM degrees").fetchall()
        self.comboBox.addItems([item[0] for item in result])
        self.pushButton_2.clicked.connect(self.filter)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        cur = self.con.cursor()
        try:
            if self.lineEdit.text():
                result = cur.execute(f"{self.lineEdit.text()}").fetchall()
            else:
                result = cur.execute(
                    """SELECT DISTINCT sorts_coffee.name, ground_beans, volume, price, degrees.degree, sorts_coffee.taste 
                    FROM sorts_coffee, degrees JOIN products
                    ON sorts_coffee.id_sort = products.id_sort AND
                    degrees.id = products.id_degree
                    ORDER BY sorts_coffee.name""").fetchall()
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(len(result[0]))
            if not self.lineEdit.text():
                self.tableWidget.setHorizontalHeaderLabels(TITLE)
            else:
                self.tableWidget.setHorizontalHeaderLabels(TITLE0)

            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
                    self.tableWidget.resizeColumnsToContents()
        except Exception as e:
            print(e)
            self.statusBar().showMessage(str(e))
            self.tableWidget.clearContents()

    def filter(self):
        cur = self.con.cursor()
        result = cur.execute(f"""
            SELECT DISTINCT sorts_coffee.name, ground_beans, volume, price, degrees.degree, sorts_coffee.taste 
            FROM sorts_coffee, degrees JOIN products
            ON sorts_coffee.id_sort = products.id_sort AND
            degrees.id = products.id_degree
            WHERE id_degree = {self.comboBox.currentIndex() + 1}
            """).fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(TITLE)

        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
                self.tableWidget.resizeColumnsToContents()



def main():
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()