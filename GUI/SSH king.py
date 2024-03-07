import wx
from PageOne import PageOne
from PageTwo import PageTwo
from PageThree import PageThree
from PageFour import PageFour


class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)

        # IP label and text ctrl
        self.label1 = wx.StaticText(self, label="Enter IP:")
        self.ip_input = wx.TextCtrl(self)

        # port label and text ctrl
        self.label2 = wx.StaticText(self, label="Enter Port:")
        self.port_input = wx.TextCtrl(self)

        top_grid = wx.GridSizer(rows=2, cols=2, vgap=5, hgap=5)
        top_grid.Add(self.label1, 0, wx.ALIGN_RIGHT)
        top_grid.Add(self.ip_input, 0, wx.ALIGN_CENTER_VERTICAL)
        top_grid.Add(self.label2, 0, wx.ALIGN_RIGHT)
        top_grid.Add(self.port_input, 0, wx.ALIGN_CENTER_VERTICAL)

        self.notebook = wx.Notebook(self)
        self.page1 = PageOne(self.notebook, self)
        self.page2 = PageTwo(self.notebook, self)
        self.page3 = PageThree(self.notebook, self)
        self.page4 = PageFour(self.notebook, self)

        self.notebook.AddPage(self.page4, "FPGA Version")
        self.notebook.AddPage(self.page3, "Commands")
        self.notebook.AddPage(self.page1, "Live Logs")
        self.notebook.AddPage(self.page2, "Download Logs")

        # Main sizer for notebook and top elements
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(top_grid, 0, wx.ALIGN_LEFT)
        main_sizer.Add(self.notebook, 1, wx.EXPAND)

        self.SetSizer(main_sizer)

    def get_port_number(self):
        return self.port_input.GetValue()

    def get_ip_address(self):
        return self.ip_input.GetValue()


if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame(None, title="Get logs from a device", size=(600, 800))
    frame.Show()
    app.MainLoop()
