import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# --- Functions ---
def get_data():
    try:
        data = entry_input.get()
        data_list = [float(x.strip()) for x in data.split(',')]
        if len(data_list) < 2:
            raise ValueError("Enter at least two numbers.")
        return np.array(data_list)
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")
        return None

def display_result(text):
    output_box.config(state='normal')
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, text)
    output_box.config(state='disabled')

def calculate_statistics():
    data = get_data()
    if data is None:
        return

    mean = np.mean(data)
    median = np.median(data)
    mode_result = stats.mode(data, keepdims=False)
    mode = mode_result.mode if mode_result.count > 0 else "No unique mode"
    variance = np.var(data, ddof=1)
    std_dev = np.std(data, ddof=1)
    data_range = np.max(data) - np.min(data)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = data[(data < lower_bound) | (data > upper_bound)]

    z_scores = stats.zscore(data)

    result = f"""
--- Statistical Summary ---
Count: {len(data)}
Mean: {mean:.2f}
Median: {median:.2f}
Mode: {mode}
Variance: {variance:.2f}
Standard Deviation: {std_dev:.2f}
Range: {data_range:.2f}
IQR (Interquartile Range): {iqr:.2f}

--- Z-Scores ---
{np.round(z_scores, 2)}

--- Outliers (using IQR method) ---
{outliers if len(outliers) > 0 else "No outliers detected"}
"""
    display_result(result)

def clear_all():
    entry_input.delete(0, tk.END)
    output_box.config(state='normal')
    output_box.delete(1.0, tk.END)
    output_box.config(state='disabled')

def plot_histogram():
    data = get_data()
    if data is None:
        return
    plt.figure(figsize=(8, 5))
    plt.hist(data, bins='auto', color='skyblue', edgecolor='black')
    plt.title('Histogram of Data')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

def plot_boxplot():
    data = get_data()
    if data is None:
        return
    plt.figure(figsize=(6, 4))
    plt.boxplot(data, vert=False)
    plt.title('Boxplot of Data')
    plt.xlabel('Value')
    plt.grid(True)
    plt.show()

def save_report():
    if output_box.get(1.0, tk.END).strip() == "":
        messagebox.showwarning("Warning", "Nothing to save. Please calculate first.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
                                             title="Save Report As")
    if file_path:
        with open(file_path, "w") as file:
            file.write(output_box.get(1.0, tk.END))
        messagebox.showinfo("Saved", f"Report saved successfully at:\n{file_path}")

# --- GUI Setup ---
root = tk.Tk()
root.title("Statistics Calculator")
root.geometry("850x600")
root.resizable(False, False)

# Input Frame
frame_input = tk.LabelFrame(root, text="Input Data", padx=10, pady=10)
frame_input.pack(padx=20, pady=10, fill='x')

tk.Label(frame_input, text="Enter numbers (comma-separated):", font=("Arial", 12)).pack(anchor="w")
entry_input = tk.Entry(frame_input, width=100, font=("Arial", 12))
entry_input.pack(pady=5)

# Buttons Frame
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Calculate Statistics", command=calculate_statistics, bg="green", fg="white", width=20).grid(row=0, column=0, padx=10)
tk.Button(frame_buttons, text="Clear", command=clear_all, bg="orange", width=10).grid(row=0, column=1, padx=10)
tk.Button(frame_buttons, text="Plot Histogram", command=plot_histogram, bg="blue", fg="white", width=15).grid(row=0, column=2, padx=10)
tk.Button(frame_buttons, text="Plot Boxplot", command=plot_boxplot, bg="red", fg="white", width=15).grid(row=0, column=3, padx=10)
tk.Button(frame_buttons, text="Save Report", command=save_report, bg="gray", fg="white", width=15).grid(row=0, column=4, padx=10)

# Output Frame
frame_output = tk.LabelFrame(root, text="Results", padx=10, pady=10)
frame_output.pack(fill="both", expand=True, padx=20, pady=10)

output_box = tk.Text(frame_output, height=20, font=("Courier New", 12), bg="black", fg="white", wrap="word")
output_box.pack(fill="both", expand=True)
output_box.config(state='disabled')

root.mainloop()
