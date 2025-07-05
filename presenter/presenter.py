


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
    

