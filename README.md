# SNC-B8 MES MSA - Print Label

## Overview

The **SNC-B8 MES MSA - Print Label** project is designed to handle label
printing for the Manufacturing Execution System (MES). This project provides a
structured approach to configuring and managing printers, along with utilities
to generate and process labels.

## Project Setup

### Prerequisites

Before running the project, ensure that you have the following installed:

- Python 3.x
- Required dependencies listed in `requirements.txt`

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/SNC-B8_MES_MSA-Print-Label.git
   cd SNC-B8_MES_MSA-Print-Label
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Environment Configuration

This project requires a `.env` file to configure essential settings.

#### Steps to Set Up `.env`

1. Create a `.env` file in the root directory.
2. Copy and paste the example below into your `.env` file.
3. Update the values according to your system configuration.

#### Example `.env` file:

```
# Printer Configuration
DEFAULT_PRINTER="Printer_POS-80"
PRINTER_PORT1=""
PRINTER_PORT2=""
PRINTER_PORT3=""
PRINTER_PORT4=""
PRINTER_PORT5=""
PRINTER_PORT6=""
PRINTER_PORT7=""
PRINTER_PORT8=""
PRINTER_PORT9=""
PRINTER_PORT10=""

# Application Port
PORT=8000
```

Ensure that the `.env` file is properly loaded in your application using
`load_dotenv()` before accessing environment variables.

### Running the Application

Start the application using the following command:

```sh
python run.py
```

## Project Structure

```
project/
├── app/
│   ├── constants/
│   │   ├── __init__.py
│   │   ├── printer.py
│   ├── helpers/
│   │   ├── __init__.py
│   │   ├── validator.py
│   │   ├── zpl.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── print.py
│   ├── types/
│   │   ├── __init__.py
│   │   ├── print.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── convert.py
│   │   ├── file.py
│   │   ├── folder.py
│   │   ├── image.py
│   │   ├── jsonify.py
│   │   ├── number.py
│   │   ├── part.py
│   │   ├── print.py
│   │   ├── scheduler.py
│   │   ├── validator.py
│   │   ├── zpl.py
│   ├── __init__.py
│   ├── routes.py
├── media/
├── temp/
│   ├── YYYY-MM-DD/
│   │   ├── images/
│   │   │   ├── labels/
│   │   │   ├── parts/
│   │   ├── zpls/
├── tests/
├── .env
├── .gitignore
├── config.py
├── LICENSE
├── README.md
├── requirements.txt
├── run.py
```

## Setting up the Application to Run on Boot

You can set up your Flask app to automatically run when your system starts using
either `systemd` .

 <!-- or `cron`. -->

<!-- #### Option 1: Using `systemd` -->

#### Using `systemd`

**Create a new `systemd` service file:**

1.  Open a terminal and create a new service file in `/etc/systemd/system/`:

```bash
sudo nano /etc/systemd/system/msa-mes-b8-printer-script.service
```

2.  Add the following content to the file:

```ini
[Unit]
Description=MSA MES B8 Printer Script
After=network.target

[Service]
WorkingDirectory=/home/username/.script/SNC-B8_MES_MSA-Print-Label
ExecStart=/home/username/.script/SNC-B8_MES_MSA-Print-Label/venv/bin/python run.py
Restart=always
User=username

[Install]
WantedBy=multi-user.target
```

3.  Reload systemd, enable the service, and start it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable msa-mes-b8-printer-script
sudo systemctl start msa-mes-b8-printer-script
```

4.  Check the status of the service:

```bash
systemctl status msa-mes-b8-printer-script
```

5.  To reload and restart the service:

```bash
sudo systemctl daemon-reload
sudo systemctl restart msa-mes-b8-printer-script
```

6.  View service log:

```bash
journalctl -u msa-mes-b8-printer-script.service -b
```

<!-- #### Option 2: Using `cron`

1.  Open the crontab editor

```bash
crontab -e
```

2.  Add the following line to run the app on reboot:

```bash
@reboot /usr/bin/python3 /path/to/your/run.py
```

3.  Save and exit the editor (Ctrl + X, then Y and Enter). -->

### Notes

Make sure to update /path/to/your/run.py with the correct path to your run.py
file.

Ensure that the create_app() function in your app module is configured correctly
for production use.

If using systemd, ensure that systemd is installed and running on your Ubuntu
system.

## License

This project is licensed under the [MIT License](LICENSE).

## Contribution

If you wish to contribute to this project, please submit a pull request or
report issues in the repository.

---

This version improves readability, structure, and formatting while maintaining
clarity and completeness. Let me know if you need any more refinements!

<!-- ---

sudo apt update sudo apt install python3-dotenv -->
<!--  -->
<!--
sodu apt install python3-pip
sodu apt install python3.12-venv

python3 -m venv venv
source venv/bin/activate
pip install python-dotenv
pip install flask
pip install flask_apscheduler
pip install flask_cors
pip install requests
pip install Pillow
-->
