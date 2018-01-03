__author__ = 'wdolowicz'

from model.project import Project
import random
import string


def test_del_project_from_mantis(app):
    app.session.login("Administrator", "root")
    assert app.session.is_logged_in_as("administrator")
    if len(app.soap.get_project_list_with_soap("Administrator", "root")) == 0:
        project = Project(name=random_string("name", 10), description=random_string("description", 30))
        app.project.create(project)
    old_projects = app.soap.get_project_list_with_soap("Administrator", "root")
    project = random.choice(old_projects)
    app.project.delete_project_by_id(project.id)
    new_projects = app.soap.get_project_list_with_soap("Administrator", "root")
    assert len(old_projects) - 1 == len(new_projects)
    old_projects.remove(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + " "*5
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])
