import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout,QHBoxLayout, QTextEdit, QPushButton,QMessageBox, QLabel
import interpreter

class MyWindow(QWidget):
    app = QApplication([])

    main_layout = QHBoxLayout()

    code_layout = QVBoxLayout()
    code_text = QTextEdit()
    values_text = QTextEdit()

    visuals_layout = QVBoxLayout()
    states_layout = QVBoxLayout()
    buttons_layout = QHBoxLayout()

    states = []

    def __init__(self):
        super().__init__()
        
        #Design
        self.setWindowTitle('Algorithm Visualiser')
        self.resize(1900, 1000)

        #Functionality

        #tmp---------------------------------
        for i in range(5):
            state = QLabel(self)
            state.setFixedSize(50, 50)  # Set size of each indicator
            state.setStyleSheet("background-color: grey; border: 1px solid black; border-radius: 25px;")
            state.setAlignment(Qt.AlignCenter)
            state.setText(str(i + 1))
            self.states.append(state)
            self.states_layout.addWidget(state)
        self.light_up_button = QPushButton("Light Up", self)
        self.light_up_button.clicked.connect(self.light_up_states)

        self.code_text.setText("number = 16\nif number >= 16:\n\tprint(number)")
        #tmp---------------------------------

        run_code_b = QPushButton("Run",self)
        run_code_b.clicked.connect(self.run_code_fun)

        create_visuals_b = QPushButton("Create visuals",self)
        create_visuals_b.clicked.connect(self.create_vis_fun)

        update_vals_b = QPushButton("Update values",self)
        update_vals_b.clicked.connect(self.update_vals_fun)

        next_state_b = QPushButton("Next state",self)
        next_state_b.clicked.connect(self.next_step_fun)

        #Layout
        self.code_text.setPlaceholderText("code")
        self.values_text.setPlaceholderText("values_text")
        self.code_layout.addWidget(self.code_text)
        self.code_layout.addWidget(self.values_text)

        #------------- tmp
        self.buttons_layout.addWidget(self.light_up_button)
        #------------- tmp

        self.buttons_layout.addWidget(create_visuals_b)
        self.buttons_layout.addWidget(run_code_b)
        self.buttons_layout.addWidget(update_vals_b)
        self.buttons_layout.addWidget(next_state_b)

        self.visuals_layout.addLayout(self.states_layout)
        self.visuals_layout.addLayout(self.buttons_layout)

        self.main_layout.addLayout(self.code_layout)
        self.main_layout.addLayout(self.visuals_layout)
        
        self.setLayout(self.main_layout)


    #button functions
    def create_vis_fun(self):
        QMessageBox.information(self, "run_b Clicked", "creating visuals")

    def update_vals_fun(self):
        QMessageBox.information(self, "run_b Clicked", "updating values")
    
    def next_step_fun(self):
        QMessageBox.information(self, "run_b Clicked", "next step transition")

    def run_code_fun(self):
        code_input = self.code_text.toPlainText()
        try:
            exec(code_input)
            QMessageBox.information(self, "run_b Clicked", f"User Input: {code_input}")
        except Exception as e:
            QMessageBox.information(self, "run_b Clicked", f"An error occurred: {e}")
    
    #tmp---------------------------------
    def light_up_states(self):
        # Change the color of each indicator to simulate "lighting up"
        for indicator in self.states:
            indicator.setStyleSheet("background-color: yellow; border: 1px solid black; border-radius: 25px;")    
    #tmp---------------------------------        




#-------------------------------------------------------------------------------------------------------------------------------------
def run_app():
    main_window = MyWindow()
    main_window.show()
    main_window.app.exec_()
    sys.exit(0)