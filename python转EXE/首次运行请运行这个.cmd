@echo off
echo ��������PIP
python -m pip install --upgrade pip

echo PIP������
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
echo �廪����������
echo ���ڰ�װpyqt5
pip install PyQt5                   

pip install PyQt5-tools

pip install PyQt5Designer 
 
pip install PyQtWebEngine
 
pip install PySimpleGUI
 
pip install PyQt5-sip
 
pip install PyQt5-stubs

echo pyqt5��װ�ɹ�
echo =================================
echo ���ڰ�װpyinstaller
pip install pyinstaller


echo���ж����Ѱ�װ��ɣ����ڣ�����Թرմ��ڣ����ļ���
