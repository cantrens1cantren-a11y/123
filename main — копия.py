from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
import requests

# БАЗОВЫЙ URL СЕРВЕРА - ЗАМЕНИЛ НА ТВОЙ RENDER URL
SERVER_URL = "https://na15hardoasvx-9.onrender.com"

Window.clearcolor = (0.1, 0.3, 0.8, 1)

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        with self.canvas.before:
            Color(0.2, 0.6, 1, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical', padding=dp(40), spacing=dp(25))
        
        with main_layout.canvas.before:
            Color(0.1, 0.3, 0.8, 1)
            Rectangle(pos=(0, 0), size=Window.size)
        
        title_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(140))
        title = Label(text='TarMAR', font_size=dp(48), color=(1, 1, 1, 1), bold=True)
        subtitle = Label(text='Мессенджер с реальными чатами', font_size=dp(16), color=(0.8, 0.9, 1, 1))
        title_layout.add_widget(title)
        title_layout.add_widget(subtitle)
        
        input_layout = BoxLayout(orientation='vertical', spacing=dp(20))
        
        self.username = TextInput(
            hint_text='👤 Имя пользователя', size_hint_y=None, height=dp(55),
            background_color=(1, 1, 1, 1), foreground_color=(0.1, 0.1, 0.1, 1),
            padding=dp(15), multiline=False
        )
        
        self.password = TextInput(
            hint_text='🔒 Пароль', password=True, size_hint_y=None, height=dp(55),
            background_color=(1, 1, 1, 1), foreground_color=(0.1, 0.1, 0.1, 1),
            padding=dp(15), multiline=False
        )
        
        button_layout = BoxLayout(orientation='vertical', spacing=dp(15))
        
        login_btn = RoundedButton(text='ВОЙТИ', size_hint_y=None, height=dp(55), font_size=dp(18), bold=True)
        register_btn = Button(text='Создать аккаунт', size_hint_y=None, height=dp(45), background_color=(0, 0, 0, 0), color=(1, 1, 1, 1), font_size=dp(14))
        
        login_btn.bind(on_press=self.login)
        register_btn.bind(on_press=self.register)
        
        input_layout.add_widget(self.username)
        input_layout.add_widget(self.password)
        button_layout.add_widget(login_btn)
        button_layout.add_widget(register_btn)
        
        main_layout.add_widget(title_layout)
        main_layout.add_widget(input_layout)
        main_layout.add_widget(button_layout)
        
        self.add_widget(main_layout)
    
    def login(self, instance):
        username = self.username.text.strip()
        password = self.password.text.strip()
        
        if not username or not password:
            self.show_error("Заполните все поля")
            return
        
        try:
            # ЗАМЕНИЛ localhost НА SERVER_URL
            response = requests.post(f"{SERVER_URL}/login", json={"username": username, "password": password})
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    app = App.get_running_app()
                    app.current_user = result["username"]
                    app.user_id = result["user_id"]
                    self.show_success("Вход выполнен!")
                    Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'contacts'), 1)
                else:
                    self.show_error(result.get("message", "Ошибка входа"))
            else:
                self.show_error("Ошибка сервера")
                
        except Exception as e:
            self.show_error("Сервер недоступен")
    
    def register(self, instance):
        username = self.username.text.strip()
        password = self.password.text.strip()
        
        if not username or not password:
            self.show_error("Заполните все поля")
            return
        
        try:
            # ЗАМЕНИЛ localhost НА SERVER_URL
            response = requests.post(f"{SERVER_URL}/register", json={"username": username, "password": password})
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    self.show_success("Регистрация успешна!")
                else:
                    self.show_error(result.get("message", "Ошибка регистрации"))
            else:
                self.show_error("Ошибка сервера")
                
        except Exception as e:
            self.show_error("Сервер недоступен")
    
    def show_success(self, message):
        self.show_popup("Успех", message, (0.2, 0.7, 0.3, 1))
    
    def show_error(self, message):
        self.show_popup("Ошибка", message, (0.9, 0.2, 0.2, 1))
    
    def show_popup(self, title, message, color):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        content.add_widget(Label(text=message, color=(0.1, 0.1, 0.1, 1)))
        btn = Button(text='OK', size_hint_y=None, height=dp(45), background_color=color)
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        popup.open()

class ContactsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        
        with self.layout.canvas.before:
            Color(0.1, 0.3, 0.8, 1)
            Rectangle(pos=(0, 0), size=Window.size)
        
        # Заголовок
        header = BoxLayout(size_hint_y=None, height=dp(80), padding=dp(15))
        with header.canvas.before:
            Color(0.2, 0.5, 0.9, 1)
            Rectangle(pos=header.pos, size=header.size)
        
        title = Label(text='Контакты', font_size=dp(22), color=(1, 1, 1, 1), bold=True)
        
        header_buttons = BoxLayout(size_hint_x=None, width=dp(110), spacing=dp(5))
        search_btn = Button(text='🔍', size_hint_x=None, width=dp(50), background_color=(0.3, 0.6, 1, 1), color=(1, 1, 1, 1))
        settings_btn = Button(text='⚙', size_hint_x=None, width=dp(50), background_color=(0.3, 0.6, 1, 1), color=(1, 1, 1, 1))
        
        search_btn.bind(on_press=self.search_users)
        settings_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'settings'))
        
        header_buttons.add_widget(search_btn)
        header_buttons.add_widget(settings_btn)
        header.add_widget(title)
        header.add_widget(header_buttons)
        
        # Список контактов - ПРОСТОЙ И ПОНЯТНЫЙ
        self.contacts_layout = GridLayout(cols=1, spacing=dp(5), size_hint_y=None, padding=dp(10))
        self.contacts_layout.bind(minimum_height=self.contacts_layout.setter('height'))
        
        self.scroll = ScrollView()
        self.scroll.add_widget(self.contacts_layout)
        
        self.layout.add_widget(header)
        self.layout.add_widget(self.scroll)
        self.add_widget(self.layout)
    
    def on_enter(self):
        self.load_contacts()
    
    def load_contacts(self):
        self.contacts_layout.clear_widgets()
        try:
            app = App.get_running_app()
            # ЗАМЕНИЛ localhost НА SERVER_URL
            response = requests.get(f"{SERVER_URL}/chats/{app.current_user}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    chats = result["chats"]
                    
                    if chats:
                        for chat in chats:
                            user_data = chat["user"]
                            # ПРОСТО ИМЯ ПОЛЬЗОВАТЕЛЯ
                            self.add_contact_card(user_data["username"])
                    else:
                        no_chats = Label(
                            text="Нет чатов\nНачните общение!",
                            color=(1, 1, 1, 1), 
                            font_size=dp(18),
                            size_hint_y=None,
                            height=dp(100)
                        )
                        self.contacts_layout.add_widget(no_chats)
                else:
                    self.show_error("Ошибка загрузки")
            else:
                self.show_error("Ошибка сервера")
                
        except Exception as e:
            self.show_error("Ошибка подключения")
    
    def add_contact_card(self, username):
        # ПРОСТАЯ КНОПКА С ИМЕНЕМ
        btn = Button(
            text=username,
            size_hint_y=None,
            height=dp(70),
            background_color=(1, 1, 1, 1),
            color=(0.1, 0.1, 0.1, 1),
            font_size=dp(18),
            bold=True
        )
        
        btn.bind(on_press=lambda x: self.open_chat({"username": username}))
        self.contacts_layout.add_widget(btn)
    
    def search_users(self, instance):
        self.manager.current = 'search'
    
    def open_chat(self, user_data):
        app = App.get_running_app()
        app.current_chat = user_data
        self.manager.current = 'chat'
    
    def show_error(self, message):
        error_label = Label(
            text=message,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(60),
            font_size=dp(16)
        )
        self.contacts_layout.add_widget(error_label)

class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        with layout.canvas.before:
            Color(0.1, 0.3, 0.8, 1)
            Rectangle(pos=(0, 0), size=Window.size)
        
        # Заголовок
        header = BoxLayout(size_hint_y=None, height=dp(80), padding=dp(15))
        with header.canvas.before:
            Color(0.2, 0.5, 0.9, 1)
            Rectangle(pos=header.pos, size=header.size)
        
        back_btn = Button(text='←', size_hint_x=None, width=dp(50), background_color=(0.3, 0.6, 1, 1), color=(1, 1, 1, 1))
        title = Label(text='Поиск пользователей', font_size=dp(20), color=(1, 1, 1, 1), bold=True)
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'contacts'))
        header.add_widget(back_btn)
        header.add_widget(title)
        
        # Поиск
        search_layout = BoxLayout(size_hint_y=None, height=dp(70), padding=dp(15), spacing=dp(10))
        self.search_input = TextInput(
            hint_text='Введите имя пользователя...', multiline=False, size_hint_x=0.7,
            background_color=(1, 1, 1, 1), foreground_color=(0.1, 0.1, 0.1, 1)
        )
        search_btn = RoundedButton(text='Найти', size_hint_x=0.3, size_hint_y=None, height=dp(50))
        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_btn)
        
        # Результаты - ПРОСТЫЕ И ПОНЯТНЫЕ
        self.results_layout = GridLayout(cols=1, spacing=dp(5), size_hint_y=None, padding=dp(10))
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        
        scroll = ScrollView()
        scroll.add_widget(self.results_layout)
        
        layout.add_widget(header)
        layout.add_widget(search_layout)
        layout.add_widget(scroll)
        
        search_btn.bind(on_press=self.perform_search)
        self.search_input.bind(on_text_validate=self.perform_search)
        self.add_widget(layout)
    
    def perform_search(self, instance):
        username = self.search_input.text.strip()
        if not username:
            return
        
        self.results_layout.clear_widgets()
        
        try:
            # ЗАМЕНИЛ localhost НА SERVER_URL
            response = requests.get(f"{SERVER_URL}/search/{username}")
            if response.status_code == 200:
                result = response.json()
                
                if result.get("users"):
                    for user in result["users"]:
                        # ПРОСТО ИМЯ ПОЛЬЗОВАТЕЛЯ
                        self.add_user_result(user["username"])
                else:
                    no_results = Label(
                        text="Пользователи не найдены", 
                        color=(1, 1, 1, 1), 
                        size_hint_y=None, 
                        height=dp(50),
                        font_size=dp(16)
                    )
                    self.results_layout.add_widget(no_results)
            else:
                self.show_error("Ошибка поиска")
                
        except Exception as e:
            self.show_error("Ошибка подключения")
    
    def add_user_result(self, username):
        # ПРОСТАЯ КНОПКА С ИМЕНЕМ
        btn = Button(
            text=username,
            size_hint_y=None, 
            height=dp(70), 
            background_color=(1, 1, 1, 1),
            color=(0.1, 0.1, 0.1, 1),
            font_size=dp(18),
            bold=True
        )
        
        btn.bind(on_press=lambda x: self.open_chat({"username": username}))
        self.results_layout.add_widget(btn)
    
    def open_chat(self, user):
        app = App.get_running_app()
        app.current_chat = user
        self.manager.current = 'chat'
    
    def show_error(self, message):
        error_label = Label(
            text=message, 
            color=(1, 1, 1, 1), 
            size_hint_y=None, 
            height=dp(50),
            font_size=dp(16)
        )
        self.results_layout.add_widget(error_label)

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = None
        self.messages_layout = None
        self.message_input = None
        
    def on_enter(self):
        self.clear_widgets()
        self.build_chat_interface()
        self.load_messages()
    
    def build_chat_interface(self):
        self.layout = BoxLayout(orientation='vertical')
        
        with self.layout.canvas.before:
            Color(0.1, 0.3, 0.8, 1)
            Rectangle(pos=(0, 0), size=Window.size)
        
        app = App.get_running_app()
        chat_user = app.current_chat
        
        # Заголовок чата
        header = BoxLayout(size_hint_y=None, height=dp(80), padding=dp(15))
        with header.canvas.before:
            Color(0.2, 0.5, 0.9, 1)
            Rectangle(pos=header.pos, size=header.size)
        
        back_btn = Button(text='←', size_hint_x=None, width=dp(50), background_color=(0.3, 0.6, 1, 1), color=(1, 1, 1, 1))
        
        user_info = BoxLayout(orientation='vertical')
        username = Label(text=f"Чат с {chat_user['username']}", font_size=dp(18), color=(1, 1, 1, 1), bold=True)
        user_info.add_widget(username)
        
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'contacts'))
        header.add_widget(back_btn)
        header.add_widget(user_info)
        
        # Сообщения - ПРОСТЫЕ И ПОНЯТНЫЕ
        self.messages_layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=dp(15))
        self.messages_layout.bind(minimum_height=self.messages_layout.setter('height'))
        
        messages_scroll = ScrollView()
        messages_scroll.add_widget(self.messages_layout)
        
        # Ввод сообщения
        input_layout = BoxLayout(size_hint_y=None, height=dp(70), padding=dp(10), spacing=dp(10))
        self.message_input = TextInput(
            hint_text='Введите сообщение...', multiline=False, size_hint_x=0.7,
            background_color=(1, 1, 1, 1), foreground_color=(0.1, 0.1, 0.1, 1)
        )
        send_btn = RoundedButton(text='📤', size_hint_x=0.3, size_hint_y=None, height=dp(50))
        
        self.message_input.bind(on_text_validate=self.send_message)
        send_btn.bind(on_press=self.send_message)
        
        input_layout.add_widget(self.message_input)
        input_layout.add_widget(send_btn)
        
        self.layout.add_widget(header)
        self.layout.add_widget(messages_scroll)
        self.layout.add_widget(input_layout)
        
        self.add_widget(self.layout)
    
    def load_messages(self):
        if not self.messages_layout:
            return
            
        self.messages_layout.clear_widgets()
        
        try:
            app = App.get_running_app()
            current_user = app.current_user
            chat_user = app.current_chat
            
            # ЗАМЕНИЛ localhost НА SERVER_URL
            response = requests.get(f"{SERVER_URL}/messages/{current_user}/{chat_user['username']}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    messages = result["messages"]
                    
                    if messages:
                        for message in messages:
                            self.add_message_to_chat(message)
                    else:
                        self.add_system_message("Нет сообщений. Начните общение!")
                    
                    Clock.schedule_once(self.scroll_to_bottom, 0.1)
                else:
                    self.add_system_message("Ошибка загрузки")
            else:
                self.add_system_message("Ошибка сервера")
                
        except Exception as e:
            self.add_system_message("Ошибка подключения")
    
    def add_message_to_chat(self, message):
        app = App.get_running_app()
        is_my_message = message["sender"] == app.current_user
        
        # ПРОСТОЕ СООБЩЕНИЕ
        message_text = f"{message['sender']}: {message['text']}"
        message_label = Label(
            text=message_text,
            size_hint_y=None,
            height=dp(60),
            color=(1, 1, 1, 1) if is_my_message else (0.1, 0.1, 0.1, 1),
            font_size=dp(16),
            text_size=(Window.width * 0.8, None)
        )
        
        self.messages_layout.add_widget(message_label)
    
    def add_system_message(self, text):
        system_label = Label(
            text=text,
            size_hint_y=None,
            height=dp(40),
            color=(1, 1, 1, 1),
            font_size=dp(16),
            italic=True
        )
        self.messages_layout.add_widget(system_label)
    
    def send_message(self, instance):
        if not self.message_input or not self.message_input.text.strip():
            return
        
        app = App.get_running_app()
        current_user = app.current_user
        chat_user = app.current_chat
        
        try:
            # ЗАМЕНИЛ localhost НА SERVER_URL
            response = requests.post(f"{SERVER_URL}/send_message", 
                                   json={"sender": current_user, "receiver": chat_user["username"], "text": self.message_input.text.strip()})
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    self.message_input.text = ""
                    Clock.schedule_once(lambda dt: self.load_messages(), 0.5)
            else:
                self.show_popup("Ошибка", "Не удалось отправить сообщение")
                
        except Exception as e:
            self.show_popup("Ошибка", "Проверьте подключение к серверу")
    
    def scroll_to_bottom(self, dt):
        if len(self.layout.children) > 1:
            try:
                self.layout.children[1].scroll_y = 0
            except:
                pass
    
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        content.add_widget(Label(text=message, color=(0.1, 0.1, 0.1, 1)))
        btn = Button(text='OK', size_hint_y=None, height=dp(45))
        popup = Popup(title=title, content=content, size_hint=(0.7, 0.3))
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        popup.open()

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        with layout.canvas.before:
            Color(0.1, 0.3, 0.8, 1)
            Rectangle(pos=(0, 0), size=Window.size)
        
        header = BoxLayout(size_hint_y=None, height=dp(80), padding=dp(15))
        with header.canvas.before:
            Color(0.2, 0.5, 0.9, 1)
            Rectangle(pos=header.pos, size=header.size)
        
        back_btn = Button(text='←', size_hint_x=None, width=dp(50), background_color=(0.3, 0.6, 1, 1), color=(1, 1, 1, 1))
        title = Label(text='Настройки', font_size=dp(22), color=(1, 1, 1, 1), bold=True)
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'contacts'))
        header.add_widget(back_btn)
        header.add_widget(title)
        
        content = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20))
        
        # ПРОСТАЯ ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ
        user_info = Label(
            text='',
            font_size=dp(20),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(60)
        )
        self.user_label = user_info
        
        # Кнопка выхода
        logout_btn = Button(
            text='🚪 Выйти', 
            size_hint_y=None, 
            height=dp(55), 
            background_color=(0.9, 0.3, 0.3, 1), 
            color=(1, 1, 1, 1),
            font_size=dp(18)
        )
        
        logout_btn.bind(on_press=self.logout)
        content.add_widget(self.user_label)
        content.add_widget(logout_btn)
        layout.add_widget(header)
        layout.add_widget(content)
        self.add_widget(layout)
    
    def on_enter(self):
        app = App.get_running_app()
        if hasattr(app, 'current_user'):
            self.user_label.text = f"Пользователь: {app.current_user}"
    
    def logout(self, instance):
        app = App.get_running_app()
        app.current_user = None
        app.user_id = None
        app.current_chat = None
        self.manager.current = 'login'

class TarMARApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = None
        self.user_id = None
        self.current_chat = None
    
    def build(self):
        self.title = "TarMAR Messenger"
        
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(ContactsScreen(name='contacts'))
        sm.add_widget(SearchScreen(name='search'))
        sm.add_widget(ChatScreen(name='chat'))
        sm.add_widget(SettingsScreen(name='settings'))
        
        return sm

if __name__ == '__main__':
    TarMARApp().run()