class Provider(object):
    """Base provider class"""
    regions = {}

    def __init__(self, key=''):
        self.key = key

    def create(self, region, name='hello'):
        raise NotImplemented()

    def start(self):
        raise NotImplemented()

    def stop(self):
        raise NotImplemented()

    def dstroy(self):
        raise NotImplemented()

    def list_servers(self):
        raise NotImplemented()

    def status(self):
        raise NotImplemented()
