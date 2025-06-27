import time
from pyg_screen import PygScreen

pyg_screen1 = PygScreen()
pyg_screen2 = PygScreen()

if __name__ == "__main__":
    while True:
        pyg_screen1.update([(20, 20), (300, 200)])
        print(pyg_screen1.camera_index)
        time.sleep(10)
        pyg_screen2.update([(200, 200), (100, 400)])
        print(pyg_screen2.camera_index)
        time.sleep(10)
