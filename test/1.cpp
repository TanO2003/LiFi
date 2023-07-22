#include <cstdint>
#include <cstddef>
#include <string>
#include <bitset>

std::uint8_t crc8(const unsigned char* data, std::size_t length) {
    std::uint8_t crc = 0x00;

    while (length--) {
        crc ^= *data++;
        for (std::uint8_t i = 0; i < 8; ++i) {
            if (crc & 0x80) {
                crc = (crc << 1) ^ 0x07;
            } else {
                crc <<= 1;
            }
        }
    }

    return crc;
}

// Function to verify the CRC
bool verifyCRC(const unsigned char* data, std::size_t length, std::uint8_t receivedCRC) {
    return crc8(data, length) == receivedCRC;
}


#include <iostream>

int main() {
    std::string message = "Hello World!";
    std::string message_byte="";
    for(int i=0;i<message.length();i++)
    {
        std::bitset<8> b(message.c_str()[i]);
        message_byte+=b.to_string();
    }
    int dataLength=message_byte.length();

    unsigned char data[256];
    for(int i=0;i<dataLength;i++)
    {
        data[i]=message_byte.c_str()[i];
    }
    for(int i=dataLength;i<256;i++)
    {
        data[i]='0';
    }


    std::uint8_t calculatedCRC = crc8(data, sizeof(data));
    
    std::cout << "Calculated CRC: " << std::hex << static_cast<int>(calculatedCRC) << std::endl;
    std::cout<<calculatedCRC<<std::endl;
    // Now, suppose you have received an 8-bit CRC and want to verify it
    //std::uint8_t receivedCRC = /* Your received 8-bit CRC goes here */;
    //bool isCRCValid = verifyCRC(data, sizeof(data), receivedCRC);
    //std::cout << "CRC is " << (isCRCValid ? "valid" : "invalid") << std::endl;

    return 0;
}
