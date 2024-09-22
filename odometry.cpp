#include <iostream>

int main() {
    float encoderPulses, pulsesPerSecond, wheelRadius, vehicleWidth, elapsedTime;
    float xg, yg, og;

    std::cerr << "Enter Encoder Pulses per Revolution: ";
    std::cin >> encoderPulses;

    std::cerr << "Enter Pulses per Second: ";
    std::cin >> pulsesPerSecond;

    std::cerr << "Enter Wheel Radius: ";
    std::cin >> wheelRadius;

    std::cerr << "Enter Vehicle Width: ";
    std::cin >> vehicleWidth;

    std::cerr << "Enter Starting Pose (xg, yg, og) separated by spaces: ";
    std::cin >> xg >> yg >> og;

    std::cerr << "Enter Elapsed Time: ";
    std::cin >> elapsedTime;

    // Pass all values to Python
    std::cout << encoderPulses << " " << pulsesPerSecond << " " << wheelRadius << " " << vehicleWidth << " "
              << xg << " " << yg << " " << og << " " << elapsedTime << std::endl;

    return 0;
}
