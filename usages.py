import math
import matplotlib.pyplot as plt
import os
import pandas as pd

# Tanium column containing application names
name_col = 'Name'
# Tanium column containing usage levels
usage_col = 'Usage'
# Tanium columns containing Agency IDs and Mission Areas
id_cols = [
    'Asset - Custom Tags.2.1',
    'Asset - Custom Tags.2.2.1',
    'Asset - Custom Tags.2.2.2.1',
    'Asset - Custom Tags.2.2.2.2.1',
    'Asset - Custom Tags.2.2.2.2.2.1',
    'Asset - Custom Tags.2.2.2.2.2.2.1',
    'Asset - Custom Tags.2.2.2.2.2.2.2.1',
    'Asset - Custom Tags.2.2.2.2.2.2.2.2.2.1'
]

# Read Tanium data as DataFrame df
print('Importing Tanium dataset')
df = pd.read_excel('tanium.xlsx')

print('Preparing data')

# Remove entries with invalid usage levels and remove duplicates
valid_usages = ['Usage not detected', 'Limited', 'Normal', 'High']
df = df[df[usage_col].isin(valid_usages)].drop_duplicates()

# Make usage column categorical to order properly
df[usage_col] = \
    df[usage_col].astype('category').cat.set_categories(valid_usages)

# Remove timestamps from some application names
df.loc[:, name_col] = df[name_col].str.replace(
    pat=' \d{4}\/\d{2}\/\d{2}-\d{2}:\d{2}:\d{2}',
    repl='',
    regex=True
    )

# Save all unique Mission Areas and Agency IDs into Set tags
tags = set()
for column in id_cols:
    tags.update(df[column].dropna().unique())

# Make folders to store data and figures
os.makedirs('./usage_data', exist_ok=True)
os.makedirs('./figures', exist_ok=True)

# Iterate through tags and create DataFrames and visualizations
for progress, tag in enumerate(tags, 1):
    print(f'Processing tag: {tag} ({progress}/{len(tags)})')

    # 'tag_indicator' signals if a row has the given tag
    df['tag_indicator'] = False
    for column in id_cols:
        df.loc[df[column] == tag, 'tag_indicator'] = True

    # Group df by application name and usage for current tag
    df_tag = df.loc[df['tag_indicator']].groupby([name_col, usage_col])\
        .size().reset_index()
    df_tag.rename(columns={df_tag.columns[2]: 'Frequency'}, inplace=True)

    # Get frequency of usages for each software
    softwares = list(df_tag[name_col].dropna().unique())
    frequencies = [
        df_tag.loc[df_tag[name_col] == software, 'Frequency']
        for software in softwares
    ]

    # Colors for visualizations, order is important
    colors = [
        '#e15759', # Usage not detected, Tableau T10 red
        '#f28e2b', # Limited,            Tableau T10 orange
        '#edc949', # Normal,             Tableau T10 yellow
        '#59a14e', # High,               Tableau T10 green
    ]

    if len(softwares) > 0:
        # Generate figure with square grid of subplots
        n = max(math.ceil(math.sqrt(len(softwares))), 2)
        fig, axs = plt.subplots(
            nrows=n, ncols=n, squeeze=False, figsize=(n * 4, n * 4)
            )
        fig.suptitle(tag + ' Usage by Software', fontsize=n * 6)
        axs = axs.flat

        # Create one legend for all subplots
        handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in colors]
        fig.legend(handles, valid_usages, loc='upper right', fontsize=n * 3)

        # Remove all extra subplots
        for ax in axs[len(softwares):]:
            ax.remove()

        # Create bar charts and export as PNGs
        for i, software in enumerate(softwares):
            axs[i].set_title(software)
            axs[i].bar(valid_usages, frequencies[i], color=colors)
            axs[i].xaxis.set_ticklabels([])
            axs[i].set_xlabel('Usage')
            axs[i].set_ylabel('Frequency')
        fig.tight_layout(rect=[0, 0, 1, 0.93])
        fig.savefig('./figures/' + tag + '_bar.png')

        # Create pie charts and export as PNGs
        for i, software in enumerate(softwares):
            axs[i].clear()
            axs[i].set_title(software)
            axs[i].pie(frequencies[i], colors=colors)
            axs[i].axis('Equal')
        fig.tight_layout(rect=[0, 0, 1, 0.93])
        fig.savefig('./figures/' + tag + '_pie.png')
        plt.close()
    
    # Pivot the DataFrame to display the software usage by usage levels
    df_tag.pivot(index=name_col, columns=usage_col, values='Frequency') \
        .to_excel('./usage_data/' + tag + '_usage.xlsx')
