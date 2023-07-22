#include <string>
#include <bitset>
#include <iostream>
#include <stdio.h>
#include <sys/time.h>
#include <string.h>
#include <wiringPi.h>
#include <stdbool.h> 
#include <stdlib.h>
#include <math.h>


#define NAME_MAX 1024
#define FILESIZE_MAX (2560)

#define frameSize 160 //Length of the actual Data Frame 

#define preambleSize 20
#define crcSize 8
#define cPackSize 8
#define tPackSize 8

#define overhead 24 //Overhead without synchro = crcSize+nameSize+extensionSize+cPackSize+tPackSize; 


class Sender
{
    private:

    std::string message_byte;
    char result[preambleSize+overhead+frameSize]={'1','0','1','0','1','0','1','0','1','0','1','1','1','1','1','1','1','1','1','1'};

    void GetMessage(std::string message);
    void ConvertToByte();
    void CalculateCRC();
    void TransferData();
    void BuildDataFrame();

    public:

    std::string message;
    int pin;

    Sender(int pin);
    void SendMessage(std::string text);

};

class Receiver
{
    private:
    struct timeval tval_before, tval_after, tval_result;
    int state=0;
    bool synchro_Done=false;
    bool senderState=false;
    bool receiveData_Done =false;
    int receivePos=preambleSize;
    int data;
    int sequenze[preambleSize]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    int dataFrame[frameSize+overhead+preambleSize]={1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1};
    int dataResult[frameSize+overhead-crcSize]={0};
    int file_content[FILESIZE_MAX * 8] = { 0 };

    void LookForSynchro();
    void BitsToArray();
    void CheckCRC();
    void ReceiveData();

    public:
    std::string message;
    int pin;

    Receiver(int pin);
    void ReceiveMessage();

};