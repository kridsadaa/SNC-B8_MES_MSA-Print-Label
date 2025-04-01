# SNC-B8_MES_MSA-Print-Label

MES | MSA | Print Label

# Project Setup

## Environment Variables

This project requires a `.env` file to configure essential settings. Below is an
example of the required environment variables:

### Example `.env` file

```
# Printer configuration
DEFAULT_PRINTER=''
PRINTER_PORT1=''
PRINTER_PORT2=''
PRINTER_PORT3=''
PRINTER_PORT4=''
PRINTER_PORT5=''
PRINTER_PORT6=''
PRINTER_PORT7=''
PRINTER_PORT8=''
PRINTER_PORT9=''
PRINTER_PORT10=''

# Application port
PORT=
```

## How to Use

1. Create a `.env` file in the root directory of your project.
2. Copy and paste the above example into your `.env` file.
3. Make sure to install dependencies by running:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   python app.py
   ```

Ensure that the `.env` file is properly loaded in your application by using
`load_dotenv()` before accessing environment variables.
