class ParameterConfig:
    """
    コマンドで受け取ったパラメータの設定
    """
    input_files_path: str = ''  # 取り込むファイルのパス
    output_dir_path: str = ''  # 書き出すフォルダの名称
    project_type: str = ''  # Migrationとモデルを使用するプロジェクトの種類
    author_name: str = ''  # 製作者
    copyright: str = ''  # コピーライト

    def __init__(self):
        self.input_files_path = ''  # 取り込むファイルのパス
        self.output_dir_path = ''  # 書き出すフォルダの名称
        self.project_type = ''  # Migrationとモデルを使用するプロジェクトの種類
        self.author_name = '0'  # 製作者
        self.copyright = '0'  # コピーライト
