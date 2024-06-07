import pandas as pd

df = pd.read_excel('hma.xlsx')
print(df)

df['test_change'] = df['Input'] - df['Input'].shift(1)
df['test_gain'] = df['test_change'].apply(lambda x: x if x > 0 else 0)
df['test_loss'] = df['test_change'].apply(lambda x: -x if x < 0 else 0)

# Calculate the initial average for the first row
initial_avg_gain = df.loc[1:14, 'test_gain'].mean()
initial_avg_loss = df.loc[1:14, 'test_loss'].mean()

df['test_avg_gain'] = None
df['test_avg_loss'] = None
df['test_HM'] = None
df['test_HMA'] = None

# Assign the initial average to the first row
df.iloc[14, df.columns.get_loc('test_avg_gain')] = initial_avg_gain
df.iloc[14, df.columns.get_loc('test_avg_loss')] = initial_avg_loss
hm = initial_avg_gain/initial_avg_loss
df.iloc[14, df.columns.get_loc('test_HM')] = hm
if hm == 0 :
    df.iloc[14, df.columns.get_loc('test_HMA')] = 100
else:
    df.iloc[14, df.columns.get_loc('test_HMA')] = 100-(100/(1+hm))

print(initial_avg_gain,initial_avg_loss)
# Calculate rolling average using vectorized operations
# Define a custom function to calculate rolling average
def rolling_avg(prev_avg, curr_val):
    new_avg = ((prev_avg * 13) + curr_val) / 14
    return new_avg

# Calculate rolling average starting from the 17th row
for i in range(15, len(df)):
    avg_gain = ((df.loc[i-1, 'test_avg_gain'] * 13) + df.loc[i, 'test_gain']) / 14
    avg_loss = ((df.loc[i-1, 'test_avg_loss'] * 13) + df.loc[i, 'test_loss']) / 14
    hm = avg_gain/avg_loss
    df.loc[i, 'test_avg_gain'] = avg_gain
    df.loc[i, 'test_avg_loss'] = avg_loss
    df.loc[i, 'test_HM'] = hm
    if hm == 0 :
        df.loc[i, 'test_HMA'] = 100
    else:
        df.loc[i, 'test_HMA'] = 100-(100/(1+hm))

df.to_csv('test.csv', index=False)