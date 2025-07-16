from command import CommandQueue
from activation import Activation
import threading
import time

class Presenter:

    def __init__(self):
        self.terminate_input_worker = threading.Event()
        self.command_activations = dict()

    def update_presentation(self, data_to_draw):
        pass

    def adjust_data(self, data_to_draw):
        for i in range(len(data_to_draw)):
            data_to_draw[i] = self.adjust_data_point(data_to_draw[i])
        return data_to_draw
    
    def adjust_data_point(self, data_point):
        return data_point

    def __call__(self, data_to_draw):
        adjusted_data = self.adjust_data(data_to_draw)
        self.update_presentation(adjusted_data)

    def add_command_activation(self, key: str, activation: Activation):
        if key in self.command_activations:
            raise Error(f"redefinition of {key} command activation")
        self.command_activations[key] = activation

    def activate_command(self, command_key: str):
        if command_key in self.command_activations:
            self.command_activations[command_key].activate_command()

    def start_input_worker(self):
        self.input_worker = threading.Thread(target=self.input_worker_wrapper)
        self.input_worker.start()

    def stop_input_worker(self):
        self.terminate_input_worker.set()

    def input_worker_wrapper(self):
        while not self.terminate_input_worker.is_set():
            self.input_worker_work()

    def input_worker_work(self):
        time.sleep(0.5)


    """
    def create_command(self, command_identifier):

        # define functions somewhere else probably, maybe in some
        # dictionary and just access them with:
        # self.command_queue.insert_command(command_dict[command_identifier])
        #   ????
        def command1(obj): pass

        match command_identifier:
            case "command1":
                id = 1
                self.command_queue.insert_command(Command(id, command1))
            case _:
                pass
    
    """

