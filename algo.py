import numpy as np


class WG:

    def __init__(self, file_path: str):
        file = open(file_path, 'r')
        self.function = [list(map(int, h.split())) for h in file.read().split('\n')]
        file.close()
        self.length = len(self.function)
        self.clusters = []

    # Характеристическая функция для пары людей

    def f(self, i: int, j: int) -> int:
        return self.function[i][j]

    # Характеристическая функция для группы
    def f_new_group(self, s: list) -> int:
        k = len(s)
        if k == 1:
            return 0
        result = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    result += self.f(s[i], s[j])
        return result

    def f_group(self, s: list, result, element) -> int:
        k = len(s)
        for i in range(k):
            result += self.f(s[i], element) + self.f(element, s[i])
        return result

    def _uni_clusters(self, groups_number: int, clusters: list) -> list:
        clusters_number = len(clusters)
        # Если участников кластера столько же
        # сколько и участников группы
        result = [[0, [clusters[0][i]]] for i in range(groups_number)]

        # Для каждого кластера
        for k in range(1, clusters_number):
            # Для каждой группы
            result.sort()
            for s in range(groups_number):
                # Для каждого человека в кластере
                mx = 0
                ind = 0
                for i in range(len(clusters[k])):
                    effect = self.f_group(result[s][1], result[s][0], clusters[k][i])
                    if effect >= mx:
                        mx = effect
                        ind = i
                result[s][1].append(clusters[k][ind])
                result[s][0] = mx
                clusters[k].pop(ind)
        return result

    def _not_uni_clusters(self, groups_number: int, clusters: list, mode: int, people_number, fl: bool) -> list:
        while len(clusters[0]) < groups_number:
            # соединить первые группы пока не станет больше
            clusters[1] += clusters[0]
            clusters.pop(0)

        if len(clusters[0]) > groups_number:
            # Какие m лидеров наиболее эффективны
            leaders = clusters[0][:]
            leaders_eff = [0 for _ in range(len(leaders))]
            for i in range(len(leaders)):
                mx = 0
                for k in range(people_number):
                    mx += self.f(k, leaders[i])
                leaders_eff[i] = mx
            leaders_eff = [(leaders_eff[i], leaders[i]) for i in range(len(leaders))]
            leaders_eff.sort()
            if len(clusters) == 1:
                clusters.append([])
            for i in range(len(leaders_eff) - groups_number):
                clusters[1].append(leaders_eff[i][1])
                clusters[0].pop(clusters[0].index(leaders_eff[i][1]))

        # Первый случай, когда важны взаимоотношения в паре с лидером
        if mode == 1:
            k = 1
            # Пока кластеры не унифицируются
            while not ((all([groups_number == i for i in [len(clusters[j]) for j in range(len(clusters)-1)]]))
                       and (groups_number >= len(clusters[-1]))):
                # Если кол-во участников k-го кластера
                # больше, чем кол-во рабочих групп
                if len(clusters[k]) > groups_number:
                    members_eff = [0 for _ in range(len(clusters[k]))]
                    for i in range(len(clusters[0])):
                        for j in range(len(clusters[k])):
                            members_eff[j] = self.f(clusters[0][i], clusters[k][j])
                    members_eff = [(members_eff[i], clusters[k][i]) for i in range(len(clusters[k]))]
                    members_eff.sort()
                    if len(clusters) == k + 1:
                        clusters.append([])
                    for i in range(len(members_eff) - groups_number):
                        clusters[k + 1].append(members_eff[i][1])
                        clusters[k].pop(clusters[k].index(members_eff[i][1]))
                    k += 1
                # Если кол-во участников k-го кластера
                # меньше, чем кол-во рабочих групп
                elif len(clusters[k]) < groups_number:
                    if k + 1 <= len(clusters) - 1:
                        clusters[k + 1] += clusters[k][:]
                        clusters.pop(k)
                else:
                    k += 1
            if len(clusters[-1]) == groups_number:
                result = self._uni_clusters(groups_number, clusters)
            else:
                result = self._uni_clusters(groups_number, clusters[:len(clusters)-1])
                flags_result = [True] * groups_number
                for i in range(len(clusters[-1])):
                    mx = 0
                    ind = -1
                    for j in range(groups_number):
                        if flags_result[j]:
                            effect = self.f_new_group(result[j][1]+[clusters[-1][i]])
                            if mx < effect:
                                mx = effect
                                if ind != -1:
                                    flags_result[ind] = True
                                ind = j
                                flags_result[ind] = False
                    result[ind][1].append(clusters[-1][i])
                    result[ind][0] = mx

        # Второй случай, когда важна общая эффективность группы
        elif mode == 2:
            result = [[0, [clusters[0][i]]] for i in range(groups_number)]
            i = 1
            while i < len(clusters):
                while len(clusters[i]) < groups_number and i != len(clusters)-1:
                    # соединить первые группы пока не станет больше
                    clusters[i + 1] += clusters[i]
                    clusters.pop(i)
                # Надо ли reserve?
                result.sort(reverse=fl)
                if i == len(clusters) - 1 and len(clusters[i]) < groups_number:
                    flags = [True] * groups_number
                    for k in range(len(clusters[i])):
                        mx = 0
                        ind = -1
                        for j in range(groups_number):
                            if flags[j]:
                                effect = self.f_group(result[j][1], result[j][0], clusters[i][k])
                                if mx < effect:
                                    mx = effect
                                    if ind != -1:
                                        flags[ind] = True
                                    ind = j
                                    flags[ind] = False
                        result[ind][1].append(clusters[i][k])
                        result[ind][0] = mx
                else:
                    flags = [True] * len(clusters[i])
                    for j in range(groups_number):
                        mx = 0
                        ind = -1
                        for k in range(len(clusters[i])):
                            if flags[k]:
                                effect = self.f_group(result[j][1], result[j][0], clusters[i][k])
                                if mx < effect:
                                    mx = effect
                                    if ind != -1:
                                        flags[ind] = True
                                    ind = k
                                    flags[ind] = False
                        result[j][1].append(clusters[i][ind])
                        result[j][0] = mx
                if len(clusters[i]) > groups_number:
                    if len(clusters) == i + 1:
                        clusters.append([])
                    for j in range(len(flags)):
                        if flags[j]:
                            clusters[i + 1].append(clusters[i][j])
                            # Не удаляю из кластера i, потому что мы к нему больше не вернемся

                i += 1
        return result

    # Разбиение на группы
    def split_groups(self, groups_number: int, mode: int, fl: bool) -> list:

        # Кол-во участников
        people_number = sum([len(i) for i in self.clusters])
        # Кол-во участников в группе
        people_group_number = people_number // groups_number

        # Если участников кластера столько же, сколько и участников группы
        # на случай неравного количества людей в группе
        group_flag = all([groups_number == i for i in [len(j) for j in self.clusters]])
        # not_equal = not all(people_one_cluster[i - 1] == people_one_cluster[i] for i in range(1, clusters_number))
        if group_flag and people_group_number == len(self.clusters):
            result = self._uni_clusters(groups_number, self.clusters)

        else:
            # Кол-во кластеров больше или равно количеству рабочих групп
            result = self._not_uni_clusters(groups_number, self.clusters, mode, people_number, fl)
        return result

    def clustering(self):
        a = self.function
        t = []
        for i in range(self.length):
            t.append(list(map(int, map(bool, a[i]))))
        a = np.array(a)
        t = np.array(t)
        # Проверка на правильность
        for i in a:
            if len(a) != len(i):
                exit()
        flag = False
        while not flag:
            # Построение транзитивной матрицы
            for k in range(self.length):
                for i in range(self.length):
                    for j in range(self.length):
                        t[i][j] = t[i][j] or (t[i][k] and t[k][j])

            # Столбец сумм строк
            s = []

            for i in range(self.length):
                if False in t[i]:
                    flag = True
                s.append(sum(t[i]))

            if not flag:
                t = []
                for i in range(self.length):
                    for j in range(self.length):
                        a[i][j] -= 1
                        if a[i][j] < 0:
                            a[i][j] = 0
                    t.append(list(map(bool, a[i])))
        # Матрица перестановок

        s_sort = sorted(s.copy(), reverse=True)
        p = [[0] * self.length for _ in range(self.length)]
        for i in range(self.length):
            p[i][s.index(s_sort[i])] = 1
            if i != 0 and s_sort[i] == s_sort[i - 1]:
                p[i][s.index(s_sort[i])] = 0
                p[i][s.index(s_sort[i], p[i - 1].index(1) + 1)] = 1

        p = np.array(p)

        # Матрица
        # P_t = P.transpose()
        # Tau = P.dot(T).dot(P_t)
        # K = P.dot(A).dot(P_t)
        i = 0
        self.clusters.append([np.where(p[i] == 1)[0][0]])
        i += 1
        while i != self.length:
            if s_sort[i] == s_sort[i - 1]:
                self.clusters[-1].append(np.where(p[i] == 1)[0][0])
            else:
                self.clusters.append([np.where(p[i] == 1)[0][0]])
            i += 1
