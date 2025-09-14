import random, traceback
from re import findall
import itertools
#from fractions import Fraction
from operator import add, sub, mul, truediv
from sympy import S
from rich import print as rprint

class TwentyFourGenerator:
    """高效的24点数字生成器"""
    
    def __init__(self):
        self.operators = [add, sub, mul, truediv]
        self.operator_symbols = ['+', '-', '*', '/']
        # 预计算一些常见的有解组合，提高效率
        self.common_solutions = {
            (3, 3, 8, 8): '8/(3-8/3)',
            (1, 5, 5, 5): '(5-1/5)*5',
            (4, 4, 4, 7): '(7-4/4)*4',
            (1, 3, 4, 6): '6/(1-3/4)',
            (2, 5, 7, 8): '(2*5-7)*8',
            (3, 3, 7, 7): '(3+3/7)*7',
            (1, 4, 5, 6): '6/(5/4-1)',
            (2, 3, 5, 12): '12/(3-5/2)'
        }
    
    def generate_numbers(self):
        """生成4个可以组成24点的数字"""
        # 80%的概率从常见解中选取，20%的概率随机生成
        if random.random() < 0.8 and self.common_solutions:
            numbers = random.choice(list(self.common_solutions.keys()))
            return list(numbers), self.common_solutions[numbers]
        
        # 随机生成并验证
        for _ in range(100):  # 最多尝试100次
            numbers = [random.randint(1, 13) for _ in range(4)]
            solution = self.solve_24(numbers)
            if solution:
                return numbers, solution
        
        # 如果随机生成失败，返回一个已知解
        numbers = random.choice(list(self.common_solutions.keys()))
        return list(numbers), self.common_solutions[numbers]
    
    def solve_24(self, numbers):
        """解决24点问题，返回解决方案"""
        # 检查是否在已知解中
        num_tuple = tuple(sorted(numbers))
        if num_tuple in self.common_solutions:
            return self.common_solutions[num_tuple]
        
        # 尝试所有可能的数字排列
        for num_perm in itertools.permutations(numbers):
            # 尝试所有可能的运算符组合
            for op1, op2, op3 in itertools.product(self.operators, repeat=3):
                # 尝试不同的运算顺序（括号位置）
                # 形式: ((a op1 b) op2 c) op3 d
                try:
                    result = op3(op2(op1(num_perm[0], num_perm[1]), num_perm[2]), num_perm[3])
                    if result == 24:
                        return self.format_solution(num_perm, [op1, op2, op3], "((a op1 b) op2 c) op3 d")
                except ZeroDivisionError:
                    pass
                
                # 形式: (a op1 (b op2 c)) op3 d
                try:
                    result = op3(op1(num_perm[0], op2(num_perm[1], num_perm[2])), num_perm[3])
                    if result == 24:
                        return self.format_solution(num_perm, [op1, op2, op3], "(a op1 (b op2 c)) op3 d")
                except ZeroDivisionError:
                    pass
                
                # 形式: a op1 ((b op2 c) op3 d)
                try:
                    result = op1(num_perm[0], op3(op2(num_perm[1], num_perm[2]), num_perm[3]))
                    if result == 24:
                        return self.format_solution(num_perm, [op1, op2, op3], "a op1 ((b op2 c) op3 d)")
                except ZeroDivisionError:
                    pass
                
                # 形式: a op1 (b op2 (c op3 d))
                try:
                    result = op1(num_perm[0], op2(num_perm[1], op3(num_perm[2], num_perm[3])))
                    if result == 24:
                        return self.format_solution(num_perm, [op1, op2, op3], "a op1 (b op2 (c op3 d))")
                except ZeroDivisionError:
                    pass
                
                # 形式: (a op1 b) op2 (c op3 d)
                try:
                    result = op2(op1(num_perm[0], num_perm[1]), op3(num_perm[2], num_perm[3]))
                    if result == 24:
                        return self.format_solution(num_perm, [op1, op2, op3], "(a op1 b) op2 (c op3 d)")
                except ZeroDivisionError:
                    pass
        
        return None
    
    def format_solution(self, numbers, operators, pattern):
        """将解决方案格式化为可读字符串"""
        a, b, c, d = numbers
        op1, op2, op3 = operators
        op1_sym = self.operator_symbols[self.operators.index(op1)]
        op2_sym = self.operator_symbols[self.operators.index(op2)]
        op3_sym = self.operator_symbols[self.operators.index(op3)]
        
        if pattern == "((a op1 b) op2 c) op3 d":
            return f"(({a} {op1_sym} {b}) {op2_sym} {c}) {op3_sym} {d}"
        elif pattern == "(a op1 (b op2 c)) op3 d":
            return f"({a} {op1_sym} ({b} {op2_sym} {c})) {op3_sym} {d}"
        elif pattern == "a op1 ((b op2 c) op3 d)":
            return f"{a} {op1_sym} (({b} {op2_sym} {c}) {op3_sym} {d})"
        elif pattern == "a op1 (b op2 (c op3 d))":
            return f"{a} {op1_sym} ({b} {op2_sym} ({c} {op3_sym} {d}))"
        elif pattern == "(a op1 b) op2 (c op3 d)":
            return f"({a} {op1_sym} {b}) {op2_sym} ({c} {op3_sym} {d})"
        
        return None
    
    def validate_answer(self, user_answer:str, numbers:list[int], correct_solution:str):
        """
        答案验证接口
        参数:
            user_answer: 用户输入的答案字符串
            numbers: 当前题目的四个数字列表
            correct_solution: 标准答案字符串
        
        返回值:
            bool: 用户答案是否正确
        
        您需要实现这个函数来验证用户的答案
        这里只是一个示例实现，您需要根据实际需求完善它
        """
        replace = {
            ' ':'',
            '\n':'',
            '（':'(',
            '）':')',
            '÷':'/'
        }
        for old,new in replace.items():
            user_answer = user_answer.replace(old,new)
        try:
            all_numbers = [int(n) for n in findall(r'\d+', user_answer)]
            print('[DEBUG] user:',all_numbers)
            validate_str = list(str(i) for i in range(1,14))+['+','-','*','/','(',')']
            print('[DEBUG] validate_str:',validate_str)
            if any(i not in validate_str for i in user_answer) or not (strip_ans:=user_answer.strip()):
                print('[DEBUG] invalid char')
                #print(f'[DEBUG] user input: {strip_ans}')
                return False
            solve_user_answer = S(user_answer)
            print('[DEBUG] eval:',solve_user_answer)
            print('[DEBUG] corr:',numbers)
            print('[DEBUG] corr eval(not sympy):',eval(correct_solution))
            if sorted(all_numbers)==sorted(numbers) and solve_user_answer == 24:
                return True
        except:
            traceback.print_exc()
            return False
        return False
    
if __name__=="__main__":
    running = True
    print("Welcome to Solve24 CLI! (Author: EricDing618, Version: v0.1.0)")
    print('Tip: Press "exit" to exit.')
    generator = TwentyFourGenerator()
    while running:
        numbers, solution = generator.generate_numbers()
        rprint('[blue]Four numbers:[/]', numbers)
        user=input('Input: ')
        if user.lower()=='exit':
            running = False
            rprint('[blue]Bye![/]')
            break
        if generator.validate_answer(user, numbers, solution):
            rprint('[green]Correct![/]\nOfficial solution is:', solution+'\n=====')
        else:
            rprint('[red]Wrong![/] The correct answer is:', solution+'\n=====')