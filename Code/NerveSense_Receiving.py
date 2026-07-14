import math
from machine import ADC, Pin, PWM, I2C, Timer
from machine_i2c_lcd import I2cLcd
import time

# --- ADC setup ---
adc = ADC(26)  # GP26 = ADC0

# --- L298N: EN/IN1/IN2 ---
in1 = Pin(14, Pin.OUT)
in2 = Pin(15, Pin.OUT)
ena = PWM(Pin(13))  # ENA (PWM speed)
ena.freq(1000)
ena.duty_u16(0)  # start disabled

# Previous equation setup
'''Sigma = 2
A = (5)/10000
L = 12.5/100
v_applied = 0.25
v_wire = 0.1
Gain = 16
v_ref = 0

I = (v_applied*Sigma*A)/L'''

def calc_distance(avg_diff_volts):
    distance = 12.8*math.exp(-22.21*avg_diff_volts) # equation created by using testing data in Excel  
    return distance

def drive_nerve():
    # 1. both off
    in1.low()
    in2.low()
    ena.duty_u16(0)
    # 2. forward 10 ms
    in1.high()
    in2.low()
    ena.duty_u16(32768)   # 50% PWM ≈ 5 V drive
    time.sleep_ms(10)
    # 3. reverse 10 ms
    in1.low()
    in2.high()
    ena.duty_u16(32768)
    time.sleep_ms(10)

# --- Calibrate baseline (mean ADC at rest) ---
def calibrate_baseline(samples=1000):
    s = 0
    for _ in range(samples):
        s += adc.read_u16()
        time.sleep_ms(1)
    return s // samples

baseline = calibrate_baseline()
print("Baseline ADC =", baseline)

# --- Display Code ---
#Adjust pins here
i2c = I2C(1, sda=Pin(6), scl=Pin(7), freq=400000)
lcd = I2cLcd(i2c, 0x27, 4, 20)

update_flag = False

#set breakpoints here (calibrate voltage)
bkpsFar = 0.1
bkpsMed = 0.25
bkpsClose= 0.4

#exists so that other code can run during screen refreshes
def on_timer(t):
    global update_flag
    update_flag = True

tim = Timer(-1)
#Refresh rate set in variable period
tim.init(period=50, mode=Timer.PERIODIC, callback=on_timer)

lcd.clear()
lcd.putstr("Nervesense On")

def displayLCD(avg_v, avg_diff_v, distance, noResponse):
    global update_flag
    if update_flag:
        update_flag = False
        lcd.clear()
        lcd.move_to(0,2)
        lcd.putstr(f"Voltage: {avg_v}")
        lcd.move_to(0,3)
        lcd.putstr(f"Delta Voltage: {avg_diff_v}")
        lcd.move_to(0,0)
        if noResponse:
            lcd.putstr(f"No samples in 0.25s")
        elif avg_v >= 5 or avg_v == 0:
            lcd.putstr(f"Outside of Site")
        elif avg_diff_v > bkpsClose:
            lcd.putstr(f"Close to Nerve")
        elif avg_diff_v > bkpsMed:
            lcd.putstr(f"Medium to Nerve")
        elif avg_diff_v > bkpsFar:
            lcd.putstr(f"Far to Nerve")
        lcd.move_to(0,1)
        lcd.putstr(str(distance))

# --- Convert ADC counts to volts ---
def adc_to_volts(val):
    return val * 3.3 / 65535.0

# --- Main loop: 0.25 s averaging ---
while True:
    #Sleep 5 seconds so that there's time to adjust
    t_start = time.ticks_ms()

    # --- 0.25 s averaging window (250 ms) ---
    adc_sum = 0
    diff_sum = 0
    n = 0
    while time.ticks_diff(time.ticks_ms(), t_start) < 250:
        drive_nerve()   # biphasic pulse, non-alternating order
        val = adc.read_u16()
        diff = val - baseline
        adc_sum += val
        diff_sum += diff
        n += 1
        time.sleep_ms(1)

    if n > 0:
        avg_adc = adc_sum // n
        avg_diff = diff_sum // n
        # Convert to volts
        avg_voltage    = adc_to_volts(avg_adc)
        avg_diff_volts = adc_to_volts(avg_diff)
        read_d = calc_distance(avg_diff_volts)
        print(read_d)
        print("avg_ADC={}, avg_diff={}".format(avg_adc, avg_diff))
        print("avg_voltage = {:.6f} V".format(avg_voltage))
        print("avg_diff_volts = {:.6f} V".format(avg_diff_volts))
        if read_d < 5:
            displayLCD(avg_voltage, avg_diff_volts, read_d, False)
        else:
            displayLCD(avg_voltage, avg_diff_volts, "> 5", False)

    else:
        print("No samples in 0.25 s")
        displayLCD(0.0, 0.0, True)
