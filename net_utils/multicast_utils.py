import socket
import struct
import netifaces as ni
from log_utils import jlog
log = jlog.logging_init("multicast_utils")

def get_eth0_ip(net_if):
    ni.ifaddresses(net_if)
    ip = ni.ifaddresses(net_if)[ni.AF_INET][0]['addr']
    print("eth ip:", ip)
    return ip

def joinMcast_with_if(mcast_addr, port=10000, net_if='enp8s0'):
    """
    Returns a live multicast socket
    mcast_addr is a dotted string format of the multicast group
    port is an integer of the UDP port you want to receive
    if_ip is a dotted string format of the interface you will use
    """
    if_ip = get_eth0_ip(net_if)
    #create a UDP socket
    mcastsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    #allow other sockets to bind this port too
    mcastsock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    #explicitly join the multicast group on the interface specified
    mcastsock.setsockopt(socket.SOL_IP,socket.IP_ADD_MEMBERSHIP,
                socket.inet_aton(mcast_addr)+socket.inet_aton(if_ip))

    #finally bind the socket to start getting data into your socket
    mcastsock.bind((mcast_addr,port))

    return mcastsock


def multicast_sock_init():
    # Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout so the socket does not block indefinitely when trying
    # to receive data.
    sock.settimeout(2)

    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    return sock
