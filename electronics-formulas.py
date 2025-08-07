import customtkinter as ctk
from tkinter import StringVar, DoubleVar, Label, W, E

# Set the appearance mode and default color theme
# 'System' will follow the system's default, but 'Dark' is used for the Win11-like theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- Formula Logic Functions ---

def calculate_ohms_law(voltage_str, current_str, resistance_str):
    """
    Calculates Ohm's Law (V = I * R).
    Takes three string inputs and returns a formatted string result.
    """
    # Convert string inputs to floats, or None if the string is empty
    try:
        V = float(voltage_str) if voltage_str else None
        I = float(current_str) if current_str else None
        R = float(resistance_str) if resistance_str else None
    except ValueError:
        return "Invalid input. Please enter numbers only."

    # Logic to determine which value to calculate
    # Check for cases where two values are provided and one is missing
    if V is not None and I is not None and R is None:
        if I == 0:
            return "Current cannot be zero."
        return f"Resistance (R) = {V / I:.3f} Ω"
    elif V is not None and R is not None and I is None:
        if R == 0:
            return "Resistance cannot be zero."
        return f"Current (I) = {V / R:.3f} A"
    elif I is not None and R is not None and V is None:
        return f"Voltage (V) = {I * R:.3f} V"
    else:
        # Handle cases where too many or too few inputs are given
        return "Enter exactly two values to calculate the third."

def calculate_voltage_divider(vin_str, r1_str, r2_str):
    """
    Calculates the output voltage of a voltage divider.
    Takes three string inputs and returns a formatted string result.
    """
    # Convert string inputs to floats
    try:
        Vin = float(vin_str)
        R1 = float(r1_str)
        R2 = float(r2_str)
    except ValueError:
        return "Invalid input. Please enter numbers only."

    # Check for valid resistor values to avoid division by zero
    if R1 + R2 == 0:
        return "Sum of resistors cannot be zero."

    Vout = Vin * (R2 / (R1 + R2))
    return f"Output Voltage ($V_{{out}}$) = {Vout:.3f} V"

def calculate_parallel_resistance(resistors_str):
    """
    Calculates the total resistance for resistors in parallel.
    Takes a comma-separated string of resistor values.
    """
    resistors = [r.strip() for r in resistors_str.split(',')]
    if not all(r for r in resistors):
        return "Please enter at least two resistor values."
    
    try:
        # Convert string values to floats
        resistor_values = [float(r) for r in resistors]
        if any(r <= 0 for r in resistor_values):
            return "Resistor values must be greater than zero."
        
        # Calculate the sum of reciprocals
        reciprocal_sum = sum(1/r for r in resistor_values)
        
        # Calculate the total resistance
        total_resistance = 1 / reciprocal_sum
        return f"Total Resistance ($R_{{total}}$) = {total_resistance:.3f} Ω"
    except ValueError:
        return "Invalid input. Please enter a comma-separated list of numbers."

# --- GUI Creator Functions for Each Calculator ---

def create_ohms_law_gui(parent_frame):
    """
    Creates and populates the GUI elements for the Ohm's Law calculator.
    """
    # Clear the parent frame first to prepare for the new widgets
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Title
    ctk.CTkLabel(parent_frame, text="Ohm's Law ($V = IR$)", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=10)
    ctk.CTkLabel(parent_frame, text="Enter any two values to calculate the third.", text_color="gray").pack(pady=(0, 20))

    # Variables for input and output
    voltage_var = StringVar(value="")
    current_var = StringVar(value="")
    resistance_var = StringVar(value="")
    result_var = StringVar(value="")

    # Create a frame for the inputs
    input_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    input_frame.pack(pady=10)

    # Input for Voltage (V)
    ctk.CTkLabel(input_frame, text="Voltage (V):").grid(row=0, column=0, sticky=W, padx=10, pady=5)
    ctk.CTkEntry(input_frame, textvariable=voltage_var).grid(row=0, column=1, padx=10, pady=5)

    # Input for Current (I)
    ctk.CTkLabel(input_frame, text="Current (I):").grid(row=1, column=0, sticky=W, padx=10, pady=5)
    ctk.CTkEntry(input_frame, textvariable=current_var).grid(row=1, column=1, padx=10, pady=5)

    # Input for Resistance (R)
    ctk.CTkLabel(input_frame, text="Resistance (R):").grid(row=2, column=0, sticky=W, padx=10, pady=5)
    ctk.CTkEntry(input_frame, textvariable=resistance_var).grid(row=2, column=1, padx=10, pady=5)

    # Function to update the result when inputs change
    def update_result(*args):
        result = calculate_ohms_law(voltage_var.get(), current_var.get(), resistance_var.get())
        result_var.set(result)

    # Trace the input variables to update the result in real-time
    voltage_var.trace_add("write", update_result)
    current_var.trace_add("write", update_result)
    resistance_var.trace_add("write", update_result)

    # Result label
    result_label = ctk.CTkLabel(parent_frame, textvariable=result_var, font=ctk.CTkFont(size=18, weight="bold"))
    result_label.pack(pady=20)


def create_voltage_divider_gui(parent_frame):
    """
    Creates and populates the GUI elements for the Voltage Divider calculator.
    """
    # Clear the parent frame
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Title
    ctk.CTkLabel(parent_frame, text="Voltage Divider", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=10)
    ctk.CTkLabel(parent_frame, text="Calculates $V_{out} = V_{in} \cdot (R_2 / (R_1 + R_2))$", text_color="gray").pack(pady=(0, 20))

    # Variables for input and output
    vin_var = StringVar(value="")
    r1_var = StringVar(value="")
    r2_var = StringVar(value="")
    result_var = StringVar(value="")

    # Create a frame for the inputs
    input_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    input_frame.pack(pady=10)

    # Input for Input Voltage (Vin)
    ctk.CTkLabel(input_frame, text="Input Voltage ($V_{in}$):").grid(row=0, column=0, sticky=W, padx=10, pady=5)
    ctk.CTkEntry(input_frame, textvariable=vin_var).grid(row=0, column=1, padx=10, pady=5)

    # Input for Resistor 1 (R1)
    ctk.CTkLabel(input_frame, text="Resistor 1 ($R_1$):").grid(row=1, column=0, sticky=W, padx=10, pady=5)
    ctk.CTkEntry(input_frame, textvariable=r1_var).grid(row=1, column=1, padx=10, pady=5)

    # Input for Resistor 2 (R2)
    ctk.CTkLabel(input_frame, text="Resistor 2 ($R_2$):").grid(row=2, column=0, sticky=W, padx=10, pady=5)
    ctk.CTkEntry(input_frame, textvariable=r2_var).grid(row=2, column=1, padx=10, pady=5)

    # Function to update the result
    def update_result(*args):
        # Only calculate if all three fields have values
        if vin_var.get() and r1_var.get() and r2_var.get():
            result = calculate_voltage_divider(vin_var.get(), r1_var.get(), r2_var.get())
            result_var.set(result)
        else:
            result_var.set("Enter all three values.")

    # Trace the input variables to update the result in real-time
    vin_var.trace_add("write", update_result)
    r1_var.trace_add("write", update_result)
    r2_var.trace_add("write", update_result)

    # Result label
    result_label = ctk.CTkLabel(parent_frame, textvariable=result_var, font=ctk.CTkFont(size=18, weight="bold"))
    result_label.pack(pady=20)


def create_parallel_resistance_gui(parent_frame):
    """
    Creates and populates the GUI for the Parallel Resistance calculator.
    """
    # Clear the parent frame
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Title
    ctk.CTkLabel(parent_frame, text="Parallel Resistance", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=10)
    ctk.CTkLabel(parent_frame, text="Enter a comma-separated list of resistor values ($R_1, R_2, ...$)", text_color="gray").pack(pady=(0, 20))
    
    resistors_var = StringVar(value="")
    result_var = StringVar(value="")

    # Input frame
    input_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    input_frame.pack(pady=10)

    # Input field for resistor values
    ctk.CTkLabel(input_frame, text="Resistor Values (Ω):").grid(row=0, column=0, sticky=W, padx=10, pady=5)
    ctk.CTkEntry(input_frame, textvariable=resistors_var, width=300).grid(row=0, column=1, padx=10, pady=5)

    # Function to update the result
    def update_result(*args):
        result = calculate_parallel_resistance(resistors_var.get())
        result_var.set(result)

    # Trace the input variable
    resistors_var.trace_add("write", update_result)
    
    # Result label
    result_label = ctk.CTkLabel(parent_frame, textvariable=result_var, font=ctk.CTkFont(size=18, weight="bold"))
    result_label.pack(pady=20)


# --- Application Class ---

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Electronics Calculator")
        self.geometry("800x500")

        # Configure grid for the main window (1 column for sidebar, 1 for content)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main frame for the sidebar/navigation
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Main frame for the calculator content
        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Label for the sidebar title
        ctk.CTkLabel(self.sidebar_frame, text="Calculators", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

        # Dictionary to easily add new calculators
        # The key is the button text, and the value is the function that builds the GUI
        self.CALCULATORS = {
            "Ohm's Law": create_ohms_law_gui,
            "Voltage Divider": create_voltage_divider_gui,
            "Parallel Resistance": create_parallel_resistance_gui,
            # To add a new calculator, just add a new entry here:
            # "New Calculator": create_new_calculator_gui_function,
        }

        # Create buttons for each calculator in the dictionary
        self.create_sidebar_buttons()

        # Display the first calculator by default
        self.show_calculator(self.CALCULATORS["Ohm's Law"])

    def create_sidebar_buttons(self):
        """
        Creates a button for each calculator in the self.CALCULATORS dictionary.
        """
        for name, gui_function in self.CALCULATORS.items():
            button = ctk.CTkButton(
                self.sidebar_frame,
                text=name,
                command=lambda func=gui_function: self.show_calculator(func),
                anchor="w" # Align text to the left
            )
            button.pack(fill="x", padx=10, pady=5)

    def show_calculator(self, gui_function):
        """
        Clears the content frame and displays the GUI for the selected calculator.
        """
        # Call the function to create the GUI within the content frame
        gui_function(self.content_frame)

if __name__ == "__main__":
    app = App()
    app.mainloop()
