class Element:
    def __init__(self, symbol:str, atomic_number:int=1):
        self.symbol = symbol
        self.atomic_number = atomic_number
        assert atomic_number > 0, "Atomic number must be positive"

    def __repr__(self):
        return f"{self.symbol}_{self.atomic_number}"

class Compound:
    def __init__(self, name:str):
        self.name = name.replace(' ','')
        self.elements: list[Element] = []
        if self.name[-1] in ('↑','↓'):
            self.name = self.name[:-1]
    def transform(self):
        current_symbol = ""
        current_num = ""
        if not self.name[0].isupper():
            raise SyntaxError("Invalid Compound")
        for s in self.name:
            if s.isupper():
                if len(list(filter(str.isupper,current_symbol))) > 1 or (current_symbol and not current_symbol[0].isupper()):
                    raise SyntaxError("Invalid Compound")
                
                if current_num:
                    self.elements.append(Element(current_symbol,int(current_num)))
                else:
                    self.elements.append(Element(current_symbol))
                current_num = ""
                current_symbol = s
            elif s.isdigit():
                if len(list(filter(str.isupper,current_symbol))) > 1 or not current_symbol[0].isupper():
                    raise SyntaxError("Invalid Compound")
                current_num+=s
            elif s.islower():
                if len(list(filter(str.isupper,current_symbol))) > 1 or not current_symbol[0].isupper():
                    raise SyntaxError("Invalid Compound")
                current_symbol+=s
            else:
                raise SyntaxError("Invalid Compound")
            
            if current_num:
                self.elements.append(Element(current_symbol,int(current_num)))
            else:
                self.elements.append(Element(current_symbol))
            
    def __transform(self):
        next_element = False
        current_symbol = ""

        for s in self.name:
            if s.isupper():
                if current_symbol:
                    if current_symbol[0].isupper():
                        self.elements.append(Element(current_symbol))
                        current_symbol=''
                    else:
                        raise SyntaxError("Invalid Compound")
                current_symbol+=s
            elif s.islower():
                if next_element or not current_symbol:
                    raise SyntaxError("Invalid Compound")
                current_symbol+=s
            elif s.isdigit():
                assert int(s) > 1, "Invalid Compound"
                if next_element or not current_symbol:
                    raise SyntaxError("Invalid Compound")
                self.elements.append(Element(current_symbol,int(s)))
                next_element=True
            else:
                raise SyntaxError("Invalid Compound")
            
class Equation:
    def __init__(self,eq:str):
        '''**eg:**  `eq="C+O2=点燃, ...=CO2"`  '''
        self.eq = eq.replace(' ','')
        reactants, condition, products = self.eq.split('=')
        self.reactants = reactants.split('+')
        self.conditions = condition.split(',')
        self.products = products.split('+')
            
test1 = Compound('CaCO3↓')
test1.transform()
test2 = Equation('H2O2=MnO2=H2O+O2↑')
print(*test1.elements)
print(*test2.reactants)
print(*test2.conditions)
print(*test2.products)