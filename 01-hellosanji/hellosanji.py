#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import os
import uuid
from sanji.core import Sanji
from sanji.core import Route
from sanji.model_initiator import ModelInitiator
from sanji.connection.mqtt import Mqtt


class Hellosanji(Sanji):

    def init(self, *args, **kwargs):
        path_root = os.path.abspath(os.path.dirname(__file__))
        self.model = ModelInitiator("hellosanji", path_root)
        self.message = "Hello Sanji!"

    @Route(methods="get", resource="/hellosanji")
    def get(self, message, response):

        # case 3: collection get
        if "collection" in message.query:
            if message.query["collection"] == "true":
                # collection=true
                return response(
                    data={"collection": self.model.db["conversationList"]})

        # case 2: single id
        if "id" in message.param:
            rsp_msg = None
            for item in self.model.db["conversationList"]:
                if item["id"] == message.param["id"]:
                    # information of specific id
                    rsp_msg = item["message"]

            return response(data=rsp_msg)

        # case 1: capability
        id_list = []
        for item in self.model.db["conversationList"]:
            id_list.append(item["id"])
        return response(data=id_list)

    @Route(methods="put", resource="/hellosanji")
    def put(self, message, response):
        if hasattr(message, "data"):
            self.message = message.data["message"]
            # case 1: put successfully
            self.model.save_db()
            return response()

        # case 2: put with bad request
        return response(code=400, data={"message": "Invaild Input."})

    @Route(methods="post", resource="/hellosanji")
    def post(self, message, response):
        if hasattr(message, "data"):
            # case 1: post successfully
            obj = {}
            obj["id"] = str(uuid.uuid4())
            obj["message"] = message.data
            self.model.db["conversationList"].append(obj)
            self.model.save_db()
            return response(data={"id": obj["id"]})

        # case 2: post with bad request
        return response(code=400, data={"message": "Invalid Post Input."})

    @Route(methods="delete", resource="/hellosanji/:id")
    def delete(self, message, response):

        del_item = None
        if "id" in message.param:
            for item in self.model.db["conversationList"]:
                if item["id"] == message.param["id"]:
                    del_item = item
                    break

            if del_item:
                # case 1: delete successfully
                del del_item
                self.message = "delete index: %s" % message.param["id"]
                self.model.save_db()
                return response(self.message)
            else:
                # case 2: delete failed
                return response(code=400, data={"message": "id is not found."})

        # case 3: delete with bad request
        return response(code=400, data={"message": "Invalid Delete Input."})


if __name__ == "__main__":
    FORMAT = "%(asctime)s - %(levelname)s - %(lineno)s - %(message)s"
    logging.basicConfig(level=0, format=FORMAT)
    logger = logging.getLogger("Hellosanji")

    hellosanji = Hellosanji(connection=Mqtt())
    hellosanji.start()
