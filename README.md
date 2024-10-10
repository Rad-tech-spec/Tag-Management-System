# Tag Management 
[![Run Python Script Every 5 Minutes](https://github.com/Rad-tech-spec/Historian-Sarnia/actions/workflows/program.yml/badge.svg?branch=main)](https://github.com/Rad-tech-spec/Historian-Sarnia/actions/workflows/program.yml) 
## Description

This system collects raw data in `.json` format from Smart Cover API's then reforms and generates tags based on GE Historian standard and stores it in Historian.<br>

### Functionalities:<br>
- Handles infomation using `REST-API` methods such as `GET` and `PUSH`. 
- Validate and updating tokens when approppriate.
- Time and timestamp handling.
- File management using Queue and Arrays and clean up after execution. 
- Manage downtimes from servers.
- Provide clean and readable logs for trouble shooting and infomation.
- Encrypts and decrypts tokens using the `cryptography` library. 
- Senstive infomation is handled inside a `.env` file. 
- Regenerates .json files when deleted. 


## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/yourproject.git
    cd yourproject
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Ensure you have the necessary configuration files and keys in place.
2. Run the main script:
    ```sh
    python main.py
    ```

## Configuration

- Ensure that the encryption key is generated and stored correctly.
- Update the `var.SC_Token_` with the appropriate token.
- Modify the `header_sc` dictionary if necessary.

## Dependencies

- `urllib3`
- `requests`
- `cryptography`
- `logconfig`
- `queue`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.