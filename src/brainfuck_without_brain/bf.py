'''最文明的一集'''

class MyInterpreter:
    def __init__(self, code:str, replace_dict:dict=None, dialect:bool=True):
        '''replace_dict格式：{方言:原指令,...}'''
        self.change(code,replace_dict,dialect)
    def change(self, code:str, replace_dict:dict=None, dialect=True):
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
        if dialect:
            assert code==self.replaceToDialect(self.replaceToBF(code))
        else:
            assert code==self.replaceToBF(self.replaceToDialect(code))
        self.code = code if not dialect else self.replaceToBF(code)
    def replaceToBF(self, code:str):
        cache = []
        for c in code:
            if c.strip():
                cache.append(self.dick.get(c,c))
        return ''.join(cache)
    def replaceToDialect(self, code:str):
        cache = []
        for c in code:
            if c.strip():
                cache.append(next((k for k, v in self.dick.items() if v == c), c))
        return ''.join(cache)

    def optimized_brainfuck(self):
        '''大部分参考Copilot+https://st1020.com/a-brainfuck-language-interpreter-implemented-in-python/'''
        bf_code = self.code
        main_list = [0] * 30000  # 预分配30000个cell
        now_id = 0
        now_position = 0
        self.output = []
        while now_position < len(bf_code):
            command = bf_code[now_position]
            if command == '<':
                if now_id == 0:
                    print(1, '内存错误，指针位于 -1')
                    return
                else:
                    now_id -= 1
            elif command == '>':
                now_id += 1
                if now_id >= len(main_list):
                    main_list.append(0)
            elif command == '+':
                main_list[now_id] = (main_list[now_id] + 1) % 256
            elif command == '-':
                main_list[now_id] = (main_list[now_id] - 1) % 256
            elif command == '.':
                print(chr(main_list[now_id]), end='')
                self.output.append(chr(main_list[now_id]))
            elif command == ',':
                while True:
                    input_chr = input('请输入：')
                    if len(input_chr) == 1:
                        if ord(input_chr) < 128:
                            main_list[now_id] = ord(input_chr)
                            break
                        else:
                            print(2, '输入错误，只能输入 ASCII 字符')
                    else:
                        print(2, '输入错误，只能输入一个字符')
            elif command == '[':
                if main_list[now_id] == 0:
                    open_brackets = 1
                    search_pos = now_position + 1
                    while search_pos < len(bf_code):
                        if bf_code[search_pos] == '[':
                            open_brackets += 1
                        elif bf_code[search_pos] == ']':
                            open_brackets -= 1
                            if open_brackets == 0:
                                break
                        search_pos += 1
                    if open_brackets != 0:
                        print(3, '代码错误，缺失：]')
                        return
                    now_position = search_pos
            elif command == ']':
                if main_list[now_id] != 0:
                    close_brackets = 1
                    search_pos = now_position - 1
                    while search_pos >= 0:
                        if bf_code[search_pos] == ']':
                            close_brackets += 1
                        elif bf_code[search_pos] == '[':
                            close_brackets -= 1
                            if close_brackets == 0:
                                break
                        search_pos -= 1
                    if close_brackets != 0:
                        print(3, '代码错误，缺失 [')
                        return
                    now_position = search_pos
            else:
                print(0, '无法解析的字符：' + command)
            now_position += 1
        # print(main_list)  # 不再输出内存
    
if __name__ == "__main__":
    bf = MyInterpreter('++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.',dialect=False)
    print(bf.replaceToDialect("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."))
    print(bf.replaceToBF("泥泥泥泥泥泥泥泥鼻卧泥泥泥泥鼻卧泥泥卧泥泥泥卧泥泥泥卧泥草草草草马德卧泥卧泥卧马卧卧泥鼻草德草马德卧卧格卧马马马格泥泥泥泥泥泥泥格格泥泥泥格卧卧格草马格草格泥泥泥格马马马马马马格马马马马马马马马格卧卧泥格卧泥泥格"))
    bf.optimized_brainfuck()
    bf.change('++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.', dialect=False)
    bf.optimized_brainfuck()
    bf.change('泥泥泥泥泥泥泥泥鼻卧泥泥泥泥鼻卧泥泥卧泥泥泥卧泥泥泥卧泥草草草草马德卧泥卧泥卧马卧卧泥鼻草德草马德卧卧格卧马马马格泥泥泥泥泥泥泥格格泥泥泥格卧卧格草马格草格泥泥泥格马马马马马马格马马马马马马马马格卧卧泥格卧泥泥格')
    bf.optimized_brainfuck()