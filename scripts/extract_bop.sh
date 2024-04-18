for file in $LOCAL_DIR/$DATASET_NAME/*.zip; do
    if [[ $file == *_base.zip ]]; then
        unzip -j "$file" -d "$(dirname "$file")"
    else
        unzip "$file" -d "$(dirname "$file")"
    fi
done

