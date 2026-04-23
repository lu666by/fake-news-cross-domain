# 文献综述草稿（中文）

## 1. 数据集背景：LIAR

本项目当前阶段主要用 **LIAR** 数据集来做假新闻检测的 baseline。LIAR 是 Wang（2017）提出的一个政治陈述数据集，数据来自 PolitiFact。这个数据集和普通新闻分类不太一样，它的文本通常都很短，更像是一个一个独立的 statement，而不是完整的新闻文章。也正因为这样，模型能利用的表面信息比较少，任务本身也会更难。

LIAR 原始是 **6 分类**。在这个项目里，我先把它改成了 **二分类**，因为这样更适合当前 baseline 阶段。具体来说，`true`、`mostly-true` 和 `half-true` 被归到 **REAL**，`barely-true`、`false` 和 `pants-fire` 被归到 **FAKE**。这种处理方式可以让模型比较更清楚，但也带来了一个问题，就是两类之间的边界会变得比较窄。像 `half-true` 和 `barely-true` 这种本来就比较靠近边界的标签，在二分类里更容易让模型混淆。

所以我觉得，LIAR 很适合作为 dissertation 当前阶段的数据集。一方面，它本身是一个比较经典、也比较有代表性的 benchmark；另一方面，它又不是一个太容易的数据集，能够比较真实地反映 sparse baseline 和 transformer baseline 在短政治陈述场景下到底能做到什么程度。

## 2. 模型与方法依据：BERT 和 weighted loss

在当前 baseline 线里，一个核心模型是 **BERT**（Devlin et al., 2019）。BERT 现在基本已经是文本分类里最常见的 transformer baseline 之一了，所以把它放进这个项目里是很自然的。对我这个项目来说，BERT 的作用主要是提供一个比 TF-IDF 更强的神经基线，看 contextual representation 能不能帮助模型更好地判断 statement 的真假。

不过，从当前实验结果来看，换成更强的 transformer 并不意味着问题就一下子解决了。LIAR 里的很多 statement 都很短，而且有些表述本身就比较模糊，还经常依赖额外的政治背景或事实背景。这些信息如果不在文本里，模型就很难完全判断清楚。所以从 TF-IDF 到 BERT，性能确实有提升，但这个提升更像是“有意义但不夸张”，而不是那种特别大的跳跃。

除了 backbone 本身，另一个很重要的问题是 **class imbalance / class-sensitive behaviour**。在当前的 LIAR 二分类实验里，一个比较明显的现象是，模型通常更容易识别 **REAL**，而 **FAKE** 这一类更难抓住。所以我后来引入了 **weighted loss**。class imbalance 相关文献也支持这种做法，因为加权损失本质上就是让模型在训练时更重视某一类错误。对这个项目来说，它的意义不是单纯去追更高的 accuracy，而是希望模型对 **FAKE** 更敏感，尽量少漏掉 fake。

这也决定了我后面怎么评价模型。如果只看 accuracy，其实很容易把两个类别之间的差别盖过去。所以这个项目除了 accuracy，也特别看 **macro-F1** 和 **FAKE recall**。尤其是 FAKE recall，它更能体现 weighted training 到底有没有真的改变模型行为，而不是只让 overall 分数有一点点变化。

## 3. 稳健性与跨数据集动机

这个 dissertation 后面真正想做的，不只是把 LIAR 上的 in-domain 分数继续往上推，而是去看模型在 **cross-dataset / cross-domain** 场景下到底能不能泛化。这一点和 robustness literature 是对得上的。Wang, Wang, and Yang（2022）提到，一个模型在同分布测试集上表现很好，并不代表它真的 robust。很多时候，模型只是学到了某个数据集里特有的模式、偏差或者一些 transfer 不出去的线索。一旦换一个数据集，性能就会掉下来。

我觉得这一点对 fake news detection 特别重要。因为不同数据集之间差别通常都不小，比如文本长度、主题分布、标签设计、来源类型，还有标注方式都可能不一样。所以一个模型在某个 benchmark 上表现不错，不代表它在另一个数据集上也会同样有效。也正因为这样，cross-dataset evaluation 对这个项目来说不是一个“附加实验”，而是后面很关键的一步。

近年的一些 fake news detection 论文也说明了这一点。有些工作会用多个 fake news 数据集来评估 transformer 或 LLM-assisted 方法，这说明现在讨论 fake news detection，已经不能只看一个 benchmark 了。不过这里也要区分清楚：**用多个数据集分别做实验**，和 **train on one dataset, test on another dataset** 其实不是一回事。前者更像 multi-dataset evaluation，后者才更接近我这个 dissertation 后面想做的 strict cross-dataset transfer。

所以从目前这些文献来看，我觉得这个项目的路线是比较清楚的：先在 LIAR 上把 in-domain baseline 线建立起来，再通过 class-sensitive metrics 和 error analysis 去理解模型为什么会这样表现，最后再进入 cross-dataset 阶段，把重点从“哪个模型在单一数据集上分高一点”转到“哪个模型在数据分布变化时更能泛化”。
