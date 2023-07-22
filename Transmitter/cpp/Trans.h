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
    int Delay_ms;

    Sender(int pin_output);
    void SendMessage(string text, int _Delay_ms);


    private:
    char binary[preambleSize+dataSize+crcSize]={'1','0','1','0','1','0','1','0','1','0','1','1','1','1','1','1','1','1','1','1'};
    string message_byte;

    void Str2Bin();
    void AddCrc();
    void SendData();

};


class Receiver
{
    pubilc:
    string message;
    int pin;
    int Delay_ms;

    Receiver(int pin_input);
    string ReceiveMessage(int _Delay_ms);


    private:
    const int sequenze[preambleSize]={1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1};
    char message_bin[totalSize]={'0'};
    

    bool LookForSync();
    void Bin2Str();

};
