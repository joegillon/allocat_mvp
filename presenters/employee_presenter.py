import globals as gbl
from presenters.presenter import Presenter


class EmployeePresenter(Presenter):

    def load_combos(self):
        pass

    def load_details(self):
        pass

    def clear_model_values(self):
        pass

    def get_form_values(self):
        pass

    def validate(self):
        pass

    def get_new_model_values(self, formValues):
        return formValues

    def update_model_values(self, model, formValues):
        pass
