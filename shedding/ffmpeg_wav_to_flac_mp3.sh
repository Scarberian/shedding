ffmpeg -y -i "$track - $artist - $title".wav -i "$track - $artist - $title".txt -map_metadata 1 -id3v2_version 3 -wri    te_id3v1 1  -acodec flac "$track - $artist - $title".flac\
metaflac --import-picture-from=folder.jpg "$track - $artist - $title".flac\
ffmpeg -y -i "$track - $artist - $title".wav -i "$track - $artist - $title".txt -i folder.jpg -map_metadata 1 -map 0     -map 2 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (Front)" -id3v2_version 3 -write_id3v1 1 -acodec m    p3 -b:a 320k "$track - $artist - $title".mp3\

