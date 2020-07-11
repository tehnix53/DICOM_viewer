import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap

import design

from pil_object import dicom_to_qt, get_label
from utility import shift_data


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.width_of = 450
        self.factor_contrast = 1
        self.factor_bright = 1
        self.autocontrast_mode = 0
        self.inversion_mode = 0
        self.pushButton_2.clicked.connect(self.open_dir)
        self.pushButton_7.clicked.connect(self.zoom_out)
        self.pushButton_8.clicked.connect(self.zoom_in)
        self.pushButton_4.clicked.connect(self.contrast_up)
        self.pushButton_5.clicked.connect(self.contrast_down)
        self.pushButton.clicked.connect(self.bright_up)
        self.pushButton_3.clicked.connect(self.bright_down)
        self.pushButton_6.clicked.connect(self.reset)

    def open_dir(self):
        self.lineEdit_7.clear()
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите папку", None, "Image (*.bin *.dcm)")[0]
        self.lineEdit_7.setText(file_name)
        if len(self.lineEdit_7.text()) > 2:
            self.load_image()
            self.set_labels()

    def load_image(self):
        file_name = self.lineEdit_7.text()
        if self.checkBox_2.isChecked():
            self.autocontrast_mode = 1
        else:
            self.autocontrast_mode = 0
        self.lineEdit.setText(str(self.autocontrast_mode))
        if self.checkBox.isChecked():
            self.inversion_mode = 1
        else:
            self.inversion_mode = 0
        qim = dicom_to_qt(file_name, self.factor_contrast,
                          self.factor_bright, self.autocontrast_mode, self.inversion_mode)
        pix = QPixmap.fromImage(qim)
        pixmap_resized = pix.scaled(self.width_of, 10000, QtCore.Qt.KeepAspectRatio)
        self.label_11.setPixmap(pixmap_resized)

    def set_labels(self):
        file_name = self.lineEdit_7.text()
        labels = get_label(file_name)
        self.lineEdit_3.setText(str(labels.PatientName))
        self.lineEdit_2.setText(str(labels.PatientID))
        self.lineEdit_5.setText(str(labels.PatientBirthDate[0:4]))
        self.lineEdit_4.setText(shift_data(str(labels.StudyDate)))
        self.lineEdit_6.setText(str(labels.Modality))
        self.lineEdit_9.setText(str(self.width_of))
        self.lineEdit_8.setText(str(self.factor_contrast))
        self.lineEdit_10.setText(str(self.factor_bright))
        self.lineEdit.setText(str(self.autocontrast_mode))

    def reset(self):
        self.factor_bright = 1
        self.lineEdit_10.setText(str(self.factor_bright))
        self.factor_contrast = 1
        self.lineEdit_8.setText(str(self.factor_contrast))
        self.load_image()
        self.autocontrast_mode = 0
        self.lineEdit.setText(str(self.autocontrast_mode))
        self.inversion_mode = 0

    def bright_up(self):
        self.factor_bright += 0.1
        self.lineEdit_10.setText(str(self.factor_bright))
        self.load_image()

    def bright_down(self):
        self.factor_bright -= 0.1
        self.lineEdit_10.setText(str(self.factor_bright))
        self.load_image()

    def contrast_up(self):
        self.factor_contrast += 0.1
        self.lineEdit_8.setText(str(self.factor_contrast))
        self.load_image()

    def contrast_down(self):
        self.factor_contrast -= 0.1
        self.lineEdit_8.setText(str(self.factor_contrast))
        self.load_image()

    def zoom_out(self):
        self.width_of -= 5
        self.lineEdit_9.setText(str(self.width_of))
        self.load_image()

    def zoom_in(self):
        self.width_of += 5
        self.lineEdit_9.setText(str(self.width_of))
        self.load_image()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
