#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import random
from tools.model import *
from base import *

class Fool(Strategie):
    """ stratégie aléatoire constructeur + next_action 
	NE PAS MODIFIER CETTE CLASSE 
    """
    def __init__(self):
        """ le constructeur parent avec les informations nécessaires """
        super().__init__(0)
        
    def next_action(self): return random.choice(self.actions)

class Gentle(Strategie):
    """ stratégie gentille, on a juste besoin de définir next_action """
    def __init__(self):
        """ le constructeur parent avec les informations nécessaires """
        super().__init__(1)
        
    def next_action(self): return 'C'
    

class Bad(Strategie):
    """ statégie méchante """
    def __init__(self):
        """ le constructeur parent avec les informations nécessaires """
        super().__init__(-1)
        
    def next_action(self): return 'D'



class GentleSulky(Strategie):
    """ statégie gentil mémoire 1"""
    def __init__(self):
        """ le constructeur parent avec les informations nécessaires """
        super().__init__(1,1,m2)

    def next_action(self) : 
        if len(self.memory) == 0 : return 'C'
        elif self.memory[-1] == 'R' : return 'C'
        else : return 'R'
    

class BadSulky(Strategie):
    """ statégie méchant mémoire 1"""
    def __init__(self):
        """ le constructeur parent avec les informations nécessaires """
        super().__init__(-1,1,m2)

    def next_action(self) :
        if len(self.memory) == 0 : return 'D'
        if self.memory[-1] == 'R' or self.memory[-1] == 'T': return 'C'
        else : return 'R'

class FoolSulky(Strategie):
    """ statégie aléatoire mémoire 1"""
    def __init__(self):
        """ le constructeur parent avec les informations nécessaires """
        super().__init__(0,1,m2)

    def next_action(self) :
        if len(self.memory) == 0 : return random.choice(('D','C'))
        if self.memory[-1] == 'R' or self.memory[-1] == 'T': return 'C'
        else : return 'R'

class Tit4Tat(Strategie):
    """ statégie oeil pour oeil"""
    def __init__(self):
       """ le constructeur parent avec les informations nécessaires """
       super().__init__(1,1)
        
    def next_action(self):
        if len(self.memory) == 0 : return 'C'
        else : return self.adv_action(self.memory[-1])
        
    
class WinStayLooseShift(Strategie):
    """ statégie constante si victoire sinon changement mémoire 1"""
    def __init__(self):
        """ le constructeur parent avec les informations nécessaires """
        super().__init__(1,1)
   
    def next_action(self):
        if len(self.memory) == 0 : return 'C'
        elif self.memory[-1] == 'T' or self.memory[-1] == 'R' :
            return self.my_action(self.memory[-1])
        elif self.memory[-1] == 'P' or self.memory[-1] == 'S' :
            if self.my_action(self.memory[-1]) == 'C' : return 'D'
            else : return 'C'


class Pavlov(Strategie):
    """ statégie pavlov mémoire 1"""
    def __init__(self):
        """ le constructeur parent avec les informations nécessaires """
        super().__init__(1,1)

    def next_action(self) :
        if len(self.memory) == 0 : return 'C'
        elif self.memory[-1] == 'P' or self.memory[-1] == 'R' :
            return self.my_action(self.memory[-1])
        elif self.memory[-1] == 'T' or self.memory[-1] == 'S' :
            if self.my_action(self.memory[-1]) == 'C' : return 'D'
            else : return 'C'

class Periodique(Strategie):
    
    """ requires an str of length p of D|C characters
    requires str to be the shortest acyclic
    CDCD is wrong since CD is sufficient
    """
    
    def __init__(self, acyclic:str):

        if len(acyclic) == 0 :
            x = -1
        elif acyclic[0] == 'D'  :
            x = -1
        else : x = 1

        super().__init__(x)

        if acyclic == '' : self.__word = self.style
        else : self.__word = acyclic
        

    @property
    def word(self) :
        return self.__word       

    def next_action(self):
        return self.__word[self.count%len(self.__word)]




class Markov(Strategie):
    """ requires a vector of length 4
    values are in [0 ; 1] U {-1}
    missing values are set to -1
    requires vector’s values to be ’probabilities’
    requires a model
    """
    def __init__(self, styl:int, probas:(list, tuple), model:Model=m1):
        p = list(probas)
        if len(p) > 4 :
            while len(p) > 4 :
                del p[-1]
        if len(p) < 4 :
            for i in range(4-len(p)):
                p.append(-1)
        probas = tuple(p)
        if len(probas) == 4 :
            self.__probas = probas
        super().__init__(styl,1,model)
            
    @property
    def probabilities(self)->tuple :
        return self.__probas

    def auto_test(self)->bool :

        for i in self.probabilities:
            if i != -1 :
                if i < 0 or i > 1 :
                    return False
        
        return True

                             

    def next_action(self) :

        if len(self.memory) == 0 :
            if self.style == 'a' :
                return random.choice(self.actions)
            else :
                return self.style

        if self.memory[-1] == 'T':
            a = 0
        if self.memory[-1] == 'R':
            a = 1
        if self.memory[-1] == 'P':
            a = 2
        if self.memory[-1] == 'S':
            a = 3

            
        if self.__probas[a] == -1 :
            return random.choice(self.actions)
        else :
            if random.random() <= self.__probas[a] :
                return 'C'
            else :
                return random.choice(self.actions.replace('C',''))
                
class Stochastique(Strategie):
    
    """ requires a vector of length at least 1 at most 9
    values are in [0 ; 1] U {-1}
    missing values are set to -1
    requires vector’s values to be ’probabilities’
    requires a model which determins the length of stored vector
    """
    
    def __init__(self, probas:(list, tuple), model:Model=m1):

        if probas[0] == 0 :
            super().__init__(-1,1,model)
            
        elif probas[0] == 1 :
            super().__init__(1,1,model)
                          
        else :
            super().__init__(0,1,model)
        
        probas = list(probas)
        
        if len(self.actions)== 2  :    
            if len(probas) > 5 :
                probas = probas[:5]
            elif len(probas) < 5 :
                probas.extend([-1 for i in range(5-len(probas))])

        else :
            if len(probas) > 9 :
                probas = probas[:9]
            elif len(probas) < 9 :
                probas.extend([-1 for i in range(9-len(probas))])

        probas = tuple(probas)

        self.__probas = probas

        

                
    @property
    def probabilities(self) :
        return self.__probas

    def auto_test(self) :

##        if self._model == 1 and len(self.__probas) > 5 or self._model == 1 and len(self.__probas) < 5 :
##            return False
##        elif self._model == 2 and len(self.__probas) < 9 or self._model == 2 and len(self.__probas) > 9 :
##            return False  
            
        
        for i in self.__probas :
            if i != -1 :
                if i < 0 or i > 1 :
                    return False

        if len(self.__probas) == 9 :

            for i in range(1,5) :
                if self.__probas[i] != -1 and self.__probas[i+4] != -1 :
                    if self.__probas[i]+self.__probas[i+4] > 1 :
                        return False

        
        return True

    def next_action(self) :
        
        if self.count ==0 :
            if self.style == 'a' :
                if self.probabilities[0] == -1 :
                    return random.choice("DC")
                else :
                    return self.style
                    
            else :
                return self.style

        else :
            lst  = self.get_probabilities(self.memory)
            p = random.random()
            if p <= lst[0] :
                return 'C'
            else :
                if len(self.probabilities) < 6 :
                    return "D"
                else :
                    p = p - lst[0]
                    if p <= lst[1] :
                        return "D"
                    else :
                        return "R" 
            
        

    def get_probabilities(self, rew:str) :

        if rew!='R' and rew!='T' and rew!= 'S' and rew !='P':
            return ()

        if rew in self._model.reward_names :

            a,b,c,d = 0,0,0,0
            if len(self.probabilities) < 6 :
                if self.my_action(rew) == 'C' :
                    a = 1
                else : 
                    a = 2
                if self.adv_action(rew) == 'C':
                    b = 3
                else :
                    b = 4

            else :
                if self.my_action(rew) == 'C' :
                    a = 1
                    c = 5
                else : 
                    a = 2
                    c = 6
                if self.adv_action(rew) == 'C':
                    b = 3
                    d = 7
                else :
                    b = 4
                    d = 8
            lst = []
            
            if len(self.probabilities) < 6 :

                
                if self.probabilities[a] != -1 and self.probabilities[b] != -1 :
                    lst.append(self.probabilities[a]+self.probabilities[b] - self.probabilities[a]*self.probabilities[b])
                    lst.append(1-lst[0])
                    lst.append(0)

                if self.probabilities[a] != -1 and self.probabilities[b] == -1 :
                    lst.append(self.probabilities[a])
                    lst.append(1-self.probabilities[a])
                    lst.append(0)

                if self.probabilities[a] == -1 and self.probabilities[b] != -1 :

                    lst.append(self.probabilities[b])
                    lst.append(1-self.probabilities[b])
                    lst.append(0)
                    
                if self.probabilities[a] == -1 and self.probabilities[b] == -1 :
                    lst.append(1/2)
                    lst.append(1/2)
                    lst.append(0)
                        


            else :

                
                if self.probabilities[a] != -1 and self.probabilities[b] != -1: #on connait les donnees de cooperer

                    

                    if self.probabilities[c] != -1 and self.probabilities[d] == -1 : #on a un renoncer sur les deux

                        r = self.probabilities[a]+self.probabilities[b] - self.probabilities[a]*self.probabilities[b]
                        lst.append(r)
                        rr = (1-r)*self.probabilities[c]
                        lst.append(1-(r+rr))
                        lst.append(rr)

                       
                    elif self.probabilities[c] == -1 and self.probabilities[d] != -1 : #on a un renoncer sur les deux 

                        r = self.probabilities[a]+self.probabilities[b] - self.probabilities[a]*self.probabilities[b]
                        lst.append(r)
                        rr = (1-r)*self.probabilities[d]
                        lst.append(1-(r+rr))
                        lst.append(rr)

                       

                    elif self.probabilities[c] != -1 and self.probabilities[d] != -1 : #on a toutes les probas de renoncer

                        
                        lst.append(self.probabilities[a]+self.probabilities[b] - self.probabilities[a]*self.probabilities[b])
                        r = (1-lst[0])*(self.probabilities[c]+self.probabilities[d]-self.probabilities[c]*self.probabilities[d])
                        lst.append(1-lst[0]-r)
                        lst.append(r)
                        
                        
                        
                    elif self.probabilities[c] == -1 and self.probabilities[d] == -1 : #on a pas les probas de renoncer
                       
                        lst.append(self.probabilities[a]+self.probabilities[b] - self.probabilities[a]*self.probabilities[b])
                        lst.append((1-lst[0])/2)
                        lst.append((1-lst[0])/2)

                        
                elif self.probabilities[a] == -1 and self.probabilities[b] == -1:  #les données pour cooperer sont inconnues

                    if self.probabilities[c] != -1 and self.probabilities[d] == -1 : #une donnée sur deux de renoncer

                        lst.append((1-self.probabilities[c])/2)
                        lst.append((1-self.probabilities[c])/2)
                        lst.append(self.probabilities[c])
    
                    if self.probabilities[c] == -1 and self.probabilities[d] != -1 :#une donnée sur deux de renoncer

                        lst.append((1-self.probabilities[d])/2)
                        lst.append((1-self.probabilities[d])/2)
                        lst.append(self.probabilities[d])

                    if self.probabilities[c] != -1 and self.probabilities[d] != -1 : #les données de renoncer sont connues 

                        pr=self.probabilities[c]+self.probabilities[d]-self.probabilities[c]*self.probabilities[d]
                        lst.append((1-pr)/2)
                        lst.append((1-pr)/2)
                        lst.append(pr)

                        
                    if self.probabilities[c] == -1 and self.probabilities[d] == -1 : #aucune données connues 

                        lst.append(1/3)
                        lst.append(1/3)
                        lst.append(1/3)
                
                        
                elif self.probabilities[a] == -1 and self.probabilities[b] != -1:

                    if self.probabilities[c] == -1 and self.probabilities[d] == -1 :
                            
                        lst.append(self.probabilities[b])
                        lst.append((1-self.probabilities[b])/2)
                        lst.append((1-self.probabilities[b])/2)

                            
                    if self.probabilities[c] != -1 and self.probabilities[d] == -1 :

                        lst.append(self.probabilities[b])
                        r = (1-self.probabilities[b])*self.probabilities[c]
                        lst.append(1-r-self.probabilities[b])
                        lst.append(r)
                                       
                    if self.probabilities[c] == -1 and self.probabilities[d] != -1 :

                        lst.append(self.probabilities[b])
                        r = (1-self.probabilities[b])*self.probabilities[d]
                        lst.append(1-r-self.probabilities[b])
                        lst.append(r)
                                       

                    if self.probabilities[c] != -1 and self.probabilities[d] != -1 :
                            
                        lst.append(self.probabilities[b])
                        r = (1-lst[0])*(self.probabilities[c]+self.probabilities[d]-self.probabilities[c]*self.probabilities[d])
                        lst.append(1-lst[0]-r)
                        lst.append(r)
                        

                elif self.probabilities[a] != -1 and self.probabilities[b] == -1:

                        
                    if self.probabilities[c] == -1 and self.probabilities[d] == -1 :
                            
                        lst.append(self.probabilities[a])
                        lst.append((1-self.probabilities[a])/2)
                        lst.append((1-self.probabilities[a])/2)
                            
                    if self.probabilities[c] != -1 and self.probabilities[d] == -1 :

                        lst.append(self.probabilities[a])
                        r = (1-self.probabilities[a])*self.probabilities[c]
                        lst.append(1-r-self.probabilities[a])
                        lst.append(r)

                    if self.probabilities[c] == -1 and self.probabilities[d] != -1 :
                       
                        lst.append(self.probabilities[a])
                        r = (1-self.probabilities[a])*self.probabilities[d]
                        lst.append(1-r-self.probabilities[a])
                        lst.append(r)

                                       

                    if self.probabilities[c] != -1 and self.probabilities[d] != -1 :

                        lst.append(self.probabilities[a])
                        r = (1-lst[0])*(self.probabilities[c]+self.probabilities[d]-self.probabilities[c]*self.probabilities[d])
                        lst.append(1-lst[0]-r)
                        lst.append(r)

            return tuple(lst)

class Automaton(Strategie):
    """
    requires a string of length 1, 5, 21 or 85
    requires the string letters in model.actions
    """
    def __init__(self, rules:str, model:Model=m1):

        if len(rules) == 0 :
            mem = 0            
            
        if len(rules) < 5 :                     #peut etre mettre intervalle
            rules = rules[:1]
            mem = 0

        elif len(rules) < 21 and len(rules) >= 5 :
            rules = rules[:5]
            mem = 1
        elif len(rules) < 85 and len(rules) >= 21 :
            rules = rules[:21]
            mem = 2

        else :
            rules = rules[:85]
            mem = 3
            
        if len(rules) == 0 :
            super().__init__(0,0,model)
        elif rules[0] == 'C' :
            super().__init__(1,mem,model)

        elif rules[0] == 'D' :
            super().__init__(-1,mem,model)
            
        else :
            super().__init__(0,mem,model)
    

        self.__rules = rules
        

    @property
    def rules(self):
            return self.__rules

    def auto_test(self) :

        if len(self.rules) != 1 and  len(self.rules) != 5 and len(self.rules) != 21 and len(self.rules) != 85 :
            return False 

        for i in self.rules :
            if i not in self.actions :
                return False

        if self.rules[0] == 'R':
            return False

        return True

    def next_action(self):

        if self.count == 0 or len(self.rules) == 1:
            return self.rules[0]
            
        
        else :
            for i in [5,21,85]:
                if len(self.rules) == i :
                    return self.rules[self._model.encoding(self.memory)]
                           
if __name__ == "__main__":
    g = Gentle()
    b = Bad()
    f = Fool()
    ws = WinStayLooseShift()
    gs = GentleSulky()
    bs = BadSulky()
    fs = FoolSulky()
    tt = Tit4Tat()
    p = Pavlov()
    f.surname = "Lunatique"
    b.surname = "Méchant"
    g.surname = "Gentil"
    evaluation(g,g)
    evaluation(b,b)
    evaluation(f,f)
    evaluation(ws,ws)
    evaluation(p,p)
    evaluation(tt,tt)
    evaluation(gs,gs,model=m2)
    evaluation(bs,f,model=m2)
    evaluation(gs,tt,model=m2)
    evaluation(gs,f,model=m2)
    evaluation(ws,g)
    m1.rewards
    m1.values
    m1.get_actions('T')
    m1.actions
    evaluation(b,b)
    evaluation(f,f)
    evaluation(ws,ws)
    evaluation(p,p)
    evaluation(tt,tt)
    evaluation(gs,gs,model=m2)
    evaluation(bs,f,model=m2)
    evaluation(gs,tt,model=m2)  
    evaluation(gs,f,model=m2)
    evaluation(ws,g)
    m1.rewards
    m1.values
    m1.get_actions('T')
    m1.actions
    m2.actions
    m1.reward_names
    m2.reward_names
    m2.get_actions('T')
    m2.get_actions('A')

    x = Periodique("C")
    x.style == 'C'
    x.size == 0
    x.word == "C"
    x.word == 'C'
    x.word == 'D'
    y = Strategie()
    issubclass(x.__class__, y.__class__)
    p = Periodique('')
    p.size == 0
    p.word == 'D'
    p.style == 'D'

    u = Majorite()
    issubclass(u.__class__, x.__class__)
    u.size
    u.majority
    u.get_reward('T')
    u.majority
    for x in "TRPS": u.get_reward(x) ; print(u.majority)
    u = Majorite(maxsz=2)
    issubclass(u.__class__, x.__class__)
    u.size
    u.majority
    u.get_reward('T')
    print("memory {0.memory}, maj {0.majority:+0d}".format(u))
    for x in "PSRT": u.get_reward(x) ; print("memory {0.memory}, maj {0.majority:+0d}".format(u))
    
    
    m = Markov(1,[1,1/2,1/3])
    evaluation(m,m)
    
    s = Stochastique([1])
    s.probabilities == (1, -1, -1, -1, -1)
    s.auto_test() == True
    s.style == "C"
    s.size == 1
    c = Stochastique([-1], model=m2)
    c.probabilities == (-1, -1, -1, -1, -1, -1, -1, -1, -1)
    c.auto_test() == True
    c.style == "a"
    c.size == 1
    d = Stochastique([-1, 1, -1, -1, 1/4, .5], model=m2)
    d.probabilities == (-1, 1, -1, -1, 0.25, .5, -1, -1, -1)
    d.auto_test() == False
    d.style == "a"
    d.size == 1
    a = Stochastique([1, -1, -1, 0, 0])
    a.get_probabilities('T')
    a.get_probabilities('S')
    s = Stochastique([1, -1, -1, -1, 0])
    s.get_probabilities('T')        
    s.get_probabilities('S')
    c = Stochastique((1, 1/2, 1/3, 1/2, -1), m2)
    c.probabilities
    c.auto_test()
    c.get_probabilities('S')
    c.get_probabilities('T')
    d = Stochastique((1, -1, -1, -1, -1, -1, 1, -1, 2/3), m2)
    d.probabilities
    d.auto_test()
    d.get_probabilities('S')
    d.get_probabilities('T')

    e = Automaton("")
    e.size == 0
    e.style == 'a'
    e.rules == ''
    e.auto_test() == False
    e = Automaton('R')
    e.size == 0
    e.style == 'a'
    e.rules == 'R'
    e.auto_test() == False
    e = Automaton('R', m2)
    e.size == 0
    e.style == 'a'
    e.rules == 'R'
    e.auto_test() == False
    e = Automaton("C"+7*"R", m2)
    e.size == 1
    e.style == 'C'
    e.rules == 'CRRRR'
    e.auto_test() == True
