import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, filedialog, StringVar, OptionMenu, Canvas, Frame, ttk, Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataPlotterApp:
    def __init__(self, master):
        self.master = master
        master.title("CBRS Network Data Analysis")
        master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))  # Open in full-screen mode

        self.file_path = StringVar()
        self.file_path.set("No file selected")
        self.graph_type = StringVar()
        self.graph_type.set("scatter")
        self.plot_color = StringVar()
        self.plot_color.set("blue")
        self.page_counter = 1  # Counter for page names

        # Create a Notebook to manage multiple pages
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(side="right", fill="both", expand=True)

        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        main_frame = Frame(self.master, bg="black")
        main_frame.pack(fill="both", expand=True)

        # Left Frame (Buttons)
        left_frame = Frame(main_frame, bg="black")
        left_frame.pack(side="left", fill="y")

        # Widgets Inside Left Frame
        self.label = Label(left_frame, text="Select a CSV file:", font=("Arial", 12), bg="black", fg="white")
        self.label.pack(pady=(20, 10), padx=(20, 0), anchor="w")

        self.button = Button(left_frame, text="Browse", command=self.browse_file, font=("Arial", 12))
        self.button.pack(pady=(0, 10), padx=(20, 0), anchor="w")

        self.file_label = Label(left_frame, textvariable=self.file_path, font=("Arial", 10), wraplength=200, anchor="w", bg="black", fg="white")
        self.file_label.pack(pady=(0, 10), padx=(20, 0), anchor="w")

        self.x_var = StringVar()
        self.y_var = StringVar()

        self.label_x = Label(left_frame, text="X Column:", font=("Arial", 12), bg="black", fg="white")
        self.label_x.pack(pady=(0, 10), padx=(20, 0), anchor="w")

        self.dropdown_x = OptionMenu(left_frame, self.x_var, "")
        self.dropdown_x.pack(pady=(0, 10), padx=(20, 0), anchor="w")

        self.label_y = Label(left_frame, text="Y Column:", font=("Arial", 12), bg="black", fg="white")
        self.label_y.pack(pady=(0, 10), padx=(20, 0), anchor="w")

        self.dropdown_y = OptionMenu(left_frame, self.y_var, "")
        self.dropdown_y.pack(pady=(0, 10), padx=(20, 0), anchor="w")

        self.plot_button = Button(left_frame, text="Plot", command=self.plot_data, font=("Arial", 12))
        self.plot_button.pack(pady=(0, 0), padx=(20, 0), anchor="w")

        # Options for Graph
        self.graph_options_label = Label(left_frame, font=("Arial", 12, "underline"), bg="black", fg="white")
        self.graph_options_label.pack(pady=(20, 10), padx=(20, 0), anchor="w")

        # Graph Type
        self.graph_type_label = Label(left_frame, text="Graph Type:", font=("Arial", 12), bg="black", fg="white")
        self.graph_type_label.pack(pady=(0, 10), padx=(20, 0), anchor="w")

        graph_types = ["scatter", "line"]
        self.graph_type.set(graph_types[0])
        self.graph_type_dropdown = OptionMenu(left_frame, self.graph_type, *graph_types)
        self.graph_type_dropdown.pack(pady=(0, 10), padx=(20, 0), anchor="w")

        # Plot Color
        self.plot_color_label = Label(left_frame, text="Plot Color:", font=("Arial", 12), bg="black", fg="white")
        self.plot_color_label.pack(pady=(0, 20), padx=(20, 0), anchor="w")

        plot_colors = ["blue", "red", "green", "purple", "orange"]
        self.plot_color.set(plot_colors[0])
        self.plot_color_dropdown = OptionMenu(left_frame, self.plot_color, *plot_colors)
        self.plot_color_dropdown.pack(pady=(0, 20), padx=(20, 0), anchor="w")

        # Reset Button
        self.reset_button = Button(left_frame, text="Reset Plot", command=self.reset_graph, font=("Arial", 12))
        self.reset_button.pack(pady=(20, 0), padx=(20, 0), anchor="w")

        # Canvas and Scrollbar
        self.canvas = Canvas(main_frame, borderwidth=0, background="black")
        self.frame = Frame(self.canvas, background="black")

        self.vsb = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.file_path.set(file_path)

        # Update dropdowns with column names
        df = pd.read_csv(file_path)
        columns = df.columns.tolist()

        self.x_var.set("")
        self.y_var.set("")

        menu_x = self.dropdown_x["menu"]
        menu_x.delete(0, "end")
        for column in columns:
            menu_x.add_command(label=column, command=lambda value=column: self.x_var.set(value))

        menu_y = self.dropdown_y["menu"]
        menu_y.delete(0, "end")
        for column in columns:
            menu_y.add_command(label=column, command=lambda value=column: self.y_var.set(value))

    def plot_data(self):
        file_path = self.file_path.get()
        x_column = self.x_var.get()
        y_column = self.y_var.get()
        graph_type = self.graph_type.get()
        plot_color = self.plot_color.get()

        if not file_path or not x_column or not y_column:
            return

        df = pd.read_csv(file_path)

        plt.figure(figsize=(8, 6))

        if graph_type == "scatter":
            plt.scatter(df[x_column], df[y_column], marker='o', color=plot_color)
        elif graph_type == "line":
            plt.plot(df[x_column], df[y_column], marker='o', color=plot_color, linestyle='-', linewidth=2)

        plt.title(f"{graph_type.capitalize()} Plot of {y_column} vs {x_column}")
        plt.xlabel(x_column)
        plt.ylabel(y_column)

        # Create a new page for each plot
        page = ttk.Frame(self.notebook)
        self.notebook.add(page, text=f"Page {self.page_counter}")
        self.page_counter += 1

        # Create a new Canvas for each plot
        canvas = FigureCanvasTkAgg(plt.gcf(), master=page)
        canvas.draw()
        canvas.get_tk_widget().pack(side="right")

    def reset_graph(self):
        # Clear the canvas and reset options to default
        self.frame.destroy()
        self.frame = Frame(self.canvas, background="black")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", tags="self.frame")
        self.graph_type.set("scatter")
        self.plot_color.set("blue")

if __name__ == "__main__":
    root = Tk()
    app = DataPlotterApp(root)
    root.mainloop()
