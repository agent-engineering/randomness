#!/usr/bin/env/python
# -*- coding: utf-8 -*-
"""
    __author__: archie
    Created Date: Sat, 09 Dec 2023; 16:24:41
"""
import random
from typing import Dict

import pandas as pd


def genRandomCombo() -> Dict:
    levels = ["Easy", "Medium", "Hard"]
    combo = {"Easy": 0, "Medium": 0, "Hard": 0}
    for _ in range(5):
        combo[random.choice(levels)] += 1
    return combo


def goWild(df: pd.DataFrame, combo: Dict = {}) -> Dict:
    if len(combo) == 0:
        combo = genRandomCombo()
    randomProbs = []
    for key, value in combo.items():
        sub = df[df["Difficulty"] == key]
        sub_idx = [random.choice(sub.index) for _ in range(value)]
        sub = sub.loc[sub_idx]
        randomProbs += sub.to_dict("records")
    return randomProbs


problemSetCombo = {"5E": {"Easy": 5},
                   "3E1M": {"Easy": 3, "Medium": 1},
                   "1E2M": {"Easy": 1, "Medium": 2},
                   "1E1M1H": {"Easy": 1, "Medium": 1, "Hard": 1},
                   "1E2M1H": {"Easy": 1, "Medium": 2, "Hard": 1}}
