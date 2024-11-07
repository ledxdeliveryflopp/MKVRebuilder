# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QListView, QMainWindow, QMenuBar, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QStatusBar,
    QVBoxLayout, QWidget)

class UiMainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(706, 679)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.main_layout = QVBoxLayout()
        self.main_layout.setObjectName(u"main_layout")
        self.source_button = QPushButton(self.centralwidget)
        self.source_button.setObjectName(u"source_button")

        self.main_layout.addWidget(self.source_button)

        self.source_label = QLabel(self.centralwidget)
        self.source_label.setObjectName(u"source_label")
        self.source_label.setMaximumSize(QSize(16777215, 50))
        self.source_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.source_label)

        self.target_button = QPushButton(self.centralwidget)
        self.target_button.setObjectName(u"target_button")

        self.main_layout.addWidget(self.target_button)

        self.target_label = QLabel(self.centralwidget)
        self.target_label.setObjectName(u"target_label")
        self.target_label.setMaximumSize(QSize(16777215, 50))
        self.target_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.target_label)

        self.temp_button = QPushButton(self.centralwidget)
        self.temp_button.setObjectName(u"temp_button")

        self.main_layout.addWidget(self.temp_button)

        self.temp_label = QLabel(self.centralwidget)
        self.temp_label.setObjectName(u"temp_label")
        self.temp_label.setMaximumSize(QSize(16777215, 50))
        self.temp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.temp_label)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.main_layout.addItem(self.verticalSpacer)

        self.bitrate_label = QLabel(self.centralwidget)
        self.bitrate_label.setObjectName(u"bitrate_label")
        self.bitrate_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.bitrate_label)

        self.bitrate_box = QComboBox(self.centralwidget)
        self.bitrate_box.setObjectName(u"bitrate_box")

        self.main_layout.addWidget(self.bitrate_box)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.main_layout.addItem(self.verticalSpacer_3)

        self.settings_button = QPushButton(self.centralwidget)
        self.settings_button.setObjectName(u"settings_button")

        self.main_layout.addWidget(self.settings_button, 0, Qt.AlignmentFlag.AlignVCenter)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.main_layout.addItem(self.verticalSpacer_2)

        self.subtitle_layout = QHBoxLayout()
        self.subtitle_layout.setObjectName(u"subtitle_layout")
        self.horizontalSpacer_2 = QSpacerItem(50, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.subtitle_layout.addItem(self.horizontalSpacer_2)

        self.subtitles_button = QRadioButton(self.centralwidget)
        self.subtitles_button.setObjectName(u"subtitles_button")

        self.subtitle_layout.addWidget(self.subtitles_button)

        self.horizontalSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.subtitle_layout.addItem(self.horizontalSpacer)


        self.main_layout.addLayout(self.subtitle_layout)

        self.lists_layout = QHBoxLayout()
        self.lists_layout.setObjectName(u"lists_layout")
        self.audio_list = QListView(self.centralwidget)
        self.audio_list.setObjectName(u"audio_list")
        self.audio_list.setMaximumSize(QSize(16777215, 340))

        self.lists_layout.addWidget(self.audio_list)

        self.subtitle_list = QListView(self.centralwidget)
        self.subtitle_list.setObjectName(u"subtitle_list")
        self.subtitle_list.setMaximumSize(QSize(16777215, 340))

        self.lists_layout.addWidget(self.subtitle_list)


        self.main_layout.addLayout(self.lists_layout)


        self.verticalLayout_2.addLayout(self.main_layout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 706, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)


        QMetaObject.connectSlotsByName(MainWindow)
