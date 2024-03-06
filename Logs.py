import wx
import time
import paramiko
import threading


class LogThread(threading.Thread):
    def __init__(self, parent, ip):
        threading.Thread.__init__(self)
        self.parent = parent
        self.ip = ip
        self.stop_flag = False

    def run(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.ip, port=22, username="root", password="evertz", timeout=10.0)
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


class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)
        self.scrolled_text = None
        self.ip_text = None
        self.InitUI()
        self.Center()
        self.log_thread = None

    def InitUI(self):
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hBox1 = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(panel, label='IP: ')
        hBox1.Add(label, flag=wx.RIGHT, border=8)

        self.ip_text = wx.TextCtrl(panel)
        hBox1.Add(self.ip_text, flag=wx.RIGHT, border=8)

        log_button = wx.Button(panel, label='Get Logs')
        log_button.Bind(wx.EVT_BUTTON, self.on_get_logs)

        hBox1.Add(log_button)

        stop_log = wx.Button(panel, label='Stop printing')
        stop_log.Bind(wx.EVT_BUTTON, self.on_stop_logs)

        hBox1.Add(stop_log)

        clear = wx.Button(panel, label='Clear')
        clear.Bind(wx.EVT_BUTTON, self.on_clear)

        hBox1.Add(clear)

        vbox.Add(hBox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 10))
        line = wx.StaticLine(panel)
        vbox.Add(line, flag=wx.EXPAND | wx.BOTTOM, border=10)

        self.scrolled_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.VSCROLL)
        vbox.Add(self.scrolled_text, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

        panel.SetSizer(vbox)

    def on_get_logs(self, event):
        self.log_thread = LogThread(self, self.ip_text.GetValue())
        self.log_thread.start()

    def on_stop_logs(self, event):
        self.log_thread.stop_logs()

    def update_text(self, result):
        self.scrolled_text.AppendText(result)

    def on_clear(self, result):
        self.scrolled_text.Clear()


if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None, title="Get logs from a device", size=(600, 800))
    frame.Show()
    app.MainLoop()
