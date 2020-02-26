#!/usr/bin/env python3

from tqdm import trange, tqdm


inputs = ['a_example', 'b_read_on', 'c_incunabula', 'd_tough_choices', 'e_so_many_books', 'f_libraries_of_the_world']


class Problem:

    def __init__(self):

        pass


    def _prepare_input(self, in_filename):

        with open('input/' + in_filename, 'r') as in_file:
            self.B, self.L, self.D = map(int, in_file.readline().split())
            self.S = list(map(int, in_file.readline().rstrip().split()))
            self.LIBS = []
            for j in range(self.L):
                lib = dict()
                lib['n'], lib['t'], lib['m'] = list(map(int, in_file.readline().rstrip().split()))
                lib['b'] = list(map(int, in_file.readline().rstrip().split()))
                self.LIBS.append(lib)


    def _generate_output(self, out_filename):

        with open('output/' + out_filename, 'w') as out_file:
            out_file.write(str(len(self.selected_libs)) + '\n')
            for lib in self.selected_libs:
                out_file.write(str(lib['i']) + ' ' + str(len(lib['b'])) + '\n')
                out_file.write(' '.join(map(str, lib['b'])) + '\n')


    def _lib_best_scored_books(self, idx, days):

        scores = { b: self.S[b] for b in self.LIBS_DICT[idx]['b'] }
        m = self.LIBS_DICT[idx]['m']

        score = 0
        books = []

        nb_books_can_scan = days * m
        for b in sorted(scores, key=scores.get, reverse=True):
            if b not in self.excluded_books and nb_books_can_scan > 0:
                books.append(b)
                nb_books_can_scan -= 1
                score += scores[b]

        return (score, books)


    def _best_scored_lib(self, days):

        best_lib_idx = -1
        best_lib_score = -1
        best_lib_books = None

        for i in tqdm(self.LIBS_DICT):
            days_left_after_signup = days - self.LIBS_DICT[i]['t']
            if days_left_after_signup > 0:
                score, books = self._lib_best_scored_books(i, days_left_after_signup)
                if score > best_lib_score:
                    best_lib_score, best_lib_idx, best_lib_books = score, i, books

        return (best_lib_idx, best_lib_books)


    def _work(self):

        days_left = self.D
        self.selected_libs = []
        self.excluded_books = set()

        self.LIBS_DICT = { i: self.LIBS[i] for i in range(len(self.LIBS)) }

        while True:
            l_idx, books = self._best_scored_lib(days_left)
            if l_idx == -1 or days_left <= 0:
                break
            days_left -= self.LIBS_DICT[l_idx]['t']
            lib = {'i': l_idx, 'b': books}
            self.selected_libs.append(lib)
            self.excluded_books.update(books)
            del self.LIBS_DICT[l_idx]


    def test(self, idx):

        self._prepare_input(inputs[idx] + '.txt')
        self._work()
        self._generate_output(inputs[idx] + '.test')
        self.score(inputs[idx] + '.test')


    def solve(self):

        for idx in range(len(inputs)):
            self._prepare_input(inputs[idx] + '.txt')
            self._work()
            self._generate_output(inputs[idx] + '.out')
            self.score(inputs[idx] + '.out')

    def score(self, out_filename):

        # TODO: verify books for days inconsistencies

        score = 0

        l, libs = None, []
        with open('output/' + out_filename, 'r') as out_file:
            l = int(out_file.readline())
            for i in range(l):
                lib = dict()
                lib['i'], lib['b'] = map(int, out_file.readline().rstrip().split())
                lib['books'] = list(map(int, out_file.readline().rstrip().split()))
                libs.append(lib)
        for i in range(l):
            for j in range(libs[i]['b']):
                book_idx = libs[i]['books'][j]
                score += self.S[book_idx]
        print(score)


def main():

    p = Problem()
    p.test(5)
    #p.solve()


if __name__ == '__main__':

    main()


