import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Import numpy


def plot_word_stats_colored_labels(csv_path: str, min_occurrences: int = 1):
    """
    Reads a CSV, processes stats, and generates a scatter plot where each unique
    point and its corresponding multi-line text label have a distinct color.

    Args:
        csv_path (str): The path to the CSV file.
        min_occurrences (int): Minimum occurrences to be included.
    """
    try:
        df = pd.read_csv(csv_path)

        summary_df = df.groupby('cuvant').agg(
            x_occurrences=('cuvant', 'size'),
            y_sum_total=('total_aparitii', 'sum')
        ).reset_index()

        filtered_df = summary_df[summary_df['x_occurrences'] >= min_occurrences]

        if filtered_df.empty:
            print(f"No words found with at least {min_occurrences} occurrences.")
            return

        print("Data to be plotted:")
        print(filtered_df)

        # --- NEW LOGIC FOR GENERATING AND APPLYING COLORS ---

        # 1. Get the unique (x, y) coordinates
        unique_points_df = filtered_df.drop_duplicates(subset=['x_occurrences', 'y_sum_total'])
        num_unique_points = len(unique_points_df)

        # 2. Generate a list of distinct colors using a colormap
        # 'tab10', 'tab20', 'viridis' are good choices for colormaps.
        cmap = plt.get_cmap('tab10')
        colors = [cmap(i) for i in np.linspace(0, 1, num_unique_points)]

        # 3. Create a dictionary to map each coordinate tuple to a color
        # This allows us to look up the color for a point later
        unique_coords_tuples = [tuple(row) for row in unique_points_df[['x_occurrences', 'y_sum_total']].to_numpy()]
        coord_to_color_map = dict(zip(unique_coords_tuples, colors))

        # --- PLOTTING WITH COLORS ---

        plt.figure(figsize=(12, 8))

        # Plot the unique points, assigning a color to each one
        # The `c` argument takes a list of colors corresponding to the points
        plt.scatter(
            unique_points_df['x_occurrences'],
            unique_points_df['y_sum_total'],
            c=colors,  # Apply the generated colors
            alpha=0.9,
            s=80,
            zorder=5
        )

        # Group words by coordinates to create labels
        grouped_by_coords = filtered_df.groupby(['x_occurrences', 'y_sum_total'])

        for (x_coord, y_coord), group_df in grouped_by_coords:
            label_text = "\n".join(group_df['cuvant'])

            # Look up the color for the current coordinate from our map
            point_color = coord_to_color_map[(x_coord, y_coord)]

            # Place the text, using the same color as the point
            plt.text(
                x=x_coord + 0.05,
                y=y_coord,
                s=label_text,
                fontsize=9,
                verticalalignment='center',
                color=point_color,  # Apply the color to the text
                fontweight='bold'  # Make text bold for better visibility
            )

        # --- END OF NEW LOGIC ---

        plt.title('Word Frequency vs. Total Appearances Sum (Colored Labels)')
        plt.xlabel('Number of Occurrences (in different files)')
        plt.ylabel('Sum of "total_aparitii"')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.subplots_adjust(right=0.85)
        plt.show()

    except FileNotFoundError:
        print(f"Error: The file '{csv_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# --- How to use it ---
if __name__ == "__main__":
    # Use the 'data_duplicates.csv' to see the grouping effect
    # You can download it from: https://pastebin.com/raw/50fQGZpD
    print("--- Plotting words with colored, grouped labels ---")
    plot_word_stats_colored_labels('data2.csv', min_occurrences=5)


