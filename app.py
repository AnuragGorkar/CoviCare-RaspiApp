import os
import sys
from time import time
import json
import string
import random
import qrcode
import socket
import subprocess
import statistics
from time import time
from cryptography.fernet import Fernet

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QGridLayout, QLineEdit

from guiCodes.gui import GUI
from databaseCodes.sqlite3.get_sqlite3 import SQLiteDataBase
from sensorCodes.PyMAX30102.get_HbO2 import GetHbO2
from sensorCodes.PyUSBMic.get_cough_record import RecordCough

def get_raspberry_pi_ip():
    ip_address = '';
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

def checkI2C(address):
    out = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
    stdout,stderr = out.communicate()
    return address in str(stdout)

def display_temp(msg, btn, self):  
    if not checkI2C("5a"):
        msg.setText("Disconnected")
    else:
        out = subprocess.Popen(['python', '/home/pi/Desktop/BE Project/sensorCodes/PyMLX90614/getTemp.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)    
        stdout,stderr = out.communicate()
        temp_value = stdout
        if temp_value is None:
            msg.setText("Retry")
        msg.setText(str(temp_value)[2:6] + " °C")
        self.vitals["temp"] = round(float(temp_value), 2)
        btn.setVisible(True)

def check_hb_o2_vals(hb_o2_dict):
    len_fnd = hb_o2_dict["fnd"]
    o2 = list(hb_o2_dict["o2"])
    len_o2 = len(o2)
    hb = list(hb_o2_dict["hb"])
    len_hb = len(hb)

    print(len_fnd, len_hb, len_o2)

    if (len_o2 < 200 or len_hb < 200 or len_fnd > (0.2 * len_o2)) or (len_fnd > (0.2 * len_hb)):
        return [0, 0]
    else:
        #Check SpO2 Values
        o2_healthy = []
        o2_copd = []
        o2_hypoxic = []
        o2_severely_hypoxic = []
        o2_emergency = []
        
        for o2_val in o2:
            if o2_val<0 or o2_val > 100:
                continue
            elif o2_val >= 94:
                o2_healthy.append(o2_val)
            elif o2_val < 94 and o2_val >= 88:
                o2_copd.append(o2_val)
            elif o2_val < 88 and o2_val >= 85:
                o2_hypoxic.append(o2_val)
            elif o2_val < 85 and o2_val >= 60:
                o2_severely_hypoxic.append(o2_val)
            elif o2_val < 60:
                o2_emergency.append(o2_val) 
        
        o2_valid = [o2_healthy, o2_copd, o2_hypoxic, o2_severely_hypoxic, o2_emergency]

        max_o2_list = o2_healthy
        for o2_val_list in o2_valid:
            if len(o2_val_list) >= len(max_o2_list):
                max_o2_list = o2_val_list 

        final_o2_val = sum(max_o2_list)/len(max_o2_list)

        #Check Heart Rate Values
        hb_low = []
        hb_med = []
        hb_normal = []
        hb_high = []
        hb_highest = []
        for hb_val in hb:
            if hb_val <= 0 or hb_val > 250:
                continue
            elif hb_val <= 40 and hb_val > 0:
                hb_low.append(hb_val)
            elif hb_val <= 60 and hb_val > 40:
                hb_med.append(hb_val)
            elif hb_val <= 120 and hb_val > 60:
                hb_normal.append(hb_val)
            elif hb_val <= 200 and hb_val >120:
                hb_high.append(hb_val)
            elif hb_val <=250 and hb_val > 220:
                hb_highest.append(hb_val)
            
        hb_valid = [hb_low, hb_med, hb_normal, hb_high, hb_highest]

        max_hb_list = hb_low
        for hb_val_list in hb_valid:
            if len(hb_val_list) >= len(max_hb_list):
                max_hb_list = hb_val_list

        mean_hb = statistics.mean(max_hb_list)
        median_hb = statistics.median(max_hb_list)
        final_hb_val = ((mean_hb + median_hb)/2)

        return [final_hb_val, final_o2_val]
    
def display_hb_o2(msg, btn, self):
    
    msg.setStyleSheet(
            "font-size: 35px; color: #ffffff; font-family: 'Roboto';" +
            "padding-left: 30px; padding-right: 30px;")    
    msg.setText("Hold finger on sensor for 30 sec")
    msg.repaint()
    
    if not checkI2C("57"):
        msg.setStyleSheet(
            "font-size: 45px; color: #ffffff; font-family: 'Roboto';" +
            "padding-left: 30px; padding-right: 30px;") 
        msg.setText("Disconnected")
        msg.repaint()
    else:
        try:
            ans = GetHbO2()
            hb_o2_dict = ans.getVal()
            values = check_hb_o2_vals(hb_o2_dict)
            msg.setVisible(True)
            msg.repaint()
            if (values[0] == 0 and values[1] == 0):
                msg.setStyleSheet(
                    "font-size: 45px; color: #ffffff; font-family: 'Roboto';" +
                    "padding-left: 30px; padding-right: 30px;")     
                msg.setText("Finger Undetected")
                msg.repaint()
            else:
                msg.setText(str(round(values[0], 2)) + " bpm" + "\n" + str(round(values[1], 2)) + " SpO2")
                self.vitals["hb"] = round(values[0], 2)
                self.vitals["o2"] = round(values[1], 2)
                msg.repaint()
                btn.setVisible(True)
        except Exception as e:
            print(e)
            msg.setStyleSheet(
                    "font-size: 45px; color: #ffffff; font-family: 'Roboto';" +
                    "padding-left: 30px; padding-right: 30px;") 
            msg.setText("Error! Retry...")
            msg.repaint()

def display_cough_recorded(recorded_cough_val, forward_btn, self):
    try:
        record_cough = RecordCough()
        recorded_cough_val.setStyleSheet(
                "font-size: 35px; color: #ffffff; font-family: 'Roboto';" +
                "padding-left: 30px; padding-right: 30px;") 
        recorded_cough_val.setText("Recording audio for 10 seconds")
        recorded_cough_val.repaint()
        record_cough.record_audio()
        recorded_cough_val.setText("Audio recorded successfully")
        recorded_cough_val.repaint()
        forward_btn.setVisible(True)
        self.vitals["cough_value"] = 0
    except Exception as e:
        recorded_cough_val.setText("Unexpected Error!")
        recorded_cough_val.repaint()
 
def display_qr(msg, image, self):
    try:             
        msg.setText("Encrypting Vitals...")    
        password = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k = 8))
        salt = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k = 6))
                
        self.vitals["raspiId"] = "UniqueRaspiId"
        self.vitals["timeStamp"] = str(round(time() * 1000))
         
        print(self.vitals)
        
        stream = os.popen(f"java EncryptVitals.java '{str(self.vitals)}' '{str(password)}' '{str(salt)}'") 
        stdout = stream.read()
        
        print("The encrypted Vitals are ", stdout)
        
        img = qrcode.make(str(stdout))
        msg.setText("Scan QR code to get vitals")
        img.save('vitals.png')
        
        pixmap = QPixmap('vitals.png')
        pixmap = pixmap.scaledToWidth(250)
        image.setPixmap(pixmap)
        image.setVisible(True)
    except Exception as e:
        print(e)
        msg.setVisible(True)
        
def display_qr_vitals_stream(msg, image, self):
    try:             
        password = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k = 8))
        salt = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k = 6))
           
        msg.setText("Scan QR for vitals streaming")
                
        stream = {"Password": password, "Salt": salt, "Data": get_raspberry_pi_ip()}
        
#        out = subprocess.Popen(['python3', '/home/pi/Desktop/BE Project/serverCodes/flaskServer.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#        sout,serr = out.communicate() 

        stream = os.popen(f"java EncryptVitals.java '{str(get_raspberry_pi_ip())}' '{str(password)}' '{str(salt)}'") 
        stdout = stream.read()
        
        print("The encrypted Vitals are ", stdout)
        
        img = qrcode.make(str(stdout))
        msg.setVisible(False)
        img.save('vitals.png')
        
        pixmap = QPixmap('vitals.png')
        pixmap = pixmap.scaledToWidth(250)
        image.setPixmap(pixmap)
        image.setVisible(True)
    except Exception as e:
        print(e)
        msg.setVisible(True)
        
class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.widgets = []
        self.vitals = {"raspiId": "Unique Raspi Id", "temp" : "NA", "hb" : "NA", "o2" : "NA", "cough_value" : "NA"}
        self.vitals_db = SQLiteDataBase()
        self.gui_elements = GUI()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        # Set Window Title and Image Icon
        self.setWindowTitle("CoviCare")
        self.setWindowIcon(QIcon("/home/pi/Desktop/BE Project/images/covicareLogo.png"))
        # Set Fixed Size for Window
        #self.setFixedSize(480, 320)
        self.setFixedSize(600, 400)
        # Set Window Framless
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # Set Window Style Properties
        self.setStyleSheet("background-color: #202124;")
        # Call Welcome Frame
        self.welcome_frame()

    def clear_widgets(self):
        for widget in self.widgets:
            widget.hide()
            widget.setParent(None)

    def frame_switch(self, frame):
        self.clear_widgets()
        frame()

    def welcome_frame(self):
        # Display App Logo
        app_logo_image = QPixmap("/home/pi/Desktop/BE Project/images/covicareLogo.png").scaled(120, 120)
        app_logo = QLabel()
        app_logo.setPixmap(app_logo_image)
        app_logo.setAlignment(QtCore.Qt.AlignCenter)
        app_logo.setStyleSheet("margin-top: 50px;")
        self.widgets.append(app_logo)

        # Display Welcome Message
        app_name = QLabel()
        app_name.setText("Welcome to CoviCare")
        app_name.setStyleSheet(
            "font-size: 22px; color: #ffffff; font-family: 'Roboto';" +
            "margin-top: 10px; margin-bottom: 10px;")
        app_name.setAlignment(QtCore.Qt.AlignCenter)
        self.widgets.append(app_name)

        # Display Go to Covicare Enter Application Button
        go_btn = self.gui_elements.get_button(
            "Go to CoviCare", "/home/pi/Desktop/BE Project/images/enterCoviCare.png")
        go_btn.clicked.connect(
            lambda: self.frame_switch(self.select_record_type_frame))
        self.widgets.append(go_btn)

        # Add widgets to grid
        self.grid.addWidget(app_logo, 0, 0)
        self.grid.addWidget(app_name, 1, 0)
        self.grid.addWidget(go_btn, 2, 0)

        self.show()

    def select_record_type_frame(self):
        self.vitals = {"temp" : "NA", "hb" : "NA", "o2" : "NA", "cough_value" : "NA"}
        record_btn = self.gui_elements.get_button("Record Vitals", "/home/pi/Desktop/BE Project/images/recordVitals.png")
        record_btn.clicked.connect(
            lambda: self.frame_switch(self.record_temp_frame))
        self.widgets.append(record_btn)

        monitor_vitals_btn = self.gui_elements.get_button(
            "Monitor Vitals", "/home/pi/Desktop/BE Project/images/monitorVitals.png")
        self.widgets.append(monitor_vitals_btn)
        monitor_vitals_btn.clicked.connect(
            lambda: self.frame_switch(self.continuous_vitals_frame))
        self.widgets.append(record_btn)

        view_vitals_btn = self.gui_elements.get_button(
            "View Vitals", "/home/pi/Desktop/BE Project/images/viewVitals.png")
        view_vitals_btn.clicked.connect(
            lambda: self.frame_switch(self.view_vitals_frame))
        self.widgets.append(view_vitals_btn)

        self.grid.addWidget(record_btn, 0, 0, 2, 3)
        self.grid.addWidget(monitor_vitals_btn, 1, 0, 2, 3)
        self.grid.addWidget(view_vitals_btn, 2, 0, 2, 3)

    def record_temp_frame(self):
        back_btn = self.gui_elements.get_back_button()
        back_btn.clicked.connect(
            lambda: self.frame_switch(self.select_record_type_frame))
        self.widgets.append(back_btn)

        forward_btn = self.gui_elements.get_forward_button()
        forward_btn.clicked.connect(lambda: self.frame_switch(self.record_hb_o2_frame))
        if str(self.vitals["temp"]) == "NA": 
            forward_btn.setVisible(False)
        else:
            forward_btn.setVisible(True)
        self.widgets.append(forward_btn)

        record_temp_msg = self.gui_elements.get_record_val_msg(
            "Please record your temperature by holding the back of your palm in front of the sensor and press the button")
        self.widgets.append(record_temp_msg)

        recorded_temp_val = self.gui_elements.get_record_val(str(self.vitals["temp"]))
        self.widgets.append(recorded_temp_val)

        record_temp_btn = self.gui_elements.get_image_button("/home/pi/Desktop/BE Project/images/thermometer.png")
        record_temp_btn.clicked.connect(lambda: display_temp(recorded_temp_val, forward_btn, self))
        self.widgets.append(record_temp_btn)

        self.grid.addWidget(back_btn, 0, 0)
        self.grid.addWidget(forward_btn, 0, 3, 1, 1, QtCore.Qt.AlignRight)
        self.grid.addWidget(record_temp_btn, 1, 0, 1, 4, QtCore.Qt.AlignCenter)
        self.grid.addWidget(record_temp_msg, 2, 0, 1, 4)
        self.grid.addWidget(recorded_temp_val, 3, 0, 1, 4)
    
    def record_hb_o2_frame(self):
        back_btn = self.gui_elements.get_back_button()
        back_btn.clicked.connect(
            lambda: self.frame_switch(self.record_temp_frame))
        self.widgets.append(back_btn)

        forward_btn = self.gui_elements.get_forward_button()
        forward_btn.clicked.connect(lambda: self.frame_switch(self.record_cough_frame))
        if str(self.vitals["hb"]) == "NA" or str(self.vitals["o2"]) == "NA": 
            forward_btn.setVisible(False)
        else:
            forward_btn.setVisible(True)
        self.widgets.append(forward_btn)

        record_hb_o2_msg = self.gui_elements.get_record_val_msg(
            "Please record your Heart Beat and Oxygen Level by holding your finger in front of the sensor and press the button")
        self.widgets.append(record_hb_o2_msg)

        recorded_hb_o2_val = self.gui_elements.get_record_val(str(self.vitals["hb"]) + "\n" +  str(self.vitals["o2"]))
        self.widgets.append(recorded_hb_o2_val)

        record_hb_o2_btn = self.gui_elements.get_image_button("/home/pi/Desktop/BE Project/images/heartBeatPulsOxygen.png")
        record_hb_o2_btn.setIconSize(QtCore.QSize(155, 135))
        record_hb_o2_btn.setFixedSize(160, 90)
        record_hb_o2_btn.clicked.connect(lambda: display_hb_o2(recorded_hb_o2_val, forward_btn, self))
        self.widgets.append(record_hb_o2_btn)

        self.grid.addWidget(back_btn, 0, 0)
        self.grid.addWidget(forward_btn, 0, 3, 1, 1, QtCore.Qt.AlignRight)
        self.grid.addWidget(record_hb_o2_btn, 1, 0, 1, 4, QtCore.Qt.AlignCenter)
        self.grid.addWidget(record_hb_o2_msg, 2, 0, 1, 4)
        self.grid.addWidget(recorded_hb_o2_val, 3, 0, 1, 4)

    def record_cough_frame(self):
        back_btn = self.gui_elements.get_back_button()
        back_btn.clicked.connect(
            lambda: self.frame_switch(self.record_hb_o2_frame))
        self.widgets.append(back_btn)

        forward_btn = self.gui_elements.get_forward_button()
        forward_btn.clicked.connect(lambda: self.frame_switch(self.get_uid_qr_frame))
        if str(self.vitals["cough_value"]) == "NA": 
            forward_btn.setVisible(False)
        else:
            forward_btn.setVisible(True)
        self.widgets.append(forward_btn)

        record_cough_msg = self.gui_elements.get_record_val_msg(
            "Please record your cough sound by pressing the button")
        self.widgets.append(record_cough_msg)

        recorded_cough_val = self.gui_elements.get_record_val(str(self.vitals["cough_value"]))
        self.widgets.append(recorded_cough_val)

        record_cough_btn = self.gui_elements.get_image_button("/home/pi/Desktop/BE Project/images/cough.png")
        
        record_cough_btn.setFixedSize(160, 90)
        record_cough_btn.clicked.connect(lambda: display_cough_recorded(recorded_cough_val, forward_btn, self))
        self.widgets.append(record_cough_btn)

        self.grid.addWidget(back_btn, 0, 0)
        self.grid.addWidget(forward_btn, 0, 3, 1, 1, QtCore.Qt.AlignRight)
        self.grid.addWidget(record_cough_btn, 1, 0, 1, 4, QtCore.Qt.AlignCenter)
        self.grid.addWidget(record_cough_msg, 2, 0, 1, 4)
        self.grid.addWidget(recorded_cough_val, 3, 0, 1, 4)

    def get_uid_qr_frame(self):
        self.vitals_db.store_vitals_data(self.vitals)
        
        back_btn = self.gui_elements.get_back_button()
        back_btn.clicked.connect(
            lambda: self.frame_switch(self.record_hb_o2_frame))
        self.widgets.append(back_btn)
        
        id_field = QLineEdit()
        id_field.setPlaceholderText("Enter Patient ID")
        id_field.setStyleSheet(
            "QLineEdit{padding: 5px 3px; border-width: 1px; border-style: solid; border-radius: 10; border-color: #6002EE; font-size: 18px; font-family: 'Roboto'; color: #FFFFFF}")
        self.widgets.append(id_field)

        enter_id_val = self.gui_elements.get_record_val_msg(
            "Press button to encrypt vitals and share using QR code.")
        self.widgets.append(enter_id_val)
        
        image_qr_label = QLabel(self)
        image_qr_label.setVisible(False)
        self.widgets.append(image_qr_label)

        show_qr_btn = QPushButton("Share with QR")
        show_qr_btn.setIcon(QIcon(
            "/home/pi/Desktop/BE Project/images/qrCode.png"))
        show_qr_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        show_qr_btn.setStyleSheet(
            "border: 1px solid #202124; border-radius: 8px;" +
            "font-size: 16px; font-weight: normal; font-family: 'Roboto';" +
            "background-color:  #202124; color: #B794F6;" +
            "padding: 8px 8px;"
        )
        show_qr_btn.clicked.connect(lambda: display_qr(enter_id_val, image_qr_label, self))
        self.widgets.append(show_qr_btn)
        
        self.grid.addWidget(back_btn, 0, 0)
        #self.grid.addWidget(id_field, 0, 1)
        self.grid.addWidget(show_qr_btn, 0, 1, 1, 3, Qt.AlignCenter)
        self.grid.addWidget(image_qr_label, 3, 0, 1, 4, Qt.AlignCenter) 
        self.grid.addWidget(enter_id_val, 2, 0, 1, 4)

    def view_vitals_frame(self):
        back_btn = self.gui_elements.get_back_button()
        back_btn.clicked.connect(
            lambda: self.frame_switch(self.select_record_type_frame))
        self.widgets.append(back_btn)

        id_field = QLineEdit()
        id_field.setPlaceholderText("Enter Patient ID")
        id_field.setStyleSheet(
            "QLineEdit{padding: 5px 3px; border-width: 1px; border-style: solid; border-radius: 10; border-color: #6002EE; font-size: 18px; font-family: 'Roboto'; color: #FFFFFF}")
        self.widgets.append(id_field)

        get_data_btn = QPushButton("Get Data")
        get_data_btn.setFixedHeight(35)
        get_data_btn.setIcon(QIcon(
            "/home/pi/Desktop/BE Project/images/downloadFile.png"))
        get_data_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        get_data_btn.setStyleSheet(
            "border: 2px solid #6002EE; border-radius: 8px;" +
            "font-size: 18px; font-weight: bold; font-family: 'Roboto';" +
            "background-color:  #B794F6; color: #202124; padding: 3px;")
        self.widgets.append(get_data_btn)
        #get_data_btn.setVisible(False)

        show_qr_btn = QPushButton("Share with QR")
        show_qr_btn.setIcon(QIcon(
            "/home/pi/Desktop/BE Project/images/qrCode.png"))
        show_qr_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        show_qr_btn.setStyleSheet(
            "border: 1px solid #202124; border-radius: 8px;" +
            "font-size: 16px; font-weight: normal; font-family: 'Roboto';" +
            "background-color:  #202124; color: #B794F6;" +
            "padding: 8px 8px;"
        )
        self.widgets.append(show_qr_btn)
        
        #id_field.setVisible(False);

        record = self.gui_elements.get_list_view()
        self.widgets.append(record[0])
        self.widgets.append(record[1])

        self.grid.addWidget(back_btn, 0, 0)
        self.grid.addWidget(id_field, 0, 1)
        self.grid.addWidget(get_data_btn, 0, 2, 1, 1)
        self.grid.addWidget(show_qr_btn, 1, 0, 1, 3, Qt.AlignCenter)
        self.grid.addWidget(record[0], 2, 0, 1, 4)
        
    def continuous_vitals_frame(self):
        back_btn = self.gui_elements.get_back_button()
        back_btn.clicked.connect(lambda: self.frame_switch(self.select_record_type_frame))
        self.widgets.append(back_btn)
        
        id_field = QLineEdit()
        id_field.setPlaceholderText("Enter Patient ID")
        id_field.setStyleSheet(
            "QLineEdit{padding: 5px 3px; border-width: 1px; border-style: solid; border-radius: 10; border-color: #6002EE; font-size: 18px; font-family: 'Roboto'; color: #FFFFFF}")
        self.widgets.append(id_field)
        id_field.setVisible(False)

        enter_id_val = self.gui_elements.get_record_val_msg(
            "Press button to start vitals streaming. Scan the QR to start vitals data.")
        self.widgets.append(enter_id_val)
        
        image_qr_label = QLabel(self)
        image_qr_label.setVisible(False)
        self.widgets.append(image_qr_label)

        show_qr_btn = QPushButton("Start continuous vitals streaming")
        show_qr_btn.setIcon(QIcon(
            "/home/pi/Desktop/BE Project/images/qrCode.png"))
        show_qr_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        show_qr_btn.setStyleSheet(
            "border: 1px solid #202124; border-radius: 8px;" +
            "font-size: 16px; font-weight: normal; font-family: 'Roboto';" +
            "background-color:  #202124; color: #B794F6;" +
            "padding: 8px 8px;"
        )
        show_qr_btn.clicked.connect(lambda: display_qr_vitals_stream(enter_id_val, image_qr_label, self))
        self.widgets.append(show_qr_btn)
        
        self.grid.addWidget(back_btn, 0, 0)
        #self.grid.addWidget(id_field, 0, 1)
        self.grid.addWidget(show_qr_btn, 0, 1, 1, 3, Qt.AlignCenter)
        self.grid.addWidget(image_qr_label, 3, 0, 1, 4, Qt.AlignCenter) 
        self.grid.addWidget(enter_id_val, 2, 0, 1, 4, Qt.AlignCenter)
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


    
