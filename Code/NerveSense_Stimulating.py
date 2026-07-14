import time

adc = machine.ADC(26) # GPIO 26
conversion_factor = 3.3 / 65535

# Define the GPIO pins connected to IN1 and IN2 of L298N
in1 = machine.Pin(21, machine.Pin.OUT)  # GPIO 21 (IN1)
in2 = machine.Pin(19, machine.Pin.OUT)  # GPIO 19 (IN2)

# Frequency of pulsed DC signal (20Hz)
frequency = 1  # 1 Hz for testing
period = 1 / frequency  # seconds

# Function to generate a pulsed DC signal
def pulsed_dc():
    # Continuously send 20Hz pulse
    while True:
        
        in1.high()  # Set IN1 HIGH
        in2.low()   # Set IN2 LOW
        time.sleep(period / 2)  # Wait for half the period (50% duty cycle)

        in1.low()   # Set IN1 LOW
        in2.high()  # Set IN2 HIGH
        time.sleep(period / 2)  # Wait for the other half of the period
