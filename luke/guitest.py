import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def submit():
    user_id = user_id_entry.get()
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()

    # You can perform actions with the user inputs here, such as sending them to your FastAPI backend

    # Create and display a popup window with some contents
    popup_window = tk.Toplevel(root)
    popup_window.title("Anomaly Detection Results")
    popup_window.geometry("800x600")
    
    # Contents of the popup window
    popup_label = ttk.Label(popup_window, text="Anomaly Detection Results", font=('Helvetica', 16), background='black', foreground='white')
    popup_label.pack(pady=10)
    
    # Display the input values
    input_values_label = ttk.Label(popup_window, text=f"User ID: {user_id}\nStart Time: {start_time}\nEnd Time: {end_time}", font=('Helvetica', 14), background='black', foreground='white')
    input_values_label.pack(pady=10)
    
    # Generate sample data for the histogram
    import numpy as np
    data = np.random.normal(size=1000)
    
    # Create a Matplotlib figure and add a histogram
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(data, bins=20, color='blue', alpha=0.7)
    ax.set_xlabel('Value')
    ax.set_ylabel('Frequency')
    ax.set_title('Histogram')
    
    # Embed the Matplotlib figure in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=popup_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    
    # Add a close button to close the popup window
    close_button = ttk.Button(popup_window, text="Close", command=popup_window.destroy, style='TButtonGreen', width=15)
    close_button.pack(pady=10)

def exit_app():
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Anomaly Detector")

# Create a frame with a dark theme for the UI elements
frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, padx=10, pady=10)

# Dark theme settings
style = ttk.Style()
style.configure('TFrame', background='#333')
style.configure('TLabel', background='#333', foreground='white', font=('Helvetica', 14))
style.configure('TEntry', fieldbackground='white', font=('Helvetica', 14))

# Create and place input fields and labels using the grid layout inside the frame
user_id_label = ttk.Label(frame, text="User ID:")
user_id_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

user_id_entry = ttk.Entry(frame)
user_id_entry.grid(row=0, column=1, padx=10, pady=10)

start_time_label = ttk.Label(frame, text="Start Time:")
start_time_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

start_time_entry = ttk.Entry(frame)
start_time_entry.grid(row=1, column=1, padx=10, pady=10)

end_time_label = ttk.Label(frame, text="End Time:")
end_time_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

end_time_entry = ttk.Entry(frame)
end_time_entry.grid(row=2, column=1, padx=10, pady=10)

# Create and place the submit button inside the frame
style.configure('TButton', font=('Helvetica', 14), relief=tk.RAISED, borderwidth=2, foreground='green', background='#333')
submit_button = ttk.Button(frame, text="Submit", command=submit, width=15)
submit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

# Create and place the exit button inside the frame
exit_button = ttk.Button(frame, text="Exit", command=exit_app, width=15)
exit_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
