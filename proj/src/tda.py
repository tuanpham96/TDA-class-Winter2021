# General computation
import numpy as np 
from scipy.stats import entropy
from copy import deepcopy

from tqdm.notebook import tqdm

# TDA packages
import gudhi as gd


def process_Dmatrix(dX, max_k, vec_rhos, 
                    process_edgedensity=True, 
                    min_k=1,
                    save_barcodes=False):
    """
    Process a difference (or distance) matrix and return barcode features and betti curve 
    Return a dictionary `bar_feats` (see output of `process_barcodes` function)
    dX: difference (or distance) matrix
    max_k: maximum simplex dimension to calculate persistent homology 
    vec_rhos: vector of edge density (or distance,difference) to consider for betti number/curve calculate, instead of considering everything 
    process_edgedensity: if True [default], convert to edge density; if false, `vec_rhos` should be a sampled distance vector 
    min_k: [default: 1] minimum simplex to process barcodes 
    save_barcodes: if False [defaul] return bar features dictionary outputs from `process_barcodes` with each key as a homology dimension
                    if True, return `{'barfeats': [bar features from process_barcodes], 'barcodes': [barcodes data]}`
    """
    N = dX.shape[0]

    if process_edgedensity:
        # Obtain rhos (i.e. edge density) from distance
        unq_d = np.unique(dX)
        edge_density = np.array([(np.sum(dX <= x) - N)/(N*(N-1)) for x in unq_d])
        dist2rho_dict = {x:y for x,y in zip(unq_d,edge_density)} 
    
    # Create a vectorized local function to process barcodes later on 
    def dist2rho(d):
        # if distance is infinity, density is 1.0 
        # otherwise use the dict 
        if np.isinf(d): 
            return 1.0
        else:
            return dist2rho_dict[d]
    dist2rho_vect = np.vectorize(dist2rho)

    # Create complex and process persistence 
    gd_tree = gd.RipsComplex(distance_matrix = dX).create_simplex_tree(max_dimension = max_k)
    gd_tree.persistence();

    # Process barcodes of dim >= min_k 
    k_range = range(min_k,max_k)
    bars_eachdim = {'B%d' %(k): gd_tree.persistence_intervals_in_dimension(k)
                    for k in k_range}
    
    if process_edgedensity:
        bars_eachdim = {k: dist2rho_vect(v) if len(v) > 0 else []
                        for k,v in bars_eachdim.items()}
    
    bar_feats = {k: process_barcodes(v, vec_rhos)
                 for k,v in bars_eachdim.items()}
    
    if save_barcodes:
        return {'barfeats': bar_feats, 'barcodes': bars_eachdim}
    else:
        return bar_feats

def process_barcodes(bars, vec_rhos, pq_pairs = ((1,1),(1,2),(2,1),(1,3),(3,1))):
    """
    Process barcodes of each dimension, return a dictionary of betti curve and features
    bars: matrix of [[b_0,d_0],[b_1,d_1],[b_2,d_2],...] of birth(b)-death(d) pairs of a single dimension
    vec_rhos: vector of edge density (or distance,difference) to consider for betti number/curve calculate, instead of considering everything 
    pq_pairs: (p,q) pairs to calculate features from sum (or mean) of (d-b)^p x (b+d)^q
    Return:
    barfeats_dict:
        - betti_num: betti number for each value of edge density 
        - int_betti: integrated betti number, by using trapezoid method 
        - mean_pers, med_pers, sum_pers, max_pers: persistence (lifetime = d-b) statistics (mean, median, sum, max)
        - ent_pers: persistence entropy (i.e. entropy of normalized lifetimes)
        - norm_ent_pers: persistence entropy normalized by log2(sum of persistence)
        - alg_p*_q*_[sum,mean]: sum (or mean) of (d-b)^p x (b+d)^q
    """
    barfeats_dict = {}    
    nonempty_bars = len(bars) > 0
    
    # betti numbers and integrated betti 
    if nonempty_bars:
        barfeats_dict['betti_num'] = np.array(
            [np.sum(np.logical_and(bars[:,0] <= x,bars[:,1] >= x)) 
             for x in vec_rhos])
        barfeats_dict['int_betti'] = np.trapz(barfeats_dict['betti_num'], x=vec_rhos)
    else: 
        barfeats_dict['betti_num'] = np.zeros((len(vec_rhos),))
        barfeats_dict['int_betti'] = 0 

    # modify bar deaths to reflect inf as longest rho
    if nonempty_bars:
        bar_births = deepcopy(bars[:,0])
        bar_deaths = deepcopy(bars[:,1])
        bar_deaths[np.isinf(bar_deaths)] = vec_rhos[-1]
    else: 
        bar_births = np.array([0])
        bar_deaths = np.array([0])
    bar_births = bar_births[:,None]
    bar_deaths = bar_deaths[:,None]
    
    # persistent scores 
    lifetimes = np.abs(bar_deaths - bar_births)
    barfeats_dict['mean_pers'] = np.mean(lifetimes)
    barfeats_dict['med_pers'] = np.median(lifetimes)
    barfeats_dict['sum_pers'] = np.sum(lifetimes)
    barfeats_dict['max_pers'] = np.max(lifetimes)
    if nonempty_bars:
        barfeats_dict['ent_pers'] = entropy(lifetimes/barfeats_dict['sum_pers'])[0] 
    else:
        barfeats_dict['ent_pers'] = 0
    
    # algebraic combination of {b,d}
    bd_sum = bar_births + bar_deaths
    for p,q in pq_pairs: 
        k = 'alg_p%d_q%d' %(p,q)
        barfeats_dict[k+'_sum'] = np.sum((lifetimes**p) * (bd_sum**q))
        barfeats_dict[k+'_mean'] = np.mean((lifetimes**p) * (bd_sum**q))

    return barfeats_dict

def concat_barfeats(barfeats_list,parent_keys,feat_keys):    
    """
    Concatenate list of bar features 
    """
    cat_feats = {}
    for pk in parent_keys:
        feat_list = [x[pk] for x in barfeats_list]
        cat_feats[pk] = {k: np.vstack([x[k] for x in feat_list if len(x) > 0]) 
                         for k in feat_keys}
    return cat_feats 

def plot_persistent_diagrams(barcodes,vec_rhos,fig_title,fig_prefix,
                             zoomin_range=None,plot=False,rho_label=None,
                             cmap_name='Set1'):
    """
    Plot persistent diagrams and barcodes
    barcodes: barcodes data
    vec_rhos: distance or edge density 
    fig_title: figure title
    fig_prefix: figure file name prefix to be saved
    zoomin_range: zoomed in range of `rhos` [default: None]
    plot: whether to do `plt.show()` after saving [default: False]
    rho_label: xlabel for barcode subplots [default: None]
    cmap_name: colormap name [default: 'Set1']
    """
    barcodes_data = deepcopy(barcodes)
    barcodes_data = {k:np.clip(v,a_min=0,a_max=vec_rhos[-1]) 
                     for k,v in barcodes_data.items()}
    persdim = list(barcodes_data.keys())

    nrows = len(persdim)
    cmap = plt.get_cmap(cmap_name)
    cmap = np.flipud(cmap(np.arange(nrows)))

    plt.figure(figsize=(20,8))
    plt.subplot2grid((3, 4), (0, 0),rowspan=3,colspan=1)
    {plt.scatter(v[:,0],v[:,1],label=k,alpha=0.5,color=cmap[i]) 
     for i,(k,v) in enumerate(barcodes_data.items()) if len(v) > 0}
    plt.plot([0,vec_rhos[-1]],[0,vec_rhos[-1]],'-k',lw=1)
    plt.gca().set_aspect('equal')
    if zoomin_range is not None:
        plt.xlim(zoomin_range)
        plt.ylim(zoomin_range)
    plt.xlabel('births')
    plt.ylabel('deaths')

    plt.title('persistence diagram')
    plt.legend()

    cnt_y = 0
    axes = [plt.subplot2grid((3, 4),(0,1),rowspan=1,colspan=3),
          plt.subplot2grid((3, 4),(1,1),rowspan=2,colspan=3)]
    for i,(k,v) in enumerate(barcodes_data.items()):
        ax = axes[0] if k == persdim[0] else axes[1]
        num_bars = len(v)
        if num_bars == 0: continue 
        ax.plot(v.T, cnt_y + np.tile(range(num_bars),(2,1)), 
                 lw=0.5 + 1.5*(i!=0), color=cmap[i])
        
        if zoomin_range is not None:
            ax.set_xlim(zoomin_range)
            
        cnt_y += (i!=0)*num_bars
    
    if rho_label is not None: 
        axes[1].set_xlabel(rho_label)
    plt.suptitle(fig_title)
    plt.tight_layout()
    plt.savefig('%s-persistent-diagram' %(fig_prefix))
    if plot:
        plt.show()
    else:
        plt.close()
        
def get_pairwise_bottleneck(barcode_list, barcode_key,
                            diag_val=np.nan,label_dict=None,
                            return_trial_and_label_dist=False):
    """
    Return pairwise bottle-neck distance of barcode list 
    barcode_list: barcode list, each element is a dictionary containing many dimensions as keys
    barcode_key: barcode key to access homology dimension 
    diag_val: [default: `np.nan`] diagonal values for the pairwise matrix  
    label_dict: [default: None] label dictionary of indices, 
                if not None, will process mean distance across different classes/labels 
    return_trial_and_label_dist: [default: False] if True will return both trial and label distance matrices, 
                else will only return the label distances 
    """
    n = len(barcode_list)
    pw_BN = np.empty((n,n))
    pw_BN[:] = diag_val
    for i in tqdm(range(n-1),desc='processing %s' %(barcode_key)):
        bars_i = barcode_list[i][barcode_key]
        for j in range(i+1,n):
            bars_j = barcode_list[j][barcode_key]
            pw_BN[i,j] = gd.bottleneck_distance(bars_i,bars_j)
            pw_BN[j,i] = pw_BN[i,j] 
            
    if label_dict is None:
        return pw_BN
    
    keys = list(label_dict.keys())  
    num_keys = len(keys)
    pw_labels = np.zeros((num_keys,num_keys))
    for i in range(num_keys):
        ind_ith = label_dict[keys[i]]
        for j in range(i,num_keys):
            ind_jth = label_dict[keys[j]]
            pw_labels[i,j] = np.nanmean(pw_BN[ind_ith,:][:,ind_jth])
            pw_labels[j,i] = pw_labels[i,j]
    
    if return_trial_and_label_dist: 
        return {'trial_mat': pw_BN, 'label_mat': pw_labels, 'labels': keys}
    else:
        return {'label_mat': pw_labels, 'labels': keys}