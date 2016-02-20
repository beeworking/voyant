import falcon
import hug

from .mongo import mongo
from .providers import PROVIDERS


@hug.post('/')
def create_vpn(key, provider, region='EU1'):
    provider = PROVIDERS.get(provider)
    if not provider:
        raise falcon.HTTPBadRequest('PROVIDER_NOT_FOUND', 'The provider does not exist.')

    provider = provider(key)

    region = provider.regions.get(region)
    if not region:
        raise falcon.HTTPBadRequest('REGION_NOT_FOUND', 'The region does not exist.')

    server = provider.create(region)

    return provider.server_to_json(server)


@hug.get('/')
def list_vpns(key, provider):
    provider = PROVIDERS.get(provider)
    if not provider:
        raise falcon.HTTPBadRequest('PROVIDER_NOT_FOUND', 'The provider does not exist.')

    provider = provider(key)
    return [provider.server_to_json(server) for server in provider.list_servers()]


@hug.delete('/')
def destroy_vpn(key, provider, vpn_id):
    provider = PROVIDERS.get(provider)
    if not provider:
        raise falcon.HTTPBadRequest('PROVIDER_NOT_FOUND', 'The provider does not exist.')

    provider = provider(key)

    try:
        provider.destroy(vpn_id)
    except:
        raise falcon.HTTPBadRequest('VPN_NOT_FOUND', 'The vpn \'{}\' does not exist.'.format(vpn_id))

    return {'success': True}


@hug.get('/config')
def get_config(key, provider, vpn_id):
    provider = PROVIDERS.get(provider)
    if not provider:
        raise falcon.HTTPBadRequest('PROVIDER_NOT_FOUND', 'The provider does not exist.')

    provider = provider(key)
    config = provider.get_config(vpn_id)

    return config


@hug.get('/config/download', output=hug.output_format.text)
def get_file(vpn_id):
    config = mongo.config.find_one({'_id': vpn_id})

    config = config.get('config')
    return config
