class Provider(object):
    """Base provider class"""
    regions = {}

    def __init__(self, key):
        self.key = key

    def create(self, region):
        raise NotImplemented()

    def start(self):
        raise NotImplemented()

    def stop(self):
        raise NotImplemented()

    def destroy(self):
        raise NotImplemented()

    def list_servers(self):
        raise NotImplemented()

    def status(self):
        raise NotImplemented()

    def get_config(self, server_id):
        raise NotImplemented()

    @staticmethod
    def server_to_json(server):
        raise NotImplemented()
