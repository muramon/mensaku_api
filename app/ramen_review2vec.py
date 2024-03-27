from flask import *
import pandas as pd
from gensim.models import Doc2Vec


def recommend_ramen(store_name=None):
    # モデルをファイルから読み込む
    model = Doc2Vec.load("./models/ramen2vec_model")
    df = pd.read_csv('./models/tokyo_ramen_review.csv')
    df_ramen = df.groupby(['store_name','score','review_cnt'])['review'].apply(list).apply(' '.join).reset_index().sort_values('score', ascending=False)
    
    index = df_ramen.reset_index().query('store_name == "{}"'.format(store_name)).index
    result = pd.DataFrame(model.docvecs.most_similar(index),columns=["index","類似度"])
    result["store_name"] = result["index"].apply(lambda x : df_ramen.iloc[x,0])
    return result["store_name"]
    