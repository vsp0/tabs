import paramiko

bservers = []


class BServer:
    def __init__(self, ip, user, server_path, passwd=None, key_file=None):
        self.ip = ip
        self.user = user
        self.server_path = server_path

        self.passwd = passwd
        self.key_file = key_file

        bservers.append(self)
    
    def can_connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(
                self.ip, 
                username=self.user, 
                password=self.passwd, 
                key_filename=self.key_file)
        
        except:
            return False
        
        return True


def get_target(bserver, instance):
    if bserver.server_path.endswith('/'):
        return bserver.server_path + f"{instance.id}"
    
    return bserver.server_path + f"/{instance.id}"
