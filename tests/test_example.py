def test_example_dot_com_title(page):
    page.goto("https://example.com")
    assert "Example Domain" in page.title()
