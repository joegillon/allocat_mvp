import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil
from models.project import Project
from views.asn_dlg import AsnDlg


class ProjectPresenter(object):

    def __init__(self, view, actor):
        self.model = gbl.theDataSet.prjRex
        self.view = view
        self.employees = gbl.theDataSet.empRex
        self.selectedIdx = 0
        actor.Install(self, view)
        self.isListening = True
        # self.initView()

    def initView(self,):
        # self.view.setList(self.model)
        self.loadView()
        self.view.setSelection(0)
        # self.loadDetails()

    def loadView(self):
        if self.isListening:
            self.isListening = False
            self.refreshList()

            investigators = [rec for rec in self.employees if rec.investigator]
            managers = [rec for rec in self.employees if not rec.investigator]
            self.view.loadPI(investigators)
            self.view.loadPM(managers)

            # self.loadDetails()
            # Refresh details
            # item = self.model[self.selectedIdx]
            # self.view.setName(item.name)
            # self.view.setFullName(item.full_name)
            # self.view.setFrum(item.frum)
            # self.view.setThru(item.thru)

            # self.updateWindowTitle()
            self.isListening = True

    def loadDetails(self):
        from dal.dao import Dao

        item = self.view.getSelection()
        if item:
            self.view.setName(item.name)
            self.view.setFullName(item.full_name)
            self.view.setFrum(item.frum)
            self.view.setThru(item.thru)
            self.view.setPI(item.investigator)
            self.view.setPM(item.manager)
            self.view.setNotes(item.notes)
            if not item.asns:
                item.asns = item.getAsns(Dao())
            self.view.setAsnList(item.asns)
            self.view.setButtonLabel('Update Project')

    def refreshList(self):
        self.view.setList(self.model)

    def setSelection(self, idx):
        self.view.setSelection(idx)

    def getSelection(self):
        return self.view.getSelection()

    def applyFilter(self, ctrl, c, target):
        if not c.isalpha():
            if c == '\b':
                target = target[:-1]
        else:
            target += c
        theList = self.view.listCtrl
        col = theList.columns[0:1]
        if ctrl == 'notesFltrCtrl':
            col = theList.columns[4:1]
        theList.SetFilter(olv.Filter.TextSearch(
            theList, columns=col, text=target))
        theList.RepopulateList()
        # self.view.setSelectedIdx(0)
        self.view.setSelection(0)
        # self.loadDetails()

    def cancelFilter(self, ctrl):
        ctrl.Clear()
        theList = self.view.listCtrl
        theList.SetFilter(None)
        theList.RepopulateList()
        self.view.setSelection(0)
        # self.view.setSelectedIdx(0)
        # self.loadDetails()

    def clear(self):
        self.view.clearSelection()
        self.view.setName('')
        self.view.setFullName('')
        self.view.setFrum('')
        self.view.setThru('')
        self.view.setPI('')
        self.view.setPM('')
        self.view.setNotes('')
        self.view.setAsnList([])
        self.view.setButtonLabel('Add Project')

    def getFormValues(self):
        return {
            'name': self.view.getName(),
            'full_name': self.view.getFullName(),
            'frum': self.view.getFrum(),
            'thru': self.view.getThru(),
            'pi': self.view.getPI(),
            'pm': self.view.getPM(),
            'notes': self.view.getNotes()
        }

    def save(self):
        errMsg = self.validate()
        if errMsg:
            uil.showError(errMsg)
            return

        formValues = self.getFormValues()
        if self.view.getSelectedIdx() == -1:
            self.addProject(formValues)
        else:
            self.updateProject(formValues)

    def addProject(self, formValues):
        formValues['investigator_id'] = formValues['pi'].id
        formValues['investigator'] = formValues['pi'].name
        del formValues['pi']
        formValues['manager_id'] = formValues['pm'].id
        formValues['manager'] = formValues['pm'].name
        del formValues['pm']

        newProject = Project(formValues)

        self.model.append(newProject)
        self.model = sorted(self.model, key=lambda i: i.name.lower())
        self.refreshList()
        self.setSelection(self.model.index(newProject))

    def updateProject(self, formValues):
        prj = self.model[self.view.getSelectedIdx()]
        prj.name = formValues['name']
        prj.full_name = formValues['full_name']
        prj.frum = formValues['frum']
        prj.thru = formValues['thru']
        prj.investigator_id = formValues['pi'].id
        prj.investigator = formValues['pi'].name
        prj.manager_id = formValues['pm'].id
        prj.manager = formValues['pm'].name
        prj.notes = formValues['notes']
        self.refreshList()
        self.setSelection(self.model.index(prj))

    def drop(self):
        idx = self.view.getSelectedIdx()
        del self.model[idx]
        self.refreshList()
        if idx >= len(self.model):
            idx = len(self.model) - 1
        self.setSelection(idx)

    def addAsn(self):
        prj = self.view.getSelection()
        owner = 'Project: %s' % prj.name
        assignee = uil.ObjComboBox(self.view,
                               self.employees,
                               'name',
                               'Employee',
                               style=16)

        dlg = AsnDlg(self.view, -1, 'New Assignment', owner, assignee)
        dlg.ShowModal()

    def dropAsn(self):
        prj = self.view.getSelection()
        selections = self.view.getAsnSelections()
        ids = [x.id for x in selections]
        if not ids:
            uil.showError('No assignments selected!')
            return
        if uil.confirm(self.view, 'Drop selected assignments?'):
            new_list = [asn for asn in prj.asns if asn.id not in ids]
            prj.asns = new_list
            self.view.setAsnList(new_list)

    def editAsn(self, asn):
        prj = self.view.getSelection()
        owner = 'Project: %s' % prj.name
        assignee = 'Employee: %s' % asn.employee
        dlg = AsnDlg(self.view, -1, 'Assignment Details', owner, assignee, asn)
        dlg.ShowModal()

    def dataFieldUpdated(self):
        pass
        # if self.isListening:
        #     self.updateWindowTitle()

    def showHelp(self):
        import lib.ui_lib as uil

        uil.showListHelp()

    def validate(self):
        import lib.validator_lib as vl
        import lib.month_lib as ml

        values = self.getFormValues()
        prj = self.view.getSelection()
        prjId = prj.id if prj else 0

        prj_match = vl.ProjectMatch(prjId, gbl.theDataSet.prjNames)
        errMsg = vl.validatePrjName(values['name'], prj_match)
        if errMsg:
            return errMsg

        prj_match = vl.ProjectMatch(prjId, gbl.theDataSet.prjFullNames)
        errMsg = vl.validatePrjFullName(values['full_name'], prj_match)
        if errMsg:
            return errMsg

        errMsg = vl.validateTimeframe(values['frum'], values['thru'])
        if errMsg:
            return errMsg

        if prj and prj.asns:
            if values['frum'] < prj.frum or \
                values['thru'] > prj.thru:
                min, max = ml.getTimeframeEdges(prj.asns)
                if values['frum'] < min or values['thru'] > max:
                    errMsg = 'Assignment(s) out of new timeframe!'
        if errMsg:
            return errMsg

        return None
