from __future__ import print_function
import base64, binascii, calendar, collections, copy, os.path, random, socket, string, struct, textwrap, time
from itertools import chain

from pdns.bit import get_bits, set_bits
from pdns.bimap import Bimap, BimapError
from pdns.buffer import Buffer, BufferError


try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest


class DNSError(Exception):
    pass

# DNS codes

QTYPE = Bimap(
    'QTYPE',
    {1: 'A',
     2: 'NS',
     5: 'CNAME',
     6: 'SOA',
     12: 'PTR',
     15: 'MX',
     16: 'TXT',
     17: 'RP',
     18: 'AFSDB',
     24: 'SIG',
     25: 'KEY',
     28: 'AAAA',
     29: 'LOC',
     33: 'SRV',
     35: 'NAPTR',
     36: 'KX',
     37: 'CERT',
     38: 'A6',
     39: 'DNAME',
     41: 'OPT',
     42: 'APL',
     43: 'DS',
     44: 'SSHFP',
     45: 'IPSECKEY',
     46: 'RRSIG',
     47: 'NSEC',
     48: 'DNSKEY',
     49: 'DHCID',
     50: 'NSEC3',
     51: 'NSEC3PARAM',
     52: 'TLSA',
     55: 'HIP',
     99: 'SPF',
     249: 'TKEY',
     250: 'TSIG',
     251: 'IXFR',
     252: 'AXFR',
     255: 'ANY',
     257: 'CAA',
     32768: 'TA',
     32769: 'DLV'}, DNSError)

CLASS = Bimap(
    'CLASS',
    {1: 'IN',
     2: 'CS',
     3: 'CH',
     4: 'Hesiod',
     254: 'None',
     255: '*'}, DNSError)

QR = Bimap(
    'QR',
    {0: 'QUERY',
     1: 'RESPONSE'}, DNSError)

RCODE = Bimap(
    'RCODE',
    {0: 'NOERROR',
     1: 'FORMERR',
     2: 'SERVFAIL',
     3: 'NXDOMAIN',
     4: 'NOTIMP',
     5: 'REFUSED',
     6: 'YXDOMAIN',
     7: 'YXRRSET',
     8: 'NXRRSET',
     9: 'NOTAUTH',
     10: 'NOTZONE'},
    DNSError)

OPCODE = Bimap(
    'OPCODE',
    {0: 'QUERY',
     1: 'IQUERY',
     2: 'STATUS',
     5: 'UPDATE'},
    DNSError)


def label(label, origin=None):
    if label.endswith('.'):
        return DNSLabel(label)
    else:
        return (origin if isinstance(origin, DNSLabel) else DNSLabel(origin)).add(label)

