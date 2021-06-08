import discord
import json
from discord.ext import commands
from discord.ext.commands.converter import MessageConverter 

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    def loadEconomy(self):
        with open("./slutprojekt/json/economy.json", "r") as f: # öppnar json fil   
            data = json.load(f)
        return data

    def saveEconomy(self, data):
        with open("./slutprojekt/json/economy.json", "w") as f:    # sparar json fil med datan som man skickar in när man använder funktionen
            json.dump(data, f, sort_keys=True, indent=2)

    def getBalance(self, member, data=None):   # hämtar värdet som en viss person har i json fil, exempel någons pengar
        if data is None: 
            data = self.loadEconomy()
        try:
            memberBalance = data[str(member.id)]
        except:
            if member.bot:
                memberBalance = 0
            else:
                memberBalance = 1000
            data[str(member.id)] = memberBalance
            self.saveEconomy(data)
        finally:
            return memberBalance

    def loadProbability(self):
        with open("./slutprojekt/json/probability.json", "r") as f:
            data = json.load(f)
        return data

    def saveProbability(self, data):
        with open("./slutprojekt/json/probability.json", "w") as f:
            json.dump(data, f, sort_keys=True, indent=2)

    def getProbability(self, prob, data=None):
        if data is None: 
            data = self.loadProbability()
        try:
            memberBalance = data[prob]
        except:
            if prob:
                memberBalance = 0
            else:
                memberBalance = 0
            data[prob] = memberBalance
            self.saveProbability(data)
        finally:
            return memberBalance

    def loadStreak(self):
        with open("./slutprojekt/json/streak.json", "r") as f:
            data = json.load(f)
        return data

    def saveStreak(self, data):
        with open("./slutprojekt/json/streak.json", "w") as f:
            json.dump(data, f, sort_keys=True, indent=2)

    def getStreak(self, member, data=None):
        if data is None: 
            data = self.loadStreak()
        try:
            memberStreak = data[str(member.id)]
        except:
            if member.bot:
                memberStreak = 0
            else:
                memberStreak = 0
            data[str(member.id)] = memberStreak
            self.saveStreak(data)
        finally:
            return memberStreak

    def loadAdmins(self):
        with open("./slutprojekt/json/admins.json", "r") as f:
            data = json.load(f)
        return data

    def saveAdmins(self, data):
        with open("./slutprojekt/json/admins.json", "w") as f:
            json.dump(data, f, sort_keys=True, indent=2)

    def getAdmins(self, member, data=None):
        if data is None: 
            data = self.loadStreak()
        try:
            admins = data[str(member.id)]
        except:
            if member.bot:
                admins = member
            else:
                admins = member
            data[str(member.id)] = admins
            self.saveStreak(data)
        finally:
            return admins

    async def getAmount(self, member, amount, data=None):
        if amount.isdigit():
            amount = round(int(amount))
            bal = self.getBalance(member)
            if bal >= amount:
                if amount == 0:
                    return None
                else:
                    return amount
            else:
                return None
        elif amount.lower() in ("all", "allin"):
            amount = self.getBalance(member)
            if amount == 0:
                return None
            else:
                return amount
        else:
            return None

    async def withdrawMoney(self, member, amount):
        data = self.loadEconomy() 
        bal = self.getBalance(member, data=data)
        if bal >= amount or member.id:
            data[str(member.id)] = int(bal - amount)
            self.saveEconomy(data)
        else:
            raise Exception()

    async def depositMoney(self, member, amount):
        data = self.loadEconomy() 
        bal = self.getBalance(member, data=data)
        data[str(member.id)] = int(bal + amount)
        try:
            self.saveEconomy(data)
        except:
            raise Exception()

    async def addProbability(self, member):
        data = self.loadProbability() 
        prob = self.getProbability(member, data=data)
        data[str(member)] = int(prob) + 1
        try:
            self.saveProbability(data)
        except:
            raise Exception()

    async def resetProbability(self, member):
        data = self.loadProbability() 
        data[str(member.id)] = 0
        try:
            self.saveProbability(data)
        except:
            raise Exception()

    async def addStreak(self, member):
        data = self.loadStreak() 
        streak = self.getStreak(member, data=data)
        data[str(member.id)] = int(streak) + 1
        try:
            self.saveStreak(data)
        except:
            raise Exception()

    async def resetStreak(self, member):
        data = self.loadStreak() 
        bal = self.getStreak(member, data=data)
        data[str(member.id)] = 0
        try:
            self.saveStreak(data)
        except:
            raise Exception()

    async def removeAdmin(self, member):
        try:
            file = json.load(open("./slutprojekt/json/admins.json"))
            file.pop(str(member.id), None)
            json.dump(file, open("./slutprojekt/json/admins.json", "w"))
        except:
            raise Exception()
        #file2 = json.load(open("./slutprojekt/json/admins.json")

    async def addAdmin(self, member):
        data = self.loadAdmins()
        data[str(member.id)] = str(member)
        try:
            self.saveAdmins(data)
        except:
            raise Exception()

    async def setMoney(self, member, amount):
        data = self.loadEconomy() 
        bal = self.getBalance(member, data=data)
        data[str(member.id)] = int(amount)
        try:
            self.saveEconomy(data)
        except:
            raise Exception()

    # Commands
    @commands.command(name="balance", aliases=["bal"], help= "kolla hur mycket pengar du har")
    async def balance(self, ctx):
        bal = self.getBalance(ctx.author) 
        message = f"<@{ctx.author.id}> Your balance is: ${bal}\n"
        if ctx.message.mentions:
            for member in ctx.message.mentions:
                if member == ctx.author: continue
                bal = self.getBalance(member) 
                message = f"{member.name}'s balance is: ${bal}\n"
        await ctx.send(message)

    @commands.command(name="probability", aliases=["prob"], help= "kolla sannolikheten hos ett spel")
    async def probability(self, ctx, *probb):
        prob = self.getProbability("heads") 
        prob2 = self.getProbability("tails")
        prob3 = self.getProbability("rock")
        prob4 = self.getProbability("paper")
        prob5 = self.getProbability("scissors")
        totalcf = self.getProbability("totalcf")
        totalssp = self.getProbability("totalssp")
        try: 
            if str(probb[0]) == "cf":
                await ctx.send(f"The probability for coinflip is: \nHeads: {round((float(prob)/float(totalcf))*100,2)}% Tails: {round((float(prob2)/float(totalcf))*100,2)}% \nBased on {totalcf} games")
            elif str(probb[0]) == "ssp":
                await ctx.send(f"The probability for rock paper scissors is: \nSten: {round((float(prob3)/float(totalssp))*100,2)}% Sax: {round((float(prob5)/float(totalssp))*100,2)}% Påse: {round((float(prob4)/float(totalssp ))*100,2)}% \nBaserat på {totalssp} spel")
        except:
            try:
                await ctx.send(f"The probability for coinflip is: \nHeads: {round((float(prob)/float(totalcf))*100,2)}% Tails: {round((float(prob2)/float(totalcf)*100),2)}% \nBased on {totalcf} games \nThe probability for rock paper scissors is: \nSten: {round((float(prob3)/float(totalssp)*100),2)}% Sax: {round((float(prob5)/float(totalssp)*100),2)}% Påse: {round((float(prob4)/float(totalssp)*100),2)}%  \nBased on {totalssp} games")
            except:
                print("ej några spel spelade")
    
    @commands.command(name="streak", aliases=["s"], help= "kolla din streak")
    async def streak(self, ctx):
        bal = self.getStreak(ctx.author) 
        message = f"<@{ctx.author.id}> Your streak is: {bal}\n"
        if ctx.message.mentions:
            for member in ctx.message.mentions:
                if member == ctx.author: continue
                bal = self.getStreak(member) 
                message = f"{member.name}'s streak is: {bal}\n"
        await ctx.send(message)

    @commands.command(name="balanceall", aliases=["balall"], help= "kolla allas pengar")
    async def balanceall(self, ctx):
        file = json.load(open("./slutprojekt/json/economy.json"))
        msg = ""
        for shits in file.items():
            user = str(f"{shits[0]}")
            user2 = await self.client.fetch_user(user)
            msg +=  str(user2) + ":   " + f"{shits[1]}\n"
        await ctx.send("Everybodys balance:\n" + msg)

    @commands.command(name="streakall", aliases=["strall"], help= "kolla allas streak")
    async def streakall(self, ctx):
        file = json.load(open("./slutprojekt/json/streak.json"))
        msg = ""
        for shits in file.items():
            userr = str(f"{shits[0]}")
            user2 = await self.client.fetch_user(userr)
            msg +=  str(user2) + ":   " + f"{shits[1]}\n"
        await ctx.send("Everybodys streak:\n" + msg)

    @commands.command(name="take", aliases=["t"], enabled=True, help= "ta pengar från någon")
    async def take(self, ctx, amount):
        file = json.load(open("./slutprojekt/json/admins.json"))
        if str(ctx.author) in list(file.values()):
            bal = self.getBalance(ctx.author) 
            try:
                bal2 = self.getBalance(ctx.message.mentions[0])
            except:
                pass
            try:
                if int(bal2) < int(amount):
                    await ctx.send("Not enough money")
                    return
            except:
                if int(bal) < int(amount):
                    await ctx.send("Not enough money")
                    return
            try:
                await self.withdrawMoney(ctx.message.mentions[0], int(amount))
                print("took $" + str(amount) + " from " + str(ctx.message.mentions[0])[:-5])
                await ctx.send("took $" + str(amount) + " from " + str(ctx.message.mentions[0])[:-5])
            except:
                await self.withdrawMoney(ctx.author, int(amount))
                print("took $" + str(amount) + " from " + str(ctx.author)[:-5])
                await ctx.send("took $" + str(amount) + " from " + str(ctx.author)[:-5])
        else:
            await ctx.message.add_reaction("👎")
            await ctx.message.add_reaction("🚫")
            await ctx.send("Not authorized")
            
    @commands.command(name="admins", enabled=True, help= "visa alla admins")
    async def admins(self, ctx):
        file = json.load(open("./slutprojekt/json/admins.json"))
        msg = ""
        for value in file.values():
            msg += f"{value}\n"
        await ctx.send("Current admins:\n" + msg)

    @commands.command(name="addadmin", aliases=["aa"], enabled=True, help= "lägg till en admin")
    async def addadmin(self, ctx):
        file = json.load(open("./slutprojekt/json/admins.json"))
        if str(ctx.author) in list(file.values()):
            await self.addAdmin(ctx.message.mentions[0])
            await ctx.send("Added " + str(ctx.message.mentions[0]) + " to admins")
            print("Added " + str(ctx.message.mentions[0]) + " to admins")
        else:
            await ctx.message.add_reaction("👎")
            await ctx.message.add_reaction("🚫")
            await ctx.send("Not authorized")

    @commands.command(name="removeadmin", aliases=["ra"], enabled=True, help= "ta bort en admin")
    async def removeadmin(self, ctx):
        file = json.load(open("./slutprojekt/json/admins.json"))
        if str(ctx.author) in list(file.values()):
            await self.removeAdmin(ctx.message.mentions[0])
            await ctx.send("Removed " + str(ctx.message.mentions[0]) + " from admins")
            print("Removed " + str(ctx.message.mentions[0]) + " from admins")
        else:
            await ctx.message.add_reaction("👎")
            await ctx.message.add_reaction("🚫")
            await ctx.send("Not authorized")

    @commands.command(name="takeall", aliases=["ta"], enabled=True, help= "ta alla pengar från någon")
    async def takeall(self, ctx):
        file = json.load(open("./slutprojekt/json/admins.json"))
        if str(ctx.author) in list(file.values()):
            try:
                bal = self.getBalance(ctx.message.mentions[0])
                await self.withdrawMoney(ctx.message.mentions[0], int(bal))
                print("took $" + str(bal) + " from " + str(ctx.message.mentions[0])[:-5])
                await ctx.send("took $" + str(bal) + " from " + str(ctx.message.mentions[0])[:-5])
            except:
                bal = self.getBalance(ctx.author)
                await self.withdrawMoney(ctx.author, int(bal))
                print("took $" + str(bal) + " from " + str(ctx.author)[:-5])
                await ctx.send("took $" + str(bal) + " from " + str(ctx.author)[:-5])
        else:
            await ctx.message.add_reaction("👎")
            await ctx.message.add_reaction("🚫")
            await ctx.send("Not authorized")

    @commands.command(name="add", aliases=["a"], enabled=True, help= "lägg till pengar till någon")
    async def add(self, ctx, amount):
        file = json.load(open("./slutprojekt/json/admins.json"))
        if str(ctx.author) in list(file.values()):
            try:
                await self.depositMoney(ctx.message.mentions[0], int(amount))
                print("added $" + amount + " to " + str(ctx.message.mentions[0])[:-5])
                await ctx.send("added $" + str(amount) + " to " + str(ctx.message.mentions[0])[:-5])
            except:
                await self.depositMoney(ctx.author, int(amount))
                print("added $" + amount + " to " + str(ctx.author)[:-5])
                await ctx.send("added $" + str(amount) + " to " + str(ctx.author)[:-5])
        else:
            await ctx.message.add_reaction("👎")
            await ctx.message.add_reaction("🚫")
            await ctx.send("Not authorized")

    @commands.command(name="give", aliases=["g"], help= "ge andra dina pengar")
    async def give(self, ctx, amount):
        amount = await self.getAmount(ctx.author, amount)
        print(amount)
        if amount is not None and len(ctx.message.mentions) == 1:
            if ctx.message.mentions[0].bot:
                await ctx.message.add_reaction("👎")
                return
            try: 
                await self.withdrawMoney(ctx.author, amount)
            except:
                await ctx.message.add_reaction("👎")
            else:
                try:
                    await self.depositMoney(ctx.message.mentions[0], amount)
                    print("edfg")
                    await ctx.send(str(ctx.author) + " gave $" + str(amount) + " to " + str(ctx.message.mentions[0])[:-5])
                    

                except:
                    await self.depositMoney(ctx.author, amount)
        else:
            await ctx.message.add_reaction("👎")

    @commands.command(name="setbalance", aliases=["sb"], help= "sätt en persons belopp till något")
    async def setbalance(self, ctx, amount):
        admins = ["Ekan#6657", "Mikty#6569"]
        if str(ctx.author) in admins:
            try:
                await self.setMoney(ctx.message.mentions[0], int(amount))
                print("set " + str(ctx.message.mentions[0])[:-5] + "'s balance to $" + amount)
                await ctx.send("set " + str(ctx.message.mentions[0])[:-5] + "'s balance to $" + str(amount))
            except:
                await self.setMoney(ctx.author, int(amount))
                print("set " + str(ctx.author)[:-5] + "'s balance to $" + amount)
                await ctx.send("set " + str(ctx.author)[:-5] + "'s balance to $" + str(amount))
        else:
            await ctx.message.add_reaction("👎")
            await ctx.message.add_reaction("🚫")
            await ctx.send("Not authorized")
    
def setup(client):
    client.add_cog(Economy(client))