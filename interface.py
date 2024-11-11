import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout,QHBoxLayout, QTextEdit, QPushButton,QMessageBox, QLabel,QScrollArea,QGridLayout
import interpreter
import State
import examlpe_codes_for_tests

class MyWindow(QWidget):
    app = QApplication([])

    main_layout = QHBoxLayout()

    code_layout = QVBoxLayout()
    code_text = QTextEdit()
    values_text = QTextEdit()

    visuals_layout = QVBoxLayout()
    states_layout = QVBoxLayout()
    buttons_layout = QHBoxLayout()

    labels_for_states = []

    def __init__(self):
        super().__init__()
        
        #Design
        self.setWindowTitle('Algorithm Visualiser')
        self.resize(1900, 1000)

        #Functionality
#tmp---------------------------------
        self.code_text.setText(examlpe_codes_for_tests.Example_Codes().code13)
#tmp---------------------------------

        create_visuals_b = QPushButton("Create visuals",self)
        create_visuals_b.clicked.connect(self.create_vis_fun)

        next_state_b = QPushButton("Next state",self)
        next_state_b.clicked.connect(self.next_step_fun)

        #Layout
        self.code_text.setPlaceholderText("code")
        self.values_text.setPlaceholderText("values_text")
        self.code_layout.addWidget(self.code_text)
        self.code_layout.addWidget(self.values_text)

        self.buttons_layout.addWidget(create_visuals_b)
        self.buttons_layout.addWidget(next_state_b)

        self.visuals_layout.addLayout(self.states_layout)
        self.visuals_layout.addLayout(self.buttons_layout)

        self.main_layout.addLayout(self.code_layout)
        self.main_layout.addLayout(self.visuals_layout)
        
        self.setLayout(self.main_layout)


    #button functions
    
    def update_vals_fun(self):
        displayed_vals = "" 
        for val in interpreter.variables_dict:
            displayed_vals += val + " = " + str(interpreter.variables_dict[val]) + "\n"
        self.values_text.setText(displayed_vals)
        return displayed_vals

    
    def next_step_fun(self):
        #execute line
        interpreter.execute_next(self.lines[interpreter.order_of_execution[self.curr_state]],interpreter.get_level(self.lines[interpreter.order_of_execution[self.curr_state]]))
        self.update_vals_fun()

        #update visuals
        if len(interpreter.order_of_execution) - 1 > self.curr_state + 1:
            self.labels_for_states[interpreter.order_of_execution[self.curr_state]].setStyleSheet("background-color: grey; border: 1px solid black; border-radius: 5px;")
            self.curr_state += 1
            self.labels_for_states[interpreter.order_of_execution[self.curr_state]].setStyleSheet("background-color: yellow; border: 1px solid black; border-radius: 5px;")
        else:
            self.values_text.setText(self.values_text.toPlainText() + "\nEND")
            self.labels_for_states[interpreter.order_of_execution[self.curr_state]].setStyleSheet("background-color: grey; border: 1px solid black; border-radius: 5px;")
            self.labels_for_states[interpreter.order_of_execution[self.curr_state + 1]].setStyleSheet("background-color: red; border: 1px solid black; border-radius: 5px;")

    def run_code_fun(self):
        code_input = self.code_text.toPlainText()
        

    def create_vis_fun(self):
        code = self.code_text.toPlainText()
        interpreter.decode_code(code)
        interpreter.variables_dict.clear()
        self.lines = code.splitlines()

        self.states = []
        for i in range(len(self.lines)):
            curr_level = interpreter.get_level(self.lines[i])
            self.states.append(State.State(i,curr_level,i))
        
            
        # Remove previous scroll areas in self.states_layout, if any
        for i in reversed(range(self.states_layout.count())):
            widget_to_remove = self.states_layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        container_widget = QWidget()
        grid_layout = QGridLayout(container_widget)

        for i, s in enumerate(self.states):
            state = QLabel(self)
            state.setFixedSize(50, 50)
            state.setStyleSheet("background-color: grey; border: 1px solid black; border-radius: 25px;")
            state.setAlignment(Qt.AlignCenter)
            state.setText(str(s.index))
            grid_layout.addWidget(state, s.pos_y, s.pos_x)
            self.labels_for_states.append(state)   

        scroll_area.setWidget(container_widget)
        scroll_area.setFixedHeight(900)

        self.states_layout.addWidget(scroll_area)

        if self.states:
            self.curr_state = 0
            self.labels_for_states[0].setStyleSheet("background-color: yellow; border: 1px solid black; border-radius: 5px;")


        


#-------------------------------------------------------------------------------------------------------------------------------------
def run_app():
    main_window = MyWindow()
    main_window.show()
    main_window.app.exec_()
    sys.exit(0)