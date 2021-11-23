# Leadbook ML Challenge

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

6. Inference

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

- `./data/departments.json`: 
- `./data/jobtitles_all.txt`: