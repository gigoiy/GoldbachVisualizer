import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import os
import sys
import traceback

'''
Goldbach's Conjecture 3D Visualization

To-Do's:
    - Add dynamic axis
    - Add line toggling
    - Create a GUI
'''

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

def goldbachs_calculation(primelist):
    coords = []
    try:
        # Only generate unique prime pairs (prime1 <= prime2)
        for i in range(len(primelist)):
            prime1 = primelist[i]
            # Start j from i to ensure prime1 <= prime2
            for j in range(i, len(primelist)):
                prime2 = primelist[j]
                y_sum = prime1 + prime2
                # Only include coordinates where the sum is even
                if y_sum % 2 == 0:
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

def main():
    # Get base directory path
    if getattr(sys, 'frozen', False):
        BASE_DIR = sys._MEIPASS
    else:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Define output paths
    csv_dir = os.path.join(BASE_DIR, "assets", "csv")
    plot_dir = os.path.join(BASE_DIR, "assets", "plot")
    csv_path = os.path.join(csv_dir, "goldbach_coords.csv")
    plot_path = os.path.join(plot_dir, "goldbach_plot.html")
    
    try:
        primelimit = input("Enter the prime limit: ")
        primes = sieve_of_eratosthenes(primelimit)
        
        if not primes:
            print("No primes generated. Please check your input value.")
            return
        
        coords = goldbachs_calculation(primes)
        print(f"Generated {len(coords)} unique prime pairs with even sums")
        
        # === 1. Generate Table ===
        df = pd.DataFrame(coords, columns=['X (Prime 1)', 'Y (Sum)', 'Z (Prime 2)'])
        print(df.head(10))  # Preview first 10 rows
        
        # Create directories and save files with error handling
        if not create_directory(csv_dir):
            return
        if not save_dataframe(df, csv_path):
            return
            
        # === 2. Interactive 3D Scatter Plot with Hover Labels ===
        fig = go.Figure()

        # Add scatter points with hover tooltips
        fig.add_trace(go.Scatter3d(
            x=df['X (Prime 1)'],
            y=df['Y (Sum)'],
            z=df['Z (Prime 2)'],
            mode='markers',
            marker=dict(size=3, color='red'),
            text=[f"Prime1: {x}, Sum: {y}, Prime2: {z}" for x, y, z in coords],
            hoverinfo='text'
        ))

        # Add lines (limit each group to a simple pairwise chain)
        for group in shared_factors(coords).values():
            if len(group) > 1:
                for i in range(len(group) - 1):
                    p1 = group[i]
                    p2 = group[i + 1]
                    fig.add_trace(go.Scatter3d(
                        x=[p1[0], p2[0]],
                        y=[p1[1], p2[1]],
                        z=[p1[2], p2[2]],
                        mode='lines',
                        line=dict(color='black', width=1),
                        hoverinfo='none'
                    ))

        # Layout
        fig.update_layout(
            title="Goldbach's Prime Table (Unique Pairs, Even Sums)",
            scene=dict(
                xaxis_title='Prime 1 (X)',
                yaxis_title='Sum (Y)',
                zaxis_title='Prime 2 (Z)'
            ),
            width=900,
            height=700,
            showlegend=False
        )
        
        # Create directories and save plot
        if not create_directory(plot_dir):
            return
        if not save_plot(fig, plot_path):
            return

        # Show plot in browser
        plot(fig)
        
        print("Program completed successfully!")
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        traceback.print_exc()
    finally:
        # Keep console open after completion
        if getattr(sys, 'frozen', False):
            input("Press Enter to exit...")

if __name__ == "__main__":
    main()