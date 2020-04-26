import board
import digitalio
import pulseio
import time
from adafruit_motor import servo
from analogio import AnalogIn

'''A PWM tester for the Adafruit ItsyBitsy M0.

	     Adafruit ItsyBitsy M0

          -------\___/-------
    Reset |  1           33 | BAT
          |                 |
       3V |  2           32 | GND
          |                 |
     AREF |  3           31 | USB
          |                 |
      Vhi |  4           30 | D13
          |                 |
     (A0) |  5           29 | D12
          |                 |
       A1 |  6           28 | D11
          |                 |
       A2 |  7           27 | D10
          |                 |
       A3 |  8           26 | D9
          |                 |
       A4 |  9           25 | D7
          |                 |
       A5 | 10           24 | D5!
          |                 |
      SCK | 11           23 | SCL
          |                 |
     MOSI | 12           22 | SDA
          |                 |
     MISO | 13           21 | D1/Tx
          |    1 1 1 1 1    |
       D2 | 14 5 6 7 8 9 20 | D0/Rx
          -------------------
               E G D D D
			   n N 8 3 4
			     D
								 
      10K OHM POTENTIOMETER
            ██████████        
          ██          ██         
        ██              ██       
      ██                  ██       
      ██       ████       ██     
      ██      ██████      ██        
      ██       ████       ██       
      ██                  ██         
        ██              ██         
          ██          ██           
            ██████████
			██  ██  ██

            P2  P5  GND			
			
	ItsyBitsy Pins:
		 2 |  3V: Potentiometer High
		 5 |  A0: Potentiometer Wiper
		 7 |  A2: PWM Out
		29 | D12: Button
		30 | D13: LED+
		32 | GND: Battery Ground
		33 | BAT: Battery Positive (5V)
		
'''

'''Pin initialization.

PWM output should be 50% duty cycle, 2^15 is 1/2 2^16
For safety, the button is set so that the PWM is only output if it is being held
'''
pwm = pulseio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)
motor = servo.Servo(pwm)
potentiometer_pin = AnalogIn(board.A0)
button = digitalio.DigitalInOut(board.D12)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

def get_voltage(pin):
  # Helper function to do the analog to digital conversion.
  return (pin.value * 3.3) / 65536

def get_pot_pct(potentiometer_pin):
  # Helper function to turn voltage into a percentage
  return (get_voltage(potentiometer_pin) / 3.3) * 100


while True:
  percent = get_pot_pct(potentiometer_pin)
  # Here we configure a dead zone in addition to our dead man's switch
  if button.value or (percent >= 43 and percent <= 57):
    percent = 50
  # The PWM pulse is set up for a relay that goes from 0 to 180 degrees
  angle = 180 * (percent / 100)
  # Output to the serial console
  print('Percent: ' + str(percent) + ' Angle: ' + str(angle) + ' Safety: ' + str(button.value))
  # Do the output
  motor.angle = angle
  # Wait a tick before updating again to prevent jitter
  time.sleep(0.1)