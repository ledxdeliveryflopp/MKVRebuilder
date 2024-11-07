# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'console_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

class UiRebuilderWidget(object):
    def setupUi(self, console_widget):
        if not console_widget.objectName():
            console_widget.setObjectName(u"console_widget")
        console_widget.resize(400, 300)
        self.verticalLayout_2 = QVBoxLayout(console_widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.main_layout = QVBoxLayout()
        self.main_layout.setObjectName(u"main_layout")
        self.sound = QLabel(console_widget)
        self.sound.setObjectName(u"sound")

        self.main_layout.addWidget(self.sound)

        self.subtitle = QLabel(console_widget)
        self.subtitle.setObjectName(u"subtitle")

        self.main_layout.addWidget(self.subtitle)

        self.ac3 = QLabel(console_widget)
        self.ac3.setObjectName(u"ac3")

        self.main_layout.addWidget(self.ac3)

        self.mkv = QLabel(console_widget)
        self.mkv.setObjectName(u"mkv")

        self.main_layout.addWidget(self.mkv)

        self.verticalLayout_2.addLayout(self.main_layout)


        QMetaObject.connectSlotsByName(console_widget)


