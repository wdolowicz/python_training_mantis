__author__ = 'wdolowicz'

from suds.client import Client
from suds import WebFault


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except:
            return False

    def get_project_list_with_soap(self, username, password):
        self.projects_list = []
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
            for element in client.service.mc_projects_get_user_accessible(username, password):
                id = element.id
                name = element.name
                description = element.description
                self.projects_list.append(Project(id=id, name=name, description=description))
            return self.projects_list