# TORify
A script that routes all system traffic through the TOR network, acting like a VPN, allowing anonymous browsing with country selection and dynamic IP changes.

![image](https://github.com/user-attachments/assets/d1a172f6-8f0c-4e59-83c6-44ce6c9b9221)

## Installation
- `git clone https://github.com/OusCyb3rH4ck/TORify`
- `cd TORify`
- `sudo python3 -m pip install --break-system-packages --upgrade pwn colorama requests argparse`
- `chmod +x TORify`

## Usage (run as root or use "sudo")
- `sudo ./torify.py`

#### Show available countries:
- `sudo ./torify.py -sc`
#### Connect to TOR (like a VPN)
- `sudo ./torify.py -s` and put the country codename when asked.
#### Change the IP using the same country
- `sudo ./torify.py -c `
#### Disconnect
- `sudo ./torify.py -d`
