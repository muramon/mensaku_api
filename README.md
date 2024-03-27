## Flask App
ソースコードを更新したら、docker-compose buildで更新反映

## DBの初期化
/docker-entrypoint-initdb.dのスクリプトを再実行したくなったら、docker-compose down --volumeを使う。名前付きボリュームが消えてDBが完全初期化されるので注意。

## elasticsearchにデータ入れる
```
docker exec -it mensaku_feeder-master-db_1 /bin/bash
python feed_dump_to_elasticsearch.py 
```

## postgresコマンド
```
psql -h postgres -p 5432 -U root -d mensaku
```