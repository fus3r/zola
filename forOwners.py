class Owners:
    Perms=[]

    def getAttributes(self):
            return [self.Perms]
    def __init__(self, Perms):
        self.Perms = Perms