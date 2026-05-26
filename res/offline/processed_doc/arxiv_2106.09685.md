LORA: LOW-RANK ADAPTATION OF LARGE LAN-
段落总结：LORA: LOW-RANK ADAPTATION OF LARGE LAN-

**********段落分割**********
GUAGE MODELSEdward Hu∗Yelong Shen∗Phillip WallisZeyuan Allen-ZhuYuanzhi LiShean WangLu WangWeizhu ChenMicrosoft Corporation{edwardhu, yeshe, phwallis, zeyuana,yuanzhil, swang, luw, wzchen}@microsoft.comyuanzhil@andrew.cmu.edu(Version 2)
段落总结：GUAGE MODELSEdward Hu∗Yelong Shen∗Phillip WallisZeyuan Allen-ZhuYuanzhi LiShean WangLu WangWeizhu Ch

**********段落分割**********
ABSTRACTAn important paradigm of natural language processing consists of large-scale pre-training on general domain data and adaptation to particular tasks or domains. Aswe pre-train larger models, full ﬁne-tuning, which retrains all model parameters,becomes less feasible. Using GPT-3 175B as an example – deploying indepen-dent instances of ﬁne-tuned models, each with 175B parameters, is prohibitivelyexpensive. We propose Low-Rank Adaptation, or LoRA, which freezes the pre-trained model weights and injects trainable rank decomposition matrices into eachlayer of the Transformer architecture, greatly reducing the number of trainable pa-rameters for downstream tasks. Compared to GPT-3 175B ﬁne-tuned with Adam,LoRA can reduce the number of trainable parameters by 10,000 times and theGPU memory requirement by 3 times. LoRA performs on-par or better than ﬁne-tuning in model quality on RoBERTa, DeBERTa, GPT-2, and GPT-3, despite hav-ing fewer trainable parameters, a higher training throughput, and, unlike adapters,no additional inference latency. We also provide an empirical investigation intorank-deﬁciency in language model adaptation, which sheds light on the efﬁcacy ofLoRA. We release a package that facilitates the integration of LoRA with PyTorchmodels and provide our implementations and model checkpoints for RoBERTa,DeBERTa, and GPT-2 at https://github.com/microsoft/LoRA.1
段落总结：ABSTRACTAn important paradigm of natural language processing consists of large-scale pre-training on

**********段落分割**********
INTRODUCTIONPretrainedWeights𝑊∈ℝ𝑑×𝑑xh𝐵= 0𝐴= 𝒩(0, 𝜎2)𝑑𝑟Figure 1: Our reparametriza-tion. We only train A and B.Many applications in natural language processing rely on adapt-ing one large-scale, pre-trained language model to multiple down-stream applications. Such adaptation is usually done via ﬁne-tuning,which updates all the parameters of the pre-trained model. The ma-jor downside of ﬁne-tuning is that the new model contains as manyparameters as in the original model. As larger models are trainedevery few months, this changes from a mere “inconvenience” forGPT-2 (Radford et al., b) or RoBERTa large (Liu et al., 2019) to acritical deployment challenge for GPT-3 (Brown et al., 2020) with175 billion trainable parameters.1Many sought to mitigate this by adapting only some parameters orlearning external modules for new tasks. This way, we only needto store and load a small number of task-speciﬁc parameters in ad-dition to the pre-trained model for each task, greatly boosting theoperational efﬁciency when deployed. However, existing techniques∗Equal contribution.0Compared to V1, this draft includes better baselines, experiments on GLUE, and more on adapter latency.1While GPT-3 175B achieves non-trivial performance with few-shot learning, ﬁne-tuning boosts its perfor-mance signiﬁcantly as shown in Appendix A.1arXiv:2106.09685v2  [cs.CL]  16 Oct 2021
段落总结：INTRODUCTIONPretrainedWeights𝑊∈ℝ𝑑×𝑑xh𝐵= 0𝐴= 𝒩(0, 𝜎2)𝑑𝑟Figure 1: Our reparametriza-tion

**********段落分割**********
[INTRODUCTION]often introduce inference latency (Houlsby et al., 2019; Rebufﬁet al., 2017) by extending modeldepth or reduce the model’s usable sequence length (Li & Liang, 2021; Lester et al., 2021; Ham-bardzumyan et al., 2020; Liu et al., 2021) (Section 3). More importantly, these method often fail tomatch the ﬁne-tuning baselines, posing a trade-off between efﬁciency and model quality.We take inspiration from Li et al. (2018a); Aghajanyan et al. (2020) which show that the learnedover-parametrized models in fact reside on a low intrinsic dimension. We hypothesize that thechange in weights during model adaptation also has a low “intrinsic rank”, leading to our proposedLow-Rank Adaptation (LoRA) approach. LoRA allows us to train some dense layers in a neuralnetwork indirectly by optimizing rank decomposition matrices of the dense layers’ change duringadaptation instead, while keeping the pre-trained weights frozen, as shown in Figure 1. Using GPT-3175B as an example, we show that a very low rank (i.e., r in Figure 1 can be one or two) sufﬁces evenwhen the full rank (i.e., d) is as high as 12,288, making LoRA both storage- and compute-efﬁcient.LoRA possesses several key advantages.• A pre-trained model can be shared and used to build many small LoRA modules for dif-ferent tasks.
段落总结：[INTRODUCTION]often introduce inference latency (Houlsby et al

**********段落分割**********
We can freeze the shared model and efﬁciently switch tasks by replacing thematrices A and B in Figure 1, reducing the storage requirement and task-switching over-head signiﬁcantly.• LoRA makes training more efﬁcient and lowers the hardware barrier to entry by up to 3times when using adaptive optimizers since we do not need to calculate the gradients ormaintain the optimizer states for most parameters. Instead, we only optimize the injected,much smaller low-rank matrices.• Our simple linear design allows us to merge the trainable matrices with the frozen weightswhen deployed, introducing no inference latency compared to a fully ﬁne-tuned model, byconstruction.• LoRA is orthogonal to many prior methods and can be combined with many of them, suchas preﬁx-tuning. We provide an example in Appendix E.Terminologies and ConventionsWe make frequent references to the Transformer architectureand use the conventional terminologies for its dimensions.We call the input and output di-mension size of a Transformer layer dmodel.We use Wq, Wk, Wv, and Wo to refer to thequery/key/value/output projection matrices in the self-attention module. W or W0 refers to a pre-trained weight matrix and ∆W its accumulated gradient update during adaptation. We use r todenote the rank of a LoRA module.
段落总结：We can freeze the shared model and efﬁciently switch tasks by replacing thematrices A and B in Figur

**********段落分割**********
We follow the conventions set out by (Vaswani et al., 2017;Brown et al., 2020) and use Adam (Loshchilov & Hutter, 2019; Kingma & Ba, 2017) for modeloptimization and use a Transformer MLP feedforward dimension dffn = 4 × dmodel.2
段落总结：We follow the conventions set out by (Vaswani et al

**********段落分割**********
PROBLEM STATEMENTWhile our proposal is agnostic to training objective, we focus on language modeling as our motivat-ing use case. Below is a brief description of the language modeling problem and, in particular, themaximization of conditional probabilities given a task-speciﬁc prompt.Suppose we are given a pre-trained autoregressive language model PΦ(y|x) parametrized by Φ.For instance, PΦ(y|x) can be a generic multi-task learner such as GPT (Radford et al., b; Brownet al., 2020) based on the Transformer architecture (Vaswani et al., 2017). Consider adapting thispre-trained model to downstream conditional text generation tasks, such as summarization, machinereading comprehension (MRC), and natural language to SQL (NL2SQL). Each downstream task isrepresented by a training dataset of context-target pairs: Z = {(xi, yi)}i=1,..,N, where both xi andyi are sequences of tokens. For example, in NL2SQL, xi is a natural language query and yi itscorresponding SQL command; for summarization, xi is the content of an article and yi its summary.2
段落总结：PROBLEM STATEMENTWhile our proposal is agnostic to training objective, we focus on language modeling

**********段落分割**********
[PROBLEM STATEMENT]During full ﬁne-tuning, the model is initialized to pre-trained weights Φ0 and updated to Φ0 + ∆Φby repeatedly following the gradient to maximize the conditional language modeling objective:maxΦX(x,y)∈Z|y|Xt=1log (PΦ(yt|x, y<t))(1)One of the main drawbacks for full ﬁne-tuning is that for each downstream task, we learn a differentset of parameters ∆Φ whose dimension |∆Φ| equals |Φ0|. Thus, if the pre-trained model is large(such as GPT-3 with |Φ0| ≈175 Billion), storing and deploying many independent instances ofﬁne-tuned models can be challenging, if at all feasible.In this paper, we adopt a more parameter-efﬁcient approach, where the task-speciﬁc parameterincrement ∆Φ = ∆Φ(Θ) is further encoded by a much smaller-sized set of parameters Θ with|Θ| ≪|Φ0|. The task of ﬁnding ∆Φ thus becomes optimizing over Θ:maxΘX(x,y)∈Z|y|Xt=1log pΦ0+∆Φ(Θ)(yt|x, y<t)(2)In the subsequent sections, we propose to use a low-rank representation to encode ∆Φ that is bothcompute- and memory-efﬁcient. When the pre-trained model is GPT-3 175B, the number of train-able parameters |Θ| can be as small as 0.01% of |Φ0|.3
段落总结：[PROBLEM STATEMENT]During full ﬁne-tuning, the model is initialized to pre-trained weights Φ0 and up

**********段落分割**********
AREN’T EXISTING SOLUTIONS GOOD ENOUGH?The problem we set out to tackle is by no means new. Since the inception of transfer learning, dozensof works have sought to make model adaptation more parameter- and compute-efﬁcient. See Sec-tion 6 for a survey of some of the well-known works. Using language modeling as an example, thereare two prominent strategies when it comes to efﬁcient adaptations: adding adapter layers (Houlsbyet al., 2019; Rebufﬁet al., 2017; Pfeiffer et al., 2021; R¨uckl´e et al., 2020) or optimizing some formsof the input layer activations (Li & Liang, 2021; Lester et al., 2021; Hambardzumyan et al., 2020;Liu et al., 2021). However, both strategies have their limitations, especially in a large-scale andlatency-sensitive production scenario.Adapter Layers Introduce Inference LatencyThere are many variants of adapters. We focuson the original design by Houlsby et al. (2019) which has two adapter layers per Transformer blockand a more recent one by Lin et al. (2020) which has only one per block but with an additionalLayerNorm (Ba et al., 2016). While one can reduce the overall latency by pruning layers or exploit-ing multi-task settings (R¨uckl´e et al., 2020; Pfeiffer et al., 2021), there is no direct ways to bypassthe extra compute in adapter layers. This seems like a non-issue since adapter layers are designedto have few parameters (sometimes <1% of the original model) by having a small bottleneck di-mension, which limits the FLOPs they can add.
段落总结：AREN’T EXISTING SOLUTIONS GOOD ENOUGH?The problem we set out to tackle is by no means new

**********段落分割**********
However, large neural networks rely on hardwareparallelism to keep the latency low, and adapter layers have to be processed sequentially. This makesa difference in the online inference setting where the batch size is typically as small as one. In ageneric scenario without model parallelism, such as running inference on GPT-2 (Radford et al., b)medium on a single GPU, we see a noticeable increase in latency when using adapters, even with avery small bottleneck dimension (Table 1).This problem gets worse when we need to shard the model as done in Shoeybi et al. (2020); Lep-ikhin et al. (2020), because the additional depth requires more synchronous GPU operations such asAllReduce and Broadcast, unless we store the adapter parameters redundantly many times.Directly Optimizing the Prompt is HardThe other direction, as exempliﬁed by preﬁx tuning (Li& Liang, 2021), faces a different challenge. We observe that preﬁx tuning is difﬁcult to optimizeand that its performance changes non-monotonically in trainable parameters, conﬁrming similarobservations in the original paper. More fundamentally, reserving a part of the sequence length foradaptation necessarily reduces the sequence length available to process a downstream task, whichwe suspect makes tuning the prompt less performant compared to other methods. We defer the studyon task performance to Section 5.3
段落总结：However, large neural networks rely on hardwareparallelism to keep the latency low, and adapter laye

**********段落分割**********
[AREN’T EXISTING SOLUTIONS GOOD ENOUGH?]Batch Size32161Sequence Length512256128|Θ|0.5M11M11MFine-Tune/LoRA1449.4±0.8338.0±0.619.8±2.7AdapterL1482.0±1.0 (+2.2%)354.8±0.5 (+5.0%)23.9±2.1 (+20.7%)AdapterH1492.2±1.0 (+3.0%)366.3±0.5 (+8.4%)25.8±2.2 (+30.3%)Table 1: Infernece latency of a single forward pass in GPT-2 medium measured in milliseconds, av-eraged over 100 trials. We use an NVIDIA Quadro RTX8000. “|Θ|” denotes the number of trainableparameters in adapter layers. AdapterL and AdapterH are two variants of adapter tuning, which wedescribe in Section 5.1. The inference latency introduced by adapter layers can be signiﬁcant in anonline, short-sequence-length scenario. See the full study in Appendix B.4
段落总结：[AREN’T EXISTING SOLUTIONS GOOD ENOUGH?]Batch Size32161Sequence Length512256128|Θ|0

**********段落分割**********
OUR METHODWe describe the simple design of LoRA and its practical beneﬁts. The principles outlined here applyto any dense layers in deep learning models, though we only focus on certain weights in Transformerlanguage models in our experiments as the motivating use case.4.1
段落总结：OUR METHODWe describe the simple design of LoRA and its practical beneﬁts

**********段落分割**********
LOW-RANK-PARAMETRIZED UPDATE MATRICESA neural network contains many dense layers which perform matrix multiplication. The weightmatrices in these layers typically have full-rank. When adapting to a speciﬁc task, Aghajanyan et al.(2020) shows that the pre-trained language models have a low “instrisic dimension” and can stilllearn efﬁciently despite a random projection to a smaller subspace. Inspired by this, we hypothe-size the updates to the weights also have a low “intrinsic rank” during adaptation. For a pre-trainedweight matrix W0 ∈Rd×k, we constrain its update by representing the latter with a low-rank de-composition W0 + ∆W = W0 + BA, where B ∈Rd×r, A ∈Rr×k, and the rank r ≪min(d, k).During training, W0 is frozen and does not receive gradient updates, while A and B contain trainableparameters. Note both W0 and ∆W = BA are multiplied with the same input, and their respectiveoutput vectors are summed coordinate-wise. For h = W0x, our modiﬁed forward pass yields:h = W0x + ∆Wx = W0x + BAx(3)We illustrate our reparametrization in Figure 1. We use a random Gaussian initialization for A andzero for B, so ∆W = BA is zero at the beginning of training. We then scale ∆Wx by αr , where αis a constant in r. When optimizing with Adam, tuning α is roughly the same as tuning the learningrate if we scale the initialization appropriately. As a result, we simply set α to the ﬁrst r we tryand do not tune it.
段落总结：LOW-RANK-PARAMETRIZED UPDATE MATRICESA neural network contains many dense layers which perform matri

**********段落分割**********
This scaling helps to reduce the need to retune hyperparameters when we varyr (Yang & Hu, 2021).A Generalization of Full Fine-tuning.A more general form of ﬁne-tuning allows the training ofa subset of the pre-trained parameters. LoRA takes a step further and does not require the accumu-lated gradient update to weight matrices to have full-rank during adaptation. This means that whenapplying LoRA to all weight matrices and training all biases2, we roughly recover the expressive-ness of full ﬁne-tuning by setting the LoRA rank r to the rank of the pre-trained weight matrices. Inother words, as we increase the number of trainable parameters 3, training LoRA roughly convergesto training the original model, while adapter-based methods converges to an MLP and preﬁx-basedmethods to a model that cannot take long input sequences.No Additional Inference Latency.When deployed in production, we can explicitly compute andstore W = W0 + BA and perform inference as usual. Note that both W0 and BA are in Rd×k.When we need to switch to another downstream task, we can recover W0 by subtracting BA andthen adding a different B′A′, a quick operation with very little memory overhead. Critically, this2They represent a negligible number of parameters compared to weights.3An inevitability when adapting to hard tasks.4
段落总结：This scaling helps to reduce the need to retune hyperparameters when we varyr (Yang & Hu, 2021)

**********段落分割**********
[LOW-RANK-PARAMETRIZED UPDATE MATRICES]guarantees that we do not introduce any additional latency during inference compared to a ﬁne-tunedmodel by construction.4.2
段落总结：[LOW-RANK-PARAMETRIZED UPDATE MATRICES]guarantees that we do not introduce any additional latency du

**********段落分割**********
APPLYING LORA TO TRANSFORMERIn principle, we can apply LoRA to any subset of weight matrices in a neural network to reduce thenumber of trainable parameters. In the Transformer architecture, there are four weight matrices inthe self-attention module (Wq, Wk, Wv, Wo) and two in the MLP module. We treat Wq (or Wk, Wv)as a single matrix of dimension dmodel ×dmodel, even though the output dimension is usually slicedinto attention heads. We limit our study to only adapting the attention weights for downstreamtasks and freeze the MLP modules (so they are not trained in downstream tasks) both for simplicityand parameter-efﬁciency.We further study the effect on adapting different types of attention weightmatrices in a Transformer in Section 7.1. We leave the empirical investigation of adapting the MLPlayers, LayerNorm layers, and biases to a future work.Practical Beneﬁts and Limitations.The most signiﬁcant beneﬁt comes from the reduction inmemory and storage usage. For a large Transformer trained with Adam, we reduce that VRAMusage by up to 2/3 if r ≪dmodel as we do not need to store the optimizer states for the frozenparameters. On GPT-3 175B, we reduce the VRAM consumption during training from 1.2TB to350GB. With r = 4 and only the query and value projection matrices being adapted, the checkpointsize is reduced by roughly 10,000× (from 350GB to 35MB)4. This allows us to train with signiﬁ-cantly fewer GPUs and avoid I/O bottlenecks.
段落总结：APPLYING LORA TO TRANSFORMERIn principle, we can apply LoRA to any subset of weight matrices in a ne

**********段落分割**********
Another beneﬁt is that we can switch between taskswhile deployed at a much lower cost by only swapping the LoRA weights as opposed to all theparameters. This allows for the creation of many customized models that can be swapped in and outon the ﬂy on machines that store the pre-trained weights in VRAM. We also observe a 25% speedupduring training on GPT-3 175B compared to full ﬁne-tuning5 as we do not need to calculate thegradient for the vast majority of the parameters.LoRA also has its limitations. For example, it is not straightforward to batch inputs to different taskswith different A and B in a single forward pass, if one chooses to absorb A and B into W to eliminateadditional inference latency. Though it is possible to not merge the weights and dynamically choosethe LoRA modules to use for samples in a batch for scenarios where latency is not critical.5
段落总结：Another beneﬁt is that we can switch between taskswhile deployed at a much lower cost by only swappi

**********段落分割**********
EMPIRICAL EXPERIMENTSWe evaluate the downstream task performance of LoRA on RoBERTa (Liu et al., 2019), De-BERTa (He et al., 2021), and GPT-2 (Radford et al., b), before scaling up to GPT-3 175B (Brownet al., 2020). Our experiments cover a wide range of tasks, from natural language understanding(NLU) to generation (NLG). Speciﬁcally, we evaluate on the GLUE (Wang et al., 2019) benchmarkfor RoBERTa and DeBERTa. We follow the setup of Li & Liang (2021) on GPT-2 for a direct com-parison and add WikiSQL (Zhong et al., 2017) (NL to SQL queries) and SAMSum (Gliwa et al.,2019) (conversation summarization) for large-scale experiments on GPT-3. See Appendix C formore details on the datasets we use. We use NVIDIA Tesla V100 for all experiments.5.1
段落总结：EMPIRICAL EXPERIMENTSWe evaluate the downstream task performance of LoRA on RoBERTa (Liu et al

**********段落分割**********
BASELINESTo compare with other baselines broadly, we replicate the setups used by prior work and reuse theirreported numbers whenever possible. This, however, means that some baselines might only appearin certain experiments.Fine-Tuning (FT) is a common approach for adaptation. During ﬁne-tuning, the model is initializedto the pre-trained weights and biases, and all model parameters undergo gradient updates.A simplevariant is to update only some layers while freezing others. We include one such baseline reportedin prior work (Li & Liang, 2021) on GPT-2, which adapts just the last two layers (FTTop2).4We still need the 350GB model during deployment; however, storing 100 adapted models only requires350GB + 35MB * 100 ≈354GB as opposed to 100 * 350GB ≈35TB.5For GPT-3 175B, the training throughput for full ﬁne-tuning is 32.5 tokens/s per V100 GPU; with the samenumber of weight shards for model parallelism, the throughput is 43.1 tokens/s per V100 GPU for LoRA.5
段落总结：BASELINESTo compare with other baselines broadly, we replicate the setups used by prior work and reu

**********段落分割**********
[BASELINES]Model & Method # TrainableParameters MNLISST-2MRPCCoLAQNLIQQPRTESTS-B Avg.RoBbase (FT)*
段落总结：[BASELINES]Model & Method # TrainableParameters MNLISST-2MRPCCoLAQNLIQQPRTESTS-B Avg

**********段落分割**********
125.0M87.694.890.263.692.891.978.791.286.4RoBbase (BitFit)*0.1M84.793.792.762.091.884.081.590.885.2RoBbase (AdptD)*0.3M 87.1±.0 94.2±.1 88.5±1.1 60.8±.4 93.1±.1 90.2±.0 71.5±2.7 89.7±.3 84.4RoBbase (AdptD)*
段落总结：125.0M87.694.890.263.692.891.978.791.286.4RoBbase (BitFit)*0.1M84.793.792.762.091.884.081.590.885.2R

**********段落分割**********
0.9M 87.3±.1 94.7±.3 88.4±.162.6±.9 93.0±.2 90.6±.0 75.9±2.2 90.3±.1 85.4RoBbase (LoRA)
段落总结：0.9M 87.3±.1 94.7±.3 88.4±.162.6±.9 93.0±.2 90.6±.0 75.9±2.2 90.3±.1 85.4RoBbase (LoRA)

**********段落分割**********
0.3M 87.5±.3 95.1±.2 89.7±.7 63.4±1.2 93.3±.3 90.8±.1 86.6±.791.5±.2 87.2RoBlarge (FT)*
段落总结：0.3M 87.5±.3 95.1±.2 89.7±.7 63.4±1.2 93.3±.3 90.8±.1 86.6±.791.5±.2 87.2RoBlarge (FT)*

**********段落分割**********
355.0M90.296.490.968.094.792.286.692.488.9RoBlarge (LoRA)0.8M 90.6±.2 96.2±.5 90.9±1.2 68.2±1.9 94.9±.3 91.6±.1 87.4±2.5 92.6±.2 89.0RoBlarge (AdptP)†3.0M 90.2±.3 96.1±.3 90.2±.7 68.3±1.0 94.8±.2 91.9±.1 83.8±2.9 92.1±.7 88.4RoBlarge (AdptP)†0.8M 90.5±.3 96.6±.2 89.7±1.2 67.8±2.5 94.8±.3 91.7±.2 80.1±2.9 91.9±.4 87.9RoBlarge (AdptH)†6.0M 89.9±.5 96.2±.3 88.7±2.9 66.5±4.4 94.7±.2 92.1±.1 83.4±1.1 91.0±1.7 87.8RoBlarge (AdptH)†0.8M 90.3±.3 96.3±.5 87.7±1.7 66.3±2.0 94.7±.2 91.5±.1 72.9±2.9 91.5±.5 86.4RoBlarge (LoRA)†0.8M 90.6±.2 96.2±.5 90.2±1.0 68.2±1.9 94.8±.3 91.6±.2 85.2±1.1 92.3±.5 88.6DeBXXL (FT)*
段落总结：355.0M90.296.490.968.094.792.286.692.488.9RoBlarge (LoRA)0.8M 90.6±.2 96.2±.5 90.9±1.2 68.2±1.9 94.9

**********段落分割**********
1500.0M91.897.292.072.096.092.793.992.991.1DeBXXL (LoRA)
段落总结：1500.0M91.897.292.072.096.092.793.992.991.1DeBXXL (LoRA)

**********段落分割**********
4.7M 91.9±.2 96.9±.2 92.6±.6 72.4±1.1 96.0±.1 92.9±.1 94.9±.493.0±.2 91.3Table 2: RoBERTabase, RoBERTalarge, and DeBERTaXXL with different adaptation methods on theGLUE benchmark. We report the overall (matched and mismatched) accuracy for MNLI, Matthew’scorrelation for CoLA, Pearson correlation for STS-B, and accuracy for other tasks. Higher is betterfor all metrics. * indicates numbers published in prior works. † indicates runs conﬁgured in a setupsimilar to Houlsby et al. (2019) for a fair comparison.Bias-only or BitFit is a baseline where we only train the bias vectors while freezing everything else.Contemporarily, this baseline has also been studied by BitFit (Zaken et al., 2021).Preﬁx-embedding tuning (PreEmbed) inserts special tokens among the input tokens. These spe-cial tokens have trainable word embeddings and are generally not in the model’s vocabulary. Whereto place such tokens can have an impact on performance. We focus on “preﬁxing”, which prependssuch tokens to the prompt, and “inﬁxing”, which appends to the prompt; both are discussed in Li &Liang (2021). We use lp (resp. li) denote the number of preﬁx (resp. inﬁx) tokens. The number oftrainable parameters is |Θ| = dmodel × (lp + li).Preﬁx-layer tuning (PreLayer) is an extension to preﬁx-embedding tuning. Instead of just learningthe word embeddings (or equivalently, the activations after the embedding layer) for some specialtokens, we learn the activations after every Transformer layer.
段落总结：4.7M 91.9±.2 96.9±.2 92.6±.6 72.4±1.1 96.0±.1 92.9±.1 94.9±.493.0±.2 91.3Table 2: RoBERTabase, RoBER

**********段落分割**********
The activations computed from pre-vious layers are simply replaced by trainable ones. The resulting number of trainable parameters is|Θ| = L × dmodel × (lp + li), where L is the number of Transformer layers.Adapter tuning as proposed in Houlsby et al. (2019) inserts adapter layers between the self-attention module (and the MLP module) and the subsequent residual connection. There are twofully connected layers with biases in an adapter layer with a nonlinearity in between. We call thisoriginal design AdapterH. Recently, Lin et al. (2020) proposed a more efﬁcient design with theadapter layer applied only after the MLP module and after a LayerNorm. We call it AdapterL. Thisis very similar to another deign proposed in Pfeiffer et al. (2021), which we call AdapterP. We alsoinclude another baseline call AdapterDrop (R¨uckl´e et al., 2020) which drops some adapter layers forgreater efﬁciency (AdapterD).
段落总结：The activations computed from pre-vious layers are simply replaced by trainable ones

**********段落分割**********
We cite numbers from prior works whenever possible to maximizethe number of baselines we compare with; they are in rows with an asterisk (*) in the ﬁrst column.In all cases, we have |Θ| = ˆLAdpt ×(2×dmodel ×r+r+dmodel)+2× ˆLLN ×dmodel where ˆLAdptis the number of adapter layers and ˆLLN the number of trainable LayerNorms (e.g., in AdapterL).LoRA adds trainable pairs of rank decomposition matrices in parallel to existing weight matrices.As mentioned in Section 4.2, we only apply LoRA to Wq and Wv in most experiments for simplicity.The number of trainable parameters is determined by the rank r and the shape of the original weights:|Θ| = 2 × ˆLLoRA × dmodel × r, where ˆLLoRA is the number of weight matrices we apply LoRA to.6
段落总结：We cite numbers from prior works whenever possible to maximizethe number of baselines we compare wit

**********段落分割**********
[4.7M 91.9±.2 96.9±.2 92.6±.6 72.4±1.1 96.0±.1 92.9±.1 94.9±.4]Model & Method
段落总结：[4.7M 91.9±.2 96.9±.2 92.6±.6 72.4±1.1 96.0±.1 92.9±.1 94.9±.4]Model & Method

**********段落分割**********
# TrainableE2E NLG ChallengeParametersBLEUNISTMET
段落总结：# TrainableE2E NLG ChallengeParametersBLEUNISTMET

**********段落分割**********
354.92M68.28.6246.271.02.47GPT-2 M (AdapterL)*0.37M66.38.4145.069.82.40GPT-2 M (AdapterL)*
段落总结：354.92M68.28.6246.271.02.47GPT-2 M (AdapterL)*0.37M66.38.4145.069.82.40GPT-2 M (AdapterL)*

**********段落分割**********
11.09M68.98.7146.171.32.47GPT-2 M (AdapterH)
段落总结：11.09M68.98.7146.171.32.47GPT-2 M (AdapterH)

**********段落分割**********
11.09M67.3±.68.50±.0746.0±.270.7±.22.44±.01GPT-2 M (FTTop2)*
段落总结：11.09M67.3±.68.50±.0746.0±.270.7±.22.44±.01GPT-2 M (FTTop2)*

**********段落分割**********
25.19M68.18.5946.070.82.41GPT-2 M (PreLayer)*0.35M69.78.8146.171.42.49GPT-2 M (LoRA)0.35M70.4±.18.85±.0246.8±.271.8±.12.53±.02
段落总结：25.19M68.18.5946.070.82.41GPT-2 M (PreLayer)*0.35M69.78.8146.171.42.49GPT-2 M (LoRA)0.35M70.4±.18.85

**********段落分割**********
774.03M68.58.7846.069.92.45GPT-2 L (AdapterL)0.88M69.1±.18.68±.0346.3±.071.4±.22.49±.0GPT-2 L (AdapterL)
段落总结：774.03M68.58.7846.069.92.45GPT-2 L (AdapterL)0.88M69.1±.18.68±.0346.3±.071.4±.22.49±.0GPT-2 L (Adapt

**********段落分割**********
23.00M68.9±.38.70±.0446.1±.171.3±.22.45±.02GPT-2 L (PreLayer)*0.77M70.38.8546.271.72.47GPT-2 L (LoRA)0.77M70.4±.18.89±.0246.8±.272.0±.22.47±.02Table 3: GPT-2 medium (M) and large (L) with different adaptation methods on the E2E NLGChallenge. For all metrics, higher is better. LoRA outperforms several baselines with comparableor fewer trainable parameters. Conﬁdence intervals are shown for experiments we ran. * indicatesnumbers published in prior works.5.2
段落总结：23.00M68.9±.38.70±.0446.1±.171.3±.22.45±.02GPT-2 L (PreLayer)*0.77M70.38.8546.271.72.47GPT-2 L (LoRA

**********段落分割**********
ROBERTA BASE/LARGERoBERTa (Liu et al., 2019) optimized the pre-training recipe originally proposed in BERT (Devlinet al., 2019a) and boosted the latter’s task performance without introducing many more trainableparameters. While RoBERTa has been overtaken by much larger models on NLP leaderboardssuch as the GLUE benchmark (Wang et al., 2019) in recent years, it remains a competitive andpopular pre-trained model for its size among practitioners. We take the pre-trained RoBERTa base(125M) and RoBERTa large (355M) from the HuggingFace Transformers library (Wolf et al., 2020)and evaluate the performance of different efﬁcient adaptation approaches on tasks from the GLUEbenchmark. We also replicate Houlsby et al. (2019) and Pfeiffer et al. (2021) according to theirsetup. To ensure a fair comparison, we make two crucial changes to how we evaluate LoRA whencomparing with adapters. First, we use the same batch size for all tasks and use a sequence lengthof 128 to match the adapter baselines. Second, we initialize the model to the pre-trained model forMRPC, RTE, and STS-B, not a model already adapted to MNLI like the ﬁne-tuning baseline. Runsfollowing this more restricted setup from Houlsby et al. (2019) are labeled with †. The result ispresented in Table 2 (Top Three Sections). See Section D.1 for details on the hyperparameters used.5.3
段落总结：ROBERTA BASE/LARGERoBERTa (Liu et al

**********段落分割**********
DEBERTA XXLDeBERTa (He et al., 2021) is a more recent variant of BERT that is trained on a much largerscale and performs very competitively on benchmarks such as GLUE (Wang et al., 2019) and Su-perGLUE (Wang et al., 2020). We evaluate if LoRA can still match the performance of a fullyﬁne-tuned DeBERTa XXL (1.5B) on GLUE. The result is presented in Table 2 (Bottom Section).See Section D.2 for details on the hyperparameters used.5.4
段落总结：DEBERTA XXLDeBERTa (He et al

**********段落分割**********
GPT-2 MEDIUM/LARGEHaving shown that LoRA can be a competitive alternative to full ﬁne-tuning on NLU, we hope toanswer if LoRA still prevails on NLG models, such as GPT-2 medium and large (Radford et al.,b). We keep our setup as close as possible to Li & Liang (2021) for a direct comparison. Dueto space constraint, we only present our result on E2E NLG Challenge (Table 3) in this section.See Section F.1 for results on WebNLG (Gardent et al., 2017) and DART (Nan et al., 2020). Weinclude a list of the hyperparameters used in Section D.3.7
段落总结：GPT-2 MEDIUM/LARGEHaving shown that LoRA can be a competitive alternative to full ﬁne-tuning on NLU,

**********段落分割**********
[GPT-2 MEDIUM/LARGE]Model&Method
段落总结：[GPT-2 MEDIUM/LARGE]Model&Method

**********段落分割**********
# TrainableWikiSQLMNLI-mSAMSumParametersAcc. (%)Acc. (%)
段落总结：# TrainableWikiSQLMNLI-mSAMSumParametersAcc

**********段落分割**********
175,255.8M73.889.552.0/28.0/44.5GPT-3 (BitFit)14.2M71.391.051.3/27.4/43.5GPT-3 (PreEmbed)3.2M63.188.648.3/24.2/40.5GPT-3 (PreLayer)20.2M70.189.550.8/27.3/43.5GPT-3 (AdapterH)7.1M71.989.853.0/28.9/44.8GPT-3 (AdapterH)40.1M73.291.553.2/29.0/45.1GPT-3 (LoRA)4.7M73.491.753.8/29.8/45.9GPT-3 (LoRA)37.7M74.091.653.4/29.2/45.1Table 4: Performance of different adaptation methods on GPT-3 175B. We report the logical formvalidation accuracy on WikiSQL, validation accuracy on MultiNLI-matched, and Rouge-1/2/L onSAMSum. LoRA performs better than prior approaches, including full ﬁne-tuning. The resultson WikiSQL have a ﬂuctuation around ±0.5%, MNLI-m around ±0.1%, and SAMSum around±0.2/±0.2/±0.1 for the three metrics.5.5
段落总结：175,255.8M73.889.552.0/28.0/44.5GPT-3 (BitFit)14.2M71.391.051.3/27.4/43.5GPT-3 (PreEmbed)3.2M63.188.

**********段落分割**********
SCALING UP TO GPT-3 175BAs a ﬁnal stress test for LoRA, we scale up to GPT-3 with 175 billion parameters. Due to the hightraining cost, we only report the typical standard deviation for a given task over random seeds, asopposed to providing one for every entry. See Section D.4 for details on the hyperparameters used.As shown in Table 4, LoRA matches or exceeds the ﬁne-tuning baseline on all three datasets. Notethat not all methods beneﬁt monotonically from having more trainable parameters, as shown in Fig-ure 2. We observe a signiﬁcant performance drop when we use more than 256 special tokens forpreﬁx-embedding tuning or more than 32 special tokens for preﬁx-layer tuning. This corroboratessimilar observations in Li & Liang (2021). While a thorough investigation into this phenomenonis out-of-scope for this work, we suspect that having more special tokens causes the input distri-bution to shift further away from the pre-training data distribution. Separately, we investigate theperformance of different adaptation approaches in the low-data regime in Section F.3.67891011log10 # Trainable Parameters0.550.600.650.700.75Validation AccuracyWikiSQLMethodFine-TunePrefixEmbedPrefixLayerAdapter(H)LoRA67891011log10 # Trainable Parameters0.840.860.880.900.92MultiNLI-matchedFigure 2: GPT-3 175B validation accuracy vs. number of trainable parameters of several adaptationmethods on WikiSQL and MNLI-matched.
段落总结：SCALING UP TO GPT-3 175BAs a ﬁnal stress test for LoRA, we scale up to GPT-3 with 175 billion parame

**********段落分割**********
LoRA exhibits better scalability and task performance.See Section F.2 for more details on the plotted data points.6
段落总结：LoRA exhibits better scalability and task performance

**********段落分割**********
RELATED WORKSTransformer Language Models.Transformer (Vaswani et al., 2017) is a sequence-to-sequencearchitecture that makes heavy use of self-attention. Radford et al. (a) applied it to autoregressive lan-guage modeling by using a stack of Transformer decoders. Since then, Transformer-based languagemodels have dominated NLP, achieving the state-of-the-art in many tasks. A new paradigm emergedwith BERT (Devlin et al., 2019b) and GPT-2 (Radford et al., b) – both are large Transformer lan-8
段落总结：RELATED WORKSTransformer Language Models

**********段落分割**********
[RELATED WORKS]guage models trained on a large amount of text – where ﬁne-tuning on task-speciﬁc data after pre-training on general domain data provides a signiﬁcant performance gain compared to training ontask-speciﬁc data directly. Training larger Transformers generally results in better performance andremains an active research direction. GPT-3 (Brown et al., 2020) is the largest single Transformerlanguage model trained to-date with 175B parameters.Prompt Engineering and Fine-Tuning.While GPT-3 175B can adapt its behavior with just afew additional training examples, the result depends heavily on the input prompt (Brown et al.,2020). This necessitates an empirical art of composing and formatting the prompt to maximize amodel’s performance on a desired task, which is known as prompt engineering or prompt hacking.Fine-tuning retrains a model pre-trained on general domains to a speciﬁc task Devlin et al. (2019b);Radford et al. (a). Variants of it include learning just a subset of the parameters Devlin et al. (2019b);Collobert & Weston (2008), yet practitioners often retrain all of them to maximize the downstreamperformance.
段落总结：[RELATED WORKS]guage models trained on a large amount of text – where ﬁne-tuning on task-speciﬁc dat

**********段落分割**********
However, the enormity of GPT-3 175B makes it challenging to perform ﬁne-tuning inthe usual way due to the large checkpoint it produces and the high hardware barrier to entry since ithas the same memory footprint as pre-training.Parameter-Efﬁcient Adaptation.Many have proposed inserting adapter layers between existinglayers in a neural network (Houlsby et al., 2019; Rebufﬁet al., 2017; Lin et al., 2020). Our methoduses a similar bottleneck structure to impose a low-rank constraint on the weight updates. Thekey functional difference is that our learned weights can be merged with the main weights duringinference, thus not introducing any latency, which is not the case for the adapter layers (Section 3).A comtenporary extension of adapter is COMPACTER (Mahabadi et al., 2021), which essentiallyparametrizes the adapter layers using Kronecker products with some predetermined weight sharingscheme. Similarly, combining LoRA with other tensor product-based methods could potentiallyimprove its parameter efﬁciency, which we leave to future work. More recently, many proposedoptimizing the input word embeddings in lieu of ﬁne-tuning, akin to a continuous and differentiablegeneralization of prompt engineering (Li & Liang, 2021; Lester et al., 2021; Hambardzumyan et al.,2020; Liu et al., 2021).
段落总结：However, the enormity of GPT-3 175B makes it challenging to perform ﬁne-tuning inthe usual way due t

**********段落分割**********
We include comparisons with Li & Liang (2021) in our experiment section.However, this line of works can only scale up by using more special tokens in the prompt, whichtake up available sequence length for task tokens when positional embeddings are learned.Low-Rank Structures in Deep Learning.Low-rank structure is very common in machine learn-ing. A lot of machine learning problems have certain intrinsic low-rank structure (Li et al., 2016;Cai et al., 2010; Li et al., 2018b; Grasedyck et al., 2013). Moreover, it is known that for manydeep learning tasks, especially those with a heavily over-parametrized neural network, the learnedneural network will enjoy low-rank properties after training (Oymak et al., 2019). Some prior workseven explicitly impose the low-rank constraint when training the original neural network (Sainathet al., 2013; Povey et al., 2018; Zhang et al., 2014; Jaderberg et al., 2014; Zhao et al., 2016; Kho-dak et al., 2021; Denil et al., 2014); however, to the best of our knowledge, none of these worksconsiders low-rank update to a frozen model for adaptation to downstream tasks. In theory liter-ature, it is known that neural networks outperform other classical learning methods, including thecorresponding (ﬁnite-width) neural tangent kernels (Allen-Zhu et al., 2019; Li & Liang, 2018) whenthe underlying concept class has certain low-rank structure (Ghorbani et al., 2020; Allen-Zhu & Li,2019; Allen-Zhu & Li, 2020a).
段落总结：We include comparisons with Li & Liang (2021) in our experiment section

**********段落分割**********
Another theoretical result in Allen-Zhu & Li (2020b) suggests thatlow-rank adaptations can be useful for adversarial training. In sum, we believe that our proposedlow-rank adaptation update is well-motivated by the literature.7
段落总结：Another theoretical result in Allen-Zhu & Li (2020b) suggests thatlow-rank adaptations can be useful

**********段落分割**********
UNDERSTANDING THE LOW-RANK UPDATESGiven the empirical advantage of LoRA, we hope to further explain the properties of the low-rankadaptation learned from downstream tasks. Note that the low-rank structure not only lowers thehardware barrier to entry which allows us to run multiple experiments in parallel, but also givesbetter interpretability of how the update weights are correlated with the pre-trained weights. Wefocus our study on GPT-3 175B, where we achieved the largest reduction of trainable parameters(up to 10,000×) without adversely affecting task performances.We perform a sequence of empirical studies to answer the following questions: 1) Given a parameterbudget constraint, which subset of weight matrices in a pre-trained Transformer should we adapt9
段落总结：UNDERSTANDING THE LOW-RANK UPDATESGiven the empirical advantage of LoRA, we hope to further explain 

**********段落分割**********
[UNDERSTANDING THE LOW-RANK UPDATES]to maximize downstream performance? 2) Is the “optimal” adaptation matrix ∆W really rank-deﬁcient? If so, what is a good rank to use in practice? 3) What is the connection between ∆W andW? Does ∆W highly correlate with W? How large is ∆W comparing to W?We believe that our answers to question (2) and (3) shed light on the fundamental principles of usingpre-trained language models for downstream tasks, which is a critical topic in NLP.7.1WHICH WEIGHT MATRICES IN TRANSFORMER SHOULD WE APPLY LORA TO?Given a limited parameter budget, which types of weights should we adapt with LoRA to obtainthe best performance on downstream tasks? As mentioned in Section 4.2, we only consider weightmatrices in the self-attention module. We set a parameter budget of 18M (roughly 35MB if storedin FP16) on GPT-3 175B, which corresponds to r = 8 if we adapt one type of attention weights orr = 4 if we adapt two types, for all 96 layers. The result is presented in Table 5.
段落总结：[UNDERSTANDING THE LOW-RANK UPDATES]to maximize downstream performance? 2) Is the “optimal” adaptati

**********段落分割**********
# of Trainable Parameters = 18MWeight TypeWqWkWvWoWq, WkWq, WvWq, Wk, Wv, WoRank r8888442WikiSQL (±0.5%)70.470.073.073.271.473.773.7MultiNLI (±0.1%)91.090.891.091.391.391.391.7Table 5: Validation accuracy on WikiSQL and MultiNLI after applying LoRA to different types ofattention weights in GPT-3, given the same number of trainable parameters. Adapting both Wq andWv gives the best performance overall. We ﬁnd the standard deviation across random seeds to beconsistent for a given dataset, which we report in the ﬁrst column.Note that putting all the parameters in ∆Wq or ∆Wk results in signiﬁcantly lower performance,while adapting both Wq and Wv yields the best result. This suggests that even a rank of fourcaptures enough information in ∆W such that it is preferable to adapt more weight matrices thanadapting a single type of weights with a larger rank.7.2WHAT IS THE OPTIMAL RANK r FOR LORA?We turn our attention to the effect of rank r on model performance.We adapt {Wq, Wv},{Wq, Wk, Wv, Wc}, and just Wq for a comparison.Weight Typer = 1r = 2r = 4r = 8r = 64WikiSQL(±0.5%)Wq68.869.670.570.470.0Wq, Wv73.473.373.773.873.5Wq, Wk, Wv, Wo74.173.774.074.073.9MultiNLI (±0.1%)Wq90.790.991.190.790.7Wq, Wv91.391.491.391.691.4Wq, Wk, Wv, Wo91.291.791.791.591.4Table 6: Validation accuracy on WikiSQL and MultiNLI with different rank r. To our surprise, arank as small as one sufﬁces for adapting both Wq and Wv on these datasets while training Wq aloneneeds a larger r.
段落总结：# of Trainable Parameters = 18MWeight TypeWqWkWvWoWq, WkWq, WvWq, Wk, Wv, WoRank r8888442WikiSQL (±0

**********段落分割**********
We conduct a similar experiment on GPT-2 in Section H.2.Table 6 shows that, surprisingly, LoRA already performs competitively with a very small r (moreso for {Wq, Wv} than just Wq). This suggests the update matrix ∆W could have a very small“intrinsic rank”.6 To further support this ﬁnding, we check the overlap of the subspaces learned bydifferent choices of r and by different random seeds. We argue that increasing r does not cover amore meaningful subspace, which suggests that a low-rank adaptation matrix is sufﬁcient.6However, we do not expect a small r to work for every task or dataset. Consider the following thoughtexperiment: if the downstream task were in a different language than the one used for pre-training, retrainingthe entire model (similar to LoRA with r = dmodel) could certainly outperform LoRA with a small r.10
段落总结：We conduct a similar experiment on GPT-2 in Section H

**********段落分割**********
[of Trainable Parameters = 18M]Subspace similarity between different r.Given Ar=8 and Ar=64 which are the learned adapta-tion matrices with rank r = 8 and 64 using the same pre-trained model, we perform singular valuedecomposition and obtain the right-singular unitary matrices UAr=8 and UAr=64.7 We hope to an-swer: how much of the subspace spanned by the top i singular vectors in UAr=8 (for 1 ≤i ≤8) iscontained in the subspace spanned by top j singular vectors of UAr=64 (for 1 ≤j ≤64)? We mea-sure this quantity with a normalized subspace similarity based on the Grassmann distance (See Ap-pendix G for a more formal discussion)φ(Ar=8, Ar=64, i, j) = ||U i⊤Ar=8U jAr=64||2Fmin(i, j)∈[0, 1](4)where U iAr=8 represents the columns of UAr=8 corresponding to the top-i singular vectors.φ(·) has a range of [0, 1], where 1 represents a complete overlap of subspaces and 0 a completeseparation. See Figure 3 for how φ changes as we vary i and j. We only look at the 48th layer(out of 96) due to space constraint, but the conclusion holds for other layers as well, as shownin Section H.1.0.00.20.40.60.81.016121823293540465258j12345678iWq16121823293540465258jWv12345678jWq12345678jWv(Ar = 64, Ar = 8, i, j)Figure 3: Subspace similarity between column vectors of Ar=8 and Ar=64 for both ∆Wq and ∆Wv.The third and the fourth ﬁgures zoom in on the lower-left triangle in the ﬁrst two ﬁgures.
段落总结：[of Trainable Parameters = 18M]Subspace similarity between different r

**********段落分割**********
The topdirections in r = 8 are included in r = 64, and vice versa.We make an important observation from Figure 3.Directions corresponding to the top singular vector overlap signiﬁcantly betweenAr=8 and Ar=64, while others do not. Speciﬁcally, ∆Wv (resp. ∆Wq) of Ar=8and ∆Wv (resp. ∆Wq) of Ar=64 share a subspace of dimension 1 with normalizedsimilarity > 0.5, providing an explanation of why r = 1 performs quite well in ourdownstream tasks for GPT-3.Since both Ar=8 and Ar=64 are learned using the same pre-trained model, Figure 3 indicates thatthe top singular-vector directions of Ar=8 and Ar=64 are the most useful, while other directionspotentially contain mostly random noises accumulated during training. Hence, the adaptation matrixcan indeed have a very low rank.Subspace similarity between different random seeds.We further conﬁrm this by plotting thenormalized subspace similarity between two randomly seeded runs with r = 64, shown in Figure 4.∆Wq appears to have a higher “intrinsic rank” than ∆Wv, since more common singular value direc-tions are learned by both runs for ∆Wq, which is in line with our empirical observation in Table 6.As a comparison, we also plot two random Gaussian matrices, which do not share any commonsingular value directions with each other.7.3HOW DOES THE ADAPTATION MATRIX ∆W COMPARE TO W ?We further investigate the relationship between ∆W and W. In particular, does ∆W highly correlatewith W?
段落总结：The topdirections in r = 8 are included in r = 64, and vice versa

**********段落分割**********
(Or mathematically, is ∆W mostly contained in the top singular directions of W?) Also,7Note that a similar analysis can be carried out with B and the left-singular unitary matrices – we stick withA for our experiments.11
段落总结：(Or mathematically, is ∆W mostly contained in the top singular directions of W?) Also,7Note that a s

**********段落分割**********
0.00.10.20.30.40.5151015202530343944495459j18162432404856iWq151015202530343944495459j(Ar = 64, A′r = 64, i, j)Wv151015202530343944495459jRandom GaussianFigure 4: Left and Middle: Normalized subspace similarity between the column vectors of Ar=64from two random seeds, for both ∆Wq and ∆Wv in the 48-th layer. Right: the same heat-mapbetween the column vectors of two random Gaussian matrices. See Section H.1 for other layers.how “large” is ∆W comparing to its corresponding directions in W? This can shed light on theunderlying mechanism for adapting pre-trained language models.To answer these questions, we project W onto the r-dimensional subspace of ∆W by comput-ing U ⊤WV ⊤, with U/V being the left/right singular-vector matrix of ∆W.Then, we com-pare the Frobenius norm between ∥U ⊤WV ⊤∥F and ∥W∥F . As a comparison, we also compute∥U ⊤WV ⊤∥F by replacing U, V with the top r singular vectors of W or a random matrix.r = 4r = 64∆WqWqRandom∆WqWqRandom||U ⊤WqV ⊤||F =0.3221.670.021.9037.710.33||Wq||F = 61.95||∆Wq||F = 6.91||∆Wq||F = 3.57Table 7: The Frobenius norm of U ⊤WqV ⊤where U and V are the left/right top r singular vectordirections of either (1) ∆Wq, (2) Wq, or (3) a random matrix. The weight matrices are taken fromthe 48th layer of GPT-3.We draw several conclusions from Table 7. First, ∆W has a stronger correlation with W comparedto a random matrix, indicating that ∆W ampliﬁes some features that are already in W.
段落总结：0.00.10.20.30.40.5151015202530343944495459j18162432404856iWq151015202530343944495459j(Ar = 64, A′r =

**********段落分割**********
Second,instead of repeating the top singular directions of W, ∆W only ampliﬁes directions that are notemphasized in W. Third, the ampliﬁcation factor is rather huge: 21.5 ≈6.91/0.32 for r = 4.See Section H.4 for why r = 64 has a smaller ampliﬁcation factor. We also provide a visualizationin Section H.3 for how the correlation changes as we include more top singular directions from Wq.This suggests that the low-rank adaptation matrix potentially ampliﬁes the important features forspeciﬁc downstream tasks that were learned but not emphasized in the general pre-training model.8
段落总结：Second,instead of repeating the top singular directions of W, ∆W only ampliﬁes directions that are n

**********段落分割**********
CONCLUSION AND FUTURE WORKFine-tuning enormous language models is prohibitively expensive in terms of the hardware requiredand the storage/switching cost for hosting independent instances for different tasks. We proposeLoRA, an efﬁcient adaptation strategy that neither introduces inference latency nor reduces inputsequence length while retaining high model quality. Importantly, it allows for quick task-switchingwhen deployed as a service by sharing the vast majority of the model parameters. While we focusedon Transformer language models, the proposed principles are generally applicable to any neuralnetworks with dense layers.There are many directions for future works. 1) LoRA can be combined with other efﬁcient adapta-tion methods, potentially providing orthogonal improvement. 2) The mechanism behind ﬁne-tuningor LoRA is far from clear – how are features learned during pre-training transformed to do wellon downstream tasks? We believe that LoRA makes it more tractable to answer this than full ﬁne-12
段落总结：CONCLUSION AND FUTURE WORKFine-tuning enormous language models is prohibitively expensive in terms o

**********段落分割**********
[CONCLUSION AND FUTURE WORK]tuning. 3) We mostly depend on heuristics to select the weight matrices to apply LoRA to. Arethere more principled ways to do it? 4) Finally, the rank-deﬁciency of ∆W suggests that W couldbe rank-deﬁcient as well, which can also be a source of inspiration for future works.
段落总结：[CONCLUSION AND FUTURE WORK]tuning

**********段落分割**********
REFERENCESArmen Aghajanyan, Luke Zettlemoyer, and Sonal Gupta. Intrinsic Dimensionality Explains theEffectiveness of Language Model Fine-Tuning. arXiv:2012.13255 [cs], December 2020. URLhttp://arxiv.org/abs/2012.13255.Zeyuan Allen-Zhu and Yuanzhi Li. What Can ResNet Learn Efﬁciently, Going Beyond Kernels? InNeurIPS, 2019. Full version available at http://arxiv.org/abs/1905.10337.Zeyuan Allen-Zhu and Yuanzhi Li. Backward feature correction: How deep learning performs deeplearning. arXiv preprint arXiv:2001.04413, 2020a.Zeyuan Allen-Zhu and Yuanzhi Li. Feature puriﬁcation: How adversarial training performs robustdeep learning. arXiv preprint arXiv:2005.10190, 2020b.Zeyuan Allen-Zhu, Yuanzhi Li, and Zhao Song. A convergence theory for deep learning via over-parameterization. In ICML, 2019. Full version available at http://arxiv.org/abs/1811.03962.Jimmy Lei Ba, Jamie Ryan Kiros, and Geoffrey E. Hinton. Layer normalization, 2016.Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhari-wal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal,Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M.Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin,Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford,Ilya Sutskever, and Dario Amodei. Language Models are Few-Shot Learners. arXiv:2005.14165[cs], July 2020.
段落总结：REFERENCESArmen Aghajanyan, Luke Zettlemoyer, and Sonal Gupta

**********段落分割**********
URL http://arxiv.org/abs/2005.14165.Jian-Feng Cai, Emmanuel J Cand`es, and Zuowei Shen. A singular value thresholding algorithm formatrix completion. SIAM Journal on optimization, 20(4):1956–1982, 2010.Daniel Cer, Mona Diab, Eneko Agirre, Inigo Lopez-Gazpio, and Lucia Specia. Semeval-2017 task1: Semantic textual similarity multilingual and crosslingual focused evaluation. Proceedings ofthe 11th International Workshop on Semantic Evaluation (SemEval-2017), 2017. doi: 10.18653/v1/s17-2001. URL http://dx.doi.org/10.18653/v1/S17-2001.Ronan Collobert and Jason Weston. A uniﬁed architecture for natural language processing: deepneural networks with multitask learning. In Proceedings of the 25th international conferenceon Machine learning, ICML ’08, pp. 160–167, New York, NY, USA, July 2008. Associationfor Computing Machinery. ISBN 978-1-60558-205-4. doi: 10.1145/1390156.1390177. URLhttps://doi.org/10.1145/1390156.1390177.Misha Denil, Babak Shakibi, Laurent Dinh, Marc’Aurelio Ranzato, and Nando de Freitas. Predictingparameters in deep learning, 2014.Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre-training of deepbidirectional transformers for language understanding, 2019a.Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. BERT: Pre-training of DeepBidirectional Transformers for Language Understanding. arXiv:1810.04805 [cs], May 2019b.URL http://arxiv.org/abs/1810.04805. arXiv: 1810.04805.William B. Dolan and Chris Brockett.
段落总结：URL http://arxiv.org/abs/2005.14165.Jian-Feng Cai, Emmanuel J Cand`es, and Zuowei Shen. A singular v

**********段落分割**********
Automatically constructing a corpus of sentential paraphrases.In Proceedings of the Third International Workshop on Paraphrasing (IWP2005), 2005. URLhttps://aclanthology.org/I05-5002.Claire Gardent, Anastasia Shimorina, Shashi Narayan, and Laura Perez-Beltrachini. The webnlgchallenge: Generating text from rdf data. In Proceedings of the 10th International Conference onNatural Language Generation, pp. 124–133, 2017.13
段落总结：Automatically constructing a corpus of sentential paraphrases

**********段落分割**********
[REFERENCES]Behrooz Ghorbani, Song Mei, Theodor Misiakiewicz, and Andrea Montanari. When do neuralnetworks outperform kernel methods? arXiv preprint arXiv:2006.13409, 2020.Bogdan Gliwa, Iwona Mochol, Maciej Biesek, and Aleksander Wawer. Samsum corpus: A human-annotated dialogue dataset for abstractive summarization. CoRR, abs/1911.12237, 2019. URLhttp://arxiv.org/abs/1911.12237.Lars Grasedyck, Daniel Kressner, and Christine Tobler.A literature survey of low-rank tensorapproximation techniques. GAMM-Mitteilungen, 36(1):53–78, 2013.Jihun Ham and Daniel D. Lee. Grassmann discriminant analysis: a unifying view on subspace-basedlearning. In ICML, pp. 376–383, 2008. URL https://doi.org/10.1145/1390156.1390204.Karen Hambardzumyan, Hrant Khachatrian, and Jonathan May. WARP: Word-level AdversarialReProgramming. arXiv:2101.00121 [cs], December 2020. URL http://arxiv.org/abs/2101.00121. arXiv: 2101.00121.Pengcheng He, Xiaodong Liu, Jianfeng Gao, and Weizhu Chen. Deberta: Decoding-enhanced bertwith disentangled attention, 2021.Neil Houlsby, Andrei Giurgiu, Stanislaw Jastrzebski, Bruna Morrone, Quentin de Laroussilhe,Andrea Gesmundo, Mona Attariyan, and Sylvain Gelly. Parameter-Efﬁcient Transfer Learningfor NLP. arXiv:1902.00751 [cs, stat], June 2019. URL http://arxiv.org/abs/1902.00751.Max Jaderberg, Andrea Vedaldi, and Andrew Zisserman. Speeding up convolutional neural networkswith low rank expansions.
段落总结：[REFERENCES]Behrooz Ghorbani, Song Mei, Theodor Misiakiewicz, and Andrea Montanari

**********段落分割**********
arXiv preprint arXiv:1405.3866, 2014.Mikhail Khodak, Neil Tenenholtz, Lester Mackey, and Nicol`o Fusi. Initialization and regularizationof factorized neural layers, 2021.Diederik P. Kingma and Jimmy Ba. Adam: A method for stochastic optimization, 2017.Dmitry Lepikhin, HyoukJoong Lee, Yuanzhong Xu, Dehao Chen, Orhan Firat, Yanping Huang,Maxim Krikun, Noam Shazeer, and Zhifeng Chen. Gshard: Scaling giant models with conditionalcomputation and automatic sharding, 2020.Brian Lester, Rami Al-Rfou, and Noah Constant. The Power of Scale for Parameter-Efﬁcient PromptTuning. arXiv:2104.08691 [cs], April 2021. URL http://arxiv.org/abs/2104.08691.arXiv: 2104.08691.Chunyuan Li, Heerad Farkhoor, Rosanne Liu, and Jason Yosinski. Measuring the Intrinsic Di-mension of Objective Landscapes.arXiv:1804.08838 [cs, stat], April 2018a.URL http://arxiv.org/abs/1804.08838. arXiv: 1804.08838.Xiang Lisa Li and Percy Liang. Preﬁx-Tuning: Optimizing Continuous Prompts for Generation.arXiv:2101.00190 [cs], January 2021. URL http://arxiv.org/abs/2101.00190.Yuanzhi Li and Yingyu Liang. Learning overparameterized neural networks via stochastic gradientdescent on structured data. In Advances in Neural Information Processing Systems, 2018.Yuanzhi Li, Yingyu Liang, and Andrej Risteski. Recovery guarantee of weighted low-rank ap-proximation via alternating minimization. In International Conference on Machine Learning, pp.
段落总结：arXiv preprint arXiv:1405

**********段落分割**********
2358–2367. PMLR, 2016.Yuanzhi Li, Tengyu Ma, and Hongyang Zhang. Algorithmic regularization in over-parameterizedmatrix sensing and neural networks with quadratic activations. In Conference On Learning The-ory, pp. 2–47. PMLR, 2018b.Zhaojiang Lin, Andrea Madotto, and Pascale Fung. Exploring versatile generative language modelvia parameter-efﬁcient transfer learning. In Findings of the Association for Computational Lin-guistics: EMNLP 2020, pp. 441–459, Online, November 2020. Association for ComputationalLinguistics.doi: 10.18653/v1/2020.ﬁndings-emnlp.41.URL https://aclanthology.org/2020.findings-emnlp.41.14
段落总结：2358–2367. PMLR, 2016.Yuanzhi Li, Tengyu Ma, and Hongyang Zhang. Algorithmic regularization in over-

**********段落分割**********
[2358–2367. PMLR, 2016.]Xiao Liu, Yanan Zheng, Zhengxiao Du, Ming Ding, Yujie Qian, Zhilin Yang, and Jie Tang. GPTUnderstands, Too. arXiv:2103.10385 [cs], March 2021. URL http://arxiv.org/abs/2103.10385. arXiv: 2103.10385.Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, MikeLewis, Luke Zettlemoyer, and Veselin Stoyanov. Roberta: A robustly optimized bert pretrainingapproach, 2019.Ilya Loshchilov and Frank Hutter.Decoupled weight decay regularization.arXiv preprintarXiv:1711.05101, 2017.Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization, 2019.Rabeeh Karimi Mahabadi, James Henderson, and Sebastian Ruder. Compacter: Efﬁcient low-rankhypercomplex adapter layers, 2021.Linyong Nan, Dragomir Radev, Rui Zhang, Amrit Rau, Abhinand Sivaprasad, Chiachun Hsieh,Xiangru Tang, Aadit Vyas, Neha Verma, Pranav Krishna, et al. Dart: Open-domain structureddata record to text generation. arXiv preprint arXiv:2007.02871, 2020.Jekaterina Novikova, Ondˇrej Duˇsek, and Verena Rieser. The e2e dataset: New challenges for end-to-end generation. arXiv preprint arXiv:1706.09254, 2017.Samet Oymak, Zalan Fabian, Mingchen Li, and Mahdi Soltanolkotabi.Generalization guaran-tees for neural networks via harnessing the low-rank structure of the jacobian. arXiv preprintarXiv:1906.05392, 2019.Jonas Pfeiffer, Aishwarya Kamath, Andreas R¨uckl´e, Kyunghyun Cho, and Iryna Gurevych.
段落总结：[2358–2367. PMLR, 2016.]Xiao Liu, Yanan Zheng, Zhengxiao Du, Ming Ding, Yujie Qian, Zhilin Yang, and

**********段落分割**********
Adapter-fusion: Non-destructive task composition for transfer learning, 2021.Daniel Povey, Gaofeng Cheng, Yiming Wang, Ke Li, Hainan Xu, Mahsa Yarmohammadi, and San-jeev Khudanpur. Semi-orthogonal low-rank matrix factorization for deep neural networks. InInterspeech, pp. 3743–3747, 2018.Alec Radford, Karthik Narasimhan, Tim Salimans, and Ilya Sutskever. Improving Language Under-standing by Generative Pre-Training. pp. 12, a.Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever. LanguageModels are Unsupervised Multitask Learners. pp. 24, b.Pranav Rajpurkar, Robin Jia, and Percy Liang. Know what you don’t know: Unanswerable questionsfor squad. CoRR, abs/1806.03822, 2018. URL http://arxiv.org/abs/1806.03822.Sylvestre-Alvise Rebufﬁ, Hakan Bilen, and Andrea Vedaldi. Learning multiple visual domains withresidual adapters. arXiv:1705.08045 [cs, stat], November 2017. URL http://arxiv.org/abs/1705.08045. arXiv: 1705.08045.Andreas R¨uckl´e, Gregor Geigle, Max Glockner, Tilman Beck, Jonas Pfeiffer, Nils Reimers, andIryna Gurevych. Adapterdrop: On the efﬁciency of adapters in transformers, 2020.Tara N Sainath, Brian Kingsbury, Vikas Sindhwani, Ebru Arisoy, and Bhuvana Ramabhadran. Low-rank matrix factorization for deep neural network training with high-dimensional output targets.In 2013 IEEE international conference on acoustics, speech and signal processing, pp. 6655–
段落总结：Adapter-fusion: Non-destructive task composition for transfer learning, 2021

**********段落分割**********
6659. IEEE, 2013.Mohammad Shoeybi, Mostofa Patwary, Raul Puri, Patrick LeGresley, Jared Casper, and BryanCatanzaro. Megatron-lm: Training multi-billion parameter language models using model par-allelism, 2020.Richard Socher, Alex Perelygin, Jean Wu, Jason Chuang, Christopher D. Manning, Andrew Ng,and Christopher Potts. Recursive deep models for semantic compositionality over a sentimenttreebank. In Proceedings of the 2013 Conference on Empirical Methods in Natural LanguageProcessing, pp. 1631–1642, Seattle, Washington, USA, October 2013. Association for Computa-tional Linguistics. URL https://aclanthology.org/D13-1170.15
段落总结：6659. IEEE, 2013.Mohammad Shoeybi, Mostofa Patwary, Raul Puri, Patrick LeGresley, Jared Casper, and 

**********段落分割**********
[6659. IEEE, 2013.]Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez,Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. In Proceedings of the 31st In-ternational Conference on Neural Information Processing Systems, pp. 6000–6010, 2017.Alex Wang, Amanpreet Singh, Julian Michael, Felix Hill, Omer Levy, and Samuel R. Bowman.Glue: A multi-task benchmark and analysis platform for natural language understanding, 2019.Alex Wang, Yada Pruksachatkun, Nikita Nangia, Amanpreet Singh, Julian Michael, Felix Hill, OmerLevy, and Samuel R. Bowman. Superglue: A stickier benchmark for general-purpose languageunderstanding systems, 2020.Alex Warstadt, Amanpreet Singh, and Samuel R Bowman. Neural network acceptability judgments.arXiv preprint arXiv:1805.12471, 2018.Adina Williams, Nikita Nangia, and Samuel Bowman. A broad-coverage challenge corpus for sen-tence understanding through inference.In Proceedings of the 2018 Conference of the NorthAmerican Chapter of the Association for Computational Linguistics: Human Language Technolo-gies, Volume 1 (Long Papers), pp. 1112–1122, New Orleans, Louisiana, June 2018. Associationfor Computational Linguistics. doi: 10.18653/v1/N18-1101.
段落总结：[6659. IEEE, 2013.]Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N 

**********段落分割**********
URL https://www.aclweb.org/anthology/N18-1101.Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue, Anthony Moi,Pierric Cistac, Tim Rault, R´emi Louf, Morgan Funtowicz, Joe Davison, Sam Shleifer, Patrickvon Platen, Clara Ma, Yacine Jernite, Julien Plu, Canwen Xu, Teven Le Scao, Sylvain Gug-ger, Mariama Drame, Quentin Lhoest, and Alexander M. Rush. Transformers: State-of-the-artnatural language processing. In Proceedings of the 2020 Conference on Empirical Methods inNatural Language Processing: System Demonstrations, pp. 38–45, Online, October 2020. As-sociation for Computational Linguistics. URL https://www.aclweb.org/anthology/2020.emnlp-demos.6.Greg Yang and Edward J. Hu.Feature Learning in Inﬁnite-Width Neural Networks.arXiv:2011.14522 [cond-mat], May 2021. URL http://arxiv.org/abs/2011.14522.arXiv: 2011.14522.Elad Ben Zaken, Shauli Ravfogel, and Yoav Goldberg. Bitﬁt: Simple parameter-efﬁcient ﬁne-tuningfor transformer-based masked language-models, 2021.Yu Zhang, Ekapol Chuangsuwanich, and James Glass. Extracting deep neural network bottleneckfeatures using low-rank matrix factorization. In 2014 IEEE international conference on acoustics,speech and signal processing (ICASSP), pp. 185–189. IEEE, 2014.Yong Zhao, Jinyu Li, and Yifan Gong. Low-rank plus diagonal adaptation for deep neural networks.In 2016 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP),pp. 5005–5009.
段落总结：URL https://www.aclweb.org/anthology/N18-1101.Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaum

**********段落分割**********
IEEE, 2016.Victor Zhong, Caiming Xiong, and Richard Socher. Seq2sql: Generating structured queries fromnatural language using reinforcement learning. CoRR, abs/1709.00103, 2017. URL http://arxiv.org/abs/1709.00103.A
段落总结：IEEE, 2016.Victor Zhong, Caiming Xiong, and Richard Socher. Seq2sql: Generating structured queries f

**********段落分割**********
LARGE LANGUAGE MODELS STILL NEED PARAMETER UPDATESFew-shot learning, or prompt engineering, is very advantageous when we only have a handful oftraining samples. However, in practice, we can often afford to curate a few thousand or more trainingexamples for performance-sensitive applications. As shown in Table 8, ﬁne-tuning improves themodel performance drastically compared to few-shot learning on datasets large and small. We takethe GPT-3 few-shot result on RTE from the GPT-3 paper (Brown et al., 2020). For MNLI-matched,we use two demonstrations per class and six in-context examples in total.16
段落总结：LARGE LANGUAGE MODELS STILL NEED PARAMETER UPDATESFew-shot learning, or prompt engineering, is very 

**********段落分割**********
[LARGE LANGUAGE MODELS STILL NEED PARAMETER UPDATES]MethodMNLI-m (Val. Acc./%)RTE (Val. Acc./%)GPT-3 Few-Shot40.669.0GPT-3 Fine-Tuned89.585.4Table 8: Fine-tuning signiﬁcantly outperforms few-shot learning on GPT-3 (Brown et al., 2020).B
段落总结：[LARGE LANGUAGE MODELS STILL NEED PARAMETER UPDATES]MethodMNLI-m (Val

**********段落分割**********
INFERENCE LATENCY INTRODUCED BY ADAPTER LAYERSAdapter layers are external modules added to a pre-trained model in a sequential manner, whereasour proposal, LoRA, can be seen as external modules added in a parallel manner. Consequently,adapter layers must be computed in addition to the base model, inevitably introducing additionallatency. While as pointed out in R¨uckl´e et al. (2020), the latency introduced by adapter layers canbe mitigated when the model batch size and/or sequence length is large enough to full utilize thehardware parallelism. We conﬁrm their observation with a similar latency study on GPT-2 mediumand point out that there are scenarios, notably online inference where the batch size is small, wherethe added latency can be signiﬁcant.We measure the latency of a single forward pass on an NVIDIA Quadro RTX8000 by averagingover 100 trials. We vary the input batch size, sequence length, and the adapter bottleneck dimensionr. We test two adapter designs: the original one by Houlsby et al. (2019), which we call AdapterH,and a recent, more efﬁcient variant by Lin et al. (2020), which we call AdapterL. See Section 5.1for more details on the designs.
段落总结：INFERENCE LATENCY INTRODUCED BY ADAPTER LAYERSAdapter layers are external modules added to a pre-tra

**********段落分割**********
We plot the slow-down in percentage compared to the no-adapterbaseline in Figure 5.05101520253035010100250AdapterH rSeq Len = 128Seq Len = 256Seq Len = 51212481632Batch Size010100250AdapterL r12481632Batch Size12481632Batch SizeFigure 5: Percentage slow-down of inference latency compared to the no-adapter (r = 0) baseline.The top row shows the result for AdapterH and the bottom row AdapterL. Larger batch size andsequence length help to mitigate the latency, but the slow-down can be as high as over 30% in anonline, short-sequence-length scenario. We tweak the colormap for better visibility.C
段落总结：We plot the slow-down in percentage compared to the no-adapterbaseline in Figure 5

**********段落分割**********
DATASET DETAILSGLUE Benchmark is a wide-ranging collection of natural language understanding tasks. It includesMNLI (inference, Williams et al. (2018)), SST-2 (sentiment analysis, Socher et al. (2013)), MRPC(paraphrase detection, Dolan & Brockett (2005)), CoLA (linguistic acceptability, Warstadt et al.(2018)), QNLI (inference, Rajpurkar et al. (2018)), QQP8 (question-answering), RTE (inference),8https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs17
段落总结：DATASET DETAILSGLUE Benchmark is a wide-ranging collection of natural language understanding tasks

**********段落分割**********
[DATASET DETAILS]and STS-B (textual similarity, Cer et al. (2017)). The broad coverage makes GLUE benchmark astandard metric to evaluate NLU models such as RoBERTa and DeBERTa. The individual datasetsare released under different permissive licenses.WikiSQL is introduced in Zhong et al. (2017) and contains 56, 355/8, 421 training/validation ex-amples. The task is to generate SQL queries from natural language questions and table schemata.We encode context as x = {table schema, query} and target as y = {SQL}. The dataset is releaseunder the BSD 3-Clause License.SAMSum is introduced in Gliwa et al. (2019) and contains 14, 732/819 training/test examples. Itconsists of staged chat conversations between two people and corresponding abstractive summarieswritten by linguists. We encode context as ”\n” concatenated utterances followed by a ”\n\n”,and target as y = {summary}. The dataset is released under the non-commercial licence: CreativeCommons BY-NC-ND 4.0.E2E NLG Challenge was ﬁrst introduced in Novikova et al. (2017) as a dataset for training end-to-end, data-driven natural language generation systems and is commonly used for data-to-text evalua-tion. The E2E dataset consists of roughly 42, 000 training, 4, 600 validation, and 4, 600 test exam-ples from the restaurant domain. Each source table used as input can have multiple references. Eachsample input (x, y) consists of a sequence of slot-value pairs, along with a corresponding naturallanguage reference text.
段落总结：[DATASET DETAILS]and STS-B (textual similarity, Cer et al

**********段落分割**********
The dataset is released under Creative Commons BY-NC-SA 4.0.DART is an open-domain data-to-text dataset described in Nan et al. (2020). DART inputs arestructured as sequences of ENTITY — RELATION — ENTITY triples. With 82K examples intotal, DART is a signiﬁcantly larger and more complex data-to-text task compared to E2E. Thedataset is released under the MIT license.WebNLG is another commonly used dataset for data-to-text evaluation (Gardent et al., 2017). With22K examples in total WebNLG comprises 14 distinct categories, nine of which are seen duringtraining. Since ﬁve of the 14 total categories are not seen during training, but are represented inthe test set, evaluation is typically broken out by “seen” categories (S), “unseen” categories (U)and “all” (A). Each input example is represented by a sequence of SUBJECT — PROPERTY —OBJECT triples. The dataset is released under Creative Commons BY-NC-SA 4.0.D
段落总结：The dataset is released under Creative Commons BY-NC-SA 4

**********段落分割**********
HYPERPARAMETERS USED IN EXPERIMENTSD.1
段落总结：HYPERPARAMETERS USED IN EXPERIMENTSD

**********段落分割**********
ROBERTAWe train using AdamW with a linear learning rate decay schedule. We sweep learning rate, numberof training epochs, and batch size for LoRA. Following Liu et al. (2019), we initialize the LoRAmodules to our best MNLI checkpoint when adapting to MRPC, RTE, and STS-B, instead of theusual initialization; the pre-trained model stays frozen for all tasks. We report the median over 5random seeds; the result for each run is taken from the best epoch. For a fair comparison with thesetup in Houlsby et al. (2019) and Pfeiffer et al. (2021), we restrict the model sequence length to 128and used a ﬁxed batch size for all tasks. Importantly, we start with the pre-trained RoBERTa largemodel when adapting to MRPC, RTE, and STS-B, instead of a model already adapted to MNLI.The runs with this restricted setup are marked with †. See the hyperparameters used in our runsin Table 9.D.2
段落总结：ROBERTAWe train using AdamW with a linear learning rate decay schedule

**********段落分割**********
DEBERTAWe again train using AdamW with a linear learning rate decay schedule. Following He et al. (2021),we tune learning rate, dropout probability, warm-up steps, and batch size. We use the same modelsequence length used by (He et al., 2021) to keep our comparison fair. Following He et al. (2021),we initialize the LoRA modules to our best MNLI checkpoint when adapting to MRPC, RTE, andSTS-B, instead of the usual initialization; the pre-trained model stays frozen for all tasks. We reportthe median over 5 random seeds; the result for each run is taken from the best epoch. See thehyperparameters used in our runs in Table 10.18
段落总结：DEBERTAWe again train using AdamW with a linear learning rate decay schedule

**********段落分割**********
[DEBERTA]MethodDatasetMNLISST-2MRPCCoLAQNLIQQPRTESTS-BOptimizerAdamWWarmup Ratio0.06LR ScheduleLinearRoBERTa baseLoRABatch Size1616163232163216
段落总结：[DEBERTA]MethodDatasetMNLISST-2MRPCCoLAQNLIQQPRTESTS-BOptimizerAdamWWarmup Ratio0

**********段落分割**********
# Epochs3060308025258040Learning Rate5E-045E-044E-044E-044E-045E-045E-044E-04LoRA Conﬁg.rq = rv = 8LoRA α8Max Seq. Len.512RoBERTa largeLoRABatch Size44444488
段落总结：# Epochs3060308025258040Learning Rate5E-045E-044E-044E-044E-045E-045E-044E-04LoRA Conﬁg

**********段落分割**********
# Epochs1010202010202030Learning Rate3E-044E-043E-042E-042E-043E-044E-042E-04LoRA Conﬁg.rq = rv = 8LoRA α16Max Seq. Len.128128512128512512512512RoBERTa largeLoRA†Batch Size4
段落总结：# Epochs1010202010202030Learning Rate3E-044E-043E-042E-042E-043E-044E-042E-04LoRA Conﬁg

**********段落分割**********
# Epochs1010202010202010Learning Rate3E-044E-043E-042E-042E-043E-044E-042E-04LoRA Conﬁg.rq = rv = 8LoRA α16Max Seq. Len.128RoBERTa largeAdptP (3M)†Batch Size32
段落总结：# Epochs1010202010202010Learning Rate3E-044E-043E-042E-042E-043E-044E-042E-04LoRA Conﬁg

**********段落分割**********
# Epochs1020202010202020Learning Rate3E-053E-053E-043E-043E-043E-043E-043E-04Bottleneck r64Max Seq. Len.128RoBERTa largeAdptP (0.8M)†Batch Size32
段落总结：# Epochs1020202010202020Learning Rate3E-053E-053E-043E-043E-043E-043E-043E-04Bottleneck r64Max Seq

**********段落分割**********
# Epochs520202010202020Learning Rate3E-043E-043E-043E-043E-043E-043E-043E-04Bottleneck r16Max Seq. Len.128RoBERTa largeAdptH (6M)†Batch Size32
段落总结：# Epochs520202010202020Learning Rate3E-043E-043E-043E-043E-043E-043E-043E-04Bottleneck r16Max Seq

**********段落分割**********
# Epochs10510105202010Learning Rate3E-053E-043E-043E-043E-043E-043E-043E-04Bottleneck r64Max Seq. Len.128RoBERTa largeAdptH (0.8M)†Batch Size32
段落总结：# Epochs10510105202010Learning Rate3E-053E-043E-043E-043E-043E-043E-043E-04Bottleneck r64Max Seq

**********段落分割**********
# Epochs10510105202010Learning Rate3E-043E-043E-043E-043E-043E-043E-043E-04Bottleneck r8Max Seq. Len.128Table 9: The hyperparameters we used for RoBERTa on the GLUE benchmark.D.3GPT-2We train all of our GPT-2 models using AdamW (Loshchilov & Hutter, 2017) with a linear learningrate schedule for 5 epochs. We use the batch size, learning rate, and beam search beam size describedin Li & Liang (2021). Accordingly, we also tune the above hyperparameters for LoRA. We report themean over 3 random seeds; the result for each run is taken from the best epoch. The hyperparametersused for LoRA in GPT-2 are listed in Table 11. For those used for other baselines, see Li & Liang(2021).D.4GPT-3For all GPT-3 experiments, we train using AdamW (Loshchilov & Hutter, 2017) for 2 epochs witha batch size of 128 samples and a weight decay factor of 0.1. We use a sequence length of 384 for19
段落总结：# Epochs10510105202010Learning Rate3E-043E-043E-043E-043E-043E-043E-043E-04Bottleneck r8Max Seq

**********段落分割**********
[Epochs]MethodDatasetMNLISST-2MRPCCoLAQNLIQQPRTESTS-BOptimizerAdamWWarmup Ratio0.1LR ScheduleLinearDeBERTa XXLLoRABatch Size883246844
段落总结：[Epochs]MethodDatasetMNLISST-2MRPCCoLAQNLIQQPRTESTS-BOptimizerAdamWWarmup Ratio0

**********段落分割**********
# Epochs51630108111110Learning Rate1E-046E-052E-041E-041E-041E-042E-042E-04Weight Decay00.010.0100.010.010.010.1CLS Dropout0.15000.10.10.20.20.2LoRA Conﬁg.rq = rv = 8LoRA α8Max Seq. Len.25612812864512320320128Table 10: The hyperparameters for DeBERTa XXL on tasks included in the GLUE benchmark.DatasetE2EWebNLGDARTTrainingOptimizerAdamWWeight Decay0.010.010.0Dropout Prob0.10.10.0Batch Size8
段落总结：# Epochs51630108111110Learning Rate1E-046E-052E-041E-041E-041E-042E-042E-04Weight Decay00

**********段落分割**********
# Epoch5Warmup Steps500Learning Rate ScheduleLinearLabel Smooth0.10.10.0Learning Rate0.0002Adaptationrq = rv = 4LoRA α32InferenceBeam Size10Length Penalty0.90.80.8no repeat ngram size4Table 11: The hyperparameters for GPT-2 LoRA on E2E, WebNLG and DART.WikiSQL (Zhong et al., 2017), 768 for MNLI (Williams et al., 2018), and 2048 for SAMSum (Gliwaet al., 2019). We tune learning rate for all method-dataset combinations. See Section D.4 for moredetails on the hyperparameters used. For preﬁx-embedding tuning, we ﬁnd the optimal lp and lito be 256 and 8, respectively, totalling 3.2M trainable parameters. We use lp = 8 and li = 8 forpreﬁx-layer tuning with 20.2M trainable parameters to obtain the overall best performance. Wepresent two parameter budgets for LoRA: 4.7M (rq = rv = 1 or rv = 2) and 37.7M (rq = rv = 8or rq = rk = rv = ro = 2). We report the best validation performance from each run. The traininghyperparameters used in our GPT-3 experiments are listed in Table 12.E
段落总结：# Epoch5Warmup Steps500Learning Rate ScheduleLinearLabel Smooth0

**********段落分割**********
COMBINING LORA WITH PREFIX TUNINGLoRA can be naturally combined with existing preﬁx-based approaches. In this section, we evaluatetwo combinations of LoRA and variants of preﬁx-tuning on WikiSQL and MNLI.LoRA+PreﬁxEmbed (LoRA+PE) combines LoRA with preﬁx-embedding tuning, where we insertlp + li special tokens whose embeddings are treated as trainable parameters. For more on preﬁx-embedding tuning, see Section 5.1.LoRA+PreﬁxLayer (LoRA+PL) combines LoRA with preﬁx-layer tuning. We also insert lp + lispecial tokens; however, instead of letting the hidden representations of these tokens evolve natu-20
段落总结：COMBINING LORA WITH PREFIX TUNINGLoRA can be naturally combined with existing preﬁx-based approaches

**********段落分割**********
[COMBINING LORA WITH PREFIX TUNING]HyperparametersFine-TunePreEmbedPreLayerBitFitAdapterHLoRAOptimizerAdamWBatch Size128
段落总结：[COMBINING LORA WITH PREFIX TUNING]HyperparametersFine-TunePreEmbedPreLayerBitFitAdapterHLoRAOptimiz

**********段落分割**********
# Epoch2Warmup Tokens250,000LR ScheduleLinearLearning Rate
段落总结：# Epoch2Warmup Tokens250,000LR ScheduleLinearLearning Rate

**********段落分割**********
2.00E-04Table 12: The training hyperparameters used for different GPT-3 adaption methods. We use thesame hyperparameters for all datasets after tuning learning rate.rally, we replace them after every Transformer block with an input agnostic vector. Thus, both theembeddings and subsequent Transformer block activations are treated as trainable parameters. Formore on preﬁx-layer tuning, see Section 5.1.In Table 15, we show the evaluation results of LoRA+PE and LoRA+PL on WikiSQL and MultiNLI.First of all, LoRA+PE signiﬁcantly outperforms both LoRA and preﬁx-embedding tuning onWikiSQL, which indicates that LoRA is somewhat orthogonal to preﬁx-embedding tuning. OnMultiNLI, the combination of LoRA+PE doesn’t perform better than LoRA, possibly because LoRAon its own already achieves performance comparable to the human baseline. Secondly, we noticethat LoRA+PL performs slightly worse than LoRA even with more trainable parameters. We at-tribute this to the fact that preﬁx-layer tuning is very sensitive to the choice of learning rate and thusmakes the optimization of LoRA weights more difﬁcult in LoRA+PL.F
段落总结：2.00E-04Table 12: The training hyperparameters used for different GPT-3 adaption methods. We use the

**********段落分割**********
ADDITIONAL EMPIRICAL EXPERIMENTSF.1
段落总结：ADDITIONAL EMPIRICAL EXPERIMENTSF

**********段落分割**********
ADDITIONAL EXPERIMENTS ON GPT-2We also repeat our experiment on DART (Nan et al., 2020) and WebNLG (Gardent et al., 2017)following the setup of Li & Liang (2021). The result is shown in Table 13. Similar to our resulton E2E NLG Challenge, reported in Section 5, LoRA performs better than or at least on-par withpreﬁx-based approaches given the same number of trainable parameters.Method
段落总结：ADDITIONAL EXPERIMENTS ON GPT-2We also repeat our experiment on DART (Nan et al

**********段落分割**********
# TrainableDARTParametersBLEU↑MET↑TER↓GPT-2 MediumFine-Tune354M46.20.390.46AdapterL0.37M42.40.360.48AdapterL11M45.20.380.46FTTop224M41.00.340.56PrefLayer0.35M46.40.380.46LoRA0.35M47.1±.20.390.46GPT-2 LargeFine-Tune774M47.00.390.46AdapterL0.88M45.7±.10.380.46AdapterL23M47.1±.10.390.45PrefLayer0.77M46.70.380.45LoRA0.77M47.5±.10.390.45Table 13: GPT-2 with different adaptation methods on DART. The variances of MET and TER areless than 0.01 for all adaption approaches.21
段落总结：# TrainableDARTParametersBLEU↑MET↑TER↓GPT-2 MediumFine-Tune354M46

**********段落分割**********
[Trainable]MethodWebNLGBLEU↑MET↑TER↓USAUSAUSAGPT-2 MediumFine-Tune (354M)27.764.246.5.30.45.38.76.33.53AdapterL (0.37M)45.154.550.2.36.39.38.46.40.43AdapterL (11M)48.360.454.9.38.43.41.45.35.39FTTop2 (24M)18.953.636.0.23.38.31.99.49.72Preﬁx (0.35M)45.662.955.1.38.44.41.49.35.40LoRA (0.35M)46.7±.462.1±.255.3±.2.38.44.41.46.33.39GPT-2 LargeFine-Tune (774M)43.165.355.5.38.46.42.53.33.42AdapterL (0.88M)49.8±.061.1±.056.0±.0.38.43.41.44.35.39AdapterL (23M)49.2±.164.7±.257.7±.1.39.46.43.46.33.39Preﬁx (0.77M)47.763.456.3.39.45.42.48.34.40LoRA (0.77M)48.4±.364.0±.357.0±.1.39.45.42.45.32.38Table 14: GPT-2 with different adaptation methods on WebNLG. The variances of MET and TERare less than 0.01 for all the experiments we ran. “U” indicates unseen categories, “S” indicates seencategories, and “A” indicates all categories in the test set of WebNLG.F.2
段落总结：[Trainable]MethodWebNLGBLEU↑MET↑TER↓USAUSAUSAGPT-2 MediumFine-Tune (354M)27

**********段落分割**********
ADDITIONAL EXPERIMENTS ON GPT-3We present additional runs on GPT-3 with different adaptation methods in Table 15. The focus is onidentifying the trade-off between performance and the number of trainable parameters.F.3
段落总结：ADDITIONAL EXPERIMENTS ON GPT-3We present additional runs on GPT-3 with different adaptation methods

**********段落分割**********
LOW-DATA REGIMETo evaluate the performance of different adaptation approaches in the low-data regime. we randomlysample 100, 1k and 10k training examples from the full training set of MNLI to form the low-dataMNLI-n tasks. In Table 16, we show the performance of different adaptation approaches on MNLI-n. To our surprise, PreﬁxEmbed and PreﬁxLayer performs very poorly on MNLI-100 dataset, withPreﬁxEmbed performing only slightly better than random chance (37.6% vs. 33.3%). PreﬁxLayerperforms better than PreﬁxEmbed but is still signiﬁcantly worse than Fine-Tune or LoRA on MNLI-100. The gap between preﬁx-based approaches and LoRA/Fine-tuning becomes smaller as we in-crease the number of training examples, which might suggest that preﬁx-based approaches are notsuitable for low-data tasks in GPT-3. LoRA achieves better performance than ﬁne-tuning on bothMNLI-100 and MNLI-Full, and comparable results on MNLI-1k and MNLI-10K considering the(±0.3) variance due to random seeds.The training hyperparameters of different adaptation approaches on MNLI-n are reported in Ta-ble 17. We use a smaller learning rate for PreﬁxLayer on the MNLI-100 set, as the training loss doesnot decrease with a larger learning rate.G
段落总结：LOW-DATA REGIMETo evaluate the performance of different adaptation approaches in the low-data regime

**********段落分割**********
MEASURING SIMILARITY BETWEEN SUBSPACESIn this paper we use the measure φ(A, B, i, j) = ψ(U iA, U jB) = ∥U i⊤
段落总结：MEASURING SIMILARITY BETWEEN SUBSPACESIn this paper we use the measure φ(A, B, i, j) = ψ(U iA, U jB)

**********段落分割**********
A UB∥2Fmin{i,j}to measure the subspacesimilarity between two column orthonormal matrices U iA ∈Rd×i and U jB ∈Rd×j, obtained bytaking columns of the left singular matrices of A and B. We point out that this similarity is simplya reverse of the standard Projection Metric that measures distance between subspaces Ham & Lee(2008).22
段落总结：A UB∥2Fmin{i,j}to measure the subspacesimilarity between two column orthonormal matrices U iA ∈Rd×i 

**********段落分割**********
[A UB∥2]MethodHyperparameters
段落总结：[A UB∥2]MethodHyperparameters

**********段落分割**********
# Trainable ParametersWikiSQLMNLI-mFine-Tune-175B73.889.5PreﬁxEmbedlp = 32, li = 80.4 M55.984.9lp = 64, li = 80.9 M58.788.1lp = 128, li = 81.7 M60.688.0lp = 256, li = 83.2 M63.188.6lp = 512, li = 86.4 M55.985.8PreﬁxLayerlp = 2, li = 25.1 M68.589.2lp = 8, li = 0
段落总结：# Trainable ParametersWikiSQLMNLI-mFine-Tune-175B73

**********段落分割**********
10.1 M69.888.2lp = 8, li = 8
段落总结：10.1 M69.888.2lp = 8, li = 8

**********段落分割**********
20.2 M70.189.5lp = 32, li = 4
段落总结：20.2 M70.189.5lp = 32, li = 4

**********段落分割**********
44.1 M66.489.6lp = 64, li = 0
段落总结：44.1 M66.489.6lp = 64, li = 0

**********段落分割**********
76.1 M64.987.9AdapterHr = 17.1 M71.989.8r = 4
段落总结：76.1 M64.987.9AdapterHr = 17.1 M71.989.8r = 4

**********段落分割**********
304.4 M72.691.5LoRArv = 24.7 M73.491.7rq = rv = 14.7 M73.491.3rq = rv = 29.4 M73.391.4rq = rk = rv = ro = 19.4 M74.191.2rq = rv = 4
段落总结：304.4 M72.691.5LoRArv = 24.7 M73.491.7rq = rv = 14.7 M73.491.3rq = rv = 29.4 M73.391.4rq = rk = rv =

**********段落分割**********
18.8 M73.791.3rq = rk = rv = ro = 2
段落总结：18.8 M73.791.3rq = rk = rv = ro = 2

**********段落分割**********
18.8 M73.791.7rq = rv = 8
段落总结：18.8 M73.791.7rq = rv = 8

**********段落分割**********
37.7 M73.891.6rq = rk = rv = ro = 4
段落总结：37.7 M73.891.6rq = rk = rv = ro = 4

**********段落分割**********
37.7 M74.091.7rq = rv = 64
段落总结：37.7 M74.091.7rq = rv = 64

**********段落分割**********
301.9 M73.691.4rq = rk = rv = ro = 64
段落总结：301.9 M73.691.4rq = rk = rv = ro = 64

**********段落分割**********
603.8 M73.991.4LoRA+PErq = rv = 8, lp = 8, li = 4
段落总结：603.8 M73.991.4LoRA+PErq = rv = 8, lp = 8, li = 4

**********段落分割**********
37.8 M75.091.4rq = rv = 32, lp = 8, li = 4
段落总结：37.8 M75.091.4rq = rv = 32, lp = 8, li = 4

**********段落分割**********
151.1 M75.991.1rq = rv = 64, lp = 8, li = 4
段落总结：151.1 M75.991.1rq = rv = 64, lp = 8, li = 4

**********段落分割**********
302.1 M76.291.3LoRA+PLrq = rv = 8, lp = 8, li = 4
段落总结：302.1 M76.291.3LoRA+PLrq = rv = 8, lp = 8, li = 4

**********段落分割**********
52.8 M72.990.2Table 15: Hyperparameter analysis of different adaptation approaches on WikiSQL and MNLI. Bothpreﬁx-embedding tuning (PreﬁxEmbed) and preﬁx-layer tuning (PreﬁxLayer) perform worse as weincrease the number of trainable parameters, while LoRA’s performance stabilizes. Performance ismeasured in validation accuracy.MethodMNLI(m)-100MNLI(m)-1kMNLI(m)-10kMNLI(m)-392KGPT-3 (Fine-Tune)60.285.888.989.5GPT-3 (PreﬁxEmbed)37.675.279.588.6GPT-3 (PreﬁxLayer)48.382.585.989.6GPT-3 (LoRA)63.885.689.291.7Table 16: Validation accuracy of different methods on subsets of MNLI using GPT-3 175B. MNLI-n describes a subset with n training examples. We evaluate with the full validation set. LoRAperforms exhibits favorable sample-efﬁciency compared to other methods, including ﬁne-tuning.To be concrete, let the singular values of U i⊤A U jB to be σ1, σ2, · · · , σp where p = min{i, j}. Weknow that the Projection Metric Ham & Lee (2008) is deﬁned as:d(U iA, U jB) =vuutp −pXi=1σ2i ∈[0, √p]23
段落总结：52.8 M72.990.2Table 15: Hyperparameter analysis of different adaptation approaches on WikiSQL and MN

**********段落分割**********
[52.8 M]HyperparametersAdaptation
段落总结：[52.8 M]HyperparametersAdaptation

**********段落分割**********
MNLI-392KOptimizer-AdamWWarmup Tokens-250,000LR Schedule-LinearBatch Size-2020100128
段落总结：MNLI-392KOptimizer-AdamWWarmup Tokens-250,000LR Schedule-LinearBatch Size-2020100128

**********段落分割**********
# Epoch-404042Learning RateFineTune
段落总结：# Epoch-404042Learning RateFineTune

**********段落分割**********
2.00E-4PreﬁxEmbed lp163264256Adaptation-PreﬁxEmbed li8SpeciﬁcPreﬁxTunelp = li = 8LoRArq = rv = 8Table 17: The hyperparameters used for different GPT-3 adaptation methods on MNLI(m)-n.where our similarity is deﬁned as:φ(A, B, i, j) = ψ(U iA, U jB) =Ppi=1 σ2ip= 1p1 −d(U iA, U jB)2This similarity satisﬁes that if U iA and U jB share the same column span, then φ(A, B, i, j) = 1. Ifthey are completely orthogonal, then φ(A, B, i, j) = 0. Otherwise, φ(A, B, i, j) ∈(0, 1).H
段落总结：2.00E-4PreﬁxEmbed lp163264256Adaptation-PreﬁxEmbed li8SpeciﬁcPreﬁxTunelp = li = 8LoRArq = rv = 8Tabl

**********段落分割**********
ADDITIONAL EXPERIMENTS ON LOW-RANK MATRICESWe present additional results from our investigation into the low-rank update matrices.H.1
段落总结：ADDITIONAL EXPERIMENTS ON LOW-RANK MATRICESWe present additional results from our investigation into

**********段落分割**********
CORRELATION BETWEEN LORA MODULESSee Figure 6 and Figure 7 for how the results presented in Figure 3 and Figure 4 generalize to otherlayers.H.2EFFECT OF r ON GPT-2We repeat our experiment on the effect of r (Section 7.2) in GPT-2. Using the E2E NLG Challengedataset as an example, we report the validation loss and test metrics achieved by different choicesof r after training for 26,000 steps. We present our result in Table 18. The optimal rank for GPT-2Medium is between 4 and 16 depending on the metric used, which is similar to that for GPT-3 175B.Note that the relationship between model size and the optimal rank for adaptation is still an openquestion.H.3
段落总结：CORRELATION BETWEEN LORA MODULESSee Figure 6 and Figure 7 for how the results presented in Figure 3 

**********段落分割**********
CORRELATION BETWEEN W AND ∆WSee Figure 8 for the normalized subspace similarity between W and ∆W with varying r.Note again that ∆W does not contain the top singular directions of W, since the similarity betweenthe top 4 directions in ∆W and the top-10% of those in W barely exceeds 0.2. This gives evidencethat ∆W contains those “task-speciﬁc” directions that are otherwise not emphasized in W.An interesting next question to answer, is how “strong” do we need to amplify those task-speciﬁcdirections, in order for the model adaptation to work well?24
段落总结：CORRELATION BETWEEN W AND ∆WSee Figure 8 for the normalized subspace similarity between W and ∆W wit

**********段落分割**********
[CORRELATION BETWEEN W AND ∆W]0.00.20.40.60.81.012345678Layer 1iWqWvWqWv12345678Layer 32i12345678Layer 64i16121823293540465258j12345678Layer 96i16121823293540465258j12345678j12345678j(Ar = 8, Ar = 64, i, j)Figure 6: Normalized subspace similarity between the column vectors of Ar=8 and Ar=64 for both∆Wq and ∆Wv from the 1st, 32nd, 64th, and 96th layers in a 96-layer Transformer.H.4
段落总结：[CORRELATION BETWEEN W AND ∆W]0

**********段落分割**********
AMPLIFICATION FACTOROne can naturally consider a feature ampliﬁcation factor as the ratio
段落总结：AMPLIFICATION FACTOROne can naturally consider a feature ampliﬁcation factor as the ratio

**********段落分割**********
∥∆W ∥F∥U ⊤W V ⊤∥F , where U and Vare the left- and right-singular matrices of the SVD decomposition of ∆W. (Recall UU ⊤WV ⊤Vgives the “projection” of W onto the subspace spanned by ∆W.)Intuitively, when ∆W mostly contains task-speciﬁc directions, this quantity measures how much ofthem are ampliﬁed by ∆W. As shown in Section 7.3, for r = 4, this ampliﬁcation factor is as largeas 20. In other words, there are (generally speaking) four feature directions in each layer (out of theentire feature space from the pre-trained model W), that need to be ampliﬁed by a very large factor20, in order to achieve our reported accuracy for the downstream speciﬁc task. And, one shouldexpect a very different set of feature directions to be ampliﬁed for each different downstream task.One may notice, however, for r = 64, this ampliﬁcation factor is only around 2, meaning thatmost directions learned in ∆W with r = 64 are not being ampliﬁed by much. This should notbe surprising, and in fact gives evidence (once again) that the intrinsic rank needed to representthe “task-speciﬁc directions” (thus for model adaptation) is low. In contrast, those directions in therank-4 version of ∆W (corresponding to r = 4) are ampliﬁed by a much larger factor 20.25
段落总结：∥∆W ∥F∥U ⊤W V ⊤∥F , where U and Vare the left- and right-singular matrices of the SVD decomposition 

**********段落分割**********
[∥∆W ∥F]0.00.10.20.30.40.50.60.70.817131925313743495561Layer 1iWqWvLayer 32WqWv161116212631364146515661j17131925313743495561Layer 64i161116212631364146515661j161116212631364146515661jLayer 96161116212631364146515661j(Ar = 64, A′r = 64, i, j)Figure 7: Normalized subspace similarity between the column vectors of Ar=64 from two randomlyseeded runs, for both ∆Wq and ∆Wv from the 1st, 32nd, 64th, and 96th layers in a 96-layer Trans-former.Rank rval lossBLEUNIST
段落总结：[∥∆W ∥F]0.00.10.20.30.40.50.60.70.817131925313743495561Layer 1iWqWvLayer 32WqWv161116212631364146515

**********段落分割**********
ROUGE LCIDEr11.2368.728.72150.45650.70522.432921.2169.178.74130.45900.70522.463941.1870.388.84390.46890.71862.534981.1769.578.74570.46360.71962.5196161.1669.618.74830.46290.71772.4985321.1669.338.77360.46420.71052.5255641.1669.248.71740.46510.71802.50701281.1668.738.67180.46280.71272.50302561.1668.928.69820.46290.71282.50125121.1668.788.68570.46370.71282.502510241.1769.378.74950.46590.71492.5090Table 18: Validation loss and test set metrics on E2E NLG Challenge achieved by LoRA withdifferent rank r using GPT-2 Medium. Unlike on GPT-3 where r = 1 sufﬁces for many tasks, herethe performance peaks at r = 16 for validation loss and r = 4 for BLEU, suggesting the GPT-2Medium has a similar intrinsic rank for adaptation compared to GPT-3 175B. Note that some of ourhyperparameters are tuned on r = 4, which matches the parameter count of another baseline, andthus might not be optimal for other choices of r.0.1000.1250.1500.1750.200j45155565876286596910721176i(Wq, Ar = 4, i, j)jWq(Wq, Ar = 8, i, j)j(Wq, Ar = 64, i, j)jRandom(Wq, Arand, i, j)Figure 8: Normalized subspace similarity between the singular directions of Wq and those of ∆Wqwith varying r and a random baseline. ∆Wq ampliﬁes directions that are important but not empha-sized in W. ∆W with a larger r tends to pick up more directions that are already emphasized inW.26
段落总结：ROUGE LCIDEr11.2368.728.72150.45650.70522.432921.2169.178.74130.45900.70522.463941.1870.388.84390.46
