import uuid
import digitalocean
import os
from .provider import Provider


class ProviderDigitalOcean(Provider):
    regions = {
        "EU1": "ams1",
        "US1": "nyc1",
        "US2": "nyc2",
    }

    def create(self, region='nyc2'):
        file_path = os.path.join(os.path.dirname(__file__), '../scripts/setup-openvpn.sh')
        droplet_name = 'voyant-{}'.format(uuid.uuid4())

        with open(file_path, 'r') as f:
            script_str = f.read()

        droplet = digitalocean.Droplet(
            token=self.key, name=droplet_name, region=region, image=15751610,
            size_slug='512mb', backups=False, user_data=script_str
        )
        droplet.create()

        return droplet.id

    def list_servers(self):
        manager = digitalocean.Manager(token=self.key)

        return manager.get_all_droplets()

    def status(self, server_id):
        manager = digitalocean.Manager(token=self.key)
        droplet = manager.get_droplet(server_id)

        actions = droplet.get_actions()
        for action in actions:
            action.load()
            print(action.status)
