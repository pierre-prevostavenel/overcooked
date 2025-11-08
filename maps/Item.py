from utils.MySprite import MySprite

class Item(MySprite):

    def __init__(self, name, rect=(0,0,50,50), image_path='./assets/trash3.png', fallback_color=(255, 255, 255), layer=0):
        self.name = name
        super().__init__(rect, image_path=image_path, fallback_color=fallback_color, layer=layer)
