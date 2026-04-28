from sqlalchemy import Engine, create_engine

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from pecapul.database import Base
from pecapul.trainer import Trainer

class PeCapulBaseApp(App):

    engine: Engine
    trainer: Trainer
    manager: ScreenManager


    

