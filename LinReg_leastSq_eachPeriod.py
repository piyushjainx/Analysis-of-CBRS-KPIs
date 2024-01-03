import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy.stats import linregress, t, pearsonr
import matplotlib.dates as mdates

matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.serif'] = 'Times New Roman'
matplotlib.rcParams['font.size'] = 10


KpiPath= "KPIcombined80%.csv"
WeatherKpi= "Weather_updated.csv"
#absolute_humidity (g/m^3) : updated_file1.csv
#temperature (degC)

# Read CSV files
kpi_df = pd.read_csv(KpiPath, parse_dates=['coll_time_round'])
# Group by coll_time_round and calculate mean of 'mean_AvgRsrp'
kpi_df = kpi_df.groupby('coll_time_round').mean().reset_index()
#kpi_df['mean_AvgRsrp'] = kpi_df['mean_AvgRsrp'].diff()

weather_df = pd.read_csv(WeatherKpi, parse_dates=['datetime (UTC)'])

# Convert coll_time_round to week number
kpi_df['week'] = kpi_df['coll_time_round'].dt.isocalendar().week
weather_df['week'] = weather_df['datetime (UTC)'].dt.isocalendar().week
#print(kpi_df.columns)
#print(weather_df.columns)

# Define the periods
no_leaves = list(range(49, 53)) + list(range(1, 13))
some_leaves = list(range(13, 18)) + list(range(44, 49))
likely_leaves = list(range(18, 44))

periods = [no_leaves, some_leaves, likely_leaves]
labels = ["NL: Dec-Mar", "SL: Apr, Oct-Nov", "LL: May-Oct"]

# Merge dataframes on date
merged_df = pd.merge(kpi_df, weather_df, how='inner', left_on='coll_time_round', right_on='datetime (UTC)')
merged_df = merged_df.drop('week_y', axis=1)
merged_df = merged_df.rename(columns={'week_x': 'week'})
#print(merged_df.columns)

# Set up the figure and axes for the subplots
#fig, axs = plt.subplots(1, 3, figsize=(14, 4))
fig, axs = plt.subplots(1, 3, figsize=(12, 4))

# Loop over periods
for i, period in enumerate(periods):
    # Extract data for the current period
    period_df = merged_df[merged_df['week'].isin(period)]
    #period_df = period_df.dropna(subset=['mean_AvgRsrp'])  # Drop rows with NaN values in 'mean_AvgRsrp_change'
    #x_values = period_df['temperature (degC)'].values
    x_values = period_df['absolute_humidity (g/m^3)'].values
    y_values = period_df['mean_AvgRsrp'].values

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(x_values, y_values)
    print(f'\n{labels[i]}:')
    print(f'Pearson correlation coefficient (Pcorr_coef): {r_value:.3f}')
    print(f'Slope: {slope:.3f}')
    print(f'Intercept: {intercept:.3f}')
    print("y= {} x {}".format(round(slope, 3), round(intercept, 3)))
    
    # Predict y values
    y_pred = slope * x_values + intercept

    # Calculate R^2
    r2 = r2_score(y_values, y_pred)
    print(f'R^2: {r2:.3f}')
    
    # Calculate residual standard error
    residuals = y_values - y_pred
    rse = np.sqrt(np.sum(residuals**2) / (len(x_values) - 2))
    print(f'Residual standard error: {rse:.3f}')

    # Calculate the 95% confidence interval for the slope coefficient
    alpha = 0.05
    t_critical = t.ppf(1 - (alpha / 2), len(x_values) - 2)
    ci = (slope - t_critical * std_err, slope + t_critical * std_err)
    print(f'95% CI for slope: {ci}')

    # Plot data and regression line
    axs[i].scatter(x_values, y_values, s=4, label="Avg RSRP")
    axs[i].plot(x_values, y_pred, color='red', label='Fitted Line', linewidth= 4)
    axs[i].legend(loc='best', ncol=2, fontsize=13)
    #axs[i].set_xlabel('Temperature ($^\degree C$)', fontsize=22)
    axs[i].set_xlabel('Absolute Humidity $(g/m^3)$', fontsize=22)
    axs[i].set_ylabel('Avg RSRP(dBm)', fontsize=22)
    axs[i].set_title(f'{labels[i]}', fontsize=22)
    #axs[0].legend(loc='best', fontsize=18)
    #axs[1].legend(loc='best', fontsize=18)
    #axs[2].legend(loc='best', fontsize=18)
    axs[i].tick_params(axis='both', which='major', labelsize=22)
    axs[i].set_ylim(-113,-84)
    #axs[0].set_ylim(-110,-85)
    #axs[1].set_ylim(-105,-90)
    #axs[2].set_ylim(-110,-90)

    # Annotate the plot with slope and R^2 values
    axs[i].text(0.01, 0.15, f'Pearson Cor: {r_value:.3f}', transform=axs[i].transAxes, verticalalignment='center', fontsize=20)
    #axs[i].text(0.05, 0.90, f'R^2: {r2:.3f}', transform=axs[i].transAxes, verticalalignment='top')
    #axs[i].text(0.01, 0.15, "y= {} x {}".format(round(slope, 3), round(intercept, 3)), transform=axs[i].transAxes, verticalalignment='center', fontsize=20)

    axs[i].text(0.01, 0.05, "y", transform=axs[i].transAxes, verticalalignment='center', fontsize=20)
    axs[i].text(0.04, 0.05, " =   ", transform=axs[i].transAxes, verticalalignment='center', fontsize=20, fontweight='bold')
    axs[i].text(0.06, 0.05, "   {} x {}".format(round(slope, 3), round(intercept, 3)), transform=axs[i].transAxes, verticalalignment='center', fontsize=20)


plt.tight_layout()
#plt.subplots_adjust(wspace=0.45)
plt.subplots_adjust(wspace=0.48)
plt.show()
