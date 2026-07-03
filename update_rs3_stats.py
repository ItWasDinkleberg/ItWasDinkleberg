import urllib.request
import os

USERNAME = "shoote45"
API_URL = f"https://secure.runescape.com/m=hiscore/index_lite.ws?player={USERNAME}"

# Map exact RS3 Skills to Emojis to bypass GitHub SVG image blocking
SKILLS = [
    ("Overall", "🌟"), ("Attack", "⚔️"), ("Defence", "🛡️"), ("Strength", "💪"), 
    ("Constitution", "❤️"), ("Ranged", "🏹"), ("Prayer", "🙏"), ("Magic", "🔮"), 
    ("Cooking", "🍳"), ("Woodcutting", "🪓"), ("Fletching", "🪶"), ("Fishing", "🎣"),
    ("Firemaking", "🔥"), ("Crafting", "🧵"), ("Smithing", "🔨"), ("Mining", "⛏️"), 
    ("Herblore", "🧪"), ("Agility", "🏃"), ("Thieving", "🥷"), ("Slayer", "💀"), 
    ("Farming", "🌾"), ("Runecrafting", "🪨"), ("Hunter", "🐾"), ("Construction", "🏗️"),
    ("Summoning", "🐺"), ("Dungeoneering", "🗝️"), ("Divination", "👁️"), ("Invention", "⚙️"), 
    ("Archaeology", "🏺"), ("Necromancy", "👻")
]

def get_stats():
    print(f"Initiating uplink for {USERNAME}...")
    req = urllib.request.Request(API_URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = response.read().decode('utf-8').strip().split('\n')
        
        stats = {}
        for i, line in enumerate(data):
            if i < len(SKILLS):
                parts = line.split(',')
                if len(parts) >= 2:
                    stats[SKILLS[i][0]] = parts[1]
        return stats
    except Exception as e:
        print(f"Uplink failed: {e}")
        return None

def draw_svg(stats):
    if not stats: 
        return
        
    # Build the Classic RuneScape UI 
    svg = [
        '<svg width="500" height="420" xmlns="http://www.w3.org/2000/svg">',
        '<style>',
        '  .bg { fill: #382A1D; stroke: #554533; stroke-width: 4; rx: 6; ry: 6; }',
        '  .inner { fill: #291E13; stroke: #110C08; stroke-width: 2; rx: 4; ry: 4; }',
        '  .title { font-family: "Georgia", serif; font-size: 20px; fill: #FF981F; font-weight: bold; text-shadow: 2px 2px 0px #000; }',
        '  .txt { font-family: "Arial", sans-serif; font-size: 14px; fill: #E8D8A0; text-shadow: 1px 1px 0px #000; }',
        '  .val { fill: #FFD900; font-weight: bold; }',
        '  .emoji { font-size: 16px; }',
        '</style>',
        
        # Draw the backgrounds
        '<rect class="bg" width="100%" height="100%" />',
        '<rect class="inner" x="10" y="50" width="480" height="355" />',
        f'<text x="250" y="32" class="title" text-anchor="middle">Live Runescape Stats for {USERNAME}</text>'
    ]
    
    # Generate the grid array 
    x_start, y_start = 25, 80
    col_width, row_height = 115, 33
    col, row = 0, 0
    
    # Skip "Overall" in the loop
    for name, emoji in SKILLS[1:]:
        x_offset = x_start + (col * col_width)
        y_offset = y_start + (row * row_height)
        level = stats.get(name, "1")
        
        display = name[:4].upper()
        
        # Place Emoji and Text
        svg.append(f'<text x="{x_offset}" y="{y_offset}" class="emoji">{emoji}</text>')
        svg.append(f'<text x="{x_offset + 25}" y="{y_offset - 2}" class="txt">{display}: <tspan class="val">{level}</tspan></text>')
        
        col += 1
        if col >= 4:
            col = 0
            row += 1
            
    # Append the Overall Total Level at the bottom
    total = stats.get("Overall", "0")
    total_y = y_start + (row * row_height) + 15
    svg.append(f'<line x1="15" y1="{total_y}" x2="485" y2="{total_y}" stroke="#110C08" stroke-width="2" />')
    svg.append(f'<line x1="15" y1="{total_y + 2}" x2="485" y2="{total_y + 2}" stroke="#554533" stroke-width="1" />')
    
    # Pushed y from +25 to +45 to center it vertically in the lower panel
    svg.append(f'<text x="250" y="{total_y + 45}" class="title" text-anchor="middle" fill="#FFD900">Total Level: {total}</text>')
    
    svg.append('</svg>')
    
    with open("rs3_stats.svg", "w", encoding="utf-8") as f:
        f.write('\n'.join(svg))
    print("RS interface graphic generated.")

if __name__ == "__main__":
    draw_svg(get_stats())
