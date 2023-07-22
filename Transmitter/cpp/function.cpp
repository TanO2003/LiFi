#include "Trans.h"

using namespace std;



uint8_t crc8(const unsigned char* data) {
    uint8_t crc = 0x00;
    size_t length = dataSize;
    while (length--) {
        crc ^= *data++;
        for (uint8_t i = 0; i < 8; ++i) {
            if (crc & 0x80) {
                crc = (crc << 1) ^ 0x07;
            } else {
                crc <<= 1;
            }
        }
    }

    return crc;
}




Sender::Sender(int pin)
{
    this->pin=pin;
    wiringPiSetup();
    pinMode(pin,OUTPUT);
}


void Sender::SendMessage(string text)
{

}


void Sender::Str2Bin()
{
    message_byte="";
    for(int i=0;i<message.length();i++)
    {
        bitset<8> b(message.c_str()[i]);
        message_byte+=b.to_string();
    }
    int dataLength=message_byte.length();
    
    if(dataLength>dataSize)
    {
        cout<<"Message is too long"<<endl;
        return -1;
    }
    else
    {
        for(int i=0;i<dataLength;i++)
        {
            binary[preambleSize+crcSize+i]=message_byte.c_str()[i];
        }
        for(int i=preambleSize+crcSize+dataLength;i<dataSize;i++)
        {
            binary[preambleSize+crcSize+i]='0';
        }
    }
}


void Sender::AddCrc()
{
    unsigned char* data_byte = &binary[28];
    uint8_t calculatedCRC = crc8(data_byte);
    for(int i=0;i<crcSize;i++)
    {
        binary[preambleSize+i]=((calculatedCRC) & (int)1<<(8-i-1)) ? '1' : '0';
    }
}

void Sender::SendData()
{
    int DataBit[totalSize];
    for(int i=0;i<totalSize;i++)
    {
        DataBit[i]=binary[i]-'0';
    }
    const int Delay_ms = 1;
    const int desiredFrequency = 1000 / Delay_ms;
    const auto timePeriod = chrono::microseconds(1000000 / desiredFrequency);
    auto nextSyncTime = chrono::steady_clock::now() + timePeriod;
    for(int i=0;i<totalSize;i++)
    {
        this_thread::sleep_until(nextSyncTime);
        digitalWrite(pin,DataBit[i]);
        nextSyncTime += timePeriod;
    }
}

