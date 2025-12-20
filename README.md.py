# D.co.il Automation Testing Project

This project contains automated end-to-end (E2E) tests for the D.co.il (Zap Golden Pages) website using Selenium and Python.

## Test Scenarios
The framework covers 5 major business flows:
* **Business Search:** Validating specific results for brands like Burger King.
* **Filtering System:** Testing regional and service filters for Plumbers.
* **Complex Search:** Executing searches for terms like "Coffee" and "E.R.N".
* **Price Lists:** Navigation through the price lobby and specific removals price lists.

## Features
* **Stealth Mode:** Implemented to bypass bot detection.
* **Error Handling:** Automatic screenshots on failure.
* **Explicit Waits:** Used to ensure stability and synchronization.

## How to Run
1. Install requirements: `pip install -r requirements.txt`
2. Run any script: `python test_ern_search.py`