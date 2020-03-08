#!/usr/bin/env python3

import numpy as np
from tqdm import trange, tqdm


inputs = ['a_example', 'b_small', 'c_medium', 'd_quite_big', 'e_also_big']
MaxMemory = 8 * 10 ** 9 # 8GB RAM
USE_BOTTOM_UP = True


class Problem:

    def __init__(self):

        pass


    #
    # Prepare input for processing
    #
    def _prepare_input(self, in_filename):

        with open('input/' + in_filename, 'r') as in_file:
            self.M, self.N = map(int, in_file.readline().split())
            self.S = list(map(int, in_file.readline().rstrip().split()))


    #
    # generate output files
    #
    def _generate_output(self, out_filename):

        with open('output/' + out_filename, 'w') as out_file:
            out_file.write(str(len(self.selected_types)) + '\n')
            out_file.write(' '.join(map(str, self.selected_types)))


    #
    # Bottom-up approch
    #
    def knapsack00_BU(self):

        slices = np.hstack(([0], self.S))
        dp = np.zeros((self.N + 1, self.M + 1), dtype=np.int64)
        for i in tqdm(range(1, self.N + 1)):
            for j in range(self.M + 1):
                if slices[i] > j:
                    dp[i, j] = dp[i-1, j]
                else:
                    dp[i, j] = max(dp[i-1, j-slices[i]] + slices[i], dp[i-1, j])

        i, j, types, total_slices = self.N, self.M, [], 0
        while i > 0 and j > 0:
            while dp[i, j] == dp[i-1, j] and j >= 0:
                i -= 1

            if i <= 0:
                break

            types.append(i-1)
            total_slices += slices[i]

            j -= slices[i]
            i -= 1

        return types


    #
    # Lazy/greedy approximation used with big inputs
    #
    def approximation(self):

        types = []
        m_max = self.M
        s_sum = 0
        for i in tqdm(range(self.N)):
            if self.S[i] <= m_max:
                types.append(i)
                s_sum += self.S[i]
                m_max -= self.S[i]

        # print(s_sum)

        return types


    #
    # memoization cache helper method for the recursion approch
    #
    def c_push(self, i, j, r):

        if not i in self.cache:
            self.cache[i] = dict()
            self.cache[i][j] = r
        if not j in self.cache[i]:
            self.cache[i][j] = r


    #
    # memoized recursion approch
    #
    def knapsack00_MR(self, m, n):

        if m <= 0 or n == 0:
            return {'idx': [], 's': 0}

        self.c_push(m, n-1, self.knapsack00_MR(m, n-1))

        if not m in self.cache or not n in self.cache[m]:
            if self.S[n-1] > m:
                self.c_push(m, n, self.knapsack00_MR(m, n-1))
            else:
                self.c_push(m-self.S[n-1], n-1, self.knapsack00_MR(m-self.S[n-1], n-1))
                ra = self.cache[m-self.S[n-1]][n-1]
                a = {'s': ra['s'] + self.S[n-1], 'idx': ra['idx'] + [n-1]}
                b = self.cache[m][n-1]
                if a['s'] > b['s']:
                    return a
                else:
                    return b

        return self.cache[m][n]


    #
    # non-memoized recursion approch (normal recursion)
    #
    def knapsack00_NMR(self, m, n):

        if m <= 0 or n == 0:
            return {'idx': [], 's': 0}

        if self.S[n-1] > m:
            return self.knapsack00_NMR(m, n-1)
        else:
            ra = self.knapsack00_NMR(m-self.S[n-1], n-1)
            a = {'s': ra['s'] + self.S[n-1], 'idx': ra['idx'] + [n-1]}
            b = self.knapsack00_NMR(m, n-1)
            if a['s'] > b['s']:
                return a
            else:
                return b


    #
    # entrypoint method
    #
    def _work(self):

        if self.M * self.N * 8 > MaxMemory:
            types = self.approximation()
        else:
            if USE_BOTTOM_UP:
                types = self.knapsack00_BU()
            else:
                self.cache = {}
                types = self.knapsack00_NMR(self.M, self.N)
                types = types['idx']

        self.selected_types = types


    #
    # testing purposes method
    #
    def test(self, idx):

        self.idx = idx
        self._prepare_input(inputs[idx] + '.in')
        self._work()
        self._generate_output(inputs[idx] + '.test')
        score = self._score(inputs[idx] + '.test')
        print('test %s score is : %d' % (chr(97+idx), score))


    #
    # solve the problem (automation)
    #
    def solve(self):

        for idx in range(len(inputs)):
            self.idx = idx
            self._prepare_input(inputs[idx] + '.in')
            self._work()
            self._generate_output(inputs[idx] + '.out')
        self.scores()


    #
    # calculate the score of selected output file
    #
    def _score(self, out_filename):

        score = 0

        N, types = None, []
        with open('output/' + out_filename, 'r') as out_file:
            N = int(out_file.readline())
            types = list(map(int, out_file.readline().rstrip().split()))
            for i in range(N):
                idx = types[i]
                score += self.S[idx]

        return score


    #
    # calculate the overall scores
    #
    def scores(self):

        scores = []

        with open('output/scores', 'w') as scores_file:
            for idx in range(len(inputs)):
                self._prepare_input(inputs[idx] + '.in')
                score = self._score(inputs[idx] + '.out')
                print('test %s score is : %d' % (chr(97+idx), score))
                scores.append(score)
            scores_file.write('\n'.join(chr(97 + idx) + ' : ' + str(scores[idx]) for idx in range(len(scores))))
            scores_file.write('\n\n')
            scores_file.write('s: %d' % sum(scores))
            print('s: %d' % sum(scores))

#
# berrrrrrraaaraa
#
def main():

    p = Problem()
    # p.test(2)
    p.solve()

if __name__ == '__main__':

    main()

