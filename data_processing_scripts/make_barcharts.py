import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Recreate your data structure
data = {
    'Metric': ['Lexical Diversity', '3-Gram Diversity', 'Syntactic Diversity', 'Syntactic Complexity'],
    "GPT-5": [-3.28, -0.59, 1.67, -0.55],
    "GPT-5_low": [-3.63, -0.84, 1.46, -0.58],
    "GPT-5_high": [-3, -0.37, 1.92, -0.52],
    'GaMS3-12b': [1.61, 1.46, 1.86, -0.7],
    'GaMS3_low': [1.29, 1.32, 1.7, -0.73],
    'GaMS3_high': [1.98, 1.63, 2.08, -0.67],
    'gemma-3-12b': [0.44, 2.05, 2.08, -0.72],
    'gemma3_low': [0.21, 1.79, 1.85, -0.75],
    'gemma3_high': [0.7, 2.37, 2.35, -0.69],
    "GaMS-27b": [1.08, 2.41, 2.22, -0.81],
    "GaMS-27b_low": [0.68, 2.03, 1.78, -0.85],
    "GaMS-27b_high": [1.62, 3, 2.78, -0.76],
    "GaMS-27b-Nemotron": [1.29, 1.42, 2.05, -0.69],
    "Nemotron_low": [0.84, 1.21, 1.77, -0.72],
    "Nemotron_high": [1.79, 1.79, 2.47, -0.66],
    "gemma-2-27b": [0.2, 2.36, 1.53, -0.76],
    "gemma2_low": [-0.07, 2.06, 1.16, -0.79],
    "gemma2_high": [0.49, 2.74, 1.97, -0.73]
}
"""
data = {
    'Metric': ['Lexical Diversity', '3-Gram Diversity*', 'Syntactic Diversity*', 'Syntactic Complexity'],
    'Value': [-0.81, -0.56, -0.33, -0.09],
    'CI_low': [-1.2, -0.96, -0.66, 0.03],
    'CI_high': [-0.44, -0.16, 0.02, 0.14]
}
"""

df = pd.DataFrame(data)

# 2. Calculate Asymmetric Errors
# Format must be a 2xN array: [[lower_offsets], [upper_offsets]]
err_gpt = [
    abs(df['GPT-5'] - df['GPT-5_low']), 
    abs(df['GPT-5_high'] - df['GPT-5'])  
]

err_gams3 = [
    abs(df['GaMS3-12b'] - df['GaMS3_low']), 
    abs(df['GaMS3_high'] - df['GaMS3-12b']) 
]

err_gemma3 = [
    abs(df['gemma-3-12b'] - df['gemma3_low']),
    abs(df['gemma3_high'] - df['gemma-3-12b'])
]

err_gams2 = [
    abs(df['GaMS-27b'] - df['GaMS-27b_low']),
    abs(df['GaMS-27b_high'] - df['GaMS-27b'])
]

err_nemotron = [
    abs(df['GaMS-27b-Nemotron'] - df['Nemotron_low']),
    abs(df['Nemotron_high'] - df['GaMS-27b-Nemotron'])
]

err_gemma2 = [
    abs(df['gemma-2-27b'] - df['gemma2_low']),
    abs(df['gemma2_high'] - df['gemma-2-27b'])
]

"""
error = [
    abs(df['Value'] - df['CI_low']), # Distance down
    abs(df['CI_high'] - df['Value'])  # Distance up
]
"""

# 3. Plotting
n_bars = 6
group_width = 0.8  # Total space occupied by the 6 bars
bar_width = group_width / n_bars
x = np.arange(len(df['Metric']))

fig, ax = plt.subplots(figsize=(14, 7)) # Widened for 6 bars

base_offset = x - (group_width / 2) + (bar_width / 2)

# Plot bars with yerr (y-error)
rects1 = ax.bar(base_offset + 0*bar_width, df['GPT-5'], bar_width, label='GPT-5', 
                color="#B42F90", yerr=err_gpt, capsize=3)

rects2 = ax.bar(base_offset + 1*bar_width, df['GaMS-27b'], bar_width, label='GaMS-27b', 
                color="#BB4F2B", yerr=err_gams2, capsize=3)

rects3 = ax.bar(base_offset + 2*bar_width, df['GaMS-27b-Nemotron'], bar_width, label='GaMS-27b-Nemotron', 
                color="#C37B29", yerr=err_nemotron, capsize=3)

rects4 = ax.bar(base_offset + 3*bar_width, df['GaMS3-12b'], bar_width, label='GaMS3-12b', 
                color="#D5D144", yerr=err_gams3, capsize=3)

rects5 = ax.bar(base_offset + 4*bar_width, df['gemma-2-27b'], bar_width, label='gemma-2-27b', 
                color="#712DD6", yerr=err_gemma2, capsize=3)

rects6 = ax.bar(base_offset + 5*bar_width, df['gemma-3-12b'], bar_width, label='gemma-3-12b', 
                color="#2D95D6", yerr=err_gemma3, capsize=3)

"""
bars = ax.bar(x - width/2, df['Value'], width, 
                color="#60B524", yerr=error, capsize=5)
"""               

# 4. Styling
ax.set_ylabel("Cohen's d")
ax.set_title("Cohen's d Comparison for Human vs. Various Models")
ax.set_xticks(x)
ax.set_xticklabels(df['Metric'])
ax.legend()
ax.axhline(0, color='black', linewidth=0.8) # Line at zero for readability

plt.tight_layout()
plt.savefig("effect_sizes_human-v-models")