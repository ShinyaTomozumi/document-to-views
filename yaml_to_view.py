#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

from models.parameter_config import ParameterConfig
from data.import_yaml import ImportYaml
from make.laravel import Laravel


# Main function
if __name__ == '__main__':
    """Main Function
    """

    # Show console log
    print('Start yaml to view files...')

    # パラメータを受け取る
    args = sys.argv

    # 引数の初期化
    parameter_config = ParameterConfig()

    # パラメータの数をチェックする（最低4つは必要)
    if len(args) < 4:
        print('No parameter / 必須パラメータを設定してください。')
        exit()

    # 受け取ったパラメータを引数に設定する。
    i = 0
    for arg in args:
        # 言語タイプを設定する
        if arg == '-t':
            if (i + 1) < len(args):
                parameter_config.project_type = args[i + 1]
        # ファイルのパスを取得する
        if arg == '-i':
            if (i + 1) < len(args):
                parameter_config.input_files_path = args[i + 1]
        # 出力先のパスを取得する
        if arg == '-o':
            if (i + 1) < len(args):
                parameter_config.output_file_path = args[i + 1]
        i += 1

    # ファイルタイプが設定されていない場合はエラーを返却する
    if parameter_config.project_type == '':
        print('Set the language (-t).')
        exit()

    # ファイルのパスが設定されていない場合はエラーを返却する
    if parameter_config.input_files_path == '':
        print('Set the file path (-i).')
        exit()

    # ファイルが存在しない場合はエラーを返却する
    if not os.path.isfile(parameter_config.input_files_path):
        print(f'The specified file does not exist. {parameter_config.input_files_path}')
        exit()

    # ファイルの拡張子が「yaml」もしくは「yml」以外の場合はエラーを返却する
    if not parameter_config.input_files_path.endswith('yaml') and not parameter_config.input_files_path.endswith('yml'):
        print('The specified file is not a "yaml" or "yml" file.')
        exit()

    # yamlからView情報を取得する
    yaml_views = ImportYaml(parameter_config)

    # プロジェクトタイプによって作成するファイルを変更する
    if parameter_config.project_type == 'laravel':
        # Laravel のViewファイルを作成する
        laravel = Laravel(parameter_config, yaml_views)
        laravel.make()
    else:
        print('The specified project does not exist.')
        exit()

    # Show finish message
    print('Finish yaml to views...')
