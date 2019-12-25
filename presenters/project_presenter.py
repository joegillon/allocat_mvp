import ObjectListView as olv
import lib.ui_lib as uil
from models.project import Project
from views.asn_dlg import AsnDlg


class ProjectPresenter(object):
    def __init__(self, model, view, actor, employees):
        self.model = model
        self.view = view
        self.employees = employees
        self.selectedIdx = 0
        actor.Install(self, view)
        self.isListening = True
        self.initView()

    def initView(self,):
        self.view.setList(self.model)
        investigators = [rec for rec in self.employees if rec.investigator]
        managers = [rec for rec in self.employees if not rec.investigator]
        self.view.loadPI(investigators)
        self.view.loadPM(managers)
        self.view.setSelection(0)
        self.view.setSelectedIdx(0)

    def loadView(self):
        if self.isListening:
            self.isListening = False
            self.refreshList()

            # Refresh details
            item = self.model[self.selectedIdx]
            self.view.setName(item.name)
            self.view.setNickname(item.nickname)
            self.view.setFrum(item.frum)
            self.view.setThru(item.thru)

            self.updateWindowTitle()
            self.isListening = True

    def loadDetails(self):
        from dal.dao import Dao

        if self.isListening:
            self.isListening = False
            item = self.view.getSelection()
            if item:
                self.view.setName(item.name)
                self.view.setNickname(item.nickname)
                self.view.setFrum(item.frum)
                self.view.setThru(item.thru)
                self.view.setPI(item.investigator)
                self.view.setPM(item.manager)
                self.view.setNotes(item.notes)
                if not item.asns:
                    item.asns = item.getAsns(Dao())
                self.view.setAsnList(item.asns)
            self.isListening = True

    def refreshList(self):
        self.selectedIdx = self.view.getSelectedIdx()
        self.view.setList(self.model)
        self.view.setSelectedIdx(self.model.index(self.selectedIdx))

    def updateWindowTitle(self):
        # self.view.setWindowTitle('Project: ' + self.view.getName())
        pass

    def applyFilter(self, evt):
        c = chr(evt.GetUnicodeKey())
        target = evt.EventObject.GetValue()
        if not c.isalpha():
            if c == '\b':
                target = target[:-1]
        else:
            target += c
        theList = self.view.listCtrl
        col = theList.columns[0:1]
        if evt.EventObject.Parent.Name == 'notesFltrCtrl':
            col = theList.columns[4:1]
        theList.SetFilter(olv.Filter.TextSearch(
            theList, columns=col, text=target))
        theList.RepopulateList()
        self.view.setSelectedIdx(0)
        self.loadDetails()
        evt.Skip()

    def cancelFilter(self, evt):
        evt.EventObject.Clear()
        theList = self.view.listCtrl
        theList.SetFilter(None)
        theList.RepopulateList()
        self.view.setSelectedIdx(0)
        self.loadDetails()
        evt.Skip()

    def clear(self):
        self.view.setSelectedIdx(-1)
        self.view.setName('')
        self.view.setNickname('')
        self.view.setFrum('')
        self.view.setThru('')
        self.view.setPI('')
        self.view.setPM('')
        self.view.setNotes('')

    def getFormValues(self):
        return {
            'name': self.view.getName(),
            'nickname': self.view.getNickname(),
            'frum': self.view.getFrum(),
            'thru': self.view.getThru()
        }

    def save(self):
        formValues = self.getFormValues()
        if self.view.getSelectedIdx() == -1:
            self.addProject(formValues)
        else:
            self.updateProject(formValues)

    def addProject(self, formValues):
        newProject = Project(formValues)
        self.model.append(newProject)
        self.view.setList(self.model)
        self.view.setSelectedIdx(self.model.index(newProject))
        self.loadView()

    def updateProject(self, formValues):
        prj = self.model[self.view.getSelectedIdx()]
        prj.name = formValues['name']
        prj.nickname = formValues['nickname']
        prj.frum = formValues['frum']
        prj.thru = formValues['thru']
        self.loadView()

    def drop(self):
        idx = self.view.getSelectedIdx()
        del self.model[idx]
        if idx >= len(self.model):
            idx = len(self.model) - 1
        self.view.setSelectedIdx(idx)
        self.loadView()

    def addAsn(self):
        prj = self.view.getSelection()
        owner = 'Project: %s' % prj.nickname
        assignee = uil.ObjComboBox(self.view,
                               self.employees,
                               'name',
                               'Employee',
                               style=16)

        dlg = AsnDlg(self.view, -1, 'New Assignment', owner, assignee)
        dlg.ShowModal()

    def dropAsn(self):
        pass

    def editAsn(self, asn):
        prj = self.view.getSelection()
        owner = 'Project: %s' % prj.nickname
        assignee = 'Employee: %s' % asn.employee
        # assignee = uil.getAssigneeLabel(self.view, 'Employee: %s' % asn.employee)
        dlg = AsnDlg(self.view, -1, 'Assignment Details', owner, assignee, asn)
        dlg.ShowModal()

    def dataFieldUpdated(self):
        if self.isListening:
            self.updateWindowTitle()

    def showHelp(self):
        import lib.ui_lib as uil

        uil.showListHelp()