import re
from collections import Counter
from collections import defaultdict
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
pattern = r'(\d+/\d+/\d+), (\d+:\d+)'
timestamps = re.findall(pattern, text)

timestamps_datetime = [datetime.strptime(f'{date} {time}', '%m/%d/%y %H:%M') for date, time in timestamps]

# Group timestamps by date and count messages
date_counts = Counter(timestamp.date() for timestamp in timestamps_datetime)

# Create lists for the x and y axes
x = list(date_counts.keys())
y = list(date_counts.values())

# Create a figure and axis
fig, ax = plt.subplots(figsize=(12, 6))

# Plot the data
ax.plot(x, y)

# Set the x-axis to use date format
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Rotate the x-axis labels for better visibility
plt.xticks(rotation=45)

# Set labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Number of Messages')
ax.set_title('Message Count Per Day')

# Display the plot
plt.savefig('output/message_count_per_day.png')
plt.show()   
