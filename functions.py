
# coding: utf-8

# In[ ]:


import numpy as np
import math
#fast Hadamard Transform
def FWHT_A(k, dist):
    if k == 1:
        return dist
    dist1 = dist[0 : k//2]
    dist2 = dist[k//2 : k]
    trans1 = FWHT_A(k//2, dist1)
    trans2 = FWHT_A(k//2, dist2)
    trans = np.concatenate((trans1+ trans2, trans1 - trans2))
    return trans

#simplex projection
def project_probability_simplex(p_estimate):
    
    k = len(p_estimate)  # Infer the size of the alphabet.
    p_estimate_sorted = np.sort(p_estimate)
    p_estimate_sorted[:] = p_estimate_sorted[::-1]
    p_sorted_cumsum = np.cumsum(p_estimate_sorted)
    i = 1
    while i < k:
        if p_estimate_sorted[i] + (1.0 / (i + 1)) * (1 - p_sorted_cumsum[i]) < 0:
            break
        i += 1
    lmd = (1.0 / i) * (1 - p_sorted_cumsum[i - 1])
    return np.maximum(p_estimate + lmd, 0)

def sparse_projection(p_estimate, s):
    k = len(p_estimate)
    ind = p_estimate.argsort()[-s:][::-1]
    p_sparse = project_probability_simplex(p_estimate[ind])
    p_out = np.zeros(k)
    p_out[ind] = p_sparse
    return p_out

#clip and normalize
def probability_normalize(dist):
    dist = np.maximum(dist,0) #map it to be positive
    norm = np.sum(dist)
    dist = np.true_divide(dist,norm) #ensure the l_1 norm is one
    return dist

#generate a random permutation matrix
def Random_Permutation(k):
    permute = np.random.permutation(k)
    reverse = np.zeros(k)
    for i in range(k):
        reverse[int(permute[i])] = i
    return permute,reverse

#pre-calculate Hadamard Matrix
def Hadamard_init(k):
    H = [None] * k
    for row in range(k):
        H[row] = [True] * k        
# Initialize Hadamard matrix of order k.
    i1 = 1
    while i1 < k:
        for i2 in range(i1):
            for i3 in range(i1):
                H[i2+i1][i3]    = H[i2][i3]
                H[i2][i3+i1]    = H[i2][i3]
                H[i2+i1][i3+i1] = not H[i2][i3]
        i1 += i1
    return H


# In[ ]:


#functions to generate distributions
def generate_geometric_distribution(k,lbd):
    elements = range(0,k)
    prob = [(1-lbd)*math.pow(lbd,x)/(1-math.pow(lbd,k)) for x in elements] # geometric dist
    return prob

def generate_uniform_distribution(k):
    raw_distribution = [1] * k
    sum_raw = sum(raw_distribution)
    prob = [float(y)/float(sum_raw) for y in raw_distribution]
    return prob

def generate_two_steps_distribution(k):
    raw_distribution = [1] * int(k/2) + [3] * int(k/2)
    sum_raw = sum(raw_distribution)
    prob = [float(y)/float(sum_raw) for y in raw_distribution]
    return prob

def generate_Zipf_distribution(k,lbd):
    raw_distribution = [1/(float(i)**(lbd)) for i in range(1,k+1)]
    sum_raw = sum(raw_distribution)
    prob = [float(y)/float(sum_raw) for y in raw_distribution]
    return prob

def generate_Dirichlet_distribution(k,lbd):  
    raw_distribution = [0] * k
    for i in range(0,k):
        raw_distribution[i] = np.random.gamma(1,1)
    sum_raw = sum(raw_distribution)
    prob = [float(y)/float(sum_raw) for y in raw_distribution]
    return prob

def generate_sparse_geometric_distribution(k, lbd, s):
    support = np.random.choice(k, s, replace=False)
    prob = np.zeros(k)
    distr = generate_geometric_distribution(s, lbd)
    prob[support] = distr
    return prob

def generate_sparse_uniform_distribution(k, s):
    support = np.random.choice(k, s, replace=False)
    prob = np.zeros(k)
    distr = generate_uniform_distribution(s)
    prob[support] = distr
    return prob

def generate_sparse_two_steps_distribution(k, s):
    support = np.random.choice(k, s, replace=False)
    prob = np.zeros(k)
    distr = generate_two_steps_distribution(s)
    prob[support] = distr
    return prob

def generate_sparse_Zipf_distribution(k, lbd, s):
    support = np.random.choice(k, s, replace=False)
    prob = np.zeros(k)
    distr = generate_Zipf_distribution(s, lbd)
    prob[support] = distr
    return prob

def generate_sparse_Dirichlet_distribution(k, lbd, s):
    support = np.random.choice(k, s, replace=False)
    prob = np.zeros(k)
    distr = generate_Dirichlet_distribution(s, lbd)
    prob[support] = distr
    return prob

