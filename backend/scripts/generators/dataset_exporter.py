"""
Dataset Exporter
"""

from pathlib import Path
import pandas as pd


class DatasetExporter:

    def __init__(self):

        self.output_dir = Path("data/generated")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(self, tickets, filename="customer_support_dataset.csv"):

        df = pd.DataFrame(tickets)

        output_file = self.output_dir / filename

        df.to_csv(output_file, index=False)

        print(f"\nDataset saved successfully!")

        print(f"Location: {output_file}")

        print(f"Total Tickets: {len(df)}")

        return output_file