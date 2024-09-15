#!/usr/bin/env bash

# Downloads all docker mod scripts
MODS=$(curl https://theme-park.dev/themes.json | jq -r '.["docker-mods"]')
if [[ "$0" == "bash" ]]; then
    DIR="/tmp/theme-park-mods"
else
    DIR="$0"
fi
mkdir -p "$DIR"
printf "\nSaving mods into $DIR\n\n"
jq -r 'to_entries | map(.key + "|" + (.value | tostring)) | .[]' <<< "$MODS" | \
  while IFS='|' read key value; do
    download_file="$DIR/98-themepark-$key"
    curl "$value" --create-dirs --output "$download_file" --silent
    echo "Fetched $key script"

    # Convert line endings from CRLF to LF manually
    if [[ "$(tail -c2 "$download_file")" == $'\r\n' ]]; then
      perl -pi -e 's/\r\n/\n/' "$download_file"
    fi
  done
chmod -R +x "$DIR"