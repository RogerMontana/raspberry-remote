import os


class Dispaly:

    @staticmethod
    def show(payload):
        if str(payload).__len__() >= 110:
            raise Exception("Payload too long to display! max 110 symbols")
        cmd = "/home/pi/Desktop/display {}".format(payload)
        os.system(cmd)
