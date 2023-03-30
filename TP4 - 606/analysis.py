# analysis.py
# -----------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

# Explication des choix de paramètres pour 2a et 2b
# Pour que la politique préfère la case +1, le facteur d'escompte ne doit pas être élevé, sinon il va préférer la case +10.
# Le bruit peut fausser la politique s'il est trop élevé, grand risque de tomber dans la falaise.
# Dans les deux cas, la récompse doit être négative : 
#  - Pour que la politique préfère la case +1, la récompense est plus petite pour passer par le chemin le plus court.
#  - Pour que la politique préfère la case +10, la récompense est plus grande afin que le chemin long soit moins pénalisant.

def question2a():
    answerDiscount = 0.5
    answerNoise = 0.2
    answerLivingReward = -4
    return answerDiscount, answerNoise, answerLivingReward

def question2b():
    answerDiscount = 0.5
    answerNoise = 0.2
    answerLivingReward = -1
    return answerDiscount, answerNoise, answerLivingReward

# Explication des choix de paramètres pour 2c et 2d
# Afin que la politique préfère la plus grande récompense (+10), il faut un facteur d'escompte plus grand.
# Dans quel cas la récompense future a plus d'importance.
# Le bruit ne doit pas être trop élevé pour ne pas fausser la politque.
# Récompense :
#  - Pour risquer la falaise, la récompense doit être négative, sinon il l'évitera.
#  - Pour éviter la falaise, la récompense doit être neutre.

def question2c():
    answerDiscount = 0.99
    answerNoise = 0.1
    answerLivingReward = -1
    return answerDiscount, answerNoise, answerLivingReward

def question2d():
    answerDiscount = 0.99
    answerNoise = 0.1
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward

# Explication des choix de paramètres pour 2e
# Le facteur d'escompte doit être faible afin que la politique préfère les récompenses immédiates.
# Le bruit n'a pas d'importance.
# La récompense peut être négative, neutre ou positive. Tant qu'elle n'est pas trop négative, sinon la politique ira vers les cases récompenses.

def question2e():
    answerDiscount = 0.001
    answerNoise = 0.5
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
