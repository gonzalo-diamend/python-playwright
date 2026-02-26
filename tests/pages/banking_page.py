from __future__ import annotations

import re

from playwright.sync_api import Page, expect


class BankingPage:
    def __init__(self, page: Page, app_url: str):
        self.page = page
        self.app_url = app_url

    def open(self) -> None:
        self.page.goto(self.app_url, wait_until="domcontentloaded")
        expect(self.page.get_by_role("button", name="Customer Login")).to_be_visible()

    def click_customer_login(self) -> None:
        self.page.get_by_role("button", name="Customer Login").click()
        expect(self.page.locator("#userSelect")).to_be_visible()

    def click_manager_login(self) -> None:
        self.page.get_by_role("button", name="Bank Manager Login").click()
        expect(self.page.get_by_role("button", name="Add Customer")).to_be_visible()

    def login_customer(self, customer_name: str) -> None:
        self.click_customer_login()
        self.page.locator("#userSelect").select_option(label=customer_name)
        self.page.locator("form[name='myForm'] button[type='submit']").click()
        expect(self.page.locator("strong", has_text="Welcome")).to_contain_text(customer_name)

    def get_balance(self) -> int:
        summary = self.page.locator("div.center", has_text="Account Number :").first
        text = summary.inner_text()
        match = re.search(r"Balance\s*:\s*(\d+)", text)
        if not match:
            raise AssertionError(f"Could not parse balance from: {text!r}")
        return int(match.group(1))

    def open_deposit_tab(self) -> None:
        self.page.get_by_role("button", name="Deposit").click()
        expect(self.page.get_by_text("Amount to be Deposited :")).to_be_visible()

    def deposit(self, amount: int) -> None:
        self.page.get_by_placeholder("amount").fill(str(amount))
        self.page.locator("form[name='myForm'] button[type='submit']").click()
        expect(self.page.locator("span.error")).to_contain_text("Deposit Successful")

    def open_withdraw_tab(self) -> None:
        self.page.get_by_role("button", name="Withdrawl").click()
        expect(self.page.get_by_text("Amount to be Withdrawn :")).to_be_visible()

    def withdraw(self, amount: int) -> None:
        self.page.get_by_placeholder("amount").fill(str(amount))
        self.page.get_by_role("button", name="Withdraw", exact=True).click()

    def open_transactions_tab(self) -> None:
        self.page.get_by_role("button", name="Transactions").click()
        expect(self.page.get_by_role("button", name="Back")).to_be_visible()

    def add_customer(self, first_name: str, last_name: str, post_code: str) -> str:
        self.click_manager_login()
        self.page.locator("button.tab", has_text="Add Customer").click()
        expect(self.page.get_by_placeholder("First Name")).to_be_visible()
        self.page.get_by_placeholder("First Name").fill(first_name)
        self.page.get_by_placeholder("Last Name").fill(last_name)
        self.page.get_by_placeholder("Post Code").fill(post_code)

        dialog_message = {"value": ""}

        def _handle_dialog(dialog) -> None:
            dialog_message["value"] = dialog.message
            dialog.accept()

        self.page.once("dialog", _handle_dialog)
        self.page.locator("form[name='myForm'] button[type='submit']").click(force=True)
        expect(self.page.locator("form[name='myForm']")).to_be_visible()
        return dialog_message["value"]

    def open_customers_tab(self) -> None:
        self.page.get_by_role("button", name="Customers").click()
        expect(self.page.get_by_placeholder("Search Customer")).to_be_visible()

    def search_customer(self, search_term: str) -> None:
        self.page.get_by_placeholder("Search Customer").fill(search_term)
