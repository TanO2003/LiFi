def str_2_bin(str):
    """
    字符串转换为二进制
    """
    return '#'.join([bin(ord(c)).replace('0b', '') for c in str])


def bin_2_str(bin):
    """
    二进制转换为字符串
    """
    return ''.join([chr(i) for i in [int(b, 2) for b in bin.split('#')]])

a = input("请输入字符串：")
print(str_2_bin(a))
print(bin_2_str(str_2_bin(a)))