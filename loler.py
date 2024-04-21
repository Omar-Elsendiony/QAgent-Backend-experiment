import re

txt = """'FAIL: test_has_close_elements_first_and_last_close (__main__.TestHasCloseElements.test_has_close_elements_first_and_last_close)\nTraceback (most recent call last):\n  File "<string>", line 40, in test_has_close_elements_first_and_last_close\nAssertionError: False is not true\n\n'"""
# lol = re.search(r"[=]{70}(.)+?-{70}", txt, re.DOTALL)
lol = re.search(r"(ERROR|FAIL):(.)+?(ERROR|FAIL)", txt, re.DOTALL)
if lol is None:
    lol = re.search(r"(ERROR|FAIL):(.)+", txt, re.DOTALL)
    print(lol)
lol = lol.group(0)
lol = lol[:-6]
print(lol)
# lol = re.search(r"=(.+)\-", txt)

# print(lol.group(1))
