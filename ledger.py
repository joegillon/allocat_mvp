if __name__ == '__main__':
    import wx
    import globals as gbl
    from models.ledger_dataset import LedgerDataSet
    from views.ledger_window import LedgerWindow

    gbl.COLOR_SCHEME = gbl.SKINS[gbl.pick_scheme()]

    app = wx.App()

    gbl.dataset = LedgerDataSet(gbl.DB_PATH)

    main_window = LedgerWindow()
    main_window.Show()

    app.MainLoop()

