for file in $LOCAL_DIR/*.zip; do
    if [[ $file == *_base.zip ]]; then
        unzip -j "$file" -d "$(dirname "$file")"
    else
        unzip "$file" -d "$(dirname "$file")"
    fi
done

