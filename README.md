# PIDR Project "Bac a sable"

## Setup Project 
```bash
python3 -m venv venv
source .venv/bin/activate
pip install -r requirements.txt
python3 src/entrypoint.py
```

## Launch *(after setup)*
```bash
source .venv/bin/activate
python3 src/entrypoint.py

deactivate
```


## Test
```bash
source .venv/bin/activate
pytest

deactivate
```