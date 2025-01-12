from colorama import Fore,Back,init
from os import system
from random import randint
import re
import time

print('Importing wordlist...')
from wordlist import *

init(autoreset=True)
class WordKey: #单词密钥加解密
    def __init__(self,text:str,key:int=3):
        self.chance=re.findall(r'\d+',text)[-1]
        self.s=text.replace(self.chance,'')
        self.key = key
        self.alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.encrypt_map = {char: self.alphabet[(i + self.key) % len(self.alphabet)] for i, char in enumerate(self.alphabet)}
        self.decrypt_map = {char: self.alphabet[(i - self.key) % len(self.alphabet)] for i, char in enumerate(self.alphabet)}
    def encode(self):
        return ''.join(self.encrypt_map.get(char, char) for char in self.s)+self.chance+str(self.key)
    def decode(self):
        return [''.join(self.decrypt_map.get(char, char) for char in self.s),int(self.chance[:-1]),self.key]
    
class WordPy:
    def __init__(self,run=True):
        self.wordlist=wordlist
        if run:
            self.homepage()
    def initguess(self,result:str,chance:int,wordlist:list|tuple=None): #初始化
        self.letterstack=[]
        self.log=[]
        self.word=result if isinstance(result,str) else result[0] #史山一行暴力清除bug，后续有时间会努力找到根源
        if wordlist:
            self.wordlist=wordlist
        self.chance=chance
    def update(self): #更新单词状态及日志
        system('cls')
        #print(self.word)
        for l in self.letterstack:
            print(*l,sep='')
        print('='*(len(self.word)+2))
        for i in self.log:
            print(i)
    def homepage(self):
        system('cls')
        char=['Welcome to ',
              Back.GREEN+Fore.WHITE+'W',
              Back.YELLOW+Fore.WHITE+'O',
              Back.LIGHTBLACK_EX+Fore.WHITE+'R',
              Back.GREEN+Fore.WHITE+'D',
              Back.YELLOW+Fore.WHITE+'P',
              Back.LIGHTBLACK_EX+Fore.WHITE+'Y']
        print(*char,sep='')
        print('Choose one:\n1. Make a word key.\n2. Guess a word.')
        a=input('> ')
        if a=='1': #获取单词密钥
            a=str(randint(1,9))
            w=input('Input your word: ')
            if self.invalid_word(w): #单词是否非法
                self.homepage()
                print(Fore.RED+'Invalid word.')
            else:
                c=input('Input the number of chances: ')
                input('Your word key is: '+WordKey(w+c,int(a)).encode())
                self.homepage()
        elif a=='2': #猜单词
            system('cls')
            print('Choose one:\n1. Random word.\n2. Use a word key.')
            a=input('> ')
            if a in ('1','2'):
                if a=='1': #随机进行猜单词
                    w=np.random.choice(wordlist)
                    self.initguess(w,6)
                elif a=='2': #使用出题者提供的密钥
                    wk=input('Input your word key: ')
                    w=WordKey(wk,int(wk[-1])).decode()
                    self.initguess(w,w[-2])
                self.log.append(Fore.BLUE+'The length of word is: '+str(len(self.word)))
                self.update()
                ok=False
                self.st=time.time()
                while ok==False:
                    w=input('> ')
                    if w != '':
                        try:
                            ok=self.give(w)
                        except Exception as e:
                            print(Fore.RED+'Invalid input.',e,sep='\n')
                    else:
                        ok=True
                self.update()
                input('Press enter to go back...')
                self.homepage()
            else:
                self.homepage()
        else:
            quit()
    def invalid_word(self,s:str): #判断该单词是否无效
        return not (s.isalpha() and any(i.islower() for i in s) and s in self.wordlist)
    def give(self,word:str):
        r=False
        if self.invalid_word(word):
            self.log.append(Fore.RED+'Invalid character.')
            r=False
        elif word==self.word:
            self.letterstack.append([Back.GREEN+Fore.WHITE+i for i in word])
            self.log.append(Fore.GREEN+'You win!  Total time:'+str(time.time()-self.st)+'s')
            r=True
        elif len(word)==len(self.word):
            self.chance-=1
            if self.chance <= 0:
                self.log.append(f'{Fore.YELLOW}You lost! The answer is "{self.word}".')
                r=True
            else:
                cache=[]
                for i in range(len(word)):
                    if word[i]==self.word[i]:
                        cache.append(Back.GREEN+Fore.WHITE+word[i])
                    elif word[i] in self.word:
                        cache.append(Back.YELLOW+Fore.WHITE+word[i])
                    else:
                        cache.append(Back.LIGHTBLACK_EX+Fore.WHITE+word[i])
                self.log.append(Fore.YELLOW+'You have only '+str(self.chance)+' chances.')
                self.letterstack.append(cache)
                r=False
        elif len(word)!=len(self.word):
            self.log.append(Fore.RED+'Invalid input.')
        else:
            raise TypeError
        self.update()
        return r
def __txt_to_py_script():
    with open('./wordlist.txt','r',encoding='utf-8') as f:
        a=f.readlines()
    b=[]
    for i in a:
        b.append(i[:-1])
    with open('./wordlist.py','w',encoding='utf-8') as f:
        f.write(f'wordlist=array({b})')

if __name__=='__main__':
    WordPy()