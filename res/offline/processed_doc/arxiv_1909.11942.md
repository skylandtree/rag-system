Published as a conference paper at ICLR 2020
段落总结：Published as a conference paper at ICLR 2020

**********段落分割**********
LEARNING OF LANGUAGE REPRESENTATIONSZhenzhong Lan1Mingda Chen2∗Sebastian Goodman1Kevin Gimpel2Piyush Sharma1Radu Soricut11Google Research2Toyota Technological Institute at Chicago{lanzhzh, seabass, piyushsharma, rsoricut}@google.com{mchen, kgimpel}@ttic.edu
段落总结：LEARNING OF LANGUAGE REPRESENTATIONSZhenzhong Lan1Mingda Chen2∗Sebastian Goodman1Kevin Gimpel2Piyush

**********段落分割**********
ABSTRACTIncreasing model size when pretraining natural language representations often re-sults in improved performance on downstream tasks. However, at some point fur-ther model increases become harder due to GPU/TPU memory limitations andlonger training times. To address these problems, we present two parameter-reduction techniques to lower memory consumption and increase the trainingspeed of BERT (Devlin et al., 2019). Comprehensive empirical evidence showsthat our proposed methods lead to models that scale much better compared tothe original BERT. We also use a self-supervised loss that focuses on modelinginter-sentence coherence, and show it consistently helps downstream tasks withmulti-sentence inputs. As a result, our best model establishes new state-of-the-artresults on the GLUE, RACE, and SQuAD benchmarks while having fewer param-eters compared to BERT-large. The code and the pretrained models are availableat https://github.com/google-research/ALBERT.1
段落总结：ABSTRACTIncreasing model size when pretraining natural language representations often re-sults in im

**********段落分割**********
INTRODUCTIONFull network pre-training (Dai & Le, 2015; Radford et al., 2018; Devlin et al., 2019; Howard &Ruder, 2018) has led to a series of breakthroughs in language representation learning. Many non-trivial NLP tasks, including those that have limited training data, have greatly beneﬁted from thesepre-trained models. One of the most compelling signs of these breakthroughs is the evolution of ma-chine performance on a reading comprehension task designed for middle and high-school Englishexams in China, the RACE test (Lai et al., 2017): the paper that originally describes the task and for-mulates the modeling challenge reports then state-of-the-art machine accuracy at 44.1%; the latestpublished result reports their model performance at 83.2% (Liu et al., 2019); the work we presenthere pushes it even higher to 89.4%, a stunning 45.3% improvement that is mainly attributable toour current ability to build high-performance pretrained language representations.Evidence from these improvements reveals that a large network is of crucial importance for achiev-ing state-of-the-art performance (Devlin et al., 2019; Radford et al., 2019). It has become commonpractice to pre-train large models and distill them down to smaller ones (Sun et al., 2019; Turc et al.,2019) for real applications. Given the importance of model size, we ask: Is having better NLPmodels as easy as having larger models?An obstacle to answering this question is the memory limitations of available hardware.
段落总结：INTRODUCTIONFull network pre-training (Dai & Le, 2015; Radford et al

**********段落分割**********
Given thatcurrent state-of-the-art models often have hundreds of millions or even billions of parameters, it iseasy to hit these limitations as we try to scale our models. Training speed can also be signiﬁcantlyhampered in distributed training, as the communication overhead is directly proportional to thenumber of parameters in the model.Existing solutions to the aforementioned problems include model parallelization (Shazeer et al.,2018; Shoeybi et al., 2019) and clever memory management (Chen et al., 2016; Gomez et al., 2017).∗Work done as an intern at Google Research, driving data processing and downstream task evaluations.1arXiv:1909.11942v6  [cs.CL]  9 Feb 2020
段落总结：Given thatcurrent state-of-the-art models often have hundreds of millions or even billions of parame

**********段落分割**********
[INTRODUCTION]Published as a conference paper at ICLR 2020These solutions address the memory limitation problem, but not the communication overhead. Inthis paper, we address all of the aforementioned problems, by designing A Lite BERT (ALBERT)architecture that has signiﬁcantly fewer parameters than a traditional BERT architecture.ALBERT incorporates two parameter reduction techniques that lift the major obstacles in scalingpre-trained models. The ﬁrst one is a factorized embedding parameterization. By decomposingthe large vocabulary embedding matrix into two small matrices, we separate the size of the hiddenlayers from the size of vocabulary embedding. This separation makes it easier to grow the hiddensize without signiﬁcantly increasing the parameter size of the vocabulary embeddings. The secondtechnique is cross-layer parameter sharing. This technique prevents the parameter from growingwith the depth of the network. Both techniques signiﬁcantly reduce the number of parameters forBERT without seriously hurting performance, thus improving parameter-efﬁciency. An ALBERTconﬁguration similar to BERT-large has 18x fewer parameters and can be trained about 1.7x faster.The parameter reduction techniques also act as a form of regularization that stabilizes the trainingand helps with generalization.To further improve the performance of ALBERT, we also introduce a self-supervised loss forsentence-order prediction (SOP).
段落总结：[INTRODUCTION]Published as a conference paper at ICLR 2020These solutions address the memory limitat

**********段落分割**********
SOP primary focuses on inter-sentence coherence and is designedto address the ineffectiveness (Yang et al., 2019; Liu et al., 2019) of the next sentence prediction(NSP) loss proposed in the original BERT.As a result of these design decisions, we are able to scale up to much larger ALBERT conﬁgurationsthat still have fewer parameters than BERT-large but achieve signiﬁcantly better performance. Weestablish new state-of-the-art results on the well-known GLUE, SQuAD, and RACE benchmarksfor natural language understanding. Speciﬁcally, we push the RACE accuracy to 89.4%, the GLUEbenchmark to 89.4, and the F1 score of SQuAD 2.0 to 92.2.2
段落总结：SOP primary focuses on inter-sentence coherence and is designedto address the ineffectiveness (Yang 

**********段落分割**********
SCALING UP REPRESENTATION LEARNING FOR NATURAL LANGUAGELearning representations of natural language has been shown to be useful for a wide range of NLPtasks and has been widely adopted (Mikolov et al., 2013; Le & Mikolov, 2014; Dai & Le, 2015; Pe-ters et al., 2018; Devlin et al., 2019; Radford et al., 2018; 2019). One of the most signiﬁcant changesin the last two years is the shift from pre-training word embeddings, whether standard (Mikolovet al., 2013; Pennington et al., 2014) or contextualized (McCann et al., 2017; Peters et al., 2018),to full-network pre-training followed by task-speciﬁc ﬁne-tuning (Dai & Le, 2015; Radford et al.,2018; Devlin et al., 2019). In this line of work, it is often shown that larger model size improvesperformance. For example, Devlin et al. (2019) show that across three selected natural languageunderstanding tasks, using larger hidden size, more hidden layers, and more attention heads alwaysleads to better performance. However, they stop at a hidden size of 1024, presumably because of themodel size and computation cost problems.It is difﬁcult to experiment with large models due to computational constraints, especially in termsof GPU/TPU memory limitations. Given that current state-of-the-art models often have hundreds ofmillions or even billions of parameters, we can easily hit memory limits. To address this issue, Chenet al.
段落总结：SCALING UP REPRESENTATION LEARNING FOR NATURAL LANGUAGELearning representations of natural language 

**********段落分割**********
(2016) propose a method called gradient checkpointing to reduce the memory requirement to besublinear at the cost of an extra forward pass. Gomez et al. (2017) propose a way to reconstruct eachlayer’s activations from the next layer so that they do not need to store the intermediate activations.Both methods reduce the memory consumption at the cost of speed. Raffel et al. (2019) proposedto use model parallelization to train a giant model. In contrast, our parameter-reduction techniquesreduce memory consumption and increase training speed.2.2
段落总结：(2016) propose a method called gradient checkpointing to reduce the memory requirement to besublinea

**********段落分割**********
CROSS-LAYER PARAMETER SHARINGThe idea of sharing parameters across layers has been previously explored with the Transformerarchitecture (Vaswani et al., 2017), but this prior work has focused on training for standard encoder-decoder tasks rather than the pretraining/ﬁnetuning setting. Different from our observations, De-hghani et al. (2018) show that networks with cross-layer parameter sharing (Universal Transformer,UT) get better performance on language modeling and subject-verb agreement than the standard2
段落总结：CROSS-LAYER PARAMETER SHARINGThe idea of sharing parameters across layers has been previously explor

**********段落分割**********
[CROSS-LAYER PARAMETER SHARING]Published as a conference paper at ICLR 2020transformer. Very recently, Bai et al. (2019) propose a Deep Equilibrium Model (DQE) for trans-former networks and show that DQE can reach an equilibrium point for which the input embeddingand the output embedding of a certain layer stay the same. Our observations show that our em-beddings are oscillating rather than converging. Hao et al. (2019) combine a parameter-sharingtransformer with the standard one, which further increases the number of parameters of the standardtransformer.2.3
段落总结：[CROSS-LAYER PARAMETER SHARING]Published as a conference paper at ICLR 2020transformer

**********段落分割**********
SENTENCE ORDERING OBJECTIVESALBERT uses a pretraining loss based on predicting the ordering of two consecutive segmentsof text. Several researchers have experimented with pretraining objectives that similarly relate todiscourse coherence. Coherence and cohesion in discourse have been widely studied and manyphenomena have been identiﬁed that connect neighboring text segments (Hobbs, 1979; Halliday &Hasan, 1976; Grosz et al., 1995). Most objectives found effective in practice are quite simple. Skip-thought (Kiros et al., 2015) and FastSent (Hill et al., 2016) sentence embeddings are learned by usingan encoding of a sentence to predict words in neighboring sentences. Other objectives for sentenceembedding learning include predicting future sentences rather than only neighbors (Gan et al., 2017)and predicting explicit discourse markers (Jernite et al., 2017; Nie et al., 2019). Our loss is mostsimilar to the sentence ordering objective of Jernite et al. (2017), where sentence embeddings arelearned in order to determine the ordering of two consecutive sentences. Unlike most of the abovework, however, our loss is deﬁned on textual segments rather than sentences. BERT (Devlin et al.,2019) uses a loss based on predicting whether the second segment in a pair has been swappedwith a segment from another document. We compare to this loss in our experiments and ﬁnd thatsentence ordering is a more challenging pretraining task and more useful for certain downstreamtasks.
段落总结：SENTENCE ORDERING OBJECTIVESALBERT uses a pretraining loss based on predicting the ordering of two c

**********段落分割**********
Concurrently to our work, Wang et al. (2019) also try to predict the order of two consecutivesegments of text, but they combine it with the original next sentence prediction in a three-wayclassiﬁcation task rather than empirically comparing the two.3
段落总结：Concurrently to our work, Wang et al

**********段落分割**********
THE ELEMENTS OF ALBERTIn this section, we present the design decisions for ALBERT and provide quantiﬁed comparisonsagainst corresponding conﬁgurations of the original BERT architecture (Devlin et al., 2019).3.1
段落总结：THE ELEMENTS OF ALBERTIn this section, we present the design decisions for ALBERT and provide quanti

**********段落分割**********
MODEL ARCHITECTURE CHOICESThe backbone of the ALBERT architecture is similar to BERT in that it uses a transformer en-coder (Vaswani et al., 2017) with GELU nonlinearities (Hendrycks & Gimpel, 2016). We follow theBERT notation conventions and denote the vocabulary embedding size as E, the number of encoderlayers as L, and the hidden size as H. Following Devlin et al. (2019), we set the feed-forward/ﬁltersize to be 4H and the number of attention heads to be H/64.There are three main contributions that ALBERT makes over the design choices of BERT.Factorized embedding parameterization.In BERT, as well as subsequent modeling improve-ments such as XLNet (Yang et al., 2019) and RoBERTa (Liu et al., 2019), the WordPiece embeddingsize E is tied with the hidden layer size H, i.e., E ≡H. This decision appears suboptimal for bothmodeling and practical reasons, as follows.From a modeling perspective, WordPiece embeddings are meant to learn context-independent repre-sentations, whereas hidden-layer embeddings are meant to learn context-dependent representations.As experiments with context length indicate (Liu et al., 2019), the power of BERT-like represen-tations comes from the use of context to provide the signal for learning such context-dependentrepresentations.
段落总结：MODEL ARCHITECTURE CHOICESThe backbone of the ALBERT architecture is similar to BERT in that it uses

**********段落分割**********
As such, untying the WordPiece embedding size E from the hidden layer size Hallows us to make a more efﬁcient usage of the total model parameters as informed by modelingneeds, which dictate that H ≫E.From a practical perspective, natural language processing usually require the vocabulary size V tobe large.1 If E ≡H, then increasing H increases the size of the embedding matrix, which has size1Similar to BERT, all the experiments in this paper use a vocabulary size V of 30,000.3
段落总结：As such, untying the WordPiece embedding size E from the hidden layer size Hallows us to make a more

**********段落分割**********
[MODEL ARCHITECTURE CHOICES]Published as a conference paper at ICLR 2020V ×E. This can easily result in a model with billions of parameters, most of which are only updatedsparsely during training.Therefore, for ALBERT we use a factorization of the embedding parameters, decomposing theminto two smaller matrices. Instead of projecting the one-hot vectors directly into the hidden space ofsize H, we ﬁrst project them into a lower dimensional embedding space of size E, and then projectit to the hidden space. By using this decomposition, we reduce the embedding parameters fromO(V × H) to O(V × E + E × H). This parameter reduction is signiﬁcant when H ≫E. Wechoose to use the same E for all word pieces because they are much more evenly distributed acrossdocuments compared to whole-word embedding, where having different embedding size (Graveet al. (2017); Baevski & Auli (2018); Dai et al. (2019) ) for different words is important.Cross-layer parameter sharing.For ALBERT, we propose cross-layer parameter sharing as an-other way to improve parameter efﬁciency. There are multiple ways to share parameters, e.g., onlysharing feed-forward network (FFN) parameters across layers, or only sharing attention parameters.The default decision for ALBERT is to share all parameters across layers. All our experimentsuse this default decision unless otherwise speciﬁed. We compare this design decision against otherstrategies in our experiments in Sec.
段落总结：[MODEL ARCHITECTURE CHOICES]Published as a conference paper at ICLR 2020V ×E

**********段落分割**********
4.5.Similar strategies have been explored by Dehghani et al. (2018) (Universal Transformer, UT) andBai et al. (2019) (Deep Equilibrium Models, DQE) for Transformer networks. Different from ourobservations, Dehghani et al. (2018) show that UT outperforms a vanilla Transformer. Bai et al.(2019) show that their DQEs reach an equilibrium point for which the input and output embeddingof a certain layer stay the same. Our measurement on the L2 distances and cosine similarity showthat our embeddings are oscillating rather than converging.0510152025Layer ID024681012141618L2 distanceBERT-largeALBERT-large0510152025Layer ID051015202530354045Cosine Similarity (Degree)BERT-largeALBERT-largeFigure 1: The L2 distances and cosine similarity (in terms of degree) of the input and output embed-ding of each layer for BERT-large and ALBERT-large.Figure 1 shows the L2 distances and cosine similarity of the input and output embeddings for eachlayer, using BERT-large and ALBERT-large conﬁgurations (see Table 1). We observe that the tran-sitions from layer to layer are much smoother for ALBERT than for BERT. These results show thatweight-sharing has an effect on stabilizing network parameters. Although there is a drop for bothmetrics compared to BERT, they nevertheless do not converge to 0 even after 24 layers.
段落总结：4.5.Similar strategies have been explored by Dehghani et al. (2018) (Universal Transformer, UT) andB

**********段落分割**********
This showsthat the solution space for ALBERT parameters is very different from the one found by DQE.Inter-sentence coherence loss.In addition to the masked language modeling (MLM) loss (De-vlin et al., 2019), BERT uses an additional loss called next-sentence prediction (NSP). NSP is abinary classiﬁcation loss for predicting whether two segments appear consecutively in the originaltext, as follows: positive examples are created by taking consecutive segments from the trainingcorpus; negative examples are created by pairing segments from different documents; positive andnegative examples are sampled with equal probability. The NSP objective was designed to improveperformance on downstream tasks, such as natural language inference, that require reasoning aboutthe relationship between sentence pairs. However, subsequent studies (Yang et al., 2019; Liu et al.,2019) found NSP’s impact unreliable and decided to eliminate it, a decision supported by an im-provement in downstream task performance across several tasks.We conjecture that the main reason behind NSP’s ineffectiveness is its lack of difﬁculty as a task,as compared to MLM. As formulated, NSP conﬂates topic prediction and coherence prediction in a4
段落总结：This showsthat the solution space for ALBERT parameters is very different from the one found by DQE

**********段落分割**********
Published as a conference paper at ICLR 2020ModelParametersLayersHiddenEmbeddingParameter-sharingBERTbase108M12768768Falselarge334M2410241024False
段落总结：Published as a conference paper at ICLR 2020ModelParametersLayersHiddenEmbeddingParameter-sharingBER

**********段落分割**********
ALBERTbase12M12768128Truelarge18M241024128Truexlarge60M242048128Truexxlarge235M124096128TrueTable 1: The conﬁgurations of the main BERT and ALBERT models analyzed in this paper.single task2. However, topic prediction is easier to learn compared to coherence prediction, and alsooverlaps more with what is learned using the MLM loss.We maintain that inter-sentence modeling is an important aspect of language understanding, but wepropose a loss based primarily on coherence. That is, for ALBERT, we use a sentence-order pre-diction (SOP) loss, which avoids topic prediction and instead focuses on modeling inter-sentencecoherence. The SOP loss uses as positive examples the same technique as BERT (two consecu-tive segments from the same document), and as negative examples the same two consecutive seg-ments but with their order swapped. This forces the model to learn ﬁner-grained distinctions aboutdiscourse-level coherence properties. As we show in Sec. 4.6, it turns out that NSP cannot solve theSOP task at all (i.e., it ends up learning the easier topic-prediction signal, and performs at random-baseline level on the SOP task), while SOP can solve the NSP task to a reasonable degree, pre-sumably based on analyzing misaligned coherence cues. As a result, ALBERT models consistentlyimprove downstream task performance for multi-sentence encoding tasks.3.2
段落总结：ALBERTbase12M12768128Truelarge18M241024128Truexlarge60M242048128Truexxlarge235M124096128TrueTable 1:

**********段落分割**********
MODEL SETUPWe present the differences between BERT and ALBERT models with comparable hyperparametersettings in Table 1. Due to the design choices discussed above, ALBERT models have much smallerparameter size compared to corresponding BERT models.For example, ALBERT-large has about 18x fewer parameters compared to BERT-large, 18M ver-sus 334M. An ALBERT-xlarge conﬁguration with H = 2048 has only 60M parameters and anALBERT-xxlarge conﬁguration with H = 4096 has 233M parameters, i.e., around 70% of BERT-large’s parameters. Note that for ALBERT-xxlarge, we mainly report results on a 12-layer networkbecause a 24-layer network (with the same conﬁguration) obtains similar results but is computation-ally more expensive.This improvement in parameter efﬁciency is the most important advantage of ALBERT’s designchoices. Before we can quantify this advantage, we need to introduce our experimental setup inmore detail.4
段落总结：MODEL SETUPWe present the differences between BERT and ALBERT models with comparable hyperparameters

**********段落分割**********
EXPERIMENTAL RESULTS4.1
段落总结：EXPERIMENTAL RESULTS4

**********段落分割**********
EXPERIMENTAL SETUPTo keep the comparison as meaningful as possible, we follow the BERT (Devlin et al., 2019) setup inusing the BOOKCORPUS (Zhu et al., 2015) and English Wikipedia (Devlin et al., 2019) for pretrain-ing baseline models. These two corpora consist of around 16GB of uncompressed text. We formatour inputs as “[CLS] x1 [SEP] x2 [SEP]”, where x1 = x1,1, x1,2 · · · and x2 = x1,1, x1,2 · · · aretwo segments.3 We always limit the maximum input length to 512, and randomly generate inputsequences shorter than 512 with a probability of 10%. Like BERT, we use a vocabulary size of30,000, tokenized using SentencePiece (Kudo & Richardson, 2018) as in XLNet (Yang et al., 2019).2Since a negative example is constructed using material from a different document, the negative-examplesegment is misaligned both from a topic and from a coherence perspective.3A segment is usually comprised of more than one natural sentence, which has been shown to beneﬁtperformance by Liu et al. (2019).5
段落总结：EXPERIMENTAL SETUPTo keep the comparison as meaningful as possible, we follow the BERT (Devlin et al

**********段落分割**********
[EXPERIMENTAL SETUP]Published as a conference paper at ICLR 2020We generate masked inputs for the MLM targets using n-gram masking (Joshi et al., 2019), with thelength of each n-gram mask selected randomly. The probability for the length n is given byp(n) =1/nPNk=1 1/kWe set the maximum length of n-gram (i.e., n) to be 3 (i.e., the MLM target can consist of up to a3-gram of complete words, such as “White House correspondents”).All the model updates use a batch size of 4096 and a LAMB optimizer with learning rate0.00176 (You et al., 2019). We train all models for 125,000 steps unless otherwise speciﬁed. Train-ing was done on Cloud TPU V3. The number of TPUs used for training ranged from 64 to 512,depending on model size.The experimental setup described in this section is used for all of our own versions of BERT as wellas ALBERT models, unless otherwise speciﬁed.4.2
段落总结：[EXPERIMENTAL SETUP]Published as a conference paper at ICLR 2020We generate masked inputs for the ML

**********段落分割**********
EVALUATION BENCHMARKS4.2.1
段落总结：EVALUATION BENCHMARKS4

**********段落分割**********
INTRINSIC EVALUATIONTo monitor the training progress, we create a development set based on the development sets fromSQuAD and RACE using the same procedure as in Sec. 4.1. We report accuracies for both MLM andsentence classiﬁcation tasks. Note that we only use this set to check how the model is converging;it has not been used in a way that would affect the performance of any downstream evaluation, suchas via model selection.4.2.2
段落总结：INTRINSIC EVALUATIONTo monitor the training progress, we create a development set based on the devel

**********段落分割**********
DOWNSTREAM EVALUATIONFollowing Yang et al. (2019) and Liu et al. (2019), we evaluate our models on three popular bench-marks: The General Language Understanding Evaluation (GLUE) benchmark (Wang et al., 2018),two versions of the Stanford Question Answering Dataset (SQuAD; Rajpurkar et al., 2016; 2018),and the ReAding Comprehension from Examinations (RACE) dataset (Lai et al., 2017). For com-pleteness, we provide description of these benchmarks in Appendix A.3. As in (Liu et al., 2019),we perform early stopping on the development sets, on which we report all comparisons except forour ﬁnal comparisons based on the task leaderboards, for which we also report test set results. ForGLUE datasets that have large variances on the dev set, we report median over 5 runs.4.3
段落总结：DOWNSTREAM EVALUATIONFollowing Yang et al

**********段落分割**********
OVERALL COMPARISON BETWEEN BERT AND ALBERTWe are now ready to quantify the impact of the design choices described in Sec. 3, speciﬁcally theones around parameter efﬁciency. The improvement in parameter efﬁciency showcases the mostimportant advantage of ALBERT’s design choices, as shown in Table 2: with only around 70% ofBERT-large’s parameters, ALBERT-xxlarge achieves signiﬁcant improvements over BERT-large, asmeasured by the difference on development set scores for several representative downstream tasks:SQuAD v1.1 (+1.9%), SQuAD v2.0 (+3.1%), MNLI (+1.4%), SST-2 (+2.2%), and RACE (+8.4%).Another interesting observation is the speed of data throughput at training time under the same train-ing conﬁguration (same number of TPUs). Because of less communication and fewer computations,ALBERT models have higher data throughput compared to their corresponding BERT models. If weuse BERT-large as the baseline, we observe that ALBERT-large is about 1.7 times faster in iteratingthrough the data while ALBERT-xxlarge is about 3 times slower because of the larger structure.Next, we perform ablation experiments that quantify the individual contribution of each of the designchoices for ALBERT.4.4
段落总结：OVERALL COMPARISON BETWEEN BERT AND ALBERTWe are now ready to quantify the impact of the design choi

**********段落分割**********
FACTORIZED EMBEDDING PARAMETERIZATIONTable 3 shows the effect of changing the vocabulary embedding size E using an ALBERT-baseconﬁguration setting (see Table 1), using the same set of representative downstream tasks. Underthe non-shared condition (BERT-style), larger embedding sizes give better performance, but not by6
段落总结：FACTORIZED EMBEDDING PARAMETERIZATIONTable 3 shows the effect of changing the vocabulary embedding s

**********段落分割**********
[FACTORIZED EMBEDDING PARAMETERIZATION]Published as a conference paper at ICLR 2020ModelParametersSQuAD1.1SQuAD2.0MNLISST-2RACEAvgSpeedupBERTbase108M90.4/83.280.4/77.684.592.868.282.34.7xlarge334M92.2/85.585.0/82.286.693.073.985.21.0
段落总结：[FACTORIZED EMBEDDING PARAMETERIZATION]Published as a conference paper at ICLR 2020ModelParametersSQ

**********段落分割**********
ALBERTbase12M89.3/82.380.0/77.181.690.364.080.15.6xlarge18M90.6/83.982.3/79.483.591.768.582.41.7xxlarge60M92.5/86.186.1/83.186.492.474.885.50.6xxxlarge235M94.1/88.388.1/85.188.095.282.388.70.3xTable 2: Dev set results for models pretrained over BOOKCORPUS and Wikipedia for 125k steps.Here and everywhere else, the Avg column is computed by averaging the scores of the downstreamtasks to its left (the two numbers of F1 and EM for each SQuAD are ﬁrst averaged).much. Under the all-shared condition (ALBERT-style), an embedding of size 128 appears to be thebest. Based on these results, we use an embedding size E = 128 in all future settings, as a necessarystep to do further scaling.ModelEParametersSQuAD1.1SQuAD2.0MNLISST-2RACEAvg
段落总结：ALBERTbase12M89.3/82.380.0/77.181.690.364.080.15.6xlarge18M90.6/83.982.3/79.483.591.768.582.41.7xxla

**********段落分割**********
ALBERTbasenot-shared6487M89.9/82.980.1/77.882.991.566.781.312889M89.9/82.880.3/77.383.791.567.981.725693M90.2/83.280.3/77.484.191.967.381.8768108M90.4/83.280.4/77.684.592.868.282.3
段落总结：ALBERTbasenot-shared6487M89

**********段落分割**********
ALBERTbaseall-shared6410M88.7/81.477.5/74.880.889.463.579.012812M89.3/82.380.0/77.181.690.364.080.125616M88.8/81.579.1/76.381.590.363.479.676831M88.6/81.579.2/76.682.090.663.379.8Table 3: The effect of vocabulary embedding size on the performance of ALBERT-base.4.5
段落总结：ALBERTbaseall-shared6410M88

**********段落分割**********
CROSS-LAYER PARAMETER SHARINGTable 4 presents experiments for various cross-layer parameter-sharing strategies, using anALBERT-base conﬁguration (Table 1) with two embedding sizes (E = 768 and E = 128). Wecompare the all-shared strategy (ALBERT-style), the not-shared strategy (BERT-style), and inter-mediate strategies in which only the attention parameters are shared (but not the FNN ones) or onlythe FFN parameters are shared (but not the attention ones).The all-shared strategy hurts performance under both conditions, but it is less severe for E = 128 (-1.5 on Avg) compared to E = 768 (-2.5 on Avg). In addition, most of the performance drop appearsto come from sharing the FFN-layer parameters, while sharing the attention parameters results in nodrop when E = 128 (+0.1 on Avg), and a slight drop when E = 768 (-0.7 on Avg).There are other strategies of sharing the parameters cross layers. For example, We can divide the Llayers into N groups of size M, and each size-M group shares parameters. Overall, our experimen-tal results shows that the smaller the group size M is, the better the performance we get. However,decreasing group size M also dramatically increase the number of overall parameters. We chooseall-shared strategy as our default choice.ModelParametersSQuAD1.1SQuAD2.0MNLISST-2RACEAvg
段落总结：CROSS-LAYER PARAMETER SHARINGTable 4 presents experiments for various cross-layer parameter-sharing 

**********段落分割**********
ALBERTbaseE=768all-shared31M88.6/81.579.2/76.682.090.663.379.8shared-attention83M89.9/82.780.0/77.284.091.467.781.6shared-FFN57M89.2/82.178.2/75.481.590.862.679.5not-shared108M90.4/83.280.4/77.684.592.868.282.3
段落总结：ALBERTbaseE=768all-shared31M88

**********段落分割**********
ALBERTbaseE=128all-shared12M89.3/82.380.0/77.182.090.364.080.1shared-attention64M89.9/82.880.7/77.983.491.967.681.7shared-FFN38M88.9/81.678.6/75.682.391.764.480.2not-shared89M89.9/82.880.3/77.383.291.567.981.6Table 4: The effect of cross-layer parameter-sharing strategies, ALBERT-base conﬁguration.7
段落总结：ALBERTbaseE=128all-shared12M89

**********段落分割**********
[ALBERT]Published as a conference paper at ICLR 20204.6
段落总结：[ALBERT]Published as a conference paper at ICLR 20204

**********段落分割**********
SENTENCE ORDER PREDICTION (SOP)We compare head-to-head three experimental conditions for the additional inter-sentence loss: none(XLNet- and RoBERTa-style), NSP (BERT-style), and SOP (ALBERT-style), using an ALBERT-base conﬁguration. Results are shown in Table 5, both over intrinsic (accuracy for the MLM, NSP,and SOP tasks) and downstream tasks.Intrinsic TasksDownstream TasksSP tasksMLMNSPSOPSQuAD1.1SQuAD2.0MNLISST-2RACEAvgNone54.952.453.388.6/81.578.1/75.381.589.961.779.0NSP54.590.552.088.4/81.577.2/74.681.691.162.379.2SOP54.078.986.589.3/82.380.0/77.182.090.364.080.1Table 5: The effect of sentence-prediction loss, NSP vs. SOP, on intrinsic and downstream tasks.The results on the intrinsic tasks reveal that the NSP loss brings no discriminative power to the SOPtask (52.0% accuracy, similar to the random-guess performance for the “None” condition). Thisallows us to conclude that NSP ends up modeling only topic shift. In contrast, the SOP loss doessolve the NSP task relatively well (78.9% accuracy), and the SOP task even better (86.5% accuracy).Even more importantly, the SOP loss appears to consistently improve downstream task performancefor multi-sentence encoding tasks (around +1% for SQuAD1.1, +2% for SQuAD2.0, +1.7% forRACE), for an Avg score improvement of around +1%.4.7WHAT IF WE TRAIN FOR THE SAME AMOUNT OF TIME?The speed-up results in Table 2 indicate that data-throughput for BERT-large is about 3.17x highercompared to ALBERT-xxlarge.
段落总结：SENTENCE ORDER PREDICTION (SOP)We compare head-to-head three experimental conditions for the additio

**********段落分割**********
Since longer training usually leads to better performance, we per-form a comparison in which, instead of controlling for data throughput (number of training steps),we control for the actual training time (i.e., let the models train for the same number of hours). InTable 6, we compare the performance of a BERT-large model after 400k training steps (after 34hof training), roughly equivalent with the amount of time needed to train an ALBERT-xxlarge modelwith 125k training steps (32h of training).ModelsStepsTimeSQuAD1.1SQuAD2.0MNLISST-2RACEAvgBERT-large400k34h93.5/87.486.9/84.387.894.677.387.2ALBERT-xxlarge125k32h94.0/88.188.3/85.387.895.482.588.7Table 6: The effect of controlling for training time, BERT-large vs ALBERT-xxlarge conﬁgurations.After training for roughly the same amount of time, ALBERT-xxlarge is signiﬁcantly better thanBERT-large: +1.5% better on Avg, with the difference on RACE as high as +5.2%.4.8
段落总结：Since longer training usually leads to better performance, we per-form a comparison in which, instea

**********段落分割**********
ADDITIONAL TRAINING DATA AND DROPOUT EFFECTSThe experiments done up to this point use only the Wikipedia and BOOKCORPUS datasets, as in(Devlin et al., 2019). In this section, we report measurements on the impact of the additional dataused by both XLNet (Yang et al., 2019) and RoBERTa (Liu et al., 2019).Fig. 2a plots the dev set MLM accuracy under two conditions, without and with additional data, withthe latter condition giving a signiﬁcant boost. We also observe performance improvements on thedownstream tasks in Table 7, except for the SQuAD benchmarks (which are Wikipedia-based, andtherefore are negatively affected by out-of-domain training material).SQuAD1.1SQuAD2.0MNLISST-2RACEAvgNo additional data89.3/82.380.0/77.181.690.364.080.1With additional data88.8/81.779.1/76.382.492.866.080.8Table 7: The effect of additional training data using the ALBERT-base conﬁguration.We also note that, even after training for 1M steps, our largest models still do not overﬁt to theirtraining data. As a result, we decide to remove dropout to further increase our model capacity. The8
段落总结：ADDITIONAL TRAINING DATA AND DROPOUT EFFECTSThe experiments done up to this point use only the Wikip

**********段落分割**********
[ADDITIONAL TRAINING DATA AND DROPOUT EFFECTS]Published as a conference paper at ICLR 20203540455055Steps (1e4)66.066.567.067.568.068.569.069.570.0Dev accuracy (MLM) %W/O additional dataW additional data(a) Adding data90100110120130140150Steps (1e4)70.070.571.071.572.072.5Dev accuracy (MLM) %W/ DropoutW/O Dropout(b) Removing dropoutFigure 2: The effects of adding data and removing dropout during training.plot in Fig. 2b shows that removing dropout signiﬁcantly improves MLM accuracy. Intermediateevaluation on ALBERT-xxlarge at around 1M training steps (Table 8) also conﬁrms that removingdropout helps the downstream tasks. There is empirical (Szegedy et al., 2017) and theoretical (Liet al., 2019) evidence showing that a combination of batch normalization and dropout in Convolu-tional Neural Networks may have harmful results. To the best of our knowledge, we are the ﬁrst toshow that dropout can hurt performance in large Transformer-based models. However, the underly-ing network structure of ALBERT is a special case of the transformer and further experimentationis needed to see if this phenomenon appears with other transformer-based architectures or not.SQuAD1.1SQuAD2.0MNLISST-2RACEAvgWith dropout94.7/89.289.6/86.990.096.385.790.4Without dropout94.8/89.589.9/87.290.496.586.190.7Table 8: The effect of removing dropout, measured for an ALBERT-xxlarge conﬁguration.4.9
段落总结：[ADDITIONAL TRAINING DATA AND DROPOUT EFFECTS]Published as a conference paper at ICLR 20203540455055

**********段落分割**********
CURRENT STATE-OF-THE-ART ON NLU TASKSThe results we report in this section make use of the training data used by Devlin et al. (2019), aswell as the additional data used by Liu et al. (2019) and Yang et al. (2019). We report state-of-the-artresults under two settings for ﬁne-tuning: single-model and ensembles. In both settings, we only dosingle-task ﬁne-tuning4. Following Liu et al. (2019), on the development set we report the medianresult over ﬁve runs.ModelsMNLIQNLIQQPRTESSTMRPCCoLASTSWNLIAvgSingle-task single models on devBERT-large86.692.391.370.493.288.060.690.0--XLNet-large89.893.991.883.895.689.263.691.8--RoBERTa-large90.294.792.286.696.490.968.092.4--
段落总结：CURRENT STATE-OF-THE-ART ON NLU TASKSThe results we report in this section make use of the training 

**********段落分割**********
ALBERT (1M)90.495.292.088.196.890.268.792.7--
段落总结：ALBERT (1M)90.495.292.088.196.890.268.792.7--

**********段落分割**********
ALBERT (1.5M)90.895.392.289.296.990.971.493.0--Ensembles on test (from leaderboard as of Sept. 16, 2019)ALICE88.295.790.783.595.292.669.291.180.887.0
段落总结：ALBERT (1.5M)90.895.392.289.296.990.971.493.0--Ensembles on test (from leaderboard as of Sept. 16, 2

**********段落分割**********
MT-DNN87.996.089.986.396.592.768.491.189.087.6XLNet90.298.690.386.396.893.067.891.690.488.4RoBERTa90.898.990.288.296.792.367.892.289.088.5Adv-RoBERTa91.198.890.388.796.893.168.092.489.088.8
段落总结：MT-DNN87.996.089.986.396.592.768.491.189.087.6XLNet90.298.690.386.396.893.067.891.690.488.4RoBERTa90

**********段落分割**********
ALBERT91.399.290.589.297.193.469.192.591.889.4Table 9: State-of-the-art results on the GLUE benchmark. For single-task single-model results, wereport ALBERT at 1M steps (comparable to RoBERTa) and at 1.5M steps. The ALBERT ensembleuses models trained with 1M, 1.5M, and other numbers of steps.The single-model ALBERT conﬁguration incorporates the best-performing settings discussed: anALBERT-xxlarge conﬁguration (Table 1) using combined MLM and SOP losses, and no dropout.4Following Liu et al. (2019), we ﬁne-tune for RTE, STS, and MRPC using an MNLI checkpoint.9
段落总结：ALBERT91.399.290.589.297.193.469.192.591.889.4Table 9: State-of-the-art results on the GLUE benchmar

**********段落分割**********
[ALBERT]Published as a conference paper at ICLR 2020The checkpoints that contribute to the ﬁnal ensemble model are selected based on development setperformance; the number of checkpoints considered for this selection range from 6 to 17, dependingon the task. For the GLUE (Table 9) and RACE (Table 10) benchmarks, we average the modelpredictions for the ensemble models, where the candidates are ﬁne-tuned from different trainingsteps using the 12-layer and 24-layer architectures. For SQuAD (Table 10), we average the pre-diction scores for those spans that have multiple probabilities; we also average the scores of the“unanswerable” decision.Both single-model and ensemble results indicate that ALBERT improves the state-of-the-art signif-icantly for all three benchmarks, achieving a GLUE score of 89.4, a SQuAD 2.0 test F1 score of92.2, and a RACE test accuracy of 89.4. The latter appears to be a particularly strong improvement,a jump of +17.4% absolute points over BERT (Devlin et al., 2019; Clark et al., 2019), +7.6% overXLNet (Yang et al., 2019), +6.2% over RoBERTa (Liu et al., 2019), and 5.3% over DCMI+ (Zhanget al., 2019), an ensemble of multiple models speciﬁcally designed for reading comprehension tasks.Our single model achieves an accuracy of 86.5%, which is still 2.4% better than the state-of-the-artensemble model.ModelsSQuAD1.1 devSQuAD2.0 devSQuAD2.0 testRACE test (Middle/High)Single model (from leaderboard as of Sept.
段落总结：[ALBERT]Published as a conference paper at ICLR 2020The checkpoints that contribute to the ﬁnal ense

**********段落分割**********
23, 2019)BERT-large90.9/84.181.8/79.089.1/86.372.0 (76.6/70.1)XLNet94.5/89.088.8/86.189.1/86.381.8 (85.5/80.2)RoBERTa94.6/88.989.4/86.589.8/86.883.2 (86.5/81.3)UPM--89.9/87.2-XLNet + SG-Net Veriﬁer++--90.1/87.2-
段落总结：23, 2019)BERT-large90

**********段落分割**********
ALBERT (1M)94.8/89.289.9/87.2-86.0 (88.2/85.1)
段落总结：ALBERT (1M)94.8/89.289.9/87.2-86.0 (88.2/85.1)

**********段落分割**********
ALBERT (1.5M)94.8/89.390.2/87.490.9/88.186.5 (89.0/85.5)Ensembles (from leaderboard as of Sept. 23, 2019)BERT-large92.2/86.2---XLNet + SG-Net Veriﬁer--90.7/88.2-UPM--90.7/88.2XLNet + DAAF + Veriﬁer--90.9/88.6-DCMN+---84.1 (88.5/82.3)
段落总结：ALBERT (1.5M)94.8/89.390.2/87.490.9/88.186.5 (89.0/85.5)Ensembles (from leaderboard as of Sept. 23, 

**********段落分割**********
ALBERT95.5/90.191.4/88.992.2/89.789.4 (91.2/88.6)Table 10: State-of-the-art results on the SQuAD and RACE benchmarks.5
段落总结：ALBERT95.5/90.191.4/88.992.2/89.789.4 (91.2/88.6)Table 10: State-of-the-art results on the SQuAD and

**********段落分割**********
DISCUSSIONWhile ALBERT-xxlarge has less parameters than BERT-large and gets signiﬁcantly better results, itis computationally more expensive due to its larger structure. An important next step is thus to speedup the training and inference speed of ALBERT through methods like sparse attention (Child et al.,2019) and block attention (Shen et al., 2018). An orthogonal line of research, which could provideadditional representation power, includes hard example mining (Mikolov et al., 2013) and moreefﬁcient language modeling training (Yang et al., 2019). Additionally, although we have convincingevidence that sentence order prediction is a more consistently-useful learning task that leads to betterlanguage representations, we hypothesize that there could be more dimensions not yet captured bythe current self-supervised training losses that could create additional representation power for theresulting representations.
段落总结：DISCUSSIONWhile ALBERT-xxlarge has less parameters than BERT-large and gets signiﬁcantly better resu

**********段落分割**********
ACKNOWLEDGEMENTThe authors would like to thank Beer Changpinyo, Nan Ding, Noam Shazeer, and Tomer Levinboimfor discussion and providing useful feedback on the project; Omer Levy and Naman Goyal forclarifying experimental setup for RoBERTa; Zihang Dai for clarifying XLNet; Brandon Norick,Emma Strubell, Shaojie Bai, Chas Leichner, and Sachin Mehta for providing useful feedback on thepaper; Jacob Devlin for providing the English and multilingual version of training data; Liang Xu,Chenjie Cao and the CLUE community for providing the training data and evaluation benechmarkof the Chinese version of ALBERT models.10
段落总结：ACKNOWLEDGEMENTThe authors would like to thank Beer Changpinyo, Nan Ding, Noam Shazeer, and Tomer Le

**********段落分割**********
[ACKNOWLEDGEMENT]Published as a conference paper at ICLR 2020
段落总结：[ACKNOWLEDGEMENT]Published as a conference paper at ICLR 2020

**********段落分割**********
REFERENCESAlexei Baevski and Michael Auli. Adaptive input representations for neural language modeling.arXiv preprint arXiv:1809.10853, 2018.Shaojie Bai, J. Zico Kolter, and Vladlen Koltun. Deep equilibrium models. In Neural InformationProcessing Systems (NeurIPS), 2019.Roy Bar-Haim, Ido Dagan, Bill Dolan, Lisa Ferro, Danilo Giampiccolo, Bernardo Magnini, andIdan Szpektor. The second PASCAL recognising textual entailment challenge. In Proceedings ofthe second PASCAL challenges workshop on recognising textual entailment, volume 6, pp. 6–4.Venice, 2006.Luisa Bentivogli, Peter Clark, Ido Dagan, and Danilo Giampiccolo. The ﬁfth PASCAL recognizingtextual entailment challenge. In TAC, 2009.Daniel Cer, Mona Diab, Eneko Agirre, I˜nigo Lopez-Gazpio, and Lucia Specia. SemEval-2017 task1: Semantic textual similarity multilingual and crosslingual focused evaluation. In Proceedings ofthe 11th International Workshop on Semantic Evaluation (SemEval-2017), pp. 1–14, Vancouver,Canada, August 2017. Association for Computational Linguistics. doi: 10.18653/v1/S17-2001.URL https://www.aclweb.org/anthology/S17-2001.Tianqi Chen, Bing Xu, Chiyuan Zhang, and Carlos Guestrin. Training deep nets with sublinearmemory cost. arXiv preprint arXiv:1604.06174, 2016.Rewon Child, Scott Gray, Alec Radford, and Ilya Sutskever. Generating long sequences with sparsetransformers. arXiv preprint arXiv:1904.10509, 2019.Kevin Clark, Minh-Thang Luong, Urvashi Khandelwal, Christopher D Manning, and Quoc VLe. Bam!
段落总结：REFERENCESAlexei Baevski and Michael Auli

**********段落分割**********
born-again multi-task networks for natural language understanding. arXiv preprintarXiv:1907.04829, 2019.Ido Dagan, Oren Glickman, and Bernardo Magnini. The PASCAL recognising textual entailmentchallenge. In Machine Learning Challenges Workshop, pp. 177–190. Springer, 2005.Andrew M Dai and Quoc V Le. Semi-supervised sequence learning. In Advances in neural infor-mation processing systems, pp. 3079–3087, 2015.Zihang Dai, Zhilin Yang, Yiming Yang, William W Cohen, Jaime Carbonell, Quoc V Le, and RuslanSalakhutdinov. Transformer-xl: Attentive language models beyond a ﬁxed-length context. arXivpreprint arXiv:1901.02860, 2019.Mostafa Dehghani, Stephan Gouws, Oriol Vinyals, Jakob Uszkoreit, and Łukasz Kaiser. Universaltransformers. arXiv preprint arXiv:1807.03819, 2018.Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. BERT: Pre-training of deepbidirectional transformers for language understanding. In Proceedings of the 2019 Conference ofthe North American Chapter of the Association for Computational Linguistics: Human LanguageTechnologies, Volume 1 (Long and Short Papers), pp. 4171–4186, Minneapolis, Minnesota, June2019. Association for Computational Linguistics. doi: 10.18653/v1/N19-1423. URL https://www.aclweb.org/anthology/N19-1423.William B. Dolan and Chris Brockett. Automatically constructing a corpus of sentential paraphrases.In Proceedings of the Third International Workshop on Paraphrasing (IWP2005), 2005.
段落总结：born-again multi-task networks for natural language understanding

**********段落分割**********
URLhttps://www.aclweb.org/anthology/I05-5002.Zhe Gan, Yunchen Pu, Ricardo Henao, Chunyuan Li, Xiaodong He, and Lawrence Carin. Learn-ing generic sentence representations using convolutional neural networks.In Proceedings ofthe 2017 Conference on Empirical Methods in Natural Language Processing, pp. 2390–2400,Copenhagen, Denmark, September 2017. Association for Computational Linguistics.doi:10.18653/v1/D17-1254. URL https://www.aclweb.org/anthology/D17-1254.11
段落总结：URLhttps://www.aclweb.org/anthology/I05-5002.Zhe Gan, Yunchen Pu, Ricardo Henao, Chunyuan Li, Xiaodo

**********段落分割**********
[REFERENCES]Published as a conference paper at ICLR 2020Danilo Giampiccolo, Bernardo Magnini, Ido Dagan, and Bill Dolan. The third PASCAL recognizingtextual entailment challenge. In Proceedings of the ACL-PASCAL Workshop on Textual Entail-ment and Paraphrasing, pp. 1–9, Prague, June 2007. Association for Computational Linguistics.URL https://www.aclweb.org/anthology/W07-1401.Aidan N Gomez, Mengye Ren, Raquel Urtasun, and Roger B Grosse. The reversible residual net-work: Backpropagation without storing activations. In Advances in neural information processingsystems, pp. 2214–2224, 2017.Linyuan Gong, Di He, Zhuohan Li, Tao Qin, Liwei Wang, and Tieyan Liu. Efﬁcient training of bertby progressively stacking. In International Conference on Machine Learning, pp. 2337–2346,2019.Edouard Grave, Armand Joulin, Moustapha Ciss´e, Herv´e J´egou, et al. Efﬁcient softmax approxima-tion for gpus. In Proceedings of the 34th International Conference on Machine Learning-Volume70, pp. 1302–1310. JMLR. org, 2017.Barbara J. Grosz, Aravind K. Joshi, and Scott Weinstein. Centering: A framework for modeling thelocal coherence of discourse. Computational Linguistics, 21(2):203–225, 1995. URL https://www.aclweb.org/anthology/J95-2003.M.A.K. Halliday and Ruqaiya Hasan. Cohesion in English. Routledge, 1976.Jie Hao, Xing Wang, Baosong Yang, Longyue Wang, Jinfeng Zhang, and Zhaopeng Tu. Modelingrecurrence for transformer. Proceedings of the 2019 Conference of the North, 2019. doi: 10.18653/v1/n19-1122.
段落总结：[REFERENCES]Published as a conference paper at ICLR 2020Danilo Giampiccolo, Bernardo Magnini, Ido Da

**********段落分割**********
URL http://dx.doi.org/10.18653/v1/n19-1122.Dan Hendrycks and Kevin Gimpel.Gaussian Error Linear Units (GELUs).arXiv preprintarXiv:1606.08415, 2016.Felix Hill, Kyunghyun Cho, and Anna Korhonen. Learning distributed representations of sentencesfrom unlabelled data. In Proceedings of the 2016 Conference of the North American Chapter ofthe Association for Computational Linguistics: Human Language Technologies, pp. 1367–1377.Association for Computational Linguistics, 2016. doi: 10.18653/v1/N16-1162. URL http://aclweb.org/anthology/N16-1162.Jerry R. Hobbs. Coherence and coreference. Cognitive Science, 3(1):67–90, 1979.Jeremy Howard and Sebastian Ruder. Universal language model ﬁne-tuning for text classiﬁcation.arXiv preprint arXiv:1801.06146, 2018.Shankar Iyer, Nikhil Dandekar, and Kornl Csernai.First quora dataset release:Ques-tionpairs,January2017.URLhttps://www.quora.com/q/quoradata/First-Quora-Dataset-Release-Question-Pairs.Yacine Jernite, Samuel R Bowman, and David Sontag. Discourse-based objectives for fast unsuper-vised sentence representation learning. arXiv preprint arXiv:1705.00557, 2017.Mandar Joshi, Danqi Chen, Yinhan Liu, Daniel S Weld, Luke Zettlemoyer, and Omer Levy.SpanBERT: Improving pre-training by representing and predicting spans.arXiv preprintarXiv:1907.10529, 2019.Ryan Kiros, Yukun Zhu, Ruslan Salakhutdinov, Richard S. Zemel, Antonio Torralba, Raquel Ur-tasun, and Sanja Fidler. Skip-thought vectors.
段落总结：URL http://dx.doi.org/10.18653/v1/n19-1122.Dan Hendrycks and Kevin Gimpel.Gaussian Error Linear Unit

**********段落分割**********
In Proceedings of the 28th International Con-ference on Neural Information Processing Systems - Volume 2, NIPS’15, pp. 3294–3302, Cam-bridge, MA, USA, 2015. MIT Press. URL http://dl.acm.org/citation.cfm?id=2969442.2969607.Taku Kudo and John Richardson.SentencePiece: A simple and language independent sub-word tokenizer and detokenizer for neural text processing. In Proceedings of the 2018 Con-ference on Empirical Methods in Natural Language Processing: System Demonstrations, pp.66–71, Brussels, Belgium, November 2018. Association for Computational Linguistics.doi:10.18653/v1/D18-2012. URL https://www.aclweb.org/anthology/D18-2012.12
段落总结：In Proceedings of the 28th International Con-ference on Neural Information Processing Systems - Volu

**********段落分割**********
Published as a conference paper at ICLR 2020Guokun Lai, Qizhe Xie, Hanxiao Liu, Yiming Yang, and Eduard Hovy. RACE: Large-scale ReAdingcomprehension dataset from examinations. In Proceedings of the 2017 Conference on EmpiricalMethods in Natural Language Processing, pp. 785–794, Copenhagen, Denmark, September 2017.Association for Computational Linguistics. doi: 10.18653/v1/D17-1082. URL https://www.aclweb.org/anthology/D17-1082.Quoc Le and Tomas Mikolov. Distributed representations of sentences and documents. In Proceed-ings of the 31st ICML, Beijing, China, 2014.Hector Levesque, Ernest Davis, and Leora Morgenstern. The Winograd schema challenge. In Thir-teenth International Conference on the Principles of Knowledge Representation and Reasoning,2012.Xiang Li, Shuo Chen, Xiaolin Hu, and Jian Yang. Understanding the disharmony between dropoutand batch normalization by variance shift. In Proceedings of the IEEE Conference on ComputerVision and Pattern Recognition, pp. 2682–2690, 2019.Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, MikeLewis, Luke Zettlemoyer, and Veselin Stoyanov. RoBERTa: A robustly optimized BERT pre-training approach. arXiv preprint arXiv:1907.11692, 2019.Bryan McCann, James Bradbury, Caiming Xiong, and Richard Socher.Learned in translation:Contextualized word vectors. In I. Guyon, U. V. Luxburg, S. Bengio, H. Wallach, R. Fergus,S. Vishwanathan, and R. Garnett (eds.), Advances in Neural Information Processing Systems 30,pp.
段落总结：Published as a conference paper at ICLR 2020Guokun Lai, Qizhe Xie, Hanxiao Liu, Yiming Yang, and Edu

**********段落分割**********
6294–6305. Curran Associates, Inc., 2017. URL http://papers.nips.cc/paper/7209-learned-in-translation-contextualized-word-vectors.pdf.Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg S Corrado, and Jeff Dean. Distributed represen-tations of words and phrases and their compositionality. In Advances in neural information pro-cessing systems, pp. 3111–3119, 2013.Allen Nie, Erin Bennett, and Noah Goodman. DisSent: Learning sentence representations from ex-plicit discourse relations. In Proceedings of the 57th Annual Meeting of the Association for Com-putational Linguistics, pp. 4497–4510, Florence, Italy, July 2019. Association for ComputationalLinguistics. doi: 10.18653/v1/P19-1442. URL https://www.aclweb.org/anthology/
段落总结：6294–6305. Curran Associates, Inc., 2017. URL http://papers.nips.cc/paper/7209-learned-in-translatio

**********段落分割**********
P19-1442.Jeffrey Pennington, Richard Socher, and Christopher Manning. Glove: Global vectors for word rep-resentation. In Proceedings of the 2014 Conference on Empirical Methods in Natural LanguageProcessing (EMNLP), pp. 1532–1543, Doha, Qatar, October 2014. Association for ComputationalLinguistics. doi: 10.3115/v1/D14-1162. URL https://www.aclweb.org/anthology/
段落总结：P19-1442.Jeffrey Pennington, Richard Socher, and Christopher Manning. Glove: Global vectors for word

**********段落分割**********
D14-1162.Matthew Peters, Mark Neumann, Mohit Iyyer, Matt Gardner, Christopher Clark, Kenton Lee, andLuke Zettlemoyer. Deep contextualized word representations. In Proceedings of the 2018 Con-ference of the North American Chapter of the Association for Computational Linguistics: Hu-man Language Technologies, Volume 1 (Long Papers), pp. 2227–2237, New Orleans, Louisiana,June 2018. Association for Computational Linguistics.doi: 10.18653/v1/N18-1202.URLhttps://www.aclweb.org/anthology/N18-1202.Alec Radford, Karthik Narasimhan, Tim Salimans, and Ilya Sutskever.Improving languageunderstanding by generative pre-training. https://s3-us-west-2.amazonaws.com/openai-assets/research-covers/language-unsupervised/language_understanding_paper.pdf, 2018.Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever. Languagemodels are unsupervised multitask learners. OpenAI Blog, 1(8), 2019.Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, YanqiZhou, Wei Li, and Peter J Liu. Exploring the limits of transfer learning with a uniﬁed text-to-texttransformer. arXiv preprint arXiv:1910.10683, 2019.13
段落总结：D14-1162.Matthew Peters, Mark Neumann, Mohit Iyyer, Matt Gardner, Christopher Clark, Kenton Lee, and

**********段落分割**********
[D14-1162.]Published as a conference paper at ICLR 2020Pranav Rajpurkar, Jian Zhang, Konstantin Lopyrev, and Percy Liang. SQuAD: 100,000+ questionsfor machine comprehension of text. In Proceedings of the 2016 Conference on Empirical Methodsin Natural Language Processing, pp. 2383–2392, Austin, Texas, November 2016. Associationfor Computational Linguistics. doi: 10.18653/v1/D16-1264. URL https://www.aclweb.org/anthology/D16-1264.Pranav Rajpurkar, Robin Jia, and Percy Liang. Know what you don’t know: Unanswerable questionsfor SQuAD. In Proceedings of the 56th Annual Meeting of the Association for ComputationalLinguistics (Volume 2: Short Papers), pp. 784–789, Melbourne, Australia, July 2018. Associationfor Computational Linguistics. doi: 10.18653/v1/P18-2124. URL https://www.aclweb.org/anthology/P18-2124.Noam Shazeer, Youlong Cheng, Niki Parmar, Dustin Tran, Ashish Vaswani, Penporn Koanantakool,Peter Hawkins, HyoukJoong Lee, Mingsheng Hong, Cliff Young, et al. Mesh-tensorﬂow: Deeplearning for supercomputers. In Advances in Neural Information Processing Systems, pp. 10414–10423, 2018.Tao Shen, Tianyi Zhou, Guodong Long, Jing Jiang, and Chengqi Zhang. Bi-directional block self-attention for fast and memory-efﬁcient sequence modeling. arXiv preprint arXiv:1804.00857,2018.Mohammad Shoeybi, Mostofa Patwary, Raul Puri, Patrick LeGresley, Jared Casper, and BryanCatanzaro.
段落总结：[D14-1162.]Published as a conference paper at ICLR 2020Pranav Rajpurkar, Jian Zhang, Konstantin Lopy

**********段落分割**********
Megatron-LM: Training multi-billion parameter language models using model par-allelism, 2019.Richard Socher, Alex Perelygin, Jean Wu, Jason Chuang, Christopher D. Manning, Andrew Ng,and Christopher Potts. Recursive deep models for semantic compositionality over a sentimenttreebank. In Proceedings of the 2013 Conference on Empirical Methods in Natural LanguageProcessing, pp. 1631–1642, Seattle, Washington, USA, October 2013. Association for Computa-tional Linguistics. URL https://www.aclweb.org/anthology/D13-1170.Siqi Sun, Yu Cheng, Zhe Gan, and Jingjing Liu. Patient knowledge distillation for BERT modelcompression. arXiv preprint arXiv:1908.09355, 2019.Christian Szegedy, Sergey Ioffe, Vincent Vanhoucke, and Alexander A Alemi.Inception-v4,inception-resnet and the impact of residual connections on learning. In Thirty-First AAAI Confer-ence on Artiﬁcial Intelligence, 2017.Iulia Turc, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Well-read students learn better:The impact of student initialization on knowledge distillation. arXiv preprint arXiv:1908.08962,2019.Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez,Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. In Advances in neural informationprocessing systems, pp. 5998–6008, 2017.Alex Wang, Amanpreet Singh, Julian Michael, Felix Hill, Omer Levy, and Samuel Bowman. GLUE:A multi-task benchmark and analysis platform for natural language understanding.
段落总结：Megatron-LM: Training multi-billion parameter language models using model par-allelism, 2019

**********段落分割**********
In Proceed-ings of the 2018 EMNLP Workshop BlackboxNLP: Analyzing and Interpreting Neural Networksfor NLP, pp. 353–355, Brussels, Belgium, November 2018. Association for Computational Lin-guistics. doi: 10.18653/v1/W18-5446. URL https://www.aclweb.org/anthology/
段落总结：In Proceed-ings of the 2018 EMNLP Workshop BlackboxNLP: Analyzing and Interpreting Neural Networksfo

**********段落分割**********
W18-5446.Wei Wang, Bin Bi, Ming Yan, Chen Wu, Zuyi Bao, Liwei Peng, and Luo Si. StructBERT: Incor-porating language structures into pre-training for deep language understanding. arXiv preprintarXiv:1908.04577, 2019.Alex Warstadt, Amanpreet Singh, and Samuel R Bowman. Neural network acceptability judgments.arXiv preprint arXiv:1805.12471, 2018.Adina Williams, Nikita Nangia, and Samuel Bowman. A broad-coverage challenge corpus for sen-tence understanding through inference.In Proceedings of the 2018 Conference of the North14
段落总结：W18-5446.Wei Wang, Bin Bi, Ming Yan, Chen Wu, Zuyi Bao, Liwei Peng, and Luo Si. StructBERT: Incor-po

**********段落分割**********
[W18-5446.]Published as a conference paper at ICLR 2020American Chapter of the Association for Computational Linguistics: Human Language Technolo-gies, Volume 1 (Long Papers), pp. 1112–1122, New Orleans, Louisiana, June 2018. Associationfor Computational Linguistics. doi: 10.18653/v1/N18-1101. URL https://www.aclweb.org/anthology/N18-1101.Zhilin Yang, Zihang Dai, Yiming Yang, Jaime Carbonell, Ruslan Salakhutdinov, and Quoc VLe. XLNet: Generalized autoregressive pretraining for language understanding. arXiv preprintarXiv:1906.08237, 2019.Yang You, Jing Li, Jonathan Hseu, Xiaodan Song, James Demmel, and Cho-Jui Hsieh. ReducingBERT pre-training time from 3 days to 76 minutes. arXiv preprint arXiv:1904.00962, 2019.Shuailiang Zhang, Hai Zhao, Yuwei Wu, Zhuosheng Zhang, Xi Zhou, and Xiang Zhou.DCMN+: Dual co-matching network for multi-choice reading comprehension. arXiv preprintarXiv:1908.11511, 2019.Yukun Zhu, Ryan Kiros, Rich Zemel, Ruslan Salakhutdinov, Raquel Urtasun, Antonio Torralba, andSanja Fidler. Aligning books and movies: Towards story-like visual explanations by watchingmovies and reading books. In Proceedings of the IEEE international conference on computervision, pp. 19–27, 2015.A
段落总结：[W18-5446.]Published as a conference paper at ICLR 2020American Chapter of the Association for Compu

**********段落分割**********
EFFECT OF NETWORK DEPTH AND WIDTHIn this section, we check how depth (number of layers) and width (hidden size) affect the perfor-mance of ALBERT. Table 11 shows the performance of an ALBERT-large conﬁguration (see Ta-ble 1) using different numbers of layers. Networks with 3 or more layers are trained by ﬁne-tuningusing the parameters from the depth before (e.g., the 12-layer network parameters are ﬁne-tunedfrom the checkpoint of the 6-layer network parameters).5 Similar technique has been used in Gonget al. (2019). If we compare a 3-layer ALBERT model with a 1-layer ALBERT model, althoughthey have the same number of parameters, the performance increases signiﬁcantly. However, thereare diminishing returns when continuing to increase the number of layers: the results of a 12-layernetwork are relatively close to the results of a 24-layer network, and the performance of a 48-layernetwork appears to decline.Number of layersParametersSQuAD1.1SQuAD2.0MNLISST-2RACEAvg118M31.1/22.950.1/50.166.480.840.152.9318M79.8/69.764.4/61.777.786.754.071.2618M86.4/78.473.8/71.181.288.960.977.21218M89.8/83.380.7/77.983.391.766.781.52418M90.3/83.381.8/79.083.391.568.782.14818M90.0/83.181.8/78.983.491.966.981.8Table 11: The effect of increasing the number of layers for an ALBERT-large conﬁguration.A similar phenomenon, this time for width, can be seen in Table 12 for a 3-layer ALBERT-largeconﬁguration. As we increase the hidden size, we get an increase in performance with diminishingreturns.
段落总结：EFFECT OF NETWORK DEPTH AND WIDTHIn this section, we check how depth (number of layers) and width (h

**********段落分割**********
At a hidden size of 6144, the performance appears to decline signiﬁcantly. We note that noneof these models appear to overﬁt the training data, and they all have higher training and developmentloss compared to the best-performing ALBERT conﬁgurations.5If we compare the performance of ALBERT-large here to the performance in Table 2, we can see that thiswarm-start technique does not help to improve the downstream performance. However, it does help the 48-layernetwork to converge. A similar technique has been applied to our ALBERT-xxlarge, where we warm-start froma 6-layer network.15
段落总结：At a hidden size of 6144, the performance appears to decline signiﬁcantly

**********段落分割**********
[EFFECT OF NETWORK DEPTH AND WIDTH]Published as a conference paper at ICLR 2020Hidden sizeParametersSQuAD1.1SQuAD2.0MNLISST-2RACEAvg102418M79.8/69.764.4/61.777.786.754.071.2204860M83.3/74.169.1/66.679.788.658.274.64096225M85.0/76.471.0/68.180.390.460.476.36144499M84.7/75.867.8/65.478.189.156.074.0Table 12: The effect of increasing the hidden-layer size for an ALBERT-large 3-layer conﬁguration.A.2DO VERY WIDE ALBERT MODELS NEED TO BE DEEP(ER) TOO?In Section A.1, we show that for ALBERT-large (H=1024), the difference between a 12-layer and a24-layer conﬁguration is small. Does this result still hold for much wider ALBERT conﬁgurations,such as ALBERT-xxlarge (H=4096)?Number of layersSQuAD1.1SQuAD2.0MNLISST-2RACEAvg1294.0/88.188.3/85.387.895.482.588.72494.1/88.388.1/85.188.095.282.388.7Table 13: The effect of a deeper network using an ALBERT-xxlarge conﬁguration.The answer is given by the results from Table 13. The difference between 12-layer and 24-layerALBERT-xxlarge conﬁgurations in terms of downstream accuracy is negligible, with the Avg scorebeing the same. We conclude that, when sharing all cross-layer parameters (ALBERT-style), thereis no need for models deeper than a 12-layer conﬁguration.A.3
段落总结：[EFFECT OF NETWORK DEPTH AND WIDTH]Published as a conference paper at ICLR 2020Hidden sizeParameters

**********段落分割**********
DOWNSTREAM EVALUATION TASKSGLUEGLUEiscomprisedof9tasks,namelyCorpusofLinguisticAcceptability(CoLA; Warstadt et al., 2018), Stanford Sentiment Treebank (SST; Socher et al., 2013), MicrosoftResearch Paraphrase Corpus (MRPC; Dolan & Brockett, 2005), Semantic Textual Similarity Bench-mark (STS; Cer et al., 2017), Quora Question Pairs (QQP; Iyer et al., 2017), Multi-Genre NLI(MNLI; Williams et al., 2018), Question NLI (QNLI; Rajpurkar et al., 2016), Recognizing TextualEntailment (RTE; Dagan et al., 2005; Bar-Haim et al., 2006; Giampiccolo et al., 2007; Bentivogliet al., 2009) and Winograd NLI (WNLI; Levesque et al., 2012). It focuses on evaluating modelcapabilities for natural language understanding. When reporting MNLI results, we only report the“match” condition (MNLI-m). We follow the ﬁnetuning procedures from prior work (Devlin et al.,2019; Liu et al., 2019; Yang et al., 2019) and report the held-out test set performance obtained fromGLUE submissions. For test set submissions, we perform task-speciﬁc modiﬁcations for WNLI andQNLI as described by Liu et al. (2019) and Yang et al. (2019).SQuADSQuAD is an extractive question answering dataset built from Wikipedia. The answersare segments from the context paragraphs and the task is to predict answer spans. We evaluate ourmodels on two versions of SQuAD: v1.1 and v2.0. SQuAD v1.1 has 100,000 human-annotatedquestion/answer pairs. SQuAD v2.0 additionally introduced 50,000 unanswerable questions.
段落总结：DOWNSTREAM EVALUATION TASKSGLUEGLUEiscomprisedof9tasks,namelyCorpusofLinguisticAcceptability(CoLA; W

**********段落分割**********
ForSQuAD v1.1, we use the same training procedure as BERT, whereas for SQuAD v2.0, models arejointly trained with a span extraction loss and an additional classiﬁer for predicting answerabil-ity (Yang et al., 2019; Liu et al., 2019). We report both development set and test set performance.RACERACE is a large-scale dataset for multi-choice reading comprehension, collected from En-glish examinations in China with nearly 100,000 questions. Each instance in RACE has 4 candidateanswers. Following prior work (Yang et al., 2019; Liu et al., 2019), we use the concatenation of thepassage, question, and each candidate answer as the input to models. Then, we use the represen-tations from the “[CLS]” token for predicting the probability of each answer. The dataset consistsof two domains: middle school and high school. We train our models on both domains and reportaccuracies on both the development set and test set.16
段落总结：ForSQuAD v1.1, we use the same training procedure as BERT, whereas for SQuAD v2.0, models arejointly

**********段落分割**********
[DOWNSTREAM EVALUATION TASKS]Published as a conference paper at ICLR 2020A.4
段落总结：[DOWNSTREAM EVALUATION TASKS]Published as a conference paper at ICLR 2020A

**********段落分割**********
HYPERPARAMETERSHyperparameters for downstream tasks are shown in Table 14. We adapt these hyperparametersfrom Liu et al. (2019), Devlin et al. (2019), and Yang et al. (2019).LRBSZ
段落总结：HYPERPARAMETERSHyperparameters for downstream tasks are shown in Table 14

**********段落分割**********
ALBERT DRClassiﬁer DRTSWSMSLCoLA
段落总结：ALBERT DRClassiﬁer DRTSWSMSLCoLA

**********段落分割**********
1.00E-051600.15336320512STS
段落总结：1.00E-051600.15336320512STS

**********段落分割**********
2.00E-051600.13598214512SST-2
段落总结：2.00E-051600.13598214512SST-2

**********段落分割**********
1.00E-053200.1209351256512MNLI
段落总结：1.00E-053200.1209351256512MNLI

**********段落分割**********
3.00E-0512800.1100001000512QNLI
段落总结：3.00E-0512800.1100001000512QNLI

**********段落分割**********
1.00E-053200.1331121986512QQP
段落总结：1.00E-053200.1331121986512QQP

**********段落分割**********
5.00E-051280.10.1140001000512RTE
段落总结：5.00E-051280.10.1140001000512RTE

**********段落分割**********
3.00E-05320.10.1800200512MRPC
段落总结：3.00E-05320.10.1800200512MRPC

**********段落分割**********
2.00E-053200.1800200512WNLI
段落总结：2.00E-053200.1800200512WNLI

**********段落分割**********
2.00E-05160.10.12000250512SQuAD v1.1
段落总结：2.00E-05160.10.12000250512SQuAD v1.1

**********段落分割**********
5.00E-054800.13649365384SQuAD v2.0
段落总结：5.00E-054800.13649365384SQuAD v2.0

**********段落分割**********
3.00E-054800.18144814512RACE
段落总结：3.00E-054800.18144814512RACE

**********段落分割**********
2.00E-05320.10.1120001000512Table 14: Hyperparameters for ALBERT in downstream tasks. LR: Learning Rate. BSZ: BatchSize. DR: Dropout Rate. TS: Training Steps. WS: Warmup Steps. MSL: Maximum SequenceLength.17
段落总结：2.00E-05320.10.1120001000512Table 14: Hyperparameters for ALBERT in downstream tasks. LR: Learning R
