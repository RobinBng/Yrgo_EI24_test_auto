#!/usr/bin/env python3
"""Python script for serial communication with the embedded system.

    This script should:
        1. Read and write data via the serial port.
        2. Format output with timestamps and color coding.
        3. Log all communication to a file.
        4. Send command strings to control program flow.
        5. Verify correct responses from the microcontroller.
"""
import os
import platform
import time
from datetime import datetime
from uart import factory, IUart

# Define log file path relative to this script
LOG_FILE = os.path.join(os.path.dirname(__file__), "serial_test_log.txt")

# Map simple names to ANSI codes
COLOR_CODES = {
    "red": "\033[31m",      # fail
    "green": "\033[32m",    # pass
    "blue": "\033[34m",     # sent
    "cyan": "\033[36m",     # received
    "": "",  # Default, no color
}

# Logging helper
def log(msg: str, color: str = "") -> None:
    """Log message with timestamp to console and file, with optional color."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"

    # Convert color name to ANSI code
    ansi_color = COLOR_CODES.get(color.lower(), "")
    print(f"{ansi_color}{line}\033[0m")  # Reset color after line

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

# Serial Helper
def send_command(uart: IUart, cmd: str) -> list[str]:
    """Send a command and collect all immediate responses."""
    log(f"> Sending command: {cmd}",color="blue")
    uart.write(cmd)
    responses = []
    timeout = 2.0
    start = time.time()
    while time.time() - start < timeout:
        line = uart.read()
        if line is None:
            time.sleep(0.05)
            continue
        log(f"< Received: {line}",color="cyan")
        responses.append(line)
    return responses

# ---------------------
# Tests
# ---------------------
def test_toggle(uart: IUart) -> bool:
    """Test toggle LED functionality and serial messages."""

    # Ensure toggle is OFF before test
    responses = send_command(uart, "s")
    if any("enabled!" in r for r in responses):
        send_command(uart, "t")  # disable

    try:
        # First toggle
        responses = send_command(uart, "t")
        if not any("enabled!" in r for r in responses):
            raise RuntimeError("First toggle failed")

        # Second toggle
        responses = send_command(uart, "t")
        if not any("disabled!" in r for r in responses):
            raise RuntimeError("Second toggle failed")

        log("Toggle test passed", color="green")
        return True
    except RuntimeError as e:
        log(f"Toggle test failed: {e}", color="red")
        return False

def test_temperature(uart: IUart) -> bool:
    """Test temperature reading."""
    try:
        responses = send_command(uart, "r")
        if not any("Temperature:" in r for r in responses):
            raise RuntimeError("Temperature not returned")
        log("Temperature test passed", color="green")
        return True
    except RuntimeError as e:
        log(f"Temperature test failed: {e}", color="red")
        return False

def test_eeprom(uart: IUart) -> bool:
    """Test EEPROM persistence (toggle state across resets)."""
    # Ensure toggle is OFF before test
    responses = send_command(uart, "s")
    if any("enabled!" in r for r in responses):
        send_command(uart, "t")  # disable

    try:
        # Enable toggle
        responses = send_command(uart, "t")
        if not any("enabled!" in r for r in responses):
            raise RuntimeError("First toggle command failed")
        # Reset the hardware
        log("Resetting the hardware")
        uart.reset()
        # Check status
        responses = send_command(uart, "s")
        if not any("enabled!" in r for r in responses):
            raise RuntimeError("First EEPROM toggle not persisted")

        # Disable toggle
        responses = send_command(uart, "t")
        if not any("disabled!" in r for r in responses):
            raise RuntimeError("Second toggle command failed")
        # Reset the hardware
        log("Resetting the hardware")
        uart.reset()
        # Check status
        responses = send_command(uart, "s")
        if not any("disabled!" in r for r in responses):
            raise RuntimeError("Second EEPROM toggle not persisted")

        log("EEPROM test passed", color="green")
        return True
    except RuntimeError as e:
        log(f"EEPROM test failed: {e}", color="red")
        return False

# ---------------------
# Main test runner
# ---------------------
if __name__ == "__main__":
    # Automatically choose stub for non-Windows
    use_stub = platform.system() != "Windows"
    # use_stub = True    # Uncheck this comment to use stub on windows
    uart = factory.create(stub=use_stub)

    results = {}
    try:
        results["toggle"] = test_toggle(uart)
        results["temperature"] = test_temperature(uart)
        results["eeprom"] = test_eeprom(uart)
    finally:
        uart.close()

    log("\n=== TEST SUMMARY ===")
    for test_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        color = "green" if passed else "red"
        log(f"{test_name}: {status}", color=color)
