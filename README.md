# Algorithm Visualizer

Algorithm Visualizer is a PyQt-based application that allows users to visualize the execution of code and monitor variable changes over time. It is designed as an educational tool for understanding the flow of algorithms and the values of variables at each step.

## Features

- **Code Editor**: Write or paste Python code into the editor for visualization.
- **State Tracking**: Step through each state of execution, observing variable changes.
- **Loop and Condition Handling**: Visualize the logic of loops (`while`, `if`) and their effect on code execution.
- **Scrollable Visualization**: Easily navigate through multiple states in a scrollable area.
- **Syntax Instructions**: View guidance on syntax requirements for the visualizer.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- PyQt5 library (`pip install PyQt5`)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/algorithm-visualizer.git

    Install required dependencies:

pip install -r requirements.txt

Run the application:

    python main.py

Directory Structure

The project’s core components are organized as follows:

    main.py: Initializes and runs the main window.
    interpreter.py: Contains code parsing and execution logic.
    State.py: Manages individual code states.
    example_codes_for_tests.py: Provides example code snippets for quick testing.

Usage

    Launch the application.
    Write or paste Python code in the Code Editor section.
    Press Create Visuals to generate a visualization based on the input code.
    Step through each state using Next State and observe variable updates in the Values section.
    Use the Code Syntax button to view guidance on supported syntax for proper visualization.

Supported Syntax

The visualizer currently supports a subset of Python, including:

    Basic arithmetic operations (+, -, *, /, %)
    Conditional statements (if, while)
    Variable assignment and updating

Example Code

Here’s an example snippet to get started:

x = 10 + 0
y = 5 + 0
while x > 0:
"\tab"x = x - y
return x 

This code will demonstrate a loop decrementing x by y in each iteration.
Limitations

    Syntax: Only supports simple loops, conditionals, and arithmetic operations. Advanced Python syntax is not supported.
    Error Handling: Minimal error handling; unsupported code may result in unexpected behavior.


Acknowledgments

Special thanks to the PyQt and Python communities for providing valuable resources and libraries that make projects like this possible.



