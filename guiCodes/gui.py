import sys
from PyQt5.QtWidgets import QLabel, QPushButton, QListWidget, QListWidgetItem, QScrollBar,  QProgressBar
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor, QIcon

from databaseCodes.sqlite3.get_sqlite3 import SQLiteDataBase

class GUI():
    def get_button(self, button_name, button_image_path):
        btn = QPushButton(button_name)
        btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        btn.setIcon(QIcon(button_image_path))
        btn.setStyleSheet(
            "border: 2px solid #6002EE; border-radius: 10px;" +
            "font-size: 18px; font-weight: bold; font-family: 'Roboto';" +
            "background-color:  #B794F6; color: #202124;" +
            "padding: 5px 0px;"
        )
        return btn

    def get_back_button(self):
        back_btn = QPushButton()
        back_btn.setIcon(QIcon(
            "/home/pi/Desktop/BE Project/images/returnButton.png"))
        back_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        back_btn.setFixedSize(45, 35)
        back_btn.setStyleSheet(
            "border: 2px solid #6002EE; border-radius: 8px;" +
            "font-size: 16px; font-weight: bold; font-family: 'Roboto';" +
            "background-color:  #B794F6; color: #202124;" +
            "padding: 8px 8px;"
        )
        return back_btn
    
    def get_forward_button(self):
        forward_btn = QPushButton()
        forward_btn.setIcon(QIcon(
            "/home/pi/Desktop/BE Project/images/forwardButton.png"))
        forward_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        forward_btn.setFixedSize(45, 35)
        forward_btn.setStyleSheet(
            "border: 2px solid #6002EE; border-radius: 8px;" +
            "font-size: 16px; font-weight: bold; font-family: 'Roboto';" +
            "background-color:  #B794F6; color: #202124;" +
            "padding: 8px 8px;"
        )
        return forward_btn
    
    def get_image_button(self, img_path):
        img_btn = QPushButton()
        img_btn.setIcon(QIcon(img_path))
        img_btn.setIconSize(QtCore.QSize(75, 75))
        img_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        img_btn.setFixedSize(95, 95)
        img_btn.setStyleSheet(
            "border: 2px solid #6002EE; border-radius: 10px;" +
            "font-size: 16px; font-weight: bold; font-family: 'Roboto';" +
            "background-color:  #B794F6; color: #202124;" +
            "padding: 8px 8px;"
        )
        return img_btn

    def get_record_image(self, path):
        record_val_img = QPixmap(path).scaled(75, 75)
        record_val = QLabel()
        record_val.setAlignment(QtCore.Qt.AlignCenter)
        record_val.setPixmap(record_val_img)
        record_val.setAlignment(QtCore.Qt.AlignCenter)
        record_val.setStyleSheet("")
        return record_val

    def get_record_val_msg(self, message):
        record_val_msg = QLabel()
        record_val_msg.setAlignment(QtCore.Qt.AlignCenter)
        record_val_msg.setText(message)
        record_val_msg.setWordWrap(True)
        record_val_msg.setStyleSheet(
            "font-size: 16px; color: #ffffff; font-family: 'Roboto';" +
            "margin-bottom: 5px; padding-left: 30px; padding-right: 30px;")
        record_val_msg.setAlignment(QtCore.Qt.AlignCenter)
        return record_val_msg

    def get_record_val(self, value):
        recorded_val_lbl = QLabel()
        recorded_val_lbl.setAlignment(QtCore.Qt.AlignCenter)
        recorded_val_lbl.setText(value)
        recorded_val_lbl.setWordWrap(True)
        recorded_val_lbl.setStyleSheet(
            "font-size: 45px; color: #ffffff; font-family: 'Roboto';" +
            "padding-left: 30px; padding-right: 30px;")
        recorded_val_lbl.setAlignment(QtCore.Qt.AlignCenter)
        return recorded_val_lbl

    def get_list_view(self):
        scrollbar_stylesheet = """
                    /* --------------------------------------- QScrollBar  -----------------------------------*/
                    QScrollBar:vertical
                    {
                        background-color: #2A2929;
                        width: 20px;
                        margin: 15px 3px 15px 3px;
                        border: 1px transparent #2A2929;
                        border-radius: 5px;
                    }

                    QScrollBar::handle:vertical
                    {
                        background-color: #6002EE;       
                        min-height: 5px;
                        border-radius: 5px;
                        width: 20px;
                        margin: 7px 1px;
                    }

                    QScrollBar::sub-line:vertical
                    {
                        margin: 0px 0px 0px 0px;
                        height: 21px;
                        width: 18px;
                        subcontrol-position: top;
                        subcontrol-origin: margin;
                    }

                    QScrollBar::add-line:vertical
                    {
                        margin: 0px 0px 0px 0px;
                        height: 21px;
                        width: 18px;
                        subcontrol-position: bottom;
                        subcontrol-origin: margin;
                    }

                    QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
                    {
                        height: 20px;
                        width: 16px;
                        subcontrol-position: top;
                        subcontrol-origin: margin;
                    }

                    QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
                    {
                        height: 20px;
                        width: 16px;
                        subcontrol-position: bottom;
                        subcontrol-origin: margin;
                    }

                    QScrollBar::up-arrow:vertical
                    {
                    }

                    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
                    {
                        background: none;
                    }
                    """
        list_widget = QListWidget()
        
        vitals_db = SQLiteDataBase()
        vitals_db_list = vitals_db.get_vitals_data();
  
        vitals_list = [ "Temp: 104  SpO2: 98    Pulse: 84   Cough: 0",
                        "Temp: 98   SpO2: 97    Pulse: 83   Cough: 0",
                        "Temp: 95  SpO2: 99    Pulse: 60   Cough: 0",
                        "Temp: 95  SpO2: 95    Pulse: 200  Cough: 0",
                        "Temp: 97  SpO2: 94    Pulse: 43   Cough: 0",
                        "Temp: 99  SpO2: 97    Pulse: 76   Cough: 0",
                        "Temp: 97  SpO2: 93    Pulse: 89   Cough: 0",
                        "Temp: 96  SpO2: 92    Pulse: 92   Cough: 0",
                        "Temp: 96  SpO2: 95    Pulse: 82   Cough: 0",
                        "Temp: 98  SpO2: 97    Pulse: 56   Cough: 0",
                        "Temp: 98  SpO2: 96    Pulse: 78   Cough: 0",
                        "Temp: 97  SpO2: 98    Pulse: 89   Cough: 0",
                        "Temp: 98  SpO2: 96    Pulse: 89   Cough: 0",
                        "Temp: 78  SpO2: 99    Pulse: 88   Cough: 0",
                        "Temp: 78  SpO2: 99    Pulse: 88   Cough: 0",
                        "Temp: 99  SpO2: 95    Pulse: 84   Cough: 0",
                        "Temp: 34  SpO2: 94    Pulse: 67   Cough: 0",
                        "Temp: 34  SpO2: 96    Pulse: 84   Cough: 0",
                        "Temp: 34  SpO2: 98    Pulse: 80   Cough: 0"]
        
        for vitals_data in vitals_db_list:
            vitals_list.insert(0, f"Temp: {vitals_data[0]}  SpO2: {vitals_data[1]}    Pulse: {vitals_data[2]}  Cough: {0}")
        
        background = True
        for vitals_string in vitals_list:
                item = QListWidgetItem(vitals_string)
                if background:
                        item.setBackground(QtGui.QColor("#B794F6"))
                        item.setFont(QtGui.QFont("Roboto", 14))
                        background = False
                else:
                        item.setForeground(QtGui.QColor("#FFFFFF"))
                        item.setBackground(QtGui.QColor("#202124"))
                        item.setFont(QtGui.QFont("Roboto", 14))
                        background = True
                list_widget.addItem(item)
                

        scroll_bar = QScrollBar()

        scroll_bar.setStyleSheet(scrollbar_stylesheet)

        list_widget.setStyleSheet(
            "QListWidget{ border: none}")
        list_widget.setVerticalScrollBar(scroll_bar)

        return [list_widget, scroll_bar]

    def get_progress_bar(self, sec_time, window):
        progress_bar_stylesheet = """
                        QProgressBar {
                            border: 3px solid #6002EE;
                            border-radius: 5px;
                        }

                        QProgressBar::chunk {
                            background-color: #B794F6;
                            width: 20px;
                        }
                        """
        progress_bar = QProgressBar(window)
        progress_bar.setAlignment(QtCore.Qt.AlignCenter)
        progress_bar.setTextVisible(False)

        progress_bar.setStyleSheet(progress_bar_stylesheet)
        progress_bar.setMaximum(sec_time)
        progress_bar.setValue(0)

        return progress_bar
