import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anm

class Cat:
    def __init__(self, params:dict):
        self.params=params
        self.glued_result = np.zeros((100, 100))
        self.matrices={}
        self.v_matrices={}
        self.results_={} # 3d array
        self.v_results_={} # 3d array
        self.all_results={} # 3d array
        self.get_matrices()
        self.get_glued_result()
        self.get_v_matrices()
        

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
    
    def get_v_matrices(self):
        for key in params["ind_lim"].keys():
            row_min=min([tup[0] for tup in params["ind_lim"][key][:-1]])
            row_max=max([tup[0] for tup in params["ind_lim"][key][:-1]])
            col_min=min([tup[1] for tup in params["ind_lim"][key][:-1]])
            col_max=max([tup[1] for tup in params["ind_lim"][key][:-1]])
            if key not in self.v_matrices.keys():
                self.v_matrices[key]=self.params["ind_lim"][key][4](
                    self.params["domain"]["grid"][row_min:row_max, col_min:col_max]
                )
            else:
                self.v_matrices[key]=self.glued_result[row_min:row_max, col_min:col_max]
        return self
   
                       
        
    def get_glued_result(self):
        for key in params["ind_lim"].keys():
            row_min=min([tup[0] for tup in params["ind_lim"][key][:-1]])
            row_max=max([tup[0] for tup in params["ind_lim"][key][:-1]])
            col_min=min([tup[1] for tup in params["ind_lim"][key][:-1]])
            col_max=max([tup[1] for tup in params["ind_lim"][key][:-1]])
            self.glued_result[row_min:row_max, col_min:col_max] = self.matrices[key]
        return self
    
    def evolve_n_steps(self, steps):
        ht,hx,hy,Du,Dv=list(self.params["par"].values())[0:5]

        self.all_results=np.zeros((steps, 100, 100))
        self.all_results[0,:,:]=self.glued_result
        for key in self.matrices:

            row_min=min([tup[0] for tup in params["ind_lim"][key][:-1]])
            row_max=max([tup[0] for tup in params["ind_lim"][key][:-1]])
            col_min=min([tup[1] for tup in params["ind_lim"][key][:-1]])
            col_max=max([tup[1] for tup in params["ind_lim"][key][:-1]])

            self.results_[key]=np.zeros((steps, self.matrices[key].shape[0], self.matrices[key].shape[1]))
            self.results_[key][0,:,:]=self.matrices[key]
            results=self.results_[key]
            self.v_results_[key]=np.zeros((steps, self.matrices[key].shape[0], self.matrices[key].shape[1]))
            self.v_results_[key][0,:,:]=self.v_matrices[key]
            v_results=self.v_results_[key]
            for i in range(steps-1): 

                if key not in ["head","body","tail","LFL", "LBL", "RFL", "RBL"]:
                    continue
                else:
                    # matrix u
                    self.results_[key][i+1,1:-1:,1:-1]=results[i,1:-1,1:-1]+Du*ht/(hx**2)*(results[i,2:,1:-1]+results[i,:-2,1:-1]-2*results[i,1:-1,1:-1])+Du*ht/(hy**2)*(results[i,1:-1,2:]+results[i,1:-1,:-2]-2*results[i,1:-1,1:-1])+self.params["func"]["f"](
                        results[i,1:-1,1:-1],v_results[i,1:-1,1:-1],self.params["par"]
                    )
                    self.results_[key][i+1,0,:]=self.results_[key][i,1,:]
                    self.results_[key][i+1,-1,:]=self.results_[key][i,-2,:]
                    self.results_[key][i+1,:,0]=self.results_[key][i,:,1]
                    self.results_[key][i+1,:,-1]=self.results_[key][i,:,-2]
                    
                    
                    # matrix v
                    self.v_results_[key][i+1,1:-1,1:-1]=v_results[i,1:-1,1:-1]+Dv*ht/(hx**2)*(v_results[i,2:,1:-1]+v_results[i,:-2,1:-1]-2*v_results[i,1:-1,1:-1])+Du*ht/(hy**2)*(v_results[i,1:-1,2:]+v_results[i,1:-1,:-2]-2*v_results[i,1:-1,1:-1])+self.params["func"]["g"](
                        results[i,1:-1,1:-1],v_results[i,1:-1,1:-1],self.params["par"]
                    )
                    self.v_results_[key][i+1,0,:]=self.v_results_[key][i,1,:]
                    self.v_results_[key][i+1,-1,:]=self.v_results_[key][i,-2,:]
                    self.v_results_[key][i+1,:,0]=self.v_results_[key][i,:,1]
                    self.v_results_[key][i+1,:,-1]=self.v_results_[key][i,:,-2]

                    self.all_results[i+1,row_min:row_max, col_min:col_max]=self.results_[key][i+1,:,:]
                    results=self.results_[key]
                    v_results=self.v_results_[key]
                    


                

        

        
        return self

params={"ind_lim":{
    "head": [(0,40), (0,60), (20,40), (20,60), lambda x: np.random.random(x.shape)],
    "body": [(20,30), (20,70), (70,30), (70,70), lambda x: np.random.random(x.shape)],
    "tail": [(70,45), (70,55), (100, 45), (100,55), lambda x: np.random.random(x.shape)],
    "LFL": [(20,0), (20,30), (30,0), (30,30), lambda x: np.random.random(x.shape)],
    "LBL": [(60,0), (60,30), (70,0), (70,30), lambda x: np.random.random(x.shape)],
    "RFL": [(20,70), (20,100), (30,70), (30,100), lambda x: np.random.random(x.shape)],
    "RBL": [(60,70), (60,100), (70, 70), (70,100), lambda x: np.random.random(x.shape)],
    "I": [(0,0), (0,40), (20,0), (20, 40), lambda x: np.zeros(x.shape)],
    "II": [(0,60), (0,100), (20,60), (20,100), lambda x: np.zeros(x.shape)],
    "III": [(30,0), (30,30), (60,0), (60,30), lambda x: np.zeros(x.shape)],
    "IV": [(30,70), (30,100), (60,70), (60,100), lambda x: np.zeros(x.shape)],
    "V": [(70,0), (70,45), (100,0), (100,45), lambda x: np.zeros(x.shape)],
    "VI": [(70,55), (70,100), (100,55), (100,100), lambda x: np.zeros(x.shape)]
    },
        "domain":{
            "grid":np.meshgrid(np.linspace(0,1,100), np.linspace(0,1,100))[0],
            "dx":1
    },
    "func":{
        "f": lambda u, v, dict_par: dict_par['a']+dict_par['b']*(u**2)/(v*(1+dict_par['K']*u**2))-dict_par['c']*u,
        "g": lambda u, v, dict_par: dict_par['d']*u**2-dict_par['e']*v
    },
    "par":{
        "ht":0.1,
        "hx":1,
        "hy":1,
        "Du":0.1,
        "Dv":2.0,
        "a":0,
        "b":0.5,
        "c":0.5,
        "d":0.5,
        "e":0.45,
        "K":0.238

    }        
}

x = Cat(params)
#plt.imshow(x.glued_result)
#plt.show()
#print(x.matrices["head"])
x.evolve_n_steps(20)
plt.imshow(x.all_results[-1,:,:])
plt.show()
print(np.var(x.all_results[-1,:,:]))

'''
fig=plt.figure()
figs=x.all_results[0,:,:]
def animation(j):
    figs=x.all_results[j,:,:]
    return figs

anim=anm.FuncAnimation(fig,
                      func=animation,
                      interval = 10,
                      blit=True)
plt.show()
'''                      
#print(x.params["func"]["f"]())

#print(x.all_results[-1,:,:])