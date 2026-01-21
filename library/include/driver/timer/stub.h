/**
 * @brief Timer driver stub.
 */
#pragma once

#include <stdint.h>

#include "driver/timer/interface.h"

namespace driver
{
namespace timer
{
/**
 * @brief Timer driver stub.
 * 
 *        This class is non-copyable and non-movable
 */
class Stub final : Interface
{
public:
    /**
     * @brief Constructor.
     */
    Stub() noexcept
    : myInitialized{true}
    , myEnabled{false}
    , myTimedout{false}
    , myTimeout_ms{0u}
    {}


    /**
     * @brief Destructor.
     */
    ~Stub() noexcept override = default;

    /**
     * @brief Check if the timer is initialized.
     * 
     *        An uninitialized timer indicates that no timer circuit was available when the timer 
     *        was created.
     * 
     * @return True if the timer is initialized, false otherwise.
     */
    bool isInitialized() const noexcept override {return myInitialized;}

    /**
     * @brief Check whether the timer is enabled.
     *
     * @return True if the timer is enabled, false otherwise.
     */
    bool isEnabled() const noexcept override {return myEnabled;}

    /**
     * @brief Check whether the timer has timed out.
     *
     * @return True if the timer has timed out, false otherwise.
     */
    bool hasTimedOut() const noexcept override {return myTimedout;}

    /**
     * @brief Set the timer state
     *
     * @return True if the timer has timed out, false otherwise.
     */
    void setTimedOut(bool enable) noexcept 
    {
        if (myInitialized) { myTimedout = enable; }
    }

    /**
     * @brief Get the timeout of the timer.
     * 
     * @return The timeout in milliseconds.
     */
    uint32_t timeout_ms() const noexcept override {return myTimeout_ms;}

    /**
     * @brief Set timeout of the timer.
     * 
     * @param[in] timeout_ms The new timeout in milliseconds.
     */
    void setTimeout_ms(uint32_t timeout_ms) noexcept override
    {
        myTimeout_ms = timeout_ms;
    }

    /**
     * @brief Start the timer.
     */
    void start() noexcept override
    {
        myEnabled = true;
    }

    /**
     * @brief Stop the timer.
     */
    void stop() noexcept override
    {
        myEnabled = false;
    }

    /**
     * @brief Toggle the timer.
     */
    void toggle() noexcept override
    {
        myEnabled = !myEnabled;
    }

    /**
     * @brief Restart the timer.
     */
    void restart() noexcept override { myTimedout = false; }

    Stub(const Stub&)            = delete; // No copy constructor.
    Stub(Stub&&)                 = delete; // No move constructor.
    Stub& operator=(const Stub&) = delete; // No copy assignment.
    Stub& operator=(Stub&&)      = delete; // No move assignment.

private:
    /** initialization state ( true = initialized). */
    bool myInitialized; 

    /** Timer enablement ( true = high, false = low). */
    bool myEnabled;

    /** Timer timeout state ( true = has timed out, false = has not run out) */
    bool myTimedout;

    /** The number of milliseconds that the timer will theoretically count up to*/
    uint32_t myTimeout_ms;

};
} // namespace timer
} // namespace driver
