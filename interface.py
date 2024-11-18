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
        """Updates the values display text box with current variable values from the interpreter."""
        displayed_vals = self.format_variable_values()
        self.values_text.setText(displayed_vals)
        return displayed_vals

    def format_variable_values(self):
        """Formats the variable values from interpreter to display in the text box."""
        return "\n".join(f"{var} = {val}" for var, val in interpreter.variables_dict.items() if var)

    def next_step_fun(self):
        """Executes the next step in the code visualization if there are remaining lines."""
        if not self.has_remaining_steps():
            return

        # Execute current step
        self.execute_current_step()

        # Update variable display
        self.update_vals_fun()

        # Update visuals to indicate the current state
        self.update_state_visuals()

    def has_remaining_steps(self):
        """Checks if there are any remaining lines to execute."""
        return len(interpreter.order_of_execution) > self.curr_state

    def execute_current_step(self):
        """Executes the code at the current line based on the interpreter's order of execution."""
        line_index = interpreter.order_of_execution[self.curr_state]
        interpreter.execute_next(self.lines[line_index], interpreter.get_level(self.lines[line_index]))

    def update_state_visuals(self):
        """Updates the state visuals by adjusting the colors to indicate progress."""
        # Set previous state to grey
        self.labels_for_states[interpreter.order_of_execution[self.curr_state]].setStyleSheet(
            "background-color: grey; border: 1px solid black; border-radius: 5px;"
        )
        self.curr_state += 1

        # Highlight the new current state or mark the end
        if self.has_remaining_steps():
            self.highlight_current_state()
        else:
            self.mark_end_of_visualization()

    def highlight_current_state(self):
        """Highlights the current state label to indicate it is active."""
        self.labels_for_states[interpreter.order_of_execution[self.curr_state]].setStyleSheet(
            "background-color: yellow; border: 1px solid black; border-radius: 5px;"
        )

    def mark_end_of_visualization(self):
        """Marks the end of the visualization and adds 'END' text to the values display."""
        self.values_text.append("\nEND")
        self.labels_for_states[-1].setStyleSheet(
            "background-color: red; border: 1px solid black; border-radius: 5px;"
        )

    def create_vis_fun(self):
        """Prepares visualization states based on code input."""
        code = self.clean_code_input()
        if not code:
            return

        # Decode code and reset interpreter
        if self.prepare_interpreter(code) == "Error: Unsupported operation":
            self.handle_unsupported_operation()
            return

        # Clear previous visualization and initialize new states
        self.initialize_states()

        # Configure the scroll area and populate with labels for each state
        self.setup_scroll_area()

        # Highlight the starting state
        self.highlight_starting_state()

    def clean_code_input(self):
        """Returns the cleaned code input without empty lines and with an appended 'return'."""
        code = "\n".join(line for line in self.code_text.toPlainText().splitlines() if line.strip())
        return f"{code}\nreturn" if code else ""

    def prepare_interpreter(self, code):
        """Sets up the interpreter with decoded code and clears variables."""
        self.lines = code.splitlines()
        interpreter.decode_code(code)
        interpreter.variables_dict.clear()

    def handle_unsupported_operation(self):
        """Handles unsupported operations by clearing input and showing an error message."""
        self.code_text.setText("")
        self.show_unsupported_operation_error()
        self.get_instructions_fun()

    def initialize_states(self):
        """Clears previous states and initializes new states for visualization."""
        self.states = []
        self.labels_for_states = []

        # Remove any previous scroll areas
        for i in reversed(range(self.states_layout.count())):
            widget_to_remove = self.states_layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()

        # Create states for each line of code
        for i, line in enumerate(self.lines):
            curr_level = interpreter.get_level(line)
            self.states.append(State.State(i, curr_level, i))

    def setup_scroll_area(self):
        """Sets up the scroll area with a grid layout of state labels."""
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        container_widget = QWidget()
        grid_layout = QGridLayout(container_widget)

        # Add labels for each state to the grid layout
        for i, state in enumerate(self.states):
            label = self.create_state_label(i, state)
            grid_layout.addWidget(label, state.pos_y, state.pos_x)
            self.labels_for_states.append(label)

        # Configure scroll area and add to layout
        scroll_area.setWidget(container_widget)
        scroll_area.setFixedHeight(850)
        self.states_layout.addWidget(scroll_area)

    def create_state_label(self, index, state):
        """Creates a QLabel for a specific state in the visualization."""
        label = QLabel(self)
        label.setFixedSize(50, 50)
        label.setStyleSheet("background-color: grey; border: 1px solid black; border-radius: 25px;")
        label.setAlignment(Qt.AlignCenter)
        label.setText(str(state.index + 1) if index != len(self.states) - 1 else "END")
        return label

    def highlight_starting_state(self):
        """Highlights the initial state to indicate the start of the visualization."""
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
