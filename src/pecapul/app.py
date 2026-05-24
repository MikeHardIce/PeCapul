from sqlalchemy import Engine

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from pecapul.trainer import Trainer

class PeCapulBaseApp(App):

    engine: Engine
    trainer: Trainer
    manager: ScreenManager


    

