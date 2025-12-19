from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp


COLORS = {
    'bg_primary': (0.95, 0.95, 0.95, 1),  
    'bg_header': (0.1, 0.5, 0.8, 1),      
    'bg_card': (1, 1, 1, 1),              
    'text_primary': (0.2, 0.2, 0.2, 1),   
    'text_secondary': (0.5, 0.5, 0.5, 1), 
    'accent': (0.1, 0.6, 0.9, 1),         
    'success': (0.2, 0.8, 0.4, 1),        
    'warning': (1, 0.6, 0.1, 1),         
    'border': (0.9, 0.9, 0.9, 1),         
}

class DashboardHeader(BoxLayout):
    def __init__(self, **kwargs):  
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(100)
        self.padding = [dp(20), dp(10)]
        
        with self.canvas.before:
            Color(*COLORS['bg_header'])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
      
        title = Label(
            text='STUDENT DASHBOARD',
            font_size=dp(24),
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(40)
        )
        
       
        username = Label(
            text='Welcome, kameliatuz Zahra!',
            font_size=dp(16),
            color=(1, 1, 1, 0.9),
            size_hint_y=None,
            height=dp(30)
        )
        
        self.add_widget(title)
        self.add_widget(username)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class StatsCard(BoxLayout):
    def __init__(self, title, value, color, **kwargs): 
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (1, 1)
        self.padding = [dp(15), dp(15)]
        self.spacing = dp(5)
        
        with self.canvas.before:
            Color(*COLORS['bg_card'])
            self.rect = Rectangle(pos=self.pos, size=self.size)
            Color(*color)
            self.border = Rectangle(pos=self.pos, size=(dp(4), self.height))
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        
        value_label = Label(
            text=str(value),
            font_size=dp(28),
            bold=True,
            color=COLORS['text_primary']
        )
        
       
        title_label = Label(
            text=title,
            font_size=dp(14),
            color=COLORS['text_secondary']
        )
        
        self.add_widget(value_label)
        self.add_widget(title_label)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.border.pos = self.pos
        self.border.size = (dp(4), self.height)

class MenuButton(BoxLayout):
    def __init__(self, text, checked=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = [dp(15), dp(5)]
        self.spacing = dp(10)
        
       
        with self.canvas.before:
            Color(*COLORS['border'])
            self.checkbox_bg = Rectangle(
                pos=(self.x, self.y + self.height/2 - dp(10)), 
                size=(dp(20), dp(20))
            )
            
            if checked:
                Color(*COLORS['accent'])
                self.checkbox_fill = Rectangle(
                    pos=(self.x + dp(4), self.y + self.height/2 - dp(6)), 
                    size=(dp(12), dp(12))
                )
        
        self.label = Label(
            text=text,
            font_size=dp(16),
            color=COLORS['text_primary'],
            halign='left',
            valign='middle'
        )
        self.label.bind(size=self.label.setter('text_size'))
        
        self.add_widget(Widget(size_hint_x=None, width=dp(30)))
        self.add_widget(self.label)
        
        self.bind(pos=self.update_checkbox, size=self.update_checkbox)
    
    def update_checkbox(self, *args):
        self.checkbox_bg.pos = (self.x + dp(10), self.y + self.height/2 - dp(10))
        if hasattr(self, 'checkbox_fill'):
            self.checkbox_fill.pos = (self.x + dp(14), self.y + self.height/2 - dp(6))

class DashboardContent(BoxLayout):
    def __init__(self, **kwargs): 
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(20), dp(20)]
        self.spacing = dp(20)
        
        stats_grid = GridLayout(cols=4, spacing=dp(15), size_hint_y=None, height=dp(100))
        
        stats_grid.add_widget(StatsCard('Total Tugas', '0', COLORS['accent']))
        stats_grid.add_widget(StatsCard('Tugas Pending', '0', COLORS['warning']))
        stats_grid.add_widget(StatsCard('Tugas Selesai', '0', COLORS['success']))
        stats_grid.add_widget(StatsCard('Tugas Mendesak', '0', (0.9, 0.3, 0.3, 1)))
        
        self.add_widget(stats_grid)
        
        menu_label = Label(
            text='Aksi:',
            font_size=dp(18),
            bold=True,
            color=COLORS['text_primary'],
            size_hint_y=None,
            height=dp(30)
        )
        self.add_widget(menu_label)
        
        menu_scroll = ScrollView(size_hint=(1, 1))
        menu_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        menu_layout.bind(minimum_height=menu_layout.setter('height'))
        
        menu_items = [
            ('Tambah Tugas', False),
            ('Lihat Tugas Saya', True),
            ('Cek Deadline', True),
            ('Export Tugas Saya', True),
            ('Refresh', True)
        ]
        
        for text, checked in menu_items:
            menu_btn = MenuButton(text, checked)
            menu_layout.add_widget(menu_btn)
        
        menu_scroll.add_widget(menu_layout)
        self.add_widget(menu_scroll)
        
        footer = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        with footer.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            footer.rect = Rectangle(pos=footer.pos, size=footer.size)
        
        footer.bind(pos=lambda obj, pos: setattr(footer.rect, 'pos', pos),
                   size=lambda obj, size: setattr(footer.rect, 'size', size))
        
        activate_label = Label(
            text='[Activate Windows]\nGo to Settings to activate Windows.',
            font_size=dp(11),
            color=(0.5, 0.5, 0.5, 1),
            halign='center',
            valign='middle'
        )
        activate_label.bind(size=activate_label.setter('text_size'))
        
        footer.add_widget(activate_label)
        self.add_widget(footer)

class StudentDashboard(BoxLayout):
    def __init__(self, **kwargs):  
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
       
        self.header = DashboardHeader()
        self.add_widget(self.header)
        
       
        self.content = DashboardContent()
        self.add_widget(self.content)

class DashboardApp(App):
    def build(self):
        Window.clearcolor = COLORS['bg_primary']
        self.title = 'Student Dashboard'
        return StudentDashboard()

if __name__ == '__main__':  
    DashboardApp().run()