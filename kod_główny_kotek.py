import numpy as np
import matplotlib.pyplot as plt

class Cat:
    def __init__(self, params:dict):
        self.glued_result = np.zeros((100, 100))
        self.matrices={}
        for key in params["ind_lim"].keys():
            row_min=min([tup[0] for tup in params["ind_lim"][key]])
            row_max=max([tup[0] for tup in params["ind_lim"][key]])
            col_min=min([tup[1] for tup in params["ind_lim"][key]])
            col_max=max([tup[1] for tup in params["ind_lim"][key]])
            self.matrices[key]=np.zeros((row_max-row_min, col_max-col_min))
            self.matrices[key][:,:]=params["mask"][key]
            self.glued_result[row_min:row_max, col_min:col_max] = self.matrices[key]


if __name__=="main":
    params={"ind_lim":{"head": [(0,40), (0,60), (20,40), (20,60)],
                        "body": [(20,30), (20,70), (70,30), (70,70)],
                        "tail": [(70,45), (70,55), (100, 45), (100,55)],
                        "LFL": [(20,0), (20,30), (30,0), (30,30)],
                        "LBL": [(60,0), (60,30), (70,0), (70,30)],
                        "RFL": [(20,70), (20,100), (30,70), (30,100)],
                        "RBL": [(60,70), (60,100), (70, 70), (70,100)],
                        "I": [(0,0), (0,40), (20,0), (20, 40)],
                        "II": [(0,60), (0,100), (20,60), (20,100)],
                        "III": [(30,0), (30,30), (60,0), (60,30)],
                        "IV": [(30,70), (30,100), (60,70), (60,100)],
                        "V": [(70,0), (70,45), (100,0), (100,45)],
                        "VI": [(70,55), (70,100), (100,55), (100,100)]},
                "resolution": 1,
                "mask": {"head": 1,
                        "body": 1,
                        "tail": 1,
                        "LFL": 1,
                        "LBL": 1,
                        "RFL": 1,
                        "RBL": 1,
                        "I": 0,
                        "II": 0,
                        "III": 0,
                        "IV": 0,
                        "V": 0,
                        "VI": 0}}
'''
x = Cat(params)
plt.imshow(x.glued_result)
plt.show()
'''