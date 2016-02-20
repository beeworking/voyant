from ..vpn import create_vpn


def test_return_hello_world():
    assert create_vpn() == 'Hello World !'
