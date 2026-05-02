import os
from typing import List

from sqlalchemy.orm import Session
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.lang import Builder

from pecapul.app import PeCapulBaseApp
from pecapul.database import Tag, Lesson


Builder.load_file(os.path.join(os.path.dirname(__file__), 'editscreen.kv'))

class AddItemBox(Button):
    pass

class EditTermBox(BoxLayout):
    label_from: Label = ObjectProperty(None)
    text_from: TextInput = ObjectProperty(None)

    label_to: Label = ObjectProperty(None)
    text_to: TextInput = ObjectProperty(None)

class TagBox(BoxLayout):
    text_tag: TextInput = ObjectProperty(None)
    btn_delete: Button = ObjectProperty(None)
    tag_id: int = -1

    def on_pre_enter(self, *args):
        self.btn_delete.disabled = self.tag_id < 0

    def on_enter_pressed(self):
        app: PeCapulBaseApp | None = App.get_running_app()

        if app is None or len(self.text_tag.text) < 1:
            return

        self.text_tag.background_color = (1, 1, 1, 1)
        tag = Tag()
        with Session(app.engine) as session:
            try:
                tag.name = self.text_tag.text
                if self.tag_id > -1:
                    tag.id = self.tag_id

                app.trainer.save_tag(session, tag)

                session.commit()

                if tag.id > -1:
                    self.tag_id = tag.id

                editLesson: EditLessonScreen = app.manager.get_screen("edit_lesson")

                editLesson.edit_tag_list.add_widget(TagBox())
            except Exception as e:
                print(e)
                session.rollback()
                self.text_tag.background_color = (1, 0, 0, 1)

    def delete_tag(self):
        app: PeCapulBaseApp | None = App.get_running_app()

        if app is None or self.tag_id < 0:
            return
        
        with Session(app.engine) as session:
            try:
                app.trainer.delete_tag(session, self.tag_id)
                session.commit()

                editLesson: EditLessonScreen = app.manager.get_screen("edit_lesson")

                editLesson.on_pre_enter()
            except Exception:
                session.rollback()

class EditLessonScreen(Screen):
    
    lesson_id: int = -1
    edit_lesson_list: GridLayout = ObjectProperty(None)
    edit_tag_list: GridLayout = ObjectProperty(None)
    lesson_name: Label = ObjectProperty(None)

    app: PeCapulBaseApp | None

    def save_lesson(self):

        if self.app is None:
            return
        
        self.app.manager.current = "main_menu"

    def cancel_lesson(self):
        
        if self.app is None:
            return
        
        self.app.manager.current = "main_menu"

    def on_pre_enter(self, *args):
        
        self.app = App.get_running_app()

        if self.app is None:
            return

        self.edit_lesson_list.clear_widgets()
        self.edit_tag_list.clear_widgets()

        with Session(self.app.engine) as session:
            lesson: Lesson = self.app.trainer.load_lesson_by_id(session, self.lesson_id)

            self.lesson_name.text = lesson.name

            for lesson_term in lesson.lesson_terms:
                box = EditTermBox()
                box.label_from.text = lesson_term.term1.tag.name
                box.text_from.text = lesson_term.term1.value

                box.label_to.text = lesson_term.term2.tag.name
                box.text_to.text = lesson_term.term2.value

                self.edit_lesson_list.add_widget(box)

            tags: List[Tag] = self.app.trainer.load_all_tags(session)

            for tag in tags:
                box = TagBox()
                box.text_tag.text = tag.name
                box.tag_id = tag.id

                self.edit_tag_list.add_widget(box)

        self.edit_lesson_list.add_widget(AddItemBox())
        self.edit_tag_list.add_widget(TagBox())

    def add_tag(self):
        pass