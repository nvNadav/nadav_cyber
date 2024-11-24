def twos_complement(value, bit_width):
    flipped_value = ~value
    twos_complement_value = flipped_value + 1
    return format(twos_complement_value & ((1 << bit_width) - 1), f'0{bit_width}b')


print (twos_complement(42,8))#output: 11010110