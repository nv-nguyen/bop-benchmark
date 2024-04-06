import os
import zipfile
from tqdm import tqdm
from pathlib import Path
from argparse import ArgumentParser


def split_zip(zip_path, output_dir, max_size_in_gb=50):
    max_size_bytes = max_size_in_gb * 1024**3  # 50 GB
    output_dir.mkdir(parents=True, exist_ok=True)

    current_size = zip_path.stat().st_size
    print(f"Current size: {current_size / 1024**3:.2f} GB")
    if current_size < max_size_bytes:
        print("Zip is smaller than the max size, no need to split")
        return

    # Extract original zip
    print("Extracting zip ...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(output_dir)
    print("Extracting zip done!")

    # Calculate split
    def split_files_by_size(start_path):
        files_and_sizes = [
            (os.path.join(dirpath, f), os.path.getsize(os.path.join(dirpath, f)))
            for dirpath, dirnames, files in os.walk(start_path)
            for f in files
        ]
        files_and_sizes.sort(key=lambda x: x[1], reverse=True)

        batches = []
        current_batch = []
        current_batch_size = 0

        for file, size in files_and_sizes:
            if current_batch_size + size > max_size_bytes:
                batches.append(current_batch)
                current_batch = []
                current_batch_size = 0
            current_batch.append(file)
            current_batch_size += size

        batches.append(current_batch)  # Add the last batch
        return batches

    # Split files
    batches = split_files_by_size(str(output_dir))

    print(f"Splitting into {len(batches)} zip ...")
    # Zip files
    for i, batch in enumerate(batches, start=1):
        batch_zip_name = output_dir / f"{zip_path.stem}_part{i}.zip"
        print(f"Creating zip {batch_zip_name} ...")
        with zipfile.ZipFile(str(batch_zip_name), "w") as zipf:
            for file in tqdm(batch):
                zipf.write(file, arcname=os.path.relpath(file, str(output_dir)))
                os.remove(file)  # Remove the file after adding to the zip
        print(f"Created zip {batch_zip_name}")

    # Clean up remaining empty directories
    for dirpath, dirnames, files in os.walk(str(output_dir), topdown=False):
        if not dirnames and not files:
            os.rmdir(dirpath)

    print(f"Splitting done at {output_dir}")


if __name__ == "__main__":

    """Usage: python scripts/split_zip.py --input_zip_path /path/to/zip --output_dir /path/to/output"""
    # Set up command line argument parser
    parser = ArgumentParser(description="Visualize script for BOP dataset")
    parser.add_argument("--input_zip_path", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    parser.add_argument("--max_size_in_gb", type=int, default=50)
    args = parser.parse_args()

    # Example usage
    output_dir = Path(args.output_dir)
    split_zip(Path(args.input_zip_path), output_dir, args.max_size_in_gb)
