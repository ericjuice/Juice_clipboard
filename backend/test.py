import unittest
import logging
from clipboard import Clipboard

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class Test(unittest.TestCase):
    
    # python -m unittest test.Test.test_add
    def test_add(self):
        c = Clipboard()
        data = Clipboard.ClipboardItem(text="test", create_time=0, expire_time=0, accesses=0)
        res = c.set(data)
        print(res)
        item = c.get(res.data)
        print(item)
