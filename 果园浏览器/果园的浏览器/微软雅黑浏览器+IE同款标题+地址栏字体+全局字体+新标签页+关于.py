import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QToolBar, QLineEdit, QAction, QWidget, QHBoxLayout, QMessageBox
from PyQt5.QtCore import QSize, QUrl, Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 设置窗口标题和大小
        self.setWindowTitle('果园浏览器3.0.5，使用谷歌内核驱动')
        self.resize(1300, 700)

        # 初始化多标签页控件
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.close_Tab)
        self.setCentralWidget(self.tabWidget)

        # 初始化第一个标签页
        self.webview = QWebEngineView(self)
        self.webview.load(QUrl("http://www.baidu.com"))
        self.webview.titleChanged.connect(self.update_window_title)
        self.create_tab(self.webview)

        # 创建导航栏
        navigation_bar = QToolBar('Navigation')
        navigation_bar.setIconSize(QSize(16, 16))
        self.addToolBar(navigation_bar)

        # 创建导航栏按钮并连接信号
        icons = ('go-previous', 'go-next', 'process-stop', 'view-refresh', 'tab-new', 'help-about')
        tips = ('返回', '前进', '停止加载', '刷新', '新标签页', '关于')
        actions = zip(icons, tips)
        
        for icon, tip in actions:
            action = QAction(QIcon.fromTheme(icon), tip, self)
            if icon == 'go-previous':
                action.triggered.connect(self.webview.back)
            elif icon == 'go-next':
                action.triggered.connect(self.webview.forward)
            elif icon == 'process-stop':
                action.triggered.connect(self.webview.stop)
            elif icon == 'view-refresh':
                action.triggered.connect(self.webview.reload)
            elif icon == 'tab-new':
                action.triggered.connect(self.add_new_tab)
            elif icon == 'help-about':
                action.triggered.connect(self.show_about)
            navigation_bar.addAction(action)

        # 创建地址栏并设置字体
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        self.urlbar.setFont(QFont("Microsoft YaHei"))
        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)

        # 设置Web引擎字体
        settings = QWebEngineSettings.globalSettings()
        settings.setFontFamily(QWebEngineSettings.StandardFont, "Microsoft YaHei")

    # 导航到地址栏输入的URL
    def navigate_to_url(self):
        url = QUrl(self.urlbar.text())
        if url.scheme() == '':
            url.setScheme('http')
        self.webview.setUrl(url)

    # 更新地址栏和窗口标题
    def update_urlbar(self, url):
        self.urlbar.setText(url.toString())

    def update_window_title(self, title):
        self.setWindowTitle(f'果园浏览器3.0.5 - {title}')

    # 创建新标签页
    def create_tab(self, webview):
        self.tab = QWidget()
        self.tabWidget.addTab(self.tab, "新标签页")
        self.tabWidget.setCurrentWidget(self.tab)
        layout = QHBoxLayout(self.tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(webview)

    # 新建标签页的槽函数
    def add_new_tab(self):
        new_webview = QWebEngineView(self)
        new_webview.load(QUrl("about:blank"))
        self.create_tab(new_webview)

    # 关闭标签页的槽函数
    def close_Tab(self, index):
        if self.tabWidget.count() > 1:
            self.tabWidget.removeTab(index)
        else:
            self.close()

    # 弹出关于窗口
    def show_about(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('关于果园浏览器')
        msg.setTextFormat(Qt.RichText)
        about_text = "果园编程工作室制作，©2023-2026版权所有<br><a href='https://gy216.github.io/'>官网：https://gy216.github.io/</a>"
        msg.setText(about_text)
        font = QFont("Microsoft YaHei")
        msg.setFont(font)
        msg.exec_()

class WebEngineView(QWebEngineView):
    def __init__(self, mainwindow, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.mainwindow = mainwindow

    def createWindow(self, type):
        new_webview = WebEngineView(self.mainwindow)
        self.mainwindow.add_new_tab()
        return new_webview

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = MainWindow()
    browser.show()
    sys.exit(app.exec_())
