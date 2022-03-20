import algo as a


if __name__ == '__main__':
    TEST_PATH = r'tests/test01/'
    new_wg = a.WG(TEST_PATH)
    print(new_wg.split_groups(2))

"""
00 0 00
000 00
00 00
"""

