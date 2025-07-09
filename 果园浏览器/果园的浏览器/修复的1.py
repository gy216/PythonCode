import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QToolBar, QLineEdit,
                             QAction, QWidget, QHBoxLayout, QStatusBar)
from PyQt5.QtCore import (QSize, QUrl, Qt, pyqtSlot)
from PyQt5.QtGui import (QIcon, QFont)
from PyQt5.QtWebEngineWidgets import (QWebEngineView, QWebEngineSettings)
import tkinter as tk
from tkinter import messagebox

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('果园浏览器3.0.5，使用谷歌内核驱动')
        self.resize(1300, 700)

        self.tabWidget = QTabWidget()
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.setCentralWidget(self.tabWidget)

        self.webview = QWebEngineView(self)
        self.webview.load(QUrl("http://www.baidu.com"))
        self.webview.urlChanged.connect(self.updateWindowTitle)
        self.createTab(self.webview)

        self.createToolbar()

        settings = QWebEngineSettings.globalSettings()
        settings.setFontFamily(QWebEngineSettings.StandardFont, "Microsoft YaHei")

    def createToolbar(self):
        navigation_bar = QToolBar('Navigation', self)
        navigation_bar.setIconSize(QSize(16, 16))
        self.addToolBar(navigation_bar)

        yahei_font = QFont("Microsoft YaHei")
        yahei_font.setPointSize(10)

        icons_and_methods = {
            'go-previous': (self.navigateBack, '返回'),
            'go-next': (self.navigateForward, '前进'),
            'process-stop': (self.stopLoading, '停止加载'),
            'view-refresh': (self.reloadPage, '刷新'),
            'tab-new': (self.newTab, '新标签页'),
            'help-about': (self.showAbout, '关于')
        }

        for icon, (method, tip) in icons_and_methods.items():
            action = QAction(QIcon.fromTheme(icon), tip, self)
            action.setFont(yahei_font)
            action.triggered.connect(method)
            navigation_bar.addAction(action)

        self.urlbar = QLineEdit(self)
        self.urlbar.returnPressed.connect(self.openUrl)
        self.urlbar.setFont(yahei_font)
        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)

    @pyqtSlot()
    def navigateBack(self):
        self.webview.back()

    @pyqtSlot()
    def navigateForward(self):
        self.webview.forward()

    @pyqtSlot()
    def stopLoading(self):
        self.webview.stop()

    @pyqtSlot()
    def reloadPage(self):
        self.webview.reload()

    @pyqtSlot()
    def newTab(self):
        self.addNewTab()

    @pyqtSlot(QUrl)
    def updateWindowTitle(self, url):
        self.setWindowTitle(f'果园浏览器3.0.5 - {url.toString()}')

    @pyqtSlot()
    def openUrl(self):
        url_text = self.urlbar.text()
        if not url_text:
            return
        url = QUrl(url_text)
        if url.scheme() == '':
            url.setScheme('https')
        self.webview.setUrl(url)

    def createTab(self, webview):
        self.tab = QWidget()
        layout = QHBoxLayout(self.tab)
        layout.setContentsMargins(0, 0, 0, 0)
        self.tab.setLayout(layout)
        self.tabWidget.addTab(self.tab, "新标签页")
        self.tabWidget.setCurrentWidget(self.tab)
        layout.addWidget(webview)

    def addNewTab(self):
        new_webview = QWebEngineView(self)
        new_webview.load(QUrl("https://www.baidu.com"))
        self.createTab(new_webview)

    def closeTab(self, index):
        if self.tabWidget.count() > 1:
            self.tabWidget.removeTab(index)
        else:
            self.close()

    def showAbout(self):
        # 使用 tkinter 创建一个关于对话框
        root = tk.Tk()
        root.withdraw()  # 隐藏初始的 Tk 主窗口
        messagebox.showinfo('关于果园浏览器', "果园编程工作室制作，©2023-2026版权所有\n官网：https://gy216.github.io/")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = MainWindow()
    browser.show()
    sys.exit(app.exec_())
