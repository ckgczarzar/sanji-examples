#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
import sys
import unittest

from sanji.connection.mockup import Mockup
from sanji.message import Message

try:
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
    from hellosanji import Hellosanji
except ImportError as e:
    print "Please check the python PATH for import test module. (%s)" \
        % __file__
    exit(1)


class TestHellosanjiClass(unittest.TestCase):

    def setUp(self):
        self.hellosanji = Hellosanji(connection=Mockup())

    def tearDown(self):
        self.hellosanji.stop()
        self.hellosanji = None

    def test_get(self):

        # case 1: capability
        message = Message({"data": {"message": "call get()"},
                          "query": {}, "param": {}})

        def resp1(code=200, data=None):
            self.assertEqual(code, 200)
            self.assertEqual(data, [1, 2])

        self.hellosanji.get(message=message, response=resp1, test=True)

        # case 2: single id
        message = Message(
            {"data": {"message": "call get()"},
             "param": {"id": 2},
             "query": {}})

        def resp2(code=200, data=None):
            self.assertEqual(code, 200)
            self.assertEqual(data, "Hello MOXA")

        self.hellosanji.get(message=message, response=resp2, test=True)

        # case 3: collection get
        message = Message(
            {"data": {"message": "call get()"},
             "query": {"collection": "true"},
             "param": {}})

        ret_msg = []
        ret_msg.append({"id": 1, "message": "Hello World"})
        ret_msg.append({"id": 2, "message": "Hello MOXA"})

        def resp3(code=200, data=None):
            self.assertEqual(code, 200)
            self.assertEqual(data, {"collection": ret_msg})
        self.hellosanji.get(message=message, response=resp3, test=True)

    def test_put(self):
        message = Message({"data": {"message": "hello kitty"}})

        # case 1: put successfully
        def resp1(code=200, data=None):
            self.assertEqual(self.hellosanji.message, "hello kitty")
        self.hellosanji.put(message=message, response=resp1, test=True)

        # case 2: put with bad request
        del message.data

        def resp2(code=200, data=None):
            self.assertEqual(400, code)
            self.assertEqual(data, {"message": "Invaild Input."})
        self.hellosanji.put(message=message, response=resp2, test=True)

    def test_post(self):
        message = Message({"data": {"message": "call post()"}})

        # case 1: post successfully
        def resp1(code=200, data=None):
            self.assertEqual(200, code)
            self.assertTrue("id" in data)
            self.assertFalse("message" in data)

        self.hellosanji.post(message=message, response=resp1, test=True)

        # case 2: post with bad request
        del message.data

        def resp2(code=200, data=None):
            self.assertEqual(400, code)
            self.assertEqual(data, {"message": "Invalid Post Input."})

        self.hellosanji.post(message=message, response=resp2, test=True)

    def test_delete(self):
        # case 1: delete successfully
        message = Message(
            {"data": {"message": "call delete()"}, "param": {"id": 2}})

        def resp1(code=200, data=None):
            self.assertEqual(self.hellosanji.message, "delete index: 2")

        self.hellosanji.delete(message=message, response=resp1, test=True)

        # case 2: delete failed
        message = Message(
            {"data": {"message": "call delete()"}, "param": {"id": 1995}})

        def resp2(code=200, data=None):
            self.assertEqual(data["message"], "id is not found.")

        self.hellosanji.delete(message=message, response=resp2, test=True)

        # case 3: delete with bad request
        message = Message(
            {"data": {"message": "call delete()"}, "param": {}})

        def resp3(code=200, data=None):
            self.assertEqual(400, code)
            self.assertEqual(data, {"message": "Invalid Delete Input."})

        self.hellosanji.delete(message=message, response=resp3, test=True)


if __name__ == "__main__":
    unittest.main()
