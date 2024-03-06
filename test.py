import time
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect('172.17.223.170', port=22, username="root", password="evertz", timeout=10.0)
except (paramiko.SSHException, IOError) as err:
    print("Unable to SSH to %s: %s" % ('172.17.223.170', str(err)))
chan = ssh.get_transport().open_session()
chan.get_pty()
chan.exec_command("cd /home/sitara/fpga; ls")
result = ""
while chan.exit_status_ready() is False:
    if chan.recv_ready():
        result = chan.recv(4096).decode("utf-8")
        print(result)
    else:
        time.sleep(0.1)
if chan.recv_ready() is True:
    print(chan.recv(4096).decode("utf-8"))
chan.close()
ssh.close()
