"""
This module allows someone to create a list of IP addresses and host
names and pings them to let the user know if they are up or down. It can notify
users via email when they are up.
"""
import os
import sys
import time
from subprocess import Popen, PIPE

import email_utility


class PingNotifier(object):
    def __init__(self):
        """Create a class capable of pinging network addresses"""
        os.system('cls')

        # Declare instance variables
        self.hosts = []
        self.offline_hosts = []

        # Populate the host list
        self.create_host_list()

    def create_host_list(self):
        """Create a list of network addresses through user input"""
        # Get first network address and add to list
        net_address = input('What is a network address you want to ping? ')
        self.hosts.append(net_address)

        # Find out if user wants to add more network addresses
        while True:
            add_another = input('Add another? (y/n) ')
            print()
            if add_another.lower() == 'n' or add_another.lower() == 'no':
                break
            elif add_another.lower() == 'y' or add_another.lower() == 'yes':
                net_address = input("What is a network address you want to ping? ")
                self.hosts.append(net_address)
            else:
                print("That is an invalid input.")
        print()
        os.system('cls')

    def check_ping(self):
        """Checks list of network addresses to see if they are up or down"""
        # Print ping status of all of your hosts, minimum padding of 8 spaces
        padding_size = max(len(max(self.hosts, key=len)) + 4, 8)
        print('{:{padding_size}}{}'.format('Host', 'Status', padding_size=padding_size))
        for host in self.hosts:
            # Get output of ping command
            output = str(Popen('ping -n 1 {}'.format(host), stdout=PIPE).communicate()[0])

            result = '{:{padding_size}}'.format(host, padding_size=padding_size)
            if 'unreachable' in output:
                result = result + 'Offline - unreachable'
                self.offline_hosts.append(host)
            elif 'could not find' in output:
                result = result + 'Offline - could not find'
                self.offline_hosts.append(host)
            elif 'transmit failed' in output:
                result = result + 'Offline - transmit failed'
                self.offline_hosts.append(host)
            elif 'timed out' in output:
                result = result + 'Offline - timed out'
                self.offline_hosts.append(host)
            else:
                result = result + 'Online'
            print(result)
        print()

    def track_down(self):
        """Continuously pings a list of network hosts until they are up"""
        num_down = len(self.offline_hosts)
        if num_down > 0:
            if num_down == 1:
                notify_question = "Would you like to be notified when the 1 device is up? (y/n) "
            else:
                notify_question = "Would you like to be notified when those %d devices are up? (y/n) " % (len(self.offline_hosts))
            while True:
                notify = input(notify_question)
                if notify.lower() == 'n' or notify.lower() == 'no':
                    input('Program complete. Press enter to exit.')
                    sys.exit()
                elif notify.lower() == 'y' or notify.lower() == 'yes':
                    # Start the EmailUtility
                    print()
                    email_util = email_utility.EmailUtility()

                    while len(self.offline_hosts) > 0:
                        for host in self.offline_hosts:
                            # Get output of ping command
                            output = str(Popen('ping -n 1 {}'.format(host), stdout=PIPE).communicate()[0])

                            result = '{:20}'.format(host)
                            if 'unreachable' in output:
                                print(host, 'is still down.')
                            elif 'could not find' in output:
                                print(host, 'is still down.')
                            elif 'transmit failed' in output:
                                print(host, 'is still down.')
                            elif 'timed out' in output:
                                print(host, 'is still down.')
                            else:
                                print(host + ' is up. Will attempt to send an email notification.')
                                email_util.send_email(host)
                                self.offline_hosts.remove(host)
                        time.sleep(15)
                    email_util.quit_smtp_session()
                    print()
                    break
                else:
                    print("That is an invalid input.\n")
        else:
            print('No hosts to track down.')


if __name__ == '__main__':
    pn = PingNotifier()
    pn.check_ping()
    pn.track_down()
    input('Program complete. Press enter to exit.')
