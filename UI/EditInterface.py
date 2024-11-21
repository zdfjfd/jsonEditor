# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\项目\project Chess\jsonEditor\UI\EditInterface.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(576, 511)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(100, 100))
        self.groupBox_2.setStyleSheet("QGroupBox {\n"
"    border: none;\n"
"}")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2.addWidget(self.groupBox)
        self.editBox = QtWidgets.QGroupBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editBox.sizePolicy().hasHeightForWidth())
        self.editBox.setSizePolicy(sizePolicy)
        self.editBox.setMinimumSize(QtCore.QSize(100, 150))
        self.editBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.editBox.setBaseSize(QtCore.QSize(100, 200))
        self.editBox.setTitle("")
        self.editBox.setObjectName("editBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.editBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_5 = QtWidgets.QGroupBox(self.editBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout.setObjectName("gridLayout")
        self.saveBox = QtWidgets.QGroupBox(self.groupBox_5)
        self.saveBox.setTitle("")
        self.saveBox.setObjectName("saveBox")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.saveBox)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.saveItemButton = PushButton(self.saveBox)
        self.saveItemButton.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.saveItemButton.setFont(font)
        self.saveItemButton.setObjectName("saveItemButton")
        self.verticalLayout_5.addWidget(self.saveItemButton)
        self.resetItemButton = PushButton(self.saveBox)
        self.resetItemButton.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.resetItemButton.setFont(font)
        self.resetItemButton.setObjectName("resetItemButton")
        self.verticalLayout_5.addWidget(self.resetItemButton)
        self.gridLayout.addWidget(self.saveBox, 1, 8, 1, 1)
        self.line = QtWidgets.QFrame(self.groupBox_5)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 3, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.groupBox_5)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 1, 3, 1, 1)
        self.groupBox_9 = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox_9.setTitle("")
        self.groupBox_9.setObjectName("groupBox_9")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_9)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.removeItemButton = TransparentToolButton(self.groupBox_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removeItemButton.sizePolicy().hasHeightForWidth())
        self.removeItemButton.setSizePolicy(sizePolicy)
        self.removeItemButton.setMinimumSize(QtCore.QSize(20, 50))
        self.removeItemButton.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.removeItemButton.setFont(font)
        self.removeItemButton.setText("")
        self.removeItemButton.setIconSize(QtCore.QSize(16, 16))
        self.removeItemButton.setObjectName("removeItemButton")
        self.horizontalLayout_6.addWidget(self.removeItemButton)
        self.itemComboBox = ComboBox(self.groupBox_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.itemComboBox.sizePolicy().hasHeightForWidth())
        self.itemComboBox.setSizePolicy(sizePolicy)
        self.itemComboBox.setMinimumSize(QtCore.QSize(50, 50))
        self.itemComboBox.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.itemComboBox.setFont(font)
        self.itemComboBox.setObjectName("itemComboBox")
        self.horizontalLayout_6.addWidget(self.itemComboBox)
        self.groupBox_8 = QtWidgets.QGroupBox(self.groupBox_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_8.sizePolicy().hasHeightForWidth())
        self.groupBox_8.setSizePolicy(sizePolicy)
        self.groupBox_8.setMinimumSize(QtCore.QSize(50, 50))
        self.groupBox_8.setMaximumSize(QtCore.QSize(16777215, 50))
        self.groupBox_8.setTitle("")
        self.groupBox_8.setObjectName("groupBox_8")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_8)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lastItemButton = TransparentToolButton(self.groupBox_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lastItemButton.sizePolicy().hasHeightForWidth())
        self.lastItemButton.setSizePolicy(sizePolicy)
        self.lastItemButton.setMinimumSize(QtCore.QSize(10, 10))
        self.lastItemButton.setMaximumSize(QtCore.QSize(30, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.lastItemButton.setFont(font)
        self.lastItemButton.setText("")
        self.lastItemButton.setIconSize(QtCore.QSize(8, 8))
        self.lastItemButton.setObjectName("lastItemButton")
        self.verticalLayout_4.addWidget(self.lastItemButton)
        self.nextItemButton = TransparentToolButton(self.groupBox_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nextItemButton.sizePolicy().hasHeightForWidth())
        self.nextItemButton.setSizePolicy(sizePolicy)
        self.nextItemButton.setMinimumSize(QtCore.QSize(10, 10))
        self.nextItemButton.setMaximumSize(QtCore.QSize(30, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.nextItemButton.setFont(font)
        self.nextItemButton.setText("")
        self.nextItemButton.setIconSize(QtCore.QSize(8, 8))
        self.nextItemButton.setObjectName("nextItemButton")
        self.verticalLayout_4.addWidget(self.nextItemButton)
        self.horizontalLayout_6.addWidget(self.groupBox_8)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.gridLayout.addWidget(self.groupBox_9, 1, 4, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 8, 1, 1)
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox_7.setTitle("")
        self.groupBox_7.setObjectName("groupBox_7")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.itemLineEdit = DropDownLineEdit(self.groupBox_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.itemLineEdit.sizePolicy().hasHeightForWidth())
        self.itemLineEdit.setSizePolicy(sizePolicy)
        self.itemLineEdit.setMinimumSize(QtCore.QSize(50, 50))
        self.itemLineEdit.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.itemLineEdit.setFont(font)
        self.itemLineEdit.setClearButtonEnabled(True)
        self.itemLineEdit.setObjectName("itemLineEdit")
        self.horizontalLayout_4.addWidget(self.itemLineEdit)
        self.gridLayout.addWidget(self.groupBox_7, 2, 4, 1, 1)
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.catalogLineEdit = DropDownLineEdit(self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.catalogLineEdit.sizePolicy().hasHeightForWidth())
        self.catalogLineEdit.setSizePolicy(sizePolicy)
        self.catalogLineEdit.setMinimumSize(QtCore.QSize(50, 50))
        self.catalogLineEdit.setMaximumSize(QtCore.QSize(16777215, 50))
        self.catalogLineEdit.setClearButtonEnabled(True)
        self.catalogLineEdit.setObjectName("catalogLineEdit")
        self.horizontalLayout_3.addWidget(self.catalogLineEdit)
        self.gridLayout.addWidget(self.groupBox_6, 2, 1, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.removeCatalogButton = TransparentToolButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removeCatalogButton.sizePolicy().hasHeightForWidth())
        self.removeCatalogButton.setSizePolicy(sizePolicy)
        self.removeCatalogButton.setMinimumSize(QtCore.QSize(20, 50))
        self.removeCatalogButton.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.removeCatalogButton.setFont(font)
        self.removeCatalogButton.setText("")
        self.removeCatalogButton.setIconSize(QtCore.QSize(16, 16))
        self.removeCatalogButton.setObjectName("removeCatalogButton")
        self.horizontalLayout.addWidget(self.removeCatalogButton)
        self.catalogComboBox = ComboBox(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.catalogComboBox.sizePolicy().hasHeightForWidth())
        self.catalogComboBox.setSizePolicy(sizePolicy)
        self.catalogComboBox.setMinimumSize(QtCore.QSize(50, 50))
        self.catalogComboBox.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.catalogComboBox.setFont(font)
        self.catalogComboBox.setObjectName("catalogComboBox")
        self.horizontalLayout.addWidget(self.catalogComboBox)
        self.gridLayout.addWidget(self.groupBox_4, 1, 1, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 2, 1, 1)
        self.label = SubtitleLabel(self.groupBox_5)
        font = QtGui.QFont()
        font.setFamily("VonwaonBitmap 16px")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.label_2 = SubtitleLabel(self.groupBox_5)
        font = QtGui.QFont()
        font.setFamily("VonwaonBitmap 16px")
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 4, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_5)
        self.line_3 = QtWidgets.QFrame(self.editBox)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.verticalLayout_2.addWidget(self.editBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 300))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.scrollArea = SmoothScrollArea(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.editFormLayout = QtWidgets.QWidget()
        self.editFormLayout.setGeometry(QtCore.QRect(0, 0, 524, 286))
        self.editFormLayout.setAutoFillBackground(True)
        self.editFormLayout.setObjectName("editFormLayout")
        self.formLayout = QtWidgets.QFormLayout(self.editFormLayout)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setSpacing(0)
        self.formLayout.setObjectName("formLayout")
        self.scrollArea.setWidget(self.editFormLayout)
        self.horizontalLayout_2.addWidget(self.scrollArea)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.saveItemButton.setToolTip(_translate("Form", "保存当前显示的数据"))
        self.saveItemButton.setText(_translate("Form", "保存"))
        self.resetItemButton.setToolTip(_translate("Form", "重置为保存前的数据"))
        self.resetItemButton.setText(_translate("Form", "重置"))
        self.removeItemButton.setToolTip(_translate("Form", "删除当前项"))
        self.itemLineEdit.setToolTip(_translate("Form", "输入键"))
        self.catalogLineEdit.setToolTip(_translate("Form", "输入键"))
        self.removeCatalogButton.setToolTip(_translate("Form", "删除当前分类"))
        self.label.setText(_translate("Form", "Catalog"))
        self.label_2.setText(_translate("Form", "Item"))
from EditorWidgets import DropDownLineEdit
from qfluentwidgets import ComboBox, PushButton, SmoothScrollArea, SubtitleLabel, TransparentToolButton