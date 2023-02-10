from typing import List
from models.dialog_views import DialogViews


class Views:
    """
    書き出し用のView情報
    """
    id: str
    title: str
    url: str
    summary: str
    description: str
    path: list[str]
    query: list[str]
    middleware: list[str]
    dialogs: List[DialogViews]

    def __init__(self):
        self.id = ''
        self.title = ''
        self.url = ''
        self.summary = ''
        self.description = ''
        self.path = []
        self.query = []
        self.middleware = []
        self.dialogs = []
