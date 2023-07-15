import numpy as np


def hamming_encode(data):
    """
    Hamming encode the data
    :param data: data to be encoded
    :return: encoded data
    """
    # Generate the parity bits
    parity = np.zeros(3)
    for i in range(3):
        parity[i] = np.sum(data[2 ** i - 1::2 ** (i + 1)])

    # Add the parity bits to the data
    data = np.insert(data, [0, 1, 3], parity)

    return data
