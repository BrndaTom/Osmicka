import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QStackedWidget,
                             QGridLayout, QLineEdit, QHBoxLayout, QFileDialog, QComboBox)
from PyQt5.QtCore import Qt

class QuizPresentation(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quiz Application")
        self.setGeometry(100, 100, 800, 600)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # Stacked widget to switch between routines
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # Main menu
        self.menu_widget = QWidget()
        self.menu_layout = QVBoxLayout()
        self.menu_widget.setLayout(self.menu_layout)

        self.add_questions_button = QPushButton("Feeder: Add Questions and Multimedia")
        self.add_questions_button.clicked.connect(self.open_add_questions)
        self.menu_layout.addWidget(self.add_questions_button)

        self.start_presentation_button = QPushButton("Presentation: Start Quiz")
        self.start_presentation_button.clicked.connect(self.open_presentation)
        self.menu_layout.addWidget(self.start_presentation_button)

        self.stack.addWidget(self.menu_widget)

        # Add Questions screen (Feeder)
        self.add_questions_widget = QWidget()
        self.add_questions_layout = QVBoxLayout()
        self.add_questions_widget.setLayout(self.add_questions_layout)

        self.section_index = 0
        self.sections = []

        for i in range(8):
            section_widget = QWidget()
            section_layout = QVBoxLayout()
            section_widget.setLayout(section_layout)

            section_label = QLabel(f"Section {i + 1}: Topic Name")
            section_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            section_layout.addWidget(section_label)

            grid_layout = QGridLayout()
            grid_layout.setSpacing(20)  # Ensure even spacing between boxes
            
            # Set column and row stretches for even distribution
            for col in range(3):
                grid_layout.setColumnStretch(col, 1)
            for row in range(2):
                grid_layout.setRowStretch(row, 1)

            # Create question boxes with type selection
            for index in range(6):
                question_box = QWidget()
                question_layout = QVBoxLayout()
                question_box.setLayout(question_layout)

                # Dropdown to select question type
                question_type = QComboBox()
                question_type.addItems(["Audio", "Video", "Picture", "Multiple Choice (ABCD)", "Text"])
                question_layout.addWidget(question_type)

                # Set default type based on box index
                if index == 0:
                    question_type.setCurrentIndex(0)  # Audio
                    self.change_question_type(0, question_layout)
                elif index == 1:
                    question_type.setCurrentIndex(1)  # Video
                elif index == 2:
                    question_type.setCurrentIndex(2)  # Picture
                elif index == 3:
                    question_type.setCurrentIndex(3)  # Multiple Choice
                else:
                    question_type.setCurrentIndex(4)  # Text

                question_type.currentIndexChanged.connect(lambda current_idx, q_layout=question_layout: self.change_question_type(current_idx, q_layout))

                grid_layout.addWidget(question_box, index // 3, index % 3)

            section_layout.addLayout(grid_layout)
            self.sections.append(section_widget)

        self.section_display = QVBoxLayout()
        self.add_questions_layout.addLayout(self.section_display)
        self.section_display.addWidget(self.sections[self.section_index])

        # Navigation Buttons
        nav_buttons_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous Section")
        self.prev_button.clicked.connect(self.prev_section)
        nav_buttons_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Next Section")
        self.next_button.clicked.connect(self.next_section)
        nav_buttons_layout.addWidget(self.next_button)

        self.add_questions_layout.addLayout(nav_buttons_layout)

        self.back_to_menu_button1 = QPushButton("Back to Main Menu")
        self.back_to_menu_button1.clicked.connect(self.back_to_menu)
        self.add_questions_layout.addWidget(self.back_to_menu_button1)

        self.stack.addWidget(self.add_questions_widget)

        # Quiz Presentation screen
        self.presentation_widget = QWidget()
        self.presentation_layout = QVBoxLayout()
        self.presentation_widget.setLayout(self.presentation_layout)

        self.label = QLabel("Welcome to the Quiz!")
        self.label.setAlignment(Qt.AlignCenter)
        self.presentation_layout.addWidget(self.label)

        self.current_slide = 0
        self.slides = [
            {"type": "text", "content": "Welcome to the Quiz!"},
            {"type": "text", "content": "Question 1: What is the capital of France?"},
            {"type": "text", "content": "Answer: Paris"}
        ]

        self.show_slide()

        self.back_to_menu_button2 = QPushButton("Back to Main Menu")
        self.back_to_menu_button2.clicked.connect(self.back_to_menu)
        self.presentation_layout.addWidget(self.back_to_menu_button2)

        self.stack.addWidget(self.presentation_widget)

        self.stack.setCurrentWidget(self.menu_widget)

    def change_question_type(self, current_idx, layout):
        # Clear existing widgets in the layout except the type selector
        while layout.count() > 1:
            item = layout.takeAt(1)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if current_idx == 0:  # Audio
            audio_input = QLineEdit()
            audio_input.setPlaceholderText("Enter Audio URL or File Path")
            layout.addWidget(audio_input)

            browse_button = QPushButton("Browse")
            browse_button.clicked.connect(lambda: self.select_audio_file(audio_input))
            layout.addWidget(browse_button)

    def select_audio_file(self, input_field):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav)")
        if file_path:
            input_field.setText(file_path)

    def prev_section(self):
        if self.section_index > 0:
            self.section_display.itemAt(0).widget().setParent(None)
            self.section_index -= 1
            self.section_display.addWidget(self.sections[self.section_index])

    def next_section(self):
        if self.section_index < len(self.sections) - 1:
            self.section_display.itemAt(0).widget().setParent(None)
            self.section_index += 1
            self.section_display.addWidget(self.sections[self.section_index])

    def open_add_questions(self):
        self.stack.setCurrentWidget(self.add_questions_widget)

    def open_presentation(self):
        self.stack.setCurrentWidget(self.presentation_widget)

    def back_to_menu(self):
        self.stack.setCurrentWidget(self.menu_widget)

    def show_slide(self):
        slide = self.slides[self.current_slide]
        
        if slide["type"] == "text":
            self.label.setText(slide["content"])

    def next_slide(self):
        self.current_slide

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizPresentation()
    window.show()
    sys.exit(app.exec_())
