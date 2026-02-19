"""Stub implementation for UART communication on Linux/Mac."""

from typing import List
from .interface import IUart

class UartStub(IUart):
    """UART stub simulating serial communication."""

    def __init__(self) -> None:
        """Initialize the stub."""
        self._buffer: List[str] = []  # Holds lines sent to the stub
        self._responses: List[str] = []  # Holds lines to return on read
        self._toggle_state: bool = False  # Simulate LED toggle state
        self._temperature: float = 23.0  # Simulate temperature reading

        # Preload startup messages (simulate firmware boot output)
        self._responses.append("Temperature prediction training succeeded!")
        if self._toggle_state:
            self._responses.append("Toggle timer enabled!")
        self._responses.extend([
            "Running the system!",
            "Please enter one of the following commands:",
            "- 't' to toggle the toggle",
            "- 'r' to read the temperature",
            "- 's' to check the state of the toggle timer",
        ])


    def write(self, data: str) -> None:
        """Simulate sending data over UART."""
        cmd = data.strip()
        self._buffer.append(cmd)

        # Generate fake response based on command
        if cmd == "q":  # Toggle LED
            self._toggle_state = not self._toggle_state
            msg = "Toggle timer enabled!" if self._toggle_state else "Toggle timer disabled!"
            self._responses.append(msg)
        elif cmd == "s":  # Status
            msg = "Toggle timer is active" if self._toggle_state else "Toggle timer is inactive"
            self._responses.append(msg)
        elif cmd == "r":  # Read temperature
            self._responses.append(f"Temperature: {self._temperature:.1f} C")
        else:
            # Unknown command
            self._responses.append(f"Unknown command: {cmd}")

    def read(self) -> str | None:
        """Return a line from the stub, or None if empty."""
        if self._responses:
            return self._responses.pop(0)
        return None

    def close(self) -> None:
        """Close the stub (no-op)."""
        self._buffer.clear()
        self._responses.clear()
