from views.asn_dlg import AsnDlg
from views.project.assignment_panel import PrjAsnPanel


class PrjAsnDlg(AsnDlg):

    def getPanel(self, prj, asn):
        return PrjAsnPanel(self, prj, asn)
