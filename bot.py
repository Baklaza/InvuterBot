import discord
import os
from discord.ext import commands
from discord.utils import get
from easy_pil import Editor, load_image_async, Font, Canvas

intents = discord.Intents.all()
discord.member = True
discord.reaction = True

bot = commands.Bot("-", intents = intents)


@bot.command()
async def invites(ctx):
    invites = await ctx.guild.invites()
    added_members_count = 0
    invitations_count = 0

    for invite in invites:
        if invite.inviter == bot.get_user(ctx.author.id):
            invitations_count += 1
            added_members_count += invite.uses

    # embed = discord.Embed()

    # embed.colour = discord.Colour.from_rgb(225, 80, 227)
    # embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    # embed.add_field(name = 'Invitations', value = invitations_count)
    # embed.add_field(name = 'Invited', value = added_members_count)
    # embed.set_image(url = )
    image = await load_image_async(str(ctx.author.avatar_url))
    author_image = Editor(image).circle_image().resize((50, 50))

    font = Font.montserrat('bold', 24)

    canvas = Canvas((1000, 200))

    template = Editor(canvas)
    template.rectangle((0, 0), width = 1000, height = 200, radius = 10, fill = (37, 37, 37))
    template.rectangle((50, 124), 900, 25, (255, 255, 255), radius = 90)
    template.paste(author_image, (50, 51))
    template.text((114, 64), f'{ctx.author.name}#{ctx.author.discriminator}', font, (255, 255, 255))
    template.text((950, 64), f'{added_members_count} / 5', font, (255, 255, 255), 'right')

    percentage = (added_members_count * 100) / 5

    if added_members_count >= 5:
        percentage = 100

    template.bar((50, 124), 900, 25, radius = 90, percentage = percentage, fill = (225, 80, 227), outline = (225, 80, 227))

    file = discord.File(fp = template.image_bytes, filename = f'{ctx.author.name}.png')

    await ctx.message.reply(file = file)
        # if i.inviter != bot.get_user(496694962101026837):
        #     print(f'{i.inviter} - {i.uses}')


@bot.command()
async def topinviters(ctx):
    inviters_dict = {}
    invites = await ctx.guild.invites()
    
    for invite in invites:
        if invite.inviter.name not in inviters_dict:
            inviters_dict[invite.inviter.name] = invite.uses
        else:
            inviters_dict[invite.inviter.name] += invite.uses
    

    sorted_values = sorted(inviters_dict.values(), reverse = True)
    sorted_dict = {}

    for i in sorted_values:
        for k in inviters_dict.keys():
            if inviters_dict[k] == i:
                sorted_dict[k] = inviters_dict[k]
                # break


    top = ''
    count = 0
    for name, inv in sorted_dict.items():
        if count == 10:
            break

        if name != 'nonenickname' and inv != 0:
            top += f'{name} - {inv} invites\n'

        count += 1

    embed = discord.Embed()
    embed.title = 'Top 10 inviters'
    embed.description = top
    embed.colour = discord.Colour.from_rgb(225, 80, 227)
    await ctx.message.reply(embed = embed)


token = os.environ.get('BOT_TOKEN')
bot.run(str(token))