import algo as a


if __name__ == '__main__':

    TEST_PATH = r'tests/test01/function.txt'
    new_wg = a.WG(TEST_PATH)
    new_wg.clustering()
    mode_groups = input("mode_groups: ")
    groups_number = input("groups_number: ")
    reverse = input("Reverse: ")
    group = new_wg.split_groups(int(groups_number), int(mode_groups), bool(int(reverse)))
    print(group)
    #for i in group:
        #print(i[0])
        #for j in i[1]:
            #print(families[j])



