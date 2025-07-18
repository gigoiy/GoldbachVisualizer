import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import os
import sys
import traceback
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

'''
Goldbach's Conjecture 3D Visualization with GUI

To-Do's:
    - Implement additional graph mode that has one axis being the numbered place of the prime in the list of primes and another axis the even sums
    - Implement another variable that displays the number of duplicates per even sum
    - Complete axis swapping functionality
'''

# Helper functions remain the same until main()

def create_directory(path):
    """Create directory if it doesn't exist with error handling"""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {path}: {str(e)}")
        return False

def save_dataframe(df, filepath):
    """Save DataFrame to CSV with error handling"""
    try:
        df.to_csv(filepath, index=False)
        print(f"Successfully saved data to {filepath}")
        return True
    except Exception as e:
        print(f"Error saving CSV file: {str(e)}")
        traceback.print_exc()
        return False

def save_plot(fig, filepath):
    """Save Plotly figure to HTML with error handling"""
    try:
        fig.write_html(filepath)
        print(f"Successfully saved plot to {filepath}")
        return True
    except Exception as e:
        print(f"Error saving HTML plot: {str(e)}")
        traceback.print_exc()
        return False

def sieve_of_eratosthenes(limit: int):
    primes = []
    try:
        limit = int(limit)
        if limit < 2:
            return primes
            
        is_prime = [True] * (limit + 1)
        is_prime[0:2] = [False, False]  # 0 and 1 are not primes

        for num in range(2, int(limit ** 0.5) + 1):
            if is_prime[num]:
                for multiple in range(num * num, limit + 1, num):
                    is_prime[multiple] = False

        for num in range(2, limit + 1):
            if is_prime[num]:
                primes.append(num)
    except Exception as e:
        print(f"Error in prime generation: {str(e)}")
        traceback.print_exc()
    
    return primes

def goldbachs_calculation(primelist, max_sum):
    coords = []
    try:
        # Only generate unique prime pairs (prime1 <= prime2)
        for i in range(len(primelist)):
            prime1 = primelist[i]
            # Start j from i to ensure prime1 <= prime2
            for j in range(i, len(primelist)):
                prime2 = primelist[j]
                y_sum = prime1 + prime2
                # Only include coordinates where sum is even and <= max_sum
                if y_sum % 2 == 0 and y_sum <= max_sum:
                    coords.append((prime1, y_sum, prime2))
    except Exception as e:
        print(f"Error in Goldbach calculation: {str(e)}")
        traceback.print_exc()
    return coords

def shared_factors(coordinates):
    y_groups = {}
    try:
        for coord in coordinates:
            x, y, z = coord
            # Only group even sums (should already be filtered, but double-check)
            if y % 2 == 0:
                if y not in y_groups:
                    y_groups[y] = []
                y_groups[y].append(coord)
    except Exception as e:
        print(f"Error in grouping coordinates: {str(e)}")
        traceback.print_exc()
    return y_groups

class GoldbachGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Goldbach Conjecture 3D Visualizer")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Initialize variables
        self.sum_limit = tk.IntVar(value=100)
        self.csv_path = tk.StringVar()
        self.html_path = tk.StringVar()
        self.show_lines = tk.BooleanVar(value=True)
        self.graph_mode = tk.StringVar(value="Standard")
        self.x_axis = tk.StringVar(value="Prime1")
        self.y_axis = tk.StringVar(value="Sum")
        self.z_axis = tk.StringVar(value="Prime2")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for different sections
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Input tab
        input_frame = ttk.Frame(notebook, padding="10")
        notebook.add(input_frame, text="Parameters")
        
        ttk.Label(input_frame, text="Maximum Sum (even number):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.sum_limit, width=10).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(input_frame, text="Graph Mode:").grid(row=1, column=0, sticky=tk.W, pady=5)
        mode_combobox = ttk.Combobox(input_frame, textvariable=self.graph_mode, state="readonly")
        mode_combobox['values'] = ("Standard", "Enhanced", "Prime Density")  # Placeholder for future modes
        mode_combobox.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Visualization options
        ttk.Label(input_frame, text="Visualization Options:").grid(row=2, column=0, sticky=tk.W, pady=10)
        
        ttk.Checkbutton(input_frame, text="Show connection lines", variable=self.show_lines).grid(
            row=3, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Axis controls frame
        axis_frame = ttk.LabelFrame(input_frame, text="Axis Assignment", padding="10")
        axis_frame.grid(row=4, column=0, columnspan=2, sticky=tk.W+tk.E, pady=10)
        
        ttk.Label(axis_frame, text="X Axis:").grid(row=0, column=0, padx=5)
        x_combobox = ttk.Combobox(axis_frame, textvariable=self.x_axis, width=10, state="readonly")
        x_combobox['values'] = ("Prime1", "Sum", "Prime2")
        x_combobox.grid(row=0, column=1, padx=5)
        
        ttk.Label(axis_frame, text="Y Axis:").grid(row=1, column=0, padx=5, pady=5)
        y_combobox = ttk.Combobox(axis_frame, textvariable=self.y_axis, width=10, state="readonly")
        y_combobox['values'] = ("Prime1", "Sum", "Prime2")
        y_combobox.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(axis_frame, text="Z Axis:").grid(row=2, column=0, padx=5)
        z_combobox = ttk.Combobox(axis_frame, textvariable=self.z_axis, width=10, state="readonly")
        z_combobox['values'] = ("Prime1", "Sum", "Prime2")
        z_combobox.grid(row=2, column=1, padx=5)
        
        # Output tab
        output_frame = ttk.Frame(notebook, padding="10")
        notebook.add(output_frame, text="Output")
        
        # File selection buttons
        ttk.Label(output_frame, text="CSV File Path:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(output_frame, textvariable=self.csv_path, width=40).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(output_frame, text="Browse...", command=self.select_csv_path).grid(row=0, column=2, pady=5)
        
        ttk.Label(output_frame, text="Plot File Path:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(output_frame, textvariable=self.html_path, width=40).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(output_frame, text="Browse...", command=self.select_html_path).grid(row=1, column=2, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Generate Visualization", command=self.generate).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save CSV Only", command=self.save_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Plot Only", command=self.save_plot).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=root.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Set default save paths
        self.set_default_paths()
    
    def set_default_paths(self):
        """Set default save paths based on current directory"""
        if getattr(sys, 'frozen', False):
            BASE_DIR = sys._MEIPASS
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        
        default_dir = os.path.join(BASE_DIR, "assets")
        self.csv_path.set(os.path.join(default_dir, "goldbach_coords.csv"))
        self.html_path.set(os.path.join(default_dir, "goldbach_plot.html"))
    
    def select_csv_path(self):
        """Select CSV save path using file dialog"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save CSV File",
            initialfile=os.path.basename(self.csv_path.get())
        )
        if file_path:
            self.csv_path.set(file_path)
    
    def select_html_path(self):
        """Select HTML plot save path using file dialog"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
            title="Save Plot File",
            initialfile=os.path.basename(self.html_path.get())
        )
        if file_path:
            self.html_path.set(file_path)
    
    def save_csv(self):
        """Save the CSV file only"""
        if not hasattr(self, 'df') or self.df is None:
            messagebox.showerror("Error", "No data to save. Please generate visualization first.")
            return
        
        if not create_directory(os.path.dirname(self.csv_path.get())):
            return
        
        if save_dataframe(self.df, self.csv_path.get()):
            self.status_var.set(f"CSV saved to {self.csv_path.get()}")
            messagebox.showinfo("Success", "CSV file saved successfully!")
    
    def save_plot(self):
        """Save the plot only"""
        if not hasattr(self, 'fig') or self.fig is None:
            messagebox.showerror("Error", "No plot to save. Please generate visualization first.")
            return
        
        if not create_directory(os.path.dirname(self.html_path.get())):
            return
        
        if save_plot(self.fig, self.html_path.get()):
            self.status_var.set(f"Plot saved to {self.html_path.get()}")
            messagebox.showinfo("Success", "Plot saved successfully!")
    
    def generate(self):
        """Main function to generate the visualization"""
        try:
            self.status_var.set("Generating primes...")
            self.root.update()
            
            # Get parameters from UI
            sum_limit_val = self.sum_limit.get()
            
            # Generate primes up to the sum limit
            primes = sieve_of_eratosthenes(sum_limit_val)
            
            if not primes:
                messagebox.showerror("Error", "No primes generated. Please check your input value.")
                self.status_var.set("Error: No primes generated")
                return
            
            # Generate Goldbach pairs
            self.status_var.set("Calculating Goldbach pairs...")
            self.root.update()
            coords = goldbachs_calculation(primes, sum_limit_val)
            
            # Create DataFrame
            self.df = pd.DataFrame(coords, columns=['X (Prime 1)', 'Y (Sum)', 'Z (Prime 2)'])
            
            # Save CSV
            if not create_directory(os.path.dirname(self.csv_path.get())):
                return
            if not save_dataframe(self.df, self.csv_path.get()):
                return
            
            # Create visualization
            self.status_var.set("Creating 3D visualization...")
            self.root.update()
            
            # Create figure
            self.fig = go.Figure()

            # Add scatter points with hover tooltips
            self.fig.add_trace(go.Scatter3d(
                x=self.df['X (Prime 1)'],
                y=self.df['Y (Sum)'],
                z=self.df['Z (Prime 2)'],
                mode='markers',
                marker=dict(size=3, color='red'),
                text=[f"Prime1: {x}, Sum: {y}, Prime2: {z}" for x, y, z in coords],
                hoverinfo='text',
                name="Prime Pairs"
            ))

            # Add lines if enabled
            if self.show_lines.get():
                for group in shared_factors(coords).values():
                    if len(group) > 1:
                        for i in range(len(group) - 1):
                            p1 = group[i]
                            p2 = group[i + 1]
                            self.fig.add_trace(go.Scatter3d(
                                x=[p1[0], p2[0]],
                                y=[p1[1], p2[1]],
                                z=[p1[2], p2[2]],
                                mode='lines',
                                line=dict(color='black', width=1),
                                hoverinfo='none',
                                name="Connections"
                            ))

            # Layout
            self.fig.update_layout(
                title=f"Goldbach's Prime Table (Sums ≤ {sum_limit_val})",
                scene=dict(
                    xaxis_title=self.x_axis.get(),
                    yaxis_title=self.y_axis.get(),
                    zaxis_title=self.z_axis.get()
                ),
                width=900,
                height=700,
                showlegend=False
            )
            
            # Save plot
            if not create_directory(os.path.dirname(self.html_path.get())):
                return
            if not save_plot(self.fig, self.html_path.get()):
                return

            # Show plot in browser
            self.status_var.set("Displaying visualization in browser...")
            self.root.update()
            plot(self.fig)
            
            self.status_var.set("Visualization completed successfully!")
            messagebox.showinfo("Success", "Visualization generated and saved successfully!")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            traceback.print_exc()

def main():
    root = tk.Tk()
    app = GoldbachGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()