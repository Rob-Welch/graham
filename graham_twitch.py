import call_response
import os # for importing env vars for the bot to use
import sys
from twitchio.ext import commands

help_msg = "Hello, I\'m Graham. I like cars and car accessories. I can talk and also use memes, replacing the need for other surviving humans. Learn how to use me at https://raw.githubusercontent.com/RSN-Bran/graham/master/graham_help.txt"

graham = call_response.call_response(help_msg=help_msg, decay_in=50)

class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...

        if "Token" in os.environ and "Channels" in os.environ:
            super().__init__(token=os.environ["Token"], prefix='~', initial_channels=os.environ["Channels"].split(','))
        else:
            super().__init__(token=sys.argv[1], prefix='~', initial_channels=sys.argv[2].split(','))

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):

        if message.echo:
            return

        if(not message.channel):
            response = graham.parse(message.content, "")
        else:
            response = graham.parse(message.content, message.channel.name)
            if(response != ""):
                await message.channel.send(response)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send("Learn to use me at https://www.twitch.tv/golden_graham_bot/about")

if __name__ == "__main__":
    bot = Bot()
    bot.run()