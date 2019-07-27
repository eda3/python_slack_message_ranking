import json
import os
import unicodedata


def main():
    work_dir = './export'

    # json ファイル読み込み
    with open(work_dir + '/' + 'channels.json') as f:
        channels_json = json.load(f)

    # アーカイブされたチャンネル一覧取得
    archived_channels = []
    for key in channels_json:
        if key['is_archived']:
            archived_channels.append(key['name'])

    # =======================================================================
    # エクスポートデータから、チャンネル名、最終更新日付、書き込み数を取得
    # =======================================================================
    result_channels = []
    for root, dirs, files in os.walk(work_dir):
        channel_name = os.path.basename(str(root))

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
        channel_name = '#' + channel_name
        last_write_date = str(files[-1]).replace('.json', '')

        check_date_count = 0

        # last_month_list = ['2019-03',]
        '''
        last_month_list = ['2019-03-01',
                           '2019-03-02',
                           '2019-03-03',
                           '2019-03-04',
                           '2019-03-05',
                           '2019-03-06',
                           '2019-03-07',
                           '2019-03-08',
                           '2019-03-09',
                           '2019-03-10',
                           '2019-03-10',
                           '2019-03-11',
                           '2019-03-12',
                           '2019-03-14',
                           '2019-03-14',
                          ]
        '''
        last_month_list = ['2019-03-15',
                           '2019-03-16',
                           '2019-03-17',
                           '2019-03-18',
                           '2019-03-19',
                           '2019-03-20',
                           '2019-03-21',
                           '2019-03-22',
                           '2019-03-23',
                           '2019-03-24',
                           '2019-03-25',
                           '2019-03-26',
                           '2019-03-27',
                           '2019-03-28',
                           '2019-03-29',
                           '2019-03-30',
                           '2019-03-31',
                           ]
        # '''
        # '''
        # 先月分の各チャンネル書き込み数一覧を取得
        for file in files:
            # 先月分のファイルのみチェックする
            for last_month in last_month_list:
                if last_month in file:
                    # 'twitter' と'rss'が含まれるファイルは除外
                    if not ('rss' in channel_name or
                            'twitter' in channel_name):
                        with open(root + os.sep + file) as f:
                            channel_file = json.load(f)
                            check_date_count += len(channel_file)

        # 各取得データを配列に格納
        result_channels += [[channel_name, last_write_date, check_date_count]]
        # result_channels += [[channel_name, last_write_date]]

    """
    # チャンネルを最終更新日順にソート
    result_channels.sort(key=lambda x: x[1])
    for f in result_channels:
        print(f[0],f[1])

    # """
    # チャンネル名を勢い順にソート
    result_channels.sort(key=lambda x: x[2], reverse=True)

    rank = 0
    pre_channel = 0
    for f in result_channels:
        # 書き込みは表示しない
        if f[2] == 0:
            continue

        if f[2] != pre_channel:
            rank += 1
            pre_channel = f[2]
        print(str(rank).zfill(2), f[0], f[2])


if __name__ == '__main__':
    main()