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
print(f"Total messages: {len(timestamps_and_users)}")

# List of users on the groupchat as saved in your contacts
users = []

# Group messages by user and calculate cumulative counts
user_cumulative_counts = {}
for date, time, user in timestamps_and_users:
    if user not in users:
        continue
    if user not in user_cumulative_counts:
        user_cumulative_counts[user] = []
    count = len(user_cumulative_counts[user])
    user_cumulative_counts[user].append((datetime.strptime(f'{date} {time}', '%m/%d/%y %H:%M'), count + 1))

# Create a figure and axis
fig, ax = plt.subplots(figsize=(12, 10))

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
        y = [count for _, count in cumulative_counts]
        print(f'{user}: {cumulative_counts[-1][1]} messages')
        ax.plot(x, y, label=user)

# --------------------------------------------------------------------------------------------------------------------

# Set the x-axis to use date format
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Rotate the x-axis labels for better visibility
plt.xticks(rotation=45)

# Set labels and title
ax.set_xlabel('Time')
ax.set_ylabel('Cumulative Message Count')
ax.set_title(f'Cumulative Message Count Over Time by User (Total: {len(timestamps_and_users)})')

# Add a legend
ax.legend(loc='upper left')

# Display the plot
plt.savefig('output/cumulative_message_count_by_user.png')
plt.show()   