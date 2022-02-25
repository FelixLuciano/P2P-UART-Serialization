import random


class Commands:
    commands = []

    @classmethod
    def get (self, *values):
        return bytearray(values)


    @classmethod
    def add (self, *values):
        self.commands.append(self.get(*values))


    @classmethod
    def getRandom (self):
        return random.choice(self.commands)


    @classmethod
    def getSequence (self, size):
        return random.choices(self.commands, k=size)


    @classmethod
    def wrap (self, content, prefix=0b01010000, sufix=0b00000101):
        return self.get(prefix) + content + self.get(sufix)


    @classmethod
    def getStream (self, content, separator=0b01010101, *args):
        return self.wrap(self.get(separator).join(content), *args)

    
    @classmethod
    def getSequenceStream (self, size, *args):
        return self.getStream(self.getSequence(size), *args)


Commands.add(0x00, 0xFF, 0x00, 0xFF)
Commands.add(0x00, 0xFF, 0xFF, 00)
Commands.add(0xFF)
Commands.add(0x00)
Commands.add(0xFF, 0x00)
Commands.add(0x00, 0xFF)

# print(Commands.getStream(Commands.getSequence(random.randint(10, 30))))

print(Commands.getSequence(10))
