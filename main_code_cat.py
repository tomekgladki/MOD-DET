import numpy as np
import matplotlib.pyplot as plt

class Cat:
    def __init__(self, params:dict):
        self.params=params
        self.glued_result = np.zeros((100, 100))
        self.matrices={}
        self.get_matrices()
        self.get_glued_result()

    def get_matrices(self):
        for key in params["ind_lim"].keys():
            row_min=min([tup[0] for tup in params["ind_lim"][key][:-1]])
            row_max=max([tup[0] for tup in params["ind_lim"][key][:-1]])
            col_min=min([tup[1] for tup in params["ind_lim"][key][:-1]])
            col_max=max([tup[1] for tup in params["ind_lim"][key][:-1]])
            if key not in self.matrices.keys():
                self.matrices[key]=self.params["ind_lim"][key][4](
                    self.params["domain"]["grid"][row_min:row_max, col_min:col_max]
                )
            else:
                self.matrices[key]=self.glued_result[row_min:row_max, col_min:col_max]
        return self
                
        
    def get_glued_result(self):
        for key in params["ind_lim"].keys():
            row_min=min([tup[0] for tup in params["ind_lim"][key][:-1]])
            row_max=max([tup[0] for tup in params["ind_lim"][key][:-1]])
            col_min=min([tup[1] for tup in params["ind_lim"][key][:-1]])
            col_max=max([tup[1] for tup in params["ind_lim"][key][:-1]])
            self.glued_result[row_min:row_max, col_min:col_max] = self.matrices[key]
        return self
    


#if __name__=="main":
params={"ind_lim":{
    "head": [(0,40), (0,60), (20,40), (20,60), lambda x: np.random.random(x.shape)],
    "body": [(20,30), (20,70), (70,30), (70,70), lambda x: np.random.random(x.shape)],
    "tail": [(70,45), (70,55), (100, 45), (100,55), lambda x: np.random.random(x.shape)],
    "LFL": [(20,0), (20,30), (30,0), (30,30), lambda x: np.random.random(x.shape)],
    "LBL": [(60,0), (60,30), (70,0), (70,30), lambda x: np.random.random(x.shape)],
    "RFL": [(20,70), (20,100), (30,70), (30,100), lambda x: np.random.random(x.shape)],
    "RBL": [(60,70), (60,100), (70, 70), (70,100), lambda x: np.random.random(x.shape)],
    "I": [(0,0), (0,40), (20,0), (20, 40), lambda x: 0],
    "II": [(0,60), (0,100), (20,60), (20,100), lambda x: 0],
    "III": [(30,0), (30,30), (60,0), (60,30), lambda x: 0],
    "IV": [(30,70), (30,100), (60,70), (60,100), lambda x: 0],
    "V": [(70,0), (70,45), (100,0), (100,45), lambda x: 0],
    "VI": [(70,55), (70,100), (100,55), (100,100), lambda x: 0]
    },
        "domain":{
            "grid":np.meshgrid(np.linspace(0,1,100), np.linspace(0,1,100))[0],
            "dx":1
    }        
}

x = Cat(params)
plt.imshow(x.glued_result)
plt.show()
