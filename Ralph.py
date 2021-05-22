import discord
from discord.ext import commands
from dotenv import load_dotenv
import numpy as np
import os 

load_dotenv()
TOKEN = os.environ['TOKEN']

bot = commands.Bot(command_prefix='$', help_command=None)

banned_symbol = ('[',']',"'")

def load():
    with np.load('data.npz') as data:
        global command
        global output
        global counter

        command = data['command']
        output = data['output']
        counter = data['counter']

def save_array(save_command, save_output, save_counter):
    np.savez('data.npz', command = save_command, output = save_output, counter = save_counter)

@bot.command()
async def show(ctx):
    command_list = ''
    for i in range(command.size):
        command_list = command_list + '\n' + command[i] + '\t\t' +  output[i]
    
    await ctx.send(command_list)

@bot.command()
async def help(ctx):
    f = open('help.txt','r')
    contents = f.read()
    f.close()

    await ctx.send(contents)

@bot.command()
async def add(ctx, new_command, new_output, new_counter):
    try:
        new_command_array = np.append(command, [new_command])
        new_output_array = np.append(output, [new_output])
        new_counter_array = np.append(counter, [new_counter])
        
        save_array(new_command_array, new_output_array, new_counter_array)
        load()

        await ctx.send('Listo!!!')
    except:
        await ctx.send('ERROR, Revisa la sintaxis')

@bot.command()
async def delete(ctx, old_command):
    index = np.where(command == old_command)
    flag = np.any(index)
    
    if flag:
        new_command_array = np.delete(command, index)
        new_output_array = np.delete(output, index)
        new_counter_array = np.delete(counter, index)

        save_array(new_command_array, new_output_array, new_counter_array)
        load()

        await ctx.send('Listo!!!')
    else:
        await ctx.send('Contador no Encontrado')

@bot.command()
async def ralph(ctx, exect_command):
    index = np.where(command == exect_command)
    flag = np.any(index)

    if flag:
        valut_counter = int(counter[index]) + 1
        counter[index] = valut_counter

        save_array(command, output, counter)
        message = str(output[index]).format(valut_counter)

        for symbol in banned_symbol:
            message = message.replace(symbol , '')

        await ctx.send(message)
    else:
        await ctx.send('Contador no Encontrado')

load()
bot.run(TOKEN)