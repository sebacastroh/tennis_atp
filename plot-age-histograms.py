# -*- coding: utf-8 -*-
"""
Created on Thu May  5 21:29:26 2022

@author: sebac
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

plt.close('all')

players = pd.read_csv('atp_players.csv')

decades = ['70s', '80s', '90s', '00s', '10s', '20s']

year_count = 0
all_ages = []
years = []
for d, decade in enumerate(decades):
    rankings = pd.read_csv('atp_rankings_%s.csv' %decade)
    weeks = rankings['ranking_date'].unique()
    
    starting_year = int(str(weeks.min())[:4])
    ending_year = int(str(weeks.max())[:4])
    
    if decade == '70s':
        startweek = weeks.min()
        
    for y, year in enumerate(range(starting_year, ending_year+1)):
        years.append(int(str(startweek+10000*year_count)[:4]))
        selected_week = weeks[np.argmin(np.abs(weeks-(startweek+10000*year_count)))]
        year_count += 1
        
        ranks = rankings[(rankings['ranking_date'] == selected_week) & (rankings['rank'] <= 100)]
        merged = pd.merge(ranks, players, how='inner', left_on=['player'], right_on=['player_id'])
        filtered = merged['dob'].dropna()
        
        ages = selected_week - np.int64(filtered)
        all_ages.append(ages)
    

# Animation
HIST_BINS = np.arange(15, 46)

def prepare_animation(bar_container):

    def animate(frame_number):
        # simulate new data coming in
        data = all_ages[frame_number]
        
        n, _ = np.histogram(np.int64(data/10000), HIST_BINS)
        for count, rect in zip(n, bar_container.patches):
            rect.set_height(count)
        
        ttl.set_text('Year: %i' %years[frame_number])
        
        return bar_container.patches + [ttl]
    return animate


fig, ax = plt.subplots()
_, _, bar_container = ax.hist([], HIST_BINS, lw=1, ec='k')
ax.set_ylim(top=20)  # set safe limit to ensure that all data is visible.
ax.set_xlabel('Age')
ax.set_ylabel('Number of players (Top 100)')
ax.grid()
ttl = ax.text(.8, 0.9, '', transform = ax.transAxes, va='center')

ani = animation.FuncAnimation(fig, prepare_animation(bar_container), len(all_ages),
                              repeat=False, blit=True)
plt.show()

ani.save('ages.gif', writer='imagemagick', fps=60)