/**
 * @brief GPIO driver stub.
 */
#pragma once

#include <stdint.h>
#include "driver/gpio/interface.h"


namespace driver
{
namespace gpio
{
/**
 * @brief GPIO driver stub.
 * 
 *        This class is non-copyable and non-movable
 */
class Stub final : public Interface
{
public:

    /** 
     * @brief Constructor.
     */
    Stub() noexcept
    : myEnabled{false}
    , myInitialized{true}
    , myInterruptEnabled{false}
    {}


    /** 
     * @brief Destructor.
     */
    ~Stub() noexcept override = default;

    /**
     * @brief Check whether the GPIO is initialized.
     * 
     *        An uninitialized device indicates that the specified PIN was unavailable or invalid
     *        when the device was created.
     * 
     * @return True if the device is initialized, false otherwise.
     */
    bool isInitialized() const noexcept override {return myInitialized;}


    /**
     * @brief Get the data direction of the GPIO.
     * 
     * @return The data direction of the GPIO.
     */
    Direction direction() const noexcept override
    {
        // The data direction is irrelevant for this stub, always return input
        return Direction::Input;
    }

    /**
     * @brief Read input of the GPIO.
     * 
     * @return True if the input is high, false otherwise.
     */
    bool read() const noexcept override;

    /**
     * @brief Write output to the GPIO.
     * 
     * @param[in] output The output value to write (true = high, false = low).
     */
    void write(bool output) noexcept override;

    /**
     * @brief Toggle the output of the GPIO.
     */
    void toggle() noexcept override;

    /**
     * @brief Enable/disable pin change interrupt for the GPIO.
     * 
     * @param[in] enable True to enable pin change interrupt for the GPIO, false otherwise.
     */
    void enableInterrupt(bool enable) noexcept override;

    /**
     * @brief Enable pin change interrupt for I/O port associated with the GPIO.
     * 
     * @param[in] enable True to enable pin change interrupt for the I/O port, false otherwise.
     */
    void enableInterruptOnPort(bool enable) noexcept override;

private:
    /** GPIO enablement (true = high, false = low). */
    bool myEnabled;

    /** Initialixation state ( true = initialized). */
    bool myInitialized;

    /** GPIO interrupt enablement ( true = interrupts are enabled). */
    bool myInterruptEnabled;

};
} // namespace gpio
} // namespace driver
