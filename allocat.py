if __name__ == '__main__':
    import wx
    import globals as gbl
    from models.dataset import AllocatDataSet
    from views.main_window import MainWindow

    gbl.COLOR_SCHEME = gbl.SKINS[gbl.pick_scheme()]

    app = wx.App()

    gbl.dataset = AllocatDataSet(gbl.DB_PATH)

    main_window = MainWindow()
    main_window.Show()

    app.MainLoop()

