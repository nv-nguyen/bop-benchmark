# bop-benchmark

Toolkit to download/upload datasets for BOP benchmark 

The official guide from HuggingFace is available for [download](https://huggingface.co/docs/huggingface_hub/main/en/guides/download) and [upload](https://huggingface.co/docs/huggingface_hub/main/en/guides/). This tutorial provides a brief overview of the process for working with BOP challenge [bop-benchmark/datasets](https://huggingface.co/datasets/bop-benchmark/datasets/).

## Downloading datasets

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

Datasets are stored in `.zip` format. You can extract them using the following command:
```
bash scripts/extract_bop.sh
```

If you are running on a machine with high bandwidth, you can increase your download speed by adding the following environment variable:
```
pip install huggingface_hub[hf_transfer]
export HF_HUB_ENABLE_HF_TRANSFER=1
```

## Uploading datasets

You create a new dataset and want to share it with BOP community. Here is a step-by-step guide to upload the dataset and create a pull request to [our huggingface hub](https://huggingface.co/datasets/bop-benchmark/datasets/). Feel free to reach out to vanngn.nguyen@gmail.com if you have any questions.

Similar to the download process, you can upload the dataset using the `huggingface_hub` library or `huggingface_hub[cli]`. We recommend using `huggingface_hub[cli]` for its simplicity.

#### Option 1: Using `huggingface_hub[cli]`:

<details><summary>Click to expand</summary>

a. Install the library:
```
pip install -U "huggingface_hub[cli]"
```

b. Log-in and create a token
```
huggingface-cli login
```
Then go to [this link](https://huggingface.co/settings/tokens) and generate a token. IMPORTANT: the token should have write access as shown below:

<img src="./media/token_hf.png" alt="image" width="300">


Make sure you are in the bop-benchmark group by running:
```
huggingface-cli whoami
```

c. Upload dataset:

The command is applied for both folders and specific files:
```
# Usage:  huggingface-cli upload bop-benchmark/datasets [local_path] [path_in_repo] --repo-type=dataset --create-pr
```
For example, to upload hope dataset:
```
export LOCAL_FOLDER=./datasets/hope
export HF_FOLDER=/hope

huggingface-cli upload bop-benchmark/datasets $LOCAL_FOLDER $HF_FOLDER --repo-type=dataset --create-pr
```

</details>

#### Option 2: Using `huggingface_hub`:

<details><summary>Click to expand</summary>

a. Install the library:
```
pip install --upgrade huggingface_hub
```
b. Creating a pull-request:

We recommend organizing the dataset in a folder and then uploading it to the huggingface hub. For example, to upload `lmo`:
```
from huggingface_hub import HfApi, CommitOperationAdd

dataset_name = "lmo"
local_dir = "./datasets/lmo"

operations = []
for file in local_dir.glob("*"):
    add_commit = CommitOperationAdd(
        path_in_repo=f"/{dataset_name}",
        path_or_fileobj=local_dir,
    )
    operations.append(add_commit)


api = HfApi()
MY_TOKEN = # get from https://huggingface.co/settings/tokens
api.create_commit(repo_id="bop-benchmark/datasets", 
                  repo_type="dataset",
                  commit_message=f"adding {dataset_name} dataset", 
                  token=MY_TOKEN,
                  operations=operations, 
                  create_pr=True)

```
If your dataset is large (> 500 GB), you can upload it in chunks by adding the `multi_commits=True, multi_commits_verbose=True,` argument. More options are available in the [official documentation](https://huggingface.co/docs/huggingface_hub/v0.22.2/en/package_reference/hf_api#huggingface_hub.HfApi.create_pull_request).

</details>

## FAQ

#### 1. How to upload a large file > 50 GB?
Note that HuggingFace limits the size of each file to 50 GB. If your dataset is larger, you can split it into smaller files:
```
zip -s 50g input.zip --out output.zip
```
This command will split the `input.zip` into multiple files of 50GB size `output.zip`, `output.z01`, `output.z01`, ... You can then extract them using one of the following commands:
```
# option 1: combine 
zip -s0 output.zip --out input.zip

# option 2: using 7z to unzip directly
7z x output.zip
```
#### 2. How to increase download speed?
If you are running on a machine with high bandwidth, you can increase your download speed by adding the following environment variable:
```
pip install huggingface_hub[hf_transfer]
export HF_HUB_ENABLE_HF_TRANSFER=1
```

