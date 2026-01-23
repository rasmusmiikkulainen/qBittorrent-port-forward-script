# qBittorrent automatic port forward script
This is a simple script to automatically get the port forwarded in Gluetun and set the same port as qBittorrent's listening port.
## Features
- Gets the current forwarded port from Gluetun
- Logs in to qBittorrent's Web API
- Compares qBittorrent's listening port to the one forwarded in Gluetun
- Updates qBittorrent's port if they differ
- Logs out of qBittorrent
## Configuration
Edit the values at the top of the script to match your setup:
```python
gluetun = "http://localhost:8003"       # Gluetun API address
qbittorrent = "http://localhost:8081"   # qBittorrent Web API address
qbittorrent_user = "admin"              # qBittorrent username
qbittorrent_pass = "adminadmin"         # qBittorrent password
```
Make sure that the provided addresses are reachable.
## Usage
This script is designed to be used with cron. You could for example run this every 15 minutes by running `crontab -e` and inputting this:
```
*/15 * * * * python3 /path/to/qbittorrent-port.py
```
However, you can also just use this manually. Typical output of the script looks something like this:
```
Port forwarded in Gluetun: 51423
qBittorrent login succesful.
qBittorrent listening port: 48210
Success! qBittorrent port changed to 51423
```
## Future improvements
- Validate status codes
- Add error handling with try/except
- Retry logic