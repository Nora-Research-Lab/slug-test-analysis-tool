import numpy as np
import matplotlib.pyplot as plt
import io
import csv

def parse_data(content):
    """Parse time and head ratio from pasted text or CSV content (string)."""
    lines = content.strip().split('\n')
    time = []
    ratio = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split(',')
        if len(parts) != 2:
            continue
        try:
            t = float(parts[0].strip())
            r = float(parts[1].strip())
            if r <= 0:
                continue
            time.append(t)
            ratio.append(r)
        except:
            continue
    return np.array(time), np.array(ratio)

def compute_ln_ratio(ratio):
    return np.log(np.maximum(ratio, 1e-10))

def linear_regression(x, y):
    n = len(x)
    if n < 2:
        return 0.0, 0.0, 0.0
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    slope = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean)**2)
    intercept = y_mean - slope * x_mean
    y_pred = slope * x + intercept
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - y_mean)**2)
    r_sq = 1 - ss_res / ss_tot if ss_tot != 0 else 0
    return slope, intercept, r_sq

def hvorslev_k(r, L, H0, time, ratio, r_unit='m'):
    if r_unit == 'cm':
        r = r / 100.0
    if L <= 0 or r <= 0 or L <= r:
        return None, None, None, None, None
    ln_ratio = compute_ln_ratio(ratio)
    if len(ln_ratio) < 2:
        return None, None, None, None, None
    slope, intercept, r_sq = linear_regression(time, ln_ratio)
    if slope >= 0:
        return None, None, None, None, None
    T0 = -1.0 / slope
    if T0 <= 0:
        return None, None, None, None, None
    K = (r**2 * np.log(L / r)) / (2 * L * T0)
    return K, slope, intercept, r_sq, T0

def bouwer_rice_k(r, L, H0, time, ratio, aquifer_thickness=None, r_unit='m'):
    if r_unit == 'cm':
        r = r / 100.0
    if L <= 0 or r <= 0 or L <= r:
        return None
    ln_ratio = compute_ln_ratio(ratio)
    if len(ln_ratio) < 2:
        return None
    slope, intercept, r_sq = linear_regression(time, ln_ratio)
    if slope >= 0:
        return None
    T0 = -1.0 / slope
    if T0 <= 0:
        return None
    # Compute ln(Re/r) using Bouwer-Rice (1976) approximation
    if aquifer_thickness is not None and aquifer_thickness > L:
        b = aquifer_thickness
        if b - L <= 0:
            ln_Re_over_r = np.log(200)  # fallback
        else:
            # Coefficients from typical implementation (A=2.0, B=2.0, C=0.53 for b>3L)
            # Simplified formula from "Analysis of Slug Tests" (Butler, 1998)
            # For unconfined, partially penetrating well:
            # ln(Re/r) = [1.1 / ln(L/r) + (0.53 + 2.0 * ln((b-L)/r)) / (L/r)]^(-1)
            term1 = 1.1 / np.log(L / r)
            term2 = (0.53 + 2.0 * np.log((b - L) / r)) / (L / r)
            ln_Re_over_r = 1.0 / (term1 + term2) if (term1 + term2) > 0 else np.log(200)
    else:
        # Large aquifer thickness (>3L) => Re ≈ 200 r
        ln_Re_over_r = np.log(200)
    K = (r**2 * ln_Re_over_r) / (2 * L * T0)
    return K

def generate_plot(time, ratio, slope, intercept, r_sq=0):
    fig, ax = plt.subplots(figsize=(6,4))
    ln_ratio = compute_ln_ratio(ratio)
    ax.scatter(time, ln_ratio, label='Data', color='blue')
    x_fit = np.linspace(min(time), max(time), 100)
    y_fit = slope * x_fit + intercept
    ax.plot(x_fit, y_fit, 'r-', label=f'Regression (R²={r_sq:.3f})')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('ln(H/H₀)')
    ax.set_title('Slug Test Analysis')
    ax.legend()
    plt.tight_layout()
    return fig

def classification_table(K_m_s):
    if K_m_s is None:
        return "Unable to classify."
    classes = [
        (1e-1, 1e0, 'Gravel'),
        (1e-4, 1e-1, 'Sand'),
        (1e-8, 1e-4, 'Silt'),
        (1e-12, 1e-8, 'Clay')
    ]
    for low, high, name in classes:
        if low <= K_m_s < high:
            return f"K = {K_m_s:.2e} m/s  →  {name}"
    return f"K = {K_m_s:.2e} m/s  →  Out of typical range"
