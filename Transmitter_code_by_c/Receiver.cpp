#include "transceiver.h"
#include <iostream>
#include <string>

using namespace std;

int main()
{
    int pin_out = 3;
    string message;
    Receiver receiver(pin_out);
    while (true)
    {
        message = receiver.receive();
        cout << message << endl;
    }
}