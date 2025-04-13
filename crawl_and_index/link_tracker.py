import pandas as pd
import pickle

class LinkTracker:
    def __init__(self):
        # Initialize the DataFrame with the required columns
        self.df = pd.DataFrame(columns=["url", "inlinks", "outlinks", "outlink_count", "page_rank"])

    def add_page(self, url, outlinks):
        """
        Add a page to the DataFrame or update its outlinks.
        :param url: The URL of the page.
        :param outlinks: A set of outlinks from the page.
        """
        if url not in self.df["url"].values:
            # Add a new row for the URL
            self.df = pd.concat([
                self.df,
                pd.DataFrame({
                    "url": [url],
                    "inlinks": [set()],
                    "outlinks": [outlinks],
                    "outlink_count": [len(outlinks)],
                    "page_rank": [None]
                })
            ], ignore_index=True)
        else:
            # Update the outlinks and outlink count
            self.df.loc[self.df["url"] == url, "outlinks"] = [outlinks]
            self.df.loc[self.df["url"] == url, "outlink_count"] = len(outlinks)

        # Update inlinks for each outlink
        for outlink in outlinks:
            if outlink not in self.df["url"].values:
                # Add a new row for the outlink if it doesn't exist
                self.df = pd.concat([
                    self.df,
                    pd.DataFrame({
                        "url": [outlink],
                        "inlinks": [set([url])],
                        "outlinks": [set()],
                        "outlink_count": [0],
                        "page_rank": [None]
                    })
                ], ignore_index=True)
            else:
                # Update the inlinks for the outlink
                self.df.loc[self.df["url"] == outlink, "inlinks"].iloc[0].add(url)

    def save_to_pickle(self, filepath):
        """
        Save the DataFrame to a pickle file.
        :param filepath: The path to save the pickle file.
        """
        with open(filepath, "wb") as file:
            pickle.dump(self.df, file)

    def load_from_pickle(self, filepath):
        """
        Load the DataFrame from a pickle file.
        :param filepath: The path to the pickle file.
        """
        with open(filepath, "rb") as file:
            self.df = pickle.load(file)