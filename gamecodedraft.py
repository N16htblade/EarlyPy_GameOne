import os
import sys
import random
import csv

with open (os.path.join(sys.path[0], "weaponPool.csv")) as csv_file:   #open and index of all container files:
    csv_reader = csv.reader(csv_file, delimiter=",")
    weaponPool = list(csv.reader(csv_file))

with open (os.path.join(sys.path[0], "armorPool.csv")) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    armorPool = list(csv.reader(csv_file))

with open (os.path.join(sys.path[0], "enemyPool.csv")) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    enemyPool = list(csv.reader(csv_file))

class Player:   #Class that controls player stats, item rolls and encounters.
    def __init__ (self, playerHealth, playerPotion, weaponLevel, weaponName, minDamage, maxDamage, weaponRating, armorLevel, armorName, armorRating, goldBag):  #Initializes the player stats and equipment, updates with new found items.
        self.playerHealth = playerHealth
        self.playerPotion = playerPotion
        self.weaponLevel = weaponLevel
        self.weaponName = weaponName
        self.minDamage = minDamage
        self.maxDamage = maxDamage
        self.weaponRating = weaponRating
        self.armorLevel = armorLevel
        self.armorName = armorName
        self.armorRating = armorRating
        self.goldBag = goldBag
        print (f"\nWelcome to a new adventure. You begin this adventure at {self.playerHealth} HP, equiped with a {self.weaponName} for combat and {self.armorName} for defense.")

    #Initiates search in weapon container.
    def searchForWeapon (self):
        playerLevel = self.weaponLevel + self.armorLevel #identify player level, if too low/negative ignore and use predefined base that enables proggresion.
        if playerLevel < 8:
            minLootPool = 1
            maxLootPool = 4
        elif playerLevel >= 57:
            minLootPool = 26
            maxLootPool = 30 
        else:
            minLootPool = round(playerLevel / 2 - 3)
            maxLootPool = round(playerLevel / 2 + 2)
        lootDrop = random.randint(minLootPool, maxLootPool)
        weaponData = weaponPool[lootDrop][0:5]
        
        #loads new found weapon atributes for check against equiped weapon
        weaponLevel = int(weaponData[0])
        weaponName = weaponData[1]
        minDamage = int(weaponData[2])
        maxDamage = int(weaponData[3])
        goldValue = int(weaponData[4])
        weaponRating = (minDamage + maxDamage) / 2

        #check if found weapon is better or worst then equiped. Swap if yes, sells if no.
        if weaponRating > self.weaponRating:
            self.weaponLevel = weaponLevel
            self.weaponName = weaponName
            self.minDamage = minDamage
            self.maxDamage = maxDamage
            self.weaponRating = weaponRating
            print (f"You found and equiped a {weaponName} ({minDamage} - {maxDamage} damage)!")
        else:
            self.goldBag += goldValue
            print (f"You found {weaponName} and sold it for {goldValue} gold.")

    #Initiates search in Armor container.
    def searchForArmor (self):
        playerLevel = self.weaponLevel + self.armorLevel #identify player level, if too low/negative ignore and use predefined base that aenables proggresion.
        if playerLevel < 8:
            minLootPool = 1
            maxLootPool = 4
        elif playerLevel >= 57:
            minLootPool = 26
            maxLootPool = 30 
        else:
            minLootPool = round(playerLevel / 2 - 3)
            maxLootPool = round(playerLevel / 2 + 2)
        lootDrop = random.randint(minLootPool, maxLootPool)
        armorData = armorPool[lootDrop][0:4]

        #loads new found armor atributes for check against equiped armor
        armorLevel = int(armorData[0])
        armorName = armorData[1]
        armorRating = int(armorData[2])
        goldValue = int(armorData[3])

        #checks if found armor is better or worst then equiped. Swap if yes, sells if no.
        if armorRating > self.armorRating:
            self.armorLevel = armorLevel
            self.armorName = armorName
            self.armorRating = armorRating
            print(f"You found and equiped a new {armorName} ({armorRating} defense)!")
        else:
            self.goldBag += goldValue
            print (f"You found a {armorName} and sold it for {goldValue} gold.")

    #Loads enemy from enemy container.
    def encounter (self):
        playerLevel = self.weaponLevel + self.armorLevel #Checks player level and selects an appropriate enemy.
        if playerLevel < 8: #early game
            minEnemyPool = 1
            maxEnemyPool = 3
        elif playerLevel >= 54 and playerLevel < 60: #end game
            minEnemyPool = 12
            maxEnemyPool = 15
        elif playerLevel == 60: #final boss
            minEnemyPool = 15
            maxEnemyPool = 16
        else:
            minEnemyPool = round(playerLevel / 4 - 1)
            maxEnemyPool = round(playerLevel / 4 + 2)
        enemyDrop = random.randint(minEnemyPool, maxEnemyPool)
        enemyData = enemyPool[enemyDrop][0:4]

        #Loads enemy attributes and communicates encounter to player
        enemyName = enemyData[1]
        enemyHealth = int(enemyData[2])
        enemyDamage = int(enemyData[3])
        print (f"\nAfter walking for a few hours, you encounter {enemyName} with {enemyHealth} HP and {enemyDamage} damage!")
        print (f"You begin this encounter with {self.playerHealth} HP, equiped with {self.weaponName} ({self.minDamage} - {self.maxDamage} Dmg) and {self.armorName} ({self.armorRating} AR).")
        
        #Loads damages and defenses and loops combat while the enemy and the player are alive.
        while enemyHealth > 0 and self.playerHealth > 0:
            attackDamage = random.randint(self.minDamage, self.maxDamage)
            enemyHealth -= attackDamage
            finalDamage = enemyDamage - self.armorRating

            #distributes damage and commnicates events with player
            if enemyHealth > 0:
                print (f"You use {self.weaponName} to deal {attackDamage} damage to {enemyName}! (remaining HP: {enemyHealth})")
                if finalDamage > 0:
                    self.playerHealth -= (enemyDamage - self.armorRating)
                    print (f"{enemyName} attacks you for {finalDamage} damage! (Player remaining HP: {self.playerHealth})")
                else:
                    print (f"{enemyName} strikes back, but can't penetrate your armor.")
            else:
                print (f"You use {self.weaponName} to deal {attackDamage} damage to {enemyName}! (remaining HP: None)")
                if finalDamage > 0:
                    self.playerHealth -= (enemyDamage - self.armorRating)
                    print (f"{enemyName} does one final attack for {finalDamage} damage! (Player remaining HP: {self.playerHealth})")
                else:
                    print (f"{enemyName} does one final attack but can't penetrate your armor.")
        
        #check if player is still alive after combat, if not exit game.
        if self.playerHealth <= 0:
            print ("Your adventure has ended with an unfortunate demise. Game Over.")
        else:
            pass

class GameControls: #Class that contains user controls; Stats, Restore, Combat and Shops.
    def playerStats (): #On request, display player stats to user.
        print (f"\nYou currently have {player1.playerHealth} HP, {player1.playerPotion} health potions, {player1.goldBag} gold, equiped with:")
        print (f"Weapon: {player1.weaponName} ({player1.minDamage} - {player1.maxDamage} damage)")
        print (f"Armor: {player1.armorName} ({player1.armorRating} defense)")

    def restoreHealth ():   #On request, initiate user healing.
        restoreHealth = player1.playerPotion - 1
        setattr (player1, "playerHealth", 100)
        setattr (player1, "playerPotion", restoreHealth)
        print (f"You used 1 health potion to restore back to full health, {player1.playerPotion} potions left.")
    
    def combatEncounter (): #On request, initiate combat encounter, generate new loot after each encounter.
        player1.encounter()
        randomloot = random.randint(1,2)
        if player1.playerHealth > 0:
            if randomloot == 1:
                player1.searchForWeapon()
            else:
                player1.searchForArmor()
        else:
            exit

    def shopEncounter ():   #On request, take user thru various shop options then return to main state.
        print (f"\nYou currently have {player1.goldBag} gold in your pouch; Armor and Weapon shops will require 10 gold to visit and Potions will require 20 gold.")
        playerSearch = input(f"What shop would you like to visit? (Armor, Weapons, Potions, Return): ")
        playerSearch = playerSearch.lower()
        searchCost = player1.goldBag - 10
        potionCost = player1.goldBag - 20

        if playerSearch == "armor" or playerSearch == "a":
            if player1.goldBag > 10:
                player1.searchForArmor()
                setattr (player1, "goldBag", searchCost)
                print (f"You now have {player1.goldBag} gold left.")
            else:
                print (f"Sorry, but you need at least 10 gold to buy new armor, you only have {player1.goldBag} gold available.")
        elif playerSearch == "weapons" or playerSearch == "w":
            if player1.goldBag > 10:
                player1.searchForWeapon()
                setattr (player1, "goldBag", searchCost)
                print (f"You now have {player1.goldBag} gold left.")
            else:
                print (f"Sorry, but you need at least 10 gold to buy a weapon, you only have {player1.goldBag} gold available.")
        elif playerSearch == "potions" or playerSearch == "p":
            if player1.goldBag > 20:
                potions = player1.playerPotion + 1
                setattr (player1, "playerPotion", potions)
                setattr (player1, "goldBag", potionCost)
                print (f"You now have {player1.playerPotion} potions and {player1.goldBag} gold left.")
            else:
                print (f"Sorry, but you need at least 20 gold to buy a potion, you only have {player1.goldBag} gold available.")

        else:
            pass


player1 = Player(100, 3, 0, "Fork", 0, 0, 0, 0, "Robes", 0, 0)  #Initiate player, dificutly can be set from here, see Class player for attributes.
print ("Before you leave on your adventure, your father hands you his old equipment. It's not much, but every little bit helps:") #Provide user with initial items. Tested without and it was a very painful and slow start.
player1.searchForWeapon()
player1.searchForArmor()

#restore point
#player1 = Player(80, 4, 30, "Adamantium Longsword", 15, 15, 15, 30, "Adamantium Vest", 30, 27)  #Initiate player, dificutly can be set from here, see Class player for attributes.

#Main game loop, keeps running while player alive, options are stored in class GameControls.
while player1.playerHealth > 0:
    playerSelection = input("\nWhat would you like to do next? (Player Stats, Restore Health, Shops, Hunt, Instructions, Quit): ")
    playerSelection = playerSelection.lower()
    if playerSelection == "player" or playerSelection == "p":
        GameControls.playerStats()
    elif playerSelection == "restore" or playerSelection == "r":
        GameControls.restoreHealth()
    elif playerSelection == "shops" or playerSelection == "s":
        GameControls.shopEncounter()
    elif playerSelection == "hunt" or playerSelection == "h":
        GameControls.combatEncounter()
    elif playerSelection == "quit" or playerSelection == "q":
        break
    elif playerSelection == "intstructions" or playerSelection == "i":
        print ("\nYou start your adventures with little to nothing in your pockets and your father's old beaten gear from wars past.")
        print ("Your objective is to reach the end of the game and defeat the Demon Lord, or find your demise by reaching 0 HP; whichever comes first.")
        print ("To interact with the game, simply type in the command your character should do next, as showin in paranteses.")
        print ("Shortcuts are also implemented as the 1st letter in each command.")
    else:
        pass