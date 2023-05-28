#
# Zookeeper client demo 1
#
# Basic client listing children of a node.

import os
import random
import time
from kazoo.client import KazooClient
from kazoo.recipe.lock import Lock

# Connect to ZooKeeper
ensemble = os.environ['ZOO_SERVERS']
zk = KazooClient(hosts=ensemble)
zk.start()

# Create a lock
lock = Lock(zk, '/distributed_lock')


# Function to simulate the critical section
def critical_section():
    print("Entering critical section", flush=True)
    # Sleep for a random duration between 5 and 15 seconds
    sleep_duration = random.randint(5, 15)
    time.sleep(sleep_duration)
    # Generate a random number from 1 to 100
    random_number = random.randint(1, 100)
    message = f"Process {os.getpid()} wrote: {random_number}, "
    log_msg = f"node 1: process {os.getpid()} accessing critical section "
    # Write the random number to the znode
    try:
        zk.set('/critical_section', str(message).encode())
    except KazooException as e:
        print(f"ZooKeeper error: {e}")
    finally:
        print(f"Random number {random_number} written to ZooKeeper.", flush=True)
        print(message, flush=True)
        print("Exiting critical section.", flush=True)

def handle_connection_error(zk):
    while True:
        try:
            zk.start()
            return True
        except ConnectionLoss:
            print("Connection lost. Retrying...", flush=True)
            time.sleep(5)
        except KazooException as e:
            print(f"ZooKeeper error: {e}", flush=True)

#infinite loop
def main():
    while True:
    #try to acquire lock
        if lock.acquire(blocking=False):
            try:
                if not zk.connected:
                    handle_connection_error(zk)
                critical_section()
            finally:
                lock.release()
                time.sleep(50) #add for reasons
        else:
            retry_delay = random.randint(5, 15)
            print(f"Could not enter critical section retrying in {retry_delay}", flush=True)
            time.sleep(retry_delay)

if not zk.exists('/critical_section'):
    try:
        zk.create('/critical_section')
    except NodeExistsError:
        print("File Exists", flush=True)
    except KazooException as e:
        print(f"ZooKeeper error: {e}", flush=True)
    finally:
        main()


#
# EOF
#
