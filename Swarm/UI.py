import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext 
from math import sin, pi
from Bench_Mark import schwefel_function, bohachevsky_function, ackley_function, himmelblau_function
from GWO_Animated import GWO_animated
from PSO_Animated import PSO_animated

bounds = {
    'bohachevsky_function': [(-100, 100), ([0, 0], 0)],
    'ackley_function': [(-32.768, 32.768), ([0, 0], 0)],
    'schwefel_function': [(-500, 500), ([420.9687, 420.9687], 0)],
    'himmelblau_function': [(-5, 5), ([3, 2], 0), ([-2.805118, 3.131312], 0), ([-3.779310, -3.283186], 0),
                            ([-1.848126, 3.584428], 0)]
}


def generate_output_text(bench_str, best_position, best_value):
    output = "*" * 50 + "\n"
    for i in range(1, len(bounds[bench_str])):
        val = bounds[bench_str]
        output += "Global optimum of x : \n" + str(val[i][0]) + "\n"
        output += "Global optimum of y : \n" + str(val[i][1]) + "\n"
    output += "-" * 50 + "\n"
    output += "Best position: " + str(best_position) + "\n"
    output += "Best value: {:.6f}".format(best_value) + "\n"
    return output

def is_float(s):
    try:
        float(s)
        return True
    except ValueError :
        return False

def submit():
    try:
        n_individuals_str = n_individuals_var.get()
        generations_str = generations_var.get()

        if not n_individuals_str or not generations_str:
            raise ValueError("Values cannot be empty.")

        n_individuals = int(n_individuals_str)
        generations = int(generations_str)

        if n_individuals <= 8 or generations <= 8:
            raise ValueError("Values must be positive numbers greater than 8.")
        bench_str = benchmark_var.get()
        benchmark = globals()[bench_str]

        algorithm = algorithm_var.get()
        bound = bounds[bench_str][0]
        plot = plot_var.get()


        # if(algorithm=="PSO"):
        #     try:
        #           # Get the string value
        #         c1 = float(pos_c1.get())        # Convert to float
        #         c2 = float(pos_c2.get())       # Get the string value
        #     except ValueError as e:
        #         messagebox.showwarning("Invalid Input", str(e)) 
   
        
        if algorithm == "PSO":
            c1 = pos_c1.get()        # Convert to float
            c2 = pos_c2.get()
            pos_w = str(w_entry.get())
            if not c1 or not c2:
                raise ValueError("Values cannot be empty.")
            c1 = float(c1)
            c2 = float(c2)
            if pos_w == 'ldw':
                pos_w = 'ldw'
            elif is_float(pos_w) == True:
                pos_w = float(pos_w)  # Convert to float
            else:
                raise ValueError("Invalid input for pos weight.")       

            if plot == "3D":
                best_position, best_value = PSO_animated(benchmark, bound, n_individuals, generations,
                                                          w=pos_w, c1=c1, c2=c2, plot_3d=1)
            else:
                best_position, best_value = PSO_animated(benchmark, bound, n_individuals, generations,
                                                          w=pos_w, c1=c1, c2=c2, plot_3d=0)
        elif algorithm == "GWO":
            if plot == "3D":
                best_position, best_value = GWO_animated(benchmark, bound, n_individuals, generations, plot_3d=1)
            else:
                best_position, best_value = GWO_animated(benchmark, bound, n_individuals, generations, plot_3d=0)

        output_text.config(state=tk.NORMAL)  # Enable editing temporarily
        output_text.delete(1.0, tk.END)  # Clear previous output
        output_text.insert(tk.END, generate_output_text(bench_str, best_position, best_value))
        output_text.config(state=tk.DISABLED)  # Make it read-only

    except ValueError as e:
        messagebox.showwarning("Invalid Input", str(e))


root = tk.Tk()
root.title("Parameter Optimization Configuration")

# Use a frame to organize the widgets
frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky="nsew")
frame.grid_rowconfigure(6, weight=1)  # Make the text field row expandable
frame.grid_columnconfigure(1, weight=1)  # Make the second column expandable

# Labels
ttk.Label(frame, text="Benchmark :").grid(row=0, column=0, sticky="w", pady=5)
ttk.Label(frame, text="Num of Individuals :").grid(row=1, column=0, sticky="w", pady=5)
ttk.Label(frame, text="Generations :").grid(row=2, column=0, sticky="w", pady=5)
ttk.Label(frame, text="Algorithm:").grid(row=3, column=0, sticky="w", pady=5)
ttk.Label(frame, text="Plot :").grid(row=4, column=0, sticky="w", pady=5)
ttk.Label(frame, text="pos weight :").grid(row=5, column=0, sticky="w", pady=5)
ttk.Label(frame, text="c1 :").grid(row=6, column=0, sticky="w", pady=5)
ttk.Label(frame, text="c2 :").grid(row=7, column=0, sticky="w", pady=5)

# Comboboxes
benchmark_var = tk.StringVar()
benchmark_combobox = ttk.Combobox(frame, textvariable=benchmark_var,
                                  values=["bohachevsky_function", "ackley_function", "schwefel_function",
                                          "himmelblau_function"], width=20, state="readonly")
benchmark_combobox.grid(row=0, column=1, pady=5, padx=5)
benchmark_combobox.set("bohachevsky_function")

# Entries
n_individuals_var = tk.StringVar()
n_individuals_entry = ttk.Entry(frame, textvariable=n_individuals_var, width=23)
n_individuals_entry.grid(row=1, column=1, pady=5, padx=5)

generations_var = tk.StringVar()
generations_entry = ttk.Entry(frame, textvariable=generations_var, width=23)
generations_entry.grid(row=2, column=1, pady=5, padx=5)

algorithm_var = tk.StringVar()
algorithm_combobox = ttk.Combobox(frame, textvariable=algorithm_var, values=["GWO", "PSO"], width=20, state="readonly")
algorithm_combobox.grid(row=3, column=1, pady=5, padx=5)
algorithm_combobox.set("PSO")

def pso_selected(event):
    algo = algorithm_combobox.get()
    if(algo == "GWO"):
        w_entry.config(state="disabled")
        c1_entry.config(state="disabled")
        c2_entry.config(state="disabled")
    else:
        w_entry.config(state="normal")
        c1_entry.config(state="normal")
        c2_entry.config(state="normal")
algorithm_combobox.bind("<<ComboboxSelected>>", pso_selected)



plot_var = tk.StringVar()
plot_combobox = ttk.Combobox(frame, textvariable=plot_var, values=["3D", "Contour"], width=20, state="readonly")
plot_combobox.grid(row=4, column=1, pady=5, padx=5)
plot_combobox.set("3D")

pos_weight = tk.StringVar()
w_entry = ttk.Entry(frame, textvariable=pos_weight, width=23)
w_entry.grid(row=5, column=1, pady=5, padx=5)


pos_c1 = tk.StringVar()
c1_entry = ttk.Entry(frame, textvariable=pos_c1, width=23)
c1_entry.grid(row=6, column=1, pady=5, padx=5)


pos_c2= tk.StringVar()
c2_entry = ttk.Entry(frame, textvariable=pos_c2, width=23)
c2_entry.grid(row=7, column=1, pady=5, padx=5)



# Submit Button
submit_button = ttk.Button(frame, text="Submit", command=submit)
submit_button.grid(row=8, column=0, columnspan=2, pady=10)

# Create text field for output
output_text = scrolledtext.ScrolledText(frame, width=50, height=10, state=tk.DISABLED)
output_text.grid(row=9, column=0, columnspan=3, pady=10, sticky="nsew")
root.resizable(False, False)
root.mainloop()
