import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QTableView, QHeaderView, QVBoxLayout
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
import json
from os import path
basedir = path.dirname(__file__)

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

assetNames = []
assetIds = []
assets = []
for i in json.load(open(path.join(basedir, 'actualids.json'))):
    assetName = i["assetName"]
    assetId = i["assetId"]
    assetNames.append(i["assetName"])
    assetIds.append(i["assetId"])
    assets.append(f"{assetName}, {assetId}")
    print(i["assetName"])
    print(i["assetId"])
class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(700, 500)
        mainLayout = QVBoxLayout()

        model = QStandardItemModel(len(assets), 1)
        model.setHorizontalHeaderLabels(['Soundate IDs'])

        for row, company in enumerate(assets):
            item = QStandardItem(company)
            model.setItem(row, 0, item)

        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(0)

        search_field = QLineEdit()          
        search_field.setStyleSheet('font-size: 20px; height: 60px;')
        search_field.textChanged.connect(filter_proxy_model.setFilterRegExp)
        mainLayout.addWidget(search_field)

        table = QTableView()
        table.setStyleSheet('font-size: 15px;')
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setModel(filter_proxy_model)
        mainLayout.addWidget(table)

        self.setLayout(mainLayout)

app = QApplication(sys.argv)
app.setApplicationName("Soundate Search")
app.setWindowIcon(QIcon(path.join(basedir, 'main.ico')))
demo = AppDemo()
demo.show()
sys.exit(app.exec_())