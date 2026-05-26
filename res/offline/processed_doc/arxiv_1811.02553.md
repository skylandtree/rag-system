Published as a conference paper at ICLR 2020
段落总结：Published as a conference paper at ICLR 2020

**********段落分割**********
A CLOSER LOOK AT DEEP POLICY GRADIENTSAndrew Ilyas1*, Logan Engstrom1*, Shibani Santurkar1, Dimitris Tsipras1,Firdaus Janoos2, Larry Rudolph1,2, and Aleksander M ˛adry11MIT2Two Sigma{ailyas,engstrom,shibani,tsipras,madry}@mit.edurudolph@csail.mit.edu, firdaus.janoos@twosigma.com
段落总结：A CLOSER LOOK AT DEEP POLICY GRADIENTSAndrew Ilyas1*, Logan Engstrom1*, Shibani Santurkar1, Dimitris

**********段落分割**********
ABSTRACTWe study how the behavior of deep policy gradient algorithms reﬂects the con-ceptual framework motivating their development. To this end, we propose a ﬁne-grained analysis of state-of-the-art methods based on key elements of this frame-work: gradient estimation, value prediction, and optimization landscapes. Our re-sults show that the behavior of deep policy gradient algorithms often deviates fromwhat their motivating framework would predict: the surrogate objective does notmatch the true reward landscape, learned value estimators fail to ﬁt the true valuefunction, and gradient estimates poorly correlate with the “true” gradient. Themismatch between predicted and empirical behavior we uncover highlights ourpoor understanding of current methods, and indicates the need to move beyondcurrent benchmark-centric evaluation methods.1
段落总结：ABSTRACTWe study how the behavior of deep policy gradient algorithms reﬂects the con-ceptual framewo

**********段落分割**********
INTRODUCTIONDeep reinforcement learning (RL) is behind some of the most publicized achievements of modernmachine learning (Silver et al., 2017; OpenAI, 2018; Dayarathna et al., 2016; OpenAI et al., 2018).In fact, to many, this framework embodies the promise of the real-world impact of machine learning.However, the deep RL toolkit has not yet attained the same level of engineering stability as, forexample, the current deep (supervised) learning framework. Indeed, recent studies demonstrate thatstate-of-the-art deep RL algorithms suffer from oversensitivity to hyperparameter choices, lack ofconsistency, and poor reproducibility (Henderson et al., 2017).This state of affairs suggests that it might be necessary to re-examine the conceptual underpinningsof deep RL methodology. More precisely, the overarching question that motivates this work is:To what degree does current practice in deep RL reﬂect the principles informing its development?Our speciﬁc focus is on deep policy gradient methods, a widely used class of deep RL algorithms.Our goal is to explore the extent to which state-of-the-art implementations of these methods succeedat realizing the key primitives of the general policy gradient framework.Our contributions.We take a broader look at policy gradient algorithms and their relation to theirunderlying framework. With this perspective in mind, we perform a ﬁne-grained examination of keyRL primitives as they manifest in practice.
段落总结：INTRODUCTIONDeep reinforcement learning (RL) is behind some of the most publicized achievements of m

**********段落分割**********
Concretely, we study:• Gradient Estimation: we ﬁnd that even when agents improve in reward, their gradientestimates used in parameter updates poorly correlate with the “true” gradient. We addition-ally show that gradient estimate quality decays with training progress and task complexity.Finally, we demonstrate that varying the sample regime yields training dynamics that areunexplained by the motivating framework and run contrary to supervised learning intuition.• Value Prediction: our experiments indicate that value networks successfully solve thesupervised learning task they are trained on, but do not ﬁt the true value function. Addi-tionally, employing a value network as a baseline function only marginally decreases the*Equal contribution. Work done in part while interning at Two Sigma.1arXiv:1811.02553v4  [cs.LG]  25 May 2020
段落总结：Concretely, we study:• Gradient Estimation: we ﬁnd that even when agents improve in reward, their gr

**********段落分割**********
[INTRODUCTION]Published as a conference paper at ICLR 2020variance of gradient estimates compared to using true value as a baseline (but still dramat-ically increases agent’s performance compared to using no baseline at all).• Optimization Landscapes: we show that the optimization landscape induced by modernpolicy gradient algorithms is often not reﬂective of the underlying true reward landscape,and that the latter is frequently poorly behaved in the relevant sample regime.Overall, our results demonstrate that the motivating theoretical framework for deep RL algorithmsis often unpredictive of phenomena arising in practice. This suggests that building reliable deep RLalgorithms requires moving past benchmark-centric evaluations to a multi-faceted understanding oftheir often unintuitive behavior. We conclude (in Section 3) by discussing several areas where suchunderstanding is most critically needed.2
段落总结：[INTRODUCTION]Published as a conference paper at ICLR 2020variance of gradient estimates compared to

**********段落分割**********
EXAMINING THE PRIMITIVES OF DEEP POLICY GRADIENT ALGORITHMSIn this section, we investigate the degree to which our theoretical understanding of RL applies tomodern methods. We consider key primitives of policy gradient algorithms: gradient estimation,value prediction and reward ﬁtting. In what follows, we perform a ﬁne-grained analysis of state-of-the-art policy gradient algorithms (PPO and TRPO) through the lens of these primitives—detailedpreliminaries, background, and notation can be found in Appendix A.1.2.1
段落总结：EXAMINING THE PRIMITIVES OF DEEP POLICY GRADIENT ALGORITHMSIn this section, we investigate the degre

**********段落分割**********
GRADIENT ESTIMATE QUALITYA central premise of policy gradient methods is that stochastic gradient ascent on a suitable objectivefunction yields a good policy. These algorithms use as a primitive the gradient of that objectivefunction:ˆg = ∇θE(st,at)∼π0πθ(at|st)π0(at|st)bAπ0(st, at)= E(st,at)∼π0∇θπθ(at|st)π0(at|st)bAπ0(st, at),(1)where in the above we use standard RL notation (see Appendix A.1 for more details). An underlyingassumption behind these methods is that we have access to a reasonable estimate of this quantity.This assumption effectively translates into an assumption that we can accurately estimate the expec-tation above using an empirical mean of ﬁnite (typically ∼103) samples. Evidently (since the agentattains a high reward) these estimates are sufﬁcient to consistently improve reward—we are thusinterested in the relative quality of these gradient estimates in practice, and the effect of gradientquality on optimization.102103104105106
段落总结：GRADIENT ESTIMATE QUALITYA central premise of policy gradient methods is that stochastic gradient as

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. pairwise cos sim
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 0TRPOPPO102103104105106
段落总结：# Iteration: 0TRPOPPO102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. pairwise cos sim
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 150TRPOPPO102103104105106
段落总结：# Iteration: 150TRPOPPO102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. pairwise cos sim
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 300TRPOPPO102103104105106
段落总结：# Iteration: 300TRPOPPO102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. pairwise cos sim
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 450TRPOPPOFigure 1: Empirical variance of the estimated gradient (c.f. (1)) as a function of the number of state-action pairs used in estimation in the MuJoCo Humanoid task. We measure the average pairwisecosine similarity between ten repeated gradient measurements taken from the same policy, with the95% conﬁdence intervals (shaded). For each algorithm, we perform multiple trials with the samehyperparameter conﬁgurations but different random seeds, shown as repeated lines in the ﬁgure.The vertical line (at x = 2K) indicates the sample regime used for gradient estimation in standardimplementations of policy gradient methods. In general, it seems that obtaining tightly concentratedgradient estimates would require signiﬁcantly more samples than are used in practice, particularlyafter the ﬁrst few timesteps. For other tasks – such as Walker2d-v2 and Hopper-v2 – the plots (seenin Appendix Figure 9) have similar trends, except that gradient variance is slightly lower. Conﬁdenceintervals calculated with 500 sample bootstrapping.2
段落总结：# Iteration: 450TRPOPPOFigure 1: Empirical variance of the estimated gradient (c

**********段落分割**********
[Iteration: 450]Published as a conference paper at ICLR 2020102103104105106
段落总结：[Iteration: 450]Published as a conference paper at ICLR 2020102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. cos sim with true grad
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 0TRPOPPO102103104105106
段落总结：# Iteration: 0TRPOPPO102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. cos sim with true grad
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 150TRPOPPO102103104105106
段落总结：# Iteration: 150TRPOPPO102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. cos sim with true grad
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 300TRPOPPO102103104105106
段落总结：# Iteration: 300TRPOPPO102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. cos sim with true grad
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 450TRPOPPOFigure 2: Convergence of gradient estimates (c.f. (1)) to the “true” expected gradient in the MuJoCoHumanoid task. We measure the mean cosine similarity between the “true” gradient approximatedusing ten million state-action pairs, and ten gradient estimates which use increasing numbers ofstate-action pairs (with 95% conﬁdence intervals). For each algorithm, we perform multiple trialswith the same hyperparameter conﬁgurations but different random seeds. The vertical line (at x =2K) indicates the sample regime used for gradient estimation in standard implementations of policygradient methods. Observe that although it is possible to empirically estimate the true gradient,this requires several-fold more samples than are used commonly in practical applications of thesealgorithms. See additionally that the estimation task becomes more difﬁcult further into training.For other tasks – such as Walker2d-v2 and Hopper-v2 – the plots (seen in Appendix Figure 10) havesimilar trends, except that gradient estimation is slightly better. Conﬁdence intervals calculated with500 sample bootstrapping.How accurate are the gradient estimates we compute?To answer this question, we examine twoof the most natural measures of estimate quality: the empirical variance and the convergence to the“true” gradient. To evaluate the former, we measure the average pairwise cosine similarity betweenestimates of the gradient computed from the same policy with independent rollouts (Figure 1).
段落总结：# Iteration: 450TRPOPPOFigure 2: Convergence of gradient estimates (c

**********段落分割**********
Weevaluate the latter by ﬁrst forming an estimate of the true gradient with a large number of state-actionpairs. We then examine the convergence of gradient estimates to this “true” gradient (which we onceagain measure using cosine similarity) as we increase the number of samples (Figure 2).We observe that deep policy gradient methods operate with relatively poor estimates of the gradient,especially as task complexity increases and as training progresses (contrast Humanoid-v2, a “hard”task, to other tasks and contrast successive checkpoints in Figures 1 and 2). This is in spite of thefact that our agents continually improve throughout training, and attain nowhere near the maximumreward possible on each task. In fact, we sometimes observe a zero or even negative correlation inthe relevant sample regime1.While these results might be reminiscent of the well-studied “noisy gradients” problem in supervisedlearning (Robbins & Monro, 1951; d’Aspremont, 2008; Kawaguchi, 2016; Safran & Shamir, 2018;Livni et al., 2014; Keskar et al., 2016; Hochreiter & Schmidhuber, 1997), we have very little un-derstanding of how gradient quality affects optimization in the substantially different reinforcementlearning setting. For example:• The sample regime in which RL algorithms operate seems to have a profound impact onthe robustness and stability of agent training—in particular, many of the sensitivity issuesreported by Henderson et al.
段落总结：Weevaluate the latter by ﬁrst forming an estimate of the true gradient with a large number of state-

**********段落分割**********
(2017) are claimed to disappear (Sutskever, 2018) in higher-sample regimes. Understanding the implications of working in this sample regime, andmore generally the impact of sample complexity on training stability remains to be pre-cisely understood.• Agent policy networks are trained concurrently with value networks (discussed more in thefollowing section) meant to reduce the variance of gradient estimates. Under our conceptualframework, we might expect these networks to help gradient estimates more as trainingprogresses, contrary to what we observe in Figure 1. The value network also makes thenow two-player optimization landscape and training dynamics even more difﬁcult to grasp,as such interactions are poorly understood.1Deep policy gradient algorithms use gradients indirectly to compute steps—in Appendix A.4 we show thatour results also hold true for these computed steps.3
段落总结：(2017) are claimed to disappear (Sutskever, 2018) in higher-sample regimes

**********段落分割**********
[Iteration: 450]Published as a conference paper at ICLR 2020• The relevant measure of sample complexity for many settings (number of state-action pairs)can differ drastically from the number of independent samples used at each training itera-tion (the number of complete trajectories). The latter quantity (a) tends to be much lowerthan the number of state-action pairs, and (b) decreases across iterations during training.All the above factors make it unclear to what degree our intuition from classical settings transfer tothe deep RL regime. And the policy gradient framework, as of now, provides little predictive powerregarding the variance of gradient estimates and its impact on reward optimization.Our results indicate that despite having a rigorous theoretical framework for RL, we lack a preciseunderstanding of the structure of the reward landscape and optimization process.2.2
段落总结：[Iteration: 450]Published as a conference paper at ICLR 2020• The relevant measure of sample complex

**********段落分割**********
VALUE PREDICTIONOur ﬁndings from the previous section motivate a deeper look into gradient estimation. After all,the policy gradient in its original formulation (Sutton et al., 1999) is known to be hard to estimate,and thus algorithms employ a variety of variance reduction methods. The most popular of thesetechniques is a baseline function. Concretely, an equivalent form of the policy gradient is given by:bgθ = Eτ∼πθX(st,at)∈τ∇θ log πθ(at|st) · (Qπθ(st, at) −b(st))(2)where b(st) is some ﬁxed function of the state st. A canonical choice of baseline function is thevalue function Vπ(s), the expected return from a given state (more details and motivation in A.1):Vπθ(st) = Eπθ[Rt|st] .(3)Indeed, ﬁtting a value-estimating function (Schulman et al., 2015c; Sutton & Barto, 2018) (a neuralnetwork, in the deep RL setting) and using it as a baseline function is precisely the approach takenby most deep policy gradient methods. Concretely, one trains a value network V πθt such that:θt = minθEV πθ (st) −(V πθt−1(st) + At)2(4)where V πθt−1(st) are estimates given by the last value function, and At is the advantage of the policy,i.e. the returns minus the estimated values. (Typically, At is estimated using generalized advantageestimation, as described in (Schulman et al., 2015c).) Our ﬁndings in the previous section promptus to take a closer look at the value network and its impact on the variance of gradient estimates.0100200300400500
段落总结：VALUE PREDICTIONOur ﬁndings from the previous section motivate a deeper look into gradient estimatio

**********段落分割**********
GAE MRETRPOPPO0100200300400500
段落总结：GAE MRETRPOPPO0100200300400500

**********段落分割**********
# Iterations2423222120Returns MRETRPOPPO(a)Figure 3: Quality of value prediction in terms of mean relative error (MRE) on heldout state-actionpairs for agents trained to solve the MuJoCo Walker2d-v2 task. We observe in (left) that the agentsdo indeed succeed at solving the supervised learning task they are trained for—the MRE on theGAE-based value loss (Vold + AGAE)2 (c.f. (4)) is small. On the other hand, in (right) we see thatthe returns MRE is still quite high—the learned value function is off by about 50% with respect tothe underlying true value function. Similar plots for other MuJoCo tasks are in Appendix A.5.4
段落总结：# Iterations2423222120Returns MRETRPOPPO(a)Figure 3: Quality of value prediction in terms of mean re

**********段落分割**********
[Iterations]Published as a conference paper at ICLR 20200200040006000800010000
段落总结：[Iterations]Published as a conference paper at ICLR 20200200040006000800010000

**********段落分割**********
# State-Action Pairs0.000.050.100.150.200.25Avg. pairwise cos sim
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 150Baselines:ZeroVtV *0200040006000800010000
段落总结：# Iteration: 150Baselines:ZeroVtV *0200040006000800010000

**********段落分割**********
# State-Action Pairs0.000.050.100.150.20Avg. pairwise cos sim
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 300Baselines:ZeroVtV *0200040006000800010000
段落总结：# Iteration: 300Baselines:ZeroVtV *0200040006000800010000

**********段落分割**********
# State-Action Pairs0.000.020.040.060.080.100.120.14Avg. pairwise cos sim
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 450Baselines:ZeroVtV *(a) Walker2d-v20200040006000800010000
段落总结：# Iteration: 450Baselines:ZeroVtV *(a) Walker2d-v20200040006000800010000

**********段落分割**********
# State-Action Pairs0.00.10.20.3Avg. pairwise cos sim
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 150Baselines:ZeroVtV *0200040006000800010000
段落总结：# Iteration: 150Baselines:ZeroVtV *0200040006000800010000

**********段落分割**********
# State-Action Pairs0.000.050.100.150.20Avg. pairwise cos sim
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 300Baselines:ZeroVtV *0200040006000800010000
段落总结：# Iteration: 300Baselines:ZeroVtV *0200040006000800010000

**********段落分割**********
# State-Action Pairs0.000.050.100.150.200.250.300.35Avg. pairwise cos sim
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 450Baselines:ZeroVtV *(b) Hopper-v2Figure 4: Efﬁcacy of the value network as a variance reducing baseline for Walker2d-v2 (top) andHopper-v2 (bottom) agents. We measure the empirical variance of the gradient (c.f. (1)) as a functionof the number of state-action pairs used in estimation, for different choices of baseline functions:the value network (used by the agent in training), the “true” value function (ﬁt to the returns us-ing 5 · 106 state-action pairs sampled from the current policy) and the “zero” value function (i.e.replacing advantages with returns). We observe that using the true value function leads to a signif-icantly lower-variance estimate of the gradient compared to the value network. In turn, employingthe value network yields a noticeable variance reduction compared to the zero baseline function,even though this difference may appear rather small in the small-sample regime (2K). Conﬁdenceintervals calculated with 10 sample bootstrapping.Value prediction as a supervised learning problem.We ﬁrst analyze the value network throughthe lens of the supervised learning problem it solves. After all, (4) describes an empirical riskminimization, where a loss is minimized over a set of sampled (st, at). So, how does V πθ perform asa solution to (4)?
段落总结：# Iteration: 450Baselines:ZeroVtV *(b) Hopper-v2Figure 4: Efﬁcacy of the value network as a variance

**********段落分割**********
And in turn, how does (4) perform as a proxy for learning the true value function?Our results (Figure 3a) show that the value network does succeed at both ﬁtting the given loss func-tion and generalizing to unseen data, showing low and stable mean relative error (MRE). However,the signiﬁcant drop in performance as shown in Figure 3 indicates that the supervised learning prob-lem induced by (4) does not lead to V πθ learning the underlying true value function.Does the value network lead to a reduction in variance?Though evaluating the V πθ baselinefunction as a value predictor as we did above is informative, in the end the sole purpose of thevalue function is to reduce variance. So: how does using our value function actually impact thevariance of our gradient estimates? To answer this question, we compare the variance reductionthat results from employing our value network against both a “true” value function and a trivial“zero” baseline function (i.e. simply replacing advantages with returns). Our results, captured inFigure 4, show that the “true” value function yields a much lower-variance estimate of the gradient.This is especially true in the sample regime in which we operate. We note, however, that despitenot effectively predicting the true value function or inducing the same degree of variance reduction,the value network does help to some degree (compared to the “zero” baseline).
段落总结：And in turn, how does (4) perform as a proxy for learning the true value function?Our results (Figur

**********段落分割**********
Additionally, theseemingly marginal increase in gradient correlation provided by the value network (compared tothe “true” baseline function) turns out to result in a signiﬁcant improvement in agent performance.(Indeed, agents trained without a baseline reach almost an order of magnitude worse reward.)Our ﬁndings suggest that we still need a better understanding of the role of the value network inagent training, and raise several questions that we discuss in Section 3.5
段落总结：Additionally, theseemingly marginal increase in gradient correlation provided by the value network (

**********段落分割**********
[Iteration: 450]Published as a conference paper at ICLR 20202.3
段落总结：[Iteration: 450]Published as a conference paper at ICLR 20202

**********段落分割**********
EXPLORING THE OPTIMIZATION LANDSCAPEAnother key assumption of policy gradient algorithms is that ﬁrst-order updates (w.r.t. policy pa-rameters) actually yield better policies. It is thus natural to examine how valid this assumption is.The true rewards landscape.We begin by examining the landscape of agent reward with respectto the policy parameters. Indeed, even if deep policy gradient methods do not optimize for the truereward directly (e.g. if they use a surrogate objective), the ultimate goal of any policy gradient al-gorithm is to navigate this landscape. First, Figure 5 shows that while estimating the true rewardlandscape with a high number of samples yields a relatively smooth reward landscape (perhaps sug-gesting viability of direct reward optimization), estimating the true reward landscape in the typical,low sample regime results in a landscape that appears jagged and poorly-behaved. The low-sampleregime thus gives rise to a certain kind of barrier to direct reward optimization. Indeed, applyingour algorithms in this regime makes it impossible to distinguish between good and bad points in thelandscape, even though the true underlying landscape is fairly well-behaved.The surrogate objective landscape.The untamed nature of the rewards landscape has led to thedevelopment of alternate approaches to reward maximization.
段落总结：EXPLORING THE OPTIMIZATION LANDSCAPEAnother key assumption of policy gradient algorithms is that ﬁrs

**********段落分割**********
Recall that an important element ofmany modern policy gradient methods is the maximization of a surrogate objective function in placeof the true rewards (the exact mechanism behind the surrogate objective is detailed in Appendix A.1,and particularly in (14)). The surrogate objective, based on relaxing the policy improvement theoremof Kakade and Langford (Kakade & Langford, 2002), can be viewed as a simpliﬁcation of the rewardmaximization objective.As a purported approximation of the true returns, one would expect that the surrogate objectivelandscape approximates the true reward landscape fairly well. That is, parameters corresponding togood surrogate objective will also correspond to good true reward.Figure 6 shows that in the early stages of training, the optimization landscapes of the true rewardand surrogate objective are indeed approximately aligned. However, as training progresses, thesurrogate objective becomes much less predictive of the true reward in the relevant sample regime. Inparticular, we often observe that directions that increase the surrogate objective lead to a decrease ofthe true reward (see Figures 6, 7). In a higher-sample regime (using several orders of magnitude moresamples), we ﬁnd that PPO and TRPO turn out to behave rather differently.
段落总结：Recall that an important element ofmany modern policy gradient methods is the maximization of a surr

**********段落分割**********
In the case of TRPO,the update direction following the surrogate objective matches the true reward much more closely.However, for PPO we consistently observe landscapes where the step direction leads to lower truereward, even in the high-sample regime. This suggests that even when estimated accurately enough,2,000 state-action pairs20,000 state-action pairs100,000 state-action pairsGradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0400420440460480500520(~21 trajectories)Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0410420430440450460(~235 trajectories)Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0410420430440(~1187 trajectories)Figure 5: True reward landscape concentration for TRPO on Humanoid-v2. We visualize the land-scape at a training iteration 150 while varying the number of trajectories used in reward estimation(each subplot), both in the direction of the step taken and a random direction. Moving one unit alongthe “step direction” axis corresponds to moving one full step in parameter space. In the random di-rection one unit corresponds to moving along a random norm 2 Gaussian vector in the parameterspace. In practice, the norm of the step is typically an order of magnitude lower than the randomdirection. While the landscape is very noisy in the low-sample regime, large numbers of samplesreveal a well-behaved underlying landscape. See Figures 20, 19 of the Appendix for additional plots.6
段落总结：In the case of TRPO,the update direction following the surrogate objective matches the true reward m

**********段落分割**********
[EXPLORING THE OPTIMIZATION LANDSCAPE]Published as a conference paper at ICLR 2020Few state-action pairs (2,000)Many state-action pairs (106)SurrogateTrue rewardSurrogateTrue rewardStep 0Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.00.10.20.30.40.5Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0108110112114116118120122Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.000.010.020.030.040.050.060.07Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0120140160180200220240Step 300Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.00.10.20.30.40.50.60.7Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0440450460470480490Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.010.020.030.040.05Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0455460465470475Figure 6: True reward and surrogate objective landscapes for TRPO on the Humanoid-v2 MuJoCotask. We visualize the landscapes in the direction of the update step and a random direction (as inFigure 5). The surrogate objective corresponds to the actual function optimized by the algorithm ateach step. We estimate true reward with 106 state-action pairs per point.
段落总结：[EXPLORING THE OPTIMIZATION LANDSCAPE]Published as a conference paper at ICLR 2020Few state-action p

**********段落分割**********
We compare the landscapesat different points in training and with varying numbers of state-action pairs used in the update step.Early in training the true and surrogate landscapes align fairly well in both sample regimes, but laterbecome misaligned in the low-sample regime. More landscapes in Appendix Figures 13-18.the surrogate objective might not be an accurate proxy for the true reward. (Recall from Section 2.1that this is a sample regime where we are able to estimate the true gradient of the reward fairly well.)3
段落总结：We compare the landscapesat different points in training and with varying numbers of state-action pa

**********段落分割**********
TOWARDS STRONGER FOUNDATIONS FOR DEEP RLDeep reinforcement learning (RL) algorithms have shown great practical promise, and are rootedin a well-grounded theoretical framework. However, our results indicate that this framework oftenfails to provide insight into the practical performance of these algorithms. This disconnect impedesour understanding of why these algorithms succeed (or fail), and is a major barrier to addressing keychallenges facing deep RL such as brittleness and poor reproducibility.To close this gap, we need to either develop methods that adhere more closely to theory, or buildtheory that can capture what makes existing policy gradient methods successful. In both cases, theﬁrst step is to precisely pinpoint where theory and practice diverge. To this end, we analyze andconsolidate our ﬁndings from the previous section.Gradient estimation. Our analysis in Section 2.1 shows that the quality of gradient estimates thatdeep policy gradient algorithms use is rather poor. Indeed, even when agents improve, such gradientestimates often poorly correlate with the true gradient (c.f. Figure 2). We also note that gradient cor-relation decreases as training progresses and task complexity increases. While this certainly does notpreclude the estimates from conveying useful signal, the exact underpinnings of this phenomenonin deep RL still elude us.
段落总结：TOWARDS STRONGER FOUNDATIONS FOR DEEP RLDeep reinforcement learning (RL) algorithms have shown great

**********段落分割**********
In particular, in Section 2.1 we outline a few keys ways in which thedeep RL setting is quite unique and difﬁcult to understand from an optimization perspective, boththeoretically and in practice Overall, understanding the impact of gradient estimate quality on deepRL algorithms is challenging and largely unexplored.Value prediction. The ﬁndings presented in Section 2.2 identify two key issues. First, while thevalue network successfully solves the supervised learning task it is trained on, it does not accuratelymodel the “true” value function. Second, employing the value network as a baseline does decreasethe gradient variance (compared to the trivial (“zero”) baseline). However, this decrease is rathermarginal compared to the variance reduction offered by the “true” value function.It is natural to wonder whether this failure in modeling the value function is inevitable. For example,how does the loss function used to train the value network impact value prediction and variancereduction? More broadly, we lack an understanding of the precise role of the value network in7
段落总结：In particular, in Section 2

**********段落分割**********
[TOWARDS STRONGER FOUNDATIONS FOR DEEP RL]Published as a conference paper at ICLR 2020Few state-action pairs (2,000)Many state-action pairs (106)SurrogateTrue rewardSurrogateTrue rewardStep 0Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.00.10.20.30.4Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0110115120125130Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.000.010.020.030.040.05Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0110120130140150160170Step 300Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.00.10.20.30.40.50.60.7Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0460480500520540560580600620Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.0000.0020.0040.0060.0080.0100.0120.014Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0530540550560570580590600610Figure 7: True reward and surrogate objective landscapes for PPO on the Humanoid-v2 MuJoCotask. See Figure 6 for a description. We observe that early in training the true and surrogate land-scapes align well. However, later increasing the surrogate objective leads to lower true reward.training. Can we empirically quantify the relationship between variance reduction and performance?And does the value network play a broader role than just variance reduction?Optimization landscape.
段落总结：[TOWARDS STRONGER FOUNDATIONS FOR DEEP RL]Published as a conference paper at ICLR 2020Few state-acti

**********段落分割**********
We have also seen, in Section 2.3, that the optimization landscape in-duced by modern policy gradient algorithms, the surrogate objective, is often not reﬂective of theunderlying true reward landscape. We thus need a deeper understanding of why current methodssucceed despite these issues, and, more broadly, how to better navigate the true reward landscape.4
段落总结：We have also seen, in Section 2

**********段落分割**********
RELATED WORKThe idea of using gradient estimates to update neural network-based RL agents dates back at leastto the REINFORCE (Williams, 1992) algorithm. Later, Sutton (Sutton et al., 1999) established aunifying framework casting these algorithms as instances of the policy gradient class of algorithms.Our work focuses on proximal policy optimization (PPO) (Schulman et al., 2017) and trust regionpolicy optimization (TRPO) (Schulman et al., 2015a), which are two of the most prominent policygradient algorithms used in deep RL, drawing inspiration from works on related algorithms, suchas (Peters et al., 2010) and Kakade (2001).Many recent works document the brittleness of deep RL algorithms (Henderson et al., 2018; 2017;Islam et al., 2017). (Rajeswaran et al., 2017) and (Mania et al., 2018) demonstrate that on manybenchmark tasks, state-of-the-art performance can be attained by augmented randomized searchapproaches. McCandlish et al. (2018) investigates gradient noise in large-batch settings, and Ahmedet al. (2018) investigates the role of entropy regularization (which we do not study) on optimization.5
段落总结：RELATED WORKThe idea of using gradient estimates to update neural network-based RL agents dates back

**********段落分割**********
CONCLUSIONIn this work, we analyze the degree to which key primitives of deep policy gradient algorithmsfollow their conceptual underpinnings. Our experiments show that these primitives often do notconform to the expected behavior: gradient estimates poorly correlate with the true gradient, bettergradient estimates can require lower learning rates and can induce degenerate agent behavior, valuenetworks reduce gradient estimation variance to a signiﬁcantly smaller extent than the true value,and the underlying optimization landscape can be misleading.This demonstrates that there is a signiﬁcant gap between the theory inspiring current algorithms andthe actual mechanisms driving their performance. Overall, our ﬁndings suggest that developing adeep RL toolkit that is truly robust and reliable will require moving beyond the current benchmark-driven evaluation model to a more ﬁne-grained understanding of deep RL algorithms.8
段落总结：CONCLUSIONIn this work, we analyze the degree to which key primitives of deep policy gradient algori

**********段落分割**********
[CONCLUSION]Published as a conference paper at ICLR 20206
段落总结：[CONCLUSION]Published as a conference paper at ICLR 20206

**********段落分割**********
ACKNOWLEDGEMENTSWork supported in part by the NSF grants CCF-1553428, CNS-1815221, the Google PhD Fellow-ship, the Open Phil AI Fellowship, and the Microsoft Corporation.
段落总结：ACKNOWLEDGEMENTSWork supported in part by the NSF grants CCF-1553428, CNS-1815221, the Google PhD Fe

**********段落分割**********
REFERENCESZafarali Ahmed, Nicolas Le Roux, Mohammad Norouzi, and Dale Schuurmans. Understanding theimpact of entropy on policy optimization, 2018.Alexandre d’Aspremont. Smooth optimization with approximate gradient. SIAM Journal on Opti-mization, 19:1171–1183, 2008.Miyuru Dayarathna, Yonggang Wen, and Rui Fan. Data center energy consumption modeling: Asurvey. IEEE Communications Surveys & Tutorials, 18(1):732–794, 2016.Peter Henderson, Riashat Islam, Philip Bachman, Joelle Pineau, Doina Precup, and David Meger.Deep reinforcement learning that matters. arXiv preprint arXiv:1709.06560, 2017.Peter Henderson, Joshua Romoff, and Joelle Pineau. Where did my optimum go?: An empiricalanalysis of gradient descent optimization in policy gradient methods, 2018.Sepp Hochreiter and Jürgen Schmidhuber. Flat minima. Neural Computation, 9:1–42, 1997.Riashat Islam, Peter Henderson, Maziar Gomrokchi, and Doina Precup. Reproducibility of bench-marked deep reinforcement learning tasks for continuous control. In ICML Reproducibility inMachine Learning Workshop, 2017.Sham M. Kakade. A natural policy gradient. In NIPS, 2001.Sham M. Kakade and John Langford. Approximately optimal approximate reinforcement learning.In ICML, 2002.Kenji Kawaguchi. Deep learning without poor local minima. In NIPS, 2016.Nitish Shirish Keskar, Dheevatsa Mudigere, Jorge Nocedal, Mikhail Smelyanskiy, and Ping Tak Pe-ter Tang. On large-batch training for deep learning: Generalization gap and sharp minima.
段落总结：REFERENCESZafarali Ahmed, Nicolas Le Roux, Mohammad Norouzi, and Dale Schuurmans

**********段落分割**********
CoRR,abs/1609.04836, 2016.Roi Livni, Shai Shalev-Shwartz, and Ohad Shamir. On the computational efﬁciency of trainingneural networks. In NIPS, 2014.Horia Mania, Aurelia Guy, and Benjamin Recht. Simple random search provides a competitiveapproach to reinforcement learning. CoRR, abs/1803.07055, 2018.Sam McCandlish, Jared Kaplan, Dario Amodei, and OpenAI Dota Team. An empirical model oflarge-batch training, 2018.OpenAI. Openai ﬁve. https://blog.openai.com/openai-five/, 2018.OpenAI, :, Marcin Andrychowicz, Bowen Baker, Maciek Chociej, Rafal Jozefowicz, Bob McGrew,Jakub Pachocki, Arthur Petron, Matthias Plappert, Glenn Powell, Alex Ray, Jonas Schneider, Szy-mon Sidor, Josh Tobin, Peter Welinder, Lilian Weng, and Wojciech Zaremba. Learning dexterousin-hand manipulation, 2018.Jan Peters, Katharina Mülling, and Yasemin Altun. Relative entropy policy search. In AAAI, 2010.Aravind Rajeswaran, Kendall Lowrey, Emanuel Todorov, and Sham M. Kakade. Towards general-ization and simplicity in continuous control. In NIPS, 2017.Herbert Robbins and Sutton Monro. A stochastic approximation method. Ann. Math. Statist., 22(3):400–407, 09 1951. doi: 10.1214/aoms/1177729586. URL https://doi.org/10.1214/aoms/1177729586.9
段落总结：CoRR,abs/1609.04836, 2016.Roi Livni, Shai Shalev-Shwartz, and Ohad Shamir. On the computational efﬁc

**********段落分割**********
[REFERENCES]Published as a conference paper at ICLR 2020Itay Safran and Ohad Shamir. Spurious local minima are common in two-layer relu neural networks.In ICML, 2018.John Schulman, Sergey Levine, Pieter Abbeel, Michael Jordan, and Philipp Moritz. Trust regionpolicy optimization. In International Conference on Machine Learning, pp. 1889–1897, 2015a.John Schulman, Philipp Moritz, Sergey Levine, Michael Jordan, and Pieter Abbeel.High-dimensional continuous control using generalized advantage estimation.arXiv preprintarXiv:1506.02438, 2015b.John Schulman, Philipp Moritz, Sergey Levine, Michael I. Jordan, and Pieter Abbeel.High-dimensional continuous control using generalized advantage estimation. CoRR, abs/1506.02438,2015c.John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policyoptimization algorithms. arXiv preprint arXiv:1707.06347, 2017.David Silver, Julian Schrittwieser, Karen Simonyan, Ioannis Antonoglou, Aja Huang, Arthur Guez,Thomas Hubert, Lucas Baker, Matthew Lai, Adrian Bolton, et al. Mastering the game of gowithout human knowledge. Nature, 550(7676):354, 2017.Ilya Sutskever. Keynote talk. NVIDIA NTECH, 2018. URL https://www.youtube.com/watch?v=w3ues-NayAs&t=467s.Richard S Sutton and Andrew G Barto. Reinforcement learning: An introduction. MIT press, 2018.Richard S. Sutton, David A. McAllester, Satinder P. Singh, and Yishay Mansour. Policy gradientmethods for reinforcement learning with function approximation.
段落总结：[REFERENCES]Published as a conference paper at ICLR 2020Itay Safran and Ohad Shamir

**********段落分割**********
In NIPS, 1999.Ronald J. Williams. Simple statistical gradient-following algorithms for connectionist reinforcementlearning. Machine Learning, 8:229–256, 1992.10
段落总结：In NIPS, 1999.Ronald J. Williams. Simple statistical gradient-following algorithms for connectionist

**********段落分割**********
Published as a conference paper at ICLR 2020A
段落总结：Published as a conference paper at ICLR 2020A

**********段落分割**********
BACKGROUNDIn the reinforcement learning (RL) setting, an agent interacts with a stateful environment with thegoal of maximizing cumulative reward. Formally, we model the environment as a (possibly random-ized) function mapping its current state s and an action a supplied by the agent to a new state s′ anda resulting reward r. The choice of actions of the agent is governed by the its policy π. This policyis a function mapping environment states to a distribution over the actions to take. The objective ofan RL algorithm is to ﬁnd a policy π which maximizes the expected cumulative reward, where theexpectation is taken over both environment randomness and the (randomized) action choices.Preliminaries and notation.For a given policy π, we denote by π(a|s) the probability that thispolicy assigns to taking action a when the environment is in the state s. We use r(s, a) to denotethe reward that the agent earns for playing action a in response to the state s. A trajectory τ ={(at, st) : t ∈{1 . . . T}} is a sequence of state-action pairs that constitutes a valid transcript ofinteractions of the agent with the environment. (Here, at (resp. st) corresponds to the action takenby the agent (resp. state of the environment) in the t-th round of interaction.) We then deﬁne π(τ)to be the probability that the trajectory τ is executed if the agent follows policy π (provided theinitial state of the environment is s1).
段落总结：BACKGROUNDIn the reinforcement learning (RL) setting, an agent interacts with a stateful environment

**********段落分割**********
Similarly, r(τ) = Pt r(st, at) denotes the cumulative rewardearned by the agent when following this trajectory, where st (resp. at) denote the t-th state (resp.action) in the trajectory τ. In the RL setting, however, we often choose to maximize the discountedcumulative reward of a policy R := R1, where Rt is deﬁned asRt(τ) =∞Xt′=tγ(t′−t)rt′ .and 0 < γ < 1 is a “discount factor”. The discount factor ensures that the cumulative reward ofa policy is well-deﬁned even for an inﬁnite time horizon, and it also incentivizes achieving rewardearlier.Policy gradient methods.A widely used class of RL algorithms that will be the focus of ouranalysis is the class of so-called policy gradient methods. The central idea behind these algorithmsis to ﬁrst parameterize the policy πθ using a parameter vector θ. (In the deep RL context, πθ isexpressed by a neural network with weights θ.) Then, we perform stochastic gradient ascent on thecumulative reward with respect to θ. In other words, we want to apply the stochastic ascent approachto our problem:maxθEτ∼πθ[r(τ)] ,(5)where τ ∼πθ represents trajectories (rollouts) sampled from the distribution induced by the policyπθ.
段落总结：Similarly, r(τ) = Pt r(st, at) denotes the cumulative rewardearned by the agent when following this 

**********段落分割**********
This approach relies on the key observation (Sutton et al., 1999) that under mild conditions, thegradient of our objective can be written as:∇θEτ∼πθ[r(τ)] = Eτ∼πθ[∇θ log(πθ(τ)) r(τ)],(6)and the latter quantity can be estimated directly by sampling trajectories according to the policy πθ.When we use the discounted variant of the cumulative reward and note that the action of the policyat time t cannot affect its performance at earlier times, we can express our gradient estimate as:bgθ = Eτ∼πθX(st,at)∈τ∇θ log πθ(at|st) · Qπθ(st, at),(7)where Qπθ(st, at) represents the expected returns after taking action at from state st:Qπθ(st, at) = Eπθ[Rt|at, st] .(8)11
段落总结：This approach relies on the key observation (Sutton et al

**********段落分割**********
[BACKGROUND]Published as a conference paper at ICLR 2020Value estimation and advantage.Unfortunately, the variance of the expectation in (7) can be (andoften is) very large, which makes getting an accurate estimate of this expectation quite challenging.To alleviate this issue, a number of variance reduction techniques have been developed. One of themost popular such techniques is the use of a so-called baseline function, wherein a state-dependentvalue is subtracted from Qπθ. Thus, instead of estimating (7) directly, we use:bgθ = Eτ∼πθX(st,at)∈τ∇θ log πθ(at|st) · (Qπθ(st, at) −b(st)),(9)where b(·) is a baseline function of our choice.A natural choice of the baseline function is the value function, i.e.Vπθ(st) = Eπθ[Rt|st] .(10)When we use the value function as our baseline, the resulting gradient estimation problem becomes:bgθ = Eτ∼πθX(st,at)∈τ∇θ log πθ(at|st) · Aπθ(st, at),(11)whereAπθ(st, at) = Qπθ(st, at) −Vπθ(st)(12)is referred to as the advantage of performing action at. Different methods of estimating Vπθ havebeen proposed, with techniques ranging from moving averages to the use of neural network predic-tors Schulman et al. (2015b).Surrogate Objective.So far, our focus has been on extracting a good estimate of the gradientwith respect to the policy parameters θ. However, it turns out that directly optimizing the cumula-tive rewards can be challenging. Thus, a modiﬁcation used by modern policy gradient algorithmsis to optimize a “surrogate objective” instead.
段落总结：[BACKGROUND]Published as a conference paper at ICLR 2020Value estimation and advantage

**********段落分割**********
We will focus on maximizing the following localapproximation of the true reward Schulman et al. (2015a):maxθE(st,at)∼ππθ(at|st)π(at|st) Aπ(st, at)= Eπθ [Aπ],(13)or the normalized advantage variant proposed to reduce variance Schulman et al. (2017):maxθE(st,at)∼ππθ(at|st)π(at|st)bAπ(st, at)(14)wherebAπ = Aπ −µ(Aπ)σ(Aπ)(15)and π is the current policy.Trust region methods.The surrogate objective function, although easier to optimize, comes at acost: the gradient of the surrogate objective is only predictive of the policy gradient locally (at thecurrent policy). Thus, to ensure that our update steps we derive based on the surrogate objective arepredictive, they need to be conﬁned to a “trust region” around the current policy. The resulting trustregion methods (Kakade, 2001; Schulman et al., 2015a; 2017) try to constrain the local variation ofthe parameters in policy-space by restricting the distributional distance between successive policies.A popular method in this class is trust region policy optimization (TRPO) Schulman et al.
段落总结：We will focus on maximizing the following localapproximation of the true reward Schulman et al

**********段落分割**********
(2015a),which constrains the KL divergence between successive policies on the optimization trajectory, lead-ing to the following problem:maxθE(st,at)∼ππθ(at|st)π(at|st)bAπ(st, at)s.t.DKL(πθ(· | s)||π(· | s)) ≤δ,∀s .(16)In practice, this objective is maximized using a second-order approximation of the KL divergenceand natural gradient descent, while replacing the worst-case KL constraints over all possible stateswith an approximation of the mean KL based on the states observed in the current trajectory.12
段落总结：(2015a),which constrains the KL divergence between successive policies on the optimization trajector

**********段落分割**********
Published as a conference paper at ICLR 2020Proximal policy optimization.In practice, the TRPO algorithm can be computationally costly—the step direction is estimated with nonlinear conjugate gradients, which requires the computationof multiple Hessian-vector products. To address this issue, Schulman et al. Schulman et al. (2017)propose proximal policy optimization (PPO), which utilizes a different objective and does not com-pute a projection. Concretely, PPO proposes replacing the KL-constrained objective (16) of TRPOby clipping the objective function directly as:maxθE(st,at)∼πhminclip (ρt, 1 −ε, 1 + ε) bAπ(st, at), ρt bAπ(st, at)i(17)whereρt = πθ(at|st)π(at|st)(18)In addition to being simpler, PPO is intended to be faster and more sample-efﬁcient thanTRPO (Schulman et al., 2017).13
段落总结：Published as a conference paper at ICLR 2020Proximal policy optimization

**********段落分割**********
Published as a conference paper at ICLR 2020A.2
段落总结：Published as a conference paper at ICLR 2020A

**********段落分割**********
EXPERIMENTAL SETUPWe use the following parameters for PPO and TRPO based on a hyperparameter grid search:Table 1: Hyperparameters for PPO and TRPO algorithms.Humanoid-v2Walker2d-v2Hopper-v2PPOTRPOPPOTRPOPPOTRPOTimesteps per iteration204820482048204820482048Discount factor (γ)0.990.990.990.990.990.99GAE discount (λ)0.950.950.950.950.950.95Value network LR0.00010.00030.00030.00030.00020.0002Value net num. epochs101010101010Policy net hidden layers[64, 64][64, 64][64, 64][64, 64][64, 64][64, 64]Value net hidden layers[64, 64][64, 64][64, 64][64, 64][64, 64][64, 64]KL constraint (δ)N/A0.07N/A0.04N/A0.13Fisher est. fractionN/A0.1N/A0.1N/A0.1Conjugate grad. stepsN/A10N/A10N/A10CG dampingN/A0.1N/A0.1N/A0.1Backtracking stepsN/A10N/A10N/A10Policy LR (Adam)0.00025N/A0.0004N/A0.00045N/APolicy epochs10N/A10N/A10N/APPO Clipping ε0.2N/A0.2N/A0.2N/AEntropy coeff.0.00.00.00.00.00.0Reward clipping[-10, 10]–[-10, 10]–[-10, 10]–Reward normalizationOnOffOnOffOnOffState clipping[-10, 10]–[-10, 10]–[-10, 10]–All error bars we plot are 95% conﬁdence intervals, obtained via bootstrapped sampling.14
段落总结：EXPERIMENTAL SETUPWe use the following parameters for PPO and TRPO based on a hyperparameter grid se

**********段落分割**********
[EXPERIMENTAL SETUP]Published as a conference paper at ICLR 2020A.3
段落总结：[EXPERIMENTAL SETUP]Published as a conference paper at ICLR 2020A

**********段落分割**********
STANDARD REWARD PLOTS0100200300400500
段落总结：STANDARD REWARD PLOTS0100200300400500

**********段落分割**********
# Iteration050010001500200025003000Mean RewardTRPOPPO(a) Hopper-v20100200300400500
段落总结：# Iteration050010001500200025003000Mean RewardTRPOPPO(a) Hopper-v20100200300400500

**********段落分割**********
# Iteration0100020003000Mean RewardTRPOPPO(b) Walker2d-v20100200300400500
段落总结：# Iteration0100020003000Mean RewardTRPOPPO(b) Walker2d-v20100200300400500

**********段落分割**********
# Iteration2004006008001000Mean RewardTRPOPPO(c) Humanoid-v2Figure 8: Mean reward for the studied policy gradient algorithms on standard MuJoCo benchmarktasks. For each algorithm, we perform 24 random trials using the best performing hyperparameterconﬁguration, with 10 of the random agents shown here.15
段落总结：# Iteration2004006008001000Mean RewardTRPOPPO(c) Humanoid-v2Figure 8: Mean reward for the studied po

**********段落分割**********
[Iteration]Published as a conference paper at ICLR 2020A.4
段落总结：[Iteration]Published as a conference paper at ICLR 2020A

**********段落分割**********
QUALITY OF GRADIENT ESTIMATION102103104105106
段落总结：QUALITY OF GRADIENT ESTIMATION102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. pairwise cos sim
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 0TRPOPPO102103104105106
段落总结：# Iteration: 0TRPOPPO102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. pairwise cos sim
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 150TRPOPPO102103104105106
段落总结：# Iteration: 150TRPOPPO102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. pairwise cos sim
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 300TRPOPPO102103104105106
段落总结：# Iteration: 300TRPOPPO102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. pairwise cos sim
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 450TRPOPPO(a) Walker2d-v2102103104105106
段落总结：# Iteration: 450TRPOPPO(a) Walker2d-v2102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. pairwise cos sim
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 0TRPOPPO102103104105106
段落总结：# Iteration: 0TRPOPPO102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. pairwise cos sim
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 150TRPOPPO102103104105106
段落总结：# Iteration: 150TRPOPPO102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. pairwise cos sim
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 300TRPOPPO102103104105106
段落总结：# Iteration: 300TRPOPPO102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. pairwise cos sim
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 450TRPOPPO(b) Hopper-v2Figure 9: Empirical variance of the gradient (c.f. (1)) as a function of the number of state-actionpairs used in estimation for policy gradient methods. We obtain multiple gradient estimates usinga given number of state-action pairs from the policy at a particular iteration. We then measure theaverage pairwise cosine similarity between these repeated gradient measurements, along with the95% conﬁdence intervals (shaded). Each of the colored lines (for a speciﬁc algorithm) representsa particular trained agent (we perform multiple trials with the same hyperparameter conﬁgurationsbut different random seeds). The dotted vertical black line (at 2K) indicates the sample regime usedfor gradient estimation in standard practical implementations of policy gradient methods.16
段落总结：# Iteration: 450TRPOPPO(b) Hopper-v2Figure 9: Empirical variance of the gradient (c

**********段落分割**********
[Iteration: 450]Published as a conference paper at ICLR 2020102103104105106
段落总结：[Iteration: 450]Published as a conference paper at ICLR 2020102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. cos sim with true grad
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 0TRPOPPO102103104105106
段落总结：# Iteration: 0TRPOPPO102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. cos sim with true grad
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 150TRPOPPO102103104105106
段落总结：# Iteration: 150TRPOPPO102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. cos sim with true grad
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 300TRPOPPO102103104105106
段落总结：# Iteration: 300TRPOPPO102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. cos sim with true grad
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 450TRPOPPO(a) Walker2d-v2102103104105106
段落总结：# Iteration: 450TRPOPPO(a) Walker2d-v2102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. cos sim with true grad
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 0TRPOPPO102103104105106
段落总结：# Iteration: 0TRPOPPO102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. cos sim with true grad
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 150TRPOPPO102103104105106
段落总结：# Iteration: 150TRPOPPO102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. cos sim with true grad
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 300TRPOPPO102103104105106
段落总结：# Iteration: 300TRPOPPO102103104105106

**********段落分割**********
# State-Action Pairs0.50.00.51.0Avg. cos sim with true grad
段落总结：# State-Action Pairs0

**********段落分割**********
# Iteration: 450TRPOPPO(b) Hopper-v2Figure 10: Convergence of gradient estimates to the “true” expected gradient (c.f. (1)). We measurethe cosine similarity between the true gradient (approximated using around 1M samples) and gradi-ent estimates, as a function of number of state-action pairs used to obtain the later. For a particularpolicy and state-action pair count, we obtain multiple estimates of this cosine similarity and thenreport the average, along with the 95% conﬁdence intervals (shaded). Each of the colored lines (fora speciﬁc algorithm) represents a particular trained agent (we perform multiple trials with the samehyperparameter conﬁgurations but different random seeds). The dotted vertical black line (at 2K)indicates the sample regime used for gradient estimation in standard practical implementations ofpolicy gradient methods.17
段落总结：# Iteration: 450TRPOPPO(b) Hopper-v2Figure 10: Convergence of gradient estimates to the “true” expec

**********段落分割**********
[Iteration: 450]Published as a conference paper at ICLR 2020A.5
段落总结：[Iteration: 450]Published as a conference paper at ICLR 2020A

**********段落分割**********
VALUE PREDICTION0100200300400500
段落总结：VALUE PREDICTION0100200300400500

**********段落分割**********
# Iterations211282522
段落总结：# Iterations211282522

**********段落分割**********
GAE MRETRPOPPO0100200300400500
段落总结：GAE MRETRPOPPO0100200300400500

**********段落分割**********
# Iterations2725232121Returns MRETRPOPPO(a) Hopper-v20100200300400500
段落总结：# Iterations2725232121Returns MRETRPOPPO(a) Hopper-v20100200300400500

**********段落分割**********
# Iterations211282522
段落总结：# Iterations211282522

**********段落分割**********
GAE MRETRPOPPO0100200300400500
段落总结：GAE MRETRPOPPO0100200300400500

**********段落分割**********
# Iterations2725232121Returns MRETRPOPPO(b) Walker2d-v20100200300400500
段落总结：# Iterations2725232121Returns MRETRPOPPO(b) Walker2d-v20100200300400500

**********段落分割**********
GAE MRETRPOPPO0100200300400500
段落总结：GAE MRETRPOPPO0100200300400500

**********段落分割**********
# Iterations232121Returns MRETRPOPPO(c) Humanoid-v2Figure 11: Quality of value prediction in terms of mean relative error (MRE) on train state-actionpairs for agents trained to solve the MuJoCo tasks. We see in that the agents do indeed succeed atsolving the supervised learning task they are trained for – the train MRE on the GAE-based valueloss (Vold+AGAE)2 (c.f. (4)) is small (left column). We observe that the returns MRE is quite smallas well (right column).18
段落总结：# Iterations232121Returns MRETRPOPPO(c) Humanoid-v2Figure 11: Quality of value prediction in terms o

**********段落分割**********
[Iterations]Published as a conference paper at ICLR 20200100200300400500
段落总结：[Iterations]Published as a conference paper at ICLR 20200100200300400500

**********段落分割**********
# Iterations211282522
段落总结：# Iterations211282522

**********段落分割**********
GAE MRETRPOPPO0100200300400500
段落总结：GAE MRETRPOPPO0100200300400500

**********段落分割**********
# Iterations2725232121Returns MRETRPOPPO(a) Hopper-v20100200300400500
段落总结：# Iterations2725232121Returns MRETRPOPPO(a) Hopper-v20100200300400500

**********段落分割**********
# Iterations2524232221
段落总结：# Iterations2524232221

**********段落分割**********
GAE MRETRPOPPO0100200300400500
段落总结：GAE MRETRPOPPO0100200300400500

**********段落分割**********
# Iterations2322212021Returns MRETRPOPPO(b) Humanoid-v2Figure 12: Quality of value prediction in terms of mean relative error (MRE) on heldout state-actionpairs for agents trained to solve MuJoCo tasks. We see in that the agents do indeed succeed atsolving the supervised learning task they are trained for – the validation MRE on the GAE-basedvalue loss (Vold + AGAE)2 (c.f. (4)) is small (left column). On the other hand, we see that thereturns MRE is still quite high – the learned value function is off by about 50% with respect to theunderlying true value function (right column).19
段落总结：# Iterations2322212021Returns MRETRPOPPO(b) Humanoid-v2Figure 12: Quality of value prediction in ter

**********段落分割**********
[Iterations]Published as a conference paper at ICLR 2020A.6
段落总结：[Iterations]Published as a conference paper at ICLR 2020A

**********段落分割**********
OPTIMIZATION LANDSCAPEFew state-action pairs (2,000)Many state-action pairs (106)SurrogateTrue rewardSurrogateTrue rewardStep 0Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.00.10.20.30.4Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0110115120125130Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.000.010.020.030.040.05Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0110120130140150160170Step 150Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.00.10.20.30.40.50.60.70.8Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0485490495500505510515520Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.0000.0020.0040.0060.0080.0100.0120.0140.016Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0460.0462.5465.0467.5470.0472.5475.0477.5480.0Step 300Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.00.10.20.30.40.50.60.7Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0460480500520540560580600620Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.0000.0020.0040.0060.0080.0100.0120.014Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0530540550560570580590600610Step 450Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.000.050.100.150.200.250.300.35Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0560580600620640660680700Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.00000.00050.00100.00150.00200.00250.00300.0035Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0535540545550555560565570Figure 13: Humanoid-v2 – PPO reward landscapes.20
段落总结：OPTIMIZATION LANDSCAPEFew state-action pairs (2,000)Many state-action pairs (106)SurrogateTrue rewar

**********段落分割**********
[OPTIMIZATION LANDSCAPE]Published as a conference paper at ICLR 2020Few state-action pairs (2,000)Many state-action pairs (106)SurrogateTrue rewardSurrogateTrue rewardStep 0Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.00.10.20.30.40.5Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0108110112114116118120122Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.000.010.020.030.040.050.060.07Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0120140160180200220240Step 150Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.10.20.30.40.50.6Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0415420425430435440445450Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.000.010.020.030.040.05Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0410420430440Step 300Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.00.10.20.30.40.50.60.7Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0440450460470480490Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.010.020.030.040.05Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0455460465470475Step 450Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.10.20.30.40.50.60.70.8Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0440460480500520540560Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.000.010.020.030.040.05Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0530535540545550555560565Figure 14: Humanoid-v2 – TRPO reward landscapes.21
段落总结：[OPTIMIZATION LANDSCAPE]Published as a conference paper at ICLR 2020Few state-action pairs (2,000)Ma

**********段落分割**********
Published as a conference paper at ICLR 2020Few state-action pairs (2,000)Many state-action pairs (106)SurrogateTrue rewardSurrogateTrue rewardStep 0Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.000.050.100.150.200.25Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.002468101214Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.0000.0250.0500.0750.1000.1250.1500.175Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.005101520253035Step 150Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.000.050.100.150.200.250.30Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0600650700750800850900950Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.0000.0010.0020.0030.0040.0050.0060.007Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0290300310320330340Step 300Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.000.020.040.060.080.100.120.140.16Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.010001500200025003000Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.0000.0020.0040.0060.0080.010Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0580600620640660680700Step 450Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.000.010.020.030.040.050.060.070.08Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.05001000150020002500Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.0000.0010.0020.0030.0040.0050.006Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0480500520540560580600Figure 15: Walker2d-v2 – PPO reward landscapes.22
段落总结：Published as a conference paper at ICLR 2020Few state-action pairs (2,000)Many state-action pairs (1

**********段落分割**********
Published as a conference paper at ICLR 2020Few state-action pairs (2,000)Many state-action pairs (106)SurrogateTrue rewardSurrogateTrue rewardStep 0Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.000.050.100.150.200.250.300.350.40Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0020406080Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.000.050.100.150.200.25Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0020406080100120Step 150Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.0000.0250.0500.0750.1000.1250.1500.1750.200Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.050060070080090010001100Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.000.010.020.030.040.05Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.04005006007008009001000Step 300Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.0000.0250.0500.0750.1000.1250.1500.175Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.08001000120014001600Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.0000.0050.0100.0150.020Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0550600650700750800850900Step 450Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.050.100.150.200.250.30Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.01000150020002500Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.0050.0000.0050.0100.0150.0200.0250.030Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.060070080090010001100Figure 16: Walker2d-v2 – TRPO reward landscapes.23
段落总结：Published as a conference paper at ICLR 2020Few state-action pairs (2,000)Many state-action pairs (1

**********段落分割**********
Published as a conference paper at ICLR 2020Few state-action pairs (2,000)Many state-action pairs (106)SurrogateTrue rewardSurrogateTrue rewardStep 0Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.010.000.010.020.030.040.05Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.01520253035Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.0000.0050.0100.0150.0200.025Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.01020304050607080Step 150Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.0000.0250.0500.0750.1000.1250.1500.175Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0400600800100012001400Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.0000.0020.0040.0060.0080.010Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0100120140160180200220Step 300Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.020.040.060.080.100.120.14Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0500750100012501500175020002250Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.0000.0050.0100.0150.020Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0150.0152.5155.0157.5160.0162.5165.0Step 450Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.000.020.040.060.080.10Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.06008001000120014001600Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.00000.00020.00040.00060.00080.00100.00120.0014Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0100200300400500600700800900Figure 17: Hopper-v2 – PPO reward landscapes.24
段落总结：Published as a conference paper at ICLR 2020Few state-action pairs (2,000)Many state-action pairs (1

**********段落分割**********
Published as a conference paper at ICLR 2020Few state-action pairs (2,000)Many state-action pairs (106)SurrogateTrue rewardSurrogateTrue rewardStep 0Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.050.100.150.20Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0203040506070Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.000.050.100.150.20Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0152025303540455055Step 150Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.000.010.020.030.040.050.06Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0500750100012501500175020002250Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.0000.0050.0100.0150.020Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.025050075010001250150017502000Step 300Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.000.020.040.060.08Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.080010001200140016001800200022002400Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.00000.00250.00500.00750.01000.01250.0150Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.070080090010001100Step 450Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.000.020.040.06Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.010001500200025003000Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.00.0000.0020.0040.0060.0080.0100.012Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.015001750200022502500275030003250Figure 18: Hopper-v2 – TRPO reward landscapes.25
段落总结：Published as a conference paper at ICLR 2020Few state-action pairs (2,000)Many state-action pairs (1

**********段落分割**********
Published as a conference paper at ICLR 20202,000 state-action pairs20,000 state-action pairs100,000 state-action pairsStep 0Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0120140160180200220240(~61 trajectories)Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0120140160180200220240(~616 trajectories)Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0120140160180200220240(~3131 trajectories)Step 150Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0400420440460480500520(~21 trajectories)Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0410420430440450460(~235 trajectories)Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0410420430440(~1187 trajectories)Step 300Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0420440460480500520540(~20 trajectories)Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0460465470475480485490495500(~215 trajectories)Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0455460465470475(~1102 trajectories)Step 450Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0500550600650700(~16 trajectories)Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0540550560570580590(~186 trajectories)Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0530535540545550555560565(~979 trajectories)Figure 19: Humanoid-v2 TRPO landscape concentration (see Figure 5 for a description).26
段落总结：Published as a conference paper at ICLR 20202,000 state-action pairs20,000 state-action pairs100,000

**********段落分割**********
Published as a conference paper at ICLR 20202,000 state-action pairs20,000 state-action pairs100,000 state-action pairsStep 0Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0110120130140150160170180190(~73 trajectories)Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0110120130140150160170(~735 trajectories)Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0110120130140150160170(~3911 trajectories)Step 150Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0420440460480500520540(~19 trajectories)Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0455460465470475480485490495(~209 trajectories)Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0460.0462.5465.0467.5470.0472.5475.0477.5480.0(~1062 trajectories)Step 300Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0540560580600620640660680(~17 trajectories)Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0530540550560570580590600610(~193 trajectories)Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0530540550560570580590600610(~990 trajectories)Step 450Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0500520540560580600620640(~16 trajectories)Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0540550560570(~182 trajectories)Gradient direction0.00.51.01.52.02.53.0Random direction0.00.51.01.52.02.53.0535540545550555560565570(~938 trajectories)Figure 20: Humanoid-v2 PPO landscape concentration (see Figure 5 for a description).27
段落总结：Published as a conference paper at ICLR 20202,000 state-action pairs20,000 state-action pairs100,000
