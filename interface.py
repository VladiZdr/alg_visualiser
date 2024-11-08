import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout,QHBoxLayout, QTextEdit, QPushButton,QMessageBox

class MyWindow(QWidget):
    app = QApplication([])

    main_layout = QHBoxLayout()

    code_layout = QVBoxLayout()
    code_text = QTextEdit()
    values_text = QTextEdit()

    visuals_layout = QVBoxLayout()
    states_layout = QHBoxLayout()
    buttons_layout = QHBoxLayout()

    def __init__(self):
        super().__init__()
        
        #Design
        self.setWindowTitle('Algorithm Visualiser')
        self.resize(1900, 1000)

        #Functionality
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

        self.buttons_layout.addWidget(create_visuals_b)
        self.buttons_layout.addWidget(run_code_b)
        self.buttons_layout.addWidget(update_vals_b)
        self.buttons_layout.addWidget(next_state_b)
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
        

#--------------
def run_app():
    main_window = MyWindow()
    main_window.show()
    main_window.app.exec_()
    sys.exit(0)