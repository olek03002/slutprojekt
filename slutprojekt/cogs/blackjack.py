import random
from datetime import datetime, timezone
import discord
from discord.ext import commands

def deal(deck):
    hand = []
    for i in range(2):
        random.shuffle(deck)
        card = deck.pop()
        hand.append(card)
    return hand

Ace = 0

class blackjack(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name= "jack", aliases=["j", "blackjack"], help= "spela blackjack bet/no bet",  case_insensitive=True)
    async def jack(self, ctx, *bet):
        economy = self.client.get_cog("Economy") 
        saldo = economy.getBalance(ctx.author) # min balans
        try: 
            if str(bet[0]) == "all":
                bet = int(saldo)
            else:
                bet = int(bet[0])
        except:
            bet = 0
        if int(bet) > saldo:
            await ctx.send("Not enough money")
            await ctx.message.add_reaction("👎")
            return
        await economy.withdrawMoney(ctx.author, int(bet))
        kort = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, "Ace"]*4 #hela kortleken
        dealer = deal(kort) # dealern tar ett kort
        player = deal(kort) # spelaren tar ett kort
        print(player, dealer)
       
        if "Ace" in player or "Ace" in dealer:
            try:
                player.remove("Ace")
                player.append(11)
            except:
                pass
            try:
                dealer.remove("Ace")
                dealer.append(11)
            except:
                pass
            try:
                player.remove("Ace")
                player.append(11)
            except:
                pass
            try:
                dealer.remove("Ace")
                dealer.append(11)
            except:
                pass
       
        if sum(dealer) == 21 and sum(player) == 21:
            if bet == 0:
                await ctx.send(ctx.message.author.mention + "\nBoth got blackjack!")
            else:
                await ctx.send(ctx.message.author.mention + "\nBoth got blackjack! \nBet returned")
            await economy.depositMoney(ctx.author, bet)
            return
        if sum(dealer) == 21:
            if bet == 0:
                await ctx.send(ctx.message.author.mention + "\nDealer got blackjack!")
            else:
                await ctx.send(ctx.message.author.mention + "\nDealer got blackjack! \nLost bet of $" + str(bet))
            return
        if sum(player) == 21:
            vinst = int(bet)*2.5
            if bet == 0:
                await ctx.send(ctx.message.author.mention + "\nYou got blackjack!")
            else:
                await ctx.send(ctx.message.author.mention + "\nYou got blackjack! \nBet x2.5  Won: $" + str(vinst))
            await economy.depositMoney(ctx.author, vinst)
            return

        print(player, dealer)

        if (sum(player) > 21):
            try:
                player.remove(11)
                player.append(1)
            except:
                pass
        if bet == 0:
            await ctx.send(ctx.message.author.mention + "\nThe dealer has a " + str(dealer[0]) + " \nYou have  "+ str(player) + "  Total: " + str(sum(player)) + "\nNo bet" + "\nYour move: stand, hit, split or double?")
        else:
            await ctx.send(ctx.message.author.mention + "\nThe dealer has a " + str(dealer[0]) + " \nYou have  "+ str(player) + "  Total: " + str(sum(player)) + "\nBet: $" + str(bet) + "\nYour move: stand, hit, split or double?")
        
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author and m.content in ["stand", "hit", "split", "double"]

        try:
            msg = await self.client.wait_for("message", timeout=30.0, check=check)
        except:
            await ctx.send("Timed out!")

        msg.content =  msg.content.lower()

        if msg.content == "double":
            saldo = economy.getBalance(ctx.author)
            if int(saldo)+int(bet) >= int(bet)*2:
                player.append(kort.pop())
                if bet != 0:
                    await ctx.send("Doubled bet: $" + str(int(bet)*2))
                bet = str(int(bet)*2)
                if 11 in player:
                    if (sum(player) > 21):
                        player.remove(11)
                        player.append(1)
                print(player, dealer)
            else:
                await ctx.send("Not enough money, returned bet\nPlay again")
                await economy.depositMoney(ctx.author, int(bet))
                return
                
        
        elif msg.content.lower() == "hit" or "stand":
            while True:
                
                if msg.content.lower() == "stand":
                    break

                if msg.content.lower() == "hit":
                    player.append(kort.pop())
                    if 11 or "Ace" in player:
                        try:
                            player.remove("Ace")
                            player.append(11)
                        except:
                            pass
                        if (sum(player) > 21):
                            try:
                                player.remove(11)
                                player.append(1)
                            except:
                                pass
                        
                print(player, dealer)
                
                if sum(player) == 21:
                    break

                await ctx.send(ctx.message.author.mention + "\nYour hand:  " + str(player) + "   Total: " + str(sum(player)))

                if sum(player) > 21:
                    if bet == 0:
                        await ctx.send("Busted")
                    else:
                        await ctx.send("Busted, you lost bet of: $" + str(bet))
                    return

                try:
                    msg = await self.client.wait_for("message", timeout=30.0, check=check)
                except:
                    await ctx.send("Timed out!")
                    if bet != 0:
                        await ctx.send("Bet returned")
                    await economy.depositMoney(ctx.author, int(bet))

        while True:
            if sum(dealer) >= 17:
                break
            dealer.append(kort.pop())
            print(player, dealer)
            if 11 or "Ace" in dealer:
                try:
                    dealer.remove("Ace")
                    dealer.append(11)
                except:
                    pass
                if (sum(dealer) > 21):
                    try:
                        dealer.remove(11)
                        dealer.append(1)
                    except:
                        pass
                try:
                    dealer.remove("Ace")
                    dealer.append(11)
                except:
                    pass
                if (sum(dealer) > 21):
                    try:
                        dealer.remove(11)
                        dealer.append(1)
                    except:
                        pass
                try:
                    dealer.remove("Ace")
                    dealer.append(11)
                except:
                    pass
                if (sum(dealer) > 21):
                    try:
                        dealer.remove(11)
                        dealer.append(1)
                    except:
                        pass
                try:
                    dealer.remove("Ace")
                    dealer.append(11)
                except:
                    pass
                if (sum(dealer) > 21):
                    try:
                        dealer.remove(11)
                        dealer.append(1)
                    except:
                        pass
            if sum(dealer) >= 17:
                if "Ace" in player or "Ace" in dealer:
                    break
                break
      
        if sum(player) > 21:
            if bet == 0:
                await ctx.send(ctx.message.author.mention + "\nYour hand:  " + str(player) + "  (" + str(sum(player)) + ")" + "\nDealers hand: " + str(dealer) + "  (" + str(sum(dealer)) + ")" + "\nBusted!")
            else:
                await ctx.send(ctx.message.author.mention + "\nYour hand:  " + str(player) + "  (" + str(sum(player)) + ")" + "\nDealers hand: " + str(dealer) + "  (" + str(sum(dealer)) + ")" + "\nBusted! \nyou lost bet of: $" + str(bet))
            return
        elif sum(dealer) <= 21 and sum(dealer) > sum(player):
            if bet == 0:
                await ctx.send(ctx.message.author.mention + "\nYour hand:  " + str(player) + "  (" + str(sum(player)) + ")" + "\nDealers hand: " + str(dealer) + "  (" + str(sum(dealer)) + ")" + "\nDealer wins!")
            else:
                await ctx.send(ctx.message.author.mention + "\nYour hand:  " + str(player) + "  (" + str(sum(player)) + ")" + "\nDealers hand: " + str(dealer) + "  (" + str(sum(dealer)) + ")" + "\nDealer wins! \nlost bet of: $" + str(bet))
            return
        elif sum(dealer) > 21:
            if bet == 0:
                await ctx.send(ctx.message.author.mention + "\nYour hand:  " + str(player) + "  (" + str(sum(player)) + ")" + "\nDealers hand: " + str(dealer) + "  (" + str(sum(dealer)) + ")" + "\nDealer busts, You win!")
            else:
                await ctx.send(ctx.message.author.mention + "\nYour hand:  " + str(player) + "  (" + str(sum(player)) + ")" + "\nDealers hand: " + str(dealer) + "  (" + str(sum(dealer)) + ")" + "\nDealer busts, You win! \nBet doubled  \nWon: $" + str(int(bet)*2))
            await economy.depositMoney(ctx.author, int(bet)*2)
            return
        elif sum(dealer) < sum(player):
            if bet == 0:
                await ctx.send(ctx.message.author.mention + "\nYour hand:  " + str(player) + "  (" + str(sum(player)) + ")" + "\nDealers hand: " + str(dealer) + "  (" + str(sum(dealer)) + ")" + "\nYou win!")
            else:
                await ctx.send(ctx.message.author.mention + "\nYour hand:  " + str(player) + "  (" + str(sum(player)) + ")" + "\nDealers hand: " + str(dealer) + "  (" + str(sum(dealer)) + ")" + "\nYou win! \nBet doubled  \nWon: $" + str(int(bet)*2))
            await economy.depositMoney(ctx.author, int(bet)*2)
            return
        elif sum(dealer) < sum(player):
            if bet == 0:
                await ctx.send(ctx.message.author.mention + "\nYour hand:  " + str(player) + "  (" + str(sum(player)) + ")" + "\nDealers hand: " + str(dealer) + "  (" + str(sum(dealer)) + ")" + "\nYou win!")
            else:
                await ctx.send(ctx.message.author.mention + "\nYour hand:  " + str(player) + "  (" + str(sum(player)) + ")" + "\nDealers hand: " + str(dealer) + "  (" + str(sum(dealer)) + ")" + "\nYou win! \nBet doubled  \nWon: $" + str(int(bet)*2))
            await economy.depositMoney(ctx.author, int(bet)*2)
            return
        elif sum(dealer) > sum(player):
            if bet == 0:
                await ctx.send(ctx.message.author.mention + "\nYour hand:  " + str(player) + "  (" + str(sum(player)) + ")" + "\nDealers hand: " + str(dealer) + "  (" + str(sum(dealer)) + ")" + "\nDealer wins!")
            else:
                await ctx.send(ctx.message.author.mention + "\nYour hand:  " + str(player) + "  (" + str(sum(player)) + ")" + "\nDealers hand: " + str(dealer) + "  (" + str(sum(dealer)) + ")" + "\nDealer wins! \nlost bet of: $" + str(bet))
            return
        elif sum(dealer) == sum(player):
            if bet == 0:
                await ctx.send(ctx.message.author.mention + "\nYour hand:  " + str(player) + "  (" + str(sum(player)) + ")" + "\nDealers hand: " + str(dealer) + "  (" + str(sum(dealer)) + ")" + "\nEqual!")
            else:
                await ctx.send(ctx.message.author.mention + "\nYour hand:  " + str(player) + "  (" + str(sum(player)) + ")" + "\nDealers hand: " + str(dealer) + "  (" + str(sum(dealer)) + ")" + "\nEqual!" + "\nBet returned")
            await economy.depositMoney(ctx.author, int(bet))
            return

        saldo = economy.getBalance(ctx.author)
        if saldo < 0:
            await economy.depositMoney(ctx.author, int(saldo)*-1)

def setup(client):
    client.add_cog(blackjack(client))
