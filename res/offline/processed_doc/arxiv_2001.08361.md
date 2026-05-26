Scaling Laws for Neural Language ModelsJared Kaplan ∗Johns Hopkins University, OpenAIjaredk@jhu.eduSam McCandlish∗OpenAIsam@openai.comTom HenighanOpenAIhenighan@openai.comTom B. BrownOpenAItom@openai.comBenjamin ChessOpenAIbchess@openai.comRewon ChildOpenAIrewon@openai.comScott GrayOpenAIscott@openai.comAlec RadfordOpenAIalec@openai.comJeffrey WuOpenAIjeffwu@openai.comDario AmodeiOpenAIdamodei@openai.comAbstractWe study empirical scaling laws for language model performance on the cross-entropy loss.The loss scales as a power-law with model size, dataset size, and the amount of computeused for training, with some trends spanning more than seven orders of magnitude. Otherarchitectural details such as network width or depth have minimal effects within a widerange. Simple equations govern the dependence of overﬁtting on model/dataset size and thedependence of training speed on model size. These relationships allow us to determine theoptimal allocation of a ﬁxed compute budget. Larger models are signiﬁcantly more sample-efﬁcient, such that optimally compute-efﬁcient training involves training very large modelson a relatively modest amount of data and stopping signiﬁcantly before convergence.∗Equal contribution.Contributions:Jared Kaplan and Sam McCandlish led the research.Tom Henighan contributed the LSTM ex-periments.Tom Brown, Rewon Child, and Scott Gray, and Alec Radford developed the optimized Transformerimplementation.
段落总结：Scaling Laws for Neural Language ModelsJared Kaplan ∗Johns Hopkins University, OpenAIjaredk@jhu

**********段落分割**********
Jeff Wu, Benjamin Chess, and Alec Radford developed the text datasets. Dario Amodei providedguidance throughout the project.arXiv:2001.08361v1  [cs.LG]  23 Jan 2020
段落总结：Jeff Wu, Benjamin Chess, and Alec Radford developed the text datasets

**********段落分割**********
Contents1Introduction22Background and Methods63Empirical Results and Basic Power Laws74Charting the Inﬁnite Data Limit and Overﬁtting105Scaling Laws with Model Size and Training Time126Optimal Allocation of the Compute Budget147Related Work188Discussion18Appendices20A Summary of Power Laws20BEmpirical Model of Compute-Efﬁcient Frontier20C Caveats22D Supplemental Figures231IntroductionLanguage provides a natural domain for the study of artiﬁcial intelligence, as the vast majority of reason-ing tasks can be efﬁciently expressed and evaluated in language, and the world’s text provides a wealth ofdata for unsupervised learning via generative modeling. Deep learning has recently seen rapid progress in lan-guage modeling, with state of the art models [RNSS18, DCLT18, YDY+19, LOG+19, RSR+19] approachinghuman-level performance on many speciﬁc tasks [WPN+19], including the composition of coherent multi-paragraph prompted text samples [RWC+19].One might expect language modeling performance to depend on model architecture, the size of neural models,the computing power used to train them, and the data available for this training process. In this work we willempirically investigate the dependence of language modeling loss on all of these factors, focusing on theTransformer architecture [VSP+17, LSP+18].
段落总结：Contents1Introduction22Background and Methods63Empirical Results and Basic Power Laws74Charting the 

**********段落分割**********
The high ceiling and low ﬂoor for performance on languagetasks allows us to study trends over more than seven orders of magnitude in scale.Throughout we will observe precise power-law scalings for performance as a function of training time, con-text length, dataset size, model size, and compute budget.1.1SummaryOur key ﬁndings for Transformer language models are are as follows:2Here we display predicted compute when using a sufﬁciently small batch size. See Figure 13 for comparison to thepurely empirical data.2
段落总结：The high ceiling and low ﬂoor for performance on languagetasks allows us to study trends over more t

**********段落分割**********
Dataset SizetokensParametersnon-embeddingComputePF-days, non-embeddingTest LossFigure 1Language modeling performance improves smoothly as we increase the model size, datasetsetsize, and amount of compute2 used for training. For optimal performance all three factors must be scaledup in tandem. Empirical performance has a power-law relationship with each individual factor when notbottlenecked by the other two.Performance depends strongly on scale, weakly on model shape:Model performance depends moststrongly on scale, which consists of three factors: the number of model parameters N (excluding embed-dings), the size of the dataset D, and the amount of compute C used for training. Within reasonable limits,performance depends very weakly on other architectural hyperparameters such as depth vs. width. (Section3)Smooth power laws:Performance has a power-law relationship with each of the three scale factorsN, D, C when not bottlenecked by the other two, with trends spanning more than six orders of magnitude(see Figure 1). We observe no signs of deviation from these trends on the upper end, though performancemust ﬂatten out eventually before reaching zero loss. (Section 3)Universality of overﬁtting:Performance improves predictably as long as we scale up N and D in tandem,but enters a regime of diminishing returns if either N or D is held ﬁxed while the other increases.
段落总结：Dataset SizetokensParametersnon-embeddingComputePF-days, non-embeddingTest LossFigure 1Language mode

**********段落分割**********
Theperformance penalty depends predictably on the ratio N 0.74/D, meaning that every time we increase themodel size 8x, we only need to increase the data by roughly 5x to avoid a penalty. (Section 4)Universality of training:Training curves follow predictable power-laws whose parameters are roughlyindependent of the model size. By extrapolating the early part of a training curve, we can roughly predict theloss that would be achieved if we trained for much longer. (Section 5)Transfer improves with test performance:When we evaluate models on text with a different distributionthan they were trained on, the results are strongly correlated to those on the training validation set witha roughly constant offset in the loss – in other words, transfer to a different distribution incurs a constantpenalty but otherwise improves roughly in line with performance on the training set. (Section 3.2.2)Sample efﬁciency:Large models are more sample-efﬁcient than small models, reaching the same level ofperformance with fewer optimization steps (Figure 2) and using fewer data points (Figure 4).Convergence is inefﬁcient:When working within a ﬁxed compute budget C but without any other restric-tions on the model size N or available data D, we attain optimal performance by training very large modelsand stopping signiﬁcantly short of convergence (see Figure 3).
段落总结：Theperformance penalty depends predictably on the ratio N 0

**********段落分割**********
Maximally compute-efﬁcient training wouldtherefore be far more sample efﬁcient than one might expect based on training small models to convergence,with data requirements growing very slowly as D ∼C0.27 with training compute. (Section 6)Optimal batch size:The ideal batch size for training these models is roughly a power of the loss only,and continues to be determinable by measuring the gradient noise scale [MKAT18]; it is roughly 1-2 milliontokens at convergence for the largest models we can train. (Section 5.1)Taken together, these results show that language modeling performance improves smoothly and predictablyas we appropriately scale up model size, data, and compute. We expect that larger language models willperform better and be more sample efﬁcient than current models.3
段落总结：Maximally compute-efﬁcient training wouldtherefore be far more sample efﬁcient than one might expect

**********段落分割**********
Larger models require fewer samplesto reach the same performance10864The optimal model size grows smoothlywith the loss target and compute budgetLine color indicatesnumber of parameters1071091011Tokens ProcessedCompute (PF-days)10-910-610-3100Test LossCompute-eﬃcienttraining stops farshort of convergence103109106103 Params109 Params10864Figure 2We show a series of language model training runs, with models ranging in size from 103 to 109parameters (excluding embeddings).100x Batch Size<10x Serial Steps>1,000,000x Model SizeData requirementsgrow relatively slowlyOptimal model sizeincreases very quicklyMinimum serial stepsincreases negligiblyFigure 3As more compute becomes available, we can choose how much to allocate towards training largermodels, using larger batches, and training for more steps. We illustrate this for a billion-fold increase incompute. For optimally compute-efﬁcient training, most of the increase should go towards increased modelsize. A relatively small increase in data is needed to avoid reuse. Of the increase in data, most can be used toincrease parallelism through larger batch sizes, with only a very small increase in serial training time required.1.2Summary of Scaling LawsThe test loss of a Transformer trained to autoregressively model language can be predicted using a power-lawwhen performance is limited by only either the number of non-embedding parameters N, the dataset size D,or the optimally allocated compute budget Cmin (see Figure 1):1.
段落总结：Larger models require fewer samplesto reach the same performance10864The optimal model size grows sm

**********段落分割**********
For models with a limited number of parameters, trained to convergence on sufﬁciently largedatasets:L(N) = (Nc/N)αN ; αN ∼0.076,Nc ∼8.8 × 1013 (non-embedding parameters)(1.1)2. For large models trained with a limited dataset with early stopping:L(D) = (Dc/D)αD ; αD ∼0.095,Dc ∼5.4 × 1013 (tokens)(1.2)3. When training with a limited amount of compute, a sufﬁciently large dataset, an optimally-sizedmodel, and a sufﬁciently small batch size (making optimal3 use of compute):L(Cmin) = Cminc/CminαminC; αminC∼0.050,Cminc∼3.1 × 108 (PF-days)(1.3)3We also observe an empirical power-law trend with the training compute C (Figure 1) while training at ﬁxed batchsize, but it is the trend with Cmin that should be used to make predictions. They are related by equation (5.5).4
段落总结：For models with a limited number of parameters, trained to convergence on sufﬁciently largedatasets:

**********段落分割**********
1071081091010Tokens in Dataset2.53.03.54.04.5LossLoss vs Model and Dataset SizeParams708M302M85M3M25M
段落总结：1071081091010Tokens in Dataset2

**********段落分割**********
393.2K104105Estimated Smin2.42.83.23.64.04.4LossLoss vs Model Size and Training Steps106107108Parameters (non-embed)Figure 4Left: The early-stopped test loss L(N, D) varies predictably with the dataset size D and modelsize N according to Equation (1.5). Right: After an initial transient period, learning curves for all modelsizes N can be ﬁt with Equation (1.6), which is parameterized in terms of Smin, the number of steps whentraining at large batch size (details in Section 5.1).These relations hold across eight orders of magnitude in Cmin, six orders of magnitude in N, and over twoorders of magnitude in D. They depend very weakly on model shape and other Transformer hyperparameters(depth, width, number of self-attention heads), with speciﬁc numerical values associated with the Webtext2training set [RWC+19]. The power laws αN, αD, αminCspecify the degree of performance improvementexpected as we scale up N, D, or Cmin; for example, doubling the number of parameters yields a loss thatis smaller by a factor 2−αN = 0.95.
段落总结：393.2K104105Estimated Smin2.42.83.23.64.04.4LossLoss vs Model Size and Training Steps106107108Parame

**********段落分割**********
The precise numerical values of Nc, Cminc, and Dc depend on thevocabulary size and tokenization and hence do not have a fundamental meaning.The critical batch size, which determines the speed/efﬁciency tradeoff for data parallelism ([MKAT18]), alsoroughly obeys a power law in L:Bcrit (L) =B∗L1/αB ,B∗∼2 · 108 tokens, αB ∼0.21(1.4)Equation (1.1) and (1.2) together suggest that as we increase the model size, we should increase the datasetsize sublinearly according to D ∝NαNαD ∼N 0.74. In fact, we ﬁnd that there is a single equation combining(1.1) and (1.2) that governs the simultaneous dependence on N and D and governs the degree of overﬁtting:
段落总结：The precise numerical values of Nc, Cminc, and Dc depend on thevocabulary size and tokenization and 

**********段落分割**********
L(N, D) ="NcN αNαD + DcD
段落总结：L(N, D) ="NcN αNαD + DcD

**********段落分割**********
#αD(1.5)with ﬁts pictured on the left in ﬁgure 4. We conjecture that this functional form may also parameterize thetrained log-likelihood for other generative modeling tasks.When training a given model for a ﬁnite number of parameter update steps S in the inﬁnite data limit, afteran initial transient period, the learning curves can be accurately ﬁt by (see the right of ﬁgure 4)
段落总结：#αD(1.5)with ﬁts pictured on the left in ﬁgure 4. We conjecture that this functional form may also p

**********段落分割**********
L(N, S) =NcNαN+ScSmin(S)αS(1.6)where Sc ≈2.1 × 103 and αS ≈0.76, and Smin(S) is the minimum possible number of optimization steps(parameter updates) estimated using Equation (5.4).When training within a ﬁxed compute budget C, but with no other constraints, Equation (1.6) leads to theprediction that the optimal model size N, optimal batch size B, optimal number of steps S, and dataset sizeD should grow asN ∝CαminC/αN ,B ∝CαminC/αB,S ∝CαminC/αS,
段落总结：L(N, S) =NcNαN+ScSmin(S)αS(1

**********段落分割**********
D = B · S(1.7)withαminC= 1/ (1/αS + 1/αB + 1/αN)(1.8)which closely matches the empirically optimal results N ∝C0.73min , B ∝C0.24min , and S ∝C0.03min . As thecomputational budget C increases, it should be spent primarily on larger models, without dramatic increasesin training time or dataset size (see Figure 3). This also implies that as models grow larger, they becomeincreasingly sample efﬁcient. In practice, researchers typically train smaller models for longer than would5
段落总结：D = B · S(1.7)withαminC= 1/ (1/αS + 1/αB + 1/αN)(1.8)which closely matches the empirically optimal r

**********段落分割**********
[D = B · S]be maximally compute-efﬁcient because of hardware constraints. Optimal performance depends on totalcompute as a power law (see Equation (1.3)).We provide some basic theoretical motivation for Equation (1.5), an analysis of learning curve ﬁts and theirimplications for training time, and a breakdown of our results per token. We also make some brief compar-isons to LSTMs and recurrent Transformers [DGV+18].1.3NotationWe use the following notation:• L – the cross entropy loss in nats. Typically it will be averaged over the tokens in a context, but insome cases we report the loss for speciﬁc tokens within the context.• N – the number of model parameters, excluding all vocabulary and positional embeddings• C ≈6NBS – an estimate of the total non-embedding training compute, where B is the batch size,and S is the number of training steps (ie parameter updates). We quote numerical values in PF-days,where one PF-day = 1015 × 24 × 3600 = 8.64 × 1019 ﬂoating point operations.• D – the dataset size in tokens• Bcrit – the critical batch size [MKAT18], deﬁned and discussed in Section 5.1. Training at thecritical batch size provides a roughly optimal compromise between time and compute efﬁciency.• Cmin – an estimate of the minimum amount of non-embedding compute to reach a given value ofthe loss.
段落总结：[D = B · S]be maximally compute-efﬁcient because of hardware constraints

**********段落分割**********
This is the training compute that would be used if the model were trained at a batch sizemuch less than the critical batch size.• Smin – an estimate of the minimal number of training steps needed to reach a given value of the loss.This is also the number of training steps that would be used if the model were trained at a batch sizemuch greater than the critical batch size.• αX – power-law exponents for the scaling of the loss as L(X) ∝1/XαX where X can be any ofN, D, C, S, B, Cmin.2Background and MethodsWe train language models on WebText2, an extended version of the WebText [RWC+19] dataset, tokenizedusing byte-pair encoding [SHB15] with a vocabulary size nvocab = 50257. We optimize the autoregres-sive log-likelihood (i.e. cross-entropy loss) averaged over a 1024-token context, which is also our principalperformance metric. We record the loss on the WebText2 test distribution and on a selection of other textdistributions. We primarily train decoder-only [LSP+18, RNSS18] Transformer [VSP+17] models, thoughwe also train LSTM models and Universal Transformers [DGV+18] for comparison.2.1Parameter and Compute Scaling of TransformersWe parameterize the Transformer architecture using hyperparameters nlayer (number of layers), dmodel (di-mension of the residual stream), dﬀ(dimension of the intermediate feed-forward layer), dattn (dimension ofthe attention output), and nheads (number of attention heads per layer).
段落总结：This is the training compute that would be used if the model were trained at a batch sizemuch less t

**********段落分割**********
We include nctx tokens in the inputcontext, with nctx = 1024 except where otherwise noted.We use N to denote the model size, which we deﬁne as the number of non-embedding parametersN ≈2dmodelnlayer (2dattn + dﬀ)= 12nlayerd2modelwith the standarddattn = dﬀ/4 = dmodel(2.1)where we have excluded biases and other sub-leading terms. Our models also have nvocabdmodel parametersin an embedding matrix, and use nctxdmodel parameters for positional embeddings, but we do not includethese when discussing the ‘model size’ N; we will see that this produces signiﬁcantly cleaner scaling laws.Evaluating a forward pass of the Transformer involves roughlyCforward ≈2N + 2nlayernctxdmodel(2.2)add-multiply operations, where the factor of two comes from the multiply-accumulate operation used inmatrix multiplication. A more detailed per-operation parameter and compute count is included in Table 1.6
段落总结：We include nctx tokens in the inputcontext, with nctx = 1024 except where otherwise noted

**********段落分割**********
OperationParametersFLOPs per TokenEmbed(nvocab + nctx) dmodel4dmodelAttention: QKVnlayerdmodel3dattn2nlayerdmodel3dattnAttention: Mask—2nlayernctxdattnAttention: Projectnlayerdattndmodel2nlayerdattndembdFeedforwardnlayer2dmodeldﬀ2nlayer2dmodeldﬀDe-embed—2dmodelnvocabTotal (Non-Embedding)N = 2dmodelnlayer (2dattn + dﬀ)Cforward = 2N + 2nlayernctxdattnTable 1Parameter counts and compute (forward pass) estimates for a Transformer model. Sub-leadingterms such as nonlinearities, biases, and layer normalization are omitted.For contexts and models with dmodel > nctx/12, the context-dependent computational cost per token is arelatively small fraction of the total compute. Since we primarily study models where dmodel ≫nctx/12,we do not include context-dependent terms in our training compute estimate. Accounting for the backwardspass (approximately twice the compute as the forwards pass), we then deﬁne the estimated non-embeddingcompute as C ≈6N ﬂoating point operators per training token.2.2Training ProceduresUnless otherwise noted, we train models with the Adam optimizer [KB14] for a ﬁxed 2.5 × 105 steps witha batch size of 512 sequences of 1024 tokens. Due to memory constraints, our largest models (more than1B parameters) were trained with Adafactor [SS18]. We experimented with a variety of learning rates andschedules, as discussed in Appendix D.6. We found that results at convergence were largely independent oflearning rate schedule.
段落总结：OperationParametersFLOPs per TokenEmbed(nvocab + nctx) dmodel4dmodelAttention: QKVnlayerdmodel3dattn

**********段落分割**********
Unless otherwise noted, all training runs included in our data used a learning rateschedule with a 3000 step linear warmup followed by a cosine decay to zero.2.3DatasetsWe train our models on an extended version of the WebText dataset described in [RWC+19]. The originalWebText dataset was a web scrape of outbound links from Reddit through December 2017 which received atleast 3 karma. In the second version, WebText2, we added outbound Reddit links from the period of Januaryto October 2018, also with a minimum of 3 karma. The karma threshold served as a heuristic for whetherpeople found the link interesting or useful. The text of the new links was extracted with the Newspaper3kpython library. In total, the dataset consists of 20.3M documents containing 96 GB of text and 1.62 × 1010words (as deﬁned by wc). We then apply the reversible tokenizer described in [RWC+19], which yields2.29 × 1010 tokens.
段落总结：Unless otherwise noted, all training runs included in our data used a learning rateschedule with a 3

**********段落分割**********
We reserve 6.6 × 108 of these tokens for use as a test set, and we also test on similarly-prepared samples of Books Corpus [ZKZ+15], Common Crawl [Fou], English Wikipedia, and a collectionof publicly-available Internet Books.3Empirical Results and Basic Power LawsTo characterize language model scaling we train a wide variety of models, varying a number of factorsincluding:• Model size (ranging in size from 768 to 1.5 billion non-embedding parameters)• Dataset size (ranging from 22 million to 23 billion tokens)• Shape (including depth, width, attention heads, and feed-forward dimension)• Context length (1024 for most runs, though we also experiment with shorter contexts)• Batch size (219 for most runs, but we also vary it to measure the critical batch size)7
段落总结：We reserve 6.6 × 108 of these tokens for use as a test set, and we also test on similarly-prepared s

**********段落分割**********
Feed-Forward Ratio (dff / dmodel)50M ParametersAspect Ratio (dmodel / nlayer)Attention Head Dimension (dmodel / nhead)25M Parameters10%8%6%4%2%0%Loss IncreaseA wide range of architecturesachieve similar performance22% additional computecompensates for 1% loss increaseFigure 5Performance depends very mildly on model shape when the total number of non-embeddingparameters N is held ﬁxed. The loss varies only a few percent over a wide range of shapes. Small differencesin parameter counts are compensated for by using the ﬁt to L(N) as a baseline. Aspect ratio in particular canvary by a factor of 40 while only slightly impacting performance; an (nlayer, dmodel) = (6, 4288) reaches aloss within 3% of the (48, 1600) model used in [RWC+19].106107108109Parameters (with embedding)234567Test Loss0 Layer1 Layer2 Layers3 Layers6 Layers> 6 Layers103104105106107108109Parameters (non-embedding)234567Test Loss1 Layer2 Layers3 Layers6 Layers> 6 LayersFigure 6Left: When we include embedding parameters, performance appears to depend strongly on thenumber of layers in addition to the number of parameters. Right: When we exclude embedding parameters,the performance of models with different depths converge to a single trend.
段落总结：Feed-Forward Ratio (dff / dmodel)50M ParametersAspect Ratio (dmodel / nlayer)Attention Head Dimensio

**********段落分割**********
Only models with fewer than 2layers or with extreme depth-to-width ratios deviate signiﬁcantly from the trend.In this section we will display data along with empirically-motivated ﬁts, deferring theoretical analysis tolater sections.3.1Approximate Transformer Shape and Hyperparameter IndependenceTransformer performance depends very weakly on the shape parameters nlayer, nheads, and dﬀwhen we holdthe total non-embedding parameter count N ﬁxed. To establish these results we trained models with ﬁxedsize while varying a single hyperparameter. This was simplest for the case of nheads. When varying nlayer,we simultaneously varied dmodel while keeping N ≈12nlayerd2model ﬁxed. Similarly, to vary dﬀat ﬁxedmodel size we also simultaneously varied the dmodel parameter, as required by the parameter counts in Table1. Independence of nlayers would follow if deeper Transformers effectively behave as ensembles of shallowermodels, as has been suggested for ResNets [VWB16]. The results are shown in Figure 5.3.2Performance with Non-Embedding Parameter Count NIn Figure 6 we display the performance of a wide variety of models, ranging from small models with shape(nlayer, dmodel) = (2, 128) through billion-parameter models, ranging in shape from (6, 4288) through(207, 768).
段落总结：Only models with fewer than 2layers or with extreme depth-to-width ratios deviate signiﬁcantly from 

**********段落分割**********
Here we have trained to near convergence on the full WebText2 dataset and observe no over-ﬁtting (except possibly for the very largest models).As shown in Figure 1, we ﬁnd a steady trend with non-embedding parameter count N, which can be ﬁt to theﬁrst term of Equation (1.5), so that
段落总结：Here we have trained to near convergence on the full WebText2 dataset and observe no over-ﬁtting (ex

**********段落分割**********
[L(N) ≈]LSTM plateaus after <100 tokensTransformer improves through the whole context2M200M3M300M54326Token Index in Context103102101Transformers asymptotically outperform LSTMsdue to improved use of long contexts3.64.23.02.44.85.4105108106107109Parameters (non-embedding)TransformersLSTMs1 Layer2 Layers4 LayersTest LossPer-tokenTest LossParameters:400K400KFigure 7To observe these trends it is crucial to study performance as a function of N; if we instead use the totalparameter count (including the embedding parameters) the trend is somewhat obscured (see Figure 6). Thissuggests that the embedding matrix can be made smaller without impacting performance, as has been seen inrecent work [LCG+19].Although these models have been trained on the WebText2 dataset, their test loss on a variety of other datasetsis also a power-law in N with nearly identical power, as shown in Figure 8.3.2.1Comparing to LSTMs and Universal TransformersIn Figure 7 we compare LSTM and Transformer performance as a function of non-embedding parametercount N. The LSTMs were trained with the same dataset and context length. We see from these ﬁguresthat the LSTMs perform as well as Transformers for tokens appearing early in the context, but cannot matchthe Transformer performance for later tokens.
段落总结：[L(N) ≈]LSTM plateaus after <100 tokensTransformer improves through the whole context2M200M3M300M543

**********段落分割**********
We present power-law relationships between performance andcontext position Appendix D.5, where increasingly large powers for larger models suggest improved abilityto quickly recognize patterns.We also compare the performance of standard Transformers to recurrent Transformers [DGV+18] in Figure17 in the appendix. These models re-use parameters, and so perform slightly better as a function of N, at thecost of additional compute per-parameter.3.2.2Generalization Among Data DistributionsWe have also tested our models on a set of additional text data distributions. The test loss on these datasetsas a function of model size is shown in Figure 8; in all cases the models were trained only on the WebText2dataset. We see that the loss on these other data distributions improves smoothly with model size, in directparallel with the improvement on WebText2. We ﬁnd that generalization depends almost exclusively on thein-distribution validation loss, and does not depend on the duration of training or proximity to convergence.We also observe no dependence on model depth (see Appendix D.8).3.3Performance with Dataset Size and ComputeWe display empirical trends for the test loss as a function of dataset size D (in tokens) and training computeC in Figure 1.For the trend with D we trained a model with (nlayer, nembd) = (36, 1280) on ﬁxed subsets of the WebText2dataset. We stopped training once the test loss ceased to decrease. We see that the resulting test losses can beﬁt with simple power-law
段落总结：We present power-law relationships between performance andcontext position Appendix D

**********段落分割**********
L(D) ≈DcDαD(3.2)in the dataset size. The data and ﬁt appear in Figure 1.The total amount of non-embedding compute used during training can be estimated as C = 6NBS, whereB is the batch size, S is the number of parameter updates, and the factor of 6 accounts for the forward andbackward passes. Thus for a given value of C we can scan over all models with various N to ﬁnd the model9
段落总结：L(D) ≈DcDαD(3.2)in the dataset size. The data and ﬁt appear in Figure 1.The total amount of non-em

**********段落分割**********
[L(D) ≈]104105106107108109Parameters (non-embedding)34567Test LossWebText2 (Test)Internet BooksBooksWikipediaCommon Crawl2.53.03.54.04.55.0Test Loss on Training Distribution2.53.03.54.04.55.0Loss on Other DistributionBooks during trainingWikipedia during trainingBooks at convergenceWikipedia at convergenceFigure 8Left: Generalization performance to other data distributions improves smoothly with model size,with only a small and very slowly growing offset from the WebText2 training distribution. Right: Gener-alization performance depends only on training distribution performance, and not on the phase of training.We compare generalization of converged models (points) to that of a single large model (dashed curves) as ittrains.with the best performance on step S =C6BS . Note that in these results the batch size B remains ﬁxed forall models, which means that these empirical results are not truly optimal. We will account for this in latersections using an adjusted Cmin to produce cleaner trends.The result appears as the heavy black line on the left-hand plot in Figure 1. It can be ﬁt with
段落总结：[L(D) ≈]104105106107108109Parameters (non-embedding)34567Test LossWebText2 (Test)Internet BooksBooks

**********段落分割**********
L(C) ≈CcCαC(3.3)The ﬁgure also includes images of individual learning curves to clarify when individual models are optimal.We will study the optimal allocation of compute more closely later on. The data strongly suggests that sampleefﬁciency improves with model size, and we also illustrate this directly in Figure 19 in the appendix.4Charting the Inﬁnite Data Limit and OverﬁttingIn Section 3 we found a number of basic scaling laws for language modeling performance. Here we willstudy the performance of a model of size N trained on a dataset with D tokens while varying N and Dsimultaneously. We will empirically demonstrate that the optimally trained test loss accords with the scalinglaw of Equation (1.5). This provides guidance on how much data we would need to train models of increasingsize while keeping overﬁtting under control.4.1Proposed L(N, D) EquationWe have chosen the parameterization (1.5) (repeated here for convenience):
段落总结：L(C) ≈CcCαC(3.3)The ﬁgure also includes images of individual learning curves to clarify when indiv

**********段落分割**********
L(N, D) ="NcN αNαD + DcD
段落总结：L(N, D) ="NcN αNαD + DcD

**********段落分割**********
#αD(4.1)using three principles:1. Changes in vocabulary size or tokenization are expected to rescale the loss by an overall factor. Theparameterization of L(N, D) (and all models of the loss) must naturally allow for such a rescaling.2. Fixing D and sending N →∞, the overall loss should approach L(D). Conversely, ﬁxing N andsending D →∞the loss must approach L(N).3. L(N, D) should be analytic at D = ∞, so that it has a series expansion in 1/D with integer powers.Theoretical support for this principle is signiﬁcantly weaker than for the ﬁrst two.Our choice of L(N, D) satisﬁes the ﬁrst requirement because we can rescale Nc, Dc with changes in thevocabulary. This also implies that the values of Nc, Dc have no fundamental meaning.10
段落总结：#αD(4.1)using three principles:1. Changes in vocabulary size or tokenization are expected to rescale

**********段落分割**********
[αD]106107108109Params (non-embed)2.53.03.54.04.5Test LossData Size BottleneckData Size21M43M86M172M344M688M1.4B22.0B104103102101NN/D/D0.00.10.20.30.40.5
段落总结：[αD]106107108109Params (non-embed)2

**********段落分割**********
L/L(D =)1OverfittingData Size21M43M86M172M344M688M1.4B22.0BFigure 9The early-stopped test loss L(N, D) depends predictably on the dataset size D and model size Naccording to Equation (1.5). Left: For large D, performance is a straight power law in N. For a smaller ﬁxedD, performance stops improving as N increases and the model begins to overﬁt. (The reverse is also true,see Figure 4.) Right: The extent of overﬁtting depends predominantly on the ratio NαNαD /D, as predicted inequation (4.3). The line is our ﬁt to that equation.Since we stop training early when the test loss ceases to improve and optimize all models in the same way, weexpect that larger models should always perform better than smaller models. But with ﬁxed ﬁnite D, we alsodo not expect any model to be capable of approaching the best possible loss (ie the entropy of text). Similarly,a model with ﬁxed size will be capacity-limited. These considerations motivate our second principle. Notethat knowledge of L(N) at inﬁnite D and L(D) at inﬁnite N fully determines all the parameters in L(N, D).The third principle is more speculative. There is a simple and general reason one might expect overﬁttingto scale ∝1/D at very large D. Overﬁtting should be related to the variance or the signal-to-noise ratioof the dataset [AS17], and this scales as 1/D. This expectation should hold for any smooth loss function,since we expect to be able to expand the loss about the D →∞limit.
段落总结：L/L(D =)1OverfittingData Size21M43M86M172M344M688M1

**********段落分割**********
However, this argument assumes that1/D corrections dominate over other sources of variance, such as the ﬁnite batch size and other limits on theefﬁcacy of optimization. Without empirical conﬁrmation, we would not be very conﬁdent of its applicability.Our third principle explains the asymmetry between the roles of N and D in Equation (1.5). Very similarsymmetric expressions4 are possible, but they would not have a 1/D expansion with integer powers, andwould require the introduction of an additional parameter.In any case, we will see that our equation for L(N, D) ﬁts the data well, which is the most important justiﬁ-cation for our L(N, D) ansatz.4.2ResultsWe regularize all our models with 10% dropout, and by tracking test loss and stopping once it is no longerdecreasing. The results are displayed in Figure 9, including a ﬁt to the four parameters αN, αD, Nc, Dc inEquation (1.5):ParameterαNαDNcDcValue0.0760.1036.4 × 10131.8 × 1013Table 2Fits to L(N, D)We obtain an excellent ﬁt, with the exception of the runs where the dataset has been reduced by a factor of1024, to about 2 × 107 tokens. With such a small dataset, an epoch consists of only 40 parameter updates.Perhaps such a tiny dataset represents a different regime for language modeling, as overﬁtting happens veryearly in training (see Figure 16).
段落总结：However, this argument assumes that1/D corrections dominate over other sources of variance, such as 

**********段落分割**********
Also note that the parameters differ very slightly from those obtained inSection 3, as here we are ﬁtting the full L(N, D) rather than just L(N, ∞) or L(∞, D).To chart the borderlands of the inﬁnite data limit, we can directly study the extent of overﬁtting. For all butthe largest models, we see no sign of overﬁtting when training with the full 22B token WebText2 dataset,so we can take it as representative of D = ∞. Thus we can compare ﬁnite D to the inﬁnite data limit by4For example, one might have used L(N, D) =  NcNαN +  DcDαDβ, but this does not have a 1/D expansion.11
段落总结：Also note that the parameters differ very slightly from those obtained inSection 3, as here we are ﬁ

**********段落分割**********
[L/L(D =]1013 × 1004 × 1006 × 100WebText2 Train Loss103104105106Critical Batch Size (Tokens)Critical Batch Size vs. PerformanceEmpirical Bcrit, N = 3MEmpirical Bcrit, N = 85MBcrit = 2.1 × 108 tokens L4.8Noise Scale MeasurementFigure 10The critical batch size Bcrit follows a power law in the loss as performance increase, and doesnot depend directly on the model size. We ﬁnd that the critical batch size approximately doubles for every13% decrease in loss. Bcrit is measured empirically from the data shown in Figure 18, but it is also roughlypredicted by the gradient noise scale, as in [MKAT18].deﬁningδL(N, D) ≡L(N, D)
段落总结：[L/L(D =]1013 × 1004 × 1006 × 100WebText2 Train Loss103104105106Critical Batch Size (Tokens)Critical

**********段落分割**********
L(N, ∞) −1(4.2)and studying it as a function of N, D. In fact, we see empirically that δL depends only a speciﬁc combinationof N and D, as shown in Figure 16. This follows from the scaling law of Equation (1.5), which impliesδL ≈
段落总结：L(N, ∞) −1(4.2)and studying it as a function of N, D. In fact, we see empirically that δL depends on

**********段落分割**********
[L(N, ∞) −1]1 + NNc αNαD DcD!αD−1(4.3)Note that at large D this formula also has a series expansion in powers of 1/D.We estimate that the variation in the loss with different random seeds is roughly 0.02, which means that toavoid overﬁtting when training to within that threshold of convergence we require
段落总结：[L(N, ∞) −1]1 + NNc αNαD DcD!αD−1(4

**********段落分割**********
D ≳(5 × 103) N 0.74(4.4)With this relation, models smaller than 109 parameters can be trained with minimal overﬁtting on the 22Btoken WebText2 dataset, but our largest models will encounter some mild overﬁtting. More generally, thisrelation shows that dataset size may grow sub-linearly in model size while avoiding overﬁtting. Note howeverthat this does not typically represent maximally compute-efﬁcient training. We should also emphasize thatwe have not optimized regularization (eg the dropout probability) while varying dataset and model size.5Scaling Laws with Model Size and Training TimeIn this section we will demonstrate that a simple scaling law provides a good description for the loss as afunction of model size N and training time. First we will explain how to use the results of [MKAT18] todeﬁne a universal training step Smin, which accounts for the fact that most of our models have not beentrained at an optimal batch size. Then we will demonstrate that we can ﬁt the model size and training timedependence of the loss using Equation (1.6). Later we will use these results to predict the optimal allocationof training compute between model size and training time, and then conﬁrm that prediction.5.1Adjustment for Training at Bcrit(L)A simple empirical theory for the batch size dependence of training was developed in [MKAT18] (see also[SLA+18, ZLN+19]).
段落总结：D ≳(5 × 103) N 0.74(4.4)With this relation, models smaller than 109 parameters can be trained with m

**********段落分割**********
It was argued that there is a critical batch size Bcrit for training; for B up to Bcritthe batch size can be increased with very minimal degradation in compute-efﬁciency, whereas for B > Bcritincreases in B result in diminishing returns. It was also argued that the gradient noise scale provides a simple12
段落总结：It was argued that there is a critical batch size Bcrit for training; for B up to Bcritthe batch siz

**********段落分割**********
[D ≳(5 × 103) N 0.74]prediction for Bcrit, and that neither depends directly on model size except through the value of the loss thathas been attained. These results can be used to predict how training time and compute will vary with thebatch size. To utilize both training time and compute as effectively as possible, it is best to train with a batchsize B ≈Bcrit. Training at B ≫Bcrit minimizes the number of training steps, while B ≪Bcrit minimizesthe use of compute.More speciﬁcally, it was demonstrated that for a wide variety of neural network tasks, the number of trainingsteps S and the number of data examples processed E = BS satisfy the simple relation SSmin−1  EEmin−1= 1(5.1)when training to any ﬁxed value of the loss L. Here Smin is the minimum number of steps necessary to reachL, while Emin is the minimum number of data examples that must be processed.We demonstrate the relation (5.1) for Transformers in Figure 18 in the appendix. This relation deﬁnes thecritical batch sizeBcrit(L) ≡EminSmin(5.2)which is a function of the target value of the loss. Training at the critical batch size makes a roughly optimaltime/compute tradeoff, requiring 2Smin training steps and processing E = 2Emin data examples.In Figure 10 we have plotted the critical batch size and gradient noise scale5 as a function of training loss fortwo different models. We see that Bcrit(L) is independent of model size, and only depends on the loss L.
段落总结：[D ≳(5 × 103) N 0.74]prediction for Bcrit, and that neither depends directly on model size except th

**********段落分割**********
Sothe predictions of [MKAT18] continue to hold for Transformer language models. The critical batch size canbe ﬁt with a power-law in the lossBcrit(L) ≈B∗L1/αB(5.3)where B∗≈2 × 108 and αB ≈0.21.We have chosen this parameterization for Bcrit(L) because as the loss approaches its minimum value Lmin,the gradient noise scale is expected to diverge, and we expect Bcrit to track this noise scale. We do notknow Lmin, as we see no sign that our models are approaching it, but Lmin > 0 since the entropy of naturallanguage is non-zero. Since apparently Lmin is much smaller than the values of L we have achieved, we useda parameterization where Bcrit diverges as L →0.We will use Bcrit(L) to estimate the relation between the number of training steps S while training at batchsize B = 219 tokens and the number of training steps while training at B ≫Bcrit. This is simplySmin(S) ≡S1 + Bcrit(L)/B(minimum steps, at B ≫Bcrit)(5.4)for any given target value L for the loss. This also deﬁnes a critical value of the compute needed to train to Lwith a model of size N if we were to train at B ≪Bcrit(L). This isCmin(C) ≡C1 + B/Bcrit(L)(minimum compute, at B ≪Bcrit)(5.5)where C = 6NBS estimates the (non-embedding) compute used at batch size B.5.2Results for L(N, Smin) and Performance with Model Size and ComputeNow we will use Smin deﬁned in Equation (5.4) to obtain a simple and universal ﬁt for the dependence of theloss on model size and training time in the inﬁnite data limit.
段落总结：Sothe predictions of [MKAT18] continue to hold for Transformer language models

**********段落分割**********
We will ﬁt the stable, Adam-optimized trainingruns using Equation (1.6), repeated here for convenience:L(N, Smin) =NcNαN+ ScSminαS(5.6)for the loss. We include all training steps after the warmup period of the learning rate schedule, and ﬁnd a ﬁtto the data with the parameters:5Although the critical batch size roughly matches the gradient noise scale, we are using a direct measurements ofBcrit from Figures 18 and 10 for all our later analyses.13
段落总结：We will ﬁt the stable, Adam-optimized trainingruns using Equation (1

**********段落分割**********
104106108Parameters (non-embedding)2345678Test LossPerformance vs Compute Budget105104103102101100PF-dayss106107108109Parameters (non-embedding)2.43.03.64.24.85.4Test LossPerformance vs Steps104105StepsFigure 11When we hold either total compute or number of training steps ﬁxed, performance followsL(N, S) from Equation (5.6). Each value of compute budget has an associated optimal model size thatmaximizes performance. Mediocre ﬁts at small S are unsurprising, as the power-law equation for the learningcurves breaks down very early in training.ParameterαNαSNcScValue0.0770.766.5 × 10132.1 × 103Table 3Fits to L(N, S)With these parameters, we obtain the learning curve ﬁts in Figure 4. Though the ﬁts are imperfect, we believethey are quite compelling given the simplicity of Equation (5.6).The data and ﬁts can be visualized in a different and more interesting way, as shown in Figure 11. There westudy the test loss as a function of model size while ﬁxing either the total non-embedding compute C usedin training, or the number of steps S. For the ﬁts we use Equation (5.5) and (5.4) along with the parametersabove and Equation (5.6).The power-law dependence of the loss on Smin reﬂects the interplay of optimizer dynamics and the losslandscape. Since the ﬁts are best late in training, when the loss may be approximately quadratic, the power-law should provide information about the spectrum of the Hessian of the loss.
段落总结：104106108Parameters (non-embedding)2345678Test LossPerformance vs Compute Budget105104103102101100PF

**********段落分割**********
Its universality suggests thatthe Hessian eigenvalue density is roughly independent of model size.5.3Lower Bound on Early Stopping StepThe results for L(N, Smin) can be used to derive a lower-bound (and rough estimate) of the step at whichearly stopping should occur when training is data limited. It is motivated by the idea that ﬁnite and inﬁnite Dlearning curves for a given model will be very similar until we reach Smin ≈Sstop. Thus overﬁtting shouldbe proportional to the correction from simply ending training at Sstop. This will underestimate Sstop, becausein reality the test loss will decrease more slowly when we have a ﬁnite D, and therefore we will require moretraining steps to reach the optimal test loss at ﬁnite D. This line of reasoning leads to the inequalitySstop(N, D) ≳Sc[L(N, D) −L(N, ∞)]1/αS(5.7)where L(N, ∞) is the converged loss, evaluated with inﬁnite available data. This inequality and its com-parison to the empirical data is displayed in Figure 16 in the appendix. In that ﬁgure, the values of Sstopand L(N, D) are empirical (though Sstop is adjusted to mimic training at B ≫Bcrit), while L(N, ∞) iscomputed from the ﬁt to L(N, D) evaluated at D = ∞.6Optimal Allocation of the Compute BudgetWe displayed the empirical trend of performance as a function of the computation used during training inthe top-right of Figure 1. However, this result involved training at a ﬁxed batch size B, whereas we know14
段落总结：Its universality suggests thatthe Hessian eigenvalue density is roughly independent of model size

**********段落分割**********
Models between 0.6x and 2.2x theoptimal size can be trained with a20% larger compute budgetSmaller models requiremore steps to train, whilelarger models require fewerOur framework does notcapture early training dynamicsFigure 12Left: Given a ﬁxed compute budget, a particular model size is optimal, though somewhat largeror smaller models can be trained with minimal additional compute. Right: Models larger than the compute-efﬁcient size require fewer steps to train, allowing for potentially faster training if sufﬁcient additional paral-lelism is possible. Note that this equation should not be trusted for very large models, as it is only valid in thepower-law region of the learning curve, after initial transient effects.108106104102100Compute (PF-days), non-embedding234567Test LossL = (Cmin/2.3 108)0.050
段落总结：Models between 0.6x and 2.2x theoptimal size can be trained with a20% larger compute budgetSmaller m

**********段落分割**********
L = (C/2.0 107)0.057Figure 13When adjusting performance to simulate training far below the critical batch size, we ﬁnd asomewhat altered power law for L(Cmin) when compared with the fully empirical results. The conspicuouslump at 10−5 PF-days marks the transition from 1-layer to 2-layer networks; we exclude 1-layer networksin the power-law ﬁts. It is the L(Cmin) trend that we expect to provide a reliable extrapolation for largercompute.that in fact we could train more efﬁciently6 by training at the batch size Bcrit discussed in Section 5.1.Large and small values of the loss could have been achieved with fewer samples or fewer steps, respectively,and correcting for this inefﬁciency by standardizing to the critical batch size results in cleaner and morepredictable trends.In this section we will adjust for this oversight. More importantly, we will use the results of Section 5to determine the optimal allocation of compute between model size N and the quantity of data processedduring training, namely 2BcritSmin. We will determine this allocation both empirically and theoretically, byusing the equation for L(N, Smin), and we will demonstrate that these methods agree.6.1Optimal Performance and AllocationsLet us ﬁrst study the loss as a function of the optimally allocated compute from Equation (5.5). The result isplotted in Figure 13, along with a power-law ﬁt.
段落总结：L = (C/2.0 107)0.057Figure 13When adjusting performance to simulate training far below the critical 

**********段落分割**********
We see that as compared to the compute plot of Figure 1, thenew ﬁt with Cmin is somewhat improved.Given L(Cmin), it is natural to ask for the optimal model size N(Cmin) that provides the minimal loss with agiven quantity of training compute. The optimal model size is shown in Figure 14. We observe that N(Cmin)6One might ask why we did not simply train at Bcrit in the ﬁrst place. The reason is that it depends not only on themodel but also on the target value of the loss we wish to achieve, and so is a moving target.15
段落总结：We see that as compared to the compute plot of Figure 1, thenew ﬁt with Cmin is somewhat improved

**********段落分割**********
[L = (C/2.0 107)]107105103101Compute (PF-days), non-embedding103105107Parameters (non-embedding)
段落总结：[L = (C/2.0 107)]107105103101Compute (PF-days), non-embedding103105107Parameters (non-embedding)

**********段落分割**********
N = (1.3 109) C0.73min
段落总结：N = (1.3 109) C0.73min

**********段落分割**********
N = (1.6 109) C0.88107105103101Compute (PF-days), excluding embeddings050001000015000StepsSmin (adjusted)Smin = (5.4 103) C0.03minS (fixed-batch)Figure 14Left: Each value of the compute budget Cmin has an associated optimal model size N. Optimalmodel size grows very rapidly with Cmin, increasing by 5x for each 10x increase in compute. The numberof data examples processed makes up the remainder of the increase, growing relatively modestly by only 2x.Right: The batch-adjusted number of optimization steps also grows very slowly, if at all, meaning that mostof the growth in data examples processed can be used for increased batch sizes.can be ﬁt very well with a power-lawN(Cmin) ∝(Cmin)0.73.(6.1)In Figure 12, we show the effect of training models of sub-optimal sizes (see Appendix B.4).By deﬁnition Cmin ≡6NBcritS, and so we can use N(Cmin) to extract further results. In particular, sinceprior ﬁts show B ∝L−4.8 and L ∝C−0.05min, we can conclude that Bcrit ∝C0.24min . This leads us to concludethat the optimal number of steps will only grow very slowly with compute, asSmin ∝(Cmin)0.03,(6.2)matching the empirical results in Figure 14.
段落总结：N = (1.6 109) C0.88107105103101Compute (PF-days), excluding embeddings050001000015000StepsSmin (adju

**********段落分割**********
In fact the measured exponent is sufﬁciently small that our resultsmay even be consistent with an exponent of zero.Thus we conclude that as we scale up language modeling with an optimal allocation of computation, weshould predominantly increase the model size N, while simultaneously scaling up the batch size via B ∝Bcrit with negligible increase in the number of serial steps. Since compute-efﬁcient training uses relativelyfew optimization steps, additional work on speeding up early training dynamics may be warranted.6.2Predictions from L(N, Smin)The results for L(Cmin) and the allocations can be predicted from the L(N, Smin) equation obtained inSection 5. Given our equation for L(N, Smin), we can substitute Smin = Cmin6NB and then ﬁnd the minimumof the loss as a function of N, while ﬁxing the training compute. We carry out this procedure in detail inAppendix B, where we also provide some additional predictions.For the loss as a function of training compute, we predict thatL(Cmin) =CmincCminαminC(6.3)whereαminC≡11/αS + 1/αB + 1/αN≈0.054(6.4)in excellent agreement with the exponent of Figure 13. We also predict thatN(Cmin) ∝(Cmin)αminC/αN ≈(Cmin)0.71(6.5)which also matches the scaling of Figure 14 to within a few percent. Our scaling laws provide a predictiveframework for the performance of language modeling.16
段落总结：In fact the measured exponent is sufﬁciently small that our resultsmay even be consistent with an ex

**********段落分割**********
[N = (1.6 109) C0.88]The intersection point is sensitive tothe precise power-law parametersFigure 15Far beyond the model sizes we study empirically, we ﬁnd a contradiction between our equationsfor L(Cmin) and L(D) due to the slow growth of data needed for compute-efﬁcient training. The intersectionmarks the point before which we expect our predictions to break down. The location of this point is highlysensitive to the precise exponents from our power-law ﬁts.6.3Contradictions and a ConjectureWe observe no signs of deviation from straight power-law trends at large values of compute, data, or modelsize. Our trends must eventually level off, though, since natural language has non-zero entropy.Indeed, the trends for compute-efﬁcient training described in this section already contain an apparent contra-diction. At scales several orders of magnitude above those documented here, the performance predicted bythe L(Cmin) scaling law decreases below what should be possible given the slow growth in training data withcompute.
段落总结：[N = (1.6 109) C0.88]The intersection point is sensitive tothe precise power-law parametersFigure 15

**********段落分割**********
This implies that our scaling laws must break down before this point, but we conjecture that theintersection point has a deeper meaning: it provides an estimate of the point at which Transformer languagemodels reach maximal performance.Since the amount of data used by compute-efﬁcient training grows slowly with the compute budget, theperformance predicted by L(Cmin) eventually hits a lower bound set by the L(D) power law (see Figure 15).Let us work this out in more detail.To keep overﬁtting under control, the results of Section 4 imply that we should scale the dataset size as
段落总结：This implies that our scaling laws must break down before this point, but we conjecture that theinte

**********段落分割**********
D ∝N 0.74 ∝C0.54min(6.6)where we have used the compute-efﬁcient N(Cmin) from Figure 14.Let us compare this to the data requirements of compute-efﬁcient training. If we train at the critical batchsize (i.e. C = 2Cmin) and never re-use data during training, we ﬁnd that data usage grows with compute asD(Cmin) =2Cmin6N(Cmin) ≈ 4 × 1010 tokens(Cmin/PF-Day)0.26(6.7)This is the maximum rate at which the dataset size can productively grow with compute, since it means thatwe are only training for a single epoch. But it grows the dataset much more slowly than in Equation (6.6).It appears to imply that compute-efﬁcient training will eventually run into a problem with overﬁtting, even ifthe training process never re-uses any data!According to Figure 1, we expect that when we are bottlenecked by the dataset size (ie by overﬁtting), theloss should scale as L(D) ∝D−0.095. This implies that the loss would scale with compute as L(D(Cmin)) ∝
段落总结：D ∝N 0.74 ∝C0.54min(6.6)where we have used the compute-efﬁcient N(Cmin) from Figure 14.Let us compar

**********段落分割**********
C−0.03minonce we are data-limited. Once again, we have a contradiction, as this will eventually intersect withour prediction for L(Cmin) from Figure 13, where we found a scaling L(Cmin) ∝C−0.050min.The intersection point of L(D(Cmin)) and L(Cmin) occurs atC∗∼104 PF-DaysN ∗∼1012 parameters,D∗∼1012 tokens,L∗∼1.7 nats/token(6.8)though the numerical values are highly uncertain, varying by an order or magnitude in either direction de-pending on the precise values of the exponents from the power-law ﬁts. The most obvious interpretation isthat our scaling laws break down at or before we reach this point, which is still many orders of magnitudeaway in both compute and model size.17
段落总结：C−0.03minonce we are data-limited. Once again, we have a contradiction, as this will eventually inte

**********段落分割**********
[C−0.03]One might also conjecture that this intersection point has a deeper meaning. If we cannot increase the modelsize beyond N ∗without qualitatively different data requirements, perhaps this means that once we reachC∗min and N ∗, we have extracted all of the reliable information available in natural language data. In thisinterpretation, L∗would provide a rough estimate for the entropy-per-token7 of natural language. In thisscenario, we would expect the loss trend to level off at or before L∗.We can guess at the functional form of L(Cmin) as it levels off by considering a version of our trainingdataset with added noise. For example, we could append a random string of tokens to each context shownto the model to artiﬁcially boost the loss by a constant additive factor. Then, the distance from the noiseﬂoor L −Lnoise would be a more meaningful performance metric, with even a small decrease in this distancepotentially representing a signiﬁcant boost in qualitative performance. Since the artiﬁcial noise would affectall of our trends equally, the critical point of 6.8 would not change (aside from the absolute value of L∗), andmay be meaningful even if it occurs after the leveling off.7Related WorkPower laws can arise from a wide variety of sources [THK18].
段落总结：[C−0.03]One might also conjecture that this intersection point has a deeper meaning. If we cannot in

**********段落分割**********
Power-law scalings with model and datasetsize in density estimation [Was06] and in random forest models [Bia12] may be connected with our results.These models suggest that power-law exponents may have a very rough interpretation as the inverse of thenumber of relevant features in the data.Some early [BB01, Goo01] work found power-law scalings between performance and dataset size. Morerecent work [HNA+17, HAD19] also investigated scaling between model size and data size; their work isperhaps the closest to ours in the literature8. Note, however, that [HNA+17] found super-linear scaling ofdataset size with model size, whereas we ﬁnd a sub-linear scaling. There are some parallels between ourﬁndings on optimal allocation of compute and [Kom19], including power-law learning curves. EfﬁcientNets[TL19] also appear to obey an approximate power-law relation between accuracy and model size. Very recentwork [RRBS19b] studies scaling with both dataset size and model size for a variety of datasets, and ﬁts anansatz similar to ours.EfﬁcientNet [TL19] advocates scaling depth and width exponentially (with different coefﬁcients) for optimalperformance of image models, resulting in a power-law scaling of width as a function of depth. We ﬁnd thatfor language models this power should be roughly one when scaling up (as width/depth should remain ﬁxed).But more importantly, we ﬁnd that the precise architectural hyperparameters are unimportant compared to theoverall scale of the language model.
段落总结：Power-law scalings with model and datasetsize in density estimation [Was06] and in random forest mod

**********段落分割**********
In [VWB16] it was argued that deep models can function as ensemblesof shallower models, which could potentially explain this ﬁnding. Earlier work [ZK16] has compared widthand depth, and found that wide ResNets can outperform deep ResNets on image classiﬁcation. Some studiesﬁx computation per data example, which tends to scale in proportion to the number of model parameters,whereas we investigate scaling with both model size and the quantity of training computation.Various works [AS17, BHMM18] have investigated generalization in highly overparameterized models, ﬁnd-ing a “jamming transition” [GJS+19] when the model size reaches the dataset size (this may require trainingmany orders of magnitude beyond typical practice, and in particular does not use early stopping). We donot observe such a transition, and ﬁnd that the necessary training data scales sublinearly in the model size.Expansions in the model size, particularly at large width [JGH18, LXS+19], may provide a useful frameworkfor thinking about some of our scaling relations. Our results on optimization, such as the shape of learningcurves, can likely be explained using a noisy quadratic model, which can provide quite accurate predictions[ZLN+19] in realistic settings.
段落总结：In [VWB16] it was argued that deep models can function as ensemblesof shallower models, which could 

**********段落分割**********
Making this connection quantitative will require a characterization of theHessian spectrum [Pap18, GKX19, GARD18].8DiscussionWe have observed consistent scalings of language model log-likelihood loss with non-embedding parametercount N, dataset size D, and optimized training computation Cmin, as encapsulated in Equations (1.5) and(1.6). Conversely, we ﬁnd very weak dependence on many architectural and optimization hyperparameters.Since scalings with N, D, Cmin are power-laws, there are diminishing returns with increasing scale.7Deﬁning words using the wc utility, the WebText2 dataset has 1.4 tokens per word and 4.3 characters per token.8After this work was completed, [RRBS19a] also appeared, which makes similar predictions for the dependence ofloss on both model and dataset size.18
段落总结：Making this connection quantitative will require a characterization of theHessian spectrum [Pap18, G

**********段落分割**********
We were able to precisely model the dependence of the loss on N and D, and alternatively on N and S, whenthese parameters are varied simultaneously. We used these relations to derive the compute scaling, magnitudeof overﬁtting, early stopping step, and data requirements when training large language models. So our scalingrelations go beyond mere observation to provide a predictive framework. One might interpret these relationsas analogues of the ideal gas law, which relates the macroscopic properties of a gas in a universal way,independent of most of the details of its microscopic consituents.It is natural to conjecture that the scaling relations will apply to other generative modeling tasks with amaximum likelihood loss, and perhaps in other settings as well. To this purpose, it will be interesting totest these relations on other domains, such as images, audio, and video models, and perhaps also for randomnetwork distillation. At this point we do not know which of our results depend on the structure of naturallanguage data, and which are universal. It would also be exciting to ﬁnd a theoretical framework fromwhich the scaling relations can be derived: a ‘statistical mechanics’ underlying the ‘thermodynamics’ wehave observed.
段落总结：We were able to precisely model the dependence of the loss on N and D, and alternatively on N and S,

**********段落分割**********
Such a theory might make it possible to derive other more precise predictions, and provide asystematic understanding of the limitations of the scaling laws.In the domain of natural language, it will be important to investigate whether continued improvement on theloss translates into improvement on relevant language tasks. Smooth quantitative change can mask majorqualitative improvements: “more is different”. For example, the smooth aggregate growth of the economyprovides no indication of the speciﬁc technological developments that underwrite it. Similarly, the smoothimprovements in language model loss may hide seemingly qualitative changes in capability.Our results strongly suggest that larger models will continue to perform better, and will also be much moresample efﬁcient than has been previously appreciated. Big models may be more important than big data.In this context, further investigation into model parallelism is warranted. Deep models can be trained usingpipelining [HCC+18], which splits parameters depth-wise between devices, but eventually requires increasedbatch sizes as more devices are used. Wide networks on the other hand are more amenable to parallelization[SCP+18], since large layers can be split between multiple workers with less serial dependency. Sparsity[CGRS19, GRK17] or branching (e.g. [KSH12]) may allow for even faster training of large networks throughincreased model parallelism.
段落总结：Such a theory might make it possible to derive other more precise predictions, and provide asystemat

**********段落分割**********
And using methods like [WRH17, WYL19], which grow networks as they train,it might be possible to remain on the compute-efﬁcient frontier for an entire training run.AcknowledgementsWe would like to thank Shan Carter, Paul Christiano, Jack Clark, Ajeya Cotra, Ethan Dyer, Jason Eisner,Danny Hernandez, Jacob Hilton, Brice Menard, Chris Olah, and Ilya Sutskever for discussions and for feed-back on drafts of this work.19
段落总结：And using methods like [WRH17, WYL19], which grow networks as they train,it might be possible to rem

**********段落分割**********
AppendicesASummary of Power LawsFor easier reference, we provide a summary below of the key trends described throughout the paper.ParametersDataComputeBatch SizeEquationN∞∞FixedL (N) = (Nc/N)αN∞DEarly StopFixedL (D) = (Dc/D)αDOptimal∞CFixedL (C) = (Cc/C)αC (naive)NoptDoptCminB ≪BcritL (Cmin) = Cminc/CminαminCNDEarly StopFixed
段落总结：AppendicesASummary of Power LawsFor easier reference, we provide a summary below of the key trends d

**********段落分割**********
L (N, D) =  NcN αNαD + DcDαDN∞S stepsB
段落总结：L (N, D) =  NcN αNαD + DcDαDN∞S stepsB

**********段落分割**********
L (N, S) =  NcNαN +ScSmin(S,B)αSTable 4The empirical ﬁtted values for these trends are:Power LawScale (tokenization-dependent)αN = 0.076Nc = 8.8 × 1013 params (non-embed)αD = 0.095Dc = 5.4 × 1013 tokensαC = 0.057Cc = 1.6 × 107 PF-daysαminC= 0.050Cminc= 3.1 × 108 PF-daysαB = 0.21B∗= 2.1 × 108 tokensαS = 0.76Sc = 2.1 × 103 stepsTable 5The optimal parameters for compute efﬁcient training are given by:Compute-Efﬁcient ValuePower LawScaleNopt = Ne · CpNminpN = 0.73Ne = 1.3 · 109 paramsB ≪Bcrit =B∗L1/αB = BeCpBminpB = 0.24Be = 2.0 · 106 tokensSmin = Se · CpSmin (lower bound)pS = 0.03Se = 5.4 · 103 stepsDopt = De · CpDmin (1 epoch)pD = 0.27De = 2 · 1010 tokensTable 6BEmpirical Model of Compute-Efﬁcient FrontierThroughout this appendix all values of C, S, and αC are adjusted for training at the critical batch size Bcrit.We have left off the ‘adj’ label to avoid cluttering the notation.B.1Deﬁning EquationsThe power-law ﬁt to the learning curves implies a simple prescription for compute-efﬁcient training. In thisappendix, we will derive the optimal performance, model size, and number of training steps as a function of20
段落总结：L (N, S) =  NcNαN +ScSmin(S,B)αSTable 4The empirical ﬁtted values for these trends are:Power LawS

**********段落分割**********
[L (N, S) =]the compute budget. We start with the Equation (1.6), repeated here for convenience:
段落总结：[L (N, S) =]the compute budget

**********段落分割**********
L (N, S) =NcNαN+ScSαS.(B.1)Here, S represents the number of parameter updates when training at the critical batch size [MKAT18],which was deﬁned in Equation (5.2)9:
段落总结：L (N, S) =NcNαN+ScSαS

**********段落分割**********
B (L) =B∗L1/αB .(B.2)We would like to determine optimal training parameters for a ﬁxed compute budget, so we replace S =C/ (6NB (L)), where C is the number of FLOPs used in the training run:
段落总结：B (L) =B∗L1/αB .(B.2)We would like to determine optimal training parameters for a ﬁxed compute budge

**********段落分割**********
L (N, C) =NcNαN+6B∗ScNL1/αBCαS.(B.3)Now, we set ∂NL
段落总结：L (N, C) =NcNαN+6B∗ScNL1/αBCαS

**********段落分割**********
[L (N, C) =]C = 0 to ﬁnd the condition for optimality:
段落总结：[L (N, C) =]C = 0 to ﬁnd the condition for optimality:

**********段落分割**********
[0 = ∂L]C= −αNNNcNαN+ αSN6B∗ScNL1/αBCαS 1 −5NL∂L∂N
段落总结：[0 = ∂L]C= −αNNNcNαN+ αSN6B∗ScNL1/αBCαS 1 −5NL∂L∂N

**********段落分割**********
C=⇒αNαSNcNαN=6B∗ScNL1/αBCαS(B.4)Equation (B.3) and (B.4) together determine the compute-efﬁcient frontier.B.2Efﬁcient TrainingNow we assemble the implications of (B.3) and (B.4). First, note that inserting (B.4) into (B.3) yieldsL (Neﬀ(C) , C) =1 + αNαSL (Neﬀ, ∞) ,(B.5)which implies that for compute-efﬁcient training, we should train to a ﬁxed percentage αNαS ≈10% abovethe converged loss. Next, let’s determine how the optimal loss depends on the compute budget. EliminatingN yields a power-law dependence of performance on compute:
段落总结：C=⇒αNαSNcNαN=6B∗ScNL1/αBCαS(B

**********段落分割**********
L (C) =CcCαC(B.6)where we deﬁnedαC = 1/ (1/αS + 1/αB + 1/αN) ≈0.052(B.7)Cc = 6NcB∗Sc1 + αNαS1/αS+1/αN  αSαN1/αS.(B.8)Similarly, we can eliminate L to ﬁnd N (C):N (C)Nc= CCcαC/αN 1 + αNαS1/αN(B.9)and
段落总结：L (C) =CcCαC(B.6)where we deﬁnedαC = 1/ (1/αS + 1/αB + 1/αN) ≈0.052(B.7)Cc = 6NcB∗Sc1 + αNαS1/αS

**********段落分割**********
S (C) =Cc6NcB∗1 + αNαS−1/αN  CCcαC/αS
段落总结：S (C) =Cc6NcB∗1 + αNαS−1/αN  CCcαC/αS

**********段落分割**********
(B.10)9There is a slight ambiguity here: we can imagine training either at a constant batch size B (Ltarget), or we couldinstead train at a variable batch size ˜B (L), where ˜B is the instantaneous critical batch size (as opposed to B, which isthe averaged version). These two prescriptions result in the same number of steps, so we can ignore this subtlety (see
段落总结：(B.10)9There is a slight ambiguity here: we can imagine training either at a constant batch size B (

**********段落分割**********
[[MKAT18]).]B.3Comparison to InefﬁcientTypically, researchers train models until they appear to be close to convergence. In this section, we comparethe efﬁcient training procedure described above to this more typical setup. We deﬁne a the convergence factorf as the percent deviation from the converged loss:L (N, C) = (1 + f) L (N, ∞) .
段落总结：[[MKAT18]).]B.3Comparison to InefﬁcientTypically, researchers train models until they appear to be c

**********段落分割**********
(B.11)For compute-efﬁcient training we have f = αN/αS ≈10% from the previous section, but researcherstypically use a much smaller value. Here, we choose f ′ = 2% as an estimate. For a ﬁxed value of the loss,we predict:NfNf ′ = 1 + f1 + f ′1/αN≈2.7
段落总结：(B.11)For compute-efﬁcient training we have f = αN/αS ≈10% from the previous section, but researcher

**********段落分割**********
[(B.12)]1 + 1f1 + 1f ′!1/αS≈0.13
段落总结：[(B.12)]1 + 1f1 + 1f ′!1/αS≈0.13

**********段落分割**********
(B.13)CfCf ′ = NfNf ′SfSf ′ ≈0.35
段落总结：(B.13)CfCf ′ = NfNf ′SfSf ′ ≈0.35

**********段落分割**********
(B.14)So that compute-efﬁcient training uses 7.7x fewer parameter updates, 2.7x more parameters, and 65% lesscompute to reach the same loss.B.4Suboptimal Model SizesWe can solve A.1 to ﬁnd an expression for the amount of compute needed to reach a given value of the lossL with a model of size N:
段落总结：(B.14)So that compute-efﬁcient training uses 7.7x fewer parameter updates, 2.7x more parameters, and

**********段落分割**********
C (N, L) =6B∗ScNL1/αB L −NcNαN −1/αS.
段落总结：C (N, L) =6B∗ScNL1/αB L −NcNαN −1/αS

**********段落分割**********
(B.15)Using A.6 and A.9, we can eliminate L in favor of Neﬀ(L), the model size which reaches L most efﬁciently.From there, we ﬁnd an expression for the excess compute needed as a consequence of using a suboptimalmodel size:C (N, Neﬀ)C (Neﬀ, Neﬀ) =NNeﬀ1 + αSαN1 −NeﬀNαN −1/αS.
段落总结：(B.15)Using A.6 and A.9, we can eliminate L in favor of Neﬀ(L), the model size which reaches L most 

**********段落分割**********
(B.16)The result is shown in Figure X. Models between 0.6x and 2.2x the optimal size can be used with only a20% increase in compute budget. Using a smaller model is useful when accounting for the cost inference. Alarger model can be trained the the same level of performance in fewer steps, allowing for more parallelismand faster training if sufﬁcient harware is available (see Figure Y):S (N, Neﬀ)S (Neﬀ, Neﬀ) =1 + αSαN1 −NeﬀNαN −1/αS.
段落总结：(B.16)The result is shown in Figure X. Models between 0.6x and 2.2x the optimal size can be used wit

**********段落分割**********
(B.17)A 2.2x larger model requires 45% fewer steps at a cost of 20% more training compute. Note that this equationshould not be trusted for very large models, as it is only valid in the power-law region of the learning curveafter initial transient effects.CCaveatsIn this section we list some potential caveats to our analysis.• At present we do not have a solid theoretical understanding for any of our proposed scaling laws.The scaling relations with model size and compute are especially mysterious. It may be possible tounderstand scaling at very large D holding model size ﬁxed [AS17], and also the shape of learningcurves late in training, by modeling the loss with a noisy quadratic. But the scaling with D at verylarge model size still remains mysterious. Without a theory or a systematic understanding of thecorrections to our scaling laws, it’s difﬁcult to determine in what circumstances they can be trusted.22
段落总结：(B.17)A 2.2x larger model requires 45% fewer steps at a cost of 20% more training compute. Note that

**********段落分割**********
[(B.17)]103104105Sc × [L(N, D)L(N,)]1/S103104105SstopEarly Stopping StepData Size21M43M86M172M344M688M1.4B103104105Step23456LossTest LossTrain Loss1081091010Dataset Size (Tokens)Figure 16Left: We characterize the step on which early stopping occurs, as a function of the extent ofoverﬁtting. The red line indicates a lower bound for early stopping that is derived in Section 5.3. Right:We display train and test loss for a series of 300M parameter models trained on different sized dataset sub-samples. The test loss typically follows that of a run done with unrestricted data until diverging. Note that thedegree of overﬁtting (as compared to the inﬁnite data limit) is signiﬁcantly overestimated by Ltest −Ltrain(denoted by a black bar for each run).• We are not especially conﬁdent in the prediction of Bcrit(L) for values of the loss far outside therange we have explored. Changes in Bcrit could have a signiﬁcant impact on trade-offs betweendata parallelism and the number of serial training steps required, which would have a major impacton training time.• We did not thoroughly investigate the small data regime, and our ﬁts for L(N, D) were poor forthe smallest values of D (where an epoch corresponded to only 40 steps). Furthermore, we didnot experiment with regularization and data augmentation.
段落总结：[(B.17)]103104105Sc × [L(N, D)L(N,)]1/S103104105SstopEarly Stopping StepData Size21M43M86M172M344M68

**********段落分割**********
Improvements in these could alter ourresults, quantitatively or qualitatively.• We used the estimated training compute C ≈6NBS, which did not include contributions propor-tional to nctx (see Section 2.1). So our scalings with compute may be confounded in practice in theregime of very large nctx, speciﬁcally where nctx ≳12dmodel.• We tuned learning rates, and we experimented with learning rate schedules. But we may haveneglected to tune some hyperparameter (e.g. intialization scale or momentum) that have an importanteffect on scaling.• The optimal choice of learning rate is sensitive to the target loss. When training close to convergence,it may be necessary to use a smaller learning rate to avoid divergences. But when conducting a shorttraining run (eg due to compute limitations), it may be possible to use a larger learning rate. We didnot experiment with higher learning rates for training runs that did not proceed to convergence.DSupplemental FiguresD.1Early Stopping and Test vs TrainIn section 5.3 we described the result shown in Figure 16, which provides a prediction for a lower bound onthe early stopping step. We also show the train and test loss for a given model size when training on differentsized datasets.D.2Universal TransformersWe compare the performance of standard Transformers to recurrent Transformers [DGV+18] in Figure 17.These models re-use parameters, and so perform slightly better as a function of N, but slightly worse as afunction of compute C.
段落总结：Improvements in these could alter ourresults, quantitatively or qualitatively

**********段落分割**********
We include several different different possibilities for parameter re-use.D.3Batch SizeWe measure the critical batch size using the data displayed in ﬁgure 18. This made it possible to estimateBcrit(L) in ﬁgure 10.23
段落总结：We include several different different possibilities for parameter re-use

**********段落分割**********
105106107108109Parameters, including reuse (non-embedding)2.53.03.54.04.5Test Loss2x Reuse4x Reuse8x ReuseNon-recurrent Models105106107108109Parameters (non-embedding)2.53.03.54.04.5Test Loss2x Reuse4x Reuse8x ReuseNon-recurrent ModelsFigure 17We compare recurrent Transformers [DGV+18], which re-use parameters, to standard Trans-formers. Recurrent Transformers perform slightly better when comparing models with equal parameter count,but slightly worse when accounting for reuse and comparing per FLOP.102103104105Step10610710810910101011Tokens ProcessedBatch Size Scan - 3M Params46810Test Loss101102103104105Step1061081010Tokens ProcessedBatch Size Scan - 85M Params46810Test LossFigure 18These ﬁgures demonstrate ﬁts to Equation (5.1) for a large number of values of the loss L, andfor two different Transformer model sizes. These ﬁts were used to measure Bcrit(L) for Figure 10.D.4Sample Efﬁciency vs Model SizeIt is easy to see from ﬁgure 2 that larger models train faster, and are therefore more sample efﬁcient. Weprovide another way of looking at this phenomenon in ﬁgure 19, which shows when different models reachvarious ﬁxed values of the loss.106107108Parameters (non-embedding)103104105Minimum Steps (Smin)2.53.03.54.04.55.05.5Loss106107108Parameters (non-embedding)10810910101011Minimum Examples (Emin)2.53.03.54.04.55.05.5LossFigure 19The number of minimum serial steps needed to reach any ﬁxed value of the test loss decreasesprecipitously with model size.
段落总结：105106107108109Parameters, including reuse (non-embedding)2

**********段落分割**********
Sample efﬁciency (show here for training far below the critical batch size)improves greatly as well, improving by a factor of almost 100 when comparing the smallest possible modelto a very large one.24
段落总结：Sample efﬁciency (show here for training far below the critical batch size)improves greatly as well,

**********段落分割**********
100101102103Token Index345678Per-Token Test Loss
段落总结：100101102103Token Index345678Per-Token Test Loss

**********段落分割**********
2.3 + 5.4 T0.62106107108Model Parameters101103105Step246810Test LossPer-token Loss (774M Params)100101102103Token IndexFigure 20This ﬁgure provides information about the performance per token as a function of model sizeand training time. Left: Loss per token as a function of its position T in the 1024-token context. Loss scalespredictably as a power-law in T. Right: Test loss per token as a function of training step.104105106107108109Parameters (excl. embedding)3.04.56.07.5Test LossToken 1/1024Token 2/1024Token 4/1024Token 8/1024Token 16/1024Token 64/1024Token 256/1024Token 1024/1024Token 1/8Token 2/8Token 4/8Token 8/8Figure 21In addition to the averaged loss, individual tokens within the 1024-token context also improvesmoothly as model size increases. Training runs with shorter context nctx = 8 (dashed lines) perform betteron early tokens, since they can allocate all of their capacity to them.D.5Context DependenceThe trends for loss as a function of model size are displayed for different tokens in the context in Figure 21.We see that models trained on nctx = 1024 show steady improvement with model size on all but the ﬁrsttoken.Fixing model size, it appears that the loss scales as a power-law as a function of position T in the context, seeFigure 20. This may be a consequence of underlying power-law correlations in language [EP94, ACDE12,LT16], or a more general feature of the model architecture and optimization.
段落总结：2.3 + 5.4 T0.62106107108Model Parameters101103105Step246810Test LossPer-token Loss (774M Params)1001

**********段落分割**********
It provides some suggestion forthe potential beneﬁts (or lack thereof) from training on larger contexts. Not only do larger models convergeto better performance at T = 1024, but they also improve more quickly at early tokens, suggesting that largermodels are more efﬁcient at detecting patterns with less contextual information. In the right-hand plot weshow how per-token performance varies for a ﬁxed model as a function of the training step. The model beginsby learning short-range information, and only learns longer-range correlations later in training.We have also included models trained with a tiny context nctx = 8 in order to compare with our longercontext models. Even modestly sized models trained on nctx = 8 can dominate our largest nctx = 1024models on very early tokens. This also suggests that further improvements should be possible with muchlarger models trained on large contexts.D.6Learning Rate Schedules and Error AnalysisWe experimented with a variety of learning rates and schedules. A host of schedules and resulting testperformances for a small language model are plotted in Figure 22. We conclude that the choice of learningrate schedule is mostly irrelevant, as long as the total summed learning rate is sufﬁciently large, and theschedule includes a warmup period and a ﬁnal decay to near-vanishing learning rate. Variations among25
段落总结：It provides some suggestion forthe potential beneﬁts (or lack thereof) from training on larger conte

**********段落分割**********
[2.3 + 5.4 T]050000100000150000200000250000Step0.00000.00020.00040.00060.00080.0010Learning Rate50100150200250LR Summed Over Steps3.653.703.753.803.853.90LossFigure 22We test a variety of learning rate schedules including cosine decay, linear decay, as well as otherfaster/slower decays schedules on a 3 million parameter model, shown on the left. For these experiments wedo not decay to zero, since we ﬁnd that this tends to give a ﬁxed improvement close to the end of training.We ﬁnd that, as long as the learning rate is not too small and does not decay too quickly, performance doesnot depend strongly on learning rate. Run-to-run variation is at the level of 0.05 in the loss, so averagingmultiple runs is necessary to validate performance changes smaller than this level.104105106107108109Parameters (non-embedding)23456Test Loss (at convergence)
段落总结：[2.3 + 5.4 T]050000100000150000200000250000Step0.00000.00020.00040.00060.00080.0010Learning Rate5010

**********段落分割**********
L = (N/8.8 1013)0.076L =0.25log(N/7.1 1012)Figure 23The trend for performance as a function of parameter count, L(N), is ﬁt better by a power lawthan by other functions such as a logarithm at a qualitative level.schedules appear to be statistical noise, and provide a rough gauge for the scale of variation between differenttraining runs. Experiments on larger models suggest that the variation in the ﬁnal test loss between differentrandom seeds is roughly constant in magnitude for different model sizes.We found that larger models require a smaller learning rate to prevent divergence, while smaller models cantolerate a larger learning rate. To implement this, the following rule of thumb was used for most runs:LR(N) ≈0.003239 + −0.0001395 log(N)(D.1)We expect that this formula could be improved. There may be a dependence on network width, likely set bythe initialization scale. The formula also breaks down for N > 1010 parameters. Nevertheless, we found thatit works sufﬁciently well for the models we considered.D.7Fit Details and Power Law QualityWe experimented with a number of functional forms for the ﬁts to L(N), L(C), and L(D); the power-lawﬁts were qualitatively much more accurate than other functions such as logarithms (see Figure 23).For L(C), we do not include small models with only 1 layer in the ﬁt, as the transition from 1 to 2 layerscauses a noticable lump in the data.
段落总结：L = (N/8.8 1013)0.076L =0.25log(N/7.1 1012)Figure 23The trend for performance as a function of param

**********段落分割**********
For L(N) we also do not include very small models with only 1 layer inthe ﬁt, and we exclude the largest models that have not trained fully to convergence. Fit parameters changemarginally if we do include them, and the trend extrapolates well in both directions regardless.D.8Generalization and ArchitectureIn ﬁgure 24 we show that generalization to other data distributions does not depend on network depth when wehold the total parameter count ﬁxed. It seems to depend only on the performance on the training distribution.26
段落总结：For L(N) we also do not include very small models with only 1 layer inthe ﬁt, and we exclude the lar

**********段落分割**********
[L = (N/8.8 1013)]101102Depth2.32.42.52.62.72.8Test LossWikipediaBooksInternet BooksCommon CrawlWebText2 (Train)WebText2 (Test)Figure 24We show evaluations on a series of datasets for models with approximately 1.5 Billion param-eters. We observe no effect of depth on generalization; generalization performance depends primarily ontraining distribution performance. The 12-layer model overﬁt the Internet Books dataset and we show theearly-stopped performance; we have not seen this surprising result in other experiments.List of Figures1Summary of simple power laws. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .32Illustration of sample efﬁciency and compute efﬁciency. . . . . . . . . . . . . . . . . . . . .43How to scale up model size, batch size, and serial steps . . . . . . . . . . . . . . . . . . . .44Performance when varying model and data size, or model and training steps, simultaneously55Weak dependence of performance on hyperparameter tuning . . . . . . . . . . . . . . . . .86Comparison of performance trend when including or excluding embeddings . . . . . . . . .87LSTM and Transformer performance comparison . . . . . . . . . . . . . . . . . . . . . . .98Generalization to other test datasets. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .109Universality of overﬁtting . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .1110Critical batch size . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
段落总结：[L = (N/8.8 1013)]101102Depth2.32.42.52.62.72.8Test LossWikipediaBooksInternet BooksCommon CrawlWebT

**********段落分割**********
.1211Performance versus compute budget or number of parameter updates . . . . . . . . . . . . .1412Training on suboptimal models . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .1513Comparison between empirical and adjusted compute trends . . . . . . . . . . . . . . . . .1514Optimal model size and serial number of steps versus compute budget . . . . . . . . . . . .1615Contradiction between compute and data trends . . . . . . . . . . . . . . . . . . . . . . . .1716Early stopping lower bound and training curves for overﬁt models. . . . . . . . . . . . . .2317Universal transformers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .2418Batch size scans . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .2419Another look at sample efﬁciency. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .2420Power-law dependence of performance on position in context . . . . . . . . . . . . . . . . .2521Performance at different context positions versus model size. . . . . . . . . . . . . . . . .2522Learning rate schedule scan . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .2623Comparison of Power-Law and Logarithmic Fits. . . . . . . . . . . . . . . . . . . . . . .2624Generalization versus depth . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .2727
段落总结：.1211Performance versus compute budget or number of parameter updates . . . . . . . . . . . . .1412T

**********段落分割**********
List of Tables1Parameter and compute counts for Transformer . . . . . . . . . . . . . . . . . . . . . . . .72Fits to L(N, D) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .113Fits to L(N, S) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .144Key trend equations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .205Key parameters to trend ﬁts . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .206Trends for compute-efﬁcient training . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .20References
段落总结：List of Tables1Parameter and compute counts for Transformer

**********段落分割**********
[ACDE12]Eduardo G Altmann, Giampaolo Cristadoro, and Mirko Degli Esposti. On the origin of long-range correlations in texts. Proceedings of the National Academy of Sciences, 109(29):11582–11587, 2012. 25
段落总结：[ACDE12]Eduardo G Altmann, Giampaolo Cristadoro, and Mirko Degli Esposti

**********段落分割**********
[AS17]Madhu S. Advani and Andrew M. Saxe. High-dimensional dynamics of generalization error inneural networks. arXiv, 2017, 1710.03667. 11, 18, 22
段落总结：[AS17]Madhu S. Advani and Andrew M. Saxe. High-dimensional dynamics of generalization error inneural

**********段落分割**********
[BB01]Michele Banko and Eric Brill. Scaling to very very large corpora for natural language disam-biguation. In Proceedings of the 39th annual meeting on association for computational linguis-tics, pages 26–33. Association for Computational Linguistics, 2001. 18[BHMM18] Mikhail Belkin, Daniel Hsu, Siyuan Ma, and Soumik Mandal. Reconciling modern machinelearning and the bias-variance trade-off. arXiv, 2018, 1812.11118. 18[Bia12]GÃŠrard Biau. Analysis of a random forests model. Journal of Machine Learning Research,13(Apr):1063–1095, 2012. 18
段落总结：[BB01]Michele Banko and Eric Brill

**********段落分割**********
[CGRS19]Rewon Child, Scott Gray, Alec Radford, and Ilya Sutskever. Generating long sequences withsparse transformers. CoRR, abs/1904.10509, 2019, 1904.10509. URL http://arxiv.org/abs/1904.10509. 19
段落总结：[CGRS19]Rewon Child, Scott Gray, Alec Radford, and Ilya Sutskever

**********段落分割**********
[DCLT18]Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre-training of deepbidirectional transformers for language understanding, 2018, arXiv:1810.04805. 2[DGV+18] Mostafa Dehghani, Stephan Gouws, Oriol Vinyals, Jakob Uszkoreit, and Lukasz Kaiser. Uni-versal transformers. CoRR, abs/1807.03819, 2018, 1807.03819. URL http://arxiv.org/abs/1807.03819. 6, 9, 23, 24
段落总结：[DCLT18]Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova

**********段落分割**********
[EP94]Werner Ebeling and Thorsten Pöschel. Entropy and long-range correlations in literary english.EPL (Europhysics Letters), 26(4):241, 1994. 25[Fou]The Common Crawl Foundation. Common crawl. URL http://commoncrawl.org. 7[GARD18] Guy Gur-Ari, Daniel A. Roberts, and Ethan Dyer. Gradient descent happens in a tiny subspace.2018, arXiv:1812.04754. 18
段落总结：[EP94]Werner Ebeling and Thorsten Pöschel

**********段落分割**********
[GJS+19]Mario Geiger, Arthur Jacot, Stefano Spigler, Franck Gabriel, Levent Sagun, Stéphane d’Ascoli,Giulio Biroli, Clément Hongler, and Matthieu Wyart. Scaling description of generalization withnumber of parameters in deep learning. arXiv, 2019, 1901.01608. 18
段落总结：[GJS+19]Mario Geiger, Arthur Jacot, Stefano Spigler, Franck Gabriel, Levent Sagun, Stéphane d’Ascoli

**********段落分割**********
[GKX19]Behrooz Ghorbani, Shankar Krishnan, and Ying Xiao. An investigation into neural net op-timization via hessian eigenvalue density. CoRR, abs/1901.10159, 2019, 1901.10159. URLhttp://arxiv.org/abs/1901.10159. 18[Goo01]Joshua Goodman. A bit of progress in language modeling. CoRR, cs.CL/0108005, 2001. URLhttp://arxiv.org/abs/cs.CL/0108005. 18
段落总结：[GKX19]Behrooz Ghorbani, Shankar Krishnan, and Ying Xiao

**********段落分割**********
[GRK17]Scott Gray, Alec Radford, and Diederik P Kingma. Gpu kernels for block-sparse weights. ope-nai.com, 2017. 19
段落总结：[GRK17]Scott Gray, Alec Radford, and Diederik P Kingma

**********段落分割**********
[HAD19]Joel Hestness, Newsha Ardalani, and Gregory Diamos. Beyond human-level accuracy: Compu-tational challenges in deep learning. In Proceedings of the 24th Symposium on Principles andPractice of Parallel Programming, PPoPP ’19, pages 1–14, New York, NY, USA, 2019. ACM.doi:10.1145/3293883.3295710. 1828
段落总结：[HAD19]Joel Hestness, Newsha Ardalani, and Gregory Diamos

**********段落分割**********
[HCC+18]Yanping Huang, Yonglong Cheng, Dehao Chen, HyoukJoong Lee, Jiquan Ngiam, Quoc V. Le,and Zhifeng Chen. Gpipe: Efﬁcient training of giant neural networks using pipeline parallelism.CoRR, abs/1811.06965, 2018, 1811.06965. URL http://arxiv.org/abs/1811.06965. 19[HNA+17] Joel Hestness, Sharan Narang, Newsha Ardalani, Gregory Diamos, Heewoo Jun, Hassan Kia-ninejad, Md. Mostofa Ali Patwary, Yang Yang, and Yanqi Zhou. Deep learning scaling is pre-dictable, empirically, 2017, 1712.00409. 18
段落总结：[HCC+18]Yanping Huang, Yonglong Cheng, Dehao Chen, HyoukJoong Lee, Jiquan Ngiam, Quoc V

**********段落分割**********
[JGH18]Arthur Jacot, Franck Gabriel, and Clément Hongler. Neural tangent kernel: Convergence andgeneralization in neural networks. In Advances in neural information processing systems, pages8571–8580, 2018. 18
段落总结：[JGH18]Arthur Jacot, Franck Gabriel, and Clément Hongler

**********段落分割**********
[KB14]Diederik P. Kingma and Jimmy Ba.Adam: A method for stochastic optimization, 2014,1412.6980. 7[Kom19]Aran Komatsuzaki. One epoch is all you need, 2019, arXiv:1906.06669. 18
段落总结：[KB14]Diederik P. Kingma and Jimmy Ba.Adam: A method for stochastic optimization, 2014,1412.6980. 7[

**********段落分割**********
[KSH12]Alex Krizhevsky, Ilya Sutskever, and Geoffrey E. Hinton. Imagenet classiﬁcation with deepconvolutional neural networks. In Proceedings of the 25th International Conference on NeuralInformation Processing Systems - Volume 1, NIPS’12, pages 1097–1105, USA, 2012. CurranAssociates Inc. URL http://dl.acm.org/citation.cfm?id=2999134.2999257. 19
段落总结：[KSH12]Alex Krizhevsky, Ilya Sutskever, and Geoffrey E

**********段落分割**********
[LCG+19]Zhenzhong Lan, Mingda Chen, Sebastian Goodman, Kevin Gimpel, Piyush Sharma, and RaduSoricut.Albert: A lite bert for self-supervised learning of language representations, 2019,1909.11942. 9
段落总结：[LCG+19]Zhenzhong Lan, Mingda Chen, Sebastian Goodman, Kevin Gimpel, Piyush Sharma, and RaduSoricut

**********段落分割**********
[LOG+19]Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, MikeLewis, Luke Zettlemoyer, and Veselin Stoyanov. Roberta: A robustly optimized BERT pretrain-ing approach. CoRR, abs/1907.11692, 2019, 1907.11692. URL http://arxiv.org/abs/1907.11692. 2
段落总结：[LOG+19]Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, MikeLewi

**********段落分割**********
[LSP+18]Peter J. Liu, Mohammad Saleh, Etienne Pot, Ben Goodrich, Ryan Sepassi, Lukasz Kaiser, andNoam Shazeer. Generating wikipedia by summarizing long sequences. arXiv:1801.10198 [cs],2018, 1801.10198. URL http://arxiv.org/abs/1801.10198. 2, 6
段落总结：[LSP+18]Peter J. Liu, Mohammad Saleh, Etienne Pot, Ben Goodrich, Ryan Sepassi, Lukasz Kaiser, andNoa

**********段落分割**********
[LT16]Henry W Lin and Max Tegmark. Criticality in formal languages and statistical physics. arXivpreprint arXiv:1606.06737, 2016. 25
段落总结：[LT16]Henry W Lin and Max Tegmark

**********段落分割**********
[LXS+19]Jaehoon Lee, Lechao Xiao, Samuel S. Schoenholz, Yasaman Bahri, Roman Novak, Jascha Sohl-Dickstein, and Jeffrey Pennington. Wide neural networks of any depth evolve as linear modelsunder gradient descent, 2019, arXiv:1902.06720. 18[MKAT18] Sam McCandlish, Jared Kaplan, Dario Amodei, and OpenAI Dota Team. An empirical modelof large-batch training, 2018, arXiv:1812.06162. 3, 5, 6, 12, 13, 21[Pap18]Vardan Papyan. The full spectrum of deep net hessians at scale: Dynamics with sample size.CoRR, abs/1811.07062, 2018, 1811.07062. URL http://arxiv.org/abs/1811.07062. 18
段落总结：[LXS+19]Jaehoon Lee, Lechao Xiao, Samuel S

**********段落分割**********
[RNSS18]Alec Radford, Karthik Narasimhan, Tim Salimans, and Ilya Sutskever. Improving languageunderstanding by generative pre-training. URL https://s3-us-west-2. amazonaws. com/openai-assets/research-covers/languageunsupervised/language understanding paper. pdf, 2018. 2, 6[RRBS19a] Jonathan S. Rosenfeld, Amir Rosenfeld, Yonatan Belinkov, and Nir Shavit.A constructiveprediction of the generalization error across scales, 2019, 1909.12673. 18[RRBS19b] Jonathan S. Rosenfeld, Amir Rosenfeld, Yonatan Belinkov, and Nir Shavit.A constructiveprediction of the generalization error across scales, 2019, arXiv:1909.12673. 18
段落总结：[RNSS18]Alec Radford, Karthik Narasimhan, Tim Salimans, and Ilya Sutskever

**********段落分割**********
[RSR+19]Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena,Yanqi Zhou, Wei Li, and Peter J. Liu. Exploring the limits of transfer learning with a uniﬁedtext-to-text transformer, 2019, arXiv:1910.10683. 2[RWC+19] Alec Radford, Jeff Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever. Languagemodels are unsupervised multitask learners. openai.com, 2019. 2, 5, 6, 7, 8
段落总结：[RSR+19]Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena,Yanqi

**********段落分割**********
[SCP+18]Noam Shazeer, Youlong Cheng, Niki Parmar, Dustin Tran, Ashish Vaswani, Penporn Koanan-takool, Peter Hawkins, HyoukJoong Lee, Mingsheng Hong, Cliff Young, Ryan Sepassi, andBlake Hechtman. Mesh-tensorﬂow: Deep learning for supercomputers, 2018, 1811.02084. 19
段落总结：[SCP+18]Noam Shazeer, Youlong Cheng, Niki Parmar, Dustin Tran, Ashish Vaswani, Penporn Koanan-takool

**********段落分割**********
[SHB15]Rico Sennrich, Barry Haddow, and Alexandra Birch. Neural machine translation of rare wordswith subword units. CoRR, 2015, 1508.07909. 629
段落总结：[SHB15]Rico Sennrich, Barry Haddow, and Alexandra Birch

**********段落分割**********
[SLA+18]Christopher J. Shallue, Jaehoon Lee, Joe Antognini, Jascha Sohl-Dickstein, Roy Frostig, andGeorge E. Dahl. Measuring the effects of data parallelism on neural network training, 2018,arXiv:1811.03600. 12
段落总结：[SLA+18]Christopher J

**********段落分割**********
[SS18]Noam Shazeer and Mitchell Stern. Adafactor: Adaptive learning rates with sublinear memorycost. CoRR, abs/1804.04235, 2018, 1804.04235. URL http://arxiv.org/abs/1804.04235.7
段落总结：[SS18]Noam Shazeer and Mitchell Stern

**********段落分割**********
[THK18]Stefan Thurner, Rudolf Hanel, and Peter Klimek. Introduction to the theory of complex systems.Oxford University Press, 2018. 18
段落总结：[THK18]Stefan Thurner, Rudolf Hanel, and Peter Klimek

**********段落分割**********
[TL19]Mingxing Tan and Quoc V. Le. Efﬁcientnet: Rethinking model scaling for convolutional neuralnetworks. CoRR, abs/1905.11946, 2019, 1905.11946. URL http://arxiv.org/abs/1905.11946. 18
段落总结：[TL19]Mingxing Tan and Quoc V

**********段落分割**********
[VSP+17]Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez,Ł ukasz Kaiser, and Illia Polosukhin. Attention is all you need. In I. Guyon, U. V. Luxburg,S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, and R. Garnett, editors, Advances in NeuralInformation Processing Systems 30, pages 5998–6008. Curran Associates, Inc., 2017. URLhttp://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf. 2, 6
段落总结：[VSP+17]Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez,Ł uka

**********段落分割**********
[VWB16]Andreas Veit, Michael Wilber, and Serge Belongie. Residual networks behave like ensemblesof relatively shallow networks, 2016, arXiv:1605.06431. 8, 18[Was06]Larry Wasserman. All of nonparametric statistics. Springer Science & Business Media, 2006.18[WPN+19] Alex Wang, Yada Pruksachatkun, Nikita Nangia, Amanpreet Singh, Julian Michael, Felix Hill,Omer Levy, and Samuel R. Bowman. Superglue: A stickier benchmark for general-purposelanguage understanding systems, 2019, 1905.00537. 2
段落总结：[VWB16]Andreas Veit, Michael Wilber, and Serge Belongie

**********段落分割**********
[WRH17]Yu-Xiong Wang, Deva Ramanan, and Martial Hebert. Growing a brain: Fine-tuning by in-creasing model capacity. 2017 IEEE Conference on Computer Vision and Pattern Recognition(CVPR), Jul 2017. doi:10.1109/cvpr.2017.323. 19
段落总结：[WRH17]Yu-Xiong Wang, Deva Ramanan, and Martial Hebert

**********段落分割**********
[WYL19]Wei Wen, Feng Yan, and Hai Li. Autogrow: Automatic layer growing in deep convolutionalnetworks, 2019, 1906.02909. 19[YDY+19] Zhilin Yang, Zihang Dai, Yiming Yang, Jaime Carbonell, Ruslan Salakhutdinov, and Quoc V.Le.Xlnet:Generalized autoregressive pretraining for language understanding, 2019,arXiv:1906.08237. 2
段落总结：[WYL19]Wei Wen, Feng Yan, and Hai Li

**********段落分割**********
[ZK16]Sergey Zagoruyko and Nikos Komodakis. Wide residual networks. Procedings of the BritishMachine Vision Conference 2016, 2016. doi:10.5244/c.30.87. 18
段落总结：[ZK16]Sergey Zagoruyko and Nikos Komodakis

**********段落分割**********
[ZKZ+15]Yukun Zhu, Ryan Kiros, Rich Zemel, Ruslan Salakhutdinov, Raquel Urtasun, Antonio Tor-ralba, and Sanja Fidler. Aligning books and movies: Towards story-like visual explanations bywatching movies and reading books. 2015 IEEE International Conference on Computer Vision(ICCV), Dec 2015. doi:10.1109/iccv.2015.11. 7
段落总结：[ZKZ+15]Yukun Zhu, Ryan Kiros, Rich Zemel, Ruslan Salakhutdinov, Raquel Urtasun, Antonio Tor-ralba, 

**********段落分割**********
[ZLN+19]Guodong Zhang, Lala Li, Zachary Nado, James Martens, Sushant Sachdeva, George E. Dahl,Christopher J. Shallue, and Roger B. Grosse. Which algorithmic choices matter at which batchsizes? insights from a noisy quadratic model. CoRR, abs/1907.04164, 2019, 1907.04164. URLhttp://arxiv.org/abs/1907.04164. 12, 1830
段落总结：[ZLN+19]Guodong Zhang, Lala Li, Zachary Nado, James Martens, Sushant Sachdeva, George E
