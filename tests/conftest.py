import os

import pytest


BASE_URL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login"


@pytest.fixture(scope="session")
def app_url() -> str:
    return os.getenv("BANKING_APP_URL", BASE_URL)
