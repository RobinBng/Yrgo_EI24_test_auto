"""Serial factory implementation."""
from .driver import UartDriver
from .interface import IUart
from .stub import UartStub

def create(baudrate: int = 9600, timeout_ms: int | float = 10, stub: bool = False) -> IUart:
    """Create serial instance.

    Args:
        baudrate: Baud rate in bps (default = 9600 bps).
        timeout_ms: Timeout in milliseconds (default = 10 ms).
        stub: True to create a stub (default = false).

    Returns:
        New serial instance.
    """
    if stub:
        return UartStub()
    return UartDriver(baudrate, timeout_ms)
