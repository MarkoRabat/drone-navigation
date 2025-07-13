from command import CommandQueue

class Presenter:

    def __init__(self):
        pass

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

    def set_command_queue(self, command_queue: CommandQueue):
        self.command_queue = command_queue

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
    

