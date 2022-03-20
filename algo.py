class WG:
    def __init__(self, file_path: str):
        self.file_function_path = file_path + 'function.txt'
        self.file_clusters_path = file_path + 'clusters.txt'

    # Характеристическая функция для пары людей
    def f(self, i: int, j: int) -> int:
        file = open(self.file_function_path, 'r')
        function = [list(map(int, h.split())) for h in file.read().split('\n')]
        file.close()
        return function[i][j]

    # Характеристическая функция для группы
    def F(self, s: list) -> int:
        k = len(s)
        result = 0
        for i in range(k):
            for j in range(k):
                if i != j:
                    result += self.f(s[i], s[j])
        return result

    def _uni_clusters(self, groups_number, clusters) -> list:
        clusters_number = len(clusters)
        people_group_number = sum([len(i) for i in clusters]) // groups_number
        # Если участников кластера столько же
        # сколько и участников группы
        result = [[] for i in range(groups_number)]
        for i in range(groups_number):
            result[i].append(clusters[0][i])
        # Для каждой группы
        for s in range(groups_number):
            # Для каждого кластера
            for i in range(clusters_number):
                # Для каждого человека в кластере
                mx = 0
                ind = 1
                for k in range(1, people_group_number):
                    if self.f(result[s][i - 1], clusters[i][k]) > mx:
                        mx = self.f(result[s][i - 1], clusters[i][k])
                        ind = s
                    if clusters[i][ind] != result[s][i - 1]:
                        result[s].append(clusters[i][ind])
        return result

    def _not_uni_clusters(self, groups_number, clusters, mode) -> list:
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
                for k in range(1, clusters_number):
                    # Если стало равным кол-во участников в
                    # группе и в кластерах
                    if all([people_group_number == i for i in [len(j) for j in clusters]]):
                        result = self._uni_clusters(groups_number, clusters)
                        break

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
                        if clusters[k + 1] is not None:
                            clusters[k + 1] += clusters[k][:]
                        else:
                            clusters.append(clusters[k][:])
            # Второй случай, когда важна общая эффективность группы
            elif mode == 2:
                # TODO
                # определить на каждом шаге максимальную пару i, j
                pass
            return result

    # Разбиение на группы
    def split_groups(self, groups_number) -> list:
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