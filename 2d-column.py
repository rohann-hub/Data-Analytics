import numpy as np
import pandas as pd
import IPython.display as display
from matplotlib import pyplot as plt
import io
import base64


index = pd.MultiIndex.from_product(
    [['North', 'South', 'East', 'West'], ['Laptops', 'Mobiles', 'Televisions']],
    names=['Region', 'Product']
)


sales_data = [50000, 75000, 30000, 40000, 65000, 25000, 
              55000, 80000, 35000, 45000, 70000, 28000]

df = pd.DataFrame({'Sales': sales_data}, index=index)

# Reshape the DataFrame into a 2D column format
df_2d = df.unstack(level='Product')  # Unstack the 'Product' level to columns

# Display the 2D DataFrame
display.display(df_2d)

# Create a 2D column visualization (bar chart)
fig, ax = plt.subplots(figsize=(10, 6))

# Get the regions and products
regions = df_2d.index
products = df_2d.columns.levels[1]  # Get the product names

# Plot settings
bar_width = 0.2
x = np.arange(len(regions))

# Plot bars for each product
for i, product in enumerate(products):
    ax.bar(x + i * bar_width, df_2d[('Sales', product)], width=bar_width, label=product)

# Customize the plot
ax.set_xlabel('Region', fontsize=12)
ax.set_ylabel('Sales', fontsize=12)
ax.set_title('Sales by Region and Product', fontsize=14)
ax.set_xticks(x + bar_width)
ax.set_xticklabels(regions, rotation=45, ha='right')
ax.legend(title='Product')
ax.grid(True, linestyle='--', alpha=0.6)

# Save the plot as an image
data = io.BytesIO()
plt.savefig(data, format='png', bbox_inches='tight')
image = f"data:image/png;base64,{base64.b64encode(data.getvalue()).decode()}"
alt = "2D Column Visualization"
display.display(display.Markdown(f"""![{alt}]({image})"""))
plt.close(fig)
