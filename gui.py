# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(810, 572)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_4.addWidget(self.checkBox)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.lineEdit_threshold_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_threshold_2.setEnabled(False)
        self.lineEdit_threshold_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_threshold_2.setReadOnly(False)
        self.lineEdit_threshold_2.setObjectName("lineEdit_threshold_2")
        self.horizontalLayout_4.addWidget(self.lineEdit_threshold_2)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.lineEdit_threshold_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_threshold_3.setEnabled(False)
        self.lineEdit_threshold_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_threshold_3.setReadOnly(False)
        self.lineEdit_threshold_3.setObjectName("lineEdit_threshold_3")
        self.horizontalLayout_4.addWidget(self.lineEdit_threshold_3)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.plotWindow = QtWidgets.QWidget(Dialog)
        self.plotWindow.setObjectName("plotWindow")
        self.plotLayout = QtWidgets.QVBoxLayout(self.plotWindow)
        self.plotLayout.setObjectName("plotLayout")
        self.verticalLayout_4.addWidget(self.plotWindow)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.plotWindow2 = QtWidgets.QWidget(Dialog)
        self.plotWindow2.setObjectName("plotWindow2")
        self.plotLayout2 = QtWidgets.QVBoxLayout(self.plotWindow2)
        self.plotLayout2.setObjectName("plotLayout2")
        self.verticalLayout_4.addWidget(self.plotWindow2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEdit_threshold = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_threshold.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_threshold.setReadOnly(False)
        self.lineEdit_threshold.setObjectName("lineEdit_threshold")
        self.horizontalLayout_2.addWidget(self.lineEdit_threshold)
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.horizontalLayout_2.setStretch(0, 2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.setStretch(3, 1)
        self.horizontalLayout_7.addLayout(self.verticalLayout_4)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout.addWidget(self.pushButton_5)
        self.horizontalLayout_7.addLayout(self.verticalLayout)
        self.horizontalLayout_7.setStretch(0, 2)
        self.horizontalLayout_7.setStretch(1, 1)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_7)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2.setStretch(0, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.checkBox.setText(_translate("Dialog", "Фильтр на чтение."))
        self.label_2.setText(_translate("Dialog", "Частота от "))
        self.lineEdit_threshold_2.setText(_translate("Dialog", "22308"))
        self.label_5.setText(_translate("Dialog", " МГц    "))
        self.label_3.setText(_translate("Dialog", "Ширина частот"))
        self.lineEdit_threshold_3.setText(_translate("Dialog", "22342"))
        self.label_6.setText(_translate("Dialog", " МГц  "))
        self.pushButton.setText(_translate("Dialog", "Выбор данных ( без шума )"))
        self.pushButton_2.setText(_translate("Dialog", "Выбор данных ( с шумом )"))
        self.pushButton_3.setText(_translate("Dialog", "Вычитание"))
        self.label.setText(_translate("Dialog", "Пороговое значение (%):"))
        self.lineEdit_threshold.setText(_translate("Dialog", "30"))
        self.pushButton_4.setText(_translate("Dialog", "Определение"))
        self.label_4.setText(_translate("Dialog", "Ширина окна просмотра \n"
" найденных частот в МГц"))
        self.lineEdit.setText(_translate("Dialog", "4"))
        self.pushButton_5.setText(_translate("Dialog", "Сохранение в файл"))
