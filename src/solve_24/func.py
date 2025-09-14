import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# 关闭LaTeX渲染，使用Matplotlib内置的数学表达式渲染
plt.rcParams['text.usetex'] = False
plt.rcParams['mathtext.fontset'] = 'cm'  # 使用Computer Modern字体
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 12

# 定义符号
x = sp.symbols('x', real=True, positive=True)
n = sp.symbols('n', integer=True)

# 创建未化简的求和表达式
# 下标n=1，上标120，右边是x^(10*((√5-1)/2))
sum_expr = sp.Sum(x**(10*(sp.sqrt(5)-1)/2), (n, 1, 120))

# 打印表达式
print("求和表达式:")
sp.pprint(sum_expr)
print("\n简化后的表达式:")
sp.pprint(sum_expr.doit())

# 为了绘制平滑曲线，我们需要计算每个x点的求和值
# 由于表达式未化简，我们需要手动计算求和
def compute_sum(x_val):
    """计算未化简的求和值"""
    exponent = 10 * (np.sqrt(5) - 1) / 2
    result = 0
    # 计算从n=1到n=120的求和
    for n_val in range(1, 121):
        result += x_val**exponent
    return result

# 生成x值范围：0 ≤ x ≤ 1
x_vals = np.linspace(0.001, 1, 500)  # 从0.001开始避免x=0时的计算问题
y_vals = [compute_sum(x_val) for x_val in x_vals]

# 创建图形
fig, ax = plt.subplots(figsize=(12, 7))

# 绘制平滑曲线
ax.plot(x_vals, y_vals, 'b-', linewidth=2)

# 设置标签和标题
ax.set_xlabel('$x$', fontsize=14)
ax.set_ylabel('$f(x)$', fontsize=14)

# 使用Matplotlib的数学表达式渲染，显示未化简的求和表达式
title_text = r'$f(x) = \sum_{n=1}^{120} x^{10 \cdot \frac{\sqrt{5}-1}{2}}$ for $0 \leq x \leq 1$'
ax.set_title(title_text, fontsize=16)

# 添加网格
ax.grid(True, linestyle='--', alpha=0.7)

# 设置坐标轴范围
ax.set_xlim(0, 1)
# 计算并显示一些关键点的值
print("\n关键点函数值:")
for x_val in [0.1, 0.3, 0.5, 0.7, 1.0]:
    y_val = compute_sum(x_val)
    print(f"f({x_val}) = {y_val:.6f}")
    
# 计算指数值
exponent_value = 10 * (np.sqrt(5) - 1) / 2
print(f"\n指数值: {exponent_value}")
print(f"简化后的指数表达式: -5 + 5√5 ≈ {exponent_value}")
# 显示图形
plt.tight_layout()
#plt.savefig('sum_function_plot.png', dpi=300, bbox_inches='tight')
plt.show()
