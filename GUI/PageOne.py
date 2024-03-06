import wx
import threading
import paramiko
import time


class LogThread(threading.Thread):
    def __init__(self, parent, ip, port):
        threading.Thread.__init__(self)
        self.parent = parent
        self.ip = ip
        self.port = port
        self.stop_flag = False

    def run(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.ip, port=self.port, username="root", password="evertz", timeout=10.0)
        except (paramiko.SSHException, IOError) as err:
            print("Unable to SSH to %s: %s" % (self.ip, str(err)))

        chan = ssh.get_transport().open_session()
        chan.get_pty()
        chan.exec_command("tail -f ../../var/log/messages")

        while chan.exit_status_ready() is False:
            if not self.stop_flag:
                if chan.recv_ready():
                    result = chan.recv(4096).decode("utf-8")
                    wx.CallAfter(self.parent.update_text, result)
                else:
                    time.sleep(0.1)
            else:
                chan.close()
                ssh.close()

    def stop_logs(self):
        self.stop_flag = True


class PageOne(wx.Panel):
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.scrolled_text = None
        self.ip_text = None
        self.InitUI()
        self.Center()
        self.log_thread = None

    def InitUI(self):

        vbox = wx.BoxSizer(wx.VERTICAL)

        hBox1 = wx.BoxSizer(wx.HORIZONTAL)

        log_button = wx.Button(self, label='Get Logs')
        log_button.Bind(wx.EVT_BUTTON, self.on_get_logs)

        hBox1.Add(log_button)

        stop_log = wx.Button(self, label='Stop printing')
        stop_log.Bind(wx.EVT_BUTTON, self.on_stop_logs)

        hBox1.Add(stop_log)

        clear = wx.Button(self, label='Clear')
        clear.Bind(wx.EVT_BUTTON, self.on_clear)

        hBox1.Add(clear)

        vbox.Add(hBox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 10))
        line = wx.StaticLine(self)
        vbox.Add(line, flag=wx.EXPAND | wx.BOTTOM, border=10)

        self.scrolled_text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.VSCROLL)
        vbox.Add(self.scrolled_text, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
        self.SetSizer(vbox)
        self.SetSizer(vbox)

    def on_get_logs(self, event):
        self.log_thread = LogThread(self, self.main_frame.get_ip_address(), self.main_frame.get_port_number())
        self.log_thread.start()

    def on_stop_logs(self, event):
        self.log_thread.stop_logs()

    def update_text(self, result):
        self.scrolled_text.AppendText(result)

    def on_clear(self, result):
        self.scrolled_text.Clear()
