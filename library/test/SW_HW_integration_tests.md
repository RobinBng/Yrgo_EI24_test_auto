# HW/SW integration specification

## 1. Power-on Test
 
### Prerequisites
* Target hardware: Arduino/ATmega328P with connected buttons, LED, and temperature sensor.
* Microchip Studio installed and configured.
* Serial terminal available
*(Example: PuTTY from CMD prompt: `putty.exe -serial <com-port> -sercfg 9600,8,n,1,N`*

### 1.1 Firmware upload and boot
1. Build and flash the firmware to the target device.
2. Open a serial terminal and connect to the board. 
3. Verify that the following message is printed in the terminal:
```
Temperature prediction training succeeded!
Running the system!
Please enter one of the following commands:
- 't' to toggle the toggle
- 'r' to read the temperature
- 's' to check the state of the toggle timer
```

## 2. Toggle Functionality

### Prerequisites
* Firmware flashed and running on ATmega328P.
* Serial terminal open and connected.

### 2.1 Toggle button press
1. Press the toggle button once.
2. Verify that the LED begins blinking.
3. Press the toggle button again.
4. Verify that the LED stops blinking.

### 2.2 Blink timing
1. Observe the LED while it is blinking.
2. Measure the interval between LED state changes (on → off → on).
3. Verify that the blink period matches the `toggleTimerTimeout` defined in the firmware (`100 ms` by default).  
   *Expected result:* LED toggles approximately every 100 ms.


### 2.3 Debounce verification
1. Press the toggle button repeatedly within 300 ms intervals.
2. Verify that only the first press is registered and additional presses are ignored.


## 3. Temperature measurement
 
### Prerequisites
* Firmware flashed and running on ATmega328P.
* Serial terminal open and connected.

### 3.1 Temperature button
1. Press the temp button. Temperature shall print immediately.
2. Value should match room temperature.
3. Warm sensor with hand; value shall increase.
4. Debounce: repeated presses within 300 ms are ignored.

### 3.2 Temperature timer
1. Verify temperature prints automatically every 60 s (or 60 s after last press).
2. Values should remain reasonable.

## 4. Watchdog Timer

### Prerequisites
* Firmware flashed and running on ATmega328P.
* Access to modify source code in Microchip Studio.
* Serial terminal open.

### 4.1 Trigger watchdog reset
1. Add the line `while (myToggleButton.read()) {}` at the end of the function `Logic::handleButtonEvent()`.
2. Rebuild and flash the firmware.
3. Verify proper startup messages appear in the serial terminal.
4. Press the toggle and temperature buttons a few times; verify normal behavior in the serial terminal.
5. Hold the toggle button for at least 3 seconds.  
   *Expected result:* Within ~2 seconds, the watchdog timer expires and the system resets. Verify that the startup messages appear again in the serial terminal.

### 4.2 Restore normal behavior
1. Remove the added `while` line from the code.
2. Rebuild and flash the firmware.
3. Repeat steps 3–5 above.  
   *Expected result:* System operates normally; no automatic resets occur.

## 5. EEPROM Persistence

### Prerequisites
* Firmware flashed and running on ATmega328P.
* Serial terminal open.

### 5.1 Toggle state saved
1. Press toggle button to enable timer; LED shall blink.
2. Power off, then on.
3. LED shall blink immediately; serial terminal shows `Toggle timer enabled!`.

### 5.2 Toggle state cleared
1. Press toggle button to disable timer; LED shall stop blinking.
2. Power off, then on.
3. LED shall remain off; toggle timer inactive.

## 6. End-to-End Scenario

### Prerequisites
* Firmware flashed and running on ATmega328P.
* Serial terminal open.
* Toggle button (pin 12), temperature button (pin 13), and LED (pin 8) connected.

### 6.1 Full workflow
1. Reset or power on the system.
2. Press toggle button → LED shall blink.
3. Press temperature button → temperature shall print in serial terminal.
4. Wait for automatic temperature readout.
5. Press toggle button → LED shall stop blinking.
6. Press toggle button again → LED shall blink.
7. Reset system → toggle shall remain active; LED shall blink.
8. Press toggle button → LED shall stop blinking.
9. Reset system → toggle shall remain inactive; LED shall be off.