import os
import random

import discord
import pandas as pd

#---- Importing Dice Tables ----#

# Damage Tables
acid_df = pd.read_csv('Dice Tables/Dice Tables_Acid.csv',
                      encoding='unicode_escape')
bludgeoning_df = pd.read_csv('Dice Tables/Dice Tables_Bludgeoning.csv',
                             encoding='unicode_escape')
cold_df = pd.read_csv('Dice Tables/Dice Tables_Cold.csv',
                      encoding='unicode_escape')
fire_df = pd.read_csv('Dice Tables/Dice Tables_Fire.csv',
                      encoding='unicode_escape')
force_df = pd.read_csv('Dice Tables/Dice Tables_Force.csv',
                       encoding='unicode_escape')
lightning_df = pd.read_csv('Dice Tables/Dice Tables_Lightning.csv',
                           encoding='unicode_escape')
necrotic_df = pd.read_csv('Dice Tables/Dice Tables_Necrotic.csv',
                          encoding='unicode_escape')
piercing_df = pd.read_csv('Dice Tables/Dice Tables_Piercing.csv',
                          encoding='unicode_escape')
poison_df = pd.read_csv('Dice Tables/Dice Tables_Poison.csv',
                        encoding='unicode_escape')
psychic_df = pd.read_csv('Dice Tables/Dice Tables_Psychic.csv',
                         encoding='unicode_escape')
radiant_df = pd.read_csv('Dice Tables/Dice Tables_Radiant.csv',
                         encoding='unicode_escape')
slashing_df = pd.read_csv('Dice Tables/Dice Tables_Slashing.csv',
                          encoding='unicode_escape')
thunder_df = pd.read_csv('Dice Tables/Dice Tables_Thunder.csv',
                         encoding='unicode_escape')

# Injury Table
injury_df = pd.read_csv('Dice Tables/Dice Tables_Injury.csv',
                        encoding='unicode_escape')

# Insanity Table
insanity_df = pd.read_csv('Dice Tables/Dice Tables_Insanity.csv',
                          encoding='unicode_escape')

#---- Discord Bot ----#

# Setup of bot
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


# Bot events
@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  # Get message content
  messageContent = message.content

  # ----Info command----
  if messageContent.startswith('!crit info'):
    await message.channel.send('''**Introduction**
The DnD Critical Hits bot is designed to assist \
Dungeon Masters (DMs) and players in using the optional rules for critical hits as \
described in the "Critical Hits Revisited" expansion for D&D 5e. This bot streamlines \
the process of incorporating the critical hit charts based on damage types, enhancing \
the combat experience with added uncertainty and potential consequences.\n
**Functions**
The bot provides the following functionalities:
- The bot can handle the critical hit roll, or the user can input the roll manually.
- DMs and players can input the type of damage, and the bot will roll on the \
corresponding damage chart.
- Detailed descriptions of critical hits effects are provided.
- The bot can also roll on injury and insanity tables to determine the additional \
consequences.
- Negated Crit (Nat 1) rolls on the damage critical hit tables have been removed \
(for auto rolls).\n
    ''')

  # ----Rules command----
  if messageContent.startswith('!crit rules'):
    await message.channel.send('''**Critical Hits Revisited**
_Below is directly from Critical Hits Revisited_
Except when noted otherwise below, use the normal rules for critical hits.
- When you land a critical hit on a creature, instead of rolling the attack’s damage \
dice twice and adding them together, roll a d20 and use the corresponding result on \
the critical hit chart determined by the damage type of your attack.
- When you score a critical hit with an attack that does two or more types of damage, \
choose one of those damage types and roll on that critical chart.
- The Half-Orc Savage Attacks trait and the Barbarian Brutal Critical feature continue \
to work as written.\n
**Injuries & Insanity**
- Critical hits can cause minor and major injuries. When a creature suffers a minor \
injury it can be healed by the spell lesser restoration or by using the recuperating \
downtime activity (Player’s Handbook, pg. 187).
- Major injuries will not heal on their own and require the powerful healing spell, \
greater restoration. Insanities, caused by critical hits that deal psychic damage, \
must be healed the same way.
- The text of certain injuries will specify other ways this injuries might resolve.
    ''')

  # ----Commands command----
  if messageContent.startswith('!crit commands'):
    await message.channel.send('''**Commands**
The bot supports the following commands:
- `!crit info` - Displays information about the bot and its functionalities.
- `!crit rules` - Displays the optional rules for critical hits.
- `!crit commands` - Displays the list of available commands.
- `!crit auto [damagetype]` - The bot will roll a d20 and determine the critical hit \
result based on the damage type.
- `!crit manual [damagetype] [roll]` - The bot will roll the specified dice and \
determine the critical hit result.
- `!crit injury [injurytype]` - The bot will roll on the injury table to determine \
the additional consequences.
- `!crit insanity` - The bot will roll on the insanity table to \
determine the additional consequences.\n
**Parameters**
- `damagetype`: The type of damage that the user wants to roll on. Included types are \
acid, bludgeoning, cold, fire, force, lightning, necrotic, piercing, poison, psychic, \
radiant, slashing, and thunder.
- `roll`: The user can manually input the roll they want to use. Range between 1-20.
- `injurytype`: The type of injury that the user wants to roll on. Included types are \
minor and major.
    ''')

  # ----Auto d20 rolls----
  if message.content.startswith('!crit auto'):

    # Get damage type
    damagetype = messageContent.split(' ')[2].lower()

    if damagetype not in ('acid', 'bludgeoning', 'cold', 'fire', 'force',
                          'lightning', 'necrotic', 'piercing', 'poison',
                          'psychic', 'radiant', 'slashing', 'thunder'):
      await message.channel.send(
          'That is not a valid damage type, please try again.')
      return

    # Roll d20
    roll = random.randint(2, 20)

    # Get damage table
    damage_df = {}
    emoji = ""

    if damagetype == 'acid':
      damage_df = acid_df
      emoji = ":skull_crossbones:"
    elif damagetype == 'bludgeoning':
      damage_df = bludgeoning_df
      emoji = ":punch:"
    elif damagetype == 'cold':
      damage_df = cold_df
      emoji = ":cold_face:"
    elif damagetype == 'fire':
      damage_df = fire_df
      emoji = ":fire:"
    elif damagetype == 'force':
      damage_df = force_df
      emoji = ":comet:"
    elif damagetype == 'lightning':
      damage_df = lightning_df
      emoji = ":cloud_lightning:"
    elif damagetype == 'necrotic':
      damage_df = necrotic_df
      emoji = ":zombie:"
    elif damagetype == 'piercing':
      damage_df = piercing_df
      emoji = ":knife:"
    elif damagetype == 'poison':
      damage_df = poison_df
      emoji = ":sick:"
    elif damagetype == 'psychic':
      damage_df = psychic_df
      emoji = ":brain:"
    elif damagetype == 'radiant':
      damage_df = radiant_df
      emoji = ":innocent:"
    elif damagetype == 'slashing':
      damage_df = slashing_df
      emoji = ":axe:"
    elif damagetype == 'thunder':
      damage_df = thunder_df
      emoji = ":mega:"
    else:
      return

    # Get damage table row
    d_message = ""

    for i in range(len(damage_df)):
      if damage_df['Min'][i] <= roll and damage_df['Max'][i] >= roll:
        d_message = damage_df["Result"][i]

    # Send message to channel with result of roll
    await message.channel.send(
        f'You rolled {roll} with {damagetype} damage! {emoji} \n\n{d_message}')

  # ----Manual d20 rolls----
  if message.content.startswith('!crit manual'):

    # Get damage type
    damagetype = messageContent.split(' ')[2].lower()

    if damagetype not in ('acid', 'bludgeoning', 'cold', 'fire', 'force',
                          'lightning', 'necrotic', 'piercing', 'poison',
                          'psychic', 'radiant', 'slashing', 'thunder'):
      await message.channel.send(
          'That is not a valid damage type, please try again.')
      return

    # Get user input roll of d20
    try:
      roll = int(messageContent.split(' ')[3])
    except ValueError:
      await message.channel.send('That is not a number, please try again.')
      return

    if roll not in range(1, 21):
      await message.channel.send('That is not a valid roll, please try again.')
      return

    # Get damage table
    damage_df = {}
    emoji = ""

    if damagetype == 'acid':
      damage_df = acid_df
      emoji = ":skull_crossbones:"
    elif damagetype == 'bludgeoning':
      damage_df = bludgeoning_df
      emoji = ":punch:"
    elif damagetype == 'cold':
      damage_df = cold_df
      emoji = ":cold_face:"
    elif damagetype == 'fire':
      damage_df = fire_df
      emoji = ":fire:"
    elif damagetype == 'force':
      damage_df = force_df
      emoji = ":comet:"
    elif damagetype == 'lightning':
      damage_df = lightning_df
      emoji = ":cloud_lightning:"
    elif damagetype == 'necrotic':
      damage_df = necrotic_df
      emoji = ":zombie:"
    elif damagetype == 'piercing':
      damage_df = piercing_df
      emoji = ":knife:"
    elif damagetype == 'poison':
      damage_df = poison_df
      emoji = ":sick:"
    elif damagetype == 'psychic':
      damage_df = psychic_df
      emoji = ":brain:"
    elif damagetype == 'radiant':
      damage_df = radiant_df
      emoji = ":innocent:"
    elif damagetype == 'slashing':
      damage_df = slashing_df
      emoji = ":axe:"
    elif damagetype == 'thunder':
      damage_df = thunder_df
      emoji = ":mega:"
    else:
      return

    # Get damage table row
    d_message = ""

    for i in range(len(damage_df)):
      if damage_df['Min'][i] <= roll and damage_df['Max'][i] >= roll:
        d_message = damage_df["Result"][i]

    # Send message to channel with result of roll
    await message.channel.send(
        f'You rolled {roll} with {damagetype} damage! {emoji} \n\n{d_message}')

  # ----Injury table roll----
  if message.content.startswith('!crit injury'):

    # Get damage type
    injurytype = messageContent.split(' ')[2].lower()

    if injurytype not in ('minor', 'major'):
      await message.channel.send(
          'That is not a valid injury type, please try again.')
      return

    # Roll d20
    roll = random.randint(1, 20)

    # Get damage table row
    i_message = ""
    emoji = ""

    for i in range(len(injury_df)):
      if injury_df['Min'][i] <= roll and injury_df['Max'][i] >= roll:
        if injurytype == 'minor':
          i_message = injury_df["Minor"][i]
          emoji = ":exclamation:"
        elif injurytype == 'major':
          i_message = injury_df["Major"][i]
          emoji = ":bangbang:"
        else:
          await message.channel.send(
              'That is not a valid injury type, please try again.')
          return

    # Send message to channel with result of roll
    await message.channel.send(
        f'You rolled {roll} with a {injurytype} injury! {emoji}\n\n{i_message}'
    )


# ----Insanity table roll----
  if message.content.startswith('!crit insanity'):

    # Roll d20
    roll = random.randint(1, 20)

    # Get damage table row
    b_message = ""

    for i in range(len(insanity_df)):
      if insanity_df['Roll'][i] == roll:
        b_message = insanity_df["Result"][i]

    # Send message to channel with result of roll
    await message.channel.send(
        f'You rolled {roll} insanity! :face_with_spiral_eyes: \n\n{b_message}')

# ----Crit Tracker Commands----

# ----Crit Tracker ~ Create Tracker----
  if message.content.startswith('!crit tracker new'):
    tracker_name = messageContent.split(' ')[3].lower()

    tracker_filename = tracker_name + ".csv"

    try:
      tracker_file = open(tracker_filename, "x")
      tracker_file.close()
      await message.channel.send(
        f':dart: You have created a new tracker: {tracker_name}')
    except FileExistsError:
      await message.channel.send('This tracker already exists')

# ----Crit Tracker ~ Delete Tracker----
  if message.content.startswith('!crit tracker delete'):
    tracker_name = messageContent.split(' ')[3].lower()

    tracker_filename = tracker_name + ".csv"
    if os.path.exists(tracker_filename):
      os.remove(tracker_filename)

      await message.channel.send(
        f':x: You have deleted tracker: {tracker_name}')
    else:
      await message.channel.send("The file does not exist")

# ----Crit Tracker ~ Add Player----
  if message.content.startswith('!crit tracker addplayer'):
    tracker_name = messageContent.split(' ')[3].lower()
    player_name = messageContent.split(' ')[4].upper()
    player_score = messageContent.split(' ')[5]

    tracker_filename = tracker_name + ".csv"
    tracker_file = open(tracker_filename, "a")
    tracker_file.write(player_name + ',' + player_score + '\n')
    tracker_file.close()

    await message.channel.send(
      f'Created player in tracker "{tracker_name}"\n\n{player_name} with a Crit Tally of {player_score}')


client.run('')
