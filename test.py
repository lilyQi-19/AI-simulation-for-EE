import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Player import Player
from Enemy import Enemy

import torch
import torch.nn as nn
import torch.utils
import torch.nn.functional as F
# import torch.optim as optim
# from torch.distributions import Categorical

# the basic input of the enemy at the start
health = 5
damage = 5
intelligence = 3
attackSpace = 4

# change parameter: no more then 1. 

# AI can give health to player
for i in range(3):
    player = Player(i,random.randint(1,10), random.randint(1,10), random.randint(1,5))
    print(i)
    for j in range(20):
        health=random.randint(3,8)
        damage=random.randint(3,20)
        intelligence=random.randint(1,8)
        attackSpace=random.randint(2, 6)
        enemy = Enemy(health,damage,intelligence,attackSpace)
        player.faceEmeny(enemy,0)
        print('ehealth:', str(health), 'damage:', str(damage),'intelligence:', str(intelligence),'attack Space:', str(attackSpace))       
        print('count:', str(player.enemyCount),  'health:', str(player.health), 'time:', str(player.time), str(player.learn), str(player.death))
        print()
        # 'hit:', str(player.hit),'dodge:', str(player.dodge),'speed:', str(player.speed),
        # print('level:', str(player.difficulty()))
        
    
    