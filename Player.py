import random

class Player:
    def __init__(self, hit, dodge, speed):
        # skill when player reach learning phase
        self.hit = hit
        self.dodge = dodge
        self.speed = speed
        # health as a percentage
        self.health = 100
        self.healthChange = 0
        self.death = False
        self.time = 0 #time taken to win
        self.enemyCount = 0
        self.learn = True

    def faceEmeny(self, enemy,regen):
        if regen:
            self.health = min(100, self.health + regen)
        self.time = 0
        self.death = False
        self.healthChange = self.health
        hitRate = self.hit
        dodgeRate = self.dodge
        speed = self.speed

        # check if player is in lerning phase
        if self.learn:
            hitRate = min(self.enemyCount + 1, hitRate)
            dodgeRate = min(self.enemyCount + 1, dodgeRate)
            speed = max(10-(self.enemyCount * 2), speed)
        if self.enemyCount > max(hitRate,dodgeRate,speed):
            self.learn = False
            
        # chance that player didn't do will/did extremely well
        if not self.learn:
            if random.randint(1,5) == 1:
                self.hit = min(10, self.hit + 1)
            elif random.randint(1,10) == 1:
                self.hit = max(1, self.hit - 1)
            if random.randint(1,5) == 1:
                self.dodge = min(10, self.dodge + 1)
            elif random.randint(1,10) == 1:
                self.dodge = max(1, self.dodge - 1)
            if random.randint(1,5) == 1:
                self.speed = max(1, self.speed - 1)
            elif random.randint(1,10) == 1:
                self.speed = self.speed + 1

        self.enemyCount += 1
        while True:
            self.time += 1
            
            # check damage
            if self.time % enemy.attackSpace == 0:
                chance = dodgeRate if self.health > 30 else min(dodgeRate + 1, 10)
                # chance of player dodge the attack
                if random.randint(1, enemy.intelligence * 2) > chance:
                    self.health = self.health - enemy.damage
            
            # player attack enemy
            if self.time % speed == 0:
                chance = hitRate if self.health > 30 else max(hitRate - 1, 1)
                if random.randint(1,enemy.intelligence*2) <= chance:
                    enemy.health -= 1
            

            # check if player or enemy have died
            if self.health <= 0:
                self.death = True
                self.health = 100
                break

            if enemy.health <= 0:
                break

        self.healthChange = self.healthChange - self.health
        if self.healthChange <= 0:
            self.healthChange += 100
            


    def reward(self):
        # calculate difficulty from 1 (easy) to 10 (hard)
        # aim to keep it between 4 ~ 6
        # long term
        level = 5 

        if self.death: 
            level += 1
            if self.healthChange < 20:
                if self.time < 10:
                    level += 1
                elif self.time > 50:
                    level -= 1
            elif self.healthChange < 60:
                if self.time < 20:
                    level += 2
                elif self.time < 50:
                    level += 1
            else:
                if self.time < 40:
                    level += 2
                elif self.time < 80:
                    level += 1
        else:
            if self.healthChange < 20:
                level += 1
            elif self.healthChange >50:
                level -= 1
            if self.time < 20:
                level += 1
            elif self.time > 80:
                level += 2
            elif self.time > 50:
                level += 1
        
        if level >= 8 or level <= 2:
            return -2
        elif level > 6 or level < 4:
            return -1
        else: 
            return 1
        
        
        
        
