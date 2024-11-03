import discord
from discord.ext import commands, tasks
import json
from datetime import datetime, timedelta

# Intents and Bot setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Load event data from JSON
def load_events():
    try:
        with open("event_data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_events(events):
    with open("event_data.json", "w") as f:
        json.dump(events, f, indent=4)

events = load_events()

# Helper to format events
def format_event(event):
    return f"**{event['title']}** - {event['date']} at {event['time']} | Organizer: {event['organizer']}"

# Bot ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    event_reminder.start()  # Start reminder task

# Add event command
@bot.command(name='create_event')
async def create_event(ctx, title: str, date: str, time: str):
    """Create a new event with a title, date (YYYY-MM-DD), and time (HH:MM)"""
    event = {
        'title': title,
        'date': date,
        'time': time,
        'organizer': ctx.author.name,
        'reminded': False
    }
    events[title] = event
    save_events(events)
    await ctx.send(f"Event '{title}' has been created for {date} at {time} by {ctx.author.name}!")

# View all events
@bot.command(name='view_events')
async def view_events(ctx):
    """View all upcoming events."""
    if not events:
        await ctx.send("No events are scheduled!")
    else:
        event_list = "\n".join([format_event(event) for event in events.values()])
        await ctx.send(f"**Upcoming Events**\n{event_list}")

# RSVP command
@bot.command(name='rsvp')
async def rsvp(ctx, event_title: str):
    """RSVP for an existing event."""
    if event_title in events:
        event = events[event_title]
        if 'rsvps' not in event:
            event['rsvps'] = []
        if ctx.author.name not in event['rsvps']:
            event['rsvps'].append(ctx.author.name)
            save_events(events)
            await ctx.send(f"{ctx.author.name} has RSVP'd for the event '{event_title}'!")
        else:
            await ctx.send(f"You have already RSVP'd for this event.")
    else:
        await ctx.send(f"No event found with the title '{event_title}'")

# Cancel event command
@bot.command(name='cancel_event')
async def cancel_event(ctx, title: str):
    """Cancel an existing event."""
    if title in events:
        del events[title]
        save_events(events)
        await ctx.send(f"Event '{title}' has been cancelled.")
    else:
        await ctx.send(f"No event found with the title '{title}'.")

# Basic greetings
@bot.command(name='hello')
async def greet_hello(ctx):
    """Greet the user."""
    await ctx.send(f"Hello {ctx.author.name}! Hope you're having a great day!")

@bot.command(name='how_are_you')
async def greet_how_are_you(ctx):
    """Respond to 'How are you?'"""
    await ctx.send("I'm just a bot, but thanks for asking! How about you? 😊")

@bot.command(name='goodbye')
async def greet_goodbye(ctx):
    """Say goodbye to the user."""
    await ctx.send("Goodbye! Hope to see you soon!")

# Background task to send reminders
@tasks.loop(minutes=1)
async def event_reminder():
    now = datetime.now()
    for event in events.values():
        event_date = datetime.strptime(event['date'] + ' ' + event['time'], '%Y-%m-%d %H:%M')
        time_until_event = event_date - now
        if time_until_event <= timedelta(minutes=30) and not event.get('reminded', False):
            channel = discord.utils.get(bot.get_all_channels(), name='general')
            if channel:
                await channel.send(f"Reminder: Event '{event['title']}' is starting in 30 minutes!")
            event['reminded'] = True
            save_events(events)

# Bot token (replace 'YOUR_TOKEN' with your actual bot token)
bot.run('YOUR_TOKEN')
