# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 00:50:54 2017

@author: jarrod
"""

data=(0x84,0xb0,0x7f,0xef,0x00,0x02)
length=len(data)
#answer: E0
crc=0x00
crc ^= 0xff
i=0
while length:
    crc ^= data[i]
    i += 1
    for k in range(8):
        if (crc & 0x80):
            crc = (crc << 1) ^ 0x1d
            print(hex(crc))
        else:
            crc << 1
            print("else")
            print(hex(crc))
        crc &= 0xff;
    length -= 1
crc &= 0xff;
crc ^= 0xff;
print(hex(crc))

"""
#include <stdint.h>

unsigned crc8sae_j1850_bit(unsigned crc, unsigned char const *data, size_t len) {
    if (data == NULL)
        return 0;
    crc ^= 0xff;
    while (len--) {
        crc ^= *data++;
        for (unsigned k = 0; k < 8; k++)
            crc = crc & 0x80 ? (crc << 1) ^ 0x1d : crc << 1;
    }
    crc &= 0xff;
    crc ^= 0xff;
    return crc;
}
"""