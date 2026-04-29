import polars as pl

import os

hwt_trees_file = os.path.join("..", "..", "STARK", "phd_venn_diagram", "pos_trees", "Solar_3.0_human_relevant_pos_trees.tsv")
mgt_trees_file = os.path.join("..", "..", "STARK", "phd_venn_diagram", "pos_trees", "Solar_GPT-5_annotated_pos_trees.tsv")

output_file = os.path.join("Solar_GPT-5_prominent_trees_descending.tsv")

n = 10 # number of trees to output

hwt_dataframe = pl.read_csv(hwt_trees_file, separator="\t").drop_nans()
mgt_dataframe = pl.read_csv(mgt_trees_file, separator="\t").drop_nans()

combined_dataframe = hwt_dataframe.join(mgt_dataframe, on="Tree", suffix="_MGT").with_columns(
                     (pl.col("logDice_MGT") - pl.col("logDice")).alias("delta_logDice")).sort(
                     "delta_logDice", descending=False)

combined_dataframe.select(["Tree", "Absolute frequency", "Absolute frequency_MGT", "Example_MGT", "delta_logDice"]
                          ).head(n).write_csv(output_file, separator="\t")
