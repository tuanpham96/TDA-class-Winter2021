import numpy as np 
from scipy.stats import entropy


def calc_info_measures(X,Y,hist_nbin,hist_range):
    """
    Return mutual information I_XY and variation of information V_XY
    X, Y: time arrays 
    hist_nbin: number of bins for histogram 
    hist_range: 2D matrix of histogram range
    """
    c_XY = np.histogram2d(X, Y, bins=hist_nbin, range=hist_range)[0]
    H_X = entropy(np.sum(c_XY,axis=0)/np.sum(c_XY)) 
    H_Y = entropy(np.sum(c_XY,axis=1)/np.sum(c_XY)) 
    H_XY = entropy(c_XY.flatten()/np.sum(c_XY))
    I_XY = H_X + H_Y - H_XY
    V_XY = H_XY - I_XY
    return I_XY, V_XY

def calc_parwise_info(X,hist_nbin,hist_range):
    """
    Return mutual information matrix I_X and variation of information matrix V_X
    X: [num_times x num_rois] dF/F0 
    hist_nbin: number of bins for histogram 
    hist_range: 2D matrix of histogram range 
    """
    n_rois = X.shape[1]
    I_X = np.zeros((n_rois,n_rois))
    V_X = np.zeros((n_rois,n_rois))
    for i in range(n_rois-1):
        for j in range(i,n_rois):
            I_X[i,j], V_X[i,j] = calc_info_measures(X[:,i],X[:,j],hist_nbin,hist_range)
            
            I_X[j,i] = I_X[i,j]
            V_X[j,i] = V_X[i,j]
        V_X[i,i] = 0 # in case of numerical issues 
    return I_X, V_X 

def calc_pairwise_corr(X):
    """
    Return correlation coefficient and distance matrices
    X: [num_times x num_rois] dF/F0 
    """
    corr_coef = np.corrcoef(X.T)
    corr_dist = np.sqrt(2*(1-corr_coef))
    return corr_coef, corr_dist

def gen_wsbm(N,k=4,model_type='assort',mu_high=2,sigma_high=0.5,mu_low=1,sigma_low=0.5):
    """
    Return a difference matrix of a symmetric weighted stochastic block model 
    The matrix will be the difference between the generated similarity matrix and its maximum
    N: number of vertices
    k: number of blocks (communities) along diagonal line
    model_type: 
        - 'assort': assortative, high within block, low everywhere else 
        - 'disassort': disassortative, low within block, high everywhere else 
        - 'core': core-periphery, high only in the big block from [(N/k) to N]
        - 'discore': flipped core 
    [mu,sigma]_[high,low]: mean and standard deviation of distributions of high and low 
    """
    if 'dis' in model_type:
        mu_high, mu_low = mu_low, mu_high
        sigma_high, sigma_low = sigma_low, sigma_high
        
    W = np.random.normal(loc=mu_low,scale=sigma_low,size=(N,N))
    nk = int(np.round(N/k))
    
    if 'assort' in model_type:
        for i in range(k):
            ind = [i*nk,min(N,(i+1)*nk)]
            ni = ind[1] - ind[0]
            W[ind[0]:ind[1],ind[0]:ind[1]] = np.random.normal(
                loc=mu_high,scale=sigma_high,size=(ni,ni))
    if 'core' in model_type: 
        ni = N - nk - 1
        W[nk:-1,nk:-1] = np.random.normal(
            loc=mu_high,scale=sigma_high,size=(ni,ni))
        
    D = np.max(W) - np.clip(W,a_min=0,a_max=None)
    D = D * (1 - np.eye(N)) # zero difference at self 
    return D

def get_list_at(L,I):
    """ Obtain list L from another list of index I"""
    return [L[i] for i in I]

def flatten_list(L):
    """ Simple flatten a double-nested list, also flatten 2D matrix if needed, return list"""
    Lf = []
    [Lf.extend(li) for li in L]
    return Lf

def minmax_norm(v,vmin=0,vmax=1):
    """ Minmax normalization, then scale between `vmin` and `vmax` (default: 0 and 1 respectively)"""
    return vmin + (vmax-vmin)*(v-np.min(v))/(np.max(v)-np.min(v))


def smooth(arr, span=10):
    """ Moving average smoothing of an array
    from: https://stackoverflow.com/a/63458548
    """
    return np.convolve(arr, np.ones(span * 2 + 1) / (span * 2 + 1), mode="same")

def legend_without_duplicate_labels(ax):
    """ Legends without duplicate labels 
    from: https://stackoverflow.com/a/56253636
    """
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
    ax.legend(*zip(*unique))