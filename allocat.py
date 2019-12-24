if __name__ == '__main__':
    import wx
    from views.main_window import MainWindow

    app = wx.App()

    main_window = MainWindow()
    main_window.Show()

    app.MainLoop()

