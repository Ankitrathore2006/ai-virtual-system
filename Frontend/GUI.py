from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QStackedWidget, 
                           QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QFrame, QLabel, QSizePolicy, QGraphicsDropShadowEffect, QGraphicsBlurEffect)
from PyQt5.QtGui import (QIcon, QPainter, QMovie, QColor, QTextCharFormat, 
                        QFont, QPixmap, QTextBlockFormat, QLinearGradient, QPalette)
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from dotenv import dotenv_values
import sys
import os


# Create necessary directories if they don't exist
current_dir = os.getcwd()
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
GraphicsDirPath = os.path.join(current_dir, "Frontend", "Graphics")

# Create directories if they don't exist
os.makedirs(TempDirPath, exist_ok=True)
os.makedirs(GraphicsDirPath, exist_ok=True)

# Initialize required data files
required_files = ['Mic.data', 'Status.data', 'Responses.data']
for file in required_files:
    file_path = os.path.join(TempDirPath, file)
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            if file == 'Mic.data':
                f.write("False")
            else:
                f.write("")

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")
old_chat_message = ""

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", 
                     "whose", "whom", "can you", "what's", "where's", "how's"]
    
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + '?'
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + '.'
        else:
            new_query += '.'
    
    return new_query.capitalize()

def SetMicrophoneStatus(Command):
    file_path = os.path.join(TempDirPath, 'Mic.data')
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(Command)

def GetMicrophoneStatus():
    file_path = os.path.join(TempDirPath, 'Mic.data')
    with open(file_path, "r", encoding='utf-8') as file:
        Status = file.read()
    return Status

def SetAssistantStatus(Status):
    file_path = os.path.join(TempDirPath, 'Status.data')
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    file_path = os.path.join(TempDirPath, 'Status.data')
    with open(file_path, "r", encoding='utf-8') as file:
        Status = file.read()
    return Status

def MicButtonInitialed():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")

def GraphicsDirectoryPath(Filename):
    return os.path.join(GraphicsDirPath, Filename)

def TempDirectoryPath(Filename):
    return os.path.join(TempDirPath, Filename)

def ShowTextToScreen(Text):
    file_path = os.path.join(TempDirPath, 'Responses.data')
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(Text)

class ModernButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background: rgba(30, 30, 60, 0.85);
                border: 1.5px solid rgba(0, 255, 255, 0.4);
                border-radius: 22px;
                color: #00fff7;
                font-family: 'Orbitron', 'Segoe UI', sans-serif;
                font-size: 16px;
                font-weight: 600;
                letter-spacing: 2px;
                padding: 12px 26px;
            }
            QPushButton:hover {
                background: rgba(0, 255, 255, 0.15);
                color: #fff;
            }
            QPushButton:pressed {
                background: rgba(0, 255, 255, 0.25);
                color: #0ff;
            }
            QPushButton:disabled {
                background: #1a1a2a;
                border: 2px solid rgba(255, 255, 255, 0.05);
                color: rgba(255, 255, 255, 0.3);
            }
        """)
        # Add enhanced shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 255, 40))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

class ChatSection(QWidget):
    def __init__(self):
        super(ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Create chat text edit with modern styling
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        self.chat_text_edit.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 0.7);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                color: white;
                font-size: 14px;
                padding: 15px;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(255, 255, 255, 0.1);
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.3);
                min-height: 30px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.4);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        
        # Add enhanced shadow effect to chat section
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 255, 50))
        shadow.setOffset(0, 3)
        self.chat_text_edit.setGraphicsEffect(shadow)
        
        layout.addWidget(self.chat_text_edit)
        
        # Create status label with enhanced styling
        self.label = QLabel("")
        self.label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
                font-weight: bold;
                padding: 12px 20px;
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 rgba(26, 26, 46, 0.8),
                    stop: 1 rgba(16, 16, 36, 0.8)
                );
                border-radius: 15px;
                border: 2px solid rgba(255, 255, 255, 0.1);
            }
        """)
        self.label.setAlignment(Qt.AlignCenter)
        
        # Add shadow effect to status label
        label_shadow = QGraphicsDropShadowEffect()
        label_shadow.setBlurRadius(20)
        label_shadow.setColor(QColor(0, 0, 255, 40))
        label_shadow.setOffset(0, 2)
        self.label.setGraphicsEffect(label_shadow)
        
        layout.addWidget(self.label)
        
        # Create container for GIF with modern styling
        gif_container = QFrame()
        gif_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 rgba(26, 26, 46, 0.8),
                    stop: 1 rgba(16, 16, 36, 0.8)
                );
                border-radius: 20px;
                border: 2px solid rgba(255, 255, 255, 0.1);
            }
        """)
        gif_layout = QHBoxLayout(gif_container)
        gif_layout.setContentsMargins(10, 10, 10, 10)
        
        # Add GIF with enhanced styling
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("""
            QLabel {
                background: transparent;
                border: none;
            }
        """)
        gif_path = GraphicsDirectoryPath('Jarvis.gif')
        if os.path.exists(gif_path):
            movie = QMovie(gif_path)
            self.gif_label.setMovie(movie)
            # Adjust GIF size for better visibility
            movie.setScaledSize(QSize(600, 4))  # Increased width and height
            self.gif_label.setAlignment(Qt.AlignCenter)
            movie.start()
        else:
            print(f"Warning: GIF file not found at {gif_path}")
        
        # Add enhanced shadow effect to GIF
        gif_shadow = QGraphicsDropShadowEffect()
        gif_shadow.setBlurRadius(30)
        gif_shadow.setColor(QColor(0, 0, 255, 60))
        gif_shadow.setOffset(0, 3)
        self.gif_label.setGraphicsEffect(gif_shadow)
        
        gif_layout.addWidget(self.gif_label)
        layout.addWidget(gif_container)
        
        # Set modern font
        font = QFont("Segoe UI", 13)
        self.chat_text_edit.setFont(font)
        
        # Setup timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.updateStatus)
        self.timer.start(5)
        
        # Set enhanced background with gradient
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #1a1a2e,
                    stop: 0.5 #16213e,
                    stop: 1 #0f3460
                );
            }
        """)

    def loadMessages(self):
        global old_chat_message
        try:
            with open(TempDirectoryPath('Responses.data'), "r", encoding='utf-8') as file:
                messages = file.read()
                if messages is None or len(messages) <= 1:
                    pass
                elif str(old_chat_message) == str(messages):
                    pass
                else:
                    self.addMessage(message=messages, color='White')
                    old_chat_message = messages
        except Exception as e:
            print(f"Error loading messages: {e}")

    def updateStatus(self):
        try:
            with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
                messages = file.read()
                self.label.setText(messages)
        except Exception as e:
            print(f"Error reading speech recognition text: {e}")

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        format = QTextCharFormat()
        formatm = QTextBlockFormat()
        formatm.setTopMargin(10)
        formatm.setLeftMargin(10)
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.setBlockFormat(formatm)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)

class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        
        # Create main layout with no margins for full-screen GIF
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Create container for full-screen GIF
        gif_container = QFrame()
        gif_container.setStyleSheet("""
            QFrame {
                background: black;
                border: none;
            }
        """)
        gif_layout = QVBoxLayout(gif_container)
        gif_layout.setContentsMargins(0, 0, 0, 0)
        gif_layout.setSpacing(0)
        
        # Create and setup GIF label for full screen
        gif_label = QLabel()
        gif_path = GraphicsDirectoryPath('Jarvis.gif')
        if os.path.exists(gif_path):
            movie = QMovie(gif_path)
            gif_label.setMovie(movie)
            # Set GIF to full screen size
            movie.setScaledSize(QSize(screen_width, screen_height))
            gif_label.setAlignment(Qt.AlignCenter)
            gif_label.setStyleSheet("""
                QLabel {
                    background: transparent;
                    border: none;
                }
            """)
            movie.start()
        else:
            print(f"Warning: GIF file not found at {gif_path}")
        
        # Add shadow effect to GIF
        gif_shadow = QGraphicsDropShadowEffect()
        gif_shadow.setBlurRadius(30)
        gif_shadow.setColor(QColor(0, 0, 255, 60))
        gif_shadow.setOffset(0, 3)
        gif_label.setGraphicsEffect(gif_shadow)
        
        gif_layout.addWidget(gif_label)
        content_layout.addWidget(gif_container)
        
        # Create overlay container for controls
        overlay_container = QFrame()
        overlay_container.setStyleSheet("""
            QFrame {
                background: rgba(0, 0,0, 0.3);
                border: none;
            }
        """)
        overlay_layout = QVBoxLayout(overlay_container)
        overlay_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create and setup icon label with glassy effect
        self.icon_label = QLabel()
        mic_on_path = GraphicsDirectoryPath('Mic_on.png')
        if os.path.exists(mic_on_path):
            pixmap = QPixmap(mic_on_path)
            new_pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.icon_label.setPixmap(new_pixmap)
        else:
            print(f"Warning: Mic icon file not found at {mic_on_path}")
        
        self.icon_label.setFixedSize(150, 150)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 75px;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
        """)
        self.toggled = True
        self.icon_label.mousePressEvent = self.toggle_icon
        
        # Create status label with glassy effect
        self.label = QLabel("")
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 10px 20px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                border: 2px solid rgba(255, 255, 255, 0.2);
                margin: 10px;
            }
        """)
        self.label.setAlignment(Qt.AlignCenter)
        
        # Add widgets to overlay layout
        overlay_layout.addStretch()
        overlay_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        overlay_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        overlay_layout.addStretch()
        
        # Add overlay to main layout
        content_layout.addWidget(overlay_container)
        
        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        
        # Set background with gradient
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #1a1a2e,
                    stop: 0.5 #16213e,
                    stop: 1 #0f3460
                );
            }
        """)
        
        # Setup timer for status updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateStatus)
        self.timer.start(5)

    def updateStatus(self):
        """Update the status label with the current assistant status"""
        try:
            with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
                messages = file.read()
                self.label.setText(messages)
        except Exception as e:
            print(f"Error updating status: {e}")

    def toggle_icon(self, event=None):
        if self.toggled:
            mic_off_path = GraphicsDirectoryPath('Mic_off.png')
            if os.path.exists(mic_off_path):
                self.load_icon(mic_off_path, 60, 60)
            MicButtonInitialed()
        else:
            mic_on_path = GraphicsDirectoryPath('Mic_on.png')
            if os.path.exists(mic_on_path):
                self.load_icon(mic_on_path, 60, 60)
            MicButtonClosed()
        self.toggled = not self.toggled

    def load_icon(self, path, width=60, height=60):
        if os.path.exists(path):
            pixmap = QPixmap(path)
            new_pixmap = pixmap.scaled(width, height)
            self.icon_label.setPixmap(new_pixmap)
        else:
            print(f"Warning: Icon file not found at {path}")

class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        Layout = QVBoxLayout()
        label = QLabel("")
        Layout.addWidget(label)
        chat_section = ChatSection()
        Layout.addWidget(chat_section)
        self.setLayout(Layout)
        self.setStyleSheet("background-color: black;")
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.parent_window = parent
        self.initUI()
        self.current_screen = None
        self.stacked_widget = stacked_widget
        self.draggable = True
        self.offset = None
        
        # Set glassy effect styling for top bar
        self.setStyleSheet("""
            QWidget {
                background: rgba(15, 52, 96, 0.7);
                border-bottom: 2px solid rgba(255, 255, 255, 0.1);
            }
            QWidget::after {
                background: linear-gradient(
                    to bottom,
                    rgba(255, 255, 255, 0.1),
                    rgba(255, 255, 255, 0.05)
                );
            }
            QPushButton {
                background: rgba(42, 42, 74, 0.7);
                border: 2px solid rgba(255, 255, 255, 0.15);
                border-radius: 15px;
                color: white;
                padding: 8px 15px;
                font-size: 14px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background: rgba(58, 58, 90, 0.8);
                border: 2px solid rgba(255, 255, 255, 0.25);
            }
            QPushButton:pressed {
                background: rgba(74, 74, 106, 0.9);
                border: 2px solid rgba(255, 255, 255, 0.35);
            }
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 5px 15px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                border: 2px solid rgba(255, 255, 255, 0.15);
            }
        """)
        
        # Add blur effect to top bar
        # blur_effect = QGraphicsBlurEffect()
        # blur_effect.setBlurRadius(10)
        # self.setGraphicsEffect(blur_effect)

    def initUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)
        
        # Create modern buttons
        home_button = ModernButton(" Home")
        home_icon = QIcon(GraphicsDirectoryPath("Home.png"))
        home_button.setIcon(home_icon)
        
        message_button = ModernButton(" Chat")
        message_icon = QIcon(GraphicsDirectoryPath("Chats.png"))
        message_button.setIcon(message_icon)
        
        minimize_button = ModernButton()
        minimize_icon = QIcon(GraphicsDirectoryPath('Minimize2.png'))
        minimize_button.setIcon(minimize_icon)
        minimize_button.clicked.connect(self.minimizeWindow)
        
        self.maximize_button = ModernButton()
        self.maximize_icon = QIcon(GraphicsDirectoryPath('Maximize.png'))
        self.restore_icon = QIcon(GraphicsDirectoryPath('Minimize.png'))
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.clicked.connect(self.maximizeWindow)
        
        close_button = ModernButton()
        close_icon = QIcon(GraphicsDirectoryPath('Close.png'))
        close_button.setIcon(close_icon)
        close_button.clicked.connect(self.closeWindow)
        close_button.setStyleSheet(close_button.styleSheet() + """
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 0.3);
            }
        """)
        
        # Create title with modern styling
        title_label = QLabel(f" {str(Assistantname).capitalize()} AI ")
        title_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 20px;
                font-weight: bold;
                padding: 5px 15px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
            }
        """)
        
        # Add shadow effect to title
        title_shadow = QGraphicsDropShadowEffect()
        title_shadow.setBlurRadius(15)
        title_shadow.setColor(QColor(0, 0, 0, 100))
        title_shadow.setOffset(0, 0)
        title_label.setGraphicsEffect(title_shadow)
        
        # Connect navigation
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)

    def minimizeWindow(self):
        """Minimize the main window"""
        try:
            if self.parent_window:
                self.parent_window.showMinimized()
        except Exception as e:
            print(f"Error minimizing window: {e}")

    def maximizeWindow(self):
        """Maximize or restore the main window"""
        try:
            if self.parent_window:
                if self.parent_window.isMaximized():
                    self.parent_window.showNormal()
                    self.maximize_button.setIcon(self.restore_icon)
                else:
                    self.parent_window.showMaximized()
                    self.maximize_button.setIcon(self.maximize_icon)
        except Exception as e:
            print(f"Error maximizing window: {e}")

    def closeWindow(self):
        """Close the main window"""
        try:
            if self.parent_window:
                self.parent_window.close()
        except Exception as e:
            print(f"Error closing window: {e}")

    def mousePressEvent(self, event):
        """Handle mouse press events for window dragging"""
        if event.button() == Qt.LeftButton and self.draggable:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        """Handle mouse move events for window dragging"""
        if self.offset is not None and self.draggable:
            self.parent_window.move(self.parent_window.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        """Handle mouse release events"""
        self.offset = None

    def paintEvent(self, event):
        """Paint the top bar background"""
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)

class MainWindow(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.initUI()
        except Exception as e:
            print(f"Error initializing MainWindow: {e}")
            raise

    def initUI(self):
        try:
            # Get screen dimensions
            desktop = QApplication.desktop()
            screen_width = desktop.screenGeometry().width()
            screen_height = desktop.screenGeometry().height()

            # Create stacked widget for managing screens
            self.stacked_widget = QStackedWidget()
            
            # Create and add screens
            self.initial_screen = InitialScreen()
            self.message_screen = MessageScreen()
            
            self.stacked_widget.addWidget(self.initial_screen)
            self.stacked_widget.addWidget(self.message_screen)
            
            # Set window properties
            self.setGeometry(0, 0, screen_width, screen_height)
            self.setStyleSheet("background-color: black;")
            
            # Create and set up top bar
            self.top_bar = CustomTopBar(self, self.stacked_widget)
            self.setMenuWidget(self.top_bar)
            
            # Set central widget
            self.setCentralWidget(self.stacked_widget)
            
            # Initialize window state
            self.is_maximized = False
            
        except Exception as e:
            print(f"Error in initUI: {e}")
            raise

    def minimizeWindow(self):
        try:
            self.showMinimized()
        except Exception as e:
            print(f"Error minimizing window: {e}")

    def maximizeWindow(self):
        try:
            if self.is_maximized:
                self.showNormal()
                self.top_bar.maximize_button.setIcon(self.top_bar.restore_icon)
            else:
                self.showMaximized()
                self.top_bar.maximize_button.setIcon(self.top_bar.maximize_icon)
            self.is_maximized = not self.is_maximized
        except Exception as e:
            print(f"Error maximizing window: {e}")

    def closeWindow(self):
        try:
            self.close()
        except Exception as e:
            print(f"Error closing window: {e}")

def GraphicalUserInterface():
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error in GraphicalUserInterface: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        GraphicalUserInterface()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)