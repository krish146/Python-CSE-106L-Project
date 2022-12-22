import random
import discord
import tok

from discord.ext import commands
client = commands.Bot(command_prefix="$") 

@client.command()
async def helpo(ctx):
    await ctx.send("here are your commands : ")
    await ctx.send("!roll : for rolling the number")
    await ctx.send("!g <num>:  for guessing the number")
    await ctx.send("!tictactoe :for starting the game")
    await ctx.send("!place <num>: for placing X or O on the board")
    await ctx.send("!end : for ending the game tictactoe")

#Bot commands and functions for guess the number ! 
pick =False
x=0
count=0

@client.command()
async def roll(ctx):
    global pick
    if pick==False:
        global x
        global count
        x=int(random.randint(1,10))
        print(x)
        pick=True
        await ctx.send("Number has been picked , make your guess by telling !g <number> ")
    else:
        await ctx.send("A number has already been picked ! -_- guess it first")

@client.command()
async def g(ctx,p:int):
    global pick
    global x
    global count
    if pick==True:
        count+=1
        if p==x:
            await ctx.send("You've guessed the number correctly")
            count=0
            pick=False

        elif p>x:
            await ctx.send("your guess is higher than the number ")
        else:
            await ctx.send("your guess is lower than the number been picked")
    else:
        await ctx.send("No number has been picked yet ! try <!roll> ")

@client.command()
async def hint(ctx):
    if pick==True:
        if x%2==0:
            await ctx.send("The picked number is even")
        else:
            await ctx.send("The picked number is odd")
    else:
        await ctx.send("No number has been rolled , try using <!roll> ")


#Bot commands and functions for tictactoe game !  
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member): 
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@client.command()
async def end(ctx):
    global board
    global gameOver
    if gameOver==False:
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        await ctx.send("Leaving already ? come again soon ! cya :heart:") 
        gameOver = True
    else:
        await ctx.send("The game has not started yet :moyai:")

@client.command()
async def place(ctx, pos:  int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)

                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")

client.run(tok.TOKEN)
























# async def send_message(message, user_message, is_private):
#     try:
#         response = responses.handle_response(user_message)
#         await message.author.send(response) if is_private else await message.channel.send(response)
#     except Exception as e:
#         print(e)

# async def guess_the_number(message, user_message):
#     global x
#     x = random.randint(1,100) 
#     try:
#         response = responses.handle_response(user_message)
#         if response == 'start':
#             return "Guess a number from 1 to 100:"
#         if int(response) == x:
#             return "Yes you've guessed the number correctly!"
#         elif response !=x:
#             return "You've guessed incorrectly"
#     except Exception as e1:
#         print(e1)

# def run_discord_bot():
#     TOKEN = 'MTA0MzUyMTQzODU5MTc0NjE4OQ.GRsf4P.dfK-cNt871y2QDL8EuAarcnTOqr2BS0SsEHUSw'
#     client = discord.Client()

#     @client.event
#     async def on_ready():
#         print(f'{client.user} is now running!')

#     @client.event
#     async def on_message(message):
#         if message.author == client.user:
#             return 
        
#         username = str(message.author)
#         user_message = str(message.content)
#         channel = str(message.channel) 

#         print(f"{username} said: '{user_message}' ({channel})")
#         if user_message =="?startgame":
#             await send_message(message,user_message,is_private=False)
#         elif user_message[0]== '?':
#             user_message = user_message[1:]
#             await send_message(message, user_message, is_private=True)
#         else:
#             await send_message(message, user_message, is_private=False)

    # @client.event
    # async def on_message(message):
    #     if message.author == client.user:
    #         return 
        
    #     username = str(message.author)
    #     user_message = str(message.content)
    #     channel = str(message.channel)

        # print(f"{username} said: '{user_message}' ({channel})")
        # if user_message=='start':
        #     await 
