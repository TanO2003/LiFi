from __future__ import print_function
from time import sleep
from sys import stdout
from daqhats import mcc118, OptionFlags, HatIDs, HatError
from daqhats_utils import select_hat_device

# Constants
CURSOR_BACK_2 = '\x1b[2D'
ERASE_TO_END_OF_LINE = '\x1b[0K'


def V2D(chan,threshold, interval):
    """
    将电压转换为高低电平，chan为模拟输入的通道，threshold为阈值
    """
    options = OptionFlags.DEFAULT
    mcc_118_num_channels = mcc118.info().NUM_AI_CHANNELS
    sample_interval = interval  # Seconds

    try:
        # Get an instance of the selected hat device object.
        address = select_hat_device(HatIDs.MCC_118)
        hat = mcc118(address)



        try:
            a = ''
            i = 0
            while i < 2:
                value = hat.a_in_read(chan, options)
                
                if value < threshold:
                    a += '0'
                else:
                    a += '1'
                
                stdout.flush()

                # Wait the specified interval between reads.
                sleep(sample_interval)    
                
                if a[-8:] == "10000001":
                    i += 1
            
            return a
                    
            


        

        except KeyboardInterrupt:
            # Clear the '^C' from the display.
            print(CURSOR_BACK_2, ERASE_TO_END_OF_LINE, '\n')

    except (HatError, ValueError) as error:
        print('\n', error)