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

in3 = Pin(21, Pin.OUT)
in4 = Pin(19, Pin.OUT)

frequency = 1
period = 1 / frequency

def calc_distance(avg_diff_volts):
    distance = 20*math.exp(-7.21*avg_diff_volts)
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


shock_timer = Timer()

def drive_shock():
    # 1. both off
    in3.low()
    in4.low()
    ena.duty_u16(0)
    # 2. forward 10 ms
    in3.high()
    in4.low()
    ena.duty_u16(32768)   # 50% PWM ≈ 5 V drive
    time.sleep_ms(500)
    # 3. reverse 10 ms
    in3.low()
    in4.high()
    ena.duty_u16(32768)
    time.sleep_ms(500)

def shock_callback(t):
    drive_shock()

shock_timer.init(period=500, mode=Timer.PERIODIC, callback=shock_callback)

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
i2c = I2C(1, sda=Pin(6), scl=Pin(7), freq=400000)
lcd = I2cLcd(i2c, 0x27, 4, 20)

update_flag = False

# Proximity thresholds (calibrated voltage deltas)
bkpsFar   = 0.1
bkpsMed   = 0.25
bkpsClose = 0.4

def on_timer(t):
    global update_flag
    update_flag = True

tim = Timer(-1)
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

# --- Main loop: 0.25 s averaging window ---
while True:
    t_start = time.ticks_ms()

    adc_sum  = 0
    diff_sum = 0
    n        = 0

    while time.ticks_diff(time.ticks_ms(), t_start) < 250:
        drive_nerve()   # biphasic pulse
        drive_shock()
        val  = adc.read_u16()
        diff = val - baseline
        adc_sum  += val
        diff_sum += diff
        n += 1
        time.sleep_ms(1)

    if n > 0:
        avg_adc        = adc_sum  // n
        avg_diff       = diff_sum // n
        avg_voltage    = adc_to_volts(avg_adc)
        avg_diff_volts = adc_to_volts(avg_diff)
        read_d         = calc_distance(avg_diff_volts)

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
