
class cmd_parser():
    def __init__(self, local_ipv4):
        print("cmd_parser construct")
        self.local_ipv4_addr = local_ipv4
        self.recv_count = 0

    def parse_packet(self, data, from_ip):
        try:

            switcher = {
                "client_recv_data_len": self.parser_client_recv_data_len,
            }
            parser_func = switcher.get(data.decode().split(":")[0], lambda x: "Invalid cmd_tag")
            return parser_func(data)
        except Exception as e:
            print(e)
        return None

    def parser_client_recv_data_len(self,  data):
        self.recv_count += 1

        try:
            print("data: %s, count : %d" %  (data.decode().split(":")[1], self.recv_count))
            type = "report_data_length"
            return 0, type, data.decode().split(":")[1]
        except Exception as e:
            print(e)
        return None
