from sympy import Matrix, shape, zeros
from src.sle.utils import SLESols


class LinEqSystem:
    """

    """

    def __init__(self, augmented_matrix: Matrix, varnames: list[str] | None = None):
        """
        Ax = b, accepts 1 agrument (A|b), this is augmented matrix (дополненная матрица).
        :param augmented_matrix:
        :return:
        """
        self.coeffs: Matrix = augmented_matrix[:, :-1]
        self.right_side: Matrix = augmented_matrix.col(-1)
        self.eq_num, self.var_num = shape(self.coeffs)
        assert shape(self.right_side)[0] == self.eq_num, 'Размер b должен совпадать с количеством уравнений.'
        self.matrix = augmented_matrix
        self.varnames = varnames or [f'x_{i}' for i in range(1, self.var_num + 1)]
        assert len(self.varnames) == self.var_num, 'Num of variables must match len of varnames'
        _, self.pivot = self.matrix.rref()

    @classmethod
    def make(cls, A: Matrix, b: Matrix):
        return cls(A.row_join(b))

    def __repr__(self):
        return '\n'.join(self.stringify())

    def tex_condition(self):
        return LinEqSystem.texify(self.stringify())

    def tex_solution(self):
        return LinEqSystem.texify(self.solve(verbose=False)['answers'])

    @staticmethod
    def texify(data: list[str]) -> str:
        tex_equations = r"\begin{equation}\left\{\begin{aligned}" + "\n"
        for eq in data:
            tex_eq = eq.replace('=', '&=')
            tex_eq += r' \\'
            tex_equations += tex_eq + "\n"
        tex_equations += r"\end{aligned}\right.\end{equation}"
        return tex_equations

    def stringify(self) -> list[str]:
        """
        matrix должна быть расширенной, A | b.
        :return:
        """
        equations = []
        for i in range(self.matrix.rows):
            equation = ''
            for j in range(len(self.varnames)):
                coeff = self.matrix.row(i)[j]
                if coeff == 0:
                    continue
                sign = '+' if coeff > 0 else '-'
                equation += f'{sign if j != 0 and len(equation) > 1 or coeff < 0 else ""}{" " if len(equation) > 1 else ""}{abs(coeff) if abs(coeff) != 1 else ""}{self.varnames[j]} '
            equation += f'= {self.matrix[i, -1]}'

            equations.append(equation.strip())

        return equations

    def main_vars(self) -> list[str]:
        return [v[i] for i, v in enumerate(self.varnames) if i in self.pivot]

    def free_vars(self) -> list[str]:
        return [self.varnames[i] for i in range(len(self.varnames)) if i not in self.pivot]

    def nullspace(self):
        return self.coeffs.nullspace()

    def columnspace(self):
        return self.coeffs.columnspace()

    def classify(self) -> SLESols:
        """
        The system has infinitely many solutions. Неопределённая система
        The system has a unique solution. Невырожденная система
        The system has no solution. Несовместная система
        :return:
        """
        solveable = self.matrix.rank() == self.coeffs.rank()  # Теорема Кронекера — Капелли
        if not solveable:
            return SLESols.NOSOL
        return SLESols.UNIQSOL if self.coeffs.rank() == self.var_num else SLESols.INFSOL

    def _particular_solution(self):
        # Приводим матрицу к главному ступенчатому виду, pivot содержат номера тех столбцов, которые содержат базисные переменные.
        X, pivot = self.matrix.rref()

        # Находим частное решение системы
        solution = zeros(self.var_num, 1)
        for h, elem in enumerate(X.col(-1)):
            if h < len(pivot):
                i = pivot[h]
            else:
                break

            solution[i] = elem

        return solution

    def solve(self, determined=False, verbose=True) -> dict[str, list[str] | list[int | None]]:
        space: list[Matrix] = self.nullspace()

        # Добавляем в ядро однородной системы.
        space.append(self._particular_solution())

        vrs: list[int | None] = [0] * self.var_num
        answers = []
        for i in range(self.var_num):
            answer = f'{self.varnames[i]} = '
            for j, mtr in enumerate(space):
                sign = '+' if mtr[i] > 0 else '-'
                begin = (sign if (len(answer.split("=")[-1]) > 1 or mtr[i] < 0) else "") + (" " if len(answer.split("=")[-1]) > 1 else "")
                if j < len(space) - 1:
                    if mtr[i] == 0:
                        continue
                    answer += f'{begin}{abs(mtr[i]) if abs(mtr[i]) != 1 else ""}C_{j + 1} '
                else:
                    answer += f'{begin}{abs(mtr[i])}.' if mtr[i] != 0 else ''

                if mtr[i] != 0 and determined and j < len(space) - 1:
                    vrs[i] = None
                if j == len(space) - 1 and vrs[i] is not None:
                    vrs[i] = mtr[i]
            answers.append(answer)
        if verbose:
            print('\n'.join(answers))
        return {'vars': vrs, 'answers': answers}

    def tex_solution_vectorform(self):
        space: list[Matrix] = self.nullspace()
        space.append(self._particular_solution())

        variables_str = '\\begin{pmatrix}\n'
        variables_str += '\\\\\n'.join(self.varnames)
        variables_str += '\n\\end{pmatrix}'

        solution_str = ''
        for i in range(len(space)):
            solution_str += f'C_{i + 1} ' if i != len(space) - 1 else ''
            solution_str += '\n\\begin{pmatrix}\n'

            solution_str += '\\\\\n'.join([str(space[i][j]) for j in range(len(space[i]))])
            solution_str += '\\\\\n'
            solution_str += '\\end{pmatrix} ' + f'{"+" if i != len(space) - 1 else ""}'

        return f"{variables_str} = {solution_str}"
