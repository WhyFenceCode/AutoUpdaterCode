from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

class install_window(QtWidgets.QDialog):

    def change_stylesheet(self, button):
        # Reset all buttons to default style
        for btn in self.button_group.buttons():
            btn.setStyleSheet("""
                color:gray;
                font-size: 20px;
                font-weight: light;
                margin-left: 10px;
                margin-right: 10px;
                margin-bottom: 15px;
                margin-top: 15px;
                border-radius: 16px;
                padding-top: 20px;
                padding-bottom: 20px;
                padding-left: 10px;
                text-align: left;
            """)

        # Apply new style to selected button
        button.setStyleSheet("""
            color:gray;
            font-size: 20px;
            font-weight: light;
            background:rgb(48, 50, 76);
            margin-left: 10px;
            margin-right: 10px;
            margin-bottom: 15px;
            margin-top: 15px;
            border-radius: 16px;
            padding-top: 20px;
            padding-bottom: 20px;
            padding-left: 10px;
            text-align: left;
        """)

    def __init__(self):
        super().__init__()

        w = 405
        h = 720

        # Set dialog size
        self.resize(w, h)
        # Remove frame
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)
        # Make the dialog transparent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Round widget
        self.round_widget = QtWidgets.QWidget(self)
        self.round_widget.resize(w, h)

        self.round_widget.setStyleSheet(
            """
            background:rgb(26, 28, 48);
            border-radius: 32px;
            """
        )

        # Layout setup (if needed)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.round_widget)

        self.button_group = QButtonGroup(self)
        self.button_group.buttonClicked.connect(self.change_stylesheet)
        

        wdg_layout = QtWidgets.QVBoxLayout()
        wdg_layout.setAlignment(QtCore.Qt.AlignTop)
        self.round_widget.setLayout(wdg_layout)

        install_text = QtWidgets.QLabel(self)
        install_text.setText("INSTALL")
        wdg_layout.addWidget(install_text)
        install_text.setFont(QFont('Calibri')) 
        install_text.setStyleSheet(
            """
            color:white;
            font-size: 36px;
            font-weight: normal;
            margin-left: 20px;
            margin-top: 40px;
            """
        )

        install_subtext = QtWidgets.QLabel(self)
        install_subtext.setText("PROGRAM WILL RUN AFTER")
        wdg_layout.addWidget(install_subtext)
        install_subtext.setFont(QFont('Calibri')) 
        install_subtext.setStyleSheet(
            """
            color:gray;
            font-size: 20px;
            font-weight: light;
            margin-left: 20px;
            margin-bottom: 90px;
            """
        )

        shortcut_on = QtWidgets.QPushButton("CREATE DESKTOP SHORTCUT")
        wdg_layout.addWidget(shortcut_on)
        self.button_group.addButton(shortcut_on, id=1)
        shortcut_on.setFont(QFont('Calibri')) 
        shortcut_on.setStyleSheet(
            """
            color:gray;
            font-size: 20px;
            font-weight: light;
            background:rgb(48, 50, 76);
            margin-left: 10px;
            margin-right: 10px;
            margin-bottom: 15px;
            margin-top: 15px;
            border-radius: 16px;
            padding-top: 20px;
            padding-bottom: 20px;
            padding-left: 10px;
            text-align: left;
            """
        )

        shortcut_off = QtWidgets.QPushButton("NO DESKTOP SHORTCUT")
        wdg_layout.addWidget(shortcut_off)
        self.button_group.addButton(shortcut_off, id=2)
        shortcut_off.setFont(QFont('Calibri')) 
        shortcut_off.setStyleSheet(
            """
            color:gray;
            font-size: 20px;
            font-weight: light;
            margin-left: 10px;
            margin-right: 10px;
            margin-bottom: 15px;
            margin-top: 15px;
            border-radius: 16px;
            padding-top: 20px;
            padding-bottom: 20px;
            padding-left: 10px;
            text-align: left;
            """
        )

        go = QtWidgets.QPushButton("INSTALL")
        wdg_layout.addWidget(go)
        go.setFont(QFont('Calibri')) 
        go.setStyleSheet(
            """
            color:rgb(26, 28, 48);
            background:rgb(13, 245, 216);
            font-size: 20px;
            font-weight: light;
            margin-left: 35px;
            margin-right: 35px;
            margin-bottom: 15px;
            margin-top: 80px;
            border-radius: 16px;
            padding-top: 20px;
            padding-bottom: 20px;
            text-align: center;
            """
        )

        self.show()





class updates_window(QtWidgets.QDialog):

    def __init__(self, version):
        super().__init__()

        w = 405
        h = 720

        # Set dialog size
        self.resize(w, h)
        # Remove frame
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)
        # Make the dialog transparent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Round widget
        self.round_widget = QtWidgets.QWidget(self)
        self.round_widget.resize(w, h)

        self.round_widget.setStyleSheet(
            """
            background:rgb(26, 28, 48);
            border-radius: 32px;
            """
        )

        # Layout setup (if needed)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.round_widget)
        

        wdg_layout = QtWidgets.QVBoxLayout()
        wdg_layout.setAlignment(QtCore.Qt.AlignTop)
        self.round_widget.setLayout(wdg_layout)

        update_text = QtWidgets.QLabel(self)
        update_text.setText("UPDATE")
        wdg_layout.addWidget(update_text)
        update_text.setFont(QFont('Calibri')) 
        update_text.setStyleSheet(
            """
            color:white;
            font-size: 36px;
            font-weight: normal;
            margin-left: 20px;
            margin-top: 40px;
            """
        )

        install_subtext = QtWidgets.QLabel(self)
        install_subtext.setText("PROGRAM WILL RUN AFTER")
        wdg_layout.addWidget(install_subtext)
        install_subtext.setFont(QFont('Calibri')) 
        install_subtext.setStyleSheet(
            """
            color:gray;
            font-size: 20px;
            font-weight: light;
            margin-left: 20px;
            margin-bottom: 90px;
            """
        )

        version_text = QtWidgets.QLabel(self)
        version_text.setText(str(version))
        wdg_layout.addWidget(version_text)
        version_text.setFont(QFont('Calibri')) 
        version_text.setStyleSheet(
            """
            color:gray;
            font-size: 20px;
            font-weight: light;
            background:rgb(48, 50, 76);
            margin-left: 10px;
            margin-right: 10px;
            margin-bottom: 50px;
            margin-top: 50px;
            border-radius: 16px;
            padding-top: 20px;
            padding-bottom: 20px;
            padding-left: 10px;
            text-align: left;
            """
        )

        go = QtWidgets.QPushButton("UPDATE")
        wdg_layout.addWidget(go)
        go.setFont(QFont('Calibri')) 
        go.setStyleSheet(
            """
            color:rgb(26, 28, 48);
            background:rgb(13, 245, 216);
            font-size: 20px;
            font-weight: light;
            margin-left: 35px;
            margin-right: 35px;
            margin-bottom: 15px;
            margin-top: 80px;
            border-radius: 16px;
            padding-top: 20px;
            padding-bottom: 20px;
            text-align: center;
            """
        )

        self.show()

app = QtWidgets.QApplication([])
win = install_window()
#win = updates_window("1.0.0")
app.exec()