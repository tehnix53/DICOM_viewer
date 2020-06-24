import sys
import os
import numpy as np
import qimage2ndarray
import pydicom as pyd

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap
import design

from plot_objects import MplCanvas

# type QPIXMAP concert from matplotlib axes!!!
# image=qimage2ndarray.array2qimage(b)
# add two layers for image and series


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.browse_folder)
        self.pushButton.clicked.connect(self.load_image)
        # self.label.setPixmap(QtGui.QPixmap.fromImage(sc))
        # self.label.setPixmap(sc)
        # первые цифры - положение на экране, третья и четвертая - размер окна
        # self.setGeometry(500, 250, 300, 300)

    def browse_folder(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите папку", None, "Image (*.bin *.dcm)")[0]
        self.lineEdit.setText(file_name)
        # self.setGeometry(200, 200, 300, 300)

    # QtGui.QPixmap.fromImage(self._image)

    def load_image(self):
        file_name = self.lineEdit.text()
        sc = MplCanvas(width=5, height=4, dpi=100)
        lung = pyd.dcmread(file_name).pixel_array
        sc.axes.imshow(lung)
        self.setCentralWidget(sc)
        # pixmap = self.lineEdit.text()
        # self.label.setPixmap(QtGui.QPixmap.fromImage(image))
        # self.setupUi(self)
        # self.label.resize(pixmap.width(200), pixmap.height(200))
        # self.resize(pixmap.width(), pixmap.height())


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
