from unittest import TestCase

from application.models import UserInfo


class Creare_user_test(TestCase):
    def setUp(self):
        UserInfo.objects.create(email="test3@gmail.com", password="Test1", first_name="test1", last_name="test1",
                                mobile_no="2323232465")
        UserInfo.objects.create(email="test4@gmail.com", password="Test2", first_name="test2", last_name="test2",
                                mobile_no="2323232358")

    def test_get_test(self):
        user1 = UserInfo.objects.filter(email="test3@gmail.com")
        print(user1)
        user2 = UserInfo.objects.filter(email="test4@gmail.com")
        print(user2)
        self.assertEqual(user1.get("email"), 'test3@gmail.com')
        self.assertEqual(user2.get("email"), 'test4@gmail.com')
