import os

import pytest
import requests

def assert_within_budget(r, budget):
    took = r.elapsed.total_seconds()
    assert took < budget, f"took {took:.2f}s, budget {budget}s"