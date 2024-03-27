# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import csv

# Elasticsearchクライアントの初期化
es = Elasticsearch("http://localhost:9200/")  # Elasticsearchのホストとポートを適切に設定

# CSVファイルのパス
# csv_file_path = './outputs/tokyo_ramen_review.csv'
csv_file_path = '/Users/muramoto/dev_project/ramen_rank/get_ramen_data/outputs/tokyo_ramen_review_group.csv'

# Elasticsearchのインデックス名
index_name = 'ramen_rank_index'

def generate_bulk_buffer():
    buf = []
    # CSVファイルを読み込んでElasticsearchにBulkインポート
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # bulk_data = []

        for row in reader:
            # インデックス化するデータを作成
            buf.append({
                "_index": index_name,
                "_id": row["index"],
                "_source": {
                    "store_name": row["store_name"],
                    "score": row["score"],
                    "review_cnt": row["review_cnt"],
                    "review": row["review"]
                }
            })
            if 500 <= len(buf):  # 500記事ずつバッファして返す
                    yield buf
                    buf.clear()
            # bulk_data.append(action)
        if buf:  # 最後に端数の記事を返す
            yield buf

        # Bulkインポートを実行
for buf in generate_bulk_buffer():
    try:
        helpers.bulk(es, buf, refresh="true")
    except Exception:
        pass  # ハンズオンのため、例外を無視する
es.close()
