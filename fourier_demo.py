import numpy as np
import sys

def generate_sine(t, freq):
    """Generates a sine wave."""
    return np.sin(2 * np.pi * freq * t)

def generate_square(t, freq):
    """Generates a square wave."""
    return np.sign(np.sin(2 * np.pi * freq * t))

def generate_sawtooth(t, freq):
    """Generates a sawtooth wave (ramp up from -1 to 1)."""
    return 2 * ((t * freq) % 1) - 1

def ascii_plot(y_values, title, height=15, width=70):
    """
    Plots a list/array of y_values as an ASCII graph.
    """
    print(f"\n  === {title} ===\n")
    
    min_y = np.min(y_values)
    max_y = np.max(y_values)
    
    # Avoid division by zero if signal is flat
    range_y = max_y - min_y
    if range_y == 0:
        range_y = 1.0
        
    # Initialize grid
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Resample y_values to fit the display width
    # We pick 'width' number of points evenly spaced from the input array
    x_indices = np.linspace(0, len(y_values) - 1, width)
    
    for col_idx, x_idx in enumerate(x_indices):
        val = y_values[int(x_idx)]
        
        # Normalize value to 0..1
        norm_val = (val - min_y) / range_y
        
        # Map to row index (0 is top, height-1 is bottom)
        row_idx = int((height - 1) * (1.0 - norm_val))
        
        # Clamp index to be safe
        row_idx = max(0, min(height - 1, row_idx))
        
        grid[row_idx][col_idx] = '*'
        
    # Print the grid with y-axis labels
    for r in range(height):
        label = "       " # Empty label placeholder
        
        # Add labels for top, middle, and bottom
        if r == 0:
            label = f"{max_y:7.2f}"
        elif r == height - 1:
            label = f"{min_y:7.2f}"
        elif r == height // 2:
            mid_y = (max_y + min_y) / 2
            label = f"{mid_y:7.2f}"
            
        line = "".join(grid[r])
        print(f"{label} |{line}")
        
    # X-axis line
    print(" " * 8 + "+" + "-" * width)

def main():
    # Simulation parameters
    duration = 1.0       # seconds
    sample_rate = 1000   # Hz (samples per second)
    freq = 3.0           # Signal frequency in Hz
    
    # Time vector
    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples, endpoint=False)
    
    while True:
        print("\nFourier Transform Demo")
        print("1. Sine Wave")
        print("2. Square Wave")
        print("3. Sawtooth Wave")
        print("q. Quit")
        
        choice = input("Select waveform: ").strip().lower()
        
        if choice == 'q':
            break
            
        y = None
        name = ""
        
        if choice == '1':
            y = generate_sine(t, freq)
            name = "Sine Wave"
        elif choice == '2':
            y = generate_square(t, freq)
            name = "Square Wave"
        elif choice == '3':
            y = generate_sawtooth(t, freq)
            name = "Sawtooth Wave"
        else:
            print("Invalid selection, please try again.")
            continue
            
        # 1. Plot Time Domain
        ascii_plot(y, f"Time Domain - {name}")
        
        # 2. Compute and Plot Frequency Domain
        fft_vals = np.fft.fft(y)
        fft_mag = np.abs(fft_vals)
        
        # Normalize magnitude (2/N for AC components)
        fft_mag = fft_mag * 2 / num_samples
        
        # Get frequencies
        freqs = np.fft.fftfreq(num_samples, 1/sample_rate)
        
        # Filter for positive frequencies only
        half_n = num_samples // 2
        pos_freqs = freqs[:half_n]
        pos_mag = fft_mag[:half_n]
        
        # Limit frequency range to 0-50Hz for better visualization
        # With high sample rate, the full spectrum is too wide for the ASCII plot
        mask = pos_freqs <= 50
        ascii_plot(pos_mag[mask], f"Frequency Domain - {name} (magnitude)")

if __name__ == "__main__":
    main()