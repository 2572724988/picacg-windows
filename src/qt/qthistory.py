import weakref

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import time

from src.qt.qtlistwidget import QtBookList, QtIntLimit
from src.util import Log
from ui.history import Ui_History


class QtHistoryData(object):
    def __init__(self):
        self.bookId = ""         # bookId
        self.name = ""           # name
        self.epsId = 0           # 章节Id
        self.picIndex = 0           # 图片Index
        self.url = ""
        self.path = ""
        self.tick = 0


class QtHistory(QtWidgets.QWidget, Ui_History):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        Ui_History.__init__(self)
        self.setupUi(self)
        self.owner = weakref.ref(owner)

        self.bookList = QtBookList(self, self.__class__.__name__)
        self.bookList.InitBook(self.LoadNextPage)
        self.gridLayout_3.addWidget(self.bookList)
        self.bookList.doubleClicked.connect(self.OpenBookInfo)
        self.pageNums = 20

        self.lineEdit.setValidator(QtIntLimit(1, 1, self))

        self.history = {}
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("history.db")

        if not self.db.open():
            Log.Warn(self.db.lastError().text())

        query = QSqlQuery(self.db)
        sql = """\
            create table if not exists history(\
            bookId varchar primary key,\
            name varchar,\
            epsId int, \
            picIndex int,\
            url varchar,\
            path varchar,\
            tick int\
            )\
            """
        suc = query.exec(sql)
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)
        self.LoadHistory()

    def SwitchCurrent(self):
        self.bookList.clear()
        self.bookList.page = 1
        self.bookList.pages = len(self.bookList) / self.pageNums + 1
        self.lineEdit.setValidator(QtIntLimit(1, self.bookList.pages, self))
        self.RefreshData(self.bookList.page)

    def GetHistory(self, bookId):
        return self.history.get(bookId)

    def AddHistory(self, bookId, name, epsId, index, url, path):
        tick = int(time.time())
        info = self.history.get(bookId)
        if not info:
            info = QtHistoryData()
            self.history[bookId] = info
        info.bookId = bookId
        info.name = name
        info.epsId = epsId
        info.picIndex = index
        info.url = url
        info.path = path
        info.tick = tick

        query = QSqlQuery(self.db)


        sql = "INSERT INTO history(bookId, name, epsId, picIndex, url, path, tick) " \
              "VALUES ('{0}', '{1}', {2}, {3}, '{4}', '{5}', {6}) " \
              "ON CONFLICT(bookId) DO UPDATE SET name='{1}', epsId={2}, picIndex={3}, url = '{4}', path='{5}', tick={6}".\
            format(bookId, name, epsId, index, url, path, tick)
        suc = query.exec(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return

    def LoadHistory(self):
        query = QSqlQuery(self.db)
        query.exec(
            """
            select * from history
            """
        )
        while query.next():
            # bookId, name, epsId, index, url, path
            info = QtHistoryData()
            info.bookId = query.value(0)
            info.name = query.value(1)
            info.epsId = query.value(2)
            info.picIndex = query.value(3)
            info.url = query.value(4)
            info.path = query.value(5)
            info.tick = query.value(6)
            self.history[info.bookId] = info
        pass

    def JumpPage(self):
        page = int(self.lineEdit.text())
        if page > self.bookList.pages:
            return
        self.bookList.page = page
        self.bookList.clear()
        self.RefreshData(page)

    def OpenSearch(self, modelIndex):
        index = modelIndex.row()
        item = self.bookList.item(index)
        widget = self.bookList.itemWidget(item)
        text = widget.infoLabel.text()
        self.owner().userForm.listWidget.setCurrentRow(0)
        self.owner().searchForm.searchEdit.setText("")
        self.owner().searchForm.OpenSearchCategories(text)
        pass

    def LoadNextPage(self):
        self.bookList.page += 1
        self.RefreshData(self.bookList.page)

    def RefreshData(self, page):
        sortedList = list(self.history.values())
        sortedList.sort(key=lambda a: a.tick, reverse=True)
        self.bookList.clear()
        start = (page-1) * self.pageNums
        end = start + self.pageNums
        for info in sortedList[start:end]:
            data = "上次读到第{}章".format(str(info.epsId+1))
            self.bookList.AddBookItem(info.bookId, info.name, data, info.url, info.path)

    def OpenBookInfo(self, modelIndex):
        index = modelIndex.row()
        item = self.bookList.item(index)
        if not item:
            return
        widget = self.bookList.itemWidget(item)
        if not widget:
            return
        bookId = widget.id
        if not bookId:
            return
        self.owner().bookInfoForm.OpenBook(bookId)
