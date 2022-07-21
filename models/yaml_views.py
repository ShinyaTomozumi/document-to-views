class YamlViews:
    """
    Yamlで定義したViewsのクラス
    """
    id: str
    title: str
    url: str
    description: str
    path: list[str]
    query: list[str]
    middleware: list[str]

    def __init__(self):
        self.id = ''
        self.title = ''
        self.url = ''
        self.description = ''
        self.path = []
        self.query = []
        self.middleware = []
