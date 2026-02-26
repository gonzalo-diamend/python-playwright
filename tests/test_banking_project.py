from __future__ import annotations

from datetime import datetime

from playwright.sync_api import expect

from tests.pages.banking_page import BankingPage


def test_login_page_has_expected_entry_points(page, app_url):
    app = BankingPage(page, app_url)
    app.open()
    expect(page.get_by_role("button", name="Customer Login")).to_be_visible()
    expect(page.get_by_role("button", name="Bank Manager Login")).to_be_visible()


def test_customer_can_deposit_and_balance_is_updated(page, app_url):
    app = BankingPage(page, app_url)
    app.open()
    app.login_customer("Harry Potter")

    starting_balance = app.get_balance()
    deposit_amount = 200

    app.open_deposit_tab()
    app.deposit(deposit_amount)

    assert app.get_balance() == starting_balance + deposit_amount


def test_customer_cannot_withdraw_more_than_balance(page, app_url):
    app = BankingPage(page, app_url)
    app.open()
    app.login_customer("Harry Potter")

    starting_balance = app.get_balance()
    app.open_withdraw_tab()
    app.withdraw(starting_balance + 1_000)

    expect(page.locator("span.error")).to_contain_text("Transaction Failed")
    assert app.get_balance() == starting_balance


def test_manager_can_add_customer_and_find_them_in_customers_list(page, app_url):
    app = BankingPage(page, app_url)
    app.open()

    suffix = datetime.now().strftime("%H%M%S")
    first_name = f"Auto{suffix}"
    last_name = "Tester"
    post_code = "12345"

    alert_message = app.add_customer(first_name=first_name, last_name=last_name, post_code=post_code)
    assert "Customer added successfully" in alert_message

    app.open_customers_tab()
    app.search_customer(first_name)
    expect(page.locator("tbody tr").filter(has_text=f"{first_name} {last_name}").first).to_be_visible()
