import random
import itertools
from fractions import Fraction

def generate_24_numbers():
    """
    生成4个整数，这些数字可以通过加减乘除组合得到24
    """
    while True:
        # 生成4个1-13之间的随机整数（类似扑克牌点数）
        numbers = [random.randint(1, 13) for _ in range(4)]
        
        # 检查这些数字是否能通过运算得到24
        solution = solve_24(numbers)
        if solution:
            return numbers, solution

def solve_24(numbers):
    """
    尝试找到使用加减乘除得到24的解法
    返回解法字符串，如果无解则返回None
    """
    # 尝试所有可能的数字排列
    for num_permutation in itertools.permutations(numbers):
        a, b, c, d = num_permutation
        
        # 尝试所有可能的运算符组合（加减乘除）
        ops = ['+', '-', '*', '/']
        for op1, op2, op3 in itertools.product(ops, repeat=3):
            # 尝试不同的运算顺序（括号位置）
            expressions = [
                # 形式: ((a op1 b) op2 c) op3 d
                f"(({a} {op1} {b}) {op2} {c}) {op3} {d}",
                # 形式: (a op1 (b op2 c)) op3 d
                f"({a} {op1} ({b} {op2} {c})) {op3} {d}",
                # 形式: a op1 ((b op2 c) op3 d)
                f"{a} {op1} (({b} {op2} {c}) {op3} {d})",
                # 形式: a op1 (b op2 (c op3 d))
                f"{a} {op1} ({b} {op2} ({c} {op3} {d}))",
                # 形式: (a op1 b) op2 (c op3 d)
                f"({a} {op1} {b}) {op2} ({c} {op3} {d})"
            ]
            
            for expr in expressions:
                try:
                    # 使用Fraction避免浮点精度问题
                    result = eval(expr, {'__builtins__': None}, 
                                 {op: getattr(Fraction, f'__{op}__') for op in ['add', 'sub', 'mul', 'truediv']})
                    if result == 24:
                        return expr
                except ZeroDivisionError:
                    continue
    return None

# 示例使用
if __name__ == "__main__":
    numbers, solution = generate_24_numbers()
    print(f"生成的数字: {numbers}")
    print(f"参考解法: {solution} = 24")
    
    # 额外生成几个例子
    print("\n更多例子:")
    for _ in range(3):
        numbers, solution = generate_24_numbers()
        print(f"数字: {numbers} -> 解法: {solution}")