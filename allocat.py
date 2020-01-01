if __name__ == '__main__':
    import wx
    import globals as gbl
    from models.dataset import AllocatDataSet
    from views.main_window import MainWindow


    app = wx.App()

    gbl.theDataSet = AllocatDataSet(gbl.DB_PATH)

    main_window = MainWindow()
    main_window.Show()

    app.MainLoop()

