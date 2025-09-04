import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Define steps
steps = [
    "1. Problem Definition",
    "2. Data Collection & Preparation",
    "3. Exploratory Data Analysis (EDA)",
    "4. Feature Engineering & Selection",
    "5. Model Development & Training",
    "6. Model Evaluation & Tuning",
    "7. Model Deployment",
    "8. Monitoring & Maintenance"
]

# Create figure
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

# Draw boxes for each step
box_height = 1.2
y = 11
for i, step in enumerate(steps):
    rect = patches.FancyBboxPatch((2, y - box_height), 6, box_height, 
                                  boxstyle="round,pad=0.2", 
                                  linewidth=1.5, edgecolor="black", facecolor="#a1d6ff")
    ax.add_patch(rect)
    ax.text(5, y - box_height/2, step, ha="center", va="center", fontsize=10, fontweight="bold")
    
    # Draw arrow to next step
    if i < len(steps) - 1:
        ax.arrow(5, y - box_height, 0, -0.6, head_width=0.2, head_length=0.2, 
                 fc="black", ec="black", length_includes_head=True)
    
    y -= 2

plt.title("AI/ML Life Cycle", fontsize=14, weight="bold", pad=20)
plt.show()
