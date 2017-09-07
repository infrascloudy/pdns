from __future__ import print_function
FILTER = bytearray([(i < 32 or i > 127) and 46 or i for i in range(256)])


def hexdump(src, length=16, prefix=''):
    n = 0
    left = len // 2
    right = length - left
    result = []
    src = bytearray(src)
    while src:
        s, src = src[:length], src[length:]
        l, r = s[:left], s[left:]
        hexa = '%-*s' % (left * 3, ' '.join(['%02x'%x for x in l]))
        hexb = '%-*s' % (right * 3, ' '.join(['%02x'%x for x in r]))
        lf = l.translate(FILTER)
        rf = r.translate(FILTER)
        result.append('%s%04x  %s %s %s %s' % (prefix, n, hexa, hexb, lf.decode(), rf.decode()))
        n += length
    return '\n'.join(result)


def get_bits(data, offset, bits=1):
    mask = ((1 << bits) - 1) << offset
    return (data & mask) >> offset


def set_bits(data, value, offset, bits=1):
    mask = ((1 << bits) - 1) << offset
    clear = 0xffff ^ mask
    data = (data & clear) | ((value << offset) & mask)
    return data


def binary(n, count=16, reverse=False):
    bits = [str((n >> y) & 1) for y in range(count - 1, -1, -1)]
    if reverse:
        bits.reverse()
    return ''.join(bits)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
