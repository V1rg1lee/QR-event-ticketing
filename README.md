# event-ticketing

## Usage

### Install the project

```bash
git clone https://github.com/V1rg1lee/event-ticketing.git
cd event-ticketing
```

### Install the dependencies

```bash
python -m venv env
source env/bin/activate # for linux
env\Scripts\activate # for windows
pip install .
```

### Run the project

```bash
python -m event-ticketing
```

### Run the project with a self signed certificate

```bash
python -m event-ticketing --ssl
```

### Run the scripts

#### Install the optional dependencies

```bash
pip install .[scripts]
```

#### Run the scripts

You must be in the root directory of the project to run the scripts.

```bash
python ./scripts/private_key_gen.py
```

```bash
python ./scripts/gen_qr_code.py
```

```bash
python ./scripts/print_qr.py
```
