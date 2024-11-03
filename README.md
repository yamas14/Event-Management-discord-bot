# Event-Management-discord-bot
Creating an Event:

1. The !create_event command allows users to create events with a title, date, and time. It saves the event data in a JSON file for persistence.
Example usage: !create_event "Game Night" 2024-11-15 20:00
Viewing Events:

2. The !view_events command lists all upcoming events. It formats them to show the title, date, time, and the organizer.
Example usage: !view_events
RSVP to Events:

3. The !rsvp command allows users to RSVP for a specific event by title. The bot will record the RSVP in the event’s data.
Example usage: !rsvp "Game Night"
Canceling an Event:

4. The !cancel_event command allows organizers to cancel an event.
Example usage: !cancel_event "Game Night"
Event Reminders:

5. A background task (event_reminder) runs every minute to check if any event is starting within the next 30 minutes. If so, it sends a reminder to the designated channel.
