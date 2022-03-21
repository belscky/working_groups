import algo as a


if __name__ == '__main__':

    TEST_PATH = r'tests/test02/'
    new_wg = a.WG(TEST_PATH)
    mode = input()
    if mode == "1":
        new_wg.clustering()
    print(new_wg.split_groups(3))
