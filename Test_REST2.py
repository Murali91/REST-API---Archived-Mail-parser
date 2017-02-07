from REST_Challenge2 import app
import unittest

class FlaskTest(unittest.TestCase):

	def test_validate_path(self):
		tester = app.test_client(self)
		response = tester.post('/path',data = dict(path = 'C:/Users/Muks/PycharmProjects/API/sampleEmails.tar.gz',keyword = "From"))
		self.assertIn('Request has been processed successfully. Output has been stored in directory path',response.data)

	def test_incorrect_path(self):
		tester = app.test_client(self)
		response = tester.post('/path',data = dict(path = "C:/Users/Muks/PycharmProjects/API/",keyword = "From"))
		self.assertIn("Incorrect file extension. Please try again with the path of a tar file that has to be parsed.", response.data)


	def test_garbagevalue_path(self):
		tester = app.test_client(self)
		response = tester.post('/path',data = dict(path = "sample",keyword = "From"))
		self.assertIn('Path seems to be incorrect. Please try again with the different input',response.data)


	def test_random_keyword(self):
		tester = app.test_client(self)
		response = tester.post('/path',data = dict(path = "C:/Users/Muks/PycharmProjects/API/sampleEmails.tar.gz",keyword = "123abdc"))
		self.assertIn('Request has been processed successfully. Output has been stored in directory path', response.data)

	def test_empty_keyword(self):
		tester = app.test_client(self)
		response = tester.post('/path',data = dict(path = "C:/Users/Muks/PycharmProjects/API/sampleEmails.tar.gz"))
		self.assertIn('Error in accessing the form data.', response.data)

	def test_multiple_keyword(self):
		tester = app.test_client(self)
		response = tester.post('/path',data = dict(path = "C:/Users/Muks/PycharmProjects/API/sampleEmails.tar.gz",keyword = "From,To"))
		self.assertIn('Request has been processed successfully. Output has been stored in directory path',response.data)

if __name__ == '__main__':
    unittest.main()


