# Unit tests: each test calls one function directly and checks its result
from app import VERSION, health_payload, render_page  # the code to test
 
 
def test_health_reports_ok():
    # the health data must say the app is running
    assert health_payload()["status"] == "ok"
 
 
def test_health_reports_version():
    # the health data must report the version in app.py
    assert health_payload()["version"] == VERSION
 
 
def test_page_lists_every_task():
    # every task we pass in must appear as a list item on the page
    page = render_page(["Write tests", "Build artifact"])
    assert "<li>Write tests</li>" in page
    assert "<li>Build artifact</li>" in page
 
 
def test_page_shows_version():
    # the version must appear on the page, even when there are no tasks
    assert f"Version {VERSION}" in render_page([])
