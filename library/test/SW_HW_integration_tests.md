# HW/SW integration specification



## 1. Basic funktionalitet
 
### Prerequisites
* Tillgång till Arduino/ATmega328P med nödvändig hårdvara (knappar, lysdiod, temperatursensor). 
* microchip studio
* Fungerande utvecklingsmiljö för att bygga och ladda upp kod till Arduino (Microchip Studio eller PlatformIO).







## 3. Temperature measurement
 
### Prerequisites
* Build and flash an ATmega328p processor.
* Run the system, open a serial terminal.

#### 3.1 Temperature button
* Press the toggle button.
* The temperature shall be printed in the terminal.

#### 3.2 Temperature timer
* Ensure that the temperature is printed every 60 seconds, 
or 60 seconds after the last pressdown.



