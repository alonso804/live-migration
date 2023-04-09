import os
from time import sleep
from multiprocessing import Process
import subprocess

PORT = 6692

def configure(target):
    print('Preparing ...')
    os.system(f'vboxmanage modifyvm {target} --teleporter off --teleporterport {PORT}')
    os.system(f'vboxmanage modifyvm {target} --teleporter on --teleporterport {PORT}')


def start_vm(target):
    os.system(f'vboxmanage startvm {target}')


def teleport(source):
    print('-- Start teleport ---')
    os.system(f'vboxmanage controlvm {source} teleport --host 127.0.0.1 --port {PORT}')
    print('-- Finish teleport ---')


def get_metrics(vm):
    metrics = subprocess.getoutput(f'vboxmanage metrics query {vm} CPU/Load/Kernel,RAM/Usage/Used')
    [cpu_str, ram_str] = metrics.split('\n')[-2:]
    cpu = cpu_str.split(' ')[-1]
    ram = ram_str.split(' ')[-2]

    return float(cpu[:-1]) * 10, float(ram) / (1024 * 1024)


def migration(source, target):
    configure(target)
    sleep(3)

    print(f'Starting virtual machine {source} ...')
    # process = Process(target=start_vm, args = (target))
    # process.start()
    # sleep(3)

    # teleport(source)


def live_migration(source, target):
    if True:
        teleport(source)

    cpu, ram = get_metrics(source)

    print(f'{cpu}%')
    print(f'{ram} GB')
    print()

    #if cpu >= 30 and ram >= 1.2:
    #    migration(source, target)
    
    sleep(1)


if __name__ == '__main__':
    while True:
        #live_migration('ubuntu_source_1', 'ubuntu_source_3')
        live_migration('ubuntu_destination_2', 'ubuntu_destination_4')
