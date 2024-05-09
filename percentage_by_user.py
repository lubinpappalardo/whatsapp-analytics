import re
from collections import defaultdict
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

with open('chat.txt', 'rb') as file:
    text_bytes = file.read()
    try:
        text = text_bytes.decode('utf-8')
    except UnicodeDecodeError:
        try:
            text = text_bytes.decode('latin-1')
        except UnicodeDecodeError:
            print("Could not decode the file content. Please check the encoding.")
            exit()

# Note: format of the exported chat vary between android and apple
pattern = r'(\d+/\d+/\d+), (\d+:\d+) - (.*?):'
timestamps_and_users = re.findall(pattern, text)

# List of users on the groupchat as saved in your contacts
users = []

# --------------------------------------------------------------------------------------------------------------------

timestamps_datetime = [datetime.strptime(f'{date} {time}', '%m/%d/%y %H:%M') for date, time, user in timestamps_and_users if user in users]
timestamps_datetime.sort()  # Sort the timestamps in chronological order

# Calculate the cumulative count of messages
cumulative_counts = []
count = 0
for timestamp in timestamps_datetime:
    count += 1
    cumulative_counts.append((timestamp, count))

cumulative_message_count = {timestamp: count for timestamp, count in cumulative_counts}

# --------------------------------------------------------------------------------------------------------------------

# Create a figure and axis
fig, ax = plt.subplots(figsize=(12, 10))

users_count = {user: 0 for user in users}

# Group messages by user and calculate cumulative counts
user_cumulative_counts = {}
for date, time, user in timestamps_and_users:
    if user not in users:
        continue
    if user not in user_cumulative_counts:
        user_cumulative_counts[user] = []
    users_count[user] += 1
    user_cumulative_counts[user].append((datetime.strptime(f'{date} {time}', '%m/%d/%y %H:%M'), users_count[user]))
    # add the timestamp with their latest count to the other users as well
    for other_user in users:
        if other_user != user:
            if other_user not in user_cumulative_counts:
                user_cumulative_counts[other_user] = []
            user_cumulative_counts[other_user].append((datetime.strptime(f'{date} {time}', '%m/%d/%y %H:%M'), users_count[other_user]))


# dictionary that maps each user to their final message count
user_final_counts = {}
for user, cumulative_counts in user_cumulative_counts.items():
    user_final_counts[user] = cumulative_counts[-1][1]

# sort the user_final_counts dictionary by values (message counts) in descending order
sorted_user_counts = sorted(user_final_counts.items(), key=lambda x: x[1], reverse=True)

# create a list of users ordered by their final message count
ordered_users = [user for user, _ in sorted_user_counts]

# Plot the data for each user
for user in ordered_users:
    if user in user_cumulative_counts:
        cumulative_counts = user_cumulative_counts[user]
        x = [timestamp for timestamp, _ in cumulative_counts]
        y = [(count / cumulative_message_count[timestamp] * 100) for timestamp, count in cumulative_counts]
        ax.plot(x, y, label=user)

# --------------------------------------------------------------------------------------------------------------------

# Set the x-axis to use date format
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Rotate the x-axis labels for better visibility
plt.xticks(rotation=45)

# Set labels and title
ax.set_xlabel('Time')
ax.set_ylabel('Chat Percentage')
ax.set_title('Chat Percentage Over Time by User')

# Add a legend
ax.legend(loc='upper left')

# Display the plot
plt.savefig('output/chat_percentage_by_user.png')
plt.show()   