#!/usr/bin/env bash

# Change into the project root
cd -- "$( dirname -- "${BASH_SOURCE[0]}" )"

# If you created a virtual python environment, source it
if [[ -f venv/bin/activate ]]; then
    echo "[*] Using virtual python environment"
    source venv/bin/activate
fi

echo "[*] Installing dependencies"
python3 -m pip install -r requirements.txt

# Install the pip package
python3 -m pip install .

# delete the output dir
[[ -d public ]] && rm -rf public


python3 -m mkdocs build -d public/

if [[ -z "$1" ]]; then
    echo "[*] To view the site run:"
    echo python3 -m http.server --directory "'$(pwd)/public/'"
else
    python3 -m http.server --directory public/ "$1"
fi
