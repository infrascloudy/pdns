class BimapError(Exception):
    pass


class Bimap(object):
    def __init__(self, name, forward, error=KeyError):
        self.name = name
        self.error = error
        self.forward = forward.copy()
        self.reverse = dict([(v,k) for (k,v) in list(forward.items())])

    def get(self, k, default=None):
        try:
            return self.forward[k]
        except KeyError:
            return default or str(k)

    def __getitem__(self, item):
        try:
            return self.forward[item]
        except KeyError:
            raise self.error('%s: Invalid forward lookup: [%s]' % (self.name, item))

    def __getattr__(self, item):
        try:
            return self.reverse[item]
        except KeyError:
            raise self.error("%s: Invalid reverse lookup: [%s]" % (self.name, item))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
