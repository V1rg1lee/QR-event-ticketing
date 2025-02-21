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

You have to set a "PASSWORD" environment variable to run the project.

```bash
python -E -m event-ticketing
```

### Run the project with a self signed certificate

You have to set a "PASSWORD" environment variable to run the project. 
If you want to use self signed certificate, you can use the "certif_gen.py" script as described below.

```bash
python -E -m event-ticketing --ssl
```

### Run the scripts

#### Install the optional dependencies

```bash
pip install .[scripts]
```

#### Run the scripts

You must be in the root directory of the project to run the scripts.

```bash
python -E ./scripts/certif_gen.py
```

```bash
python -E ./scripts/private_key_gen.py
```

```bash
python -E ./scripts/gen_qr_code.py
```

```bash
python -E ./scripts/print_qr.py
```
