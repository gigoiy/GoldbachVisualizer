import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot

'''
Goldbach's Prime Table Algorithm
'''

def sieve_of_eratosthenes(limit: int):
    primes = []
    is_prime = [True] * (int(limit) + 1)
    is_prime[0:2] = [False, False]  # 0 and 1 are not primes

    for num in range(2, int(int(limit) ** 0.5) + 1):
        if is_prime[num]:
            for multiple in range(num * num, int(limit) + 1, num):
                is_prime[multiple] = False

    for num in range(2, int(limit) + 1):
        if is_prime[num]:
            primes.append(num)

    return primes

def goldbachs_calculation(primelist):
    coords = []
    for i in range(len(primelist)):
        mainprime = primelist[i]
        for j in range(len(primelist)):
            coords.append((mainprime, mainprime + primelist[j], j))
    return coords

def shared_factors(coordinates):
    y_groups = {}  # dictionary to group coordinates by their y-value (sum)

    for coord in coordinates:
        x, y, z = coord
        if y not in y_groups:
            y_groups[y] = []
        y_groups[y].append(coord)

    return y_groups

primelimit = input("Enter the prime limit: ")
primes = sieve_of_eratosthenes(primelimit)
coords = goldbachs_calculation(primes)

# === 1. Generate Table ===
df = pd.DataFrame(coords, columns=['X (Prime 1)', 'Y (Sum)', 'Z (Index of Prime 2)'])
print(df.head(10))  # Preview first 10 rows
df.to_csv("goldbach_coords.csv", index=False)

# === 2. Interactive 3D Scatter Plot with Hover Labels ===
fig = go.Figure()

# Add scatter points with hover tooltips
fig.add_trace(go.Scatter3d(
    x=df['X (Prime 1)'],
    y=df['Y (Sum)'],
    z=df['Z (Index of Prime 2)'],
    mode='markers',
    marker=dict(size=3, color='red'),
    text=[f"X: {x}, Y: {y}, Z: {z}" for x, y, z in coords],
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
    title="Goldbach's Prime Table (Interactive)",
    scene=dict(
        xaxis_title='Prime 1 (X)',
        yaxis_title='Sum (Y)',
        zaxis_title='Index of Prime 2 (Z)'
    ),
    width=900,
    height=700,
    showlegend=False
)

# Show plot in browser
plot(fig)