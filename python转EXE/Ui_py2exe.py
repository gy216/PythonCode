from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QFileDialog

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(650, 350)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.label = QtWidgets.QLabel("Py文件完整路径（不支持中文）：")
        self.layout.addWidget(self.label)

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.layout.addWidget(self.lineEdit)

        # 浏览按钮
        self.browseButton = QtWidgets.QPushButton("浏览以选择Python文件")
        self.browseButton.clicked.connect(self.openFileDialog)  # 连接信号和槽
        self.layout.addWidget(self.browseButton)

        self.checkBox = QtWidgets.QCheckBox("要隐藏CMD窗口，如果有print请慎重选择")
        self.layout.addWidget(self.checkBox)

        self.label_2 = QtWidgets.QLabel("图标路径：")
        self.layout.addWidget(self.label_2)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.layout.addWidget(self.lineEdit_2)
        
        self.iconBrowseButton = QtWidgets.QPushButton("浏览以选择图标文件")
        self.iconBrowseButton.clicked.connect(self.openIconFileDialog)  # 连接信号和槽
        self.layout.addWidget(self.iconBrowseButton)

        self.pushButton_2 = QtWidgets.QPushButton("打包！")
        self.layout.addWidget(self.pushButton_2)  # 添加按钮到布局

        self.label_3 = QtWidgets.QLabel("exe保存路径为源文件所在文件夹的dist目录里")
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.layout.addWidget(self.label_3)

        self.label_admin = QtWidgets.QLabel("请使用管理员运行这个程序")
        self.label_admin.setStyleSheet("color: red; font-weight: bold;")
        self.layout.addWidget(self.label_admin)

        self.label_custom1 = QtWidgets.QLabel("（运行之前请运行CMD文件）")
        self.layout.addWidget(self.label_custom1)

        self.label_custom2 = QtWidgets.QLabel("（最好新建一个文件夹，把PY文件放进去，用原地址可能很乱（记得，文件夹不是中文））")
        self.layout.addWidget(self.label_custom2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.apply_style()
        # 去掉了按钮动画的设置，以避免布局错位的问题
        # self.setup_button_animation(self.pushButton_2)
        self.iconPath = ""

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "果园编程专用PY打包程序3.0.3"))
        self.label.setText(_translate("MainWindow", "Py文件完整路径（不支持中文）："))
        self.checkBox.setText(_translate("MainWindow", "要隐藏CMD窗口，如果有print请慎重选择"))
        self.pushButton_2.setText(_translate("MainWindow", "打包！"))
        self.label_2.setText(_translate("MainWindow", "图标路径："))
        self.label_3.setText(_translate("MainWindow", "exe保存路径为源文件所在文件夹的dist目录里"))

    def apply_style(self):
        style = """
        QWidget {
            background-color: #f4f4f4;
        }
        QLabel {
            color: #333;
            font: 10pt;
        }
        QLineEdit {
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 2px;
            font: 10pt;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QCheckBox {
            color: #333;
            font: 10pt;
        }
        """
        self.centralwidget.setStyleSheet(style)

    def setup_button_animation(self, button):
        animation = QPropertyAnimation(button, b"size")
        animation.setDuration(300)
        start_width = button.width()
        start_height = button.height()
        end_width = int(start_width * 1.1)
        end_height = int(start_height * 1.1)
        animation.setStartValue(QtCore.QSize(start_width, start_height))
        animation.setEndValue(QtCore.QSize(end_width, end_height))
        animation.setDirection(QPropertyAnimation.Forward)
        self.animation = animation  # 保存引用以避免垃圾回收
        button.clicked.connect(lambda: animation.start())

    def openFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "选择Py文件（请确保路径里没有除了英文外的所有语言）", "",
                                                  "你的PYTHON文件 (*.py)", options=options)
        if fileName:
            self.lineEdit.setText(fileName)

    def openIconFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "选择图标文件（请确保路径里没有除了英文外的所有语言）", "",
                                                  "图片文件必须是ico格式 (*.ico)", options=options)
        if fileName:
            self.lineEdit_2.setText(fileName)
            self.updateIconPath()

    def updateIconPath(self):
        # 检查用户是否选择了图标文件
        if self.lineEdit_2.text():
            # 如果选择了图标文件，将图标路径设置为所选文件
            self.iconPath = self.lineEdit_2.text()
        else:
            # 如果没有选择图标文件，将图标路径设置为空字符串
            self.iconPath = ""

# 测试代码
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    # 连接打包按钮的点击信号到一个示例槽函数，您需要替换为您自己的打包逻辑
    MainWindow.pushButton_2.clicked.connect(ui.dabao)  
    MainWindow.show()
    sys.exit(app.exec_())
