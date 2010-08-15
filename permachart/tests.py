import os, sys
os.environ["DJANGO_SETTINGS_MODULE"] =  'settings'
sys.path[0:0] = [
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'google_appengine')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'deps', 'Django-1.2.1')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'deps', 'pychart')),
]
import unittest
from charter.form_utils import BaseFormSet
from charter.forms import DataRowFormSet
from charter.models import DataRow

class FormSetTests(unittest.TestCase):
    def setUp(self):
        self.row1 = DataRow(data_key='asdf', data_value='1234')
        self.row2 = DataRow(data_key='jkl;', data_value='4321')
    
    def test_new_form_instantiation(self):
        fs = DataRowFormSet()
        # empty forms
        self.assertEquals(2, len(fs.forms))

    def test_empty_fields_work_properly(self):
        fs = DataRowFormSet(extra_forms=0)
        self.assertEquals(0, len(fs.forms))

    def test_edit_form_instantiation(self):
        fs = DataRowFormSet(instances=[self.row1, self.row2])
        # 2 normal + 2 empty
        self.assertEquals(4, len(fs.forms))

    def test_edit_form_success(self):
        pass

    def test_edit_form_deleting_data(self):
        pass

    def test_edit_form_delete_all_data(self):
        pass
    
    def test_new_form_no_data(self):
        # someone posts an empty set to newform
        pass

    def test_new_form_success(self):
        pass


class DataRowFormTest(unittest.TestCase):
    def test_validation_of_form_values(self):
        pass

if __name__ == '__main__':
    unittest.main()
