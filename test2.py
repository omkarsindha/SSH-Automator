import time
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect('172.17.223.24', port=22, username="mvx", password="mvx", timeout=10.0)
except (paramiko.SSHException, IOError) as err:
    print("Unable to SSH to %s: %s" % ('172.17.223.170', str(err)))

chan = ssh.invoke_shell()
commands = [
    b'cd /opt/mvx/regic\n',
    b'sudo chmod 777 proj_ifce_x86\n',
    b'mvx\n',
    b'sudo ./proj_ifce_x86 ..build_info -d\n'
]

try:
    for command in commands:
        chan.send(command)
        time.sleep(1)

    if chan.recv_ready():
        print(chan.recv(4096).decode("utf-8"))

except paramiko.SSHException as e:
    print(f"SSHException: {e}")

except Exception as ex:
    print(f"Exception: {ex}")

finally:
    chan.close()
    ssh.close()
