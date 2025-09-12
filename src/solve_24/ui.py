if __name__ == "__main__":
    from base import TwentyFourGenerator
else:
    from .base import TwentyFourGenerator
import sys, traceback

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from sympy import S
from re import findall


class NumberLabel(QLabel):
    """自定义数字标签，带有圆角和颜色"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont("Microsoft YaHei", 24, QFont.Bold))
        
        # 设置样式
        self.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            border-radius: 15px;
            padding: 10px;
        """)
        self.setMinimumSize(60, 60)


class AnswerLineEdit(QLineEdit):
    """自定义答案输入框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Microsoft YaHei", 12))
        self.setPlaceholderText("请输入表达式，如 (6+2)*3")
        
        # 设置默认样式
        self.normal_style = """
            QLineEdit {
                border: 2px solid #2196F3;
                border-radius: 8px;
                padding: 8px;
                background-color: white;
            }
        """
        self.correct_style = """
            QLineEdit {
                border: 2px solid #4CAF50;
                border-radius: 8px;
                padding: 8px;
                background-color: white;
            }
        """
        self.wrong_style = """
            QLineEdit {
                border: 2px solid #F44336;
                border-radius: 8px;
                padding: 8px;
                background-color: white;
            }
        """
        
        self.setStyleSheet(self.normal_style)
    
    def set_correct(self, is_correct):
        """根据答案正确与否设置样式"""
        if is_correct:
            self.setStyleSheet(self.correct_style)
        else:
            self.setStyleSheet(self.wrong_style)


class Solve24Game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.generator = TwentyFourGenerator()
        self.current_numbers = []
        self.current_solution = ""
        self.init_ui()
        self.new_problem()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("Solve24 - By EricDing618 and DeepSeek")
        self.setMinimumSize(500, 400)
        
        # 设置中心部件和主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 20, 30, 30)
        
        # 标题标签
        self.title_label = QLabel("请作答")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        self.title_label.setStyleSheet("color: #2196F3;")
        main_layout.addWidget(self.title_label)
        
        # 数字显示区域
        numbers_layout = QHBoxLayout()
        numbers_layout.setSpacing(15)
        
        self.number_labels = []
        for i in range(4):
            label = NumberLabel("")
            self.number_labels.append(label)
            numbers_layout.addWidget(label)
        
        main_layout.addLayout(numbers_layout)
        
        # 随机按钮
        self.random_button = QPushButton("随机一题")
        self.random_button.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        self.random_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 15px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        self.random_button.clicked.connect(self.new_problem)
        main_layout.addWidget(self.random_button)
        
        # 答案输入区域
        answer_frame = QFrame()
        answer_frame.setStyleSheet("background-color: transparent;")
        answer_layout = QVBoxLayout(answer_frame)
        answer_layout.setContentsMargins(0, 0, 0, 0)
        
        # 答案标签
        answer_title = QLabel("你的答案：")
        answer_title.setFont(QFont("Microsoft YaHei", 10))
        answer_title.setStyleSheet("color: #555; margin-left: 5px;")
        answer_layout.addWidget(answer_title)
        
        # 答案输入框
        self.answer_input = AnswerLineEdit()
        self.answer_input.returnPressed.connect(self.check_answer)
        answer_layout.addWidget(self.answer_input)
        
        main_layout.addWidget(answer_frame)
        
        # 设置窗口背景色
        self.setStyleSheet("background-color: white;")
    
    def new_problem(self):
        """生成新题目"""
        self.current_numbers, self.current_solution = self.generator.generate_numbers()
        print(f'=====debug: {self.current_numbers} -> {self.current_solution}')  # 调试输出
        # 更新数字标签
        for i, label in enumerate(self.number_labels):
            label.setText(str(self.current_numbers[i]))
        
        # 重置界面状态
        self.title_label.setText("请作答")
        self.title_label.setStyleSheet("color: #2196F3;")
        self.answer_input.setStyleSheet(self.answer_input.normal_style)
        self.answer_input.clear()
        self.answer_input.setFocus()
    
    def check_answer(self):
        """检查答案是否正确"""
        user_answer = self.answer_input.text().strip()
        
        # 这里是答案验证接口
        # 您需要实现 validate_answer 函数
        is_correct = self.validate_answer(user_answer, self.current_numbers, self.current_solution)
        
        # 根据验证结果更新界面
        if is_correct:
            self.title_label.setText("恭喜你，你答对啦！")
            self.title_label.setStyleSheet("color: #4CAF50;")
            self.answer_input.set_correct(True)
        else:
            self.title_label.setText(f"正解：{self.current_solution}")
            self.title_label.setStyleSheet("color: #F44336;")
            self.answer_input.set_correct(False)
    
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
        # 示例实现：简单比较用户输入和标准答案
        # 实际实现应该更复杂，需要验证用户使用了给定的数字
        # 并且表达式的结果确实等于24
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
            print('user:',all_numbers)
            solve_user_answer = S(user_answer)
            print('eval:',solve_user_answer)
            print('corr:',numbers)
            print('corr eval(not sympy):',eval(correct_solution))
            if set(all_numbers)==set(numbers) and solve_user_answer == 24:
                return True
        except:
            traceback.print_exc()
            return False
        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Solve24Game()
    game.show()
    sys.exit(app.exec_())