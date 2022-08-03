class UpdateState():
    def __init__(self) -> None:
        self.available = True
    
    def block(self):
        self.available = False
    
    def unblock(self):
        self.available = True