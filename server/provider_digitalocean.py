import uuid
import digitalocean
import os
import falcon

from urllib.request import urlopen
from passlib.hash import bcrypt

from .provider import Provider
from .mongo import mongo
from string import Template


class ProviderDigitalOcean(Provider):
    docker_image_id = 15751610
    droplet_name_prefix = 'voyant-'
    regions = {
        "AMS1": "ams1",
        "AMS2": "ams2",
        "AMS3": "ams3",
        "FRA1": "fra1",
        "NYC1": "nyc1",
        "NYC2": "nyc2",
        "NYC3": "nyc3",
        "SFO1": "sfo1",
        "SGP1": "sgp1",
        "LON1": "long1",
        "TOR1": "tor1"
    }

    def __init__(self, key):
        super().__init__(key)
        self.regions = self.get_available_regions_for_docker_image()

    def get_available_regions_for_docker_image(self):
        manager = digitalocean.Manager(token=self.key)
        dk_image = manager.get_image(self.docker_image_id)
        return {key: val for key, val in self.regions.items() if val in dk_image.regions}

    def get_droplet(self, server_id):
        manager = digitalocean.Manager(token=self.key)
        return manager.get_droplet(server_id)

    def create(self, region='nyc2'):
        file_path = os.path.join(os.path.dirname(__file__), '../scripts/setup-openvpn.sh')
        local_id = uuid.uuid4()
        droplet_name = '{}{}'.format(self.droplet_name_prefix, local_id)

        with open(file_path, 'r') as f:
            script_str = f.read()

        script_str = Template(script_str).substitute(
            VOYANT_ROOT_URL=self.hq_root_url,
            VOYANT_VPN_API_KEY=self.key,
            VOYANT_VPN_PROVIDER='digitalocean'
        )

        droplet = digitalocean.Droplet(
            token=self.key, name=droplet_name, region=region, image=self.docker_image_id,
            size_slug='512mb', backups=False, user_data=script_str
        )
        droplet.create()

        server = self.server_to_json(droplet)
        server.update({'local_id': local_id})
        mongo.servers.insert_one(server)

        return droplet

    def list_servers(self):
        manager = digitalocean.Manager(token=self.key)
        droplets = manager.get_all_droplets()
        return [droplet for droplet in droplets if self.droplet_name_prefix in droplet.name]

    def status(self, server_id):
        droplet = self.get_droplet(server_id)
        actions = droplet.get_actions()
        for action in actions:
            action.load()
            print(action.status)

    def destroy(self, server_id):
        droplet = self.get_droplet(server_id)
        droplet.destroy()

    def get_config(self, server_id):
        config = mongo.config.find_one({'_id': server_id})

        if not config:
            droplet = self.get_droplet(server_id)
            config = urlopen('https://{}:8080'.format(droplet.ip_address)).read().decode('utf-8')
            config = {'_id': server_id, 'config': config, 'key': bcrypt.encrypt(self.key)}
            mongo.config.insert_one(config)
        else:
            if not bcrypt.verify(self.key, config.get('key')):
                raise falcon.HTTPForbidden('NOT_AUTHORIZED', 'The key was not valid.')

        if 'key' in config:
            del config['key']

        return config

    @staticmethod
    def server_to_json(server):
        return {
            'id': server.id,
            'name': server.name,
            'region': server.region.get('name') if type(server.region) is dict else server.region,
            'status': server.status,
            'ip_address': server.ip_address,
        }
