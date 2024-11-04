# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class UiSettingsWidget(object):
    def setupUi(self, settings_widget):
        if not settings_widget.objectName():
            settings_widget.setObjectName(u"settings_widget")
        settings_widget.resize(365, 258)
        self.verticalLayout_2 = QVBoxLayout(settings_widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.main_layout = QVBoxLayout()
        self.main_layout.setObjectName(u"main_layout")
        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.main_layout.addItem(self.verticalSpacer)

        self.bitrate_label = QLabel(settings_widget)
        self.bitrate_label.setObjectName(u"bitrate_label")
        self.bitrate_label.setMaximumSize(QSize(500, 50))

        self.main_layout.addWidget(self.bitrate_label)

        self.bitrate_box = QComboBox(settings_widget)
        self.bitrate_box.setObjectName(u"bitrate_box")

        self.main_layout.addWidget(self.bitrate_box, 0, Qt.AlignmentFlag.AlignVCenter)

        self.verticalSpacer_3 = QSpacerItem(20, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.main_layout.addItem(self.verticalSpacer_3)

        self.start_button = QPushButton(settings_widget)
        self.start_button.setObjectName(u"start_button")

        self.main_layout.addWidget(self.start_button, 0, Qt.AlignmentFlag.AlignVCenter)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.main_layout.addItem(self.verticalSpacer_2)


        self.verticalLayout_2.addLayout(self.main_layout)

        QMetaObject.connectSlotsByName(settings_widget)


