import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import os
from pathlib import PureWindowsPath
from Ui_py2exe import Ui_MainWindow  # 确保这个路径与您的文件结构相匹配

print("欢迎使用果园的打包工具")
print("===============================================")
print("版本4.4，内核3.5")
print("===============================================")
print("首次运行请运行CMD文件安装需要的库")
print("===============================================")
print("产品已激活")
print("===============================================")
print("等待初始化")
print("===============================================")
print("程序报告 库已成功导入")
print("===============================================")

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)  # 使用Ui_MainWindow的setupUi方法初始化界面
        self.iconPath = ""

    def dabao(self):
        # 打包逻辑
        fullpath = self.lineEdit.text()
        self.iconPath = self.lineEdit_2.text()
        if not fullpath:
            QMessageBox.warning(self, "警告", "请先选择Python文件")
            return
        f = PureWindowsPath(fullpath)
        filedir = fullpath.replace(f.name, "")
        command = f"cd {filedir} && pyinstaller "
        if self.checkBox.isChecked():
            command += "-w "
        if self.iconPath:
            command += f"--icon={self.iconPath} "
        command += f"-F {fullpath}"
        result = os.system(command)
        if result == 0:
            QMessageBox.information(self, "执行结果", "恭喜！成功打包exe")
            print("===============================================")
            print("打包成功")
        else:
            QMessageBox.critical(self, "执行结果", "错误：打包失败，请检查命令行输出和文件路径")
            print("===============================================")
            print("打包失败")
        self.iconPath = ""
        fullpath = ""
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()  # 创建窗口实例
    print("窗口初始化完成")
    print("===============================================")
    print("创建窗口实例完成")
    print("===============================================")
    print("UI文件成功载入")
    print("===============================================")

    mainWindow.pushButton_2.clicked.connect(mainWindow.dabao)  # 连接按钮点击事件
    mainWindow.show()
    print("连接按钮点击事件完成，等待程序运行")
    print("===============================================")
    print("窗口已显示")
    print("===============================================")
    sys.exit(app.exec_())
