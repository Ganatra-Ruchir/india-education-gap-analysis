"""Generate a 1080x1080 Instagram graphic summarising the project."""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "outputs"
OUT.mkdir(exist_ok=True)

INK = "#0f2a43"
ACCENT = "#e8873a"
TEAL = "#1f7a8c"
CREAM = "#faf6ee"

fig = plt.figure(figsize=(10.8, 10.8), dpi=100)
fig.patch.set_facecolor(CREAM)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# top accent band
ax.add_patch(patches.Rectangle((0, 88), 100, 12, facecolor=INK, zorder=1))
ax.text(6, 94, "SDG 4  ·  QUALITY EDUCATION", color=CREAM, fontsize=15,
        fontweight="bold", va="center", family="DejaVu Sans")

# headline
ax.text(6, 79, "What India's", color=INK, fontsize=44, fontweight="bold", va="center")
ax.text(6, 70, "classrooms", color=ACCENT, fontsize=44, fontweight="bold", va="center")
ax.text(6, 61, "tell us", color=INK, fontsize=44, fontweight="bold", va="center")

# three stat blocks
def stat(x, big, label, color):
    ax.text(x, 44, big, color=color, fontsize=40, fontweight="bold", ha="center", va="center")
    ax.text(x, 34, label, color=INK, fontsize=12.5, ha="center", va="center", wrap=True)

ax.add_patch(patches.Rectangle((5, 27), 90, 26, facecolor="white",
             edgecolor=INK, linewidth=1.5, zorder=1))
stat(22, "~30 pts", "gap between top and\nbottom states", TEAL)
stat(50, "27.9 pts", "widest male–female\nliteracy gap", ACCENT)
stat(78, "r = -0.74", "literacy tracks a\nsmaller gender gap", TEAL)

# bottom line
ax.text(6, 18, "Higher literacy states have smaller gender gaps.", color=INK,
        fontsize=15, fontweight="bold", va="center")
ax.text(6, 13.5, "Classroom crowding, though? No clear link to pass rates.", color=INK,
        fontsize=13, style="italic", va="center")

# footer
ax.add_patch(patches.Rectangle((0, 0), 100, 6, facecolor=INK, zorder=1))
ax.text(6, 3, "github.com/Ganatra-Ruchir", color=CREAM, fontsize=12,
        fontweight="bold", va="center")
ax.text(94, 3, "data analysis · open source", color=CREAM, fontsize=11,
        va="center", ha="right")

# small disclaimer
ax.text(94, 8.5, "real UDISE 2015-16 data", color="#888", fontsize=8.5,
        va="center", ha="right", style="italic")

plt.savefig(OUT / "instagram_post.png", facecolor=CREAM)
plt.close()
print(f"Wrote {OUT / 'instagram_post.png'}")
