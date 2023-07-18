#include <stdio.h>
#include <sys/time.h>
#include <string.h>
#include <wiringPi.h>
#include <stdbool.h> 
#include <stdlib.h>
#include <math.h>

#define NAME_MAX 1024
#define FILESIZE_MAX (2560) //(2.5 * 1024) //256 packages -> 2,5kB Maximum -> frameSize 80
static int file_content[FILESIZE_MAX * 8] = { 0 }; //to convert it to bits
static long file_size = 0;


//Frame Sizes in Bits
#define frameSize 160 //Length of the actual Data Frame 

#define preambleSize 20
#define crcSize 8
#define nameSize 16
#define extensionSize 24
#define cPackSize 8
#define tPackSize 8

#define overhead 64 //Overhead without synchro = crcSize+nameSize+extensionSize+cPackSize+tPackSize; 

int dataFrame[frameSize+overhead+preambleSize]={1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1};
int dataResult[frameSize+overhead-crcSize]={0};


char result[preambleSize+overhead+frameSize]={'1','0','1','0','1','0','1','0','1','0','1','1','1','1','1','1','1','1','1','1'};


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


int read_file(const char filename[NAME_MAX], const char extension[NAME_MAX], int content[FILESIZE_MAX * 8])
{
    /*
        Combine filename and extension using '.'
    */
    char buffer[NAME_MAX * 2] = { 0 };
    snprintf(buffer, (NAME_MAX * 2) - 1, "%s.%s",  filename, extension);

    /*
        Try opening file
    */
    FILE *input = fopen(buffer, "rb");
    if (input == NULL) return FILE_NOT_FOUND;

    /*
        Seek to end and get cursor position
        which will give us size
        Seek to start of file
    */
    fseek(input, 0, SEEK_END);
    long size = ftell(input);
    fseek(input, 0, SEEK_SET);

    /*
        So, if size is greater than array size, return from function
        Store size in global variable
    */
    file_size = size; //Length of Bytes
    if (size >= FILESIZE_MAX)
    {
        fclose(input);
        return MEMORY_NOT_AVAILABLE;
    }

    /*
        For every byte, read it, and store every bit in int array
    */
    for (long i = 0, current_index = 0; i < size; i++)
    {
        char content_byte;
        if (fread(&content_byte, 1, 1, input) != 1)
        {
            fclose(input);
            return READ_ERROR;
        }

        content[current_index++] = (content_byte >> 7) & 1;
        content[current_index++] = (content_byte >> 6) & 1;
        content[current_index++] = (content_byte >> 5) & 1;
        content[current_index++] = (content_byte >> 4) & 1;
        content[current_index++] = (content_byte >> 3) & 1;
        content[current_index++] = (content_byte >> 2) & 1;
        content[current_index++] = (content_byte >> 1) & 1;
        content[current_index++] = (content_byte >> 0) & 1;
    }

    fclose(input);

    return OK;
    
}
void CalculateCRC(char dataFrame[], int startpoint)
{	
    int polynom[9]={1,0,0,1,0,1,1,1,1};
	int k=preambleSize+overhead-crcSize+startpoint; 	
	int p=9; // lenght of polynom 
    int frame[preambleSize+overhead+frameSize]; //n=k+p-1 buffer frame with perfect size for CRC
    
    //convert char array to int array
    for(int i=0;i<preambleSize+overhead+frameSize;i++){
		if(i<k){
			frame[i]=dataFrame[i]-'0'; //converts an char number to corresponding int number
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
            digitalWrite(22, HIGH);
            pos++;
            }
            
        else if(result[pos]=='0'){
            digitalWrite(22,  LOW) ;
            pos++;
            }
    }
    
}

void BuildDataFrame(const char filename[NAME_MAX], const char extension[NAME_MAX], int content[FILESIZE_MAX * 8])
{
    double length=(double)file_size*8;

    int packages= (int)round(0.5+(length/frameSize)); //added 0.5, damit es immer noch oben rundet, also 1,1 zu 2 packete wird  //printf ("Number of packages is: %d \n",packages);
    if((int)length%frameSize==0)
    {packages=(int)length/frameSize;}
    
    //convert total number of packages to binary here
    char packagesBinary[8];
    for (int i=0;i<8;i++)   
    {
        packagesBinary[i] = (packages & (int)1<<(8-i-1)) ? '1' : '0';
    }
    
    for (int j=0; j<packages; j++) //Für jedes Paket ausführen
    {
        //Add FileName
        for(int l=0;l<2;l++) //read in the Filename and set the first two letters in the frame
        {
            for(int i=7; i>=0;i--){
                result[preambleSize+7-i+(8*l)]= (filename[l]&(1<<i))?'1':'0';  
            }
        }

        //Add File Ending
        for(int l=0;l<3;l++) //read in the Fileending (png, jpg, txt usw.) and send it in the frame -> only 3 letters
        { 
            for(int i=7; i>=0;i--){
                result[preambleSize+nameSize+7-i+(8*l)]= (extension[l]&(1<<i))?'1':'0';  
            }
        }
        //Add current and total packages Number
        for (int i=0;i<8;i++)   
        {
            result[preambleSize+nameSize+extensionSize+i]= ((j+1) & (int)1<<(8-i-1)) ? '1' : '0';  //current Package zum Frame hinzufügen  Paket Teil beginnt an Stelle 60 im Frame
            
            result[preambleSize+nameSize+extensionSize+cPackSize+i]=packagesBinary[i]; //Die totale Anzahl der Pakete bleibt immer gleich
   
        }
        
        int rest=(int) length % frameSize; 
        if(j!=packages-1||rest==0)
        {
            //Add the file content
            for(int k=frameSize*j;k<frameSize*(j+1);k++)
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
        }
        
        
        if (j==packages-1&&rest!=0)
        {
            printf("Restwert: %d \n",rest);

            //Konvertiert die Texteingabe in Binärzahlen
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
        
        //Vor dem Versenden CRC berechnen und an result dranhängen
        CalculateCRC(result,frameSize);
        
        printf("Wert von Result: ");
        
        for(int x=0; x<preambleSize+overhead+frameSize;x++)
        {
            
                printf("%c",result[x]);
        }
        printf("\n");
        //Senden der Daten
        TransferData();
    }
}



void LookForSynchro(int data)
{
    bool same=true;
    int preamble[preambleSize]={1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1}; 
    //int preamble[preambleSize]={1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1}; 
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

void Write_file(int totalPackages, char filename[], char extension[], int content[], int rest)
{
    /*
        Combine filename and extension using '.'
    */
    char buffer[12];
    snprintf(buffer, 12, "%c%c-copy.%c%c%c",  filename[0],  filename[1], extension[0], extension[1], extension[2]);

    /*
        Try creating the file
    */
    FILE *output = fopen(buffer, "wb");
    if (output == NULL) 
    {
        printf("Can not create file!\n");
    }

    /*
        For every byte, stitch its bit and write that byte to file
    */
    long size = ((frameSize*totalPackages)/8)-rest;  //frame Size times total packages
    for (long i = 0, current_index = 0; i < size; i++)
    {
        char content_byte = 0;
        for (int j = 0; j < 8; j++)
        {
            content_byte <<= 1;
            content_byte |= content[current_index++];
        }

        if (fwrite(&content_byte, 1, 1, output) != 1)
        {
            fclose(output);
            printf("Error occured!\n");
        }
    }
    fclose(output);
    receiveData_Done=true; 
    senderState=true;
}

void Print_file(int totalPackages, char filename[], char extension[], int content[], int rest)
{
       /*
        Simple print
    */
    printf("Name: %c%c\n",  filename[0],  filename[1]);
    printf("Extension: %c%c%c\n", extension[0], extension[1], extension[2]);
    printf("Content:\n");

    long size = ((frameSize*totalPackages)/8)-rest;   //frame Size times total packages
    /*
        For every byte
    */
    for (long i = 0, current_index = 0; i < size; i++)
    {
        /*
            After 8 bytes, go to new line
        */
        if (i % 8 == 0 && i != 0)
        {
            printf("\n");
        }

        /*
            Write 8 bits, with same terminology of current_index,
            increasing every time
        */
        for (long j = 0; j < 8; j++) printf("%d", content[current_index++]);

        /*
            Write space to indicate end of byte
        */
        printf(" ");
    }
    printf("\n");
}


void BitsToArray()
{ 
  for (int i=0;i<frameSize+overhead;i++)
  {dataResult[i]=dataFrame[i+preambleSize];}
  
  //Converting the Header Bits here
  char fileName[2];
  char fileEnding[3];
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
      if (i<=1) //ersten beiden Bytes sind der Name der Datei
      {fileName[i]= (char)n;}
            
      if (i>=2&&i<=4) // Byte 3, 4 und 5 sind die Endung der Datei
      {fileEnding[i-2]= (char)n;}
      
      if(i==5)
      {
         currentPackage =n;
      }
      if(i==6)
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
    printf("ZeroCounter: %d\n",zeroCounter);
    Print_file(totalPackages, fileName, fileEnding, file_content,zeroCounter);
        Write_file(totalPackages, fileName, fileEnding, file_content,zeroCounter);
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
  /**
  for(int i=0;i<n;i++){
      printf("%i",frame[i]);
    
  }
   printf("Here!\n");
  **/
  
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





void ReceiveData(int data)
{
    dataFrame[receivePos++]=data;
    
    
    
    if(receivePos==(overhead+frameSize+preambleSize))
    {
        CheckCRC();
    } 
    
}










int main()
{
    struct timeval tval_before, tval_after, tval_result;
    gettimeofday(&tval_before, NULL);
    wiringPiSetup () ;
	pinMode (0, INPUT) ;
    pinMode (1, OUTPUT) ;
    pinMode (2,OUTPUT);
    
    char mode;
    bool modeReceiver=false;
    
    
    while(1)
    {
        digitalWrite (2, HIGH);
        printf("Press the R button for Receiver Mode or any other key for Sender Mode\n");
        scanf(" %c",&mode);
        
        if (mode=='R'||mode=='r')
        {
            digitalWrite(2,LOW);
            modeReceiver=true;
        }
        
        if (mode!='R'&&mode!='r')
        {
            digitalWrite(2,LOW);
            modeReceiver=false;
            
            char dataName[NAME_MAX];
            char dataExtension[NAME_MAX];
            
               
            printf("\n Name of file WITHOUT extension: ");
            scanf("%s",dataName);

            printf("\n Extension: ");
            scanf("%s",dataExtension);

            if (read_file(dataName, dataExtension, file_content) != OK)
            {
                printf("File read error, size exceeds array size\n");
                return -1;
            }
            BuildDataFrame(dataName, dataExtension, file_content);
        }
        
        
        
        while(modeReceiver)
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
            
            //int data=0;
            //int swap= digitalRead(0);  //ACHTUNG!!!! Aus irgendeinem Grund sind die Werte dieses Bauteils invertiert. DAS IST NICHT NORMAL! 
            //if(swap==0){data=1;}
            int data = digitalRead(0);
            
            
            switch (state)
            {
                case 0:
                    //looking for preamble pattern
                    synchro_Done=false;
                    LookForSynchro(data);
                    
                    if (synchro_Done==true)
                    {
                        state=1;
                    }
                    break;
                    
                case 1:
                    //receive the actual data
                    receiveData_Done=false;
                    senderState=false;
                    ReceiveData(data);
                    
                    if(receiveData_Done&&senderState==false)
                    {
                        state=0;
                    }
                    if(senderState==true){
                        senderState=false;
                        state=0;
                        modeReceiver=false;
                        }
                    break;
                  
            }
            
        }
    }
    
    
    
    
    
    
    
    
    

    return 0;
}




