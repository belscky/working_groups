import algo as a


if __name__ == '__main__':

    TEST_PATH = r'tests/test01/'
    new_wg = a.WG(TEST_PATH)
    print("mode_cluster: ")
    mode_cluster = input()
    if mode_cluster == "1":
        new_wg.clustering()
    print("mode_groups: ")
    mode_groups = input()
    print("groups_number: ")
    groups_number = input()
    print(new_wg.split_groups(int(groups_number), int(mode_groups)))

