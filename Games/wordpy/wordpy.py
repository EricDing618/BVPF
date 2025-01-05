from colorama import Fore,Back,init
from os import system

init(autoreset=True)
class WordKey:
    def __init__(self,string:str):
        self.s=string
    def encode(self):
        ...
    def decode(self):
        ...
class WordPy:
    def __init__(self):
        self.letterstack=[]
        self.log=[]
    def initguess(self,result:str,wordlist:list|tuple,chance:int):
        self.word=result
        self.wordlist=wordlist
        self.chance=chance
    def update(self):
        system('cls')
        for l in self.letterstuck:
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
        if input('> ')=='1':


    def give(self,word:str):
        if self.chance <= 0:
            self.log.append(f'{Fore.YELLOW}You lost! The answer is "{self.word}.')
        elif not word.isalpha():
            self.log.append(Fore.RED+'Invalid character.')
            return False
        elif word==self.word:
            self.letterstack.append([Back.GREEN+Fore.WHITE+i for i in word])
            return True
        elif len(word)==len(self.word):
            self.chance-=1
            cache=[]
            for i in range(len(word)):
                if word[i]==self.word[i]:
                    cache.append(Back.GREEN+Fore.WHITE+word[i])
                elif word[i] in self.word:
                    cache.append(Back.YELLOW+Fore.WHITE+word[i])
                else:
                    cache.append(Back.LIGHTBLACK_EX+Fore.WHITE+word[i])
            self.letterstack.append(cache)
            return False
        else:
            raise TypeError
        self.update()

if __name__=='__main__':
