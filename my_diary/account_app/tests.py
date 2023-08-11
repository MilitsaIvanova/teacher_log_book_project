from django.contrib.auth import get_user_model
from django.core import exceptions
from django.test import TestCase, Client
from django.urls import reverse
from .models import TeachersSubject

from my_diary.account_app.models import validate_phone_number

UserModel = get_user_model()


class PhoneNumberValidatorTest(TestCase):

    def test_valid_phone_number(self):
        try:
            validate_phone_number('123456')
        except exceptions.ValidationError:
            self.fail('Valid phone number was registered as invalid.')

    def test_invalid_phone_number_letters(self):
        with self.assertRaises(exceptions.ValidationError):
            validate_phone_number('123456a')

    def test_invalid_phone_number_special_chars(self):
        with self.assertRaises(exceptions.ValidationError):
            validate_phone_number('123456-123456')


class CreateSubjectViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.client = Client()

        self.client.login(username='testuser', password='testpassword')

        self.create_subject_url = reverse('create subject')

    def test_create_subject(self):
        data = {
            'name': 'English',
            'code': "10",
            'description': 'some text'
        }

        response = self.client.post(self.create_subject_url, data)

        subject = TeachersSubject.objects.first()
        self.assertEqual(subject.name, 'English')
        self.assertEqual(subject.code, '10')
        self.assertEqual(subject.description, 'some text')

        self.assertEqual(subject.teacher, self.user)

        self.assertRedirects(response, reverse('classes', kwargs={'pk': self.user.pk}))


class EditSubjectViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        self.subject = TeachersSubject.objects.create(
            teacher=self.user,
            name="German",
            code="20",
            description="some text"
        )

        self.edit_subject_url = reverse('edit subject', kwargs={'pk': self.subject.pk})

    def test_edit_subject(self):
        data = {
            'name': 'German',
            'code': '20',
            'description': 'some text'
        }
        response = self.client.post(self.edit_subject_url, data)

        self.subject.refresh_from_db()

        self.assertEqual(self.subject.name, 'German')
        self.assertEqual(self.subject.code, '20')
        self.assertEqual(self.subject.description, 'some text')

        self.assertRedirects(response, reverse('classes', kwargs={'pk': self.user.pk}))


class DeleteSubjectViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        self.subject = TeachersSubject.objects.create(
            teacher=self.user,
            name="Spanish",
            code="30",
            description="some text"
        )

        self.delete_subject_url = reverse('delete subject', kwargs={'pk': self.subject.pk})

    def test_delete_subject(self):
        response = self.client.post(self.delete_subject_url)

        self.assertFalse(TeachersSubject.objects.filter(pk=self.subject.pk).exists())

        self.assertRedirects(response, reverse('classes', kwargs={'pk': self.user.pk}))
