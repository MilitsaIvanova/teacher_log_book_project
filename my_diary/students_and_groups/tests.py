from django.test import TestCase,Client

from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Student, TeachersSubject, Group
from .forms import AddStudentForm, EditStudentForm

class StudentViewTests(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')


        self.subject = TeachersSubject.objects.create(
            teacher=self.user,
            name='English',
            code='10',
            description='some text',
        )


        self.student = Student.objects.create(
            name='Gosho',
            email='some@email.com',
            teacher=self.user,
            subject=self.subject
        )

    def test_add_student_view(self):
        url = reverse('add student')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = {
            'name': 'Gosho',
            'email': 'some@email.com',
            'contact_number': '1234567890',
            'teacher': self.user.pk,
            'place': 'some place',
            'lesson_time': '12:00:00',
            'more_information': 'some information',
            'subject': self.subject.pk
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, f'/classes/{self.user.pk}')
        self.assertEqual(Student.objects.count(), 2)

    def test_edit_student_view(self):
        url = reverse('edit student', kwargs={'pk': self.student.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


        updated_data = {
            'name': 'Pesho',
            'email': 'updated@email.com',
            'contact_number': '0987654321',
            'teacher': self.user.pk,
            'place': 'Updated Place',
            'lesson_time': '14:00:00',
            'more_information': 'Updated information',
            'subject': self.subject.pk
        }
        response = self.client.post(url, updated_data)
        self.assertRedirects(response, f'/classes/{self.user.pk}')

        self.student.refresh_from_db()
        self.assertEqual(self.student.name, 'Pesho')
        self.assertEqual(self.student.email, 'updated@email.com')

    def test_delete_student_view(self):
        url = reverse('delete student', kwargs={'pk': self.student.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url)

        self.assertRedirects(response, reverse('classes', kwargs={'pk': self.user.pk}))
        self.assertEqual(Student.objects.count(), 0)

class GroupViewTests(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')


        self.subject = TeachersSubject.objects.create(
            teacher=self.user,
            name='English',
            code='10',
            description='some text'
        )

        self.student = Student.objects.create(
            name='Gosho',
            email='some@email.com',
            teacher=self.user,
            subject=self.subject
        )

        self.group = Group.objects.create(
            name='Test Group',
            year=2023,
            teacher=self.user,
            subject=self.subject,
        )

    def test_create_group_view(self):
        url = reverse('create group')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


        data = {
            'name': 'New Group',
            'year': 2023,
            'teacher': self.user.pk,
            'students': [self.student.pk],
            'place':'some place',
            'lesson_time': '14:00:00',
            'subject': self.subject.pk,

        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('groups', kwargs={'pk': self.user.pk}))
        self.assertEqual(Group.objects.count(), 2)

    def test_edit_group_view(self):
        url = reverse('edit group', kwargs={'pk': self.group.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        updated_data = {
            'name': 'Updated Group',
            'year': 2024,
            'teacher': self.user.pk,
            'students': [self.student.pk],
            'place': 'Updated Place',
            'lesson_time': '15:00:00',
            'subject': self.subject.pk,
        }
        response = self.client.post(url, updated_data)
        self.assertRedirects(response, reverse('groups', kwargs={'pk': self.user.pk}))

        self.group.refresh_from_db()
        self.assertEqual(self.group.name, 'Updated Group')
        self.assertEqual(self.group.year, 2024)

    def test_delete_group_view(self):
        url = reverse('group delete', kwargs={'pk': self.group.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('groups', kwargs={'pk': self.user.pk}))
        self.assertEqual(Group.objects.count(), 0)