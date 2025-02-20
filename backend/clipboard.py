"""
Clipboard Server

Author: EricJuice
Date: 2024-07-29
Updated: 2025-02-11
"""

from typing import Dict, Tuple
from dataclasses import dataclass
import random
import string
import time
import logging
import traceback

from models import ResponseFormat

class Clipboard:

    @dataclass
    class ClipboardItem:
        code: str = None
        text: str = None
        create_time: int = 0
        expire_time: int = 0 # in seconds
        access_limit: int = 1
        accesses: int = 0

        def __repr__(self):
            return self.text

    def __init__(self):
        self.clipboard: Dict[str, Clipboard.ClipboardItem] = {}  # code: ClipboardItem
        logging.info("Init Clipboard")

    def __generateCode(self) -> str:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))

    def __check_leagal(self, item: ClipboardItem) -> Tuple[bool,str]:
        """
        check if the item is leagal

        :return: (bool, str): bool: True if leagal; str: error message
        """
        if item.accesses >= item.access_limit:
            return False, "Access Limit Reached"
        if time.time() - item.create_time > item.expire_time:
            return False, "Expired"
        return True, "ok"
    

    def clearIllegalItems(self):
        for code in list(self.clipboard.keys()):
            is_ok, res = self.__check_leagal(self.clipboard[code])
            if not is_ok:
                self.clipboard.pop(code)
                logging.info(f"Clear {code}: {res}")

    def getAllItem(self) -> str:
        d = self.clipboard
        res = str([item for item in d.keys()])
        return res

    def clearAll(self) -> int:
        cnt = len(self.clipboard)
        self.clipboard = {}
        logging.info(f"Clear All: {cnt}")
        return cnt

    def set(self, item: ClipboardItem) -> ResponseFormat:
        """
        set text to clipboard
        
        @param item: ClipboardItem
        @return ResponseFormat : code is in res.data
        """
        res = ResponseFormat()
        try:
            code = self.__generateCode()
            res.data = code
            item.code = code
            item.create_time = time.time()
            self.clipboard[code] = item
        except Exception as e:
            logging.error(f"Upload failed! Exception: {str(e)}; {traceback.format_exc()}")
            res.msg = str(e)
        return res

    def get(self, code: str) -> str:
        """
        get text from clipboard
        
        @param code: str of 4 chars
        @return: str
        """
        res = "None"
        if code in self.clipboard:
            if_ok, res = self.__check_leagal(self.clipboard[code])
            self.clipboard[code].accesses += 1
            res = self.clipboard[code].text if if_ok else res
            if not if_ok:
                self.clipboard.pop(code)
                logging.info(f"Clear {code}: {res}")
        else:
            res = "404 Not Found"
            logging.warning(f"The code {code} not found")
        return res
