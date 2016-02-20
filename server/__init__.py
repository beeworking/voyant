import hug
from . import vpn


@hug.get('/')
def main():
    return "Hello World !"


@hug.extend_api('/api')
def vpn_api():
    return [vpn]
