# endcoding: utf-8

'''
Created by
@author: Dianyi Hu
@date: 2023/12/21 
@time: 02:11
'''


import data
from os import path, getcwd, makedirs
from pandas import concat
from time import strftime
from matplotlib import use
from ctypes import windll
from sys import exit
from glob import glob

from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
from main_ui import Ui_MainWindow
from plot_fun import analysis_fig_1, analysis_fig_2, analysis_fig_3, analysis_fig_4, analysis_fig_5, analysis_fig_6


myappid = 'mySimpleApp'
ui_file = 'layout.ui'
use('Qt5Agg')

windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class Main(QMainWindow):
    def __init__(self, ui_file):
        super(Main, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(ui_file, self)
        self.file_list = []


    def openfolder(self):
        self.statusbar.clearMessage()
        self.Cate_ID.clear()
        self.X_select.clear()
        self.Y_select.clear()

        try:
            self.folder = QFileDialog.getExistingDirectory(self, "Open folder", './')
            self.Folder_show.setText(self.folder)
            f_list = glob(self.folder+'/*.xlsx')+glob(self.folder+'/*.xls')+glob(self.folder+'/*.xls')
            self.file_list = [i for i in f_list if not i.split('\\')[-1].startswith('~')]
            Files_show_list = [j.split('\\')[-1] for j in self.file_list]
            self.Files_show.addItems(Files_show_list)
            data.init(self.file_list)
            self.Cate_ID.addItems(data.cat_cols)
            self.X_select.addItems(data.cols)
            self.Y_select.addItems(data.cols)
        except:
            self.statusbar.showMessage('ERROR!')


    def addfile(self):
        self.statusbar.clearMessage()
        self.Cate_ID.clear()
        self.X_select.clear()
        self.Y_select.clear()

        try:
            fname, f_type = QFileDialog.getOpenFileName(self, 'Open file', '', '')
            if fname.endswith('.xlsx') or fname.endswith('.xls') or fname.endswith('.csv') or fname.endswith('.XLSX'):
                self.file_list.append(fname)
                self.Files_show.addItems(fname.split('./')[-1])
                data.add_file(fname)
                self.Cate_ID.addItems(data.cat_cols)
                self.X_select.addItems(data.cols)
                self.Y_select.addItems(data.cols)
        except:
            self.statusbar.showMessage('ERROR!')

    def rmvfile(self):
        self.statusbar.clearMessage()
        item_index = self.Files_show.currentRow()
        if item_index != -1:
            self.Cate_ID.clear()
            self.X_select.clear()
            self.Y_select.clear()

            try:
                self.file_list.pop(item_index)
                self.Files_show.takeItem(item_index)
                data.rmv_file(item_index)
                self.Cate_ID.addItems(data.cat_cols)
                self.X_select.addItems(data.cols)
                self.Y_select.addItems(data.cols)
            except:
                self.statusbar.showMessage('ERROR!')


    def drawfig(self):
        self.statusbar.clearMessage()
        self.figure.clear()
        try:
            df = concat(data.df_list, ignore_index=True)
            match self.Plot_fun_currentIndex():
                case 0:
                    if self.X_select.currentText() == self.Cate_ID.currentText():
                        analysis_fig_1(self.figure, df, self.X_select.currentText(), self.Y_select.currentText())
                    else:
                        analysis_fig_1(self.figure, df, self.X_select.currentText(), self.Y_select.currentText(), self.Cate_ID.currentText())
                    self.figure.suptitle(f'{self.X_select.currentText()} vs. {self.Y_select.currentText()} violinplot', fontsize=16)
                case 1:
                    analysis_fig_2(self.figure, df, self.X_select.currentText(), self.Y_select.currentText(), self.Cate_ID.currentText())
                    self.figure.suptitle(f'{self.X_select.currentText()} vs. {self.Y_select.currentText()} boxplot', fontsize=16)
                case 2:
                    analysis_fig_3(self.figure, df, self.X_select.currentText(), self.Y_select.currentText(), self.Cate_ID.currentText())
                    self.figure.suptitle(f'{self.X_select.currentText()} vs. {self.Y_select.currentText()} heatmap', fontsize=16)
                case 3:
                    analysis_fig_4(self.figure, df, self.X_select.currentText(), self.Y_select.currentText(), self.Cate_ID.currentText())
                    self.figure.suptitle(f'{self.X_select.currentText()} vs. {self.Y_select.currentText()} runpath plot', fontsize=16)
                case 4:
                    analysis_fig_5(self.figure, df, self.X_select.currentText(), self.Y_select.currentText(), self.Cate_ID.currentText())
                    self.figure.suptitle(f'{self.X_select.currentText()} vs. {self.Y_select.currentText()} kde plot', fontsize=16)
                case 5:
                    analysis_fig_6(self.figure, df, self.X_select.currentText(), self.Y_select.currentText(), self.Cate_ID.currentText())
                    self.figure.suptitle(f'{self.X_select.currentText()} vs. {self.Y_select.currentText()} barplot', fontsize=16)

            self.canvas.draw()

        except:
            self.statusbar.clearMessage('ERROR!')


    def savefig(self):
        self.statusbar.clearMessage()
        try:
            folder = path.join(getcwd(), 'output')
            if not path.exists(folder):
                makedirs(folder)
            name = path.join(folder, strftime('%Y%m%d_%H %M %S')+'.png')
            self.figure.savefig(name, dpi=300)
            print('Figure saved!')
            self.statusbar.showMessage('Figure saved.')
            print(folder)
        except:
            self.statusbar.showMessage('ERROR!')


    def xy_show(self):
        self.X_label_setVisible(True)
        self.X_select.setVisible(True)
        self.Y_label_setVisible(True)
        self.Y_select.setVisible(True)


    def xy_hide(self):
        self.X_label_setVisible(False)
        self.X_select.setVisible(False)
        self.Y_label_setVisible(False)
        self.Y_select.setVisible(False)


    def plotfun_changed(self):
        if self.Plot_fun.currentIndex()==3:
            self.xy_hide()
        elif self.Plor_fun.currentIndex()==4:
            self.Y_label.setVisible(False)
            self.Y_select.SetVisible(False)
        else:
            self.xy_show()


if __name__ == '__main__':
    app = QApplication([])
    widget = Main(ui_file)
    exit(app.exec_())

