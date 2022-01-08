import call_response
import os # for importing env vars for the bot to use
import sys
from twitchio.ext import commands

help_msg = "Learn how to use me at https://www.twitch.tv/golden_graham_bot/about"

graham = call_response.call_response(help_msg=help_msg, decay_in=50)

class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=os.environ['TMI_TOKEN'], prefix='~', initial_channels=sys.argv[1].split(','))

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):

        if message.echo:
            return

        #if message.content == "~help":
        #    return

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
    print(sys.argv[1])

    bot = Bot()
    bot.run()