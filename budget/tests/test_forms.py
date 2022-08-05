from django.test import SimpleTestCase

from budget.forms import ExpenseForm


class TestForms(SimpleTestCase):
    def test_ExpenseForm_valid_data(self):
        form = ExpenseForm(data ={
            'title': 'expense1',
            'amount': 1000,
            'category': 'development'
        })
        self.assertTrue(form.is_valid())

    def test_ExpenseForm_no_data(self):
        form = ExpenseForm(data = {})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3) #3 for each empty field
