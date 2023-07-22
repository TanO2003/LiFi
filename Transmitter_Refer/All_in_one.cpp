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
//static int file_content[FILESIZE_MAX * 8] = { 0 }; //to convert it to bits
//static long file_size = 0;


//Frame Sizes in Bits
#define frameSize 160 //Length of the actual Data Frame 

#define preambleSize 20
#define crcSize 8
#define cPackSize 8
#define tPackSize 8

#define overhead 24 //Overhead without synchro = crcSize+nameSize+extensionSize+cPackSize+tPackSize; 

//int dataFrame[frameSize+overhead+preambleSize]={1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1};
//int dataResult[frameSize+overhead-crcSize]={0};


//char result[preambleSize+overhead+frameSize]={'1','0','1','0','1','0','1','0','1','0','1','1','1','1','1','1','1','1','1','1'};


//different global variables
/*
int state=0;
bool synchro_Done=false;
bool senderState=false;
bool receiveData_Done =false;
int receivePos=preambleSize;
*/

//int sequenze[preambleSize]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
/*
enum Result
{
    OK, ARGUMENT_ERROR, FILE_NOT_FOUND, CANNOT_CREATE_FILE, MEMORY_NOT_AVAILABLE, READ_ERROR, WRITE_ERROR
};
*/



class Sender
{
    private:
    string message_byte;
    char result[preambleSize+overhead+frameSize]={'1','0','1','0','1','0','1','0','1','0','1','1','1','1','1','1','1','1','1','1'};


    void GetMessage(string message)
    {
        this->message=message;
    }


    void ConvertToByte()
    {
        for(int i=0;i<message.length();i++)
        {
            bitset<8> b(message.c_str()[i]);
            message_byte+=b.to_string();
        }
    }
    

        void CalculateCRC()
    {
        int polynom[9]={1,0,0,1,0,1,1,1,1};
        int k=preambleSize+overhead-crcSize+frameSize; 	
        int p=9; // lenght of polynom 
        int frame[preambleSize+overhead+frameSize]; //n=k+p-1 buffer frame with perfect size for CRC
        
        //convert char array to int array
        for(int i=0;i<preambleSize+overhead+frameSize;i++){
            if(i<k){
                frame[i]=result[i]-'0'; //converts an char number to corresponding int number
            }
            else{
                frame[i]=0;
            }	
        }
        
        //make the division
        int i=0;
        while (  i <  k  ){											
            for( int j=0 ; j < p ; j++){
                if( frame[i+j] == polynom[j] )	{
                    frame[i+j]=0;
                }
                else{
                    frame[i+j]=1;
                }			
            }
            while( i< preambleSize+overhead+frameSize && frame[i] != 1)
                i++; 
        }
        
        //CRC
        for(int j=k; j-k<p-1;j++)
        {
            //erst am Ende des Frames die CRC Sequenz deswegen j=k
            if (frame[j]==1)
            {
                result[j]='1';
                }
            else{
                result[j]='0';
            }
            
        }
    }



    void TransferData()
    {
        
        int pos=0;
        struct timeval tval_before, tval_after, tval_result;
        gettimeofday(&tval_before, NULL);
        while(pos!=overhead+preambleSize+frameSize)
        {
            gettimeofday(&tval_after, NULL);
            timersub(&tval_after, &tval_before, &tval_result);
            double time_elapsed = (double)tval_result.tv_sec + ((double)tval_result.tv_usec/1000000.0f);
            
            while(time_elapsed < 0.001)
            {
                gettimeofday(&tval_after, NULL);
                timersub(&tval_after, &tval_before, &tval_result);
                time_elapsed = (double)tval_result.tv_sec + ((double)tval_result.tv_usec/1000000.0f);
            }
            gettimeofday(&tval_before, NULL);
            
            if (result[pos]=='1')
            {
                digitalWrite(pin, HIGH);
                pos++;
                }
                
            else if(result[pos]=='0'){
                digitalWrite(pin,  LOW) ;
                pos++;
                }
        }
    
    }


    void BuildDataFrame()
    {
        double length = message_byte.length();
        int packages=0;

        if ((int)length%frameSize==0)
        {
            packages=(int)length/frameSize;
        }else                                                                                                                                                    
        {
            packages=(int)length/frameSize+1;
        }

        //convert total number of packages to binary here
        bitset<8> b(packages);


        for (int j=0;j<packages;j++)
        {
            // Add current package number to the frame
            for (int i=0; i<cPackSize;i++)
            {
                result[preambleSize+i]=((j+1) & (int)1<<(8-i-1)) ? '1' : '0';
                result[preambleSize+cPackSize+i]=b.to_string()[i];
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
                    result[preambleSize+overhead-crcSize+k-(frameSize*j)]=message_byte[k];          
                }
                for(int k=rest;k<frameSize;k++)
                {
                    result[preambleSize+overhead-crcSize+k]='0';
                }
                
            }

            //Add CRC
            CalculateCRC();

            //Send
            TransferData();
        }


    }

    public:
    string message;
    int pin;



    Sender(int pin)
    {
        this->pin=pin;
        wiringPiSetup();
        pinMode(pin,OUTPUT);
    }

    void SendMessage(string text)
    {
        GetMessage(text);
        ConvertToByte();
        BuildDataFrame();
    }

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

    void LookForSynchro()
    {
        bool same=true;
        int preamble[preambleSize]={1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1}; 
        for (int i = 0; i < preambleSize-1; i++) {
            sequenze[i]=sequenze[i+1];
        }
            sequenze[preambleSize-1]=data;
    
        for(int i=0;i<preambleSize;i++){
            if(sequenze[i]!=preamble[i])
            {
                same=false;
            }
        }
        
        
        if(same==true)
        {
            for (int i = 0; i < preambleSize; i++) {
                sequenze[i]=0;
            }
            receivePos=preambleSize;
            synchro_Done=true;
        }
    }

    void BitsToArray()
    { 
    for (int i=0;i<frameSize+overhead;i++)
    {dataResult[i]=dataFrame[i+preambleSize];}
    
    //Converting the Header Bits here
    int currentPackage=0;
    int totalPackages=0;
    for(int i = 0; i < (overhead/8)-1; i++) // -1 because last Byte is for CRC and has no message data
    {
        int pl[8];
        for(int l = i*8; l < 8*(i+1); l++){ 
            pl[l-(i*8)]= dataResult[l];
        }
            
        int n = 0;
        for(int j = 0; j < 8; j++)
        {
            int x = pl[j];
            for(int k = 0; k < 7-j; k++)  x *= 2;
            n += x;
        }
        if(i==0)
        {
            currentPackage =n;
        }
        if(i==1)
        {
            totalPackages =n;
        }
    }
        for(int i=0;i<frameSize;i++)
        {
            file_content[i+((currentPackage-1)*frameSize)]=dataResult[i+overhead-crcSize];
        }

    if (currentPackage==totalPackages)
    {
        int zeroCounter=0;
        for(int i=totalPackages*frameSize; i>=0;i--)
        {
        if (file_content[i]==0)
        {
            zeroCounter++;
        }
        else{break;}
        }
        zeroCounter=zeroCounter/8; //for Bytes
        //printf("ZeroCounter: %d\n",zeroCounter);
        for(int i=0;i<(totalPackages*frameSize)-zeroCounter;i++)
        {
            message+=file_content[i];
        }
    }

    
    receiveData_Done=true; 
    }


    void CheckCRC()
    {
        
    int polynom[9]={1,0,0,1,0,1,1,1,1};
    int p=9; //int p=strlen(polynom); // lenght of polynom (normaly fix, but it is better to use a variable if I want to change the polynom later
    int k= frameSize+preambleSize+overhead;  
    int frame[frameSize+preambleSize+overhead+crcSize]; //add crcSize again for calculation buffer space
        
    //fill the buffer array
    for(int i=0;i<frameSize+preambleSize+overhead+crcSize;i++){
        if (i<k)
        {
        frame[i]=dataFrame[i];}
        else
        {frame[i]=0;}
    }
    
    //make the division
    int i=0;
    while (  i <  k  ){                     
        for( int j=0 ; j < p ; j++){
                if( frame[i+j] == polynom[j] )  {
                    frame[i+j]=0;
                }
                else{
                    frame[i+j]=1;
                }     
        }
        while( i< frameSize+preambleSize+overhead+crcSize && frame[i] != 1)
                i++; 
    }

    bool CRC_Done_false=false;  
    for(int j=k; j-k<p-1;j++)
    {
        //erst am Ende des Frames die CRC Sequenz deswegen j=k
        if (frame[j]==1){
        CRC_Done_false=true;
        }     
    }  

    if(CRC_Done_false==false)
    {
        
        //printf("Nachricht fehlerfrei empfangen!\n");
        BitsToArray();
    }

    if(CRC_Done_false==true)
    {
        receiveData_Done=true; 
        printf("Nachricht war fehlerhaft und wurde verworfen!\n");
    }
    
    }


    void ReceiveData()
    {
        dataFrame[receivePos++]=data;
        
        
        
        if(receivePos==(overhead+frameSize+preambleSize))
        {
            CheckCRC();
        } 
        
    }

    public:
    string message;
    int pin;

    Receiver(int pin)
    {
        this->pin=pin;
        wiringPiSetup();
        pinMode(pin,INPUT);
    }


    void ReceiveMessage()
    {
        gettimeofday(&tval_after, NULL);
        timersub(&tval_after, &tval_before, &tval_result);
        double time_elapsed = (double)tval_result.tv_sec + ((double)tval_result.tv_usec/1000000.0f);


        while(time_elapsed < 0.001)
        {
            gettimeofday(&tval_after, NULL);
            timersub(&tval_after, &tval_before, &tval_result);
            time_elapsed = (double)tval_result.tv_sec + ((double)tval_result.tv_usec/1000000.0f);
        }
        gettimeofday(&tval_before, NULL);

        data = digitalRead(pin);


        switch (state)
        {
            case 0:
                //looking for preamble pattern
                synchro_Done=false;
                LookForSynchro();
                
                if (synchro_Done==true)
                {
                    state=1;
                }
                break;
                
            case 1:
                //receive the actual data
                receiveData_Done=false;
                senderState=false;
                ReceiveData();
                
                if(receiveData_Done&&senderState==false)
                {
                    state=0;
                }
                if(senderState==true)
                {
                    senderState=false;
                    state=0;
                }
                break;
                
        }


    }

};

/*
int main()
{
    string message;
    int pin_in = 3;
    Sender sender(pin_in);
    while(1)
    {
        cout << "Enter message: "<<endl;
        cin >> message;
        sender.SendMessage(message);
    }
    return 0;
}
*/
int main()
{
    int pin_out = 22;
    string message;
    Receiver receiver(pin_out);
    while (true)
    {
        receiver.ReceiveMessage();
        if (receiver.message != ""){
        cout << receiver.message << endl;}
    }
}
