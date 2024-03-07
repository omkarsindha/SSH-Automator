import time

import wx
import paramiko
import os


class PageFour(wx.Panel):
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.scrolled_text = None
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        old_button = wx.Button(self, label="570 IPG")
        new_button = wx.Button(self, label="670 IPG")

        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.Add(old_button, 0, wx.ALIGN_LEFT)
        hBox.Add(new_button, 0, wx.ALIGN_LEFT)

        vbox.Add(hBox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        self.SetSizer(vbox)

        line = wx.StaticLine(self)
        vbox.Add(line, flag=wx.EXPAND | wx.BOTTOM, border=10)

        self.scrolled_text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.VSCROLL)
        vbox.Add(self.scrolled_text, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
        self.SetSizer(vbox)

        old_button.Bind(wx.EVT_BUTTON, self.on_old)
        new_button.Bind(wx.EVT_BUTTON, self.on_new)

    def on_old(self, event):
        self.scrolled_text.Clear()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.main_frame.get_ip_address(), port=self.main_frame.get_port_number(), username="root", password="evertz", timeout=10.0)
        except (paramiko.SSHException, IOError) as err:
            print("Unable to SSH to %s: %s" % ('172.17.223.170', str(err)))
        chan = ssh.get_transport().open_session()
        chan.get_pty()
        chan.exec_command("cd /home/sitara/fpga; ls")
        result = ""
        while chan.exit_status_ready() is False:
            if chan.recv_ready():
                result = chan.recv(4096).decode("utf-8")
                self.scrolled_text.AppendText(result)
            else:
                time.sleep(0.1)
        if chan.recv_ready() is True:
            result = chan.recv(4096).decode("utf-8")
            self.scrolled_text.AppendText(result)
        chan.close()
        ssh.close()

    def on_new(self, event):
        self.scrolled_text.Clear()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.main_frame.get_ip_address(), self.main_frame.get_port_number(), username="mvx", password="mvx", timeout=10.0)
        except (Exception, IOError) as err:
            print("Unable to SSH ")

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
                self.scrolled_text.AppendText(chan.recv(4096).decode("utf-8"))
                # print(chan.recv(4096).decode("utf-8"))

        except paramiko.SSHException as e:
            print(f"SSHException: {e}")

        finally:
            chan.close()
            ssh.close()