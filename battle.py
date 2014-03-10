import sys, random, os

class Monster(object):
    exp = 0
    level = 1
    decay = 0

    def __init__(self, name, atk, arm, hp, spec, nextLevel, regen):
        self.name = name
        self.HP = hp
        self.atk = atk
        self.armor = armor
        self.spec = spec
        self.maxHP = hp
        self.nextLevel = nextLevel    
        self.regen = regen

    def attack(self, opp):
        damage = random.randint(10, 18)
        damage += self.atk
        opp.defend(damage)

    def specAttack(self, opp):
        damage = random.randint(3, 25)
        damage += self.spec
        if damage < 10 or damage > 25:
            opp.decay += self.spec / 2
        opp.defend(damage)

    def defend(self, damage):
        damage /= self.armor
        hp = self.HP
        self.HP = max(0, self.HP - damage)
        print("%s lost %s HP!" % (self.name,round( hp - self.HP, 1)))

    def heal(self):
        heal = random.randint(5, 20)
        heal += max(1, self.spec)
        hp = self.HP
        self.HP = min(self.maxHP, self.HP + heal)
        print("%s healed %s HP." % (self.name, round(self.HP - hp, 1)))

    def addExp(self, exp):
        self.exp += exp
        if self.exp >= self.nextLevel:
            self.levelUp()

    def levelUp(self):
        self.level += 1
        self.maxHP += 5
        self.armor = round(self.armor + 0.1, 1)
        self.atk = round(self.atk + 0.1, 1)
        print("%s reached level %s" % (self.name, self.level))
        print("Stats: ")
        if self.level % 5 == 0:
            self.evolve()
        elif self.level % 7 == 0:
            self.regen += 0.5
            self.spec += 0.5
        self.nextLevel = round(self.nextLevel + self.nextLevel / 2)
        print(self.stats())

    def evolve(self):
        invalidChoice = True
        while invalidChoice:
            print("1. Greater attack power")
            print("2. Stronger armor")
            print("3. Poison arrows")
            print("4. Health regeneration")
            print("5. More Health Points")
            powerup = int(input("Choose your powerup: "))
            if powerup in range(1,6):
                invalidChoice = False
                if powerup == 1:
                    self.atk = 3
                elif powerup == 2:
                    self.armor += 3
                elif powerup == 3:
                    self.spec += 1
                elif powerup == 4:
                    self.regen += 1
                elif powerup == 5:
                    self.maxHP += 5
                print()
                print(self.stats())

    def suffer(self):
        hp = self.HP
        self.HP = max(0, self.HP - self.decay)
        dif = self.HP - hp
        if self.decay > 10:
            print("%s was greatly hurt by poison. (%sHP)" % (self.name, dif))
        elif self.decay > 5:
            print("%s was hurt by poison. (%sHP)" % (self.name, dif))
        elif self.decay > 0:
            print("%s is suffering from poison. (%sHP)" % (self.name, dif))
        

    def stats(self):
        return "--------------------\n HP: %s\n ATK: %s\n DEF: %s\n SPEC: %s\n REGEN: %s\n EXP: %s\%s\n--------------------" % (self.maxHP, self.atk, self.armor, self.spec, self.regen, self.exp, self.nextLevel)

def clear_console():
    print("\n\n")
    print("%s: %s HP" % (opponent.name, round(opponent.HP, 1)))
    print("%s: %s HP" % (player.name, round(player.HP, 1)))
    print("--------------------")

def turn():
    clear_console()
    player.suffer()

    print("1. Attack")
    print("2. Heal")
    print("3. Spec. Attack")
    command = int(input("Pick a move: "))
    if command not in range(1, 4):
        turn()
    else:
        if command == 1:
            player.attack(opponent)
        elif command == 2:
            player.heal()
        elif command == 3:
            player.specAttack(opponent)
        
def ai_turn():
    opponent.suffer()
    heal = random.randint(1, 10) >= random.randint(1, 10)
    if opponent.HP / opponent.maxHP < 0.3 and heal:
        opponent.heal()
    elif player.HP > 67 and opponent.spec > 2:
        opponent.specAttack(player)
    else:
        opponent.attack(player)

hp = 100
atk = 1.0
armor = 1.0
spec = 0.0
regen = 0.0
monsters_slain = 0

opponent = Monster("Bobtimus Prime", 1, 1, 100, 0, 0, 0)
name = input("Your name: ")
player   = Monster(name, 1.0, 1.0, 125.0, 0.0, 20.0, 0)
while True:
    turn()
    if opponent.HP == 0:
        player.addExp(10)
        monsters_slain += 1
        print("Opponent #%s slain!" % monsters_slain)
        if monsters_slain % 5 == 0:
            atk += 0.2
            armor += 0.2
        if monsters_slain % 8 == 0:
            hp += 5
        if monsters_slain % 10 == 0:
            spec += 0.5
            regen += 0.5
        opponent = Monster("B. Prime", atk, armor, hp, spec, 0, regen)
        player.HP = player.maxHP
        turn()

    ai_turn()
    if player.HP == 0:
        print("Game Over!")
        print("You reached level %s by slaying %s monsters!" % (player.level, monsters_slain))
        break
