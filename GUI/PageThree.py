import time
import wx
import paramiko


class PageThree(wx.Panel):
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.scrolled_text = None
        self.InitUI()
        self.log_thread = None

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        date_button = wx.Button(self, label="Date")

        lspci_button = wx.Button(self, label="lspci")

        ifconfig_button = wx.Button(self, label="IfConfig")

        top_button = wx.Button(self, label="Top")

        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.Add(date_button, 0, wx.ALIGN_LEFT)
        hBox.Add(lspci_button, 0, wx.ALIGN_LEFT)
        hBox.Add(ifconfig_button, 0, wx.ALIGN_LEFT)
        hBox.Add(top_button, 0, wx.ALIGN_LEFT)

        vbox.Add(hBox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        self.SetSizer(vbox)

        line = wx.StaticLine(self)
        vbox.Add(line, flag=wx.EXPAND | wx.BOTTOM, border=10)

        self.scrolled_text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.VSCROLL)
        vbox.Add(self.scrolled_text, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
        self.SetSizer(vbox)

        date_button.Bind(wx.EVT_BUTTON, self.on_date)
        lspci_button.Bind(wx.EVT_BUTTON, self.on_lspci)
        ifconfig_button.Bind(wx.EVT_BUTTON, self.on_ifconfig)
        top_button.Bind(wx.EVT_BUTTON, self.on_top)

    def on_date(self, event):
        self.scrolled_text.Clear()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.main_frame.get_ip_address(), port=self.main_frame.get_port_number(), username="root",
                        password="evertz", timeout=5.0)
        except (paramiko.SSHException, IOError) as error:
            print("Some error occurred during SSH \n %s" % str(error))

        chan = ssh.get_transport().open_session()
        chan.get_pty()
        chan.exec_command("date")
        time.sleep(1)
        if chan.recv_ready() is True:
            self.scrolled_text.AppendText(chan.recv(4096).decode("utf-8"))

        chan.close()
        ssh.close()

    def on_lspci(self, event):
        self.scrolled_text.Clear()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.main_frame.get_ip_address(), port=self.main_frame.get_port_number(), username="root",
                        password="evertz", timeout=5.0)
        except (paramiko.SSHException, IOError) as error:
            print("Some error occurred during SSH \n %s" % str(error))

        chan = ssh.get_transport().open_session()
        chan.get_pty()
        chan.exec_command("lspci")

        time.sleep(2)

        if chan.recv_ready() is True:
            self.scrolled_text.AppendText(chan.recv(4096).decode("utf-8"))

        chan.close()
        ssh.close()

    def on_ifconfig(self, event):
        self.scrolled_text.Clear()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.main_frame.get_ip_address(), port=self.main_frame.get_port_number(), username="root",
                        password="evertz", timeout=5.0)
        except (paramiko.SSHException, IOError) as error:
            print("Some error occurred during SSH \n %s" % str(error))

        chan = ssh.get_transport().open_session()
        chan.get_pty()
        chan.exec_command("ifconfig")

        while chan.exit_status_ready() is False:
            if chan.recv_ready():
                result = chan.recv(4096).decode("utf-8")
                self.scrolled_text.AppendText(result)
            else:
                time.sleep(0.1)
        if chan.recv_ready() is True:
            self.scrolled_text.AppendText(chan.recv(4096).decode("utf-8"))

        chan.close()
        ssh.close()

    def on_top(self, event):
        self.scrolled_text.Clear()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.main_frame.get_ip_address(), port=self.main_frame.get_port_number(), username="root",
                        password="evertz", timeout=5.0)
        except (paramiko.SSHException, IOError) as error:
            print("Some error occurred during SSH \n %s" % str(error))

        chan = ssh.get_transport().open_session()
        chan.get_pty()
        chan.exec_command("top")

        time.sleep(2)
        if chan.recv_ready() is True:
            self.scrolled_text.AppendText(chan.recv(4096).decode("utf-8"))

        chan.close()
        ssh.close()

