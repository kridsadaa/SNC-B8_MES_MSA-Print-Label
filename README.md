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
DEFAULT_PRINTER=""
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
PORT=
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

## License

This project is licensed under the [MIT License](LICENSE).

## Contribution

If you wish to contribute to this project, please submit a pull request or
report issues in the repository.

---

This version improves readability, structure, and formatting while maintaining
clarity and completeness. Let me know if you need any more refinements!
