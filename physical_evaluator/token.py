TNUMBER = 0
TOP1 = 1
TOP2 = 2
TVAR = 3
TFUNCALL = 4

class Token:
    def __init__(self, type, index, prio, number):
        self.type_ = type
        self.index_ = index or 0
        self.prio_ = prio or 0
        self.number_ = number if number != None else 0

    def to_string(self):
        if self.type_ == TNUMBER:
            return self.number_
        if self.type_ == TOP1 or self.type_ == TOP2 or self.type_ == TVAR:
            return self.index_
        elif self.type_ == TFUNCALL:
            return 'CALL'
        else:
            return 'Invalid Token'
