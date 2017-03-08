###COMBINATORIAL GAME THEORY MODULE###

from math import ceil
from math import floor
from fractions import Fraction

#COMBINATORIAL GAMES AS A CLASS:
class Game:
    def __init__(self):
        self.left_set = []
        self.right_set = []
        self.value = None

    ##COMPARISON OF GAMES (BY MATHEMATICAL DEFINITION):
    def __ge__(self,other):
        for G_R in self.right_set:
            if other >= G_R:
                return False
        for H_L in other.left_set:
            if H_L >= self:
                return False
        return True

    def __le__(self,other):
        if other >= self:
            return True
        return False

    def __lt__(self,other):
        if self <= other and not self >= other:
            return True
        return False

    def __gt__(self,other):
        if other < self:
            return True
        return False

    def __eq__(self,other):
        if self >= other and self <= other:
            return True
        return False

    ##FINDING CANONICAL FORM OF A GAME:
    def removeDominated(self): #Remove dominated options
        new_left_set = []
        for option in self.left_set:
            for option2 in self.left_set:
                if option < option2:
                    break
            else:
                if option not in new_left_set:
                    new_left_set.append(option)
        self.left_set = new_left_set

        new_right_set = []
        for option in self.right_set:
            for option2 in self.right_set:
                if option > option2:
                    break
            else:
                if option not in new_right_set:
                    new_right_set.append(option)
        self.right_set = new_right_set

    
    def replaceReversible(self): #Replace reversible options
        new_left_set = []
        for G_L in self.left_set:
            for G_LR in G_L.right_set:
                if G_LR <= self: #G_L is reversible through G_LR
                    for G_LRL in G_LR.left_set:
                        if G_LRL not in new_left_set:
                            new_left_set.append(G_LRL)
                    break
            else: #Not reversible
                if G_L not in new_left_set:
                    new_left_set.append(G_L)
        self.left_set = new_left_set
        
        new_right_set = []
        for G_R in self.right_set:
            for G_RL in G_R.left_set:
                if G_RL >= self: #G_R is reversible through G_RL
                    for G_RLR in G_RL.right_set:
                        if G_RLR not in new_right_set:
                            new_right_set.append(G_RLR)
                    break
            else: #Not reversible
                if G_R not in new_right_set:
                    new_right_set.append(G_R)
        self.right_set = new_right_set

    def canonicalize(self): #Canonicalizes a game
        self.removeDominated()
        for G_L in self.left_set:
            G_L.canonicalize()
        for G_R in self.right_set:
            G_R.canonicalize()
        self.replaceReversible()  
        self.value = self.evaluate()
        return(self)
        
    #DETERMINE THE VALUE OF A GAME:
    def evaluate(self):
        gameform = '{'
        for i in range(len(self.left_set)):
            gameform += self.left_set[i].evaluate()
            if not i == len(self.left_set)-1:
                gameform += ', '
        gameform += ' | '
        for i in range(len(self.right_set)):
            gameform += self.right_set[i].evaluate()
            if not i == len(self.right_set)-1:
                gameform += ', '
        gameform += '}'

        ##Different notation for special games:
        if gameform == '{ | }' or gameform == '0':
            gameform = '0'
        elif gameform == '{0 | 0}' or gameform == '*':
            gameform = '*'
        elif gameform == '{0 | *}' or gameform == '^':
            gameform = '^'
        elif gameform == '{* | 0}' or gameform == 'v':
            gameform = 'v'
        elif gameform == '{0, * | 0}' or gameform == '{*, 0 | 0}' or gameform == '^*':
            gameform = '^*'
        elif gameform == '{0 | *, 0}' or gameform == '{0 | 0, *}' or gameform == 'v*':
            gameform = 'v*'
    
        ##Nimbers
        elif self.checkImpartial():
            i = 1
            nimbers = []
            while True:
                new_nimber = Game()
                for nimber in nimbers:
                    new_nimber.leftAdd(nimber)
                    new_nimber.rightAdd(nimber)
                nimbers.append(new_nimber)
                for option in self.left_set:
                    if option not in nimbers:
                        break
                else:
                    gameform = '*'+str(i)
                    break
                i += 1
                if i == 10: #Gone too far without success
                    break

        elif self.isANumber():
            #Integer
            if self.right_set == [] and self.left_set == []:
                gameform = '0'
            elif self.right_set == [] and not self.left_set == []:
                n = float(self.left_set[0].value)+1
                gameform = str(floor(n))
            elif self.left_set == [] and not self.right_set == []:
                n = float(self.right_set[0].value)-1
                gameform = str(ceil(n))
            #Dyadic rational: NOT YET COMPLETE, AVOID RATIONALS!
            else:
##                print('Trying to evaluate dyadic rational')
##                print(self.sequence)
##                print('isANumber: ' + str(self.isANumber()))
##                print('Left set:')
##                for G_L in self.left_set:
##                    print(G_L)
##                print('Right set:')
##                for G_R in self.right_set:
##                    print(G_R)
                
                x = float(self.left_set[0].value)
                y = float(self.right_set[0].value)
                gameform = str((x+y)/2)
                
                  
        self.value = gameform
        return(gameform)

    ##CHECK IF A GAME IS IMPARTIAL:
    def checkImpartial(self):
        zero = Game()
        if self == zero:
            return(True)
        elif self.left_set == self.right_set:
            for G in self.left_set:
                if G.checkImpartial() == True:
                    return(True)
        return(False)

    ##CHECK IF A GAME IS A NUMBER:
    def isANumber(self):
        for G_L in self.left_set:
            if not G_L.isANumber():
                return(False)
        for G_R in self.right_set:
            if not G_R.isANumber():
                return(False)
        
        for G_L in self.left_set:
             for G_R in self.right_set:
                if G_L < G_R:
                    continue
                else:
                    return(False)
        return(True)

    ##PRINT GAMES AS STRINGS:
    def __str__(self):
        form = self.evaluate()
        try:
            return(str(Fraction(float(form))))
        except ValueError:
            return(form)

    ##SUM OF GAMES (FROM MATHEMATICAL DEFINITION):
    def __add__(self,other):
        gamesum = Game()
        for G_L in self.left_set:
            option = G_L + other
            if option not in gamesum.left_set:
                gamesum.left_set.append(option)
        for H_L in other.left_set:
            option = self + H_L
            if option not in gamesum.left_set:
                gamesum.left_set.append(option)
        for G_R in self.right_set:
            option = G_R + other
            if option not in gamesum.right_set:
                gamesum.right_set.append(option)
        for H_R in other.right_set:
            option = self + H_R
            if option not in gamesum.right_set:
                gamesum.right_set.append(option)
        return gamesum

    ##NEGATIVE OF A GAME AND SUBTRACTION OF GAMES:
    def __neg__(self):
        minus_G = Game()
        for G_L in self.left_set:
            minus_G.rightAdd(-G_L)
        for G_R in self.right_set:
            minus_G.leftAdd(-G_R)
        return(minus_G)

    def __sub__(self,other):
        return self+(-other)

    ##MANIPULATE LEFT AND RIGHT SETS:
    def leftAdd(self,G_L): #Add left option
        if G_L not in self.left_set:
            self.left_set.append(G_L)

    def rightAdd(self,G_R): #Add right option
        if G_R not in self.right_set:
            self.right_set.append(G_R)
