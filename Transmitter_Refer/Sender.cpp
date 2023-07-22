#include <iostream>
#include <string>
#include "transceiver.h"

using namespace std;

int main()
{
    string message;
    int pin_out = 3;
    Sender sender(pin_out);
    while(1)
    {
        cout << "Enter message: "<<endl;
        cin >> message;
        sender.SendMessage(message);
    }
    return 0;
}