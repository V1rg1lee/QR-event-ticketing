# event-ticketing
## Description

This project is used to generate a given number of unforgeable QR codes for event entry or other purposes. The QR codes are protected by a private key known only to the server. The QR code identifiers have UUIDs as identifiers. Once a QR code is scanned, it cannot be used a second time, so it is protected from reusability.

There are different scripts in this project:
- The basic website that allows you to scan QR codes generated on the server.
- The script to generate a certificate if you want to run the site with a self-signed certificate.
- The script to generate a private key that will be used to sign the QR codes in order to protect them against falsification.
- The script to generate QR codes.
- The script to put QR codes in a PDF.
  
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

**Warning:** this will launch the website without a certificate. The website can not work entirely like this. It's better to launch the website with a self-signed certificate if you don't have a certificate, it's described below in **Run the project with a self signed certificate**.

You have to set a "PASSWORD" environment variable to run the project. The password will be used by staff to connect to the site on the interface to scan.

You can do it with the following command on linux:

```bash
export PASSWORD="your_password"
```

Then you can launch the website with the following command:
(Be careful, you need to generate the private key and the QR codes before running the website, you can do it with the additional scripts described below)

```bash
python -E -m event-ticketing
```

### Run the project with a self signed certificate

You have to set a "PASSWORD" environment variable to run the project. The password will be used by staff to connect to the site on the interface to scan.
If you want to use self signed certificate, you can use the "certif_gen.py" script as described below.

You can do it with the following command on linux:

```bash
export PASSWORD="your_password"
```

Then you can launch the website with the following command:
(Be careful, you need to generate the private key and the QR codes before running the website, you can do it with the additional scripts described below)

```bash
python -E -m event-ticketing --ssl
```

If you want to use the website with your own certificate, you can put your `cert.pem` and `key.pem` files in the `certs` directory.

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
