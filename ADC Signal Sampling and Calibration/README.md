# ADC Signal Sampling and Calibration

A Python implementation for sampling analogue signals using the MCP3208 12-bit ADC with Raspberry Pi, featuring real-time data acquisition, Nyquist frequency analysis, and ADC calibration procedures.

## Overview

This project demonstrates fundamental concepts in data acquisition and handling through:
- Real-time sampling of periodic analogue signals
- Nyquist frequency calculations and aliasing demonstration
- ADC calibration using square wave references
- Statistical analysis of measurement accuracy

## Hardware Requirements

- Raspberry Pi 5 with Raspbian Bookworm
- MCP3208 12-bit ADC (SPI interface)
- Breadboard and GPIO adapter
- Bench signal generator (0-3.3V capability)
- Digital oscilloscope with probe
- Jumper wires and basic electronics components

## Circuit Setup

### Power Connections
- Pi 3.3V (pin 1) → MCP3208 VDD (pin 16) and VREF (pin 15)
- Pi GND (pin 6) → MCP3208 AGND (pin 14) and DGND (pin 9)

### SPI Interface
- Pi SCLK (GPIO 11, pin 23) → MCP3208 SCK (pin 13)
- Pi MOSI (GPIO 10, pin 19) → MCP3208 DIN (pin 11)
- Pi MISO (GPIO 9, pin 21) → MCP3208 DOUT (pin 12)
- Pi CE0 (GPIO 8, pin 24) → MCP3208 CS (pin 10)

### Signal Input
- Signal generator output → MCP3208 CH0 (pin 1)
- Oscilloscope probe → same signal line for monitoring

## Key Features

### 1. Signal Sampling
- Samples 10 Hz sine wave at ~100 Hz sampling rate
- Calculates sampling statistics (Δt, fs, Nyquist frequency)
- Visualizes voltage vs. time data
- Demonstrates proper signal reconstruction

### 2. Nyquist Analysis
- Calculates theoretical maximum measurable frequency (fs/2)
- Shows relationship between sampling rate and signal fidelity
- Provides foundation for understanding aliasing effects

### 3. ADC Calibration
- Two-point calibration using square wave references
- Full-scale (0-3.3V) and half-scale (0-1.65V) measurements
- Statistical analysis of high/low voltage levels
- Calibration curve plotting against ideal response

## Technical Implementation

### Sampling Algorithm
```python
# Real-time voltage sampling with timing analysis
for i in range(num_samples):
    voltage = ADC0.analogReadVolt(0)
    elapsed = time.time() - start_time
    voltages.append(voltage)
    timestamps.append(elapsed)
```

### Calibration Procedure
- Separates square wave samples into high/low groups using threshold
- Calculates statistical means for each voltage level
- Compares ADC measurements against oscilloscope references
- Identifies systematic gain and offset errors

## Results and Analysis

The system achieves:
- **Sampling Rate**: ~95 Hz (limited by Python execution overhead)
- **Nyquist Limit**: ~47.6 Hz maximum measurable frequency
- **Calibration Accuracy**: Typically <1% gain error, <50mV offset error
- **Signal Fidelity**: 9.5 samples per cycle for 10Hz input

## Educational Outcomes

This project demonstrates:
- **Digital Signal Processing**: Nyquist theorem application
- **Measurement Science**: Calibration and error analysis
- **Embedded Systems**: SPI communication and ADC interfacing
- **Data Analysis**: Statistical processing and visualization

## Dependencies

```python
from DAH import MCP3208  # Custom DAH library for MCP3208
import time
import matplotlib.pyplot as plt
```

## Usage

1. Set up hardware circuit as described
2. Configure signal generator for 10 Hz sine wave (0-3.3V)
3. Run the Python script
4. Follow prompts for calibration measurements
5. Analyze generated plots and statistics

## Applications

This foundational work applies to:
- Sensor data acquisition systems
- Scientific instrumentation
- Real-time monitoring applications
- Educational demonstrations of ADC principles

## Future Enhancements

- Anti-aliasing filter implementation
- Higher sampling rates using compiled code
- Multi-channel simultaneous sampling
- Advanced calibration algorithms