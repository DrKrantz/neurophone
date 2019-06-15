import numpy as np
import time
from outputDevices import Sforzando


def generate_rates(n_channels=20, n_steps=1000, offset=10, scale=0.1, lambda_min=0, lambda_max=None):
    valmat = np.random.normal(0, scale, (n_channels, n_steps))
    processes = np.cumsum(valmat, 1) + offset
    processes[processes<lambda_min] = lambda_min
    if lambda_max is not None:
        processes[processes>=lambda_max] = lambda_max

    return processes


def rates_to_velocities(rates, lambda_max, vel_min=0, vel_max=127):
    return np.array(vel_max*rates/lambda_max, dtype=int)


if __name__ == '__main__':
    min_note = 80
    max_note = 81
    notes = list(range(min_note, max_note+1))
    n = max_note-min_note+1

    lambda_min = 0
    lambda_max = 30
    Ts = 5
    h = 500  # resolution, in ms
    lambda_base = 10  # Hz
    sigma = 0.1
    rates = generate_rates(n, int(1000 * Ts / h), lambda_base, sigma, lambda_min=lambda_min, lambda_max=lambda_max)

    velocities = rates_to_velocities(rates, lambda_max)

