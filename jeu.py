import json
import random
from typing import Dict
from unidecode import unidecode as decode
import discord
import os
import sqlite3


class MauvaisIndice(Exception):
    pass

class jeu:
    niveauMax = 0
    niveau = 0
    nbTours = 1
    scores = {"joueur": "score"}
    tourNumero = 0
    tourCommence = False
    partieCommencee = False
    partieEnPrepOuCommencee = False
    country_name: str
    countries_picked=[]

    def decode(self, mot):
        return decode(mot).lower()

    def reset(self):
        self.__init__(1, 1, 0, {}, False, False, False, "",[])

    async def prochainTourOuFin(self, message, json_flag):
        if self.tourNumero < self.nbTours:
            self.country_name = self.pickCountry()
            while self.country_name in self.countries_picked:
                self.country_name = self.pickCountry()
            self.countries_picked.append(str(self.country_name))
            print(self.countries_picked)
            print("New country : ",self.country_name)

            file=discord.File("D:/CODING/DISCORD BOT/Bot/Images/"+self.country_name, filename=self.country_name)      
            flag=discord.Embed(
                title=f"Guess the Country -- {self.tourNumero} rounds over {self.nbTours}",
                description="Be quick, otherwise your opponent might win :)",
                colour=discord.Colour.green()
            )
            flag.set_image(url='attachment://'+self.country_name)
            await message.channel.send(embed=flag,file=file)
            """
            file=discord.File("D:/CODING/DISCORD BOT/Bot/Images/"+self.country_name, filename=self.country_name) 
            flag=discord.Embed(
                title="What happened you guys? Cmon **wake up**",
                description="Be quick, otherwise your opponent might win :)",
                colour=discord.Colour.green()
            )
            flag.set_image(url='attachment://'+j.country_name)
            await message.channel.send(embed=flag,file=file)
            """
            self.tourNumero += 1
            self.tourCommence = True
            json_flag[0][str(message.guild.id)]["flag_game"][message.channel.id] = (
                int(self.niveau), int(self.nbTours), int(self.tourNumero), self.scores, True, True, True, self.country_name,self.countries_picked)
            json.dump(json_flag, open('flag-info.json', 'w'), indent=2)

        else:
            self.scores = {k: v for k, v in sorted(self.scores.items(), key=lambda item: item[1], reverse=True)}
            DIR = os.path.dirname(__file__)
            db = sqlite3.connect(os.path.join(DIR, "BankAccounts.db"))
            SQL = db.cursor()
            embed = discord.Embed(title="End of game", description= "Round " + str(self.tourNumero) + " Done ", color=0x4169e1)
            if len(self.scores) > 0:


                v = list(self.scores.values())
                print(v)
                maxScore = max(v)
                print(self.scores)
                print("maxScore : ", maxScore)

                for i in self.scores:
                    print(i, "and",self.scores[i])

                    embed.add_field(name=(":crown: " if self.scores[i] == maxScore else "") + "%s" % i,
                                    value=str(self.scores[i]) + " Point" + ("s" if self.scores[i] != 1 else ""),
                                    inline=True)
                    
                    
                    
                    await message.channel.send(f'During this game, we have added {self.scores[i]} to your account, {str(i)}')
            else:
                embed.add_field(name="No winner...", value="Oopsee", inline=True)
            SQL.execute('update Accounts set advice1 = 0') 
            db.commit()
            SQL.execute('update Accounts set advice2 = 0')
            db.commit()
            await message.channel.send(embed=embed)
            print("End of game",self.countries_picked)
            self.reset()
            json_flag[0][str(message.guild.id)]["flag_game"][message.channel.id] = (1, 1, 0, {}, False, False, False, "",[])
            json.dump(json_flag, open('flag-info.json', 'w'), indent=2)

    def getAttributes(self):
        return [self.niveau, self.nbTours, self.tourNumero, self.scores, self.tourCommence,
                self.partieCommencee, self.partieEnPrepOuCommencee, self.country_name,self.countries_picked]
    def __init__(self, niveau, nbTours, tourNumero, scores, tourCommence, partieCommencee,
                 partieEnPrepOuCommencee, country_name, countries_picked):
        self.setNiveauMax()
        self.setNiveau(niveau)
        self.nbTours = nbTours
        self.scores = scores
        self.tourNumero = tourNumero
        self.tourCommence = tourCommence
        self.partieCommencee = partieCommencee
        self.partieEnPrepOuCommencee = partieEnPrepOuCommencee
        self.country_name = country_name
        self.countries_picked=countries_picked

    def leaderboard(self):
        return self.scores
    
    def pickCountry(self):
        return random.choice(os.listdir("D:\\CODING\\DISCORD BOT\\Bot\\Images\\"+str(self.niveau)))
    
    def maxTours(self):
        directory = 'D:\\CODING\\DISCORD BOT\\Bot\\Images\\'+str(self.niveau)
        number_of_files = len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])
        return number_of_files

    def setNiveauMax(self):
        self.niveauMax = 4

    def setNiveau(self, niveau):
        if niveau not in range(0, self.niveauMax + 1):
            raise MauvaisIndice('Erreur : niveau demandé pas un entier entre 1 et %i' % self.niveauMax)
        else:
            self.niveau = niveau
    
    
    def __str__(self):
        return "Number of Rounds : %s. Current Round: %i. Level : %s." % (self.nbTours, self.tourNumero, self.niveau)
    def addPlayer(self, nom):
        self.scores[nom] = 0