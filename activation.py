class Activation():
    def __init__(self):
        # command_generator reference
        self.cg_reference = None

    def set_reference(self, cg_reference):
        self.cg_reference = cg_reference

    def unset_reference(self):
        self.cg_reference = None

    def activate_command(self):
        self.cg_reference.activate()

class UserInput(Activation):
    def __init__(self):
        super().__init__()

    #def activate(self):
        #super().activate();

