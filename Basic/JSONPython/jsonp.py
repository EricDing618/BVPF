import json5
import os.path as op
import os

class JSONFileParser:
    def __init__(self,fp:str,mode=0):
        '''
        mode=0:code=keys();
            =1:code=values()
        '''
        self.fp=fp
        with open(self.fp,'r',encoding='utf-8') as f:
            self.code:dict=json5.load(f)
        self.code,self.comment=self.code.keys(),self.code.values()
        #print(self.code,self.comment) #调试
        if mode!=0:
            self.code,self.comment=self.comment,self.code

    def getcode(self):
        if not self.code:
            return (),()
        else:
            return tuple(self.code),tuple(self.comment)
    
    def run(self):
        temp=f'./Basic/JSONPython/temp/{op.splitext(op.basename(self.fp))[0]}_.py'
        with open(temp,'w',encoding='utf-8') as f:
            f.write('\n'.join(self.code))
        os.system(f'python {temp}')
        os.remove(temp)

class PythonFileParser:
    def __init__(self,fp:str):
        self.fp=fp
        with open(self.fp,'r',encoding='utf-8') as f:
            self.code=f.readlines()
        self.c1,self.c2=[],[]
        for i in self.code:
            c3=i.split('#')
            if len(c3)>1:
                for j in range(len(c3)):
                    if c3[j][-1]!='\\' and j != 0:
                        self.c2.append(''.join(c3[1:]))
            else:
                self.c2.append('')
            self.c1.append(c3[0])
    def getcode(self):
        return self.c1,self.c2
    
    def run(self):
        #print(''.join(self.code)) #调试
        os.system(f'python {self.fp}')
        '''for i in self.code:
            exec(i)'''

class FileGenerator:
    def __init__(self,parser:JSONFileParser|PythonFileParser,outdir:str,mode=0):
        '''
        mode= 0: from .json to .py;
            = 1: from .py to .json;
        '''
        if mode==0:
            c1=[]
            for code,comment in zip(*parser.getcode()):
                if not (comment=='' or comment.isspace()):
                    c1.append(code+' # '+comment)
                else:
                    c1.append(code)
            with open(op.join(outdir,op.splitext(op.basename(parser.fp))[0]+'.py'),'w',encoding='utf-8') as f:
                f.writelines(c1)
        else:
            c1=dict()
            for code,comment in zip(*parser.getcode()):
                if not (comment=='' or comment.isspace()):
                    c1[code]=comment.replace(' ','',0)
                else:
                    c1[code]=''
            with open(op.join(outdir,op.splitext(op.basename(parser.fp))[0]+'.json'),mode='w',encoding='utf-8') as f:
                json5.dump(c1,f,indent=4,ensure_ascii=False,separators=(',',': '))

def demo():
    run=True
    while run:
        fp=input('输入你的文件绝对路径（退出输入“/quit”）> ')
        if fp=='/quit':
            run=False
            input('按回车退出...')
        else:
            mode=int(input('你想要运行（0）还是转换（1）文件？'))
            if mode not in (0,1):
                print('输入错误！')
            elif mode==0:
                if op.splitext(op.basename(fp))[-1] in ('.py','.pyw'):
                    PythonFileParser(fp).run()
                else:
                    wm=int(input('该文件的格式为{代码:注释}（0）还是{注释:代码}（1）？'))
                    JSONFileParser(fp,wm).run()
                input('已运行完毕，按回车继续...')
            else:
                outdir=input('请输入导出目录的绝对路径> ')
                if op.splitext(op.basename(fp))[-1] in ('.py','.pyw'):
                    FileGenerator(PythonFileParser(fp),outdir,1)
                else:
                    wm=int(input('该文件的格式为{代码:注释}（0）还是{注释:代码}（1）？'))
                    FileGenerator(JSONFileParser(fp,wm),outdir,0)
                print('导出成功！')

if __name__=='__main__':
    demo()