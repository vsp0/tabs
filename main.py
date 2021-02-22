import lib.instances as b_instances
from lib import bservers
import datetime
import json


servers = json.load(open('data/servers.json'))
instances = json.load(open('data/instances.json'))


print('Initializing servers...')

for server in servers.values():
    bservers.BServer(
        server['ip'], 
        server['user'], 
        server['server_path'],
        server['passwd'], 
        server['key_file']
    )

print('Initializing instances...')

for instance in instances.values():
    b_instances.Instance(
        instance['source'],
        instance['delay']
    )

for instance in b_instances.instances:
    print(f'Backing up instance {instance.id}...')

    instance.backup()

    delay = datetime.timedelta(seconds=instance.delay)

    instance.backup_next = datetime.datetime.now() + delay

    print(f'Successfully backed up {instance.id}, next backup scheduled to {instance.backup_next}...')


while True:
    started = datetime.datetime.now()

    for instance in b_instances.instances:
        if instance.is_time_between(started):
            print(f'Backing up instance {instance.id}...')

            instance.backup()

            delay = datetime.timedelta(seconds=instance.delay)

            instance.backup_next = datetime.datetime.now() + delay

            print(f'Successfully backed up {instance.id}, next backup scheduled to {instance.backup_next}...')
