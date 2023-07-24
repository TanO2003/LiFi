#include "Trans.h"

using namespace std;

const int delay_ms = 10;
const int pin = 2;

int main()
{
    Sender sender(pin);
    string text;
    while (1)
    {
        cout<<"Enter your message: ";
        cin>>text;
        sender.SendMessage(text, delay_ms);
    }

    return 0;
}
