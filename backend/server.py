"""
Clipboard Server

Author: EricJuice
Date: 2024-07-29
Updated: 2025-02-11
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import random
import string
import time
import logging
import traceback

from models import ClipboardRequest, ResponseFormat
from clipboard import Clipboard

class ClipboardServer:

    def __init__(self):
        self.__clipboard = Clipboard()

        self.router = APIRouter()
        self.router.add_api_route("/", self.hello, methods=["GET"])
        self.router.add_api_route("/hello", self.hello)
        self.router.add_api_route("/upload", self.upload, methods=["POST"])
        self.router.add_api_route("/get/{code}", self.getItem, methods=["GET"])
        self.router.add_api_route("/getAll", self.getAll, methods=["GET"])
        self.router.add_api_route("/clearAll", self.clearAll, methods=["GET"])

        self.exit_flag = False

    def hello(self):
        return HTMLResponse("Hello")

    def exit(self):
        self.exit_flag = True

    def run(self):
        while not self.exit_flag:
            self.__clipboard.clearIllegalItems()
            time.sleep(5)
        logging.info("ClipboardServer exit!")

    def generateCode(self) -> str:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))

    def upload(self, item: ClipboardRequest) -> ResponseFormat:
        """
        Upload text to clipboard
        """
        res = ResponseFormat()
        try:
            logging.info("Upload!")
            data = item.model_dump()
            text = data.get("text", "")
            ex = data.get("expire_time", "")
            access = data.get("access_limit", "")
            if_one_time = data.get("if_one_time", "")
            code = self.generateCode()
            logging.info(f"data: {len(text)} bytes. expire_time: {ex} min. access_limit: {access}. if_one_time: {if_one_time}. code: {code}")
            res.data = code

            res = self.__clipboard.set(Clipboard.ClipboardItem(text=text, expire_time=(int(ex)*60), access_limit=access, code=code))
            
            return res
        except Exception as e:
            logging.error(f"Upload failed! Exception: {str(e)}; {traceback.format_exc()}")
            return {"code": str(e)}

    def getItem(self, code: str) -> ResponseFormat:
        res = ResponseFormat(msg="success", code="0", data="")
        data = self.__clipboard.get(code)
        res.data = data

        return res

    def getAll(self) -> ResponseFormat:
        res = ResponseFormat(msg="success", code="0", data="")
        res.data = self.__clipboard.getAllItem()
        return res

    def clearAll(self) -> ResponseFormat:
        res = ResponseFormat(msg="success", code="0", data="")
        res.data = str(self.__clipboard.clearAll())
        return res
