def analyze_sequence(sequence):
   # Split the sequence into groups of 5 emojis
   groups = [sequence[i:i+5] for i in range(0, len(sequence), 5)]
   
   # Count the occurrences of each emoji
   emoji_counts = {}
   for group in groups:
       for emoji in group:
           if emoji in emoji_counts:
               emoji_counts[emoji] += 1
           else:
               emoji_counts[emoji] = 1
   
   # Find the most common emojis
   top_emojis = sorted(emoji_counts.items(), key=lambda x: x[1], reverse=True)[:5]
   
   print(f"Most common emojis:")
   for emoji, count in top_emojis:
       print(f"- {emoji}: {count}")

analyze_sequence("🙃🏹🦠🔮🔻🏴‍☠️🧮🥷🏻🤖🧪📱🎻🦠🗿⭕️")
