if __name__ == "__main__":
    from base import TwentyFourGenerator
else:
    from .base import TwentyFourGenerator

import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

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
        self.setPlaceholderText("请输入表达式，如 (6+2)*3。解法可含分数，按回车提交。")
        
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
        self.setWindowTitle("Solve24 - By EricDing618")
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
        print(f'[DEBUG] ====={self.current_numbers} -> {self.current_solution}=====')  # 调试输出
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
        is_correct = self.generator.validate_answer(user_answer, self.current_numbers, self.current_solution)
        
        # 根据验证结果更新界面
        if is_correct:
            self.title_label.setText("恭喜你，你答对啦！")
            self.title_label.setStyleSheet("color: #4CAF50;")
            self.answer_input.set_correct(True)
        else:
            self.title_label.setText(f"正解：{self.current_solution}")
            self.title_label.setStyleSheet("color: #F44336;")
            self.answer_input.set_correct(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Solve24Game()
    game.show()
    sys.exit(app.exec_())