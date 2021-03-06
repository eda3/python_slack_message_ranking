# import argparse
import json
import os
import sys
import unicodedata
from typing import List, Tuple


def main() -> None:
    # 引数チェック
    args: List[str] = sys.argv

    # 引数パーサを作成
    # s: str = "Slackの全メッセージをエクスポートしたデータをランキング順 or 最終書き込み日順に表示する"
    # parser = argparse.ArgumentParser(description=s)

    if not check_args(args):
        print("### 引数のチェックに問題があったため処理を終了します")
        sys.exit()

    work_dir: str = "./export"

    # json ファイル読み込み
    with open(work_dir + "/" + "channels.json") as f:
        channels_json: List[dict] = json.load(f)

    # アーカイブされたチャンネル一覧取得
    archived_channels: List[dict] = get_archived_channels(channels_json)

    # =======================================================================
    # エクスポートデータから、チャンネル名、最終更新日付、書き込み数を取得
    # =======================================================================
    result_channels: List[Tuple[str, str, int]] = []
    for root, dirs, files in os.walk(work_dir):  # type: str, List[str], List[str]
        channel_name: str = os.path.basename(str(root))

        # Macの場合、ディレクトリ名がNFD形式であるため変換を行う
        # 参考：http://r9.hateblo.jp/entry/2015/05/11/233000
        channel_name = unicodedata.normalize("NFC", channel_name)

        # 走査の対象から、トップディレクトリとアーカイブチャンネルを除く
        if channel_name in archived_channels or len(dirs) != 0:
            continue

        # 走査の対象から、空ディレクトリを除く
        if len(files) == 0:
            continue

        # チャンネル名と最終書き込み日を取得
        channel_name = "#" + channel_name
        last_write_date: str = str(files[-1]).replace(".json", "")

        check_date_count: int = 0

        # last_month_list = get_date_list(args)
        last_month_list: List[str] = args

        # 各チャンネル書き込み数一覧を取得
        for file in files:
            # ファイルのみチェックする
            for last_month in last_month_list:
                if last_month in file:
                    with open(root + os.sep + file) as f:
                        channel_file: List[dict] = json.load(f)
                        check_date_count += len(channel_file)

        # 各取得データを配列に格納
        result_channels += [(channel_name, last_write_date, check_date_count)]
        # result_channels += [[channel_name, last_write_date]]

    # チャンネルを最終更新日順にソート
    result_channels.sort(key=lambda x:x[1])
    for result in result_channels:  # type: Tuple[str, str, int]
        print(result[0], result[1])

    # チャンネル名を勢い順にソート
    result_channels.sort(key=lambda x: x[2], reverse=True)

    rank: int = 0
    pre_channel: int = 0
    for result in result_channels:
        # 書き込みゼロは表示しない
        if result[2] == 0:
            continue

        if result[2] != pre_channel:
            rank += 1
            pre_channel = result[2]
        print(str(rank).zfill(2), result[0], result[2])


def check_args(args: list) -> bool:
    # 引数は最低一つ必要
    if len(args) == 1:
        print("引数をyyyy-mm-ddで指定してください")
        return False
    return True


def get_archived_channels(channels_json: List[dict]) -> List[dict]:
    # アーカイブされたチャンネル一覧取得
    archived_channels: List[dict] = []
    for key in channels_json:
        if key["is_archived"]:
            archived_channels.append(key["name"])

    return archived_channels


if __name__ == "__main__":
    main()
