
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
        return builder_function(CommandGenerator())
    def build_from(self, configuration): pass


class CommandGenerator():
    def __init__(self):
        self.command_queue = None
        self.commands = []

    def set_command_queue(command_queue):
        self.command_queue = command_queue

    def add_command(command):
        if command: self.commands.append(command)

    def set_activation(activation: Activation)

    def activate():
        if not self.command_queue:
            raise Error("command_generator error: command queue not set")
        for command in self.commands:
            self.command_queue.insert_command(command)

















