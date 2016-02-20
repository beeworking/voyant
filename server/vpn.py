import hug


@hug.get('/')
def create_vpn():
    return 'Hello World !'
