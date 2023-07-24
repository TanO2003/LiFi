#include <iostream>
#include <string>
#include <bitset>
#include <wiringPi.h>
#include <cstdint>
#include <cstddef>
#include <chrono>
#include <thread>
#include <stack>
#include <cmath>



const int preambleSize = 20;
const int crcSize = 8;
const int dataSize = 256;
const int totalSize = preambleSize + crcSize + dataSize;




uint8_t crc8(const unsigned char* data);



class Sender
{
    public:
    std::string message;
    int pin;
    int Delay_ms;

    Sender(int pin_output);
    void SendMessage(std::string text, int _Delay_ms);


    private:
    char binary[preambleSize+dataSize+crcSize]={'0','1','0','1','0','1','0','1','0','1','0','0','0','0','0','0','0','0','0','0'};
    std::string message_byte;

    void Str2Bin();
    void AddCrc();
    void SendData();

};


class Receiver
{
    public:
    std::string message;
    int pin;
    int Delay_ms;

    Receiver(int pin_input);
    std::string ReceiveMessage(int _Delay_ms);


    private:
    const int sequenze[preambleSize]={0,1,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0};
    char message_bin[totalSize]={'0'};
    

    bool LookForSync();
    void Bin2Str();

};
