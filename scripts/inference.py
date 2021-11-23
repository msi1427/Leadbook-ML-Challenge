from gdown.download import download
from sentence_transformers import SentenceTransformer, util, models
import preprocessing
import argparse, os, json
import torch
import gdown
from tqdm import tqdm
import pandas as pd
from polyglot.detect import Detector
from polyglot.detect.base import logger as polyglot_logger
polyglot_logger.setLevel("ERROR")

parser = argparse.ArgumentParser()
parser.add_argument('--test_data', type=str, default='jobtitles_all.txt', help='')
parser.add_argument('--dept_data', type=str, default='departments_processed.json', help='')
parser.add_argument('--gpu', type=int, default=0, help='')
parser.add_argument('--trained_model', type=str, default='paraphrase-MiniLM-L6-v2', help='')
args = parser.parse_args()
device=torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() else "cpu")

def preprocess_data(phrase_list : list):
    phrase_list = preprocessing.replace_and_or(phrase_list)
    phrase_list = preprocessing.keep_alnum_batch(phrase_list)
    phrase_list = preprocessing.remove_noisy_words(phrase_list)
    return phrase_list

def map_dept_topics(root_dir: str):
    with open(f"{root_dir}data/{args.dept_data}", 'r') as fp:
        department_dict = json.load(fp)
    topic_map = {value : key for key,value_list in department_dict.items() for value in value_list}
    return topic_map

def download_trained_model(root_dir: str):
    gdown_id = ""
    if args.trained_model == "all-MiniLM-L6-v2": gdown_id = "1-17X2-loxZ4DQqzMVE0RQXTgL8EwQOdx"
    elif args.trained_model == "all-mpnet-base-v2": gdown_id = "11mND3vAIshua3Ou5VutSecENbd_QRwNU"
    elif args.trained_model == "bert-base-nli-mean-tokens": gdown_id = "12nB5bdPrY93xKCmhK_BiWQ0VcimAoWq3"
    elif args.trained_model == "paraphrase-MiniLM-L6-v2": gdown_id = "10jZwCRjegapZ1JRI5W5hWoU7b5wITvbh"
    elif args.trained_model == "paraphrase-mpnet-base-v2": gdown_id = "1-kgb0K1DwBk7vqsRaRi2q3W4dP4cZjJU"
    os.chdir(f"{root_dir}models")
    url = f'https://drive.google.com/drive/folders/{gdown_id}?usp=sharing'
    gdown.download_folder(url)
    os.chdir(f"{root_dir}scripts")
    return

def get_dept_preds(queries,embedder,corpus_embeddings):
    top_k = 20
    dept_prediction = []

    for query in tqdm(queries):
        preds = []
        if len(query.split())==0: 
            dept_prediction.append(preds)
            continue
        
        try:
            lang_detector = Detector(query)
            if lang_detector.language.name != "English": 
                dept_prediction.append(preds)
                continue 
        except:
            dept_prediction.append(preds)
            continue

        query_embedding = embedder.encode(query, convert_to_tensor=True)
        cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
        top_cos_results = torch.topk(cos_scores, k=top_k)

        for score,idx in zip(top_cos_results[0],top_cos_results[1]):
            if float(score) >= 0.5:
                topic = corpus[int(idx)]
                preds.append(topic_map[topic])
        preds = list(set(preds))

        dept_prediction.append(preds)
    
    return dept_prediction

if __name__ == "__main__" :
    root_dir = os.path.dirname(os.path.abspath(__file__)) + "/../"
    with open( f"{root_dir}data/jobtitles_all.txt", 'r') as fp:
        job_titles = fp.read()
    job_titles = job_titles.split("\n")
    job_titles_processed = preprocess_data(job_titles)
    topic_map = map_dept_topics(root_dir)
    download_trained_model(root_dir)
    
    embedder = SentenceTransformer(f"{root_dir}models/{args.trained_model}/",device=device)
    corpus = list(topic_map.keys())
    queries = job_titles_processed
    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

    print("Inference:")
    dept_prediction = get_dept_preds(queries,embedder,corpus_embeddings)

    pred_df = pd.DataFrame()
    pred_df["Job Titles"] = job_titles
    pred_df["Department Predictions"] = dept_prediction
    pred_df.to_csv(f"{root_dir}output/dept_preds.csv",index=False)
    print("\nInference Complete")