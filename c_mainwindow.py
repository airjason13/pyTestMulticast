from UI.mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui, QtCore, QtNetwork
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QThread, QStringListModel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QRadioButton

from log_utils import jlog
from net_utils.c_parser_packet import cmd_parser
from led_client.c_led_client import led_client
from pyqt_worker import *
from net_utils import multicast_utils
from global_def.global_def import *
import socket

log = jlog.logging_init("MainWindow")

import threading
qmut = threading.Lock()

class MainWindow(QtWidgets.QMainWindow ):
    def __init__(self):
        super().__init__()
        log.debug("MainWindow construct")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.slm = QStringListModel()

        # only for client ipv4 saved
        self.client_ipv4_List = []

        # class of c_led_client
        self.client_list = []
        self.slm.setStringList(self.client_ipv4_List)
        self.ui.listView_client.setModel(self.slm)
        self.ipv4_addr = multicast_utils.get_eth0_ip('enp8s0')
        print("self.ipv4_addr = ", self.ipv4_addr)
        print("type(self.ipv4_addr) :", type(self.ipv4_addr))
        self.multicast_socket = multicast_utils.multicast_sock_init()
        #self.multicast_socket = multicast_utils.joinMcast_with_if(MULTICAST_IP)
        self.cmd_parser = cmd_parser(local_ipv4=self.ipv4_addr)

        self.send_data_total_len = 0
        self.send_data_total_len_per_sec = 0
        self.send_data_count = 0
        self.recv_count = 0
        self.thread_send = Worker(method=self.send_multicast)
        #self.thread_send.start()

        self.thread_recv = Worker(method=self.recv_multicast)
        #self.thread_recv.start()

        self._timer_send_data = QTimer(self)
        self._timer_send_data.timeout.connect(self.send_data)

        self._timer_recv_data = QTimer(self)
        self._timer_recv_data.timeout.connect(self.recv_multicast)


        self._timer_network_profile = QTimer(self)
        self._timer_network_profile.timeout.connect(self.cal_network_profile)
        self.btn_init()
        #self._timer_send_data.start(0.01)
        self._timer_network_profile.start(1)


    def btn_init(self):
        self.ui.btn_start_test.clicked.connect(self.start_test)
        self.ui.btn_stop_test.clicked.connect(self.stop_test)

    def start_test(self):
        print("start_test")
        self._timer_send_data.start(0.01)
        self._timer_recv_data.start(0.001)
        #self._timer_network_profile.start(1)

    def stop_test(self):
        if self._timer_send_data is not None:
            self._timer_send_data.stop()
        print("stop_test")

    def send_data(self):
        data_tmp = "A".encode()
        sent_data_len = self.multicast_socket.sendto(data_tmp * 65000, MULTICAST_GROUP)
        self.send_data_total_len_per_sec += sent_data_len
        self.send_data_total_len += sent_data_len
        self.send_data_count += 1
        #print("send_data_count : ", self.send_data_count)
        #self.recv_multicast()
        #self.stop_test()

    def cal_network_profile(self):
        speed_val = self.send_data_total_len_per_sec
        self.send_data_total_len_per_sec = 0
        label_str = "Speed: " + str(speed_val) + "Bytes"
        self.ui.label_profile_per_sec.setText(label_str)

        total_val = self.send_data_total_len
        label_str = "Total: " + str(total_val) + "Bytes"
        self.ui.label_profile_total.setText(label_str)


    def send_multicast(self):
        if(self.multicast_socket is None):
            print("No multicast socket")
            return
        #print("send_multicast")
        self.send_data()

    def recv_multicast(self):
        if(self.multicast_socket is None):
            print("No multicast socket")
            return
        try:
            data, from_ip = self.multicast_socket.recvfrom(32)
        except socket.timeout:
            print('timed out, no more responses')
        else:
            if from_ip[0] == '192.168.7.2':
                print('received "%s" from %s' % (data, from_ip))
            else:
                ret, type, response = self.cmd_parser.parse_packet(data, from_ip)
                self.recv_count += 1
                #print("self.recv_count : ", self.recv_count)
                if type == "report_data_length":
                    #print("type : %s, response :%s" % (type, response))
                    add_client_to_list = True
                    index = 0
                    for n in self.client_ipv4_List:
                        if n.split("   ")[0] == from_ip[0]:
                            add_client_to_list = False
                            break
                        index += 1
                    if add_client_to_list is True:
                        self.client_ipv4_List.append(from_ip[0] + "   " + response)
                        self.slm.setStringList(self.client_ipv4_List)
                        client = led_client(from_ip[0])
                        client.set_client_recv_total_len(response)
                        self.client_list.append(client)

                    else:
                        for n in self.client_list:
                            if n.get_ipv4_addr() == from_ip[0]:
                                n.set_client_recv_total_len(int(n.get_client_recv_total_len()) + int(response))
                                self.client_ipv4_List[index] = (from_ip[0] + "   " + str(n.get_client_recv_total_len()))
                                self.slm.setStringList(self.client_ipv4_List)


    def closeEvent(self, event):
        log.debug("closeEvent")