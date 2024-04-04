# bop-benchmark

Toolkit to download/upload datasets for BOP benchmark 

The official guide from HuggingFace is available for [download](https://huggingface.co/docs/huggingface_hub/main/en/guides/download) and [upload](https://huggingface.co/docs/huggingface_hub/main/en/guides/). This tutorial provides a brief overview of the process for working with BOP challenge [bop-benchmark/datasets](https://huggingface.co/datasets/bop-benchmark/datasets/).

### Downloading datasets

#### Option 1: Using `huggingface_hub`:

<details><summary>Click to expand</summary>

a. Install the library:
```
pip install --upgrade huggingface_hub
```
b. Download the dataset:
```
from huggingface_hub import snapshot_download

dataset_name = "hope"
local_dir = "./datasets"

snapshot_download(repo_id="bop-benchmark/datasets", 
                  allow_patterns=f"{dataset_name}/*zip",
                  repo_type="dataset", 
                  local_dir=local_dir)
```
If you want to download the entire BOP datasets (~3TB), please remove the `allow_patterns` argument. More options are available in the [official documentation](https://huggingface.co/docs/huggingface_hub/main/en/guides/download).

</details>


#### Option 2: Using `huggingface_hub[cli]`:

<details><summary>Click to expand</summary>

a. Install the library:
```
pip install -U "huggingface_hub[cli]"
```
b. Download the dataset:
```
export LOCAL_DIR=./datasets
export DATASET_NAME=hope

huggingface-cli download bop-benchmark/datasets --include "$DATASET_NAME/*.zip" --local-dir $LOCAL_DIR --repo-type=dataset  
```
Please remove this argument `--include "$DATASET_NAME/*.zip"` to download entire BOP datasets (~3TB). More options are available in the [official documentation](https://huggingface.co/docs/huggingface_hub/main/en/guides/download).
</details>

#### Option 3: Using `wget`:

<details><summary>Click to expand</summary>

Similar `wget` command as in [BOP website](https://bop.felk.cvut.cz/datasets/) can be used to download the dataset from huggingface hub:
```
export SRC=https://huggingface.co/datasets/bop-benchmark/datasets/resolve/main

wget $SRC/lm/lm_base.zip         # Base archive 
wget $SRC/lm/lm_models.zip       # 3D object models
wget $SRC/lm/lm_test_all.zip     # All test images ("_bop19" for a subset)
wget $SRC/lm/lm_train_pbr.zip    # PBR training images 
```
</details>

### Uploading datasets

You create a new dataset and want to share it with the BOP community. Here is a step-by-step guide to upload the dataset and create a pull request to [our huggingface hub](https://huggingface.co/datasets/bop-benchmark/datasets/).

<details><summary>Click to expand</summary>

Similar to the download process, you can upload the dataset using the `huggingface_hub` library or the command line. 

#### Option 2: Using command-line

a. Log-in and create a token
```
huggingface-cli login
```
Then go to [this link](https://huggingface.co/settings/tokens) and generate a token. IMPORTANT: the token should have write access as shown below:

<img src="./media/token_hf.png" alt="image" width="300">


Make sure you are in the bop-benchmark group by running:
```
huggingface-cli whoami
```

b. Upload
The command is applied for both folders and specific files:
```
# Usage:  huggingface-cli upload [repo_id] [local_path] [path_in_repo] --repo-type=dataset -commit-message="message"
```
For example, to upload MegaPose-GSO:
```
export LOCAL_FOLDER=~/datasets/MegaPose-GSO
export HF_FOLDER=/MegaPose-GSO

huggingface-cli upload bop-benchmark/datasets $LOCAL_FOLDER $HF_FOLDER --repo-type=dataset
```

</details>