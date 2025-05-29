# Passive vs Aggressive Strategies in High-Frequency Trading

## Introduction

When thinking about HFT strategies, a useful distinction is that of *passive* (or *making*) versus *aggressive* (or *taking*) strategies.

In his book *Trading at the Speed of Light: How Ultrafast Algorithms Are Transforming Financial Markets*, Donald Mackenzie describes how trading groups can often be categorized based on whether they focus on passive or aggressive strategies. 

> Often, though certainly not always, trading groups and sometimes even entire companies specialize in one or the other. For example, those interviewees who were sufficiently senior in compartmentalized companies—those made up of separate trading groups—to be familiar with those groups’ trading strategies reported that groups often focused either on making or on taking, but not both.
> 

Mackenzie further notes:

> There can be large differences among companies in the proportions of their algorithms’ trades that are making versus taking, differences that are broadly stable over time. It is unusual for a firm to mostly make in one month and take in the next.
> 

The fact that it is uncommon to mix the two types of strategies is attributed to the fact that passive strategies simply look very different from aggressive strategies. One of Mackenzie’s interviewees, who has a senior position at a trading firm, said the following:

> I think there is just something that’s so different about having to have an opinion all the time [a passive strategy] versus occasionally having an opinion [an aggressive strategy]… for some reason those two things can’t really be married without somehow ruining an aspect of the other one.
> 

As a result, the distinction between passive and aggressive strategies provides a useful framework through which to understand a particular trading firm’s activity. If one knows whether a trading team is focused on passive or aggressive strategies, there is a lot that can be subsequently inferred about the nature of that trading team’s operations. 

## Passive vs Aggressive

A **passive** strategy is one that relies on placing limit orders in the order book and waiting for them to be filled, while an **aggressive** strategy is one that relies on placing market orders that fill existing limit orders. Sometimes, passive strategies are described as “making” because they add liquidity, and aggressive strategies are described as “taking” because they remove liquidity. 

The simplicity of this distinction belies how different passive and aggressive strategies end up being. At first glance, it isn’t obvious that it would be difficult for a trading algorithm to rely on both limit orders and market orders. But we’ll soon see why this is the case. 

Most of the time, a passive algorithm is one engaged in market-making—the algorithm continuously posts both a bid and an ask in the order book, updating its prices frequently based on what it sees in the market. It doesn’t fill others’ orders; rather, it declares its willingness to buy and sell and waits for other market participants to engage with it. This is why the interviewee from earlier stated that a passive strategy must “have an opinion all the time”—it is always required to have quotes in the order book. 

An aggressive algorithm, on the other hand, doesn’t need to submit orders until it wants to. Most of the time, an aggressive algorithm is observing the market and performing quantitative analysis of what it sees. At some point, this analysis indicates that there is an opportunity to profit—the price is about to move. So the aggressive algorithm submits market orders, taking liquidity from the order book, and then profits when the market moves in its favor. 

Note: there is a certain class of aggressive strategies which aim to identify and pick off the stale quotes of other market participants before they have had time to update. Such strategies require little quantitative sophistication and are highly dependent on speed, and as such stand apart from most other aggressive strategies. For that reason, when we refer to aggressive strategies in this essay, we usually won’t be talking about these fast-and-dumb strategies. Yet it’s important to note that they exist. 

## Hitting Singles vs Hitting Home Runs

Because passive algorithms constantly have orders in the book and profit off of the spread, they tend to make a small amount of money on a very consistent basis. Aggressive algorithms, on the other hand, make no money most of the time, and then make a lot of money at once. It is common for a passive, market-making algorithm to operate in competition with an aggressive algorithm. If an aggressive algorithm is able to successfully out-predict a passive algorithm and buy/sell from it at a profit, the passive algorithm has been “run over” and ends up losing a significant amount of money. Mackenzie states that market-makers tend to simply accept that this will happen occasionally:

> No market-maker reported being able to entirely avoid being run over, but all try as hard as they can, often successfully, to ensure that the resultant losses do not fully cancel out the repeated small gains.
> 

Douglas Cifu, CEO of Virtu Financial, once described market-making as a business of “hitting singles.”

> We don’t try to hit doubles or triples or home runs. It’s really, really hard to be a consistent singles hitter.
> 

If it is the case that passive strategies aim to consistently hit singles, then aggressive strategies are those which aim to occasionally hit a home run. 

## Being Fast vs Being Smart

Perhaps the most important difference between passive and aggressive strategies is fact that passive strategies tend to be fast and dumb, and aggressive strategies tend to be smart and slow. 

A market-making algorithm must be fast in order to succeed. There are two main reasons for this. The first is that it must be able to update its quotes in real-time as quickly as possible to avoid losing money. If there is a signal in the market indicating that a price rise is imminent, a market-maker must adjust its prices to account for this before other market participants (including other HFT’s) fill its now-outdated offers. Having an opinion all the time necessitates being able to update your opinion as quickly as possible. 

The second reason for why speed is essential to a market-maker is because in most markets, orders at the same price level are arranged in a time-priority queue, meaning that if a market-maker wants its orders to be executed first at a particular price level, it must submit its orders before anyone else. This means that there are often races between different HFT’s to submit their orders as fast as possible to be in the front of the queue and thus be the first to have access to a profit opportunity. 

This requirement for speed does not exist for an aggressive algorithm. Once an aggressive algorithm identifies a profit opportunity, while it is important to act on this opportunity immediately, its ability to profit does not depend on submitting its orders as fast as is technologically possible. If an aggressive algorithm recognizes that a price movement will occur 1 second in the future, as long as its order arrives before that price movement occurs, any further speedup is unlikely to make a meaningful difference. As Mackenzie puts it, 

> There is… seldom a queue to “take.”
> 

For an aggressive strategy, the key demand is quantitative sophistication. Aggressive algorithms tend to process a large amount of data and employ advanced statistical techniques to predict price movements. Mackenzie describes one such algorithm that a firm uses to predict the price movements of Treasury futures in the Chicago Mercantile Exchange: 

> The algorithm will take into account the pattern of bids, offers, and trades in those futures, as well as patterns in the trading of the other Treasury and interest-rate futures also traded in that datacenter. The algorithm will receive, via microwave links, data on the buying and selling of the underlying Treasurys, which are traded in the two datacenters in New Jersey… Via Hibernia Atlantic’s ultrafast transatlantic cable, it will receive data on the trading of futures on UK sovereign bonds (these futures are traded in a datacenter just outside of London) and the equivalent German futures, traded in a datacenter in Frankfurt called FR2. Data on Japanese government bonds will come from a transpacific cable and yet more microwave links. The algorithm will continuously fuse all this information into a prediction of the price of the futures it is trading, taking when it looks profitable to do so.
> 

As  Mackenzie notes, it is simply not possible for a passive algorithm to perform quantitative analysis of this sophistication due to the requirement of speed: 

> All of this information is also available to market-making algorithms, at least those deployed by the larger HFT firms. Market-making algorithms, though, often have to be ultrafast (and therefore not too complex), because of their need to be at or close to the head of the time-priority queue for execution and the danger of their quotes becoming stale and being picked off…
> 

One of Mackenzie’s interviewees, who works at a market-making firm, described market-making as such:

> We add, subtract, multiply, and divide really, really well… We’re not doing high math and high quant.
> 

## Engineering vs Mathematics

The different demands of passive and aggressive algorithms produce a difference in the specializations of the teams and individuals working on such strategies. 

In addition to needing to be fast, market-making strategies must also be extremely robust. The fact that a market-maker must constantly update its bids and offers, typically for a variety of financial instruments and across many different markets, places them in a highly vulnerable position where any outage in their trading system, even lasting for only a few seconds, could result in disastrous losses. Failure is intolerable. The combined demands of extreme speed and extreme robustness result in the core challenge of building passive strategies being engineering the systems capable of executing them. 

Aggressive strategies, in contrast, do not tend to have an exceptional dependence on speed or robustness. As such, the core challenge of building aggressive strategies lies in developing the complex algorithms and mathematical models that power their price predictions. Mackenzie writes:

> Takers, we might say, can afford to concentrate on the mathematics of HFT, not on its engineering; makers need excellent engineering.
> 

## Conclusion

High-frequency trading is a rather opaque industry. Trading firms rarely publicize details of their operations, and it can be difficult to develop a satisfying understanding of the landscape of strategies employed across these firms. Though I had heard of the distinction between passive and aggressive strategies before, the thorough discussion of this distinction in *Trading at the Speed of Light* struck me as highly elucidating and conceptually useful. The substantial differences between passive trading and aggressive trading are reflections of dynamics and tradeoffs that are fundamental to HFT, and thus by understanding these differences, we gain deep insight into the nature of the industry as a whole.