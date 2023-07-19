#include <iostream>
#include <string>
#include "transceiver.h"

using namespace std;

int main()
{
    string message;
    int pin_in = 12;
    Sender sender(pin_in);
    while(1)
    {
        cout << "Enter message: "<<endl;
        cin >> message;
        sender.SendMessage(message);
    }
    return 0;
}