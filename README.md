# tabs
Tabs is a backup program that backs up your local files, and transfers them to one or multiple remote servers using ssh.

## Installation

1. Clone or download the repository on a place on your local computer using the command:

    `git clone https://github.com/vsp0/tabs.git`

2. Modify `data/bservers.json` and add a remote server with an open ssh port (22), like this:
    ```json
    {
        "server_name": {
            "ip": "192.168.1.1",
            "user": "root",
            "server_path": "/home/root/Desktop/tabs_backup/",
            "passwd": "password_to_remote_server",
            "key_file": "key_to_remote_server.pem"
        }
    }
    ```

    `ip` is the ip of the remote backup server.
    
    `user` is the user of the remote backup server, this could be `root` for example.

    `server_path` is the path to where you want to store your files on the remote server.

    `passwd` is the password of the remote backup server.

    `key_file` is the key file for the remote backup server, some severs may require this to login using ssh.

    **NOTE: Either `passwd` or `key_file` is required.**

    You can add as many remote servers as you'd like, but only one is required. 


3. Modify `data/instances.json` and add a backup instance, like this:

    ```json
    {
        "instance_name": {
            "source": "C:/Users/user/Desktop/my_important_images",
            "delay": "120"
        }
    }
    ```

    `source` is the path to what you want `tabs` to backup.
    
    `delay` is the delay (specified in seconds) of how often tabs is going to backup to the different backup servers.

4. Now run `main.py` and it will automatically start backing up to the different backup servers.
