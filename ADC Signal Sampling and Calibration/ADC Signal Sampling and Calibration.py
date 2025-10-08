from DAH import MCP3208
import time
import matplotlib.pyplot as plt


# Instantiate MCP3208 ADC chip 0 (CE0)
ADC0 = MCP3208.chip0

num_samples = 100
delay = 0.01  # seconds between samples

voltages = []
timestamps = []

start_time = time.time()

for i in range(num_samples):
    # Read voltage from channel 0 (single-ended)
    voltage = ADC0.analogReadVolt(0)
    elapsed = time.time() - start_time
    voltages.append(voltage)
    timestamps.append(elapsed)

total_time = time.time() - start_time
dt = total_time / num_samples
fs = 1.0 / dt

print(f"Samples: {num_samples}")
print(f"Total time: {total_time:.3f} s")
print(f"Δt: {dt:.6f} s → fs ≈ {fs:.1f} Hz")
print(f"Nyquist frequency: {fs / 2.0:.1f} Hz")

# Plot ADC voltage readings over time
plt.figure(figsize=(8, 4))
plt.plot(timestamps, voltages, 'o-', label='Channel 0 Voltage (V)')
plt.title("Checkpoint 3: ADC Sampling of 10 Hz Signal")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.legend()
plt.grid()
plt.show()

n = 100
def sample_voltages(channel, n, delay):
    samples = []
    for _ in range(n):
        samples.append(ADC0.analogReadVolt(channel))
        time.sleep(delay)
    return samples


threshold = 1.65  # Voltage midpoint to separate high/low samples

# Measure full-scale square wave (0–3.3 V)
print("Measuring full-scale square wave (0–3.3 V)...")
full_samples = sample_voltages(0, num_samples, delay)
high_vals = [v for v in full_samples if v > threshold]
low_vals = [v for v in full_samples if v <= threshold]
mean_high_full = sum(high_vals) / len(high_vals)
mean_low_full = sum(low_vals) / len(low_vals)
print(f"Full scale mean high: {mean_high_full:.3f} V")
print(f"Full scale mean low : {mean_low_full:.3f} V")

# Prompt for half-scale (0–1.65 V)
input("Set generator to 0–1.65 V and press Enter to continue...")

half_samples = sample_voltages(0, num_samples, delay)
high_vals_half = [v for v in half_samples if v > threshold]
low_vals_half = [v for v in half_samples if v <= threshold]
mean_high_half = sum(high_vals_half) / len(high_vals_half)
mean_low_half = sum(low_vals_half) / len(low_vals_half)
print(f"Half scale mean high: {mean_high_half:.3f} V")
print(f"Half scale mean low : {mean_low_half:.3f} V")

# Plot calibration curve
scope_volts = [3.3, 0.0, 1.65, 0.0]
adc_means = [mean_high_full, mean_low_full, mean_high_half, mean_low_half]

plt.figure(figsize=(6, 6))
plt.plot(scope_volts, adc_means, 's-', label='ADC Measurement')
plt.plot(scope_volts, scope_volts, 'k--', label='Ideal Curve (y=x)')
plt.title("Checkpoint 3: ADC Calibration Curve")
plt.xlabel("Oscilloscope Voltage (V)")
plt.ylabel("ADC Voltage (V)")
plt.legend()
plt.grid()
plt.show()
