from model import AudioModel
from view import AudioView

class AudioController:
    def __init__(self):
        self.model = AudioModel()
        self.view = AudioView(self)

if __name__ == "__main__":
    controller = AudioController()
    controller.view.run()
