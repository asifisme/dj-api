# from django.test import TestCase, Client
# from django.contrib.auth import get_user_model
# import time
# import json

# User = get_user_model()

# class AuthLoadTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email='hello@gmail.com',
#             password='testpassword'
#         )

#     def test_login_load(self):
#         num_requests = 10  # Number of login attempts to simulate
#         success_count = 0
#         start_time = time.time()

#         for i in range(num_requests):
#             client = Client()
#             response = client.post(
#                 '/api/v1/signin/',
#                 data=json.dumps({
#                     'username_or_email': 'hello@gmail.com',
#                     'password': 'testpassword'
#                 }),
#                 content_type='application/json'
#             )

#             if response.status_code == 200:
#                 success_count += 1
#             else:
#                 print(f"Failed [{i+1}] - Status: {response.status_code}, Body: {response.content}")

#         end_time = time.time()
#         duration = end_time - start_time

#         print(f"\n Load Test Results")
#         print(f"Total Requests: {num_requests}")
#         print(f"Successful Logins: {success_count}")
#         print(f"Duration: {duration:.2f} seconds")
#         print(f"Requests per second: {num_requests / duration:.2f}")

#         self.assertEqual(success_count, num_requests, "Not all logins succeeded")
