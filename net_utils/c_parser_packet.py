
class cmd_parser():
    def __init__(self, local_ipv4):
        print("cmd_parser construct")
        self.local_ipv4_addr = local_ipv4

    def parse_packet(self, data, from_ip):
        #print("parse_packet")
        #print("adv ", data.decode().split(":"))
        switcher = {
            "client_recv_data_len": self.parser_client_recv_data_len,
        }
        parser_func = switcher.get(data.decode().split(":")[0], lambda x: "Invalid cmd_tag")
        return parser_func(data)

    def parser_client_recv_data_len(self,  data):
        #print("in parser_client_recv_data_len, data:", data)
        type = "report_data_length"
        return 0, type, data.decode().split(":")[1]