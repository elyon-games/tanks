import common.random
class Packet:
    def __init__(self, datas):
        self.id = common.random.generate_random_hex()
        self.datas = datas

packets: dict[str, Packet] = {}