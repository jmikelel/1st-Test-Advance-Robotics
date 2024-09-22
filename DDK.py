import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Constants
WHEEL_RADIUS = 0.036  # meters
PPS = 40  # pulses per second
CIRCUMFERENCE = 2 * np.pi * WHEEL_RADIUS  # Circumference of the wheel
PPR_MIN = 16
PPR_MAX = 25

def compute_distance(PPR, elapsed_time):
    RPS = PPS / PPR  # Revolutions per second
    distance = RPS * CIRCUMFERENCE * elapsed_time  # Distance in meters
    return distance

def generate_sensor_readings(size):
    return np.random.uniform(PPR_MIN, PPR_MAX, size)

def display_histograms_and_table(data, distances):
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    # Histogram for PPR values
    ax[0].hist(data, bins=20, edgecolor='black', alpha=0.7, density=True)
    
    mu_ppr, sigma_ppr = np.mean(data), np.std(data)
    best_fit_line_ppr = norm.pdf(np.linspace(PPR_MIN, PPR_MAX, 100), mu_ppr, sigma_ppr)
    ax[0].plot(np.linspace(PPR_MIN, PPR_MAX, 100), best_fit_line_ppr, 'r-', linewidth=2,
               label=f'Normal Dist. (Mean: {mu_ppr:.2f}, σ: {sigma_ppr:.2f})')

    # Shading for ±1σ for PPR
    ax[0].fill_between(np.linspace(PPR_MIN, PPR_MAX, 100), 0, best_fit_line_ppr,
                       where=((np.linspace(PPR_MIN, PPR_MAX, 100) >= mu_ppr - sigma_ppr) & 
                              (np.linspace(PPR_MIN, PPR_MAX, 100) <= mu_ppr + sigma_ppr)),
                       color='yellow', alpha=0.5, label='±1σ Area')

    # Shading for area outside ±1σ for PPR
    ax[0].fill_between(np.linspace(PPR_MIN, PPR_MAX, 100), 0, best_fit_line_ppr,
                       where=((np.linspace(PPR_MIN, PPR_MAX, 100) < mu_ppr - sigma_ppr) | 
                              (np.linspace(PPR_MIN, PPR_MAX, 100) > mu_ppr + sigma_ppr)),
                       color='purple', alpha=0.5, label='Outside ±1σ Area')

    ax[0].axvline(mu_ppr, color='red', linestyle='dashed', linewidth=1.5, label=f'Mean: {mu_ppr:.2f}')
    ax[0].axvline(mu_ppr + sigma_ppr, color='green', linestyle='dashed', linewidth=1.5, label=f'+1σ: {mu_ppr + sigma_ppr:.2f}')
    ax[0].axvline(mu_ppr - sigma_ppr, color='green', linestyle='dashed', linewidth=1.5, label=f'-1σ: {mu_ppr - sigma_ppr:.2f}')
    
    ax[0].set_xlabel('Random PPR Values')
    ax[0].set_ylabel('Frequency')
    ax[0].set_title('Histogram of PPR Values')
    ax[0].legend()

    # Histogram for distance values
    ax[1].hist(distances, bins=20, edgecolor='black', alpha=0.7, density=True)
    
    mu_distance, sigma_distance = np.mean(distances), np.std(distances)
    best_fit_line_distance = norm.pdf(np.linspace(min(distances), max(distances), 100), mu_distance, sigma_distance)
    ax[1].plot(np.linspace(min(distances), max(distances), 100), best_fit_line_distance, 'r-', linewidth=2,
               label=f'Normal Dist. (Mean: {mu_distance:.2f}, σ: {sigma_distance:.2f})')

    # Shading for ±1σ for distance
    ax[1].fill_between(np.linspace(min(distances), max(distances), 100), 0, best_fit_line_distance,
                       where=((np.linspace(min(distances), max(distances), 100) >= mu_distance - sigma_distance) & 
                              (np.linspace(min(distances), max(distances), 100) <= mu_distance + sigma_distance)),
                       color='yellow', alpha=0.5, label='±1σ Area')

    # Shading for area outside ±1σ for distance
    ax[1].fill_between(np.linspace(min(distances), max(distances), 100), 0, best_fit_line_distance,
                       where=((np.linspace(min(distances), max(distances), 100) < mu_distance - sigma_distance) | 
                              (np.linspace(min(distances), max(distances), 100) > mu_distance + sigma_distance)),
                       color='purple', alpha=0.5, label='Outside ±1σ Area')

    ax[1].axvline(mu_distance, color='red', linestyle='dashed', linewidth=1.5, label=f'Mean: {mu_distance:.2f}')
    ax[1].axvline(mu_distance + sigma_distance, color='green', linestyle='dashed', linewidth=1.5, label=f'+1σ: {mu_distance + sigma_distance:.2f}')
    ax[1].axvline(mu_distance - sigma_distance, color='green', linestyle='dashed', linewidth=1.5, label=f'-1σ: {mu_distance - sigma_distance:.2f}')
    
    ax[1].set_xlabel('Distance (meters)')
    ax[1].set_ylabel('Frequency')
    ax[1].set_title('Histogram of Distances')
    ax[1].legend()

    # Create table with index starting from 1
    plt.figure(figsize=(8, 4))
    table_data = [["PPR", "Index", "Distance"]] + [[f"{value:.2f}", index + 1, distances[index]] for index, value in enumerate(data)]
    plt.axis('tight')
    plt.axis('off')
    table = plt.table(cellText=table_data, colLabels=None, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    try:
        size = int(input("Enter the size of the set of random PPR values: "))
        elapsed_time = float(input("Enter the elapsed time for the test (in seconds): "))

        sensor_data = generate_sensor_readings(size)
        distances = [compute_distance(ppr, elapsed_time) for ppr in sensor_data]

        # Calculate mean and uncertainty
        mean_distance = np.mean(distances)
        uncertainty = np.std(distances)

        print(f"Mean Estimated Distance: {mean_distance:.2f} meters")
        print(f"Uncertainty (1st sigma): {uncertainty:.2f} meters")

        display_histograms_and_table(sensor_data, distances)

    except ValueError as e:
        print("Invalid input. Please enter numerical values.")
