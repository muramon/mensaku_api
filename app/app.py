from flask import *
from flask_cors import CORS
from elasticsearch import Elasticsearch
import json
import ramen_review2vec
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['DATABASE'] = {
    'host': 'postgres',
    'user': 'root',
    'password': 'secret',
    'dbname': 'mensaku'
}

# 特定のオリジンだけを許可する
# cors = CORS(app, resources={r"/*": {"origins": ["192.168.10.1023"]}})
# cors = CORS(app, resources={
#     r"/api/*": {
#         "origins": ["192.168.10.102"],
#         "methods": ["GET", "POST"],  # 許可するHTTPメソッド
#         "allow_headers": ["Content-Type", "Authorization"],  # 許可するヘッダー
#         "supports_credentials": True  # クレデンシャルをサポートするか
#     }
# })

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host=app.config['DATABASE']['host'],
            user=app.config['DATABASE']['user'],
            password=app.config['DATABASE']['password'],
            dbname=app.config['DATABASE']['dbname']
        )
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    # データベースへのクエリ実行例
    db = get_db()
    cursor = db.cursor()
    # cursor.execute('SELECT s.id, s.name, i.score, m.image_url from shops s left join information i on s.id = i.shop_id left join images m on s.id = m.id;')
    cursor.execute('SELECT s.id, s.name, i.score, m.image_url from shops s left join information i on s.id = i.shop_id left join (SELECT DISTINCT ON (shop_id) shop_id, image_url FROM images ORDER BY shop_id, image_url) m on s.id = m.shop_id where m.image_url is not Null limit 30;')
    results = cursor.fetchall()
    results = [{'id':str(result[0]), 'name': (result[1]), 'score': result[2], 'img': result[3]} for result in results]
    return jsonify(results)
# @app.route('/')
# def index():
#     return "hello compose"
@app.route('/detail', methods=['GET'])
def get_detail():
    id_param = request.args.get('id')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT s.name, i.* from shops s left join information i on s.id = i.shop_id left join images m on s.id = m.id where s.id = {};'.format(id_param))
    results = cursor.fetchall()
    results = [{'address': (result[4]), 'latitude': result[5], 'longitude': result[6], 'operationg_hours': result[7], 'shop_holidays': result[8], 'sns': result[9]} for result in results]
    return jsonify(results[0])

@app.route('/title', methods=['GET'])
def get_shop_name():
    id_param = request.args.get('id')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT s.id, s.name, i.score, m.image_url from shops s left join information i on s.id = i.shop_id left join images m on s.id = m.id where s.id = {};'.format(id_param))
    results = cursor.fetchall()
    results = [{'id':str(result[0]), 'name': (result[1]), 'score': result[2], 'img': result[3]} for result in results]
    return jsonify(results)

@app.route('/recommend', methods=['GET'])
def recommend():
    store_name = request.args.get('title')
    recomemended_ramen = ramen_review2vec.recommend_ramen(store_name=store_name)
    """
    類似度が高いラーメン店の
    title: string;
    content: string;
    img: string;
    をjsonで返す
    """
    db = get_db()
    cursor = db.cursor()
    results_list = []
    for index, shop_name in recomemended_ramen.items():
        print(f"Shop Name: {shop_name}")
        cursor.execute('SELECT s.id, s.name, i.score, m.image_url from shops s left join information i on s.id = i.shop_id left join images m on s.id = m.id where s.name = \'{}\';'.format(shop_name))
        results = cursor.fetchall()
        result_list = [{'id':str(result[0]), 'name': (result[1]), 'score': result[2], 'img': result[3]} for result in results]
        results_list.append(result_list[0])
    print(results_list)
    return jsonify(results_list)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    es = Elasticsearch("http://search-engine:9200")
    # keywords="二郎"
    # extra_query_params = {}
    # body = generate_query_func(keywords, **extra_query_params)
    # print(body)
    # response = es.search(index="ramen_rank_index", body=body)
    # print(response)
    resp = es.search(index="ramen_rank_index", body={"query": {"match": {"review": "{}".format(query)}}})
    db = get_db()
    cursor = db.cursor()
    results_list = []
    for x in resp['hits']['hits']:
        shop_name = x['_source']['store_name']
        cursor.execute('SELECT s.id, s.name, i.score, m.image_url from shops s left join information i on s.id = i.shop_id left join images m on s.id = m.id where s.name = \'{}\';'.format(shop_name))
        results = cursor.fetchall()
        if len(results)!=0:
            result_list = [{'id':str(result[0]), 'name': (result[1]), 'score': result[2], 'img': result[3]} for result in results]
            results_list.append(result_list[0])
    return jsonify(results_list)

@app.route('/images', methods=['GET'])
def get_shop_images():
    id_param = request.args.get('id')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT image_url, context FROM public.images where shop_id = {} limit 9;'.format(id_param))
    results = cursor.fetchall()
    results = [{'img': result[0], 'context': result[1]} for result in results]
    return jsonify(results)

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5001,
    )
