import wx
import paramiko
import os


class PageTwo(wx.Panel):
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.InitUI()

    def InitUI(self):
        down_button = wx.Button(self, label="Download Logs")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(down_button, 0, wx.ALIGN_CENTER)
        self.SetSizer(sizer)
        down_button.Bind(wx.EVT_BUTTON, self.on_download)

    def on_download(self, event):
        IP = self.main_frame.get_ip_address()
        PORT = self.main_frame.get_port_number()
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(IP, port=PORT, username='root', password='evertz')
        sftp = ssh_client.open_sftp()
        sftp.get('../../var/log/messages', os.getcwd() + "\\messages.txt")
        sftp.get('../../var/log/messages.0', os.getcwd() + "\\messages1.txt")
        sftp.get('../../var/log/messages.1', os.getcwd() + "\\messages0.txt")
        sftp.close()
        ssh_client.close()
