---
bibliography: [./library.bib]
notes: convert by `pandoc --defaults front.yml  -s project-proposal.md -o project-proposal.pdf`
---

# Proposal: _Applying TDA on Purkinje population calcium data_

{% include head.html %}

{% katexmm %}

## Inspiration

With the incredible advancement of high resolution neural recording, manipulation technology and computing power, the amount of data for both experimental and simulated neural population activity is increasing tremendously (and personally in the direction of becoming quite overwhelming). Computational and analytical tools to interpret and build models from such volumes of data for hypothesis testing and exploratory purposes are catching up (though personally slowly). Tools like topological data analysis (TDA) and network analysis inevitably are necessary for extracting and exploring potential structures and patterns within these data.

__*TDA in neuroscience*__: Over the last decade (roughly two), there have been multiple applications of algebraic topology tools in neuroscience, extending analysis from graph theory methods. Aside from the more theoretical endeavors, these applications involve using TDA in neural population data across different subfields of computational neuroscience, most of which involve clique topology analysis. Examples span across different data domain and areas, from electrophysiological recordings in a specific area [@Giusti2015-uo] (rodent hippocampal place cells), to brain-wide structural human connectome [@Sizemore2018-ql], as well as within detailed biophysical neural simualations and models [@Reimann2017-ji].

I will be basing my project around the ideas and methods from [@Giusti2015-uo], which shows the geometric organization in hippocampal correlation structure across different states of the animal, including during wheel-running behavior and sleep. This is accomplished by compare the Betti number curves (edge density vs Betti numbers) from the data with those from generated random geometric networks, as well as comparing with a null based on shuffled data.

__*Data*__: Although there have been quite many population studies across other areas like neocortex, subcortical areas and hippocampus, not many network studies are done in the cerebellar Purkinje population recordings, even though these cells are among the popular neurons usually shown in textbooks with their beautiful complicated morphology, responsible for many developmental and learning functions such as motor learning. To my knowledge, there are no studies to date applying TDA in the cerrebellum population data.

Hence, I will be applying TDA on Purkinje cell population and drawing comparison with different models of random graphs, similar to [@Giusti2015-uo]. Briefly, the data are calcium imaging (proxy for neural activity) data of Purkinje population in rodent during awake states, respondong to sensory stimuli. Each trial is roughly 20 seconds of 60Hz sampling rate, and the stimulus (if present) is briefly on at 10-second. These data are obtained from my lab from another student's experiments (see _Acknowledgements_).

## Proposal

__*Note*__: I would tend to try *"deliverable"* first for testing, bechmarking purposes. But if there's something wrong, I might try the  *"tentative/alternative"*.

__*Similarity/distance matrix*__: First, from the data, I will build similarity (or distance) matrix from the activity around 2 seconds before (*base*) and after the stimulus onset (*stim*) for each trial separately.

- Deliverable: I will utilize the simple correlation coefficient $r_{i,j}$ as the first approach, as a measure of similarity. To transform to a distance, I could use $1 - r_{i,j}$
- Tentative/alternative: I could also use mutual information $I(X_i,X_j) = H(X_i) + H(X_j) - H(X_i,X_j)$, where $H(A)$ denotes the entropy of $A$, as another measure of similarity to include not only linear relationship between neural activity. However, these are not really distance metrics, so I can use $\sqrt{2(1-r_{i,j})}$ for correlation distance, or variation of information $V(X_i,X_j) = H(X_i,X_j) - I(X_i,X_j)$.
- Note: all these will result in unidirected weighted graphs, so filtration methods from class could be applied more straightforwardly.

__*Different null models*__:

- Deliverable: Following [@Giusti2015-uo], I will also build null models to compare with the matrices from the data above:
  1. Shuffled: matrices built by shuffling the original matrices
  2. Geometric: random geometric models with nodes sampled from a hypercube, and probablity of connectivity of two nodes decrease with their distance.
- Tentative/alternative: Other random structures I could include are:
  1. ER: Erdős–Rényi random graph model with matched statistics
  2. BA: Barabási–Albert model to generate scale-free networks (I did observe some baseline degree distributions looking close to that of a scale-free model in preliminary analysis)

__*TDA*__:

- Deliverable:
  1. I will generate Betti curves (up to $\beta_3(\rho)$) as a function of the edge density similarly to [@Giusti2015-uo] using TDA packages suggested in class.
  2. I will first confirm that I could replicate Fig. 2B (main) in [@Giusti2015-uo]. Then I will repeat for the data for each trial, as well as the null model counterparts.
  3. Similar to [@Giusti2015-uo], I will compare the integrated Betti curves ($S_{\beta}$) of the data and the $S_{\beta}$ distributions from the null models. Then I will use statistical test to observe if there is any significant difference between the data and the respective nulls.
  4. Additionally, I will also compare $S_{\beta}$ distributions aggregated from across different trials, between the *base* and *stim* windows, as well as between *sham* trial (no stimulus present) and *light* trial (trial with light stimulation to the animal).
- (Super-) tentative/alternative: there are also some recordings with other stimuli groups (*air puff*, *sound* in addition to *sham* and *light*). In the optimistic case where all the above goes smoothly, I could apply the same analysis on these additional groups, and perform comparison across groups. Furthermore, I could use persistance landscapes of these different groups and try to see if I can build a model to classify the different stimuli groups. Since the number of trials per group are small (usually less than 20 for practical reasons), I could use train on 95% of all groups and test on the remaining 5%, and repeat for different permutations of the dataset.

## Acknowledgements

The experimental data are obtained from my lab (Dr. Christian Hansel) by Silas Busch and Ting-Feng Lin. I would like to acknowledge and thank them for allowing me to use their data to play around for the project. Since these data are not published yet, I will not make the data public but the codes and final report will be.

{% endkatexmm %}

{% bibliography %}

{% include footer.html %}
