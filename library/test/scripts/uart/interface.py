"""Interface definition for UART communication."""

from abc import ABC, abstractmethod

class IUart(ABC):
    """Interface for UART communication."""

    @abstractmethod
    def write(self, data: str) -> None:
        """Send a string over UART."""

    @abstractmethod
    def read(self) -> str | None:
        """Read a single line from UART, or return None if no data is available."""

    @abstractmethod
    def close(self) -> None:
        """Close the UART connection."""

    @abstractmethod
    def reset(self) -> None:
        """Reset the Uart Connection"""   
