import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from disk_scheduling import DiskScheduler
from page_replacement import PageReplacement

class DiskPageSimulator:
    def __init__(self):
        self.root = ThemedTk(theme="arc")
        self.root.title("Disk Scheduling & Page Replacement Simulator")
        self.root.geometry("1200x800")
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs
        self.disk_frame = ttk.Frame(self.notebook)
        self.page_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.disk_frame, text='Disk Scheduling')
        self.notebook.add(self.page_frame, text='Page Replacement')
        
        self._setup_disk_scheduling_tab()
        self._setup_page_replacement_tab()
        
        # Theme toggle
        self.theme_var = tk.BooleanVar(value=False)
        self.theme_toggle = ttk.Checkbutton(
            self.root,
            text="Dark Mode",
            variable=self.theme_var,
            command=self._toggle_theme
        )
        self.theme_toggle.pack(side='bottom', pady=5)

    def _setup_disk_scheduling_tab(self):
        # Input Frame
        input_frame = ttk.LabelFrame(self.disk_frame, text="Input Parameters")
        input_frame.pack(fill='x', padx=10, pady=5)
        
        # Algorithm selection
        ttk.Label(input_frame, text="Algorithm:").grid(row=0, column=0, padx=5, pady=5)
        self.disk_algo = ttk.Combobox(
            input_frame,
            values=['FCFS', 'SSTF', 'SCAN', 'C-SCAN', 'LOOK', 'C-LOOK']
        )
        self.disk_algo.grid(row=0, column=1, padx=5, pady=5)
        self.disk_algo.set('FCFS')
        
        # Request sequence input
        ttk.Label(input_frame, text="Request Sequence:").grid(row=1, column=0, padx=5, pady=5)
        self.request_sequence = ttk.Entry(input_frame, width=50)
        self.request_sequence.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(input_frame, text="(comma-separated numbers)").grid(row=1, column=2, padx=5, pady=5)
        
        # Initial head position
        ttk.Label(input_frame, text="Initial Head Position:").grid(row=2, column=0, padx=5, pady=5)
        self.head_pos = ttk.Entry(input_frame)
        self.head_pos.grid(row=2, column=1, padx=5, pady=5)
        
        # Total cylinders
        ttk.Label(input_frame, text="Total Cylinders:").grid(row=3, column=0, padx=5, pady=5)
        self.total_cylinders = ttk.Entry(input_frame)
        self.total_cylinders.grid(row=3, column=1, padx=5, pady=5)
        
        # Direction (for SCAN and LOOK)
        ttk.Label(input_frame, text="Direction:").grid(row=4, column=0, padx=5, pady=5)
        self.direction = ttk.Combobox(input_frame, values=['up', 'down'])
        self.direction.grid(row=4, column=1, padx=5, pady=5)
        self.direction.set('up')
        
        # Simulate button
        ttk.Button(
            input_frame,
            text="Simulate",
            command=self._simulate_disk_scheduling
        ).grid(row=5, column=0, columnspan=3, pady=10)
        
        # Results Frame
        self.disk_results_frame = ttk.LabelFrame(self.disk_frame, text="Results")
        self.disk_results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create matplotlib figure for disk scheduling
        self.disk_fig = plt.Figure(figsize=(8, 4))
        self.disk_canvas = FigureCanvasTkAgg(self.disk_fig, self.disk_results_frame)
        self.disk_canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Seek time label
        self.seek_time_label = ttk.Label(self.disk_results_frame, text="Total Seek Time: 0")
        self.seek_time_label.pack(pady=5)

    def _setup_page_replacement_tab(self):
        # Input Frame
        input_frame = ttk.LabelFrame(self.page_frame, text="Input Parameters")
        input_frame.pack(fill='x', padx=10, pady=5)
        
        # Algorithm selection
        ttk.Label(input_frame, text="Algorithm:").grid(row=0, column=0, padx=5, pady=5)
        self.page_algo = ttk.Combobox(
            input_frame,
            values=['FIFO', 'LRU', 'Optimal', 'LFU']
        )
        self.page_algo.grid(row=0, column=1, padx=5, pady=5)
        self.page_algo.set('FIFO')
        
        # Reference string input
        ttk.Label(input_frame, text="Reference String:").grid(row=1, column=0, padx=5, pady=5)
        self.ref_string = ttk.Entry(input_frame, width=50)
        self.ref_string.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(input_frame, text="(comma-separated numbers)").grid(row=1, column=2, padx=5, pady=5)
        
        # Number of frames
        ttk.Label(input_frame, text="Number of Frames:").grid(row=2, column=0, padx=5, pady=5)
        self.num_frames = ttk.Entry(input_frame)
        self.num_frames.grid(row=2, column=1, padx=5, pady=5)
        
        # Simulate button
        ttk.Button(
            input_frame,
            text="Simulate",
            command=self._simulate_page_replacement
        ).grid(row=3, column=0, columnspan=3, pady=10)
        
        # Results Frame
        self.page_results_frame = ttk.LabelFrame(self.page_frame, text="Results")
        self.page_results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create treeview for page replacement visualization
        self.page_tree = ttk.Treeview(self.page_results_frame)
        self.page_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Page faults label
        self.page_faults_label = ttk.Label(self.page_results_frame, text="Total Page Faults: 0")
        self.page_faults_label.pack(pady=5)

    def _validate_input_sequence(self, sequence_str):
        """Validate and convert input sequence string to list of integers."""
        try:
            # Remove any whitespace and split by comma
            sequence = sequence_str.replace(" ", "").split(",")
            # Convert to integers and validate
            return [int(x) for x in sequence if x]  # Skip empty strings
        except ValueError as e:
            raise ValueError("Invalid input sequence. Please enter comma-separated numbers only.")

    def _validate_positive_int(self, value, field_name):
        """Validate and convert a string to positive integer."""
        try:
            num = int(value)
            if num < 0:
                raise ValueError
            return num
        except ValueError:
            raise ValueError(f"Invalid {field_name}. Please enter a positive number.")

    def _simulate_disk_scheduling(self):
        try:
            # Validate request sequence
            requests = self._validate_input_sequence(self.request_sequence.get())
            if not requests:
                raise ValueError("Request sequence cannot be empty")

            # Validate head position
            head = self._validate_positive_int(self.head_pos.get(), "head position")

            # Validate total cylinders
            cylinders = self._validate_positive_int(self.total_cylinders.get(), "total cylinders")

            # Validate head position is within cylinder range
            if head >= cylinders:
                raise ValueError(f"Head position must be less than total cylinders ({cylinders})")

            # Validate requests are within cylinder range
            if max(requests) >= cylinders:
                raise ValueError(f"All requests must be less than total cylinders ({cylinders})")

            algorithm = self.disk_algo.get()
            direction = self.direction.get()

            # Create scheduler instance
            scheduler = DiskScheduler()
            
            # Execute selected algorithm
            if algorithm == 'FCFS':
                sequence, seek_time = scheduler.fcfs(requests, head, cylinders)
            elif algorithm == 'SSTF':
                sequence, seek_time = scheduler.sstf(requests, head, cylinders)
            elif algorithm == 'SCAN':
                sequence, seek_time = scheduler.scan(requests, head, cylinders, direction)
            elif algorithm == 'C-SCAN':
                sequence, seek_time = scheduler.cscan(requests, head, cylinders)
            elif algorithm == 'LOOK':
                sequence, seek_time = scheduler.look(requests, head, cylinders, direction)
            else:  # C-LOOK
                sequence, seek_time = scheduler.clook(requests, head, cylinders)
            
            # Update visualization
            self.disk_fig.clear()
            ax = self.disk_fig.add_subplot(111)
            
            # Plot seek sequence
            x = range(len(sequence))
            ax.plot(x, sequence, 'b-o')
            ax.set_title(f"{algorithm} Disk Scheduling")
            ax.set_xlabel("Request Sequence")
            ax.set_ylabel("Cylinder")
            ax.grid(True)
            
            # Update seek time label
            self.seek_time_label.config(text=f"Total Seek Time: {seek_time}")
            
            self.disk_canvas.draw()
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def _simulate_page_replacement(self):
        try:
            # Validate reference string
            ref_string = self._validate_input_sequence(self.ref_string.get())
            if not ref_string:
                raise ValueError("Reference string cannot be empty")

            # Validate number of frames
            frames = self._validate_positive_int(self.num_frames.get(), "number of frames")
            if frames < 1:
                raise ValueError("Number of frames must be at least 1")

            # Validate all page numbers are non-negative
            if any(page < 0 for page in ref_string):
                raise ValueError("All page numbers must be non-negative")

            algorithm = self.page_algo.get()
            
            # Create page replacement instance
            replacer = PageReplacement()
            
            # Execute selected algorithm
            if algorithm == 'FIFO':
                history, page_faults = replacer.fifo(ref_string, frames)
            elif algorithm == 'LRU':
                history, page_faults = replacer.lru(ref_string, frames)
            elif algorithm == 'Optimal':
                history, page_faults = replacer.optimal(ref_string, frames)
            else:  # LFU
                history, page_faults = replacer.lfu(ref_string, frames)
            
            # Clear previous results
            for item in self.page_tree.get_children():
                self.page_tree.delete(item)
            
            # Configure treeview columns
            self.page_tree['columns'] = ['Step'] + [f'Frame {i+1}' for i in range(frames)] + ['Page']
            self.page_tree.heading('#0', text='')
            self.page_tree.column('#0', width=0)
            
            for col in self.page_tree['columns']:
                self.page_tree.heading(col, text=col)
                self.page_tree.column(col, width=100, anchor='center')
            
            # Populate treeview with results
            for i, frame_state in enumerate(history):
                values = [i+1] + frame_state + [ref_string[i]]
                self.page_tree.insert('', 'end', values=values)
            
            # Update page faults label
            self.page_faults_label.config(text=f"Total Page Faults: {page_faults}")
                
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def _toggle_theme(self):
        if self.theme_var.get():
            self.root.set_theme("equilux")
        else:
            self.root.set_theme("arc")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DiskPageSimulator()
    app.run() 