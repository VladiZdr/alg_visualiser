import sys
from PyQt5.QtCore import Qt
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
        self.code_text.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;  
                color: #f8f8f2;            
                border: 1px solid #4d4d4d; 
                padding: 5px;
                selection-background-color: 
            }
        """)
        self.code_text.setFixedSize(900,450)
        self.values_text.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;  
                color: #f8f8f2;            
                border: 1px solid #4d4d4d; 
                padding: 5px;
                selection-background-color: 
            }
        """)
        self.values_text.setFixedSize(900,450)

        #Functionality

        #tmp 
        #self.code_text.setText(examlpe_codes_for_tests.Example_Codes().code13)

        create_visuals_b = QPushButton("Create visuals",self)
        create_visuals_b.clicked.connect(self.create_vis_fun)

        next_state_b = QPushButton("Next state",self)
        next_state_b.clicked.connect(self.next_step_fun)

        code_synatx_b = QPushButton("Code syntax: ", self)
        code_synatx_b.clicked.connect(self.get_instructions_fun)

        #Layout
        self.code_text.setPlaceholderText(examlpe_codes_for_tests.Example_Codes().placeholder_t_for_code_segment)
        self.values_text.setPlaceholderText("values")
        self.code_layout.addWidget(self.code_text)
        self.code_layout.addWidget(self.values_text)

        self.buttons_layout.addWidget(create_visuals_b)
        self.buttons_layout.addWidget(next_state_b)
        self.buttons_layout.addWidget(code_synatx_b)

        self.visuals_layout.addLayout(self.states_layout)
        self.visuals_layout.addLayout(self.buttons_layout)

        self.main_layout.addLayout(self.code_layout)
        self.main_layout.addLayout(self.visuals_layout)
        
        self.setLayout(self.main_layout)


#---button functions-------------------------------------------------------------------------------------------------------------------------------
    
    def update_vals_fun(self):
        displayed_vals = "" 
        for val in interpreter.variables_dict:
            displayed_vals += val + " = " + str(interpreter.variables_dict[val]) + "\n"
        self.values_text.setText(displayed_vals)
        return displayed_vals

    def next_step_fun(self):
        #execute line if not finished
        if len(interpreter.order_of_execution) <= self.curr_state:
            return
        interpreter.execute_next(self.lines[interpreter.order_of_execution[self.curr_state]], interpreter.get_level(self.lines[interpreter.order_of_execution[self.curr_state]]))
        self.update_vals_fun()
        
        #update visuals
        self.labels_for_states[interpreter.order_of_execution[self.curr_state]].setStyleSheet("background-color: grey; border: 1px solid black; border-radius: 5px;")
        self.curr_state += 1
        
        if len(interpreter.order_of_execution)  > self.curr_state:
            self.labels_for_states[interpreter.order_of_execution[self.curr_state]].setStyleSheet("background-color: yellow; border: 1px solid black; border-radius: 5px;")
        else:
            self.values_text.setText(self.values_text.toPlainText() + "\nEND")
            self.labels_for_states[len(self.labels_for_states) - 1].setStyleSheet("background-color: red; border: 1px solid black; border-radius: 5px;")
    
    def create_vis_fun(self):
        code = self.code_text.toPlainText()
        if code == "":
            return
        code += "\nreturn"
        #decide order of states and clear dictionary so the second execution starts from scratch
        interpreter.decode_code(code)
        interpreter.variables_dict.clear()
        self.lines = code.splitlines()

        #clear states if button has already been pressed
        self.states = []
        self.labels_for_states = []

        #remove previous scroll areas in self.states_layout if any
        for i in reversed(range(self.states_layout.count())):
            widget_to_remove = self.states_layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()

        #create states
        for i in range(len(self.lines)):
            curr_level = interpreter.get_level(self.lines[i])
            self.states.append(State.State(i,curr_level,i))
        
        #grid for states
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        container_widget = QWidget()
        grid_layout = QGridLayout(container_widget)

        #Labels to display each state
        for i, s in enumerate(self.states):
            state = QLabel(self)
            state.setFixedSize(50, 50)
            state.setStyleSheet("background-color: grey; border: 1px solid black; border-radius: 25px;")
            state.setAlignment(Qt.AlignCenter)
            if i != len(self.states):
                state.setText(str(s.index))
            else:
                state.setText("END")
            grid_layout.addWidget(state, s.pos_y, s.pos_x)
            self.labels_for_states.append(state)  

        #add end state 
        end_label = QLabel(self)
        end_label.setFixedSize(50, 50)
        end_label.setStyleSheet("background-color: grey; border: 1px solid black; border-radius: 25px;")
        end_label.setAlignment(Qt.AlignCenter)
        end_label.setText("END")
        grid_layout.addWidget(end_label, len(self.lines) , 0)
        self.labels_for_states[len(self.labels_for_states) - 1] = end_label

        scroll_area.setWidget(container_widget)
        scroll_area.setFixedHeight(800)
        self.states_layout.addWidget(scroll_area)

        #set starting state
        if self.states:
            self.curr_state = 0
            self.labels_for_states[0].setStyleSheet("background-color: yellow; border: 1px solid black; border-radius: 5px;")

    def get_instructions_fun(self):
        msg_box = QMessageBox(self)
        
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Information")
        msg_box.setText(examlpe_codes_for_tests.Example_Codes().placeholder_t_for_code_segment)
        
        
        msg_box.exec_()
        
        


#---------------------------------------------------------------------------------------------------------------------------------------------------
def run_app():
    main_window = MyWindow()
    main_window.show()
    main_window.app.exec_()
    sys.exit(0)