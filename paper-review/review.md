---
bibliography: [./library.bib]
notes: convert by `pandoc --defaults front.yml  -s review.md -o review.pdf`
colorlinks: true
linkcolor: blue
filecolor: blue
citecolor: blue
urlcolor: blue
toccolor: blue
---

# Paper review: _Persistent Homology of Complex Networks for Dynamic State Detection by Myers et al (2019)_

## General information

- **Paper source**: Audun Myers, Elizabeth Munch, and Firas A. Khasawneh (2019). *Persistent homology of complex networks for dynamic state detection*. Phys. Rev. E 100, 022314. [@Myers2019-ws]

- **Related softwares**: TDA with time series packages [`teaspoon`](https://github.com/lizliz/teaspoon) [@Myers_undated-yl] by the authors of the paper, and another package [`giotto-tda`](https://github.com/giotto-ai/giotto-tda) [@Tauzin2020-eo] by another group.

The authors of this paper [@Myers2019-ws] discussed the application of TDA, particularly 1D persistent diagram properties, in detecting periodicity or chaos of dynamical systems. From the time series data of a given simulation or empirical measurements, one could construct a network through sub-sampling the seres and obtain a distance matrix to extract persistent diagrams. The authors focused on two ways of constructing such networks: (1) Taken's embedding and k-NN graphs and (2) ordinal partition networks from permutation sequence construction. Properties (scores) of persistent diagrams of dimension 1 are computed and compared to the standard Lyapunov exponent to indicate chaos, as well as other standard network degree statistics. Additionally, they also established the robustness of the proposed persistent scores due to noise.

## Essential introduction

### Network construction

Before performing TDA, networks that encode possible underlying attractor dynamics of the original time series or dynamical systems need to be constructed. The first way is to use a time-delayed series of only one variable (i.e. Taken's theorem) of appropriate dimension $d$ and delay $\tau$ (appropriate choices involve reducing redundancy between signals of different delays and false nearest neighbors when embedding dimensions change). A collection of data points $x_i \in R^d$ will then be constructed into a k-nearest neighbor graph, in which an edge is created for $x_i$ and $x_j$ if $x_j$ is among the $k$ nearest neighbors of $x_j$.

The second way is to use permutation sequences and construct an ordinal partition graph. More specifically, instead of examining the actual values of a delayed time sequence, this method examines the orders of length $d$, separated by time delay $\tau$. For example, when $d=3$, there will be $d! = 6$ permutation states (ignoring equalities), such as 012 indicating $x(i) < x(i+\tau) < x(i + 2\tau)$ and 201 for $x(i+\tau) < x(i + 2\tau) < x(i)$. Choices of $d$ and $\tau$ are optimized to maximize the permutation entropy. A (un)directed graph between the permutation states can be constructed as edges represent transitions between the states.

### Persistent scores and chaos indicators

For both of these construction methods, the distance matrix could then be obtained afterwards via the shortest path distance between the vertices of the network. Persistent diagrams would then be computed with clique/flag filtration. The authors focused mainly on $D = D_1$ (persistent classes of dimension 1) as (intuitively) periodicity usually represents only few long-lasting 1D holes in the graph. Chaos or period-doubling phenomena would tend to appear when there is a mixture of short-lasting 1D holes. With such intuition the paper introduces 3 persistent scores: small values mean more periodic while larger values mean more chaotic:

- periodicity score $P(D) = 1 - \dfrac{\mathrm{maxpers}(D)}{L_n}$ where $\mathrm{maxpers}(D) = \max_{x \in D} \mathrm{pers}(x)$ is the maximum persistence ($\mathrm{pers}(x) = |d_x-b_x|$) of a given diagram and $L_n$ is the maximum persistence of a diagram of a network with exactly one cycle born at 1 and same $n$ vertices. Higher $P(D)$ indicates limited persistence.
- ratio $M(D) = |D|/|V|$ between the number of classes in the diagram $D$ and number of vertices $V$. Larger $M(D)$ and $P(D)$ could represent many short-lasting periods leading up to chaos.
- normalized persistent entropy $E(D) = -\displaystyle\sum_{x \in D} \mathrm{npers}(x) \log_2(\mathrm{npers}(x))/\log_2(L(D))$ where $\mathrm{npers}(x) = \mathrm{pers}(x)/L(D)$ (i.e. normalized persistence) and $L(D) = \displaystyle \sum_{x \in D}\mathrm{pers}(x)$

The Lyapunov exponents $\lambda$ indicate the sensitivity of the trajectories of the dynamical variables due to perturbation to initial conditions: negative values usually correspond to stability and predictability, whereas positive exponents correspond to chaos and unpredictability.

Additionally, the authors also compared with network degree statistics including the mean and variance of the outgoing degree in the constructed network.

## Main results

The authors simulated the Rössler system (3 variables) and inspect the bifurcation of the dynamical system due to one of the parameters ($a$). They observed that the sign of the Lyapunov exponents agree with the magnitude of the persistent scores for both network constructions, especially with $P(D)$ and $E(D)$ while $M(D)$ is more variable. Additionally, certain ranges of $a$ in between indicate periodicity, which could also be captured with the sudden drops in these persistent scores. Looking only at the degree statistics of these networks would be quite hard to establish these phase transitions, especially with the period phase in between. They also simulated other systems such as the Lorenz system and find similar trends for the persistent scores.

However, the empirical data (EEG and ECG time series data) results are harder to distinguish. This is except for EEG using ordinal partition network method, they were able to distinguish between epileptic seizure patients and normal individuals. Interestingly, they did not discuss the fact that while they assumed seizure group to be chaotic, the persistent scores were actually lower for the seizure group. This indicates some periodic in seizure EEG data compared to normal EEG data. This actually makes sense under inspection of ictal data - a quick image search would lead to observation of ordinal periodicity within ictal data (the big, some times fast wax-and-wane of EEG signal). For the EEG data with kNN from Taken's embedding, similar trends could be observed though less clear, the most pronounced would be $M(D)$. This might be because Taken's embedding is generally sensitive to noise in empirical data.

Lastly, the authors examined how noise could affect the detection using the persistent scores and network degree statistics by adding Gaussian noise to one periodic and one chaotic variant of the Rössler system. The persistent scores, especially $E(D)$, require smaller SNR to detect chaos than network degree mean or variance.

## General impression

Hence, per the paper, persistent scores prove to be quite useful and robust for detecting dynamic states of time series data and dynamical systems in both simulations and certain situations of empirical data. I found the construction to networks from time series data quite interesting and useful, especially in describing the topology of the underlying attractors. From reading the paper, I think the idea itself is not that novel but the application of TDA and PH on the ordinal partition graph might be. And this adds to the growing works of applying TDA in dynamical systems, especially when one of the goals of the field (dynamical system, complex system) is to capture the qualitative nature of the system of interest. Though I am aware there exists a subfield beyond my grasp called topological dynamical systems that also bridges topology and dynamical systems, I believe there are still really interesting ongoing efforts (like discovering gravitational waves [@Bresten2019-si]) and challenges of capturing topology of dynamical systems in practice.

However, there are a few things I am unsure of in this paper. First, it is unclear to me how these scores can capture and distinguish some other dynamics like single fixed points and multiple periodicity like [@Mittal2017-hx]. Secondly, for comparison, the authors only chose 2-3 network statistics which focus mainly on degree distributions, without regards for graph connectedness, community or modularity. It would have been more thorough to compare these different graph statistics with the persistent scores to see whether it is truly the latter that reveal more clearly and robustly the topology of the underlying dynamics.

Third, it is unclear to me whether the authors used the largest Lyapunov or average exponents. Forth, it would be nice to also look at higher dimensions than just 1D holes, as we already have standard measures like the Lyapunov exponents for detection of chaos. For example, a [tutorial](https://docs-tda.giotto.ai/latest/notebooks/topology_time_series.html) on PH of the Lorenz system from `giotto-tda` shows that there is also a 2D hole, in addition to two long-lasting 1D hole, of a nonperiodic Lorenz system. Though it might be hard to interpret the existence of higher order holes and fit into the spectrum of periodicity-attractor-chaos, I think such quantification might result in interesting topological discoveries and further classification of chaos (if possible and not already exist) hidden within known dynamical systems like biological neural networks.

## Reproducibility

Although the paper does not provide their code repository, the authors have developed a TDA package for time series and dynamical system analysis called [`teaspoon`](https://github.com/lizliz/teaspoon), essentially to perform the network construction and persistent homology analysis within the package. Additionally there also exists another package called [`giotto-tda`](https://github.com/giotto-ai/giotto-tda) by another group that seems to have similar functionality at least for the kNN network construction from Taken's embedding part. Moreover, since most of the results are from simulations of dynamical systems, the details provided in the paper seem sufficient to reproduce the essential results. As for the experimental data, though the ECG data has a reference to a database, the reference to the EEG data is another academic paper without a reference to a data repository. Regardless, these types of data are now easily found online, so I think it is within expectation that the main results with these empirical data could be replicated.

## References
