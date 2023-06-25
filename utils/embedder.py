import discord


class EmbedTextSimpleField:
  def __init__(self, name, value):
    self.name = name
    self.value = value

def embed(title, description, list, footer):
  embed = discord.Embed(
    title = title,
    url = '',
    description = description,
    color = discord.Color.blue()
  )
  embed.set_author(name='The Archer Queen', url='')
  for x in list:
    embed.add_field(name = x.name, value = x.value, inline = False)
  embed.set_footer(text=footer)
  return embed

def embedimage(title, description, image, footer):
  embed = discord.Embed(
    title = title,
    url = '',
    description = description,
    color = discord.Color.blue()
  )
  embed.set_author(name='The Archer Queen', url='')
  embed.set_image(url = image)
  embed.set_footer(text=footer)
  return embed