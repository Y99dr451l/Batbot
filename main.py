#import os
import numpy
import discord
from keep_alive import keep_alive

client = discord.Client()
rng = numpy.random.default_rng()
wittwer = numpy.zeros(16)  # [0,0,..]
wittwerw = numpy.arange(16)  # [0,1,2,...,15]
wb = 0
wz = 0
emojis = [
    '<:16:859536749982253076>', '<:15:859536749582745611>',
    '<:14:859536749708574721>', '<:13:859536749897056287>',
    '<:12:859536749922091068>', '<:11:859536749982384168>',
    '<:8_:859536749624557569>', '<:7_:859536749897056286>',
    '<:6_:859536749646839829>', '<:5_:859536749850918963>',
    '<:4_:859536749835452416>', '<:3_:859536749796786215>',
    '<:2_:859536749838991420>', '<:0_:859847678745247775>',
    '<:1_:859536749830471740>'
]
invalidmovestr = 'Wittwer both fends off the dark forces you tried to bring into his realm and disarms you of your immortality within a quarter of a Planck interval.'


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global wb
    global wz
    global wittwer
    if message.author == client.user:
        return
    if message.content.startswith('$'):
        input = message.content[1:]  # removes $
        #puzzle commands ------------------------------------------
        if input == 'wittymix' and wb == 0:
            wb = 1
            wittwer = numpy.arange(16)
            rng.shuffle(wittwer)  # random
            for n in range(0, 16):
                if wittwer[n] == 15:
                    wz = n  # tile with empty cell
                    break
            await message.channel.send(printwitty(wittwer))
            await message.channel.send(
                'Witty has been mixed.\n Use $l, $r, $u, $d to move a tile.\nWhile dismantled, Witty shall correct the analysis exams of the 421 universes under his guard at a mean rate of 68.9 Yottaflops.\nDo not disappoint him.'
            )
            return

        elif input == 'wittymix' and wb == 1:
            await message.channel.send(
                'Witty is already mixed, use $wittyunmix to restart')
            return

        elif input == 'wittyunmix':
            wb = 0
            await message.channel.send(
                'You disappointed Witty.\nHe used a puny 0.01% of his ungodly power to fully regenerate.'
            )
            return

        #elif input=='r' or input=='l' or input=='d' or input=='u':
        elif set(input).issubset({'u', 'd', 'l', 'r'}) == True:
            if wb == 0:
                await message.channel.send(
                    'You very foolishly attempted to move an unmixed Wittwer.\nHorrible things will happen.'
                )
                return
            elif wb == 1:
                input2 = input
                error = 0
                for l in range(len(input2)):
                    input = input2[l]
                    if input == 'r' and error == 0:
                        if wz == 0 or wz == 4 or wz == 8 or wz == 12:
                            await message.channel.send(invalidmovestr)
                            error = 1
                        else:
                            temp = wittwer[wz - 1]
                            wittwer[wz - 1] = wittwer[wz]
                            wittwer[wz] = temp
                            wz -= 1

                    if input == 'l' and error == 0:
                        if wz == 3 or wz == 7 or wz == 11 or wz == 15:
                            await message.channel.send(invalidmovestr)
                            error = 1
                        else:
                            temp = wittwer[wz + 1]
                            wittwer[wz + 1] = wittwer[wz]
                            wittwer[wz] = temp
                            wz += 1

                    if input == 'd' and error == 0:
                        if wz == 0 or wz == 1 or wz == 2 or wz == 3:
                            await message.channel.send(invalidmovestr)
                            error = 1
                        else:
                            temp = wittwer[wz - 4]
                            wittwer[wz - 4] = wittwer[wz]
                            wittwer[wz] = temp
                            wz -= 4

                    if input == 'u' and error == 0:
                        if wz == 12 or wz == 13 or wz == 14 or wz == 15:
                            await message.channel.send(invalidmovestr)
                            error = 1
                        else:
                            temp = wittwer[wz + 4]
                            wittwer[wz + 4] = wittwer[wz]
                            wittwer[wz] = temp
                            wz += 4
            await message.channel.send(printwitty(wittwer))
            cnt = 0
            for n in range(16):
                if wittwer[n] == wittwerw[n]:
                    cnt += 1
            if cnt == 16:
                error = 1
                wb = 0
                await message.channel.send(
                    'Witty has been saved from your stupidity and can now carry on with waking you up every monday and wednesday at 8:15 with no remorse whatsoever.'
                    + emojis[5] + emojis[6] +
                    '\n\n\nᵇᶦᵍ ᵍᵍ ᵗʰᵒᵘᵍʰ ᵗʰᶦˢ ᶦˢ ᵃᵐᵃᶻᶦⁿᵍ')
            return

#random commands ------------------------------------------
        elif input == 'witty':
            wittweri = numpy.arange(16)
            wittweri[15] += 1
            await message.channel.send(printwitty(wittweri))
            return

        elif input == 'plagueis':
            await message.channel.send(
                'Did you ever hear the tragedy of Darth Plagueis The Wise? I thought not. It’s not a story the Jedi would tell you. It’s a Sith legend. Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life… He had such a knowledge of the dark side that he could even keep the ones he cared about from dying. The dark side of the Force is a pathway to many abilities some consider to be unnatural. He became so powerful… the only thing he was afraid of was losing his power, which eventually, of course, he did. Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep. Ironic. He could save others from death, but not himself.'
            )
            await message.channel.send('https://tenor.com/bk8ik.gif')
            return


#rest --------------------------------------------------------
        else:
            await message.channel.send('me no understand')
            return


def printwitty(arrayinput):
    global wz
    ppwstr = ''
    cnt = 0
    for n in range(0, 16):
        ppwstr += emojis[arrayinput[n]]
        cnt += 1
        if cnt == 4:
            cnt = 0
            ppwstr += '\n'
    return ppwstr


keep_alive()
TOKEN = os.environ['TOKEN']
client.run(TOKEN)
