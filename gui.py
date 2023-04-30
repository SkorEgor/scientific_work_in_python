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
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(810, 572)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon_main/app_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setToolTip("")
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
        self.checkBox_read_filter = QtWidgets.QCheckBox(Dialog)
        self.checkBox_read_filter.setObjectName("checkBox_read_filter")
        self.horizontalLayout_4.addWidget(self.checkBox_read_filter)
        self.label_text_frequency_from = QtWidgets.QLabel(Dialog)
        self.label_text_frequency_from.setObjectName("label_text_frequency_from")
        self.horizontalLayout_4.addWidget(self.label_text_frequency_from)
        self.lineEdit_filter_frequency_start = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_filter_frequency_start.setEnabled(False)
        self.lineEdit_filter_frequency_start.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_filter_frequency_start.setReadOnly(False)
        self.lineEdit_filter_frequency_start.setObjectName("lineEdit_filter_frequency_start")
        self.horizontalLayout_4.addWidget(self.lineEdit_filter_frequency_start)
        self.label_text_MHz_from = QtWidgets.QLabel(Dialog)
        self.label_text_MHz_from.setObjectName("label_text_MHz_from")
        self.horizontalLayout_4.addWidget(self.label_text_MHz_from)
        self.label_text_frequency_to = QtWidgets.QLabel(Dialog)
        self.label_text_frequency_to.setObjectName("label_text_frequency_to")
        self.horizontalLayout_4.addWidget(self.label_text_frequency_to)
        self.lineEdit_filter_frequency_end = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_filter_frequency_end.setEnabled(False)
        self.lineEdit_filter_frequency_end.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_filter_frequency_end.setReadOnly(False)
        self.lineEdit_filter_frequency_end.setObjectName("lineEdit_filter_frequency_end")
        self.horizontalLayout_4.addWidget(self.lineEdit_filter_frequency_end)
        self.label_text_MHz_to = QtWidgets.QLabel(Dialog)
        self.label_text_MHz_to.setObjectName("label_text_MHz_to")
        self.horizontalLayout_4.addWidget(self.label_text_MHz_to)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.plotWindow_empty_and_signal = QtWidgets.QWidget(Dialog)
        self.plotWindow_empty_and_signal.setObjectName("plotWindow_empty_and_signal")
        self.plotLayout = QtWidgets.QVBoxLayout(self.plotWindow_empty_and_signal)
        self.plotLayout.setObjectName("plotLayout")
        self.verticalLayout_4.addWidget(self.plotWindow_empty_and_signal)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_loading_empty_data = QtWidgets.QPushButton(Dialog)
        self.pushButton_loading_empty_data.setObjectName("pushButton_loading_empty_data")
        self.horizontalLayout.addWidget(self.pushButton_loading_empty_data)
        self.pushButton_loading_signal_data = QtWidgets.QPushButton(Dialog)
        self.pushButton_loading_signal_data.setObjectName("pushButton_loading_signal_data")
        self.horizontalLayout.addWidget(self.pushButton_loading_signal_data)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_signal_difference = QtWidgets.QPushButton(Dialog)
        self.pushButton_signal_difference.setObjectName("pushButton_signal_difference")
        self.horizontalLayout_2.addWidget(self.pushButton_signal_difference)
        self.label_text_threshold_value = QtWidgets.QLabel(Dialog)
        self.label_text_threshold_value.setObjectName("label_text_threshold_value")
        self.horizontalLayout_2.addWidget(self.label_text_threshold_value)
        self.lineEdit_threshold = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_threshold.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_threshold.setReadOnly(False)
        self.lineEdit_threshold.setObjectName("lineEdit_threshold")
        self.horizontalLayout_2.addWidget(self.lineEdit_threshold)
        self.pushButton_update_threshold = QtWidgets.QPushButton(Dialog)
        self.pushButton_update_threshold.setObjectName("pushButton_update_threshold")
        self.horizontalLayout_2.addWidget(self.pushButton_update_threshold)
        self.horizontalLayout_2.setStretch(0, 2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.setStretch(1, 1)
        self.horizontalLayout_7.addLayout(self.verticalLayout_4)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget_frequency_absorption = QtWidgets.QTableWidget(Dialog)
        self.tableWidget_frequency_absorption.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidget_frequency_absorption.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_frequency_absorption.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_frequency_absorption.setObjectName("tableWidget_frequency_absorption")
        self.tableWidget_frequency_absorption.setColumnCount(0)
        self.tableWidget_frequency_absorption.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget_frequency_absorption)
        self.label_statistics_on_selected_frequencies = QtWidgets.QLabel(Dialog)
        self.label_statistics_on_selected_frequencies.setText("")
        self.label_statistics_on_selected_frequencies.setObjectName("label_statistics_on_selected_frequencies")
        self.verticalLayout.addWidget(self.label_statistics_on_selected_frequencies)
        self.label_text_window_width = QtWidgets.QLabel(Dialog)
        self.label_text_window_width.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_text_window_width.setAlignment(QtCore.Qt.AlignCenter)
        self.label_text_window_width.setObjectName("label_text_window_width")
        self.verticalLayout.addWidget(self.label_text_window_width)
        self.lineEdit_window_width = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_window_width.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_window_width.setObjectName("lineEdit_window_width")
        self.verticalLayout.addWidget(self.lineEdit_window_width)
        self.pushButton_save_table_to_file = QtWidgets.QPushButton(Dialog)
        self.pushButton_save_table_to_file.setObjectName("pushButton_save_table_to_file")
        self.verticalLayout.addWidget(self.pushButton_save_table_to_file)
        self.horizontalLayout_7.addLayout(self.verticalLayout)
        self.horizontalLayout_7.setStretch(0, 2)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_7)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2.setStretch(0, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Детектирование сигнала - метод Порогового значения"))
        self.checkBox_read_filter.setText(_translate("Dialog", "Диапазон чтения"))
        self.label_text_frequency_from.setText(_translate("Dialog", "Частота от "))
        self.lineEdit_filter_frequency_start.setText(_translate("Dialog", "22308"))
        self.label_text_MHz_from.setText(_translate("Dialog", " МГц    "))
        self.label_text_frequency_to.setText(_translate("Dialog", "   до "))
        self.lineEdit_filter_frequency_end.setText(_translate("Dialog", "22342"))
        self.label_text_MHz_to.setText(_translate("Dialog", " МГц  "))
        self.pushButton_loading_empty_data.setText(_translate("Dialog", "Выбор данных ( без шума )"))
        self.pushButton_loading_signal_data.setText(_translate("Dialog", "Выбор данных ( с шумом )"))
        self.pushButton_signal_difference.setText(_translate("Dialog", "Вычитание"))
        self.label_text_threshold_value.setText(_translate("Dialog", "Пороговое значение (%):"))
        self.lineEdit_threshold.setText(_translate("Dialog", "30"))
        self.pushButton_update_threshold.setText(_translate("Dialog", "Определение"))
        self.label_text_window_width.setText(_translate("Dialog", "Ширина окна просмотра \n"
" найденных частот в МГц"))
        self.lineEdit_window_width.setText(_translate("Dialog", "4"))
        self.pushButton_save_table_to_file.setText(_translate("Dialog", "Сохранение в файл"))
import icon
