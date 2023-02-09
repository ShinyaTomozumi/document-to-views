from typing import List, Type
from models.views import Views


class ImportViewsBase:
    """
    View情報の基底クラス
    """
    version: str
    copyright: str
    author: str
    description: str
    views: List[Views]

    def __init__(self):
        self.version = ''
        self.copyright = ''
        self.author = ''
        self.description = ''
        self.views = []
