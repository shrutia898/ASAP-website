import sqlite3
import datetime
import schedule
import time
from plyer import notification

# Function to create a SQLite database and table if they don't exist
def create_database():
    conn = sqlite3.connect("daily_mood.db")
    cursor = conn.cursor()

    # Create a table to store daily mood entries
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_mood (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME,
            mood TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Function to prompt the user and insert daily mood into the database
def record_daily_mood():
    mood = input("How are you doing today? Enter your mood: ")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("daily_mood.db")
    cursor = conn.cursor()

    # Insert the mood into the database
    cursor.execute("INSERT INTO daily_mood (timestamp, mood) VALUES (?, ?)", (timestamp, mood))

    conn.commit()
    conn.close()

# Function to send a notification at 12 PM
def send_notification():
    notification_title = "Daily Mood Reminder"
    notification_message = "Don't forget to record your daily mood!"
    notification.timeout = 10  # Set the notification timeout (in seconds)

    notification.notify(
        title=notification_title,
        message=notification_message,
    )

if __name__ == "__main__":
    create_database()

    # Schedule the script to run at 12 PM and send a notification
    schedule.every().day.at("12:00").do(send_notification)

    while True:
        schedule.run_pending()
        time.sleep(1)
