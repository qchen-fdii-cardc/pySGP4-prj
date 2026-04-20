import pathlib
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt

# Radii in km
diff = 21  # difference between equatorial and polar radius in km
# adding a factor to exaggerate the difference for visualization
diff_visual = diff * 60
equatorial = 6378
polar = 6357
polar_visual = equatorial - diff_visual

fig, ax = plt.subplots(figsize=(6, 6))

# Draw ellipse for oblate Earth
earth = Ellipse((0, 0), 2*equatorial, 2*polar_visual,
                edgecolor='royalblue', facecolor='aliceblue', lw=2, label='Oblate Earth')
ax.add_patch(earth)

# Draw reference circle (mean of equatorial and polar) with different fill color
circle = plt.Circle((0, 0), polar_visual, color='lightcoral',
                    alpha=0.3, label='Reference Circle')
ax.add_patch(circle)

# Draw axes
ax.axhline(0, color='gray', linestyle='--', linewidth=1)
ax.axvline(0, color='gray', linestyle='--', linewidth=1)

# Draw equatorial and polar radii as lines
ax.plot([0, equatorial], [0, 0], color='blue', linewidth=2)
ax.plot([0, 0], [0, polar_visual], color='green', linewidth=2)


# Add text labels (no arrows)
ax.text(equatorial / 2, 100,
        f'{equatorial} km', fontsize=10, color='blue', ha='center')
ax.text(-200, polar_visual / 2,
        f'{polar} km', fontsize=10, color='green', ha='right')
ax.text(equatorial - 600, -600,
        f'{diff} km', fontsize=10, color='red', ha='center')


ax.text(0, polar_visual+200, "N", fontsize=16,
        color='black', ha='center', va='bottom')
ax.text(0, -polar_visual-200, "S", fontsize=16,
        color='black', ha='center', va='top')

ax.set_xlim(-6500, 6500)
ax.set_ylim(-6500, 6500)
ax.set_aspect('equal')
# ax.set_title('Oblate Earth: Equatorial vs Polar Radius')
ax.axis('off')
# ax.legend(loc='upper right')
# plt.show()

# Ensure imgs directory exists and save plot
img_dir = pathlib.Path(__file__).parent / ".." / "imgs"
img_dir = img_dir.resolve()
img_dir.mkdir(parents=True, exist_ok=True)
img_path = img_dir / "oblate_earth.png"
# save the plot to the specified path
plt.savefig(img_path)
print(f"Plot saved to: {img_path}")
