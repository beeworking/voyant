import falcon
import hug

from .providers import PROVIDERS


@hug.post('/')
def create_vpn(key, provider, region='EU1'):
    provider = PROVIDERS.get(provider)
    if not provider:
        raise falcon.HTTPBadRequest('PROVIDER_NOT_FOUND', 'The provider does not exist.'.format(provider))

    provider = provider(key)

    region = provider.regions.get(region)
    if not region:
        raise falcon.HTTPBadRequest('REGION_NOT_FOUND', 'The region does not exist.'.format(region))

    provider.create(region)

    return {'success': True}


@hug.get('/')
def list_vpns(key, provider):
    provider = PROVIDERS.get(provider)
    if not provider:
        raise falcon.HTTPBadRequest('PROVIDER_NOT_FOUND', 'The provider does not exist.'.format(provider))

    provider = provider(key)
    return [provider.server_to_json(server) for server in provider.list_servers()]
