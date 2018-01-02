__author__ = 'wdolowicz'

from model.project import Project
import random
import string
import re

def test_add_project_mantis(app):
    app.session.login("Administrator", "root")
    assert app.session.is_logged_in_as("administrator")
    old_projects = app.project.get_project_list()
    project = Project(name=random_string("name", 10), description=random_string("description", 30))
    app.project.create(project)
    new_projects = app.project.get_project_list()
    old_projects.append(clean(project))
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + " "*10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def clean(project):
    return Project(id=project.id, name=re.sub("[ ]{2,}", " ", (project.name).strip()),
                   description=re.sub("[ ]{2,}", " ", (project.description).strip()))
