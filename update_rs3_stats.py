import urllib.request
import os

USERNAME = "shoote45"
API_URL = f"https://secure.runescape.com/m=hiscore/index_lite.ws?player={USERNAME}"

# Exact RS3 Skills list mapped to the API return order
SKILLS = [
    "Overall", "Attack", "Defence", "Strength", "Constitution", "Ranged",
    "Prayer", "Magic", "Cooking", "Woodcutting", "Fletching", "Fishing",
    "Firemaking", "Crafting", "Smithing", "Mining", "Herblore", "Agility",
    "Thieving", "Slayer", "Farming", "Runecrafting", "Hunter", "Construction",
    "Summoning", "Dungeoneering", "Divination", "Invention", "Archaeology", "Necromancy"
]

def get_stats():
    print(f"Initiating uplink for {USERNAME}...")
    req = urllib.request.Request(API_URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            # API returns a comma-separated list of ranks, levels, and xp per skill per line
            data = response.read().decode('utf-8').strip().split('\n')
        
        stats = {}
        for i, line in enumerate(data):
            if i < len(SKILLS):
                parts = line.split(',')
                if len(parts) >= 2:
                    stats[SKILLS[i]] = parts[1] # Index 1 is the actual level
        return stats
    except Exception as e:
        print(f"Uplink failed: {e}")
        return None

def draw_svg(stats):
    if not stats: 
        return
        
    # Build a raw SVG mimicking our darknet terminal layout
    svg = [
        '<svg width="500" height="380" xmlns="http://www.w3.org/2000/svg">',
        '<style>',
        '  .bg { fill: #0d1117; stroke: #30363d; stroke-width: 2; rx: 8; ry: 8; }',
        '  .hdr { font-family: Courier, monospace; font-size: 16px; fill: #3fb950; font-weight: bold; }',
        '  .txt { font-family: Courier, monospace; font-size: 13px; fill: #8b949e; }',
        '  .val { fill: #c9d1d9; font-weight: bold; }',
        '</style>',
        '<rect class="bg" width="100%" height="100%" />',
        f'<text x="20" y="30" class="hdr">&gt; RS3_UPLINK --target {USERNAME}</text>',
        '<text x="20" y="50" class="hdr" fill="#00ff00">&gt; STATUS: ALIVE</text>',
        '<line x1="20" y1="65" x2="480" y2="65" stroke="#30363d" stroke-width="1" />'
    ]
    
    # Generate the grid array for the 29 individual skills
    x_start, y_start = 20, 95
    col_width, row_height = 115, 25
    col, y_offset = 0, y_start
    
    # Skip "Overall" in the main loop to handle it at the bottom
    for skill in SKILLS[1:]:
        x_offset = x_start + (col * col_width)
        level = stats.get(skill, "1")
        
        # Abbreviate to 4 characters for clean grid alignment
        display = skill[:4].upper()
        
        svg.append(f'<text x="{x_offset}" y="{y_offset}" class="txt">{display}: <tspan class="val">{level}</tspan></text>')
        
        col += 1
        if col >= 4:
            col = 0
            y_offset += row_height
            
    # Append the Overall Total Level
    total = stats.get("Overall", "0")
    svg.append(f'<line x1="20" y1="{y_offset + 10}" x2="480" y2="{y_offset + 10}" stroke="#30363d" stroke-width="1" />')
    svg.append(f'<text x="20" y="{y_offset + 35}" class="hdr" fill="#58a6ff">&gt; SYS.TOTAL_LVL : {total}</text>')
    
    svg.append('</svg>')
    
    # Save the file to the current working directory
    with open("rs3_stats.svg", "w") as f:
        f.write('\n'.join(svg))
    print("Telemetry graphic generated.")

if __name__ == "__main__":
    draw_svg(get_stats())
