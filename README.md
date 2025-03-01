# TORify
A script that routes all system traffic through the TOR network, acting like a VPN, allowing anonymous browsing with country selection and dynamic IP changes.

![image](https://github.com/user-attachments/assets/d1a172f6-8f0c-4e59-83c6-44ce6c9b9221)

## Installation
- `git clone https://github.com/OusCyb3rH4ck/TORify`
- `cd TORify`
- `sudo python3 -m pip install --break-system-packages --upgrade pwn colorama requests argparse`
- `chmod +x torify.py`

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

## Instructions if the IP does not change with the '-c' parameter
  1. Change country by modifying the "**/etc/tor/torrc**" file
    ![image](https://github.com/user-attachments/assets/3c628494-735e-4c47-b32a-0c58a8988485)

  2. Use "NetCat" to force a node or IP change

     2.1: Create a hash with the password to connect
       ```bash
        tor --hash-password "test123"
       ```
      2.2: Copy the resulting hash and paste it into this part of the "**/etc/tor/torrc**" file
        ![Pasted image 20250226164811](https://github.com/user-attachments/assets/fe34dbf8-13e3-44b8-9fc2-ae7dd46fa05c)

      2.3: Restart the TOR service to save the changes
        ```bash
        sudo systemctl restart tor
        ```
      2.4: Connect with "**NetCat**" to the service and run the following commands:
        ```bash
        nc 127.0.0.1 9051

          AUTHENTICATE "16:B190..."
          SIGNAL NEWNYM
        ```
      2.5:  If you receive "**250 OK**" on both commands executed in "**NetCat**", it's done (_the IP and nodes will have changed_)
        - Verify on "_whoer.net_" or using the "**nyx**" tool.
