#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

from models.parameter_config import ParameterConfig
from data.import_yaml import ImportYaml
from data.import_uiflow import ImportUIFlow
from make.laravel import Laravel
from make.next_js import NextJs


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
        # 読み込むドキュメントの種類を設定
        if arg == '-doc':
            if (i + 1) < len(args):
                parameter_config.document_type = args[i + 1]
        # ファイルのパスを取得する
        if arg == '-i':
            if (i + 1) < len(args):
                parameter_config.input_files_path = args[i + 1]
        # 出力先のパスを取得する
        if arg == '-o':
            if (i + 1) < len(args):
                parameter_config.output_dir_path = args[i + 1]
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

    # ドキュメントの種類によって、Viewの情報を読み込む処理を切り分ける
    if parameter_config.document_type == 'yaml':
        # ファイルの拡張子が「yaml」もしくは「yml」以外の場合は、エラーを返却する
        if not parameter_config.input_files_path.endswith('yaml') \
                and not parameter_config.input_files_path.endswith('yml'):
            print('The specified file is not a "yaml" or "yml" file.')
            exit()

        # 「yaml」から、View情報を読み込む
        views = ImportYaml(parameter_config)

    elif parameter_config.document_type == 'uiflow':
        # ファイルの拡張子が「uif」以外の場合は、エラーを返却する
        if not parameter_config.input_files_path.endswith('uif'):
            print('The specified file is not a "uif" file.')
            exit()

        # 「uiflows」から、View情報を読み込む
        views = ImportUIFlow(parameter_config)

    else:
        # 対応しているドキュメント種類以外は、エラーを返却する
        print('Please set the document type correctly.\n'
              'The supported types are the following formats.\n'
              ' - yaml\n'
              ' - uiflow')
        exit()

    # 指定されたプロジェクトタイプによって、作成するファイルを変更する
    if parameter_config.project_type == 'laravel':
        # Laravel の、Viewファイルを作成する
        laravel = Laravel(parameter_config, views)
        laravel.make()

    elif parameter_config.project_type == 'next_js':
        # UI Flows の、Viewファイルを作成する
        next_js = NextJs(parameter_config, views)
        next_js.make()

    else:
        print('The specified project does not exist.')
        exit()

    # Show finish message
    print('Finish yaml to views...')
