import constants
import sys
import openai
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QTextEdit,
)

openai.api_key = constants.API_KEY


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # create the widgets
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap('logo.png').scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(self.logo_pixmap)
        self.input_label = QLabel('Ask a Real Estate Question:')
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('Type here ...')
        self.answer_label = QLabel('Answer :')
        self.answer_field = QTextEdit()
        self.answer_field.setReadOnly(True)
        self.submit_button = QPushButton('Submit')
        self.submit_button.setStyleSheet(
            """
            QPushButton{
                background-color:#4CAF50;
                border:none;
                color: white;
                padding: 15px 32px ;
                font-size: 18px;
                font-weight:bold;
                border-radius:10 px;
                }
            QPushButton:hover{
                background-color: #3e8e41;
                }
                """
        )

        self.popular_questions_group = QGroupBox('Popular Questions')
        self.popular_questions_layout = QVBoxLayout()
        self.popular_questions = ["How do I find a good real estate agent?",
                                  "What are the most important things to look for when buying a house?",
                                  "How can I get the best mortgage rate?",
                                  # "What is the process for buying a house?",
                                  # "Should I buy a house or rent?",
                                  # "How do I determine how much house I can afford?",
                                  # "What are the most common mistakes to avoid when buying a house?"
                                  ]
        self.question_buttons = []

        # create a layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        # Add Logo
        layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)

        # Add input field
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.submit_button)
        layout.addLayout(input_layout)

        # Add Answer Field
        layout.addWidget(self.answer_label)
        layout.addWidget(self.answer_field)

        # Add the popular questions buttons

        for question in self.popular_questions:
            button = QPushButton(question)
            button.setStyleSheet(
                """
                QPushButton{
                    backgroud-color:#FFFFFF;
                    border:2px solid #00AEFF;
                    color:#00AEFF;
                    padding:10px 20px ;
                    font-size:18px;
                    font-weight:bold;
                    border-radius:5px;
                    }
                QPushButton:hover{
                    background-color:#00AEFF;
                    color:#FFFFFF
                    }"""

            )
            button.clicked.connect(lambda _, q=question: self.input_field.setText(q))
            self.popular_questions_layout.addWidget(button)
            self.question_buttons.append(button)
        self.popular_questions_group.setLayout(self.popular_questions_layout)
        layout.addWidget(self.popular_questions_group)

        # set the layout
        self.setLayout(layout)

        # set the window properties
        self.setWindowTitle('Real Estate Chatbot')
        self.setGeometry(200, 200, 600, 600)

        # Connect the submit button to the function which queries OpenAI's GPT-3
        self.submit_button.clicked.connect(self.get_answer)

    def get_answer(self):
        question = self.input_field.text()

        completion = openai.Completion.create(
            engine="davinci",
            prompt=f'{question}',
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )

        answer = completion.choices[0].text
        self.answer_field.setText(answer)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
