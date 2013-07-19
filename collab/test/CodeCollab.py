import unittest
from ..CodeCollab import CodeCollabClient

class Test(unittest.TestCase):


    def test_get_current_user(self):
        cc = CodeCollabClient()
        user = cc.get_current_user()
        self.assertEqual(user, 'scrosby', 'Can\t get username')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()