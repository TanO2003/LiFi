#include <iostream>
#include <vector>
#include <bitset>
#include <wiringPi.h>

// Function to convert binary to string
std::string bin_2_str(const std::string& binary) {
    // Find all substrings between '10000001'
    std::vector<std::string> messages;
    std::string::size_type pos = 0;
    while ((pos = binary.find("10000001", pos)) != std::string::npos) {
        messages.push_back(binary.substr(pos + 8, 8));
        pos += 9; // Move the position past the matched substring
    }

    std::string result;
    for (const auto& message : messages) {
        // Split message into bytes (8 bits each) and convert to char
        for (size_t i = 0; i < message.size(); i += 8) {
            std::string byte = message.substr(i, 8);
            char c = static_cast<char>(std::bitset<8>(byte).to_ulong());
            result += c;
        }
    }

    return result;
}

int main() {
    // Set up WiringPi library
    if (wiringPiSetup() == -1) {
        std::cerr << "Failed to initialize WiringPi." << std::endl;
        return 1;
    }

    // Set GPIO pin mode to input
    const int gpioPin = 6;
    pinMode(gpioPin, INPUT);

    // Set your desired delay (in milliseconds)
    int delay_ms = 500;

    while (true) {
        std::string a;
        int i = 0;

        while (i < 2) {
            a += std::to_string(digitalRead(gpioPin));
            delay(delay_ms);
            if (a.substr(a.size() - 8) == "10000001") {
                i++;
            }
        }

        std::cout << bin_2_str(a) << std::endl;
    }

    return 0;
}
