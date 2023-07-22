#include <iostream>
#include <string>
#include <bitset>
#include <wiringPi.h>
#include <cstdint>
#include <cstddef>
#include <chrono>
#include <thread>


using namespace std;

const int preambleSize = 20;
const int crcSize = 8;
const int dataSize = 256;
const int totalSize = preambleSize + crcSize + dataSize;




uint8_t crc8(const unsigned char* data);



class Sender
{
    pubilc:
    string message;
    int pin;

    Sender(int pin);
    void SendMessage(string text);


    private:
    char binary[preambleSize+dataSize+crcSize]={'1','0','1','0','1','0','1','0','1','0','1','1','1','1','1','1','1','1','1','1'};
    string message_byte;

    void Str2Bin();
    void AddCrc();
    void SendData();

};


class Receiver
{

};
