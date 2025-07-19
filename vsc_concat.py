# Step 1: Import libraries
import pandas as pd
import glob

# Step 2: Find all CSV files in the data folder located in the current directory
csv_files = glob.glob('data/*.csv')
print(f"Found {len(csv_files)} CSV files:", csv_files)

# Step 3: Check if files are found
if not csv_files:
    print("No CSV files found in the 'data' folder.")
    exit(1)


# Step 4: Load all CSV files into a list of DataFrames
all_dfs = [pd.read_csv(file) for file in csv_files]

# Step 5: Concatenate all DataFrames into a single DataFrame
combined_df = pd.concat(all_dfs, ignore_index=True)

# Step 6: Define standard column order and reindex the combined DataFrame
# This ensures a consistent output format, adding missing columns as NaN
# and dropping any columns not in the standard list.
standard_columns = [
    'entity', 'externalHome', 'internalHome', 'internalHomeId',
    'externalAway', 'internalAway', 'internalAwayId', 'externalTournament',
    'internalTournament', 'internalTournamentId', 'internalMatch',
    'externalMatch', 'externalSource', 'timestamp'
]
combined_df = combined_df.reindex(columns=standard_columns)
print("Final column order enforced.")

# Step 7: Export the final DataFrame to a new CSV file
combined_df.to_csv('combined_output.csv', index=False)
print(f"Combined CSV saved as 'combined_output.csv' with {combined_df.shape[0]} rows.")

# Step 8: Reorder columns to prioritize mapping-related fields
mapping_priority = [
    'entity', 'externalHome', 'internalHome', 'internalHomeId',
    'internalMatch', 'externalAway', 'internalAway', 'internalAwayId',
    'externalTournament', 'internalTournament', 'internalTournamentId'
]
remaining_columns = [col for col in combined_df.columns if col not in mapping_priority]
ordered_columns = mapping_priority + remaining_columns
combined_df_html = combined_df.reindex(columns=ordered_columns)

# Step 9: Apply conditional formatting for mapping validation
def highlight_row(row):
    color = ''
    # Check for mismatches
    if (
        pd.notna(row['internalHome']) and pd.notna(row['externalHome']) and row['internalHome'] != row['externalHome']
    ) or (
        pd.notna(row['internalTournament']) and pd.notna(row['externalTournament']) and row['internalTournament'] != row['externalTournament']
    ) or (
        pd.notna(row['internalHomeId']) and pd.notna(row['internalMatch']) and str(row['internalHomeId']) not in str(row['internalMatch'])
    ):
        color = 'background-color: #ffcccc;'
    return [color] * len(row)

styled_html = combined_df_html.style.apply(highlight_row, axis=1)

# Step 10: Export the styled DataFrame to an interactive HTML file
styled_html.set_table_attributes('class="table table-striped"').to_html('mapping_validation_report.html', render_links=True)
print("Interactive mapping validation report saved as 'mapping_validation_report.html'.")
