#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 15:16:21 2024

@author: yzy
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


label_file = '/Users/yzy/Documents/goodchip/labels.csv'

labels_df = pd.read_csv('labels.csv', header=None)
labels_df.columns = ["filename", "score"]

plt.figure(figsize=(10, 6))
sns.histplot(labels_df["score"], bins=30, kde=False, color="orange")  # Use histplot for distribution
plt.title("Distribution of Scores")
plt.xlabel("Score")
plt.ylabel("Count")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()