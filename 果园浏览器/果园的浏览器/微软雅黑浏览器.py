import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QToolBar, QLineEdit, QAction, QWidget, QHBoxLayout
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('果园浏览器3.0.5测试版 谷歌内核')
        self.resize(1300, 700)
        self.show()

        self.tabWidget = QTabWidget()
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.close_Tab)
        self.setCentralWidget(self.tabWidget)

        self.webview = QWebEngineView(self)
        self.webview.load(QUrl("http://www.baidu.com"))
        self.create_tab(self.webview)

        navigation_bar = QToolBar('Navigation')
        navigation_bar.setIconSize(QSize(16, 16))
        self.addToolBar(navigation_bar)

        back_button = QAction(QIcon('icons/houtui.png'), 'Back', self)
        next_button = QAction(QIcon('icons/qianjin.png'), 'Forward', self)
        stop_button = QAction(QIcon('icons/close.png'), 'Stop', self)
        reload_button = QAction(QIcon('icons/shuaxin.png'), 'Reload', self)

        back_button.triggered.connect(self.webview.back)
        next_button.triggered.connect(self.webview.forward)
        stop_button.triggered.connect(self.webview.stop)
        reload_button.triggered.connect(self.webview.reload)

        navigation_bar.addAction(back_button)
        navigation_bar.addAction(next_button)
        navigation_bar.addAction(stop_button)
        navigation_bar.addAction(reload_button)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)

        self.webview.urlChanged.connect(self.renew_urlbar)

        # 设置微软雅黑字体
        settings = QWebEngineSettings.globalSettings()
        settings.setFontFamily(QWebEngineSettings.StandardFont, "Microsoft YaHei")
        settings.setFontFamily(QWebEngineSettings.FixedFont, "Microsoft YaHei")
        settings.setFontFamily(QWebEngineSettings.SerifFont, "Microsoft YaHei")
        settings.setFontFamily(QWebEngineSettings.SansSerifFont, "Microsoft YaHei")
        settings.setFontFamily(QWebEngineSettings.CursiveFont, "Microsoft YaHei")
        settings.setFontFamily(QWebEngineSettings.FantasyFont, "Microsoft YaHei")

    def navigate_to_url(self):
        url = QUrl(self.urlbar.text())
        if url.scheme() == '':
            url.setScheme('http')
        self.webview.setUrl(url)

    def renew_urlbar(self, url):
        self.urlbar.setText(url.toString())
        self.urlbar.setCursorPosition(0)

    def create_tab(self, webview):
        self.tab = QWidget()
        self.tabWidget.addTab(self.tab, "新建页面")
        self.tabWidget.setCurrentWidget(self.tab)
        layout = QHBoxLayout(self.tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(webview)

    def close_Tab(self, index):
        if self.tabWidget.count() > 1:
            self.tabWidget.removeTab(index)
        else:
            self.close()

class WebEngineView(QWebEngineView):
    def __init__(self, mainwindow, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.mainwindow = mainwindow

    def createWindow(self, type):
        new_webview = WebEngineView(self.mainwindow)
        self.mainwindow.create_tab(new_webview)
        return new_webview

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = MainWindow()
    browser.show()
    sys.exit(app.exec_())
