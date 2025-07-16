from activation import Activation

# Singleton
class CommandGeneratorBuilder():
    _instance = None
    def __init__(self): pass
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def build_empty(self): return CommandGenerator()
    def build_with(self, builder_function):
        new_command_generator = CommandGenerator()
        builder_function(new_command_generator)
        return new_command_generator
    def build_from(self, configuration): pass


class CommandGenerator():
    def __init__(self):
        self.command_queue = None
        self.commands = []
        self.activation = None

    def set_command_queue(self, command_queue):
        self.command_queue = command_queue

    def add_command(self, command):
        if command: self.commands.append(command)

    def set_activation(self, activation: Activation):
        if self.activation is not None:
            self.activation.unset_reference()
        self.activation = activation
        self.activation.set_reference(self)

    def activate(self):
        if not self.command_queue:
            raise Error("command_generator error: command queue not set")
        for command in self.commands:
            self.command_queue.insert_command(command)

















