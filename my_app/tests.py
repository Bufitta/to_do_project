from django.test import TestCase
from my_app.models import ToDoList

class MyTest(TestCase):
    def test_ok_create_work(self):
        data = {'work_title': 'test'}
        self.client.post('/form/', data)
        q_work = ToDoList.objects.filter()
        self.assertEquals(q_work.count(), 1)
        work = q_work.get()
        self.assertEquals(work.work_title, data['work_title'])

    def test_ok_delete_work(self):
        work = ToDoList.objects.create(work_title='test_title')
        work_id_delete = work.id
        data = {'delete': work_id_delete,'work_title':work.work_title}
        self.client.post('/main/', data)
        q_work = ToDoList.objects.filter(work_title=data['work_title']).count()
        self.assertEquals(q_work, 0)

    def test_ok_update(self):
        work = ToDoList.objects.create(work_title='test_title')
        work_id_update = work.id
        data = {'work_id': work_id_update,'work_title': 'Yes'}
        self.client.post('/form/', data)
        q_work = ToDoList.objects.filter(id=work_id_update)
        work = q_work.get()
        self.assertEquals(work.work_title, data['work_title'])
