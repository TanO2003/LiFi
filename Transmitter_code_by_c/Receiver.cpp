#include "transceiver.h"
#include <iostream>
#include <string>

using namespace std;

int main()
{
    int pin_in = 12;
    string message;
    Receiver receiver(pin_in);
    while (true)
    {
        receiver.ReceiveMessage();
        if (receiver.message != ""){
        cout << receiver.message << endl;}
    }
}