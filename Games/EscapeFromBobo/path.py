import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"]="1" #禁用Pygame的输出

getcwd=os.getcwd

def join(*args:str):
    '''更好地兼容这个项目'''
    c1=[]
    c2=getcwd()
    for p in args:
        p=p.replace('/','\\').replace('\\\\','\\')
        if p[0]==".":
            p=p[1:]
        c1.append(p)

    for p in c1:
        if p != getcwd:
            c2=os.path.join(c2,p)

    return c2


if "EscapeFromBobo" not in getcwd():
    workpath=join(getcwd(),"EscapeFromBobo")
else:
    workpath=getcwd()

if __name__=='__main__':
    print(
        join(
        'C:\\\\a\\',
        'b\\',
        './c'
    )
    )