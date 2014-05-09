from suds.client import Client, Object as SudsObject
from .objects import Project, MantisObject


class MantisClient(object):
    def __init__(self, username, password, server_url):
        self.conn = Client(server_url)
        self.username = username
        self.password = password

    def get_users_projects(self):
        projects = self.conn.service.mc_projects_get_user_accessible(
                self.username, self.password)

        return [MantisObject(project, self) for project in projects]

    def project_get_issues(self, project, page, window_size):
        issues = self.conn.service.mc_project_get_issues(
            self.username, self.password,
            project.id, page, window_size)

        return MantisObject(issues, self)
