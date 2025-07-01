import numpy as np

def factors(num):
    return [i for i in range(1, num + 1) if num % i == 0]

def compute_magnitude(u, v, w):
    return np.sqrt(float(u) ** 2 + float(v) ** 2 + float(w) ** 2)