"""
params models

@author: EricJuice
@date: 2024-07-29
@updated: 2025-02-11
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class ClipboardRequest(BaseModel): # Post request. this should be consistent with frontend
    text: str = Field(default="", description="text")
    expire_time: int = Field(default=0, description="expire_time")
    access_limit: int = Field(default=0, description="access_limit")
    if_one_time: bool = Field(default=False, description="if_one_time")

class ResponseFormat(BaseModel):
    msg: str = Field(default="success", description="response message")
    code: int = Field(default=0, description="response code")
    data: Optional[str] = Field(default=None, description="response data")