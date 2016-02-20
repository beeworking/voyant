import falcon
import hug

from .providers import PROVIDERS


@hug.get('/')
def create_vpn(key, provider, region='EUW'):
    provider = PROVIDERS.get(provider)
    if not provider:
        raise falcon.HTTPBadRequest('PROVIDER_NOT_FOUND', 'The provider does not exist.'.format(provider))

    region = provider.regions.get(region)
    if not region:
        raise falcon.HTTPBadRequest('REGION_NOT_FOUND', 'The region does not exist.'.format(region))

    provider = provider(key)
    provider.create(region)

    return {'success': True}
