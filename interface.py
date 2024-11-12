import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QMessageBox, QLabel, QScrollArea, QGridLayout
import interpreter
import State
import examlpe_codes_for_tests

class MyWindow(QWidget):
    # Initialize a QApplication and layouts used in the GUI
    app = QApplication([])

    main_layout = QHBoxLayout()  # Main layout to hold all UI sections

    code_layout = QVBoxLayout()  # Layout for code input and variable display sections
    code_text = QTextEdit()      # Text edit box for user to enter code
    values_text = QTextEdit()    # Text edit box for displaying variable values

    visuals_layout = QVBoxLayout()  # Layout for state visualization and control buttons
    states_layout = QVBoxLayout()   # Layout specifically for visualizing states
    buttons_layout = QHBoxLayout()  # Layout to hold control buttons

    labels_for_states = []  # List to hold QLabel references for each state display

    def __init__(self):
        super().__init__()
        
        # Configure the main window appearance
        self.setWindowTitle('Algorithm Visualiser')
        self.resize(1900, 1000)
        
        # Styling code input box
        self.code_text.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;  
                color: #f8f8f2;            
                border: 1px solid #4d4d4d; 
                padding: 5px;
            }
        """)
        self.code_text.setFixedSize(900, 450)
        
        # Styling variables display box
        self.values_text.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;  
                color: #f8f8f2;            
                border: 1px solid #4d4d4d; 
                padding: 5px;
            }
        """)
        self.values_text.setFixedSize(900, 450)

        # Creating and connecting buttons to functions
        create_visuals_b = QPushButton("Create visuals", self)
        create_visuals_b.clicked.connect(self.create_vis_fun)

        next_state_b = QPushButton("Next state", self)
        next_state_b.clicked.connect(self.next_step_fun)

        code_syntax_b = QPushButton("Code syntax:", self)
        code_syntax_b.clicked.connect(self.get_instructions_fun)

        # Add placeholders and widgets to layouts
        self.code_text.setPlaceholderText(examlpe_codes_for_tests.Example_Codes().placeholder_t_for_code_segment)
        self.values_text.setPlaceholderText("values")
        
        # Arrange the code layout with code input and values display
        self.code_layout.addWidget(self.code_text)
        self.code_layout.addWidget(self.values_text)

        # Add buttons to the button layout
        self.buttons_layout.addWidget(create_visuals_b)
        self.buttons_layout.addWidget(next_state_b)
        self.buttons_layout.addWidget(code_syntax_b)

        # Add states and button layouts to the visuals layout
        self.visuals_layout.addLayout(self.states_layout)
        self.visuals_layout.addLayout(self.buttons_layout)

        # Arrange all main layouts
        self.main_layout.addLayout(self.code_layout)
        self.main_layout.addLayout(self.visuals_layout)
        
        self.setLayout(self.main_layout)

#--- Functions for Button Actions -------------------------------------------------------------------------------------------------------

    def update_vals_fun(self):
        # Updates the values display text box with current variable values from the interpreter
        displayed_vals = ""
        for val in interpreter.variables_dict:
            displayed_vals += f"{val} = {interpreter.variables_dict[val]}\n"
        self.values_text.setText(displayed_vals)
        return displayed_vals

    def next_step_fun(self):
        # Executes the next step if there are remaining lines 
        if len(interpreter.order_of_execution) <= self.curr_state:
            return
        
        # Execute line at current state
        interpreter.execute_next(
            self.lines[interpreter.order_of_execution[self.curr_state]],
            interpreter.get_level(self.lines[interpreter.order_of_execution[self.curr_state]])
        )
        
        # Update variable display
        self.update_vals_fun()

        # Change the color of the last state
        self.labels_for_states[interpreter.order_of_execution[self.curr_state]].setStyleSheet(
            "background-color: grey; border: 1px solid black; border-radius: 5px;"
        )
        self.curr_state += 1

        # Highlight the current state or end the visualization
        if len(interpreter.order_of_execution) - 1 > self.curr_state:
            self.labels_for_states[interpreter.order_of_execution[self.curr_state]].setStyleSheet(
                "background-color: yellow; border: 1px solid black; border-radius: 5px;"
            )
        else:
            self.values_text.setText(self.values_text.toPlainText() + "\nEND")
            self.labels_for_states[-1].setStyleSheet(
                "background-color: red; border: 1px solid black; border-radius: 5px;"
            )

    def create_vis_fun(self):
        # Prepares visualization states based on code input
        code = self.code_text.toPlainText()
        code = "\n".join([line for line in code.splitlines() if line.strip()])  # Remove empty lines
        if not code:
            return
        
        code += "\nreturn"  # Add a return statement at the end

        # Decode the code for execution order and reset variables
        self.lines = code.splitlines()
        if interpreter.decode_code(code) == "Error: Unsupported operation":
            self.code_text.setText("")
            self.show_unsupported_operation_error()
            return
        interpreter.variables_dict.clear()

        # Clear any previous states in the UI
        self.states = []
        self.labels_for_states = []

        # Remove previous scroll areas in `states_layout`
        for i in reversed(range(self.states_layout.count())):
            widget_to_remove = self.states_layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()

        # Create new states for each line of code
        for i in range(len(self.lines)):
            curr_level = interpreter.get_level(self.lines[i])
            self.states.append(State.State(i, curr_level, i))

        # Initialize scroll area and grid layout for state labels
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        container_widget = QWidget()
        grid_layout = QGridLayout(container_widget)

        # Create QLabel for each state and add to grid layout
        for i, s in enumerate(self.states):
            state = QLabel(self)
            state.setFixedSize(50, 50)
            state.setStyleSheet("background-color: grey; border: 1px solid black; border-radius: 25px;")
            state.setAlignment(Qt.AlignCenter)
            state.setText(str(s.index + 1) if i != len(self.states) - 1 else "END")
            grid_layout.addWidget(state, s.pos_y, s.pos_x)
            self.labels_for_states.append(state)

        # Add container widget to scroll area and configure it
        scroll_area.setWidget(container_widget)
        scroll_area.setFixedHeight(850)
        self.states_layout.addWidget(scroll_area)

        # Set the first state to highlighted yellow
        if self.states:
            self.curr_state = 0
            self.labels_for_states[0].setStyleSheet(
                "background-color: yellow; border: 1px solid black; border-radius: 5px;"
            )

    def get_instructions_fun(self):
        # Displays a message box with code syntax information
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Information")
        msg_box.setText(examlpe_codes_for_tests.Example_Codes().placeholder_t_for_code_segment)
        msg_box.exec_()

    def show_unsupported_operation_error(self):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText("Error: Unsupported operation")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
#---------------------------------------------------------------------------------------------------------------------------------------------------

def run_app():
    # Runs the application
    main_window = MyWindow()
    main_window.show()
    main_window.app.exec_()
    sys.exit(0)
