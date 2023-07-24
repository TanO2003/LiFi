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




Sender::Sender(int pin_output)
{
    this->pin=pin_output;
    wiringPiSetup();
    pinMode(pin,OUTPUT);
}


void Sender::SendMessage(string text, int _Delay_ms)
{
    this->message=text;
    this->Delay_ms=_Delay_ms;
    Str2Bin();
    AddCrc();
    SendData();
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
    unsigned char* data_byte = &binary[preambleSize+crcSize];
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


Receiver::Receiver(int pin_input)
{
    this->pin=pin_input;
    wiringPiSetup();
    pinMode(pin,INPUT);
}



bool Receiver::LookForSync()
{
    stack<int> p_stack;
    const int desiredFrequency = 1000 / Delay_ms;
    const auto timePeriod = chrono::microseconds(1000000 / desiredFrequency);
    auto nextSyncTime = chrono::steady_clock::now() + timePeriod;
    if (digitalRead(pin) == sequenze[0])
    {
        p_stack.push(digitalRead(pin));
        for(int i=1;i<preambleSize;i++)
        {
            this_thread::sleep_until(nextSyncTime);
            p_stack.push(digitalRead(pin));
            nextSyncTime += timePeriod;
        }
        for (int i = preambleSize-1; i >= 0; i--)
        {
            if (p_stack.top() != sequenze[i])
            {
                return false;
            }
            p_stack.pop();
        }
    }
    else 
    {
        return false;
    }
    return true;
}


void Receiver::Bin2Str()
{
    for(int i=0;i<dataSize/8;i++)
    {
        int temp=0;
        for(int j=0;j<8;j++)
        {
            temp +=(message_bin[preambleSize+crcSize+i*8+j]-'0') * pow(2,7-j);
        }
        message += (char)temp;
    }

}


string Receiver::ReceiveMessage(int _Delay_ms)
{
    this->Delay_ms=_Delay_ms;
    while (LookForSync())
    {
        const int desiredFrequency = 1000 / Delay_ms;
        const auto timePeriod = chrono::microseconds(1000000 / desiredFrequency);
        auto nextSyncTime = chrono::steady_clock::now() + timePeriod;
        for(int i=preambleSize;i<totalSize;i++)
        {
            this_thread::sleep_until(nextSyncTime);
            message_bin[i]=digitalRead(pin)+'0';
            nextSyncTime += timePeriod;
        }
        //crc check
        unsigned char* data_byte = &message_bin[preambleSize+crcSize];
        uint8_t calculatedCRC = crc8(data_byte);
        uint8_t receivedCRC = 0x00;
        for(int i=0;i<crcSize;i++)
        {
            receivedCRC += (message_bin[preambleSize+i]-'0') * pow(2,crcSize-i-1);
        }
        if (calculatedCRC == receivedCRC)
        {
            Bin2Str();
            break;
        }
        else
        {
            cout<<"CRC check failed"<<endl;
            return;
        }

    }

    return message;
}