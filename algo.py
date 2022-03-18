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

    def _uni_clusters(self, m, t, c, r) -> list:
        # Если участников кластера столько же
        # сколько и участников группы
        result = [[] for i in range(m)]
        for i in range(m):
            result[i].append(t[0][i])
        # Для каждой группы
        for s in range(m):
            # Для каждого кластера
            for i in range(c):
                # Для каждого человека в кластере
                mx = 0
                ind = 1
                for k in range(1, r):
                    if self.f(result[s][i - 1], t[i][k]) > mx:
                        mx = self.f(result[s][i - 1], t[i][k])
                        ind = s
                    if t[i][ind] != result[s][i - 1]:
                        result[s].append(t[i][ind])
        return result

    def _not_uni_clusters(self, m, t, c, r, mode) -> list:
        if len(t[0]) > m:
            # Какие m лидеров наиболее эффективны
            leaders = t[0][:]
            leaders_eff = [0 for i in range(len(leaders))]
            for i in range(len(leaders)):
                for k in range(c):
                    mx = 0
                    for j in range(len(t[k])):
                        if self.f(leaders[i], t[k][j]) > mx:
                            mx = self.f(leaders[i], t[k][j])
                    leaders_eff[i] = mx
            leaders_eff = [(leaders_eff[i], leaders[i]) for i in range(len(leaders))]
            leaders_eff.sort()
            for i in range(len(leaders_eff) - m):
                t[1].append(leaders_eff[i][1])
                t[0].pop(t[0].index(leaders_eff[i][1]))
            # Первый случай, когда важны взаимоотношения в паре с лидером
            if mode == 1:
                for k in range(1, c):
                    # Если стало равным кол-во участников в
                    # группе и в кластерах
                    if all([r == i for i in [len(j) for j in t]]):
                        result = self._uni_clusters(m, t, c, r)
                        break

                    # Если кол-во участников k-го кластера
                    # больше, чем кол-во рабочих групп
                    if len(t[k]) > m:
                        members_eff = [0 for i in range(len(t[k]))]
                        for i in range(len(t[0])):
                            for j in range(len(t[k])):
                                members_eff[j] = self.f(t[0][i], t[k][j])
                        members_eff = [(members_eff[i], t[k][i]) for i in range(len(t[k]))]
                        members_eff.sort()
                        for i in range(len(members_eff) - m):
                            t[k + 1].append(members_eff[i][1])
                            t[k].pop(t[0].index(members_eff[i][1]))
                    # Если кол-во участников k-го кластера
                    # меньше, чем кол-во рабочих групп
                    elif len(t[k]) < m:
                        t[k + 1] += t[k][:]
            # Второй случай, когда важна общая эффективность группы
            elif mode == 2:
                # TODO
                # определить на каждом шаге максимальную пару i, j
                pass
            return result

    # Разбиение на группы
    def split_groups(self, m) -> list:
        clusters_file = open(self.file_clusters_path,'r')
        clusters = clusters_file.read()
        clusters_file.close()
        t = [list(map(int, i.split())) for i in clusters.split('\n')]
        # Кол-во кластеров
        c = len(t)
        # Кол-во участников в i-1 кластере
        tn = [len(i) for i in t]
        # Кол-во участников
        n = sum(tn)
        # Кол-во участников в группе
        r = n // m

        # Если участников кластера столько же, сколько и участников группы
        if all([r == i for i in tn]):
            result = self._uni_clusters(m, t, c, r)

        # Если участников в кластерах разное количество
        elif not all(tn[i-1] == tn[i] for i in range(1, c)):
            # Кол-во кластеров больше или равно количеству рабочих групп
            if c >= m:
                result = self._not_uni_clusters(m, t, c, r, 1)
            else:
                result = self._not_uni_clusters(m, t, c, r, 2)
        return result
