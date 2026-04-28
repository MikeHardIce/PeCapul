from sqlalchemy import create_engine

from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from pecapul.app import PeCapulBaseApp
from pecapul.database import Base
from pecapul.editscreen import EditLessonScreen
from pecapul.menuscreen import PeCapulMenuScreen
from pecapul.trainer import Trainer

Window.top = 50
Window.left = 100
Window.size = (1600, 900)

class PeCapulWindowManager(ScreenManager):
    pass

class PeCapulApp(PeCapulBaseApp):

    def build(self):
        self.engine = create_engine('sqlite:///my_database.db', echo=True)
    
        Base.metadata.create_all(self.engine)

        self.trainer = Trainer()
        self.manager = PeCapulWindowManager()

        self.manager.add_widget(PeCapulMenuScreen(name="main_menu"))
        self.manager.add_widget(EditLessonScreen(name="edit_lesson"))

        return self.manager

def main():
    PeCapulApp().run()

if __name__ == '__main__':
    main()