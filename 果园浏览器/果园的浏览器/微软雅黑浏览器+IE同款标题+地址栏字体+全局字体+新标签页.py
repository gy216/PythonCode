import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QToolBar, QLineEdit, QAction, QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 设置窗口标题和大小
        self.setWindowTitle('果园浏览器3.0.5，使用谷歌内核驱动')
        self.resize(1300, 700)
        self.show()

        # 初始化 QTabWidget 用于多标签页管理
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabShape(QTabWidget.Triangular)  # 设置标签形状
        self.tabWidget.setDocumentMode(True)  # 设置为文档模式
        self.tabWidget.setMovable(True)  # 允许拖动标签排序
        self.tabWidget.setTabsClosable(True)  # 允许关闭标签
        self.tabWidget.tabCloseRequested.connect(self.close_Tab)  # 连接关闭标签的信号

        # 将 tabWidget 设置为主窗口的中心部件
        self.setCentralWidget(self.tabWidget)

        # 初始化第一个标签页并加载起始网页
        self.webview = QWebEngineView(self)
        self.webview.load(QUrl("http://www.baidu.com"))
        self.webview.titleChanged.connect(self.update_window_title)  # 连接网页标题改变的信号
        self.create_tab(self.webview)

        # 创建导航栏
        navigation_bar = QToolBar('Navigation')
        navigation_bar.setIconSize(QSize(16, 16))  # 设置图标大小
        self.addToolBar(navigation_bar)  # 将导航栏添加到主窗口

        # 创建导航栏按钮并设置对应的槽函数
        back_button = QAction(QIcon.fromTheme('go-previous'), '返回', self)
        next_button = QAction(QIcon.fromTheme('go-next'), '前进', self)
        stop_button = QAction(QIcon.fromTheme('process-stop'), '停止加载', self)
        reload_button = QAction(QIcon.fromTheme('view-refresh'), '刷新', self)

        back_button.triggered.connect(self.webview.back)
        next_button.triggered.connect(self.webview.forward)
        stop_button.triggered.connect(self.webview.stop)
        reload_button.triggered.connect(self.webview.reload)

        # 将按钮添加到导航栏
        navigation_bar.addAction(back_button)
        navigation_bar.addAction(next_button)
        navigation_bar.addAction(stop_button)
        navigation_bar.addAction(reload_button)

        # 创建并设置地址栏
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)  # 按下回车时加载地址栏中的URL
        self.urlbar.setFont(QFont("Microsoft YaHei"))  # 设置地址栏字体为微软雅黑
        navigation_bar.addSeparator()  # 添加分隔符
        navigation_bar.addWidget(self.urlbar)  # 将地址栏添加到导航栏

        # 创建并设置新建标签页按钮
        new_tab_button = QAction(QIcon.fromTheme('tab-new'), '新标签页', self)
        new_tab_button.triggered.connect(self.add_new_tab)  # 连接新建标签页的槽函数
        navigation_bar.addAction(new_tab_button)

        # 设置全局Web引擎字体为微软雅黑
        settings = QWebEngineSettings.globalSettings()
        settings.setFontFamily(QWebEngineSettings.StandardFont, "Microsoft YaHei")

    # 导航到地址栏中输入的URL
    def navigate_to_url(self):
        url = QUrl(self.urlbar.text())
        if url.scheme() == '':
            url.setScheme('http')  # 如果没有协议头，则默认为http
        self.webview.setUrl(url)  # 在当前激活的webview中加载URL

    # 更新地址栏中的URL
    def update_urlbar(self, url):
        self.urlbar.setText(url.toString())

    # 更新窗口标题为当前网页标题或默认标题
    def update_window_title(self, title):
        if title:
            self.setWindowTitle(f'果园浏览器3.0.5 - {title}')
        else:
            self.setWindowTitle('果园浏览器3.0.5')

    # 创建一个新的标签页并将webview添加到其中
    def create_tab(self, webview):
        self.tab = QWidget()
        self.tabWidget.addTab(self.tab, "新标签页")  # 添加标签页并设置默认标题
        self.tabWidget.setCurrentWidget(self.tab)
        layout = QHBoxLayout(self.tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(webview)  # 将webview添加到标签布局中

    # 新建一个标签页并加载about:blank
    def add_new_tab(self):
        new_webview = QWebEngineView(self)
        new_webview.load(QUrl("about:blank"))  # 默认加载about:blank
        self.create_tab(new_webview)  # 创建新标签并将webview添加进去

    # 关闭标签页的槽函数
    def close_Tab(self, index):
        if self.tabWidget.count() > 1:
            self.tabWidget.removeTab(index)  # 如果多于一个标签，则关闭指定的标签
        else:
            self.close()  # 如果只有一个标签，则关闭窗口

class WebEngineView(QWebEngineView):
    def __init__(self, mainwindow, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.mainwindow = mainwindow

    # 重写createWindow方法以支持在新标签页中打开链接
    def createWindow(self, type):
        new_webview = WebEngineView(self.mainwindow)
        self.mainwindow.add_new_tab()  # 在新标签页中打开
        return new_webview

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = MainWindow()
    browser.show()
    sys.exit(app.exec_())
