# Leadbook ML Challenge

## Output File

The final output file is `./output/dept_preds.csv`. There are two columns:

- **Job Titles:** All the job titles provided in `./data/jobtitles_all.txt`
- **Department Predictions:** The department predictions. There can be no, one or more than one department attributed to a job title.

Example

| **Job Titles**                    | **Department Predictions**                            |
| --------------------------------- | ----------------------------------------------------- |
| art auctioneer                    | ['Art and Photography']                               |
| tv host                           | ['Entertainment']                                     |
| senior fuel and feedstocks trader | ['Energy and Mining', 'Logistics and Transportation'] |
| tiler                             | ['Construction']                                      |
| senior credit analyst             | ['Financials']                                        |

## Build from Sources

1. Clone the repo

   ```bash
   git clone https://github.com/msi1427/Leadbook-ML-Challenge.git
   cd Leadbook-ML-Challenge
   ```

2. Initialize and activate a virtual environment

   ```bash
   virtualenv --no-site-packages env
   source env/bin/activate
   ```

3. Install the dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Prepare the data

   ```bash
   py scripts/data_prep.py
   ```

   *If you want to provide a different datafile with the same format of* `./data/departments.json`, *but a different name:*

   ```bash
   py scripts/data_prep.py --raw_dept_data <json_file_name>
   ```

5. Train the Phrase Similarity Model

   ```bash
   py scripts/train.py
   ```

   *If you want to provide a different datafile with the same format of* `./data/train.csv`, *but a different name:*

   ```bash
   py scripts/train.py --train_data <csv_file_name>
   ```

   *If you want to use a particular GPU for training:*

   ```bash
   py scripts/train.py --gpu <gpu_index>
   ```

6. Inference on trained models

   ```bash
   py scripts/inference.py
   ```

   *If you want to provide a different test datafile with the same format of* `./data/train.csv`, *but a different name:*

   ```bash
   py scripts/inference.py --test_data <csv_file_name>
   ```

   *If you want to provide a different department datafile with the same format of* `./data/departments_processed.csv`, *but a different name:*

   ```bash
   py scripts/inference.py --dept_data <json_file_name>
   ```

   *If you want to use a particular GPU for training:*

   ```bash
   py scripts/inference.py --gpu <gpu_index>
   ```

   *I have trained 5 trained models. You can choose any of them for inference. By default, it will use 'paraphrase-MiniLM-L6-v2' model for inference.*

   ```bash
   py scripts/inference.py --trained_model <model_name>
   ```

## Details

**Problem Statement:** Build a model which can classify given job title into departments. A job title may have more than one department or none. <br/>

**Data:** The data provided are two files:

- `./data/departments.json`: There are **35 departments** with some indicating phrases. The data format of that file is:

  ```
  [
  	{
  		"department_name1" : ['indicating_phrase_list']
  	},
  	{
  		"department_name2" : ['indicating_phrase_list']
  	}
  ]
  ```

- `./data/jobtitles_all.txt`: There are **141564 job titles** to attribute to departments. Each line is a particular job title.

**Data Preparation:** There are 2 parts in data preparation for training the phrase similarity models:

- **Data Preprocessing:** The `./data/departments.json` file is converted to `./data/departments_processed.json` file with the file format:

  ```
  {
  	"department_name1" : ['indicating_phrase_list'],
  	"department_name2" : ['indicating_phrase_list']
  }
  ```

  The phrases are preprocessed in 2 steps:

  1. The '/'s are replaced with 'or' and '&'s are replaced with 'and'.
  2. All the words are lowercased. This is done because the provided `./data/jobtitles_all.txt` lines are lowercased.

- **Train Data Preparation:** The intuition here is that if two phrases are under a particular department, they are similar and if two phrases are not under a particular department, they are not similar. The train dataset is paired like that from `./data/departments_processed.json` file. The `./data/train.csv` have **113204** samples. The format of the train data is: 

  | **phrase1** | **phrase2**              | **score** |
  | ----------- | ------------------------ | --------- |
  | defence     | space                    | 0.9       |
  | space       | defense                  | 0.9       |
  | defence     | animation                | 0.1       |
  | defense     | motion pictures and film | 0.1       |

**Training Phrase Similarity Model:** I fine-tune [Sentence Transformers](https://sbert.net/) to measure phrase similarity for my task. The train data `./data/train.csv` is split into 90-10 as train-validation set. 5 best performing **Sentence Transformer** pretrained models were chosen as shown in the following table. While training, the batch size was 16 and the data were shuffled when building the DataLoaders. As the loss function, I use *CosineSimilarityLoss* and we use *Cosine Pearson Index* as metric. All the models are trained for 5 epochs and the model weights will be saved as `./model/{model_name}/`. The performance on validation set is shown in the following table:

| **model_name**            | **cosine_pearson** |
| ------------------------- | ------------------ |
| all-MiniLM-L6-v2          | 99.66              |
| paraphrase-mpnet-base-v2  | 99.70              |
| paraphrase-MiniLM-L6-v2   | 99.67              |
| all-mpnet-base-v2         | 99.67              |
| bert-base-nli-mean-tokens | 99.71              |

**Inference on Trained Models:** I use `paraphrase-MiniLM-L6-v2` for my inference to get the output file `./output/dept_preds.csv` because this model is  much faster than other models while performing almost closer than other. In case of production, we need to consider these tradeoffs. The inference is done in 3 steps:

- **Data Preprocessing:** There are a lot of noises in the `./data/jobtitles_all.txt` file. The preprocessing is done in 3 steps:

  1. The '/'s are replaced with 'or' and '&'s are replaced with 'and'.
  2. Remove all the punctuations.
  3. Remove all the noisy words. The noisy words I identified are the following:

- **Loading the Models:** Since the trained models are of big size, they are currently stored in Google Drive. The models are automatically downloaded whenever specified. The default model is `paraphrase-MiniLM-L6-v2`. The corpus embeddings of department topics are generated. 

- **Inference:** The inference is done in 3 steps:

  1. If all the words in the a job title is a noisy word, the title is ignored.
  2. If the job title is not English, the title is ignored. I used `polyglot` library to identify the language.
  3. The `top 20 phrases` similar to the job title is selected. If they have `>=0.5` similarity score, the departments are taken into consideration and attributed to the job title.

  More about the output file is discussed [in the first section](#output-file).

## Possible Improvements:

