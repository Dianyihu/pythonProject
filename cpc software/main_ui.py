# endcoding: utf-8

'''
Created by
@author: Dianyi Hu
@date: 2023/12/21 
@time: 02:57
'''


from PyQt5.QtWidgets import (QPushButton, QListWidget, QStatusBar, QComboBox, QHBoxLayout, QTextBrowser, QLineEdit)
from PyQt5 import uic
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasAgg as FigureCanvas


class Ui_MainWindow(object):
    def setupUi(self, ui_file, MainWindow):
        MainWindow.window = uic.loadUi(ui_file)
        MainWindow.statusbar = MainWindow.window.findChild(QStatusBar, 'statusbar')

        MainWindow.figure = plt.figure()
        MainWindow.canvas = FigureCanvas(MainWindow.figure)
        MainWindow.ax = MainWindow.fig.add_axes([0.11,0.13,0.6,0.8])

        MainWindow.DataLayout = MainWindow.window.findChild(QHBoxLayout, 'plot_show')
        MainWindow.DataLayout.insertWidget(0, MainWindow.canvas)

        MainWindow.Open_button = MainWindow.window.findChild(QPushButton, 'open')
        MainWindow.Open_button.clicked.connect(MainWindow.openfolder)

        MainWindow.Plt_button = MainWindow.window.findChild(QPushButton, 'plot')
        MainWindow.Plt_button.clicked.connect(MainWindow.drawfig)

        MainWindow.Rmv_button = MainWindow.window.findChild(QPushButton, 'remove')
        MainWindow.Rmv_button.clicked.connect(MainWindow.removefile)

        MainWindow.Add_button = MainWindow.window.findChild(QPushButton, 'add')
        MainWindow.Add_button.clicked.connect(MainWindow.addfile)

        MainWindow.Cate_ID = MainWindow.window.findChild(QComboBox, 'Cate_list')
        MainWindow.X_select = MainWindow.window.findChild(QComboBox, 'X_list')
        MainWindow.Y_select = MainWindow.window.findChild(QComboBox, 'Y_list')
        MainWindow.X_label = MainWindow.window.findChild(QComboBox, 'X')
        MainWindow.Y_label = MainWindow.window.findChild(QComboBox, 'Y')

        MainWindow.Folder_show = MainWindow.window.findChild(QTextBrowser, 'f_name')
        MainWindow.Files_show = MainWindow.window.findChild(QListWidget, 'file_list')

        MainWindow.Plot_fun = MainWindow.window.findChild(QComboBox, 'plot_fun')
        MainWindow.Plot_fun.addItems(['Violinplot','Boxplot','Heatmap','Runpath plot','KDE','Barplot'])
        MainWindow.Plot_fun.currentTextchanged.connect(MainWindow.plotfun_changed)

        MainWindow.window.show()
