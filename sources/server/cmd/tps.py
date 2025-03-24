from server.services.cmd.main import classCMD
from server.services.clock import getTPS, getTickRate

class tpsCMD(classCMD):
    def __init__(self):
        super().__init__(
            description="Permet de voir le TPS du serveur !",
            args=[]
        )

    def run(self, args=[]):
        tps = getTPS()
        tick_rate = getTickRate()
        percentage = (tps / tick_rate) * 100

        if percentage >= 90:
            comment = "Very Good"
        elif percentage >= 75:
            comment = "Good"
        elif percentage >= 50:
            comment = "Bad"
        else:
            comment = "Very Bad"

        print(f"TPS: {tps}/{tick_rate} - ({comment})")