"""Driver implementation for UART communication on Windows."""

import time
from serial import Serial
from serial.tools import list_ports as serial_ports
from .interface import IUart

class UartDriver(IUart):
    """UART driver for Windows using real COM ports."""

    def __init__(self, baudrate: int = 9600, timeout_ms: float = 10.0) -> None:
        """Initialize the UART driver and connect to Arduino."""
        self._baudrate = baudrate
        self._timeout = timeout_ms / 1000.0  # Convert ms to seconds
        self._ser: Serial | None = None

        # Find COM port automatically
        com_port = self._get_com_port()
        if com_port is None:
            raise RuntimeError("Arduino Uno not found on any COM port!")

        # Open serial connection
        self._ser = Serial(com_port, baudrate=self._baudrate, timeout=self._timeout)

        # Wait for Arduino to start up
        time.sleep(2)

    def _get_com_port(self) -> str | None:
        """Get COM port of Arduino Uno.
        
        Returns:
            COM port connected to Arduino Uno as a string, or none if not found.
        """
        # Iterate through all COM ports, return port name if Arduino Uno is found.
        for port in serial_ports.comports():
            # Check if port description contains "arduino" or "uno".
            desc = (port.description or "").lower()
            if "arduino" in desc or "uno" in desc:
                return port.device
            # If that didn't match, check if the hardware ID matches Arduino Uno.
            # Note: SB VID:PID for Arduino ID is 2341:0043.
            hw_id = (port.hwid or "").lower()
            if "vid:pid=2341:0043" in hw_id:
                return port.device
        # Return none if no Arduino Uno was found.
        return None

    def write(self, data: str) -> None:
        """Send a string over UART."""
        if self._ser is not None:
            self._ser.write(data.encode())

    def read(self) -> str | None:
        """Read a single line from UART, or None if no data is available."""
        if self._ser is None or self._ser.in_waiting == 0:
            return None
        line = self._ser.readline().decode("utf-8", errors="replace").strip()
        return line if line else None

    def close(self) -> None:
        """Close the UART connection."""
        if self._ser is not None and self._ser.is_open:
            self._ser.close()
            self._ser = None

    def reset(self) -> None:
        """Toggle DTR to trigger hardware reset (DTR is wired to RESET on Arduino Uno)."""
        print("Resetting the hardware") 
        self._ser.dtr = False
        time.sleep(0.1)
        self._ser.dtr = True
        time.sleep(5.0) # Boot time
