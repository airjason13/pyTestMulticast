# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
from log_utils import jlog
message = 'very important data'
from PyQt5 import QtWidgets

from c_mainwindow import *

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    log = jlog.logging_init("main")
    log.debug("This is main")
    print("yeah")
    qtapp = QtWidgets.QApplication([])
    window = MainWindow()


    window.move(0, 0)
    window.show()

    sys.exit(qtapp.exec_())

    """Send Data and Recv"""

    """sock = multicast_sock_init()
    multicast_group = ('224.3.29.71', 10000)
    try:

        # Send data to the multicast group
        print( 'sending "%s"' % message)
        sent = sock.sendto(message.encode(), multicast_group)

        # Look for responses from all recipients
        while True:
            print('waiting to receive')
            try:
                data, server = sock.recvfrom(16)
            except socket.timeout:
                print( 'timed out, no more responses')
                break
            else:
                print( 'received "%s" from %s' % (data, server))

    finally:
        print ('closing socket' )
        sock.close()"""

    """ Recv Data and Send"""
    """multicast_group = '224.3.29.71'
    server_address = ('', 10000)

    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind to the server address
    sock.bind(server_address)

    # Tell the operating system to add the socket to the multicast group
    # on all interfaces.
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while True:
        print('\nwaiting to receive message')
        data, address = sock.recvfrom(1024)

        print('received %s bytes from %s' % (len(data), address))
        print(data)

        print('sending acknowledgement to', address)
        sock.sendto('ack', address)"""