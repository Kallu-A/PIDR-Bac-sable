# PIDR Project "Bac a sable"

## Setup Project 
### Dependencies
- [Thymio Suite](https://www.thymio.org/download-thymio-suite-redirect/)
Select the appropriate version to your computer and follow the instruction (useful link for [setup the robot](https://www.thymio.org/support/configuration-setup/))
- Python 3 & pip

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Launch *(after setup)*
open the Thymio Suite application and 
```bash
source venv/bin/activate
python3 src/entrypoint.py

deactivate
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