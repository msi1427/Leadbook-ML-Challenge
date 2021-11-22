import pandas as pd
from sklearn.model_selection import train_test_split
import os, argparse, torch
from sentence_transformers import SentenceTransformer, InputExample, losses, evaluation
from torch.utils.data import DataLoader

parser = argparse.ArgumentParser()
parser.add_argument('--train_data', type=str, default='train.csv', help='')
parser.add_argument('--gpu', type=int, default=0, help='')
args = parser.parse_args()

device=torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() else "cpu")

if __name__ == "__main__" : 
    dept_data_file_name = args.train_data
    root_dir = os.path.dirname(os.path.abspath(__file__)) + "/../"
    
    df = pd.read_csv(root_dir + "data/train.csv")
    train_df, valid_df = train_test_split(df, test_size=0.1, random_state=42)

    pretrained_models = ["all-MiniLM-L6-v2",           
                        "paraphrase-mpnet-base-v2",    
                        "paraphrase-MiniLM-L6-v2",   
                        "all-mpnet-base-v2",        
                        "bert-base-nli-mean-tokens"]   

    train_examples = [InputExample(texts=[row['phrase1'],row['phrase2']],label=row['score']) for idx,row in train_df.iterrows()]
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)

    phrase1 = [ phrase for phrase in valid_df['phrase1']]
    phrase2 = [ phrase for phrase in valid_df['phrase2']]
    scores = [ score for score in valid_df['score']]

    evaluator = evaluation.EmbeddingSimilarityEvaluator(phrase1, phrase2, scores)

    for model_name in pretrained_models:
        print(f"Finetuning {model_name}")
        model = SentenceTransformer(model_name, device=device)
        train_loss = losses.CosineSimilarityLoss(model)
        model.fit(train_objectives=[(train_dataloader, train_loss)], 
                    epochs=5, 
                    warmup_steps=100, 
                    evaluator=evaluator, 
                    evaluation_steps=500,
                    output_path= f"{root_dir}/models/{model_name}/")

    