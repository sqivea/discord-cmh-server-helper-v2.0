import os.path

from dotenv import load_dotenv


def load_variales() -> None:
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)


# Load the current environment variables defined in .env file.
load_variales()
