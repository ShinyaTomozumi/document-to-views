from typing import List, Type
from models.dialog_views import DialogViews


class TempViews:
    """
    一時的に保存するView 情報
    """
    id: str
    summary: str
    title: str
    url: str
    path: list[str]
    query: list[str]
    middleware: list[str]
    dialogs: List[DialogViews]

    def __init__(self):
        self.id = ''
        self.summary = ''
        self.title = ''
        self.url = ''
        self.path = []
        self.description = ''
        self.middleware = []
        self.query = []
        self.dialogs = []
