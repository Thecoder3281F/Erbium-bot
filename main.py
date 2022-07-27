import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import random
import asyncio

client = commands.Bot(command_prefix="er!", case_insensitive=True)

client.remove_command("help")
status = cycle(['Waiting for er!help', 'Hi', '9+10=21', "I like memes", "ErBr3"])

@client.event
async def on_ready():
    change_status.start()
    print("The bot is now online.")

@tasks.loop(seconds = 10)
async def change_status():
    await client.change_presence(status = discord.Status.online, activity = discord.Game(next(status)))


@client.command()
async def help(ctx):
    help_embed = discord.Embed()
    help_embed.title = "Your general purpose Discord bot"
    help_embed.description = "I can do (almost) anything you want, including moderation, fun, math and memes."
    help_embed.colour = discord.Colour.dark_green()

    # Bot prefix
    help_embed.add_field(
        name = "The bot's prefix is:",
        value = "`er!`",
        inline = False
    )
    # utility commands
    help_embed.add_field(
        name = "Utility commands",
        value = """
        `hello` - Says something back
        `ping` - Displays client latency
        """,
        inline = False
    )

    # fun commands
    help_embed.add_field(
        name = "Fun commands",
        value = """
        `8ball` - Basically a Magic 8 Ball. Just ask it a question and you will get a response.
        `toxic` - Self-explanatory. Imagine.
        `roast` - A random roast.

        *Emojis*
        `facepalm` - Facepalm emoji.
        `hmm` - Thinking emojis.
        `trackball` - Trackball emoji.
        """,
        inline = False
    )

    # moderation commands
    help_embed.add_field(
        name = "Moderation commands",
        value = """
        `clear` - Removes a specified number of messages.
        `kick` - Kicks a member.
        `ban` - Bans a member.
        `unban` - Unbans a member.
        `mute` - Mutes a member.
        `unmute` - Unmutes a member.
        """,
        inline = False
    )

    # games commands
    help_embed.add_field(
        name = "Games commands",
        value = """
        `dice` - Rolls a 6-sided dice.
        `guess` - Guess a number within a specified range.
        """,
        inline = False
    )

    # meme commands
    help_embed.add_field(
        name = "Meme commands",
        value = """
        `rickroll` - Please click the link.
        `basic_math` - Self-explanatory.
        `twentyonekid` - The best meme in the world.
        """,
        inline = False
    )

    # math commands
    help_embed.add_field(
        name = "Math commands",
        value = """
        `calc` - Basic 4 operations calculator. (work-in-progress)
        """,
        inline = False
    )

    await ctx.send(embed=help_embed)

# Utility commands
@client.command()
async def hello(ctx):
    await ctx.send("Hello!")

@client.command()
async def ping(ctx):
    latency = round(client.latency * 1000)
    embed = discord.Embed()
    embed.title = "Latency"
    embed.description = f"The bot's latency is: {latency}ms"
    embed.colour = discord.Colour.from_rgb(5, 23, 7)
    embed.set_author(
        name="L",
        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    icon_url="https://cdn.shopify.com/s/files/1/0407/1351/9262/products/7195n-8XMDL._AC_SL1000_360x.jpg?v=1597310031"
    )
    
    await ctx.send(embed=embed)



# Fun commands
@client.command(aliases=["8ball"])
async def eightball(ctx, *, question):
    responses = [
        "Yes, definitely.",
        "Most likely.",
        "My sources say no.",
        "Outlook not so good.",
        "Concentrate and ask again."
    ]

    response = random.choice(responses)

    await ctx.send("Question: " + question)
    await ctx.send("Answer: " + response)
    
@client.command()
async def toxic(ctx):
    await ctx.send(":face_with_symbols_over_mouth: L + bozo + ratio")

@client.command()
async def facepalm(ctx):
    await ctx.send(":facepalm:")

@client.command()
async def hmm(ctx):
    await ctx.send(":thinking: :face_with_monocle: :face_with_raised_eyebrow:")

@client.command()
async def trackball(ctx):
    await ctx.send(":trackball:")

@client.command()
async def roast(ctx):
    roasts = ["imagine being so bad", 
              "L bozo", 
              "get good", 
              "ratio"
             ]
    
    await ctx.send(random.choice(roasts))



# Games commands
@client.command()
async def dice(ctx):
    await ctx.send(f":game_die: {random.randint(1, 6)}")

@client.command()
async def guess(ctx):
    attempts = 3
    
    bottom_range, upper_range = 1, 10
    await ctx.send("Please specify the bottom range and the upper range of the answer. (space-separated)")
    
    ranges = await client.wait_for("message", timeout=30.0)
    ranges = ranges.content.split()

    if len(ranges) >= 2 and ranges[0].isdigit() and ranges[1].isdigit():
        bottom_range, upper_range = int(ranges[0]), int(ranges[1])
    
    else:
        await ctx.send("invalid input")
            
    answer = random.randint(bottom_range, upper_range)
    
    await ctx.send(f"Please guess a number from {bottom_range} to {upper_range}.")


    while attempts > 0:
        try:
            userguess = await client.wait_for("message", timeout=30.0)
            
        except asyncio.TimeoutError:
            await ctx.send("timeout due to inactivity")
            return
            
        except ValueError:
            await ctx.send("Not a number")
            await ctx.send(f"You have {attempts} attempt(s) left.")
        
        else:
            userguess = userguess.content
            userguess = int(userguess)
            if userguess < bottom_range or userguess > upper_range:
                await ctx.send("Outside of range")
                continue
            if int(userguess) == answer:
                await ctx.send("Congratulations you guessed correctly!")
                break
                    
            elif userguess > answer:
                await ctx.send("Too high")

            elif userguess < answer:
                await ctx.send("Too low")

            attempts -= 1
            await ctx.send(f"You have {attempts} attempt(s) left.")

    if attempts <= 0:
        await ctx.send("No more attempts")
        await ctx.send(f"Imagine being so bad\n The answer was {answer}")




# Moderation commands
@client.command(aliases=["purge"])
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount=10):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)

@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason=""):
    await member.kick(reason=reason)
    await ctx.send(f"successfully kicked {member.name}#{member.discriminator}")
    await ctx.send(f"reason: {reason}")

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member, *, reason=""):
    await member.ban(reason=reason)
    await ctx.send(f"successfully banned {member.name}#{member.discriminator}")
    await ctx.send(f"reason: {reason}")

@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    banned = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban in banned:
        user = ban.user
        if user.name == member_name and user.discriminator == member_discriminator:
            await ctx.guild.unban(user)
            await ctx.send(f"successfully unbanned {user.name}#{user.discriminator}")
            return

@client.command()
@commands.has_permissions(manage_roles = True)
async def mute(ctx, member: discord.Member, *, reason=""):
    guild = ctx.guild
    muted_role = discord.utils.get(guild.roles, name = "Muted")

    if not muted_role:
        muted_role = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(muted_role, speak = False, send_messages = False, view_channels = False)

    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f"Successfully muted {member.name}#{member.discriminator}.\nReason: {reason}")
    await member.send(f"you were muted in the server {ctx.guild.name} for {reason}")

@client.command()
@commands.has_permissions(manage_roles = True)
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name = "Muted")
    await member.remove_roles(muted_role)
    await ctx.send(f"successfully unmuted {member.name}#{member.discriminator}")
    await member.send(f"you were unmuted in the server {ctx.guild.name}.")



# Meme commands
@client.command()
async def rickroll(ctx):
    await ctx.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    await ctx.send("https://www.youtube.com/watch?v=hWFiyAfknWc")

@client.command()
async def basic_math(ctx):
    await ctx.send("9+10=21")
    
@client.command()
async def twentyonekid(ctx):
    embed = discord.Embed()
    embed.title = "The classic meme"
    embed.description = "9+10=21 forever"
    embed.colour = discord.Colour.from_rgb(5, 23, 7)
    embed.set_author(
        name="Twenty one kid fanatic",
        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    icon_url="https://cdn.shopify.com/s/files/1/0407/1351/9262/products/7195n-8XMDL._AC_SL1000_360x.jpg"
    )
    
    embed.set_image(
        url="https://i.kym-cdn.com/photos/images/newsfeed/001/049/862/8b6.jpg"
    )
    
    embed.set_thumbnail(
        url="https://pbs.twimg.com/media/E-0mmepXoAUVA0b?format=jpg&name=medium"
    )

    embed.set_footer(
        text="Yes this is definitely true. Celebrate 09/10/21",
        icon_url="https://www.iconsdb.com/icons/preview/green/checkmark-xxl.png"
    )

    embed.add_field(
        name="Guy:",
        value="You stupid.",
        inline=False
    )

    embed.add_field(
        name="21 Kid:",
        value="No I'm not.",
        inline=False
    )

    embed.add_field(
        name="Guy:",
        value="What's 9+10?",
        inline=False
    )

    embed.add_field(
        name="21 Kid:",
        value="21.",
        inline=False
    )

    embed.add_field(
        name="Guy:",
        value="You stupid.",
        inline=False
    )

    await ctx.send(embed=embed)




# Math commands
@client.command()
async def calc(ctx, a, b):
    await ctx.send("Operations: 1. Add\n 2. Subtract\n 3. Multiply\n 4. Divide")
    try:
        operation = await client.wait_for("message", timeout=30)
            
    except asyncio.TimeoutError:
        await ctx.send("timeout due to inactivity")
        return

    operation = int(operation)

    if operation == 1:
        operation = "+"
    elif operation == 2:
        operation = "-"
    elif operation == 3:
        operation = "*"
    elif operation == 4:
        operation = "/"
    else:
        await ctx.send("Invalid operation.")





token = os.getenv("token")
client.run(token)