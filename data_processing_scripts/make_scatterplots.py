import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl
import numpy as np
from scipy.spatial.distance import pdist, squareform
 
# ── Example data ─────────────────────────────────────────────────────────────
# Replace these DataFrames with your actual data.
# Each DataFrame must have:
#   - index (or a column) with POS tag names
#   - a column named 'residual' with the chi-squared residual value
 
"""
# default prompt upos:
english_residuals = pd.DataFrame({
    'pos': ["NOUN", "PUNCT", "CCONJ", "ADJ", "VERB", "INTJ", "SYM", "PROPN", "X", "ADP", "NUM", "PART", "SCONJ", "ADV", "DET", "PRON", "AUX"],
    'residual': [37.89163109, 35.13848625, 20.04966371, 14.63385417, 2.564737572, -1.102748951, -4.735049331, -6.133730691, -8.316885752, -10.79006926, -11.21841485, -16.66581884, -20.41746157, -22.18562172, -29.00986232, -33.33574059, -35.13754958]
}).set_index('pos')
 
slovenian_residuals = pd.DataFrame({
    'pos': ["NOUN", "PUNCT", "CCONJ", "ADJ", "VERB", "INTJ", "SYM", "PROPN", "X", "ADP", "NUM", "PART", "SCONJ", "ADV", "DET", "PRON", "AUX"],
    'residual': [74.31904263, 27.88919254, -1.343601127, 33.39025678, -28.4487277, 1.978702907, -17.37762888, -34.66643186, -9.31030522, 1.496315582, -4.858120266, -18.52352694, -3.681497837, -24.42949464, -35.01960771, -42.34379542, -52.44881086]
}).set_index('pos')
"""

# map_g prompt upos:
english_residuals = pd.DataFrame({
    'pos': ["PUNCT", "NOUN", "CCONJ", "ADJ", "VERB", "PROPN", "INTJ", "SYM", "ADP", "X", "ADV", "NUM", "PART", "SCONJ", "PRON", "DET", "AUX"],
    'residual': [30.92795232, 23.10134918, 15.8974376, 7.412752957, 3.400571428, -0.9176679324, -1.524910759, -6.340245589, -7.35740837, -8.902998385, -11.47614852, -12.23062667, -14.83928415, -15.29808745, -18.55959746, -18.92605808, -27.34944399]
}).set_index('pos')
 
slovenian_residuals = pd.DataFrame({
    'pos': ["PUNCT", "NOUN", "CCONJ", "ADJ", "VERB", "PROPN", "INTJ", "SYM", "ADP", "X", "ADV", "NUM", "PART", "SCONJ", "PRON", "DET", "AUX"],
    'residual': [33.24679383, 41.77411629, -6.515839064, 10.84303945, -13.80561285, -32.35038383, 1.369211089, -17.77586691, -0.2631210305, -11.7136574, -5.267440828, -0.993568496, -6.213743085, 10.6521357, -19.61474365, -25.73740057, -45.20474687]
}).set_index('pos')

"""
# default prompt deprel:
english_residuals = pd.DataFrame({
    'pos': ["amod", "nmod", "conj", "punct", "parataxis", "appos", "nsubj", "acl", "cc", "cc:preconj", "case", "cop", "orphan", "goeswith", "vocative", "list", "nummod", "csubj", "discourse", "fixed", "mark", "flat", "advcl", "ccomp", "obl", "obj", "expl", "xcomp", "root", "iobj", "det", "advmod", "aux"],
    'residual': [24.90587128, -6.751471136, 36.29985916, 35.2698401, 4.445738081, 6.135944761, -0.7440775904, -2.92336092, 19.48332074, 3.190637741, -5.976759419, -14.98438235, 0.9435610643, -0.8727430409, -1.059822361, 0.9820333643, -8.427594737, -4.584562299, -1.35942009, -10.00466154, -26.56953098, -3.429724878, -7.037350391, -13.10859755, -2.464057952, 15.69737251, -21.31351844, -16.22154192, 1.183791934, -2.335993462, -28.32673928, -23.9064853, -24.70990956]
}).set_index('pos')
 
slovenian_residuals = pd.DataFrame({
    'pos': ["amod", "nmod", "conj", "punct", "parataxis", "appos", "nsubj", "acl", "cc", "cc:preconj", "case", "cop", "orphan", "goeswith", "vocative", "list", "nummod", "csubj", "discourse", "fixed", "mark", "flat", "advcl", "ccomp", "obl", "obj", "expl", "xcomp", "root", "iobj", "det", "advmod", "aux"],
    'residual': [37.03460117, 33.30563585, 32.07436282, 27.77062689, 22.68671161, 18.78160354, 18.56271832, 12.21913769, 6.689237894, 5.70326232, 4.902657253, 3.723790099, 3.450337014, 1.376869903, -1.452578671, -1.463321538, -2.570049919, -4.208048605, -4.530730825, -6.772280788, -7.898445212, -9.446998855, -12.92135885, -13.80156556, -14.8276271, -16.93768352, -17.82310233, -17.87473111, -20.59248883, -22.26881957, -25.89516596, -40.15780648, -80.22817791]
}).set_index('pos')
"""

"""
# map_g prompt deprel:
english_residuals = pd.DataFrame({
    'pos': ["punct", "parataxis", "conj", "acl", "appos", "nsubj", "amod", "mark", "orphan", "nmod", "cop", "csubj", "case", "cc:preconj", "advcl", "goeswith", "nummod", "cc", "vocative", "fixed", "list", "ccomp", "discourse", "flat", "expl", "obl", "xcomp", "obj", "iobj", "root", "advmod", "det", "aux"],
    'residual': [31.0249575, 8.996958739, 28.22193039, -3.521283684, 3.886648685, 5.60785865, 13.2943078, -21.18356939, 0.9493631779, -8.511118341, -10.70161349, -1.781810059, -4.508411053, 2.798665811, -7.663252298, -1.762587581, -10.31801919, 15.57507733, -1.053345216, -8.828035528, -0.103983155, -7.522610346, -2.400278578, -3.697975612, -14.88799435, 1.679674257, -11.93999392, 9.004388909, -2.755483298, 2.599097871, -13.13427624, -18.42494437, -20.57200234]
}).set_index('pos')
 
slovenian_residuals = pd.DataFrame({
    'pos': ["punct", "parataxis", "conj", "acl", "appos", "nsubj", "amod", "mark", "orphan", "nmod", "cop", "csubj", "case", "cc:preconj", "advcl", "goeswith", "nummod", "cc", "vocative", "fixed", "list", "ccomp", "discourse", "flat", "expl", "obl", "xcomp", "obj", "iobj", "root", "advmod", "det", "aux"],
    'residual': [33.10159623, 21.1759573, 21.11109338, 15.28202835, 14.26442334, 13.65211599, 10.12883829, 8.597412554, 6.377559846, 6.040961053, 4.952108898, 2.970779881, 2.374903112, 2.197467632, 1.840514278, 0.947131179, 0.5579802881, -0.467735004, -0.6723348778, -1.597801538, -3.223301221, -5.008267505, -5.075837723, -9.885441697, -10.84965824, -12.65272816, -13.22757049, -13.43574698, -14.2559575, -16.53263751, -16.96229227, -21.37106821, -69.79669341]
}).set_index('pos')
"""

# ── Merge ─────────────────────────────────────────────────────────────────────
df = pd.DataFrame({
    'english': english_residuals['residual'],
    'slovenian': slovenian_residuals['residual'],
})
 
# ── Classify each POS tag ─────────────────────────────────────────────────────
def classify(row):
    """Both positive → more in AIGT; both negative → less in AIGT; mixed → language-specific."""
    if row['english'] > 0 and row['slovenian'] > 0:
        return 'aigt_more'
    elif row['english'] < 0 and row['slovenian'] < 0:
        return 'aigt_less'
    else:
        return 'specific'
 
df['category'] = df.apply(classify, axis=1)
 
# ── Gradient colour based on diagonal position ────────────────────────────────
df['score'] = df['english'] + df['slovenian']
norm = mpl.colors.Normalize(df['score'].min(), df['score'].max())
cmap = mpl.colors.LinearSegmentedColormap.from_list('blue_green', ["#0d58bb", "#29a043"])

# ── Code for making labels display only when not too crowded ──────────────────

def get_labels_to_show(df, x_col, y_col, min_dist=1.5):
    """
    Only label a point if it is at least min_dist away from all
    already-labelled points. Points are processed in order of
    increasing local density (least crowded first get priority).
    """
    coords = df[[x_col, y_col]].values
    dist_matrix = squareform(pdist(coords))
    
    # Rank by local density (sum of distances to all neighbours)
    # — least crowded points get labelled first
    density = dist_matrix.sum(axis=1)
    order = np.argsort(-density)  # descending: isolated points first
    
    labelled_coords = []
    show_label = np.zeros(len(df), dtype=bool)
    
    for i in order:
        if not labelled_coords:
            show_label[i] = True
            labelled_coords.append(coords[i])
        else:
            dists = [np.linalg.norm(coords[i] - c) for c in labelled_coords]
            if min(dists) >= min_dist:
                show_label[i] = True
                labelled_coords.append(coords[i])
    
    return show_label

show_label = get_labels_to_show(df, 'english', 'slovenian', min_dist=4.3)
 
# ── Plot ───────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
 
for idx, (pos, row) in enumerate(df.iterrows()):
    color = cmap(norm(row['score']))
    if row['category'] == 'specific':
        ax.scatter(
            row['english'], row['slovenian'],
            facecolors='none',
            edgecolors=[color],
            marker='o',
            linewidths=1.5,
            s=70,
            zorder=4,
        )
    else:
        ax.scatter(
            row['english'], row['slovenian'],
            color=[color],
            marker='o',
            s=70,
            zorder=3,
        )
    if show_label[idx]:
        ax.annotate(
            pos,
            xy=(row['english'], row['slovenian']),
            xytext=(4, 3),
            textcoords='offset points',
            fontsize=12,
            color='#222222',
        )
 
# Reference lines at 0
ax.axhline(0, color='#aaaaaa', linewidth=0.8, linestyle='--', zorder=1)
ax.axvline(0, color='#aaaaaa', linewidth=0.8, linestyle='--', zorder=1)
 
# Axis labels
ax.set_xlabel('English: Part-of-speech Tag χ2 Residual', fontsize=16)
ax.set_ylabel('Slovenian: Part-of-speech Tag χ2 Residual', fontsize=16)
 
# Colorbar
sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, fraction=0.03, pad=0.02)
cbar.set_label('← Less in AIGT   |   More in AIGT →', fontsize=16)
 
# Legend
legend_handles = [
    mpatches.Patch(color="#7dcb64", label='More in AIGT (both languages)'),
    mpatches.Patch(color="#696bdf", label='Less in AIGT (both languages)'),
    plt.Line2D([0], [0], marker='o', color='#555555', linestyle='None',
               markersize=8, markerfacecolor='none', markeredgewidth=1.5,
               label='Language-specific distribution'),
]
ax.legend(handles=legend_handles, fontsize=12, loc='lower right',
          framealpha=0.9, edgecolor='#cccccc')
 
ax.tick_params(labelsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
 
plt.tight_layout()
plt.savefig('pos_chisq_scatter_map_g.svg', dpi=150, bbox_inches='tight')
plt.savefig('pos_chisq_scatter_map_g.png', dpi=150, bbox_inches='tight')
plt.show()
