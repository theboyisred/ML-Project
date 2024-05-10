from pandas import DataFrame
from sklearn.cluster import MiniBatchKMeans
from matplotlib.figure import Figure
import seaborn as sns

def preprocessor(data: dict):
    # Convert data to a DataFrame
    DF = DataFrame([data])
    Xcol = DF.fillna(0)

    # Cluster the data
    kmeans = MiniBatchKMeans(n_clusters=1, random_state=0,
                             batch_size=100, max_iter=100, n_init=3).fit(Xcol)
    one = kmeans.cluster_centers_[0]
    print(one)
    # Calculate personality traits scores
    personality_traits = {}    
    personality_traits['Openness_score'] = one[40] - one[41] + one[42] - one[43] + one[44] - one[45] + one[46] + one[47] + one[48] + one[49]
    personality_traits['Conscientiousness_score'] = one[30] - one[31] + one[32] - one[33] + one[34] - one[35] + one[36] - one[37] + one[38] + one[39]
    personality_traits['Extroversion_score'] = one[0] - one[1] + one[2] - one[3] + one[4] - one[5] + one[6] - one[7] + one[8] - one[9]
    personality_traits['Agreeableness_score'] = -one[20] + one[21] - one[22] + one[23] - one[24] - one[25] + one[26] - one[27] + one[28] + one[29]
    personality_traits['Neuroticism_score'] = one[10] - one[11] + one[12] - one[13] + one[14] + one[15] + one[16] - one[17] + one[18] + one[19]

    # Normalize the data
    nmlzd_personality_traits = {}
    for key, value in personality_traits.items():
        nmlzd_personality_traits[key] = (value - min(personality_traits.values())) / (max(personality_traits.values()) - min(personality_traits.values()))

    # Plot the personality scores
    keys = list(nmlzd_personality_traits.keys())
    values = list(nmlzd_personality_traits.values())
    _values = values.copy()
    _values[1] *= -1
    # Set the style
    sns.set_style("whitegrid")

    # Increase figure size and DPI
    fig = Figure(figsize=(12, 8), dpi=120)

    ax = fig.add_subplot(1, 1, 1)

    # Use Seaborn's barplot
    sns.barplot(x=keys, y=values, color='red', alpha=0.9, ax=ax)  # Set alpha for transparency
    ax.set_ylim(0, 1)
    ax.set_xticklabels(keys, rotation=45, fontsize=12)  # Rotate x-axis labels for better readability
    ax.set_xlabel('Personality Traits', fontsize=14)
    ax.set_ylabel('Normalized Scores', fontsize=14)
    ax.set_title('Normalized Personality Scores', fontsize=16)
    fig.tight_layout()  # Adjust layout to prevent clipping of labels

    return fig, sum(_values)