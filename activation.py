class Activation():
    def __init__(self):
        # command_generator reference
        self.cg_reference = None

    def set_reference(self, cg_reference):
        self.cg_reference = cg_reference

    def unset_reference(self):
        self.cg_reference = None

    def activate_command(self):
        if self.cg_reference is None:
            raise Error("command generator reference not set")
        self.cg_reference.activate()
    
    def set_parameter(self, param_key, param_value):
        if self.cg_reference is None:
            raise Error("command generator reference not set")
        for command in self.cg_reference.commands:
            command.set_parameter(param_key, param_value)
    
    def clear_parameters(self):
        if self.cg_reference is None:
            raise Error("command generator reference not set")
        for command in self.cg_reference.commands:
            command.clear_parameters()


class UserInput(Activation):
    def __init__(self):
        super().__init__()

    #def activate(self):
        #super().activate();

