#include "Trans.h"

using namespace std;

const int delay_ms = 10;
const int pin = 22;

int main()
{
    Receiver receiver(pin);
    while (1)
    {
        string message = receiver.ReceiveMessage(delay_ms);
        if (message != "")
        {
            cout << "Message: " << message << endl;
        }
    }
    return 0;
}