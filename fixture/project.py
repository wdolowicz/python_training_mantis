__author__ = 'wdolowicz'


from model.project import Project
import re


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_manage_proj_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("/manage_proj_page.php"):
            wd.get("http://localhost/mantisbt-1.2.20/manage_proj_page.php")

    def setvalue(self, value, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(value).click()
            wd.find_element_by_name(value).clear()
            wd.find_element_by_name(value).send_keys(text)

    def fill_project_form(self, project):
        wd = self.app.wd
        self.setvalue("name", project.name)
        self.setvalue("description", project.description)

    def create(self, project):
        wd = self.app.wd
        self.open_manage_proj_page()
        wd.find_element_by_css_selector("input[value='Create New Project']").click()
        self.fill_project_form(project)
        wd.find_element_by_css_selector("input[value='Add Project']").click()
        if not wd.current_url.endswith("/manage_proj_page.php"):
            self.return_to_project_page()
        self.project_cache = None

    def return_to_project_page(self):
        wd = self.app.wd
        wd.get("http://localhost/mantisbt-1.2.20/manage_proj_page.php")

    project_cache = None

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_manage_proj_page()
            self.project_cache = []
            index = 0
            for i2 in wd.find_elements_by_xpath("//table[3]/tbody/tr/td[1]/a"):
                name = i2.text
                if "manage_proj_edit_page.php?project_id=" in i2.get_attribute("href"):
                    href = i2.get_attribute("href")
                    id = int(re.search("\d+$", href).group(0))
                    description = wd.find_elements_by_xpath("//table[3]/tbody/tr/td[5]")[index].text
                    self.project_cache.append(Project(id=id, name=name, description=description))
                index += 1
        return list(self.project_cache)

    def delete_project_by_name(self, name):
        wd = self.app.wd
        self.open_manage_proj_page()
        wd.find_element_by_link_text("%s" % name).click()
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        text_page_confirm_delete = wd.find_element_by_css_selector("div[align='center']").text
        confirm_str = "Are you sure you want to delete this project and all attached issue reports?"
        if confirm_str in text_page_confirm_delete:
            wd.find_element_by_css_selector("input[value='Delete Project']").click()
        if not wd.current_url.endswith("/manage_proj_page.php"):
            self.return_to_project_page()
        self.project_cache = None

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.open_manage_proj_page()
        wd.find_element_by_css_selector('a[href="manage_proj_edit_page.php?project_id=%s"]' % id).click()
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        text_page_confirm_delete = wd.find_element_by_css_selector("div[align='center']").text
        confirm_str = "Are you sure you want to delete this project and all attached issue reports?"
        if confirm_str in text_page_confirm_delete:
            wd.find_element_by_css_selector("input[value='Delete Project']").click()
        if not wd.current_url.endswith("/manage_proj_page.php"):
            self.return_to_project_page()
        self.project_cache = None
