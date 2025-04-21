import numpy as np
import matplotlib.pyplot as plt
import os

# Try importing 3D plotting support
HAS_3D = False
try:
    from mpl_toolkits.mplot3d import Axes3D
    HAS_3D = True
except ImportError:
    print("Warning: 3D plotting not available, falling back to 2D plots")

# Read the trajectory file
def read_trajectory(filename):
    """
    Reads trajectory data from file
    Format is typically: timestamp tx ty tz qx qy qz qw
    or just: tx ty tz qx qy qz qw
    """
    try:
        # Expand user directory if path contains ~
        filename = os.path.expanduser(filename)
        # Remove any trailing whitespace
        filename = filename.strip()
        data = np.loadtxt(filename)
        print(f"Successfully loaded data with shape {data.shape}")
        return data
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        return None

# Extract trajectory positions from data
def extract_positions(data):
    # Determine position columns based on data shape
    # If 7 columns: tx ty tz qx qy qz qw
    # If 8 columns: timestamp tx ty tz qx qy qz qw
    
    if data.shape[1] >= 7:
        # Determine if first column is timestamp or not
        if data.shape[1] == 8:
            pos_indices = [1, 2, 3]  # tx, ty, tz are at indices 1,2,3
        else:  # 7 columns
            pos_indices = [0, 1, 2]  # tx, ty, tz are at indices 0,1,2
        
        # Extract positions
        x = data[:, pos_indices[0]]
        y = data[:, pos_indices[1]]
        z = data[:, pos_indices[2]]
        
        return x, y, z
    else:
        print("Data format not recognized. Expected at least 7 columns.")
        return None, None, None

# Plot two trajectories on the same plot for direct comparison
def plot_trajectories(data1, label1, data2, label2):
    x1, y1, z1 = extract_positions(data1)
    x2, y2, z2 = extract_positions(data2)
    
    if x1 is None or x2 is None:
        return
    
    # Create a single plot, either 3D or 2D
    fig = plt.figure(figsize=(12, 10))
    
    if HAS_3D:
        # 3D plot with both trajectories
        ax = fig.add_subplot(111, projection='3d')
        
        # First trajectory in blue
        ax.plot(x1, y1, z1, 'b-', linewidth=2, label=f'Trajectory: {label1}')
        ax.scatter(x1[0], y1[0], z1[0], color='cyan', s=100, marker='o', label=f'{label1} Start')
        ax.scatter(x1[-1], y1[-1], z1[-1], color='blue', s=100, marker='s', label=f'{label1} End')
        
        # Second trajectory in red
        ax.plot(x2, y2, z2, 'r-', linewidth=2, label=f'Trajectory: {label2}')
        ax.scatter(x2[0], y2[0], z2[0], color='magenta', s=100, marker='o', label=f'{label2} Start')
        ax.scatter(x2[-1], y2[-1], z2[-1], color='darkred', s=100, marker='s', label=f'{label2} End')
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Trajectory Comparison (3D View)')
    else:
        # 2D plot (top-down view) with both trajectories
        ax = fig.add_subplot(111)
        
        # First trajectory in blue
        ax.plot(x1, y1, 'b-', linewidth=2, label=f'Trajectory: {label1}')
        ax.scatter(x1[0], y1[0], color='cyan', s=100, marker='o', label=f'{label1} Start')
        ax.scatter(x1[-1], y1[-1], color='blue', s=100, marker='s', label=f'{label1} End')
        
        # Second trajectory in red
        ax.plot(x2, y2, 'r-', linewidth=2, label=f'Trajectory: {label2}')
        ax.scatter(x2[0], y2[0], color='magenta', s=100, marker='o', label=f'{label2} Start')
        ax.scatter(x2[-1], y2[-1], color='darkred', s=100, marker='s', label=f'{label2} End')
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Trajectory Comparison (Top-Down View)')
        ax.grid(True)
        ax.axis('equal')
    
    # Add legend with better placement
    ax.legend(loc='best')
    plt.tight_layout()
    plt.show()

# Main function
def main():
    # File paths
    file1 = "/home/yui/Desktop/f_dataset-MH02_mono.txt"  # First trajectory
    file2 = "/home/yui/Desktop/kf_dataset-MH02_mono.txt"  # Second trajectory
    
    # Load data
    data1 = read_trajectory(file1.strip())
    data2 = read_trajectory(file2.strip())
    
    # Plot if both files loaded successfully
    if data1 is not None and data2 is not None:
        plot_trajectories(data1, "Frame Trajectory", data2, "Keyframe Trajectory")
    else:
        print("Failed to load one or both trajectory files")

if __name__ == "__main__":
    main()