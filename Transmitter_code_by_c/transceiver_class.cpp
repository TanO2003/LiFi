#include <stdio.h>
#include <sys/time.h>
#include <string.h>
#include <wiringPi.h>
#include <stdbool.h> 
#include <stdlib.h>
#include <math.h>
#include <string>
#include <bitset>
#include <iostream>

using namespace std;

#define NAME_MAX 1024
#define FILESIZE_MAX (2560) //(2.5 * 1024) //256 packages -> 2,5kB Maximum -> frameSize 80
static int file_content[FILESIZE_MAX * 8] = { 0 }; //to convert it to bits
static long file_size = 0;


//Frame Sizes in Bits
#define frameSize 160 //Length of the actual Data Frame 

#define preambleSize 20
#define crcSize 8
#define cPackSize 8
#define tPackSize 8

#define overhead 24 //Overhead without synchro = crcSize+nameSize+extensionSize+cPackSize+tPackSize; 

int dataFrame[frameSize+overhead+preambleSize]={1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1};
int dataResult[frameSize+overhead-crcSize]={0};


//char result[preambleSize+overhead+frameSize]={'1','0','1','0','1','0','1','0','1','0','1','1','1','1','1','1','1','1','1','1'};


//different global variables
int state=0;
bool synchro_Done=false;
bool senderState=false;
bool receiveData_Done =false;
int receivePos=preambleSize;

int sequenze[preambleSize]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

enum Result
{
    OK, ARGUMENT_ERROR, FILE_NOT_FOUND, CANNOT_CREATE_FILE, MEMORY_NOT_AVAILABLE, READ_ERROR, WRITE_ERROR
};




class Sender
{
    public:
    string message;
    string message_byte;
    char result[preambleSize+overhead+frameSize]={'1','0','1','0','1','0','1','0','1','0','1','1','1','1','1','1','1','1','1','1'};



    void Sender(string message)
    {
        this->message=message;
    }

    void convertToByte()
    {
        for(int i=0;i<message.length();i++)
        {
            bitset<8> b(message.c_str()[i]);
            message_byte+=b.to_string();
        }
    }
    
    void BuildDataFrame()
    {
        double length = message_byte.length();
        int packages=0;

        if ((int)length%frameSize==0)
        {
            packages=(int)length/frameSize;
        }else:
        {
            packages=(int)length/frameSize+1;
        }

        //convert total number of packages to binary here
        bitset<8> b(packages);
        for (int j=0; j<cPackSize;j++)
        {
            packagesBinary[i]=b[i];
        }
        
        for (int j=0;j<packages;j++)
        {
            // Add current package number to the frame
            for (int i=0; i<cPackSize;i++)
            {
                result[preambleSize+i]=((j+1) & (int)1<<(8-i-1)) ? '1' : '0';
                result[preambleSize+cPackSize+i]=packagesBinary[i];
            }

            int rest=(int) length % frameSize; 
            
            if(j!=packages-1||rest==0)
            {
                //Add the file content
                for(int k=frameSize*j;k<frameSize*(j+1);k++)
                {
                    result[preambleSize+overhead-crcSize+k-(frameSize*j)]=message_byte[k];
                }
            }


            if (j==packages-1&&rest!=0)
            {
                for(int k=frameSize*j;k<(frameSize*j)+rest;k++)
                {
                    if(content[k]==1)
                    {
                        result[preambleSize+overhead-crcSize+k-(frameSize*j)]='1';
                    }
                    else if(content[k]==0)
                    {
                        result[preambleSize+overhead-crcSize+k-(frameSize*j)]='0';
                    }            
                }
                for(int k=rest;k<frameSize;k++)
                {
                    result[preambleSize+overhead-crcSize+k]='0';
                }
                
            }
        }


    }

};