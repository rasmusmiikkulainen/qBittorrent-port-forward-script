import requests

gluetun = "http://localhost:8003"       # Gluetun API address
qbittorrent = "http://localhost:8081"   # qBittorrent Web UI/API address
qbittorrent_user = "admin"              # qBittorrent username
qbittorrent_pass = "adminadmin"         # qBittorrent password

# TODO:
# error handling (status codes, try/except)

def getGluetun():
    """
    Gets the forwarded port in Gluetun using it's API.
    Returns:
        returns a tuple of the following:
        index 0: whether or not the operation was succesful (True/False)
        index 1: the port forwarded in gluetun (only if index 0 == True)
    """
    net = requests.get(f"{gluetun}/v1/portforward")
    if str(net.json()["port"]).isnumeric():
        gluetun_port = int(net.json()["port"])
        print(f"Port forwarded in Gluetun: {gluetun_port}")
        return (True, gluetun_port)
    else:
        print("Gluetun port not found")
        return (False)

def torrentLogin():
    """
    Log in to the qBittorrent API.
    Returns:
        returns a tuple of the following:
        index 0: whether or not the operation was succesful (True/False)
        index 1: qBittorrent login cookie (only if index 0 == True)
    """
    net = requests.post(f"{qbittorrent}/api/v2/auth/login", data={"username": qbittorrent_user, "password": qbittorrent_pass})
    if net.text == "Ok.":
        print("qBittorrent login succesful.")
        return (True, net.cookies)
    else:
        print("qBittorrent login failed.")
        return (False)

def changePort(cookies, gluetun_port):
    """
    Change the active port in qBittorrent
    Params:
        cookies: login cookie from torrentLogin()
        gluetun_port: the port number to change the qBittorrent port to
    """
    net = requests.get(
        f"{qbittorrent}/api/v2/app/preferences", cookies=cookies)
    torrent_port = net.json()["listen_port"]
    print(f"qBittorrent listening port: {torrent_port}")
    if torrent_port != gluetun_port:
        requests.post(f"{qbittorrent}/api/v2/app/setPreferences", cookies=cookies, json={"listen_port": gluetun_port})
        if requests.get(f"{qbittorrent}/api/v2/app/preferences", cookies=cookies).json()["listen_port"] == gluetun_port:
            print(f"Success! qBittorrent port changed to {gluetun_port}")
        else:
            print(f"Failed to set new qBittorrent port.")
    else:
        print("Ports already match, no action required.")
    requests.post(f"{qbittorrent}/api/v2/auth/logout", cookies=cookies)

def autoPort():
    """
    Program flow
    """
    gluetun = getGluetun()
    if gluetun[0]:
        torrent_login = torrentLogin()
        if torrent_login[0]:
            changePort(torrent_login[1], gluetun[1])

autoPort()
