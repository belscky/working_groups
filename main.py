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
    families = ["Акишев", "Астахова","Атюнкин","Авраменко",	"Бударов", "Васильев","Вашукова", "Власов", "Гордеев","Гусева","Жемалтдинов","Жестоканов","Жуков","Забелина","Затухин","Зуев","Каминцева","Купцов", "Ларин","Лебедев","Лизина",	"Лобанов","Неклюдов","Никоноров","Перфильев","Пескичев","Петрова","Ращупкин","Тайцель","Федорова","Чабан","Шарашева","Якупов","Салимов","Измайлов"]
    group = new_wg.split_groups(int(groups_number), int(mode_groups))
    print(group)
    for i in group:
        print(i[0])
        for j in i[1]:
            print(families[j])



