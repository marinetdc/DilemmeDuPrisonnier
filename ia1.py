#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import random

class Model:
    def __init__(self, rewards:dict, values:dict):
        """ 
            à partir des récompenses (rewards) et des valeurs (values) 
            construit plusieurs attributs (property)
	        self.rewards : 
                 les récompenses et les actions les causant
	        self.values : 
                 les valeurs
	        self.actions : 
                 les actions valides
	        self.reward_names : 
                 les noms des récompenses

            et dispose d'une méthode
	        self.get_actions(rew:str) -> str : 
                 les actions associées aux récompenses
        """
        self.__recompenses = set(''.join([x for x in rewards.values()]))
        self.__actions = set(''.join([x for x in rewards.keys()]))
        if len(rewards) != len(self.__actions)**2:
            raise Exception("Actions inconsistency")
        if len(self.__recompenses) != len(values):
            raise Exception("Rewards inconsitency")
        self.__rewards = rewards
        self.__values = values
        self.__rewact = {}
        for k,v in rewards.items():
            for (i,x) in enumerate(v):
                _old = self.__rewact.get(x, set())
                if i == 0: _old.add(k)
                else: _old.add(k[::-1])
                self.__rewact[x] = _old

        for k in self.__rewact:
            if len(self.__rewact[k]) != 1:
                self.__rewact[k] = list(self.__rewact[k])
            else:
                self.__rewact[k] = self.__rewact[k].pop()

    @property
    def rewards(self): return self.__rewards
    @property
    def values(self): return self.__values
    @property
    def actions(self):
        return ''.join(sorted(list(self.__actions), reverse=True))
    @property
    def reward_names(self):
        return ''.join(sorted(list(self.__recompenses)))

    def get_actions(self, rew):
        """ for a given reward send the actions involved 
            1st is mine, 2nd is adversary
        """
        return self.__rewact.get(rew,'')
    
    def __repr__(self) -> str:
        return ("{0}({1.rewards}, {1.values})"
                .format(self.__class__.__name__, self))
    def __str__(self) -> str:
        _str = ""
        _str += "{:<19s} '{}'\n".format("actions authorized:", self.actions)
        _str += "{:<19s} '{}'\n".format("rewards' names:", self.reward_names)
        _str += "{:<19s} {}\n".format("rewards' values:", list(self.values.items()))
        return _str

default = { 'DD': 'PP', 'DC': 'TS', 'CD': 'ST', 'CC': 'RR' }
default_val = { 'T': 7, 'R': 5, 'P': 2, 'S': 0}
m1 = Model( default.copy(), default_val.copy() )
for x in "DC":
    default[x+'R'] = default['R'+x] = "AA"
default["RR"] = "AA"
default_val['A'] = 3    
m2 = Model( default, default_val )



class Strategie:
    ID = 0
    def __init__(self, styl:int=1, maxsz:int=0, model:Model=m1):
        """ constructeur 
	    styl in {-1, 0, 1} le style correspondant au premier coup joué
	    maxsz : la taille maximum occupée par la mémoire
	    model : le modèle dans lequel on joue
	"""
        # NE PAS MODIFIER LES 2 LIGNES SUIVANTES
        self.__idnum = self.ID
        Strategie.ID += 1
        # ICI les variables locales communes à initialiser
        # avec styl, maxsz, actions ou encore surname et color

        
        self.mod = model
        self.taille = -1 if maxsz < 0 else maxsz
        self.taille_memoire = 0
        self.memoire = str()
        self.surnom = str()
        self.surnom = self.name
        self.nb_coup = 0
        self.hist = {}
        self.col = self.idnum

        if styl == -1 : self.styleto = 'D'
        elif styl == 1: self.styleto = 'C'
        else  : self.styleto = 'a'

        
        
        self.action = model.actions

        # ENSUITE reset
        self.reset()

    def reset(self) -> None:
        """ raz des variables """
        self.nb_coup = 0
        self.memoire = str()
        self.taille_memoire = 0
        self.hist = {}
        
        

    # NE PAS MODIFIER CES 4 LIGNES
    @property
    def idnum(self) -> int:
        return self.__idnum
    @property
    def name(self) -> str:
        return "Strat_{0.idnum:03d}".format(self) # return "Strat_"+str(self.idnum)

    # A PARTIR D'ICI IL FAUT FAIRE QQUE CHOSE
    @property
    def size(self) -> int:
        """ renvoie la taille max de la mémoire
        - infinie: -1
        - sinon un entier >= 0
        """
        return self.taille 
        

    @property
    def memsz(self) -> int:
        """ renvoie la taille mémoire occupée """ 
        return self.taille_memoire

    @property
    def memory(self) -> str:
        """ renvoie la mémoire des dernières récompenses """
        return self.memoire

    @property
    def actions(self) -> str:
        """ renvoie les actions autorisées DC ou DCA ordre quelconque """
        return self.action
        

    @property
    def count(self) -> int:
        """ le nombre de récompenses depuis reset """
        return self.nb_coup

    @property
    def style(self) -> str:
        """ renvoie D, C ou a """
        return self.styleto
        
        
    @property
    def surname(self) -> str:
        """ renvoie le petit nom de la stratégie """
        return self.surnom
        
    @surname.setter
    def surname(self, v) -> None:
        """ change le petit nom de la stratégie """
        if type(v) == str :
            self.surnom= v


    @property
    def color(self) -> int:
        """ un entier entre 0 et 255 """
        return self.col
    @color.setter
    def color(self, v) -> None:
        """ modifie la valeur de la couleur """
        if v in range(256):  self.col = v

    def __repr__(self) -> str:
        """ pour afficher les paramètres du constructeur """
        return str(self.__class__.__name__)+"("+str(self.styleto)+","+str(self.taille)+","+str(repr(self.mod))+")"
    
    def __str__(self) -> str:
        """ donne des informations détaillées sur la stratégie """
        strr = str()
        strr = "Strategie :{0.idnum}\n Taille max :{0.taille} \n Taille memoire :{0.taille_memoire} \n Memoire :{0.memoire}\n Nom :{0.name}\n Style :{0.style} \n Action :{0.action}\n Nombre de coup :{0.nb_coup}".format(self) 
        return strr
    
    def get_reward(self, rew) -> None:
        """ stocke la dernière récompense """
        if rew not in self.hist.keys() :
            self.hist[rew]= 1
        else :
            self.hist[rew]= 1 + self.hist[rew]
        self.nb_coup += 1
        if self.taille == 0 :
            pass
        if self.taille_memoire == 0 and self.taille > 0 :
            self.memoire = self.memoire+str(rew)
            self.taille_memoire += 1
        elif self.taille == -1 :
            self.memoire = self.memoire+str(rew)
            self.taille_memoire += 1
        elif self.taille_memoire < self.taille :
            self.memoire = self.memoire+str(rew)
            self.taille_memoire += 1
        elif self.taille_memoire == self.taille and self.taille != 0:
            self.memoire = self.memoire[1:]
            self.memoire = self.memoire+str(rew)
        

        
                
    def history(self) -> tuple:
        """ renvoie un n-uplet de paire (récompense, int) """
        return self.hist.items()

        

    def my_action(self, rew:str) -> str:
        """ renvoie l'action que j'ai faite en fonction de la récompense """
        if rew not in self.hist : return '' 
        if rew == 'P' :
            return 'D'
        if rew == 'T' :
            return 'D'
        if rew == 'S' :
            return 'C'
        if rew == 'R' :
            return 'C'
        if rew == 'A' :
            return 'R'
        
    
    def adv_action(self, rew:str) -> str:
        """ renvoie l'action faite par mon adversaire
            en fonction de la récompense
        """
        if rew not in self.hist : return '' 
        if rew == 'P' :
            return 'D'
        if rew == 'T' :
            return 'C'
        if rew == 'S' :
            return 'D'
        if rew == 'A' :
            return 'R'
        if rew == 'R' :
            return 'C'
        

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
        if len(self.memoire) == 0 : return 'C'
        elif self.memoire[-1] == 'R' : return 'C'
        else : return 'R'
    

class BadSulky(Strategie):
    """ statégie méchant mémoire 1"""
    def __init__(self):
        """ le constructeur parent avec les informations nécessaires """
        super().__init__(-1,1,m2)

    def next_action(self) :
        if len(self.memoire) == 0 : return 'D'
        if self.memoire[-1] == 'R' or self.memoire[-1] == 'T': return 'C'
        else : return 'R'

class FoolSulky(Strategie):
    """ statégie aléatoire mémoire 1"""
    def __init__(self):
        """ le constructeur parent avec les informations nécessaires """
        super().__init__(0,1,m2)

    def next_action(self) :
        if len(self.memoire) == 0 : return random.choice(('D','C'))
        if self.memoire[-1] == 'R' or self.memoire[-1] == 'T': return 'C'
        else : return 'R'

class Tit4Tat(Strategie):
    """ statégie oeil pour oeil"""
    def __init__(self):
       """ le constructeur parent avec les informations nécessaires """
       super().__init__(1,1)
        
    def next_action(self):
        if len(self.memoire) == 0 : return 'C'
        else : return self.adv_action(self.memoire[-1])
        
    
class WinStayLooseShift(Strategie):
    """ statégie constante si victoire sinon changement mémoire 1"""
    def __init__(self):
        """ le constructeur parent avec les informations nécessaires """
        super().__init__(1,1)
   
    def next_action(self):
        if len(self.memoire) == 0 : return 'C'
        elif self.memoire[-1] == 'T' or self.memoire[-1] == 'R' :
            return self.my_action(self.memoire[-1])
        elif self.memoire[-1] == 'P' or self.memoire[-1] == 'S' :
            if self.my_action(self.memoire[-1]) == 'C' : return 'D'
            else : return 'C'


class Pavlov(Strategie):
    """ statégie pavlov mémoire 1"""
    def __init__(self):
        """ le constructeur parent avec les informations nécessaires """
        super().__init__(1,1)

    def next_action(self) :
        if len(self.memoire) == 0 : return 'C'
        elif self.memoire[-1] == 'P' or self.memoire[-1] == 'R' :
            return self.my_action(self.memoire[-1])
        elif self.memoire[-1] == 'T' or self.memoire[-1] == 'S' :
            if self.my_action(self.memoire[-1]) == 'C' : return 'D'
            else : return 'C'


                    

# le système d'évaluation décrit dans la fiche jalon01
# NE PAS MODIFIER
def evaluation(st1:Strategie, st2:Strategie, nbMatch:int=10, 
               min_iter:int=1, max_iter:int=100, model:Model=m1) -> tuple:
    """ renvoie les gains moyens de st1 & st2
	c'est la moyenne des gains moyens de chaque match (moyenne sur nbMatch)
	chaque match est une suite d'itérations comprises entre min_iter et max_iter
	Par défaut on fera 10 match d'au plus 100 rencontres
    """
    rewards = model.rewards
    valeurs = model.values
    total_st1 = 0
    total_st2 = 0
    total_iter = 0
    for i in range(nbMatch):
        st1.reset()
        st2.reset()
        nb_iter = random.randrange(min_iter, max_iter)
        total_iter += nb_iter
        for j in range(nb_iter):
            a_1 = st1.next_action()
            a_2 = st2.next_action()
            gains = rewards[a_1+a_2]
            st1.get_reward(gains[0])
            st2.get_reward(gains[1])
        total_st1 += sum([valeurs[key]*v for (key, v) in st1.history()]) / nb_iter 
        total_st2 += sum([valeurs[key]*v for (key, v) in st2.history()]) / nb_iter 
    mean_st1 = round(total_st1 / nbMatch, 3)
    mean_st2 = round(total_st2 / nbMatch, 3)
    return mean_st1, mean_st2



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
    m2.actions
    m1.reward_names
    m2.reward_names
    m2.get_actions('T')
    m2.get_actions('A')
    

    
    
