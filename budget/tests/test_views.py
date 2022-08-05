import json
from unicodedata import category
from urllib import response
from django.test import Client, TestCase
from django.urls import reverse

from budget.models import Category, Expense, Project


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.project1 = Project.objects.create(
            name='project1',
            budget=10000 
        )
        self.detail_url = reverse('detail', args=['project1'])

    def test_project_list_GET(self):
        response = self.client.get(reverse('list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-list.html')

    def test_project_detail_GET(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-detail.html')

    def test_project_detail_POST(self):
        Category.objects.create(
            project = self.project1,
            name = 'development'
        )

        response = self.client.post(self.detail_url, {
            'title': 'expense1',
            'amount': 1000,
            'category': 'development'
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.project1.expenses.first().title, 'expense1')


    def test_project_detail_POST_no_data(self):
        response = self.client.post(self.detail_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.project1.expenses.count(), 0)

    def test_project_detail_DELETE(self):
        category1 = Category.objects.create(
            project = self.project1,
            name = 'development'
        )
        Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount = 1000,
            category = category1
        )
        response = self.client.delete(self.detail_url, json.dumps({
            'id': 1 
        }))

        self.assertEquals(response.status_code, 204)
        self.assertEquals(self.project1.expenses.count(), 0)

    def test_project_detail_DELETE_no_id(self):
        category1 = Category.objects.create(
            project = self.project1,
            name = 'development'
        )
        Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount = 1000,
            category = category1
        )
        response = self.client.delete(self.detail_url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(self.project1.expenses.count(), 1)

    def test_project_create_POST(self):
        url = reverse('add')
        response = self.client.post(url, {
            'name': 'project2',
            'budget': 10000,
            'categoriesString': 'design,development'
        })

        project2 = Project.objects.get(id=2)
        self.assertEquals(project2.name, 'project2')
        first_category = Category.objects.get(id=1)
        self.assertEquals(first_category.project, project2)
        self.assertEquals(first_category.name, 'design')
        second_category = Category.objects.get(id=2)
        self.assertEquals(second_category.project, project2)
        self.assertEquals(second_category.name, 'development')

