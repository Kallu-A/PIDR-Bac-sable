# PIDR Project "Bac a sable"

## Setup Project 
### Dependencies
https://github.com/epfl-mobots/thymio-python
- Python 3 & pip

```bash
python3 -m venv venv
source venv/bin/activate
source venv/Scripts/activate
pip install -r requirements.txt
```

## Launch *(after setup)*
```bash
source venv/bin/activate
python3 src/entrypoint.py

deactivate
```

### Stop the current program
```bash
python3 -m tdmclient run --stop
```

## Test
```bash
source venv/bin/activate
pytest

deactivate
```

## Update depedencies 
```bash
pip freeze > requirements.txt 
```