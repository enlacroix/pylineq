from sympy import Matrix

from src.sle.lineq import LinEqSystem

MATRICES = {
    '1': Matrix([[1, 2, 1, 1, 7],
                 [1, 2, 2, -1, 12],
                 [2, 4, 0, 6, 4]]),

    # Она вычислит первые три переменные, но она ничего не знает достоверно о четвёртом угле, поэтому ему присвоен None.
    '2': Matrix([[1, 1, 1, 0, 180],
                 [1, -3, 0, 0, 0],
                 [0, 0, 1, 0, 20]]),

    '3': Matrix([[-1, 1, 1, 0, 180],
                 [0, 0, 0, 1, 20]]),

}


def run_tests():
    for k, m in MATRICES.items():
        print(f'Система {k}:')
        les = LinEqSystem(m)
        print(les, '\n')
        sol1 = les.solve(verbose=False)['vars']
        sol2 = les.solve(determined=True)['vars']
        print(sol1, sol2)

def certain():
    A = Matrix([[1, 2, 1, 1],
                [1, 2, 2, -1],
                [2, 4, 0, 6]])
    b = Matrix([7, 12, 4])
    sle = LinEqSystem.make(A, b)
    print(sle)
    sle.solve()
    print(sle.tex_condition())
    print(sle.tex_solution())

    sle.classify()
    sle.nullspace()
    sle.columnspace()
    sle.free_vars()

    #print(les.tex_solution())


if __name__ == '__main__':
    # run_tests()
    certain()
