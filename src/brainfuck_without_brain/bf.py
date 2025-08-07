# DeepSeek大手之力(85%)
import sys

class Interpreter:
    def __init__(self, code:str, replace_dict:dict=None, dialect:bool=True):
        '''replace_dict格式：{方言:原指令,...}'''
        self.dialect = dialect
        self.dick = { #故意的（
            '卧': '>',
            '草': '<',
            '泥': '+',
            '马': '-',
            '德': '.',
            '勒': ',',
            '格': '.',
            '鼻': '[',
            '德': ']'
        } if not replace_dict else replace_dict
        self.code = code if not dialect else self.replaceToBF(code)
    def replaceToBF(self, code:str):
        cache = []
        for c in code:
            if c.strip():
                cache.append(self.dick.get(c,'?'))
        return ''.join(cache)
    def replaceToDialect(self, code:str):
        cache = []
        for c in code:
            if c.strip():
                cache.append(next((k for k, v in self.dick.items() if v == c), None))
        return ''.join(cache)
    def optimized_brainfuck(self, input_str=""):
        data = bytearray(30000)
        ptr = 0
        pc = 0
        input_iter = iter(input_str)
        output = []
        
        # 预处理：去除注释、构建跳转表
        clean_code = [c for c in self.code if c in '><+-.,[]']
        loop_stack = []
        loop_pairs = {}
        
        for i, cmd in enumerate(clean_code):
            if cmd == '[':
                loop_stack.append(i)
            elif cmd == ']':
                if loop_stack:
                    start = loop_stack.pop()
                    loop_pairs[start] = i
                    loop_pairs[i] = start
        
        # 合并连续相同操作
        optimized_ops = []
        i = 0
        n = len(clean_code)
        
        while i < n:
            cmd = clean_code[i]
            if cmd in '><+-':
                count = 1
                while i + count < n and clean_code[i + count] == cmd:
                    count += 1
                optimized_ops.append((cmd, count))
                i += count
            else:
                optimized_ops.append((cmd, 1))
                i += 1
        
        # 执行优化后的指令
        while pc < len(optimized_ops):
            cmd, arg = optimized_ops[pc]
            
            if cmd == '>':
                ptr += arg
                if ptr >= len(data):
                    data.extend(bytes(len(data)))  # 双倍扩展
            elif cmd == '<':
                ptr -= arg
                if ptr < 0:
                    ptr = 0
            elif cmd == '+':
                data[ptr] = (data[ptr] + arg) % 256
            elif cmd == '-':
                data[ptr] = (data[ptr] - arg) % 256
            elif cmd == '.':
                output.append(chr(data[ptr]))
                # 直接输出到stdout更高效
                # sys.stdout.write(chr(data[ptr]))
            elif cmd == ',':
                try:
                    data[ptr] = ord(next(input_iter))
                except StopIteration:
                    data[ptr] = 0
            elif cmd == '[':
                if data[ptr] == 0:
                    pc = loop_pairs[pc]
            elif cmd == ']':
                if data[ptr] != 0:
                    pc = loop_pairs[pc]
            
            pc += 1
        
        return ''.join(output)
    
if __name__ == "__main__":
    bf = Interpreter('泥泥泥泥泥泥泥泥鼻卧泥泥泥泥鼻卧泥泥卧泥泥泥卧泥泥泥卧泥草草草草马德卧泥卧泥卧马卧卧泥鼻草德草马德卧卧格卧马马马格泥泥泥泥泥泥泥格格泥泥泥格卧卧格草马格草格泥泥泥格马马马马马马格马马马马马马马马格卧卧泥格卧泥泥格')
    print(bf.replaceToDialect("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."))
    print(bf.optimized_brainfuck())