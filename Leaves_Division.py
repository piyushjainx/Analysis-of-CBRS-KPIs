import calendar
import matplotlib
from matplotlib.lines import Line2D
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.serif'] = 'Times New Roman'
matplotlib.rcParams['font.size'] = 10

KpiPath = "KPIcombined80%.csv"
WeatherKpi = "Weather_updated.csv"

# temperature (degC)	
# relative_humidity (0-1)	
# wind_speed (m/s)	
# surface_pressure (Pa)	
# total_precipitation (mm of water equivalent) 
# snowfall (mm of water equivalent)
# absolute_humidity (g/m^3)

df = pd.read_csv(KpiPath)
df['coll_time_round'] = pd.to_datetime(df['coll_time_round'])
df.set_index('coll_time_round', inplace=True)

# Read the weather data
weather_df = pd.read_csv(WeatherKpi)
weather_df['datetime (UTC)'] = pd.to_datetime(weather_df['datetime (UTC)'])
weather_df.set_index('datetime (UTC)', inplace=True)

# Merge the dataframes
merged_df = pd.merge_asof(df, weather_df, left_index=True, right_index=True, direction='nearest')
print("test",weather_df.index.isnull().sum())

# Filter out non-numeric columns
merged_df = merged_df.select_dtypes(include='number')

# Take the average of Avg Rsrp values for each hour
merged_df = merged_df.groupby(merged_df.index).mean()

# Save the merged DataFrame to a CSV file
csv_output_path = '/Users/piyushjain/Desktop/WN4SS Lab/KPI_combined_80%.csv'
merged_df.to_csv(csv_output_path, index=True)  # Set index=True if you want to include the datetime index in the CSV file

# start, end = '2022-10-10', '2022-11-12' 
# merged_df = merged_df.loc[start:end]

# Calculate moving averages for both columns
rolling_avg_rsrp = merged_df['mean_AvgRsrp'].rolling(window=168).mean()  # window by hours
rolling_avg_temp = merged_df['temperature (degC)'].rolling(window=168).mean()
 
def get_rolling_average_data():
    return rolling_avg_rsrp, rolling_avg_temp

# Plot the results
fig, ax = plt.subplots()
ax2 = ax.twinx()

prev_month = merged_df.index[0].week
start_idx = merged_df.index[0]

for idx in merged_df.index[1:]:
    current_month = idx.week
    if current_month != prev_month:
        sinr_segment = rolling_avg_rsrp[start_idx:idx]
        temp_segment = rolling_avg_temp[start_idx:idx]
        if prev_month in list(range(49,52)) + list(range(1,12)):
            color = 'red'
            label = 'No leaves: Dec-Mar'
        elif prev_month in list(range(13,17)) + list(range(44,48)):
            color = 'blue'
            label = 'Some leaves: Apr, Nov'
        elif prev_month in list(range(18,43)):
            color = 'green'
            label = 'Likely leaves: May-Oct'

        ax.plot(sinr_segment.index, sinr_segment, color=color, label=label, linewidth= 5)
        ax2.plot(temp_segment.index, temp_segment, color="gray", linewidth= 5)
        
        start_idx = idx
        prev_month = current_month

# Plot the last segment
sinr_segment = rolling_avg_rsrp[start_idx:]
temp_segment = rolling_avg_temp[start_idx:]

#if prev_month in [12, 1, 2, 3]:
if prev_month in list(range(49,52)) + list(range(1,12)):
    color = 'red'
    label = 'NL: Dec-Mar'
#elif prev_month in [4, 11, 10]:
elif prev_month in list(range(13,17)) + list(range(44,48)):
    color = 'blue'
    label = 'SL: Apr, Oct-Nov'
elif prev_month in list(range(18,43)):
    color = 'green'
    label = 'LL: May-Oct'

ax.plot(sinr_segment.index, sinr_segment, color=color, label=label, linewidth= 5)
ax2.plot(temp_segment.index, temp_segment, color="gray",  linewidth= 5)

legend_elements = [Line2D([0], [0], color='green', label='RSRP: LL: May-Oct', linewidth= 5),
                   Line2D([0], [0], color='blue', label='RSRP: SL: Apr, Oct-Nov', linewidth= 5),
                   Line2D([0], [0], color='red', label='RSRP: NL: Dec-Mar', linewidth= 5),
                   Line2D([0], [0], color='gray', label='Temperature', linewidth= 5)]

ax.legend(handles=legend_elements, loc='best', ncol=2, columnspacing=1.0, fontsize=18)

#ax.set_title(' 7 Day Moving Average of RSRP and Temperature over Time', fontsize=20)
ax.set_xlabel('Date', fontsize=22)
ax.set_ylabel('Avg RSRP (dBm)', fontsize=28)
ax2.set_ylabel('Temperature ($^\circ$C) ', fontsize=28)
#ax2.set_ylabel('Absolute Humidity $(g/m^3)$', fontsize=28)
ax2.set_ylim(-10,31) #for tem
ax.set_ylim(-103,-90)
#ax2.set_ylim(-2,25) #for humd
ax.tick_params(axis='both', which='major', labelsize=26)
ax2.tick_params(axis='both', which='major', labelsize=26)

ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y')) #to change the date format to Jul 22..
plt.show()


