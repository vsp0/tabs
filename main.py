import lib.instances as b_instances
from lib import bservers
import datetime
import json


servers = json.load(open('creds/servers.json'))
instances = json.load(open('creds/instances.json'))

for server in servers.values():
    bservers.BServer(
        server['ip'], 
        server['user'], 
        server['passwd'], 
        server['key_file']
    )

for instance in instances.values():
    b_instances.Instance(
        instance['source'],
        instance['delay']
    )

for instance in b_instances.instances:
    instance.backup()

    delay = datetime.timedelta(seconds=instance.delay)

    instance.backup_next = datetime.datetime.now() + delay


while True:
    started = datetime.datetime.now()

    for instance in b_instances.instances:
        if instance.is_time_between(started):
            instance.backup()

            delay = datetime.timedelta(seconds=instance.delay)

            instance.backup_next = datetime.datetime.now() + delay
