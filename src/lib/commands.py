import binascii
import random


class Commands:
    commands = []

    @classmethod
    def get (self, *values):
        return bytes(bytearray(values))


    @classmethod
    def add (self, *values):
        self.commands.append(self.get(*values))


    @classmethod
    def getRandom (self):
        return random.choice(self.commands)


    @classmethod
    def getSequence (self, size):
        return random.choices(self.commands, k=size)


# Commands.add(0x00, 0xFF, 0x00, 0xFF)
# Commands.add(0x00, 0xFF, 0xFF, 00)
# Commands.add(0xFF)
# Commands.add(0x00)
# Commands.add(0xFF, 0x00)
# Commands.add(0x00, 0xFF)
