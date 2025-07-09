import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QToolBar, QLineEdit,
                             QAction, QWidget, QHBoxLayout, QStatusBar, QMessageBox)
from PyQt5.QtCore import (QSize, QUrl, Qt, pyqtSlot)
from PyQt5.QtGui import (QIcon, QFont, QPixmap)
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
        self.webview.load(QUrl("https://www.baidu.com"))
        self.webview.urlChanged.connect(self.updateWindowTitle)
        self.createTab(self.webview)

        self.createToolbar()

        settings = QWebEngineSettings.globalSettings()
        settings.setFontFamily(QWebEngineSettings.StandardFont, "Microsoft YaHei")

        # 设置窗口图标
        self.setWindowIcon(QIcon('logo.png'))  # 替换为你的图标文件路径

    def createToolbar(self):
        navigation_bar = QToolBar('Navigation', self)
        navigation_bar.setIconSize(QSize(16, 16))
        self.addToolBar(navigation_bar)

        yahei_font = QFont("Microsoft YaHei")
        yahei_font.setPointSize(10)

        navigation_actions = {
            'go-previous': ('返回', self.navigateBack),
            'go-next': ('前进', self.navigateForward),
            'process-stop': ('停止加载', self.stopLoading),
            'view-refresh': ('刷新', self.reloadPage),
            'tab-new': ('新标签页', self.newTab),
            'help-about': ('关于', self.showAbout),
        }

        for icon, (tip, method) in navigation_actions.items():
            action = QAction(QIcon.fromTheme(icon), tip, self)
            action.setFont(yahei_font)
            action.triggered.connect(method)
            navigation_bar.addAction(action)

        self.urlbar = QLineEdit(self)
        self.urlbar.returnPressed.connect(self.openUrl)
        self.urlbar.setFont(yahei_font)
        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)

    # 确保每个函数定义后都有正确的缩进
    @pyqtSlot()
    def navigateBack(self):
        if self.webview.history().canGoBack():
            self.webview.back()

    @pyqtSlot()
    def navigateForward(self):
        if self.webview.history().canGoForward():
            self.webview.forward()

    @pyqtSlot()
    def stopLoading(self):
        self.webview.stop()

    @pyqtSlot()
    def reloadPage(self):
        self.webview.reload()

    @pyqtSlot()
    def newTab(self):
        new_webview = QWebEngineView(self)
        new_webview.load(QUrl("https://www.baidu.com"))
        self.createTab(new_webview)

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
