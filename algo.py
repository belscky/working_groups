import numpy as np
class WG:
    def __init__(self, file_path: str):
        self.file_function_path = file_path + 'function.txt'
        self.file_clusters_path = file_path + 'clusters.txt'
        file = open(self.file_function_path, 'r')
        self.function = [list(map(int, h.split())) for h in file.read().split('\n')]
        file.close()

    # Характеристическая функция для пары людей
    def f(self, i: int, j: int) -> int:
        return self.function[i][j]

    # Характеристическая функция для группы
    def F(self, s: list) -> int:
        k = len(s)
        if k == 1:
            return 0
        result = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    result += self.f(s[i], s[j])
        return result

    def _uni_clusters(self, groups_number: int, clusters: list) -> list:
        clusters_number = len(clusters)
        # Если участников кластера столько же
        # сколько и участников группы
        result = [[] for i in range(groups_number)]
        for i in range(groups_number):
            result[i].append(clusters[0][i])
        # Для каждого кластера
        for k in range(1, clusters_number):
            # Для каждой группы
            for s in range(groups_number):
                # Для каждого человека в кластере
                mx = 0
                ind = 0
                for i in range(len(clusters[k])):
                    effect = self.F(result[s] + [clusters[k][i]])
                    if effect > mx:
                        mx = effect
                        ind = i
                result[s].append(clusters[k][ind])
                clusters[k].pop(ind)
        return result

    def _not_uni_clusters(self, groups_number: int, clusters: list, mode: int) -> list:
        clusters_number = len(clusters)
        people_group_number = sum([len(i) for i in clusters]) // groups_number

        if len(clusters[0]) > groups_number:
            # Какие m лидеров наиболее эффективны
            leaders = clusters[0][:]
            leaders_eff = [0 for i in range(len(leaders))]
            for i in range(len(leaders)):
                for k in range(clusters_number):
                    mx = 0
                    for j in range(len(clusters[k])):
                        if self.f(leaders[i], clusters[k][j]) > mx:
                            mx = self.f(leaders[i], clusters[k][j])
                    leaders_eff[i] = mx
            leaders_eff = [(leaders_eff[i], leaders[i]) for i in range(len(leaders))]
            leaders_eff.sort()
            for i in range(len(leaders_eff) - groups_number):
                clusters[1].append(leaders_eff[i][1])
                clusters[0].pop(clusters[0].index(leaders_eff[i][1]))
            # Первый случай, когда важны взаимоотношения в паре с лидером
            if mode == 1:
                k = 1
                # Пока кластеры не унифицируются
                while not all([people_group_number == i for i in [len(j) for j in clusters]]):
                    # Если кол-во участников k-го кластера
                    # больше, чем кол-во рабочих групп
                    if len(clusters[k]) > groups_number:
                        members_eff = [0 for i in range(len(clusters[k]))]
                        for i in range(len(clusters[0])):
                            for j in range(len(clusters[k])):
                                members_eff[j] = self.f(clusters[0][i], clusters[k][j])
                        members_eff = [(members_eff[i], clusters[k][i]) for i in range(len(clusters[k]))]
                        members_eff.sort()
                        for i in range(len(members_eff) - groups_number):
                            clusters[k + 1].append(members_eff[i][1])
                            clusters[k].pop(clusters[0].index(members_eff[i][1]))
                    # Если кол-во участников k-го кластера
                    # меньше, чем кол-во рабочих групп
                    elif len(clusters[k]) < groups_number:
                        if k + 1 <= len(clusters) - 1:
                            clusters[k + 1] += clusters[k][:]
                        else:
                            clusters.append(clusters[k][:])
                    k += 1
                result = self._uni_clusters(groups_number, clusters)
            # Второй случай, когда важна общая эффективность группы
            elif mode == 2:
                # TODO
                # определить на каждом шаге максимальную пару i, j
                pass
            return result

    # Разбиение на группы
    def split_groups(self, groups_number: int) -> list:
        clusters_file = open(self.file_clusters_path, 'r')
        clusters = clusters_file.read()
        clusters_file.close()
        clusters = [list(map(int, i.split())) for i in clusters.split('\n')]
        # Кол-во кластеров
        clusters_number = len(clusters)
        # Кол-во участников в i-1 кластере
        people_one_cluster = [len(i) for i in clusters]
        # Кол-во участников
        people_number = sum(people_one_cluster)
        # Кол-во участников в группе
        people_group_number = people_number // groups_number

        # Если участников кластера столько же, сколько и участников группы
        if all([people_group_number == i for i in people_one_cluster]):
            result = self._uni_clusters(groups_number, clusters)

        # Если участников в кластерах разное количество
        elif not all(people_one_cluster[i - 1] == people_one_cluster[i] for i in range(1, clusters_number)):
            # Кол-во кластеров больше или равно количеству рабочих групп
            if clusters_number >= groups_number:
                result = self._not_uni_clusters(groups_number, clusters, 1)
            else:
                result = self._not_uni_clusters(groups_number, clusters, 2)
        return result

    def clustering(self):
        f = open(self.file_function_path)
        A = []
        T = []
        for line in f:
            targ = list(map(int, line.split()))
            A.append(targ)
            T.append(list(map(bool, targ.copy())))
        A = np.array(A)
        T = np.array(T)

        # Проверка на правильность

        n = len(A)
        for i in A:
            if len(A) != len(i):
                exit()
        # Построение транзитивной матрицы

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    T[i][j] = T[i][j] or (T[i][k] and T[k][j])

        # Столбец сумм строк

        S = []
        Flag = False
        for i in range(n):
            if False in T[i]:
                Flag = True
            S.append(sum(T[i]))

        if Flag == False:
            exit(0)

        # Матрица перестановок

        S_sort = sorted(S.copy(), reverse=True)
        P = [[0] * n for i in range(n)]
        for i in range(n):
            P[i][S.index(S_sort[i])] = 1
            if i != 0 and S_sort[i] == S_sort[i - 1]:
                P[i][S.index(S_sort[i])] = 0
                P[i][S.index(S_sort[i], P[i - 1].index(1) + 1)] = 1

        P = np.array(P)

        # Матрица

        #P_t = P.transpose()
        #Tau = P.dot(T).dot(P_t)
        #K = P.dot(A).dot(P_t)
        f = open(self.file_clusters_path, "w")
        i = 0
        print(np.where(P[i] == 1)[0][0])
        f.write(str(np.where(P[i] == 1)[0][0]))
        i += 1
        while i != n:
            if S_sort[i] == S_sort[i - 1]:
                f.write(" " + str(np.where(P[i] == 1)[0][0]))
            else:
                f.write("\n" + str(np.where(P[i] == 1)[0][0]))
            i += 1
        f.close()