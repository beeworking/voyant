from .provider_digitalocean import ProviderDigitalOcean

PROVIDERS = {
    'digitalocean': {
        "class": ProviderDigitalOcean,
        "text": "DigitalOcean",
        "value": "digitalocean",
    },
}
