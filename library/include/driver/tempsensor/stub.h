/**
 * @brief Temperature sensor driver stub.
 */
#pragma once

#include <stdint.h>

#include "driver/tempsensor/interface.h"

namespace driver
{
namespace tempsensor
{
/**
 * @brief Temperature sensor driver stub.
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
        : myTemperature{0}
        , myInitialized{true}
    {}

    /**
     * @brief Destructor.
     */
    ~Stub() noexcept override = default;

    /**
     * @brief Check if the temperature sensor is initialized.
     * 
     * @return True if the temperature sensor is initialized, false otherwise.
     */
    bool isInitialized() const noexcept override{ return myInitialized; }

    /**
     * @brief Read the temperature sensor.
     *
     * @return The temperature in degrees Celsius.
     */
    int16_t read() const noexcept override{ return myTemperature; } 


     /**
     * @brief Set sensor initialization state.
     * 
     * @param[in] initialized sensor initialixation state ( true = initialized)
     */
    void setInitialized(bool initialized) noexcept
    {
        myInitialized = initialized;

        // reset temperature if the stub is uninitialized
        if(!myInitialized)
        {
            myTemperature = 0;
        }
    }

    /**
     * @brief Set the temperature sensor
     */
    void setTemperature(int16_t temperature) noexcept
    {
        if(myInitialized)
        {
            myTemperature = temperature;
        }
    }

    /**
     * @brief Clear the temperature sensor
     */
    void clearTemperature() noexcept
    {
        if(myInitialized)
        {
            myTemperature = 0;
        }
    }

    Stub(const Stub&)            = delete; // No copy constructor.
    Stub(Stub&&)                 = delete; // No move constructor.
    Stub& operator=(const Stub&) = delete; // No copy assignment.
    Stub& operator=(Stub&&)      = delete; // No move assignment.

private:
    /** Sensor temperature (from -32,768 to 32,768). */
    int16_t myTemperature;

    /** initialization state ( true = initialized). */
    bool myInitialized;
};
} // namespace tempsensor
} // namespace driver
