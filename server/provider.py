class Provider(object):
    """Base provider class"""
    regions = {}

    def __init__(self, key=''):
        self.key = key

    def create(self):
        raise NotImplemented()

    def start(self):
        raise NotImplemented()

    def stop():
        raise NotImplemented()

    def dstroy():
        raise NotImplemented()

    def list_servers():
        raise NotImplemented()

    def status():
        raise NotImplemented()
