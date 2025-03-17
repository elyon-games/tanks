import common.random
from common.time import get_current_time_ms
class Packet:
    def __init__(self, type="client-to-server", datas={}):
        self.id = common.random.generate_random_hex(8)
        self.time = get_current_time_ms()
        self.datas = datas
        self.type = type
        self.status = "init"