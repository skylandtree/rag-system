Published as a conference paper at ICLR 2017
段落总结：Published as a conference paper at ICLR 2017

**********段落分割**********
SEMI-SUPERVISED CLASSIFICATION WITH
段落总结：SEMI-SUPERVISED CLASSIFICATION WITH

**********段落分割**********
GRAPH CONVOLUTIONAL NETWORKSThomas N. KipfUniversity of AmsterdamT.N.Kipf@uva.nlMax WellingUniversity of AmsterdamCanadian Institute for Advanced Research (CIFAR)M.Welling@uva.nl
段落总结：GRAPH CONVOLUTIONAL NETWORKSThomas N

**********段落分割**********
ABSTRACTWe present a scalable approach for semi-supervised learning on graph-structureddata that is based on an efﬁcient variant of convolutional neural networks whichoperate directly on graphs. We motivate the choice of our convolutional archi-tecture via a localized ﬁrst-order approximation of spectral graph convolutions.Our model scales linearly in the number of graph edges and learns hidden layerrepresentations that encode both local graph structure and features of nodes. Ina number of experiments on citation networks and on a knowledge graph datasetwe demonstrate that our approach outperforms related methods by a signiﬁcantmargin.1
段落总结：ABSTRACTWe present a scalable approach for semi-supervised learning on graph-structureddata that is 

**********段落分割**********
INTRODUCTIONWe consider the problem of classifying nodes (such as documents) in a graph (such as a citationnetwork), where labels are only available for a small subset of nodes. This problem can be framedas graph-based semi-supervised learning, where label information is smoothed over the graph viasome form of explicit graph-based regularization (Zhu et al., 2003; Zhou et al., 2004; Belkin et al.,2006; Weston et al., 2012), e.g. by using a graph Laplacian regularization term in the loss function:L = L0 + λLreg ,withLreg =Xi,jAij∥f(Xi) −f(Xj)∥2 = f(X)⊤∆f(X) .(1)Here, L0 denotes the supervised loss w.r.t. the labeled part of the graph, f(·) can be a neural network-like differentiable function, λ is a weighing factor and X is a matrix of node feature vectors Xi.∆= D −A denotes the unnormalized graph Laplacian of an undirected graph G = (V, E) withN nodes vi ∈V, edges (vi, vj) ∈E, an adjacency matrix A ∈RN×N (binary or weighted) anda degree matrix Dii = Pj Aij. The formulation of Eq. 1 relies on the assumption that connectednodes in the graph are likely to share the same label. This assumption, however, might restrictmodeling capacity, as graph edges need not necessarily encode node similarity, but could containadditional information.In this work, we encode the graph structure directly using a neural network model f(X, A) andtrain on a supervised target L0 for all nodes with labels, thereby avoiding explicit graph-basedregularization in the loss function.
段落总结：INTRODUCTIONWe consider the problem of classifying nodes (such as documents) in a graph (such as a c

**********段落分割**********
Conditioning f(·) on the adjacency matrix of the graph willallow the model to distribute gradient information from the supervised loss L0 and will enable it tolearn representations of nodes both with and without labels.Our contributions are two-fold. Firstly, we introduce a simple and well-behaved layer-wise prop-agation rule for neural network models which operate directly on graphs and show how it can bemotivated from a ﬁrst-order approximation of spectral graph convolutions (Hammond et al., 2011).Secondly, we demonstrate how this form of a graph-based neural network model can be used forfast and scalable semi-supervised classiﬁcation of nodes in a graph. Experiments on a number ofdatasets demonstrate that our model compares favorably both in classiﬁcation accuracy and efﬁ-ciency (measured in wall-clock time) against state-of-the-art methods for semi-supervised learning.1arXiv:1609.02907v4  [cs.LG]  22 Feb 2017
段落总结：Conditioning f(·) on the adjacency matrix of the graph willallow the model to distribute gradient in

**********段落分割**********
[INTRODUCTION]Published as a conference paper at ICLR 20172
段落总结：[INTRODUCTION]Published as a conference paper at ICLR 20172

**********段落分割**********
FAST APPROXIMATE CONVOLUTIONS ON GRAPHSIn this section, we provide theoretical motivation for a speciﬁc graph-based neural network modelf(X, A) that we will use in the rest of this paper. We consider a multi-layer Graph ConvolutionalNetwork (GCN) with the following layer-wise propagation rule:H(l+1) = σ˜D−1
段落总结：FAST APPROXIMATE CONVOLUTIONS ON GRAPHSIn this section, we provide theoretical motivation for a spec

**********段落分割**********
2 ˜A ˜D−12 H(l)W (l).(2)Here, ˜A = A + IN is the adjacency matrix of the undirected graph G with added self-connections.IN is the identity matrix, ˜Dii = Pj ˜Aij and W (l) is a layer-speciﬁc trainable weight matrix. σ(·)denotes an activation function, such as the ReLU(·) = max(0, ·). H(l) ∈RN×D is the matrix of ac-tivations in the lth layer; H(0) = X. In the following, we show that the form of this propagation rulecan be motivated1 via a ﬁrst-order approximation of localized spectral ﬁlters on graphs (Hammondet al., 2011; Defferrard et al., 2016).2.1
段落总结：2 ˜A ˜D−12 H(l)W (l)

**********段落分割**********
SPECTRAL GRAPH CONVOLUTIONSWe consider spectral convolutions on graphs deﬁned as the multiplication of a signal x ∈RN (ascalar for every node) with a ﬁlter gθ = diag(θ) parameterized by θ ∈RN in the Fourier domain,i.e.:gθ ⋆x = UgθU ⊤x ,(3)where U is the matrix of eigenvectors of the normalized graph Laplacian L = IN −D−1
段落总结：SPECTRAL GRAPH CONVOLUTIONSWe consider spectral convolutions on graphs deﬁned as the multiplication 

**********段落分割**********
2 AD−12 =UΛU ⊤, with a diagonal matrix of its eigenvalues Λ and U ⊤x being the graph Fourier transformof x. We can understand gθ as a function of the eigenvalues of L, i.e. gθ(Λ). Evaluating Eq. 3 iscomputationally expensive, as multiplication with the eigenvector matrix U is O(N 2). Furthermore,computing the eigendecomposition of L in the ﬁrst place might be prohibitively expensive for largegraphs. To circumvent this problem, it was suggested in Hammond et al. (2011) that gθ(Λ) can bewell-approximated by a truncated expansion in terms of Chebyshev polynomials Tk(x) up to Kthorder:gθ′(Λ) ≈KXk=0θ′kTk(˜Λ) ,(4)with a rescaled ˜Λ =2λmax Λ −IN. λmax denotes the largest eigenvalue of L. θ′ ∈RK is now avector of Chebyshev coefﬁcients. The Chebyshev polynomials are recursively deﬁned as Tk(x) =2xTk−1(x) −Tk−2(x), with T0(x) = 1 and T1(x) = x. The reader is referred to Hammond et al.(2011) for an in-depth discussion of this approximation.Going back to our deﬁnition of a convolution of a signal x with a ﬁlter gθ′, we now have:gθ′ ⋆x ≈KXk=0θ′kTk(˜L)x ,(5)with ˜L =2λmax L −IN; as can easily be veriﬁed by noticing that (UΛU ⊤)k = UΛkU ⊤. Note thatthis expression is now K-localized since it is a Kth-order polynomial in the Laplacian, i.e. it dependsonly on nodes that are at maximum K steps away from the central node (Kth-order neighborhood).The complexity of evaluating Eq. 5 is O(|E|), i.e. linear in the number of edges.
段落总结：2 AD−12 =UΛU ⊤, with a diagonal matrix of its eigenvalues Λ and U ⊤x being the graph Fourier transfo

**********段落分割**********
Defferrard et al.(2016) use this K-localized convolution to deﬁne a convolutional neural network on graphs.2.2
段落总结：Defferrard et al.(2016) use this K-localized convolution to deﬁne a convolutional neural network on 

**********段落分割**********
LAYER-WISE LINEAR MODELA neural network model based on graph convolutions can therefore be built by stacking multipleconvolutional layers of the form of Eq. 5, each layer followed by a point-wise non-linearity. Now,imagine we limited the layer-wise convolution operation to K = 1 (see Eq. 5), i.e. a function that islinear w.r.t. L and therefore a linear function on the graph Laplacian spectrum.1We provide an alternative interpretation of this propagation rule based on the Weisfeiler-Lehman algorithm(Weisfeiler & Lehmann, 1968) in Appendix A.2
段落总结：LAYER-WISE LINEAR MODELA neural network model based on graph convolutions can therefore be built by 

**********段落分割**********
[LAYER-WISE LINEAR MODEL]Published as a conference paper at ICLR 2017In this way, we can still recover a rich class of convolutional ﬁlter functions by stacking multiplesuch layers, but we are not limited to the explicit parameterization given by, e.g., the Chebyshevpolynomials. We intuitively expect that such a model can alleviate the problem of overﬁtting onlocal neighborhood structures for graphs with very wide node degree distributions, such as socialnetworks, citation networks, knowledge graphs and many other real-world graph datasets. Addition-ally, for a ﬁxed computational budget, this layer-wise linear formulation allows us to build deepermodels, a practice that is known to improve modeling capacity on a number of domains (He et al.,2016).In this linear formulation of a GCN we further approximate λmax ≈2, as we can expect that neuralnetwork parameters will adapt to this change in scale during training. Under these approximationsEq. 5 simpliﬁes to:gθ′ ⋆x ≈θ′0x + θ′1 (L −IN) x = θ′0x −θ′1D−1
段落总结：[LAYER-WISE LINEAR MODEL]Published as a conference paper at ICLR 2017In this way, we can still recov

**********段落分割**********
2 AD−12 x ,(6)with two free parameters θ′0 and θ′1. The ﬁlter parameters can be shared over the whole graph.Successive application of ﬁlters of this form then effectively convolve the kth-order neighborhood ofa node, where k is the number of successive ﬁltering operations or convolutional layers in the neuralnetwork model.In practice, it can be beneﬁcial to constrain the number of parameters further to address overﬁttingand to minimize the number of operations (such as matrix multiplications) per layer. This leaves uswith the following expression:gθ ⋆x ≈θ
段落总结：2 AD−12 x ,(6)with two free parameters θ′0 and θ′1

**********段落分割**********
2 AD−12x ,(7)with a single parameter θ = θ′0 = −θ′1. Note that IN + D−1
段落总结：2 AD−12x ,(7)with a single parameter θ = θ′0 = −θ′1

**********段落分割**********
2 AD−12 now has eigenvalues inthe range [0, 2]. Repeated application of this operator can therefore lead to numerical instabilitiesand exploding/vanishing gradients when used in a deep neural network model. To alleviate thisproblem, we introduce the following renormalization trick: IN +D−1
段落总结：2 AD−12 now has eigenvalues inthe range [0, 2]

**********段落分割**********
2 ˜A ˜D−12 , with˜A = A + IN and ˜Dii = Pj ˜Aij.We can generalize this deﬁnition to a signal X ∈RN×C with C input channels (i.e. a C-dimensionalfeature vector for every node) and F ﬁlters or feature maps as follows:
段落总结：2 ˜A ˜D−12 , with˜A = A + IN and ˜Dii = Pj ˜Aij

**********段落分割**********
2 XΘ ,(8)where Θ ∈RC×F is now a matrix of ﬁlter parameters and Z ∈RN×F is the convolved signalmatrix. This ﬁltering operation has complexity O(|E|FC), as ˜AX can be efﬁciently implementedas a product of a sparse matrix with a dense matrix.3
段落总结：2 XΘ ,(8)where Θ ∈RC×F is now a matrix of ﬁlter parameters and Z ∈RN×F is the convolved signalmatrix

**********段落分割**********
SEMI-SUPERVISED NODE CLASSIFICATIONHaving introduced a simple, yet ﬂexible model f(X, A) for efﬁcient information propagation ongraphs, we can return to the problem of semi-supervised node classiﬁcation. As outlined in the in-troduction, we can relax certain assumptions typically made in graph-based semi-supervised learn-ing by conditioning our model f(X, A) both on the data X and on the adjacency matrix A of theunderlying graph structure. We expect this setting to be especially powerful in scenarios where theadjacency matrix contains information not present in the data X, such as citation links between doc-uments in a citation network or relations in a knowledge graph. The overall model, a multi-layerGCN for semi-supervised learning, is schematically depicted in Figure 1.3.1
段落总结：SEMI-SUPERVISED NODE CLASSIFICATIONHaving introduced a simple, yet ﬂexible model f(X, A) for efﬁcien

**********段落分割**********
EXAMPLEIn the following, we consider a two-layer GCN for semi-supervised node classiﬁcation on a graphwith a symmetric adjacency matrix A (binary or weighted). We ﬁrst calculate ˆA = ˜D−1
段落总结：EXAMPLEIn the following, we consider a two-layer GCN for semi-supervised node classiﬁcation on a gra

**********段落分割**********
2 ˜A ˜D−12 ina pre-processing step. Our forward model then takes the simple form:Z = f(X, A) = softmaxˆA ReLU
段落总结：2 ˜A ˜D−12 ina pre-processing step

**********段落分割**********
[W (1)]Published as a conference paper at ICLR 2017Cinput layerX1X2X3X4Foutput layerZ1Z2Z3Z4hiddenlayersY1Y4(a) Graph Convolutional Network(b) Hidden layer activationsFigure 1: Left: Schematic depiction of multi-layer Graph Convolutional Network (GCN) for semi-supervised learning with C input channels and F feature maps in the output layer. The graph struc-ture (edges shown as black lines) is shared over layers, labels are denoted by Yi. Right: t-SNE(Maaten & Hinton, 2008) visualization of hidden layer activations of a two-layer GCN trained onthe Cora dataset (Sen et al., 2008) using 5% of labels. Colors denote document class.Here, W (0) ∈RC×H is an input-to-hidden weight matrix for a hidden layer with H feature maps.W (1) ∈RH×F is a hidden-to-output weight matrix. The softmax activation function, deﬁned assoftmax(xi) = 1Z exp(xi) with Z = Pi exp(xi), is applied row-wise. For semi-supervised multi-class classiﬁcation, we then evaluate the cross-entropy error over all labeled examples:L = −Xl∈YLFXf=1Ylf ln Zlf ,(10)where YL is the set of node indices that have labels.The neural network weights W (0) and W (1) are trained using gradient descent. In this work, weperform batch gradient descent using the full dataset for every training iteration, which is a viableoption as long as datasets ﬁt in memory. Using a sparse representation for A, memory requirementis O(|E|), i.e. linear in the number of edges.
段落总结：[W (1)]Published as a conference paper at ICLR 2017Cinput layerX1X2X3X4Foutput layerZ1Z2Z3Z4hiddenl

**********段落分割**********
Stochasticity in the training process is introduced viadropout (Srivastava et al., 2014). We leave memory-efﬁcient extensions with mini-batch stochasticgradient descent for future work.3.2
段落总结：Stochasticity in the training process is introduced viadropout (Srivastava et al

**********段落分割**********
IMPLEMENTATIONIn practice, we make use of TensorFlow (Abadi et al., 2015) for an efﬁcient GPU-based imple-mentation2 of Eq. 9 using sparse-dense matrix multiplications. The computational complexity ofevaluating Eq. 9 is then O(|E|CHF), i.e. linear in the number of graph edges.4
段落总结：IMPLEMENTATIONIn practice, we make use of TensorFlow (Abadi et al

**********段落分割**********
RELATED WORKOur model draws inspiration both from the ﬁeld of graph-based semi-supervised learning and fromrecent work on neural networks that operate on graphs. In what follows, we provide a brief overviewon related work in both ﬁelds.4.1
段落总结：RELATED WORKOur model draws inspiration both from the ﬁeld of graph-based semi-supervised learning a

**********段落分割**********
GRAPH-BASED SEMI-SUPERVISED LEARNINGA large number of approaches for semi-supervised learning using graph representations have beenproposed in recent years, most of which fall into two broad categories: methods that use someform of explicit graph Laplacian regularization and graph embedding-based approaches. Prominentexamples for graph Laplacian regularization include label propagation (Zhu et al., 2003), manifoldregularization (Belkin et al., 2006) and deep semi-supervised embedding (Weston et al., 2012).2Code to reproduce our experiments is available at https://github.com/tkipf/gcn.4
段落总结：GRAPH-BASED SEMI-SUPERVISED LEARNINGA large number of approaches for semi-supervised learning using 

**********段落分割**********
[GRAPH-BASED SEMI-SUPERVISED LEARNING]Published as a conference paper at ICLR 2017Recently, attention has shifted to models that learn graph embeddings with methods inspired bythe skip-gram model (Mikolov et al., 2013). DeepWalk (Perozzi et al., 2014) learns embeddingsvia the prediction of the local neighborhood of nodes, sampled from random walks on the graph.LINE (Tang et al., 2015) and node2vec (Grover & Leskovec, 2016) extend DeepWalk with moresophisticated random walk or breadth-ﬁrst search schemes. For all these methods, however, a multi-step pipeline including random walk generation and semi-supervised training is required where eachstep has to be optimized separately. Planetoid (Yang et al., 2016) alleviates this by injecting labelinformation in the process of learning embeddings.4.2
段落总结：[GRAPH-BASED SEMI-SUPERVISED LEARNING]Published as a conference paper at ICLR 2017Recently, attentio

**********段落分割**********
NEURAL NETWORKS ON GRAPHSNeural networks that operate on graphs have previously been introduced in Gori et al. (2005);Scarselli et al. (2009) as a form of recurrent neural network. Their framework requires the repeatedapplication of contraction maps as propagation functions until node representations reach a stableﬁxed point. This restriction was later alleviated in Li et al. (2016) by introducing modern practicesfor recurrent neural network training to the original graph neural network framework. Duvenaudet al. (2015) introduced a convolution-like propagation rule on graphs and methods for graph-levelclassiﬁcation. Their approach requires to learn node degree-speciﬁc weight matrices which does notscale to large graphs with wide node degree distributions. Our model instead uses a single weightmatrix per layer and deals with varying node degrees through an appropriate normalization of theadjacency matrix (see Section 3.1).A related approach to node classiﬁcation with a graph-based neural network was recently introducedin Atwood & Towsley (2016). They report O(N 2) complexity, limiting the range of possible appli-cations. In a different yet related model, Niepert et al.
段落总结：NEURAL NETWORKS ON GRAPHSNeural networks that operate on graphs have previously been introduced in G

**********段落分割**********
(2016) convert graphs locally into sequencesthat are fed into a conventional 1D convolutional neural network, which requires the deﬁnition of anode ordering in a pre-processing step.Our method is based on spectral graph convolutional neural networks, introduced in Bruna et al.(2014) and later extended by Defferrard et al. (2016) with fast localized convolutions. In contrastto these works, we consider here the task of transductive node classiﬁcation within networks ofsigniﬁcantly larger scale. We show that in this setting, a number of simpliﬁcations (see Section 2.2)can be introduced to the original frameworks of Bruna et al. (2014) and Defferrard et al. (2016) thatimprove scalability and classiﬁcation performance in large-scale networks.5
段落总结：(2016) convert graphs locally into sequencesthat are fed into a conventional 1D convolutional neural

**********段落分割**********
EXPERIMENTSWe test our model in a number of experiments: semi-supervised document classiﬁcation in cita-tion networks, semi-supervised entity classiﬁcation in a bipartite graph extracted from a knowledgegraph, an evaluation of various graph propagation models and a run-time analysis on random graphs.5.1
段落总结：EXPERIMENTSWe test our model in a number of experiments: semi-supervised document classiﬁcation in c

**********段落分割**********
DATASETSWe closely follow the experimental setup in Yang et al. (2016). Dataset statistics are summarizedin Table 1. In the citation network datasets—Citeseer, Cora and Pubmed (Sen et al., 2008)—nodesare documents and edges are citation links. Label rate denotes the number of labeled nodes that areused for training divided by the total number of nodes in each dataset. NELL (Carlson et al., 2010;Yang et al., 2016) is a bipartite graph dataset extracted from a knowledge graph with 55,864 relationnodes and 9,891 entity nodes.Table 1: Dataset statistics, as reported in Yang et al. (2016).DatasetTypeNodesEdgesClassesFeaturesLabel rateCiteseerCitation network3,3274,73263,7030.036CoraCitation network2,7085,42971,4330.052PubmedCitation network19,71744,33835000.003NELLKnowledge graph65,755266,1442105,4140.0015
段落总结：DATASETSWe closely follow the experimental setup in Yang et al

**********段落分割**********
[DATASETS]Published as a conference paper at ICLR 2017Citation networksWe consider three citation network datasets: Citeseer, Cora and Pubmed (Senet al., 2008). The datasets contain sparse bag-of-words feature vectors for each document and a listof citation links between documents. We treat the citation links as (undirected) edges and constructa binary, symmetric adjacency matrix A. Each document has a class label. For training, we only use20 labels per class, but all feature vectors.NELLNELL is a dataset extracted from the knowledge graph introduced in (Carlson et al., 2010).A knowledge graph is a set of entities connected with directed, labeled edges (relations). We followthe pre-processing scheme as described in Yang et al. (2016). We assign separate relation nodesr1 and r2 for each entity pair (e1, r, e2) as (e1, r1) and (e2, r2). Entity nodes are described bysparse feature vectors. We extend the number of features in NELL by assigning a unique one-hotrepresentation for every relation node, effectively resulting in a 61,278-dim sparse feature vector pernode. The semi-supervised task here considers the extreme case of only a single labeled exampleper class in the training set. We construct a binary, symmetric adjacency matrix from this graph bysetting entries Aij = 1, if one or more edges are present between nodes i and j.Random graphsWe simulate random graph datasets of various sizes for experiments where wemeasure training time per epoch.
段落总结：[DATASETS]Published as a conference paper at ICLR 2017Citation networksWe consider three citation ne

**********段落分割**********
For a dataset with N nodes we create a random graph assigning2N edges uniformly at random. We take the identity matrix IN as input feature matrix X, therebyimplicitly taking a featureless approach where the model is only informed about the identity of eachnode, speciﬁed by a unique one-hot vector. We add dummy labels Yi = 1 for every node.5.2
段落总结：For a dataset with N nodes we create a random graph assigning2N edges uniformly at random

**********段落分割**********
EXPERIMENTAL SET-UPUnless otherwise noted, we train a two-layer GCN as described in Section 3.1 and evaluate pre-diction accuracy on a test set of 1,000 labeled examples. We provide additional experiments usingdeeper models with up to 10 layers in Appendix B. We choose the same dataset splits as in Yang et al.(2016) with an additional validation set of 500 labeled examples for hyperparameter optimization(dropout rate for all layers, L2 regularization factor for the ﬁrst GCN layer and number of hiddenunits). We do not use the validation set labels for training.For the citation network datasets, we optimize hyperparameters on Cora only and use the same setof parameters for Citeseer and Pubmed. We train all models for a maximum of 200 epochs (trainingiterations) using Adam (Kingma & Ba, 2015) with a learning rate of 0.01 and early stopping with awindow size of 10, i.e. we stop training if the validation loss does not decrease for 10 consecutiveepochs. We initialize weights using the initialization described in Glorot & Bengio (2010) andaccordingly (row-)normalize input feature vectors. On the random graph datasets, we use a hiddenlayer size of 32 units and omit regularization (i.e. neither dropout nor L2 regularization).5.3
段落总结：EXPERIMENTAL SET-UPUnless otherwise noted, we train a two-layer GCN as described in Section 3

**********段落分割**********
BASELINESWe compare against the same baseline methods as in Yang et al. (2016), i.e. label propagation(LP) (Zhu et al., 2003), semi-supervised embedding (SemiEmb) (Weston et al., 2012), manifoldregularization (ManiReg) (Belkin et al., 2006) and skip-gram based graph embeddings (DeepWalk)(Perozzi et al., 2014). We omit TSVM (Joachims, 1999), as it does not scale to the large number ofclasses in one of our datasets.We further compare against the iterative classiﬁcation algorithm (ICA) proposed in Lu & Getoor(2003) in conjunction with two logistic regression classiﬁers, one for local node features alone andone for relational classiﬁcation using local features and an aggregation operator as described inSen et al. (2008). We ﬁrst train the local classiﬁer using all labeled training set nodes and useit to bootstrap class labels of unlabeled nodes for relational classiﬁer training. We run iterativeclassiﬁcation (relational classiﬁer) with a random node ordering for 10 iterations on all unlabelednodes (bootstrapped using the local classiﬁer). L2 regularization parameter and aggregation operator(count vs. prop, see Sen et al. (2008)) are chosen based on validation set performance for each datasetseparately.Lastly, we compare against Planetoid (Yang et al., 2016), where we always choose their best-performing model variant (transductive vs. inductive) as a baseline.6
段落总结：BASELINESWe compare against the same baseline methods as in Yang et al

**********段落分割**********
[BASELINES]Published as a conference paper at ICLR 20176
段落总结：[BASELINES]Published as a conference paper at ICLR 20176

**********段落分割**********
SEMI-SUPERVISED NODE CLASSIFICATIONResults are summarized in Table 2. Reported numbers denote classiﬁcation accuracy in percent. ForICA, we report the mean accuracy of 100 runs with random node orderings. Results for all otherbaseline methods are taken from the Planetoid paper (Yang et al., 2016). Planetoid* denotes the bestmodel for the respective dataset out of the variants presented in their paper.Table 2: Summary of results in terms of classiﬁcation accuracy (in percent).MethodCiteseerCoraPubmedNELLManiReg [3]60.159.570.721.8SemiEmb [28]59.659.071.126.7
段落总结：SEMI-SUPERVISED NODE CLASSIFICATIONResults are summarized in Table 2

**********段落分割**********
LP [32]45.368.063.026.5DeepWalk [22]43.267.265.358.1
段落总结：LP [32]45.368.063.026.5DeepWalk [22]43.267.265.358.1

**********段落分割**********
ICA [18]69.175.173.923.1Planetoid* [29]64.7 (26s)75.7 (13s)77.2 (25s)61.9 (185s)GCN (this paper)70.3 (7s)81.5 (4s)79.0 (38s)66.0 (48s)GCN (rand. splits)67.9 ± 0.580.1 ± 0.578.9 ± 0.758.4 ± 1.7We further report wall-clock training time in seconds until convergence (in brackets) for our method(incl. evaluation of validation error) and for Planetoid. For the latter, we used an implementation pro-vided by the authors3 and trained on the same hardware (with GPU) as our GCN model. We trainedand tested our model on the same dataset splits as in Yang et al. (2016) and report mean accuracyof 100 runs with random weight initializations. We used the following sets of hyperparameters forCiteseer, Cora and Pubmed: 0.5 (dropout rate), 5 · 10−4 (L2 regularization) and 16 (number of hid-den units); and for NELL: 0.1 (dropout rate), 1 · 10−5 (L2 regularization) and 64 (number of hiddenunits).In addition, we report performance of our model on 10 randomly drawn dataset splits of the samesize as in Yang et al. (2016), denoted by GCN (rand. splits). Here, we report mean and standarderror of prediction accuracy on the test set split in percent.6.2
段落总结：ICA [18]69.175.173.923.1Planetoid* [29]64.7 (26s)75.7 (13s)77.2 (25s)61.9 (185s)GCN (this paper)70.3

**********段落分割**********
EVALUATION OF PROPAGATION MODELWe compare different variants of our proposed per-layer propagation model on the citation networkdatasets. We follow the experimental set-up described in the previous section. Results are summa-rized in Table 3. The propagation model of our original GCN model is denoted by renormalizationtrick (in bold). In all other cases, the propagation model of both neural network layers is replacedwith the model speciﬁed under propagation model. Reported numbers denote mean classiﬁcationaccuracy for 100 repeated runs with random weight matrix initializations. In case of multiple vari-ables Θi per layer, we impose L2 regularization on all weight matrices of the ﬁrst layer.Table 3: Comparison of propagation models.DescriptionPropagation modelCiteseerCoraPubmedChebyshev ﬁlter (Eq. 5)K = 3PKk=0 Tk(˜L)XΘk69.879.574.4K = 269.681.273.81st-order model (Eq. 6)
段落总结：EVALUATION OF PROPAGATION MODELWe compare different variants of our proposed per-layer propagation m

**********段落分割**********
2 AD−12 XΘ168.380.077.5Single parameter (Eq. 7)
段落总结：2 AD−12 XΘ168.380.077.5Single parameter (Eq. 7)

**********段落分割**********
2 AD−12 )XΘ69.379.277.4Renormalization trick (Eq. 8)˜D−1
段落总结：2 AD−12 )XΘ69.379.277.4Renormalization trick (Eq. 8)˜D−1

**********段落分割**********
2 ˜A ˜D−12 XΘ70.381.579.01st-order term onlyD−1
段落总结：2 ˜A ˜D−12 XΘ70.381.579.01st-order term onlyD−1

**********段落分割**********
2 AD−12 XΘ68.780.577.8Multi-layer perceptronXΘ46.555.171.43https://github.com/kimiyoung/planetoid7
段落总结：2 AD−12 XΘ68.780.577.8Multi-layer perceptronXΘ46.555.171.43https://github.com/kimiyoung/planetoid7

**********段落分割**********
[2 AD−1]Published as a conference paper at ICLR 20176.3
段落总结：[2 AD−1]Published as a conference paper at ICLR 20176

**********段落分割**********
TRAINING TIME PER EPOCH1k10k100k1M10M
段落总结：TRAINING TIME PER EPOCH1k10k100k1M10M

**********段落分割**********
# Edges10-310-210-1100101Sec./epoch*GPUCPUFigure 2: Wall-clock time per epoch for randomgraphs. (*) indicates out-of-memory error.Here, we report results for the mean trainingtime per epoch (forward pass, cross-entropycalculation, backward pass) for 100 epochs onsimulated random graphs, measured in secondswall-clock time. See Section 5.1 for a detaileddescription of the random graph dataset usedin these experiments. We compare results ona GPU and on a CPU-only implementation4 inTensorFlow (Abadi et al., 2015). Figure 2 sum-marizes the results.7
段落总结：# Edges10-310-210-1100101Sec

**********段落分割**********
SEMI-SUPERVISED MODELIn the experiments demonstrated here, our method for semi-supervised node classiﬁcation outper-forms recent related methods by a signiﬁcant margin. Methods based on graph-Laplacian regular-ization (Zhu et al., 2003; Belkin et al., 2006; Weston et al., 2012) are most likely limited due to theirassumption that edges encode mere similarity of nodes. Skip-gram based methods on the other handare limited by the fact that they are based on a multi-step pipeline which is difﬁcult to optimize.Our proposed model can overcome both limitations, while still comparing favorably in terms of ef-ﬁciency (measured in wall-clock time) to related methods. Propagation of feature information fromneighboring nodes in every layer improves classiﬁcation performance in comparison to methods likeICA (Lu & Getoor, 2003), where only label information is aggregated.We have further demonstrated that the proposed renormalized propagation model (Eq. 8) offers bothimproved efﬁciency (fewer parameters and operations, such as multiplication or addition) and betterpredictive performance on a number of datasets compared to a na¨ıve 1st-order model (Eq. 6) orhigher-order graph convolutional models using Chebyshev polynomials (Eq. 5).7.2
段落总结：SEMI-SUPERVISED MODELIn the experiments demonstrated here, our method for semi-supervised node class

**********段落分割**********
LIMITATIONS AND FUTURE WORKHere, we describe several limitations of our current model and outline how these might be overcomein future work.Memory requirementIn the current setup with full-batch gradient descent, memory requirementgrows linearly in the size of the dataset. We have shown that for large graphs that do not ﬁt in GPUmemory, training on CPU can still be a viable option. Mini-batch stochastic gradient descent canalleviate this issue. The procedure of generating mini-batches, however, should take into account thenumber of layers in the GCN model, as the Kth-order neighborhood for a GCN with K layers has tobe stored in memory for an exact procedure. For very large and densely connected graph datasets,further approximations might be necessary.Directed edges and edge featuresOur framework currently does not naturally support edge fea-tures and is limited to undirected graphs (weighted or unweighted). Results on NELL howevershow that it is possible to handle both directed edges and edge features by representing the originaldirected graph as an undirected bipartite graph with additional nodes that represent edges in theoriginal graph (see Section 5.1 for details).Limiting assumptionsThrough the approximations introduced in Section 2, we implicitly assumelocality (dependence on the Kth-order neighborhood for a GCN with K layers) and equal impor-tance of self-connections vs. edges to neighboring nodes.
段落总结：LIMITATIONS AND FUTURE WORKHere, we describe several limitations of our current model and outline ho

**********段落分割**********
For some datasets, however, it might bebeneﬁcial to introduce a trade-off parameter λ in the deﬁnition of ˜A:˜A = A + λIN .(11)4Hardware used: 16-core Intel R⃝Xeon R⃝CPU E5-2640 v3 @ 2.60GHz, GeForce R⃝GTX TITAN X8
段落总结：For some datasets, however, it might bebeneﬁcial to introduce a trade-off parameter λ in the deﬁniti

**********段落分割**********
[LIMITATIONS AND FUTURE WORK]Published as a conference paper at ICLR 2017This parameter now plays a similar role as the trade-off parameter between supervised and unsuper-vised loss in the typical semi-supervised setting (see Eq. 1). Here, however, it can be learned viagradient descent.8
段落总结：[LIMITATIONS AND FUTURE WORK]Published as a conference paper at ICLR 2017This parameter now plays a 

**********段落分割**********
CONCLUSIONWe have introduced a novel approach for semi-supervised classiﬁcation on graph-structured data.Our GCN model uses an efﬁcient layer-wise propagation rule that is based on a ﬁrst-order approx-imation of spectral convolutions on graphs. Experiments on a number of network datasets suggestthat the proposed GCN model is capable of encoding both graph structure and node features in away useful for semi-supervised classiﬁcation. In this setting, our model outperforms several recentlyproposed methods by a signiﬁcant margin, while being computationally efﬁcient.
段落总结：CONCLUSIONWe have introduced a novel approach for semi-supervised classiﬁcation on graph-structured 

**********段落分割**********
ACKNOWLEDGMENTSWe would like to thank Christos Louizos, Taco Cohen, Joan Bruna, Zhilin Yang, Dave Herman,Pramod Sinha and Abdul-Saboor Sheikh for helpful discussions. This research was funded by SAP.
段落总结：ACKNOWLEDGMENTSWe would like to thank Christos Louizos, Taco Cohen, Joan Bruna, Zhilin Yang, Dave He

**********段落分割**********
REFERENCESMart´ın Abadi et al. TensorFlow: Large-scale machine learning on heterogeneous systems, 2015.James Atwood and Don Towsley. Diffusion-convolutional neural networks. In Advances in neuralinformation processing systems (NIPS), 2016.Mikhail Belkin, Partha Niyogi, and Vikas Sindhwani. Manifold regularization: A geometric frame-work for learning from labeled and unlabeled examples. Journal of machine learning research(JMLR), 7(Nov):2399–2434, 2006.Ulrik Brandes, Daniel Delling, Marco Gaertler, Robert Gorke, Martin Hoefer, Zoran Nikoloski,and Dorothea Wagner. On modularity clustering. IEEE Transactions on Knowledge and DataEngineering, 20(2):172–188, 2008.Joan Bruna, Wojciech Zaremba, Arthur Szlam, and Yann LeCun. Spectral networks and locallyconnected networks on graphs. In International Conference on Learning Representations (ICLR),2014.Andrew Carlson, Justin Betteridge, Bryan Kisiel, Burr Settles, Estevam R. Hruschka Jr, and Tom M.Mitchell. Toward an architecture for never-ending language learning. In AAAI, volume 5, pp. 3,2010.Micha¨el Defferrard, Xavier Bresson, and Pierre Vandergheynst. Convolutional neural networks ongraphs with fast localized spectral ﬁltering. In Advances in neural information processing systems
段落总结：REFERENCESMart´ın Abadi et al

**********段落分割**********
(NIPS), 2016.Brendan L. Douglas. The Weisfeiler-Lehman method and graph isomorphism testing. arXiv preprintarXiv:1101.5211, 2011.David K. Duvenaud, Dougal Maclaurin, Jorge Iparraguirre, Rafael Bombarell, Timothy Hirzel, Al´anAspuru-Guzik, and Ryan P. Adams. Convolutional networks on graphs for learning molecularﬁngerprints. In Advances in neural information processing systems (NIPS), pp. 2224–2232, 2015.Xavier Glorot and Yoshua Bengio. Understanding the difﬁculty of training deep feedforward neuralnetworks. In AISTATS, volume 9, pp. 249–256, 2010.Marco Gori, Gabriele Monfardini, and Franco Scarselli. A new model for learning in graph domains.In Proceedings. 2005 IEEE International Joint Conference on Neural Networks., volume 2, pp.
段落总结：(NIPS), 2016.Brendan L. Douglas. The Weisfeiler-Lehman method and graph isomorphism testing. arXiv p

**********段落分割**********
729–734. IEEE, 2005.Aditya Grover and Jure Leskovec. node2vec: Scalable feature learning for networks. In Proceedingsof the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining.
段落总结：729–734. IEEE, 2005.Aditya Grover and Jure Leskovec. node2vec: Scalable feature learning for network

**********段落分割**********
[ACM, 2016.]Published as a conference paper at ICLR 2017David K. Hammond, Pierre Vandergheynst, and R´emi Gribonval. Wavelets on graphs via spectralgraph theory. Applied and Computational Harmonic Analysis, 30(2):129–150, 2011.Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recog-nition. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2016.Thorsten Joachims. Transductive inference for text classiﬁcation using support vector machines. InInternational Conference on Machine Learning (ICML), volume 99, pp. 200–209, 1999.Diederik P. Kingma and Jimmy Lei Ba. Adam: A method for stochastic optimization. In Interna-tional Conference on Learning Representations (ICLR), 2015.Yujia Li, Daniel Tarlow, Marc Brockschmidt, and Richard Zemel. Gated graph sequence neuralnetworks. In International Conference on Learning Representations (ICLR), 2016.Qing Lu and Lise Getoor. Link-based classiﬁcation. In International Conference on Machine Learn-ing (ICML), volume 3, pp. 496–503, 2003.Laurens van der Maaten and Geoffrey Hinton. Visualizing data using t-sne. Journal of MachineLearning Research (JMLR), 9(Nov):2579–2605, 2008.Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg S. Corrado, and Jeff Dean. Distributed repre-sentations of words and phrases and their compositionality. In Advances in neural informationprocessing systems (NIPS), pp. 3111–3119, 2013.Mathias Niepert, Mohamed Ahmed, and Konstantin Kutzkov.
段落总结：[ACM, 2016.]Published as a conference paper at ICLR 2017David K. Hammond, Pierre Vandergheynst, and 

**********段落分割**********
Learning convolutional neural net-works for graphs. In International Conference on Machine Learning (ICML), 2016.Bryan Perozzi, Rami Al-Rfou, and Steven Skiena.Deepwalk: Online learning of social repre-sentations. In Proceedings of the 20th ACM SIGKDD international conference on Knowledgediscovery and data mining, pp. 701–710. ACM, 2014.Franco Scarselli, Marco Gori, Ah Chung Tsoi, Markus Hagenbuchner, and Gabriele Monfardini.The graph neural network model. IEEE Transactions on Neural Networks, 20(1):61–80, 2009.Prithviraj Sen, Galileo Namata, Mustafa Bilgic, Lise Getoor, Brian Galligher, and Tina Eliassi-Rad.Collective classiﬁcation in network data. AI magazine, 29(3):93, 2008.Nitish Srivastava, Geoffrey E. Hinton, Alex Krizhevsky, Ilya Sutskever, and Ruslan Salakhutdinov.Dropout: a simple way to prevent neural networks from overﬁtting. Journal of Machine LearningResearch (JMLR), 15(1):1929–1958, 2014.Jian Tang, Meng Qu, Mingzhe Wang, Ming Zhang, Jun Yan, and Qiaozhu Mei. Line: Large-scaleinformation network embedding. In Proceedings of the 24th International Conference on WorldWide Web, pp. 1067–1077. ACM, 2015.Boris Weisfeiler and A. A. Lehmann. A reduction of a graph to a canonical form and an algebraarising during this reduction. Nauchno-Technicheskaya Informatsia, 2(9):12–16, 1968.Jason Weston, Fr´ed´eric Ratle, Hossein Mobahi, and Ronan Collobert. Deep learning via semi-supervised embedding. In Neural Networks: Tricks of the Trade, pp. 639–655.
段落总结：Learning convolutional neural net-works for graphs

**********段落分割**********
Springer, 2012.Zhilin Yang, William Cohen, and Ruslan Salakhutdinov. Revisiting semi-supervised learning withgraph embeddings. In International Conference on Machine Learning (ICML), 2016.Wayne W. Zachary. An information ﬂow model for conﬂict and ﬁssion in small groups. Journal ofanthropological research, pp. 452–473, 1977.Dengyong Zhou, Olivier Bousquet, Thomas Navin Lal, Jason Weston, and Bernhard Sch¨olkopf.Learning with local and global consistency. In Advances in neural information processing systems(NIPS), volume 16, pp. 321–328, 2004.Xiaojin Zhu, Zoubin Ghahramani, and John Lafferty. Semi-supervised learning using gaussian ﬁeldsand harmonic functions. In International Conference on Machine Learning (ICML), volume 3,pp. 912–919, 2003.10
段落总结：Springer, 2012.Zhilin Yang, William Cohen, and Ruslan Salakhutdinov. Revisiting semi-supervised lear

**********段落分割**********
Published as a conference paper at ICLR 2017A
段落总结：Published as a conference paper at ICLR 2017A

**********段落分割**********
RELATION TO WEISFEILER-LEHMAN ALGORITHMA neural network model for graph-structured data should ideally be able to learn representations ofnodes in a graph, taking both the graph structure and feature description of nodes into account. Awell-studied framework for the unique assignment of node labels given a graph and (optionally) dis-crete initial node labels is provided by the 1-dim Weisfeiler-Lehman (WL-1) algorithm (Weisfeiler& Lehmann, 1968):Algorithm 1: WL-1 algorithm (Weisfeiler & Lehmann, 1968)Input: Initial node coloring (h(0)1 , h(0)2 , ..., h(0)N )Output: Final node coloring (h(T )1, h(T )2, ..., h(T )N )t ←0;repeatfor vi ∈V doh(t+1)i←hashPj∈Ni h(t)j;t ←t + 1;until stable node coloring is reached;Here, h(t)idenotes the coloring (label assignment) of node vi (at iteration t) and Ni is its set ofneighboring node indices (irrespective of whether the graph includes self-connections for every nodeor not). hash(·) is a hash function. For an in-depth mathematical discussion of the WL-1 algorithmsee, e.g., Douglas (2011).We can replace the hash function in Algorithm 1 with a neural network layer-like differentiablefunction with trainable parameters as follows:h(l+1)i= σXj∈Ni1cijh(l)j W (l),(12)where cij is an appropriately chosen normalization constant for the edge (vi, vj). Further, we cantake h(l)inow to be a vector of activations of node i in the lth neural network layer.
段落总结：RELATION TO WEISFEILER-LEHMAN ALGORITHMA neural network model for graph-structured data should ideal

**********段落分割**********
W (l) is alayer-speciﬁc weight matrix and σ(·) denotes a differentiable, non-linear activation function.By choosing cij =pdidj, where di = |Ni| denotes the degree of node vi, we recover the propaga-tion rule of our Graph Convolutional Network (GCN) model in vector form (see Eq. 2)5.This—loosely speaking—allows us to interpret our GCN model as a differentiable and parameter-ized generalization of the 1-dim Weisfeiler-Lehman algorithm on graphs.A.1
段落总结：W (l) is alayer-speciﬁc weight matrix and σ(·) denotes a differentiable, non-linear activation funct

**********段落分割**********
NODE EMBEDDINGS WITH RANDOM WEIGHTSFrom the analogy with the Weisfeiler-Lehman algorithm, we can understand that even an untrainedGCN model with random weights can serve as a powerful feature extractor for nodes in a graph. Asan example, consider the following 3-layer GCN model:Z = tanhˆA tanhˆA tanh
段落总结：NODE EMBEDDINGS WITH RANDOM WEIGHTSFrom the analogy with the Weisfeiler-Lehman algorithm, we can und

**********段落分割**********
W (2),(13)with weight matrices W (l) initialized at random using the initialization described in Glorot & Bengio(2010). ˆA, X and Z are deﬁned as in Section 3.1.We apply this model on Zachary’s karate club network (Zachary, 1977). This graph contains 34nodes, connected by 154 (undirected and unweighted) edges. Every node is labeled by one offour classes, obtained via modularity-based clustering (Brandes et al., 2008). See Figure 3a for anillustration.5Note that we here implicitly assume that self-connections have already been added to every node in thegraph (for a clutter-free notation).11
段落总结：W (2),(13)with weight matrices W (l) initialized at random using the initialization described in Gl

**********段落分割**********
[W (2)]Published as a conference paper at ICLR 2017(a) Karate club network(b) Random weight embeddingFigure 3: Left: Zachary’s karate club network (Zachary, 1977), colors denote communities obtainedvia modularity-based clustering (Brandes et al., 2008). Right: Embeddings obtained from an un-trained 3-layer GCN model (Eq. 13) with random weights applied to the karate club network. Bestviewed on a computer screen.We take a featureless approach by setting X = IN, where IN is the N by N identity matrix. N isthe number of nodes in the graph. Note that nodes are randomly ordered (i.e. ordering contains noinformation). Furthermore, we choose a hidden layer dimensionality6 of 4 and a two-dimensionaloutput (so that the output can immediately be visualized in a 2-dim plot).Figure 3b shows a representative example of node embeddings (outputs Z) obtained from an un-trained GCN model applied to the karate club network. These results are comparable to embeddingsobtained from DeepWalk (Perozzi et al., 2014), which uses a more expensive unsupervised trainingprocedure.A.2
段落总结：[W (2)]Published as a conference paper at ICLR 2017(a) Karate club network(b) Random weight embeddi

**********段落分割**********
SEMI-SUPERVISED NODE EMBEDDINGSOn this simple example of a GCN applied to the karate club network it is interesting to observe howembeddings react during training on a semi-supervised classiﬁcation task. Such a visualization (seeFigure 4) provides insights into how the GCN model can make use of the graph structure (and offeatures extracted from the graph structure at later layers) to learn embeddings that are useful for aclassiﬁcation task.We consider the following semi-supervised learning setup: we add a softmax layer on top of ourmodel (Eq. 13) and train using only a single labeled example per class (i.e. a total number of 4 labelednodes). We train for 300 training iterations using Adam (Kingma & Ba, 2015) with a learning rateof 0.01 on a cross-entropy loss.Figure 4 shows the evolution of node embeddings over a number of training iterations. The modelsucceeds in linearly separating the communities based on minimal supervision and the graph struc-ture alone. A video of the full training process can be found on our website7.6We originally experimented with a hidden layer dimensionality of 2 (i.e. same as output layer), but observedthat a dimensionality of 4 resulted in less frequent saturation of tanh(·) units and therefore visually morepleasing results.7http://tkipf.github.io/graph-convolutional-networks/12
段落总结：SEMI-SUPERVISED NODE EMBEDDINGSOn this simple example of a GCN applied to the karate club network it

**********段落分割**********
[SEMI-SUPERVISED NODE EMBEDDINGS]Published as a conference paper at ICLR 2017(a) Iteration 25(b) Iteration 50(c) Iteration 75(d) Iteration 100(e) Iteration 200(f) Iteration 300Figure 4: Evolution of karate club network node embeddings obtained from a GCN model after anumber of semi-supervised training iterations. Colors denote class. Nodes of which labels wereprovided during training (one per class) are highlighted (grey outline). Grey links between nodesdenote graph edges. Best viewed on a computer screen.13
段落总结：[SEMI-SUPERVISED NODE EMBEDDINGS]Published as a conference paper at ICLR 2017(a) Iteration 25(b) Ite

**********段落分割**********
Published as a conference paper at ICLR 2017B
段落总结：Published as a conference paper at ICLR 2017B

**********段落分割**********
EXPERIMENTS ON MODEL DEPTHIn these experiments, we investigate the inﬂuence of model depth (number of layers) on classiﬁcationperformance. We report results on a 5-fold cross-validation experiment on the Cora, Citeseer andPubmed datasets (Sen et al., 2008) using all labels. In addition to the standard GCN model (Eq. 2),we report results on a model variant where we use residual connections (He et al., 2016) betweenhidden layers to facilitate training of deeper models by enabling the model to carry over informationfrom the previous layer’s input:H(l+1) = σ˜D−1
段落总结：EXPERIMENTS ON MODEL DEPTHIn these experiments, we investigate the inﬂuence of model depth (number o

**********段落分割**********
2 ˜A ˜D−12 H(l)W (l)+ H(l) .(14)On each cross-validation split, we train for 400 epochs (without early stopping) using the Adamoptimizer (Kingma & Ba, 2015) with a learning rate of 0.01. Other hyperparameters are chosen asfollows: 0.5 (dropout rate, ﬁrst and last layer), 5 · 10−4 (L2 regularization, ﬁrst layer), 16 (numberof units for each hidden layer) and 0.01 (learning rate). Results are summarized in Figure 5.12345678910Number of layers0.500.550.600.650.700.750.800.850.90AccuracyCiteseerTrainTrain (Residual)TestTest (Residual)12345678910Number of layers0.550.600.650.700.750.800.850.900.95AccuracyCoraTrainTrain (Residual)TestTest (Residual)12345678910Number of layers0.760.780.800.820.840.860.88AccuracyPubmedTrainTrain (Residual)TestTest (Residual)Figure 5: Inﬂuence of model depth (number of layers) on classiﬁcation performance. Markersdenote mean classiﬁcation accuracy (training vs. testing) for 5-fold cross-validation. Shaded areasdenote standard error. We show results both for a standard GCN model (dashed lines) and a modelwith added residual connections (He et al., 2016) between hidden layers (solid lines).For the datasets considered here, best results are obtained with a 2- or 3-layer model. We observethat for models deeper than 7 layers, training without the use of residual connections can becomedifﬁcult, as the effective context size for each node increases by the size of its Kth-order neighbor-hood (for a model with K layers) with each additional layer.
段落总结：2 ˜A ˜D−12 H(l)W (l)+ H(l)

**********段落分割**********
Furthermore, overﬁtting can becomean issue as the number of parameters increases with model depth.14
段落总结：Furthermore, overﬁtting can becomean issue as the number of parameters increases with model depth
