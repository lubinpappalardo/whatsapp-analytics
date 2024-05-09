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
timestamp_counts = Counter(timestamps_datetime)

x = list(timestamp_counts.keys())
y = list(timestamp_counts.values())

timestamps_datetime = [datetime.strptime(f'{date} {time}', '%m/%d/%y %H:%M') for date, time in timestamps]
timestamps_datetime.sort()  # Sort the timestamps in chronological order

# Calculate the cumulative count of messages
cumulative_counts = []
count = 0
for timestamp in timestamps_datetime:
    count += 1
    cumulative_counts.append((timestamp, count))

# Create lists for the x and y axes
x = [timestamp for timestamp, _ in cumulative_counts]
y = [count for _, count in cumulative_counts]

# Create a figure and axis
fig, ax = plt.subplots(figsize=(12, 6))

# Plot the data
ax.plot(x, y)

# Set the x-axis to use date format
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(mdates.DayLocator())

# Rotate the x-axis labels for better visibility
plt.xticks(rotation=45)

# Set labels and title
ax.set_xlabel('Time')
ax.set_ylabel('Cumulative Message Count')
ax.set_title('Cumulative Message Count Over Time')

# Display the plot
plt.save("output/cumulative_message_count_over_time.png")
plt.show()   