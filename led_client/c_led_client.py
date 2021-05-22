class led_client():
    def __init__(self, ipv4_addr):
        self.ipv4_addr = ipv4_addr
        self.recv_total_len = 0

    def get_ipv4_addr(self):
        return self.ipv4_addr

    def set_client_recv_total_len(self, val):
        self.recv_total_len = val

    def get_client_recv_total_len(self):
        return self.recv_total_len