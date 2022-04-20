# On-Chain Analysis for blockchain data using the Whale Alert API framework in python.

A simple tutorial of how to implement On-Chain Analysis for one
specific metric called Inflow and 
Outflow transactions of BTC to exchanges using the [Whale Alert API](https://docs.whale-alert.io/#introduction). In the market is a 
consensus that this metric shows a correlation with the price of BTC. I am not an expert in On-Chain Analysis, this is one way to work around with topic and to learn and to study more about it.

I strong recomend NOT to use this tutorial to make an investiment decision, and the proposal of this example is to study the topic only.

<!--
Hi, I am a Bitcoin enthusiastic and maximalist (almost 99%) and since 2017 I started reading and studying about the crypto market, and now I still reading and studying more and more about it, because I believe what Bitcoin did for the first time in human history. Below the best description that I see so far about Bitcoin:

![](images/btc_fundamentals.png)

```bash
In 2008 a person or group of people using pseudonym
Satoshi Nakamoto proposed a decentralized peer-to-peer system 
for making and processing payments a key challenge in digital 
payments is to prevent the same assets from being spent twice 
the bitcoin white paper proposed a novel method for validating 
transactions using crytography that address the so-called double 
spend problem this and other innovations related to distributed 
ledger technology are the foundation for based digital assets.
```
-->

In this article, I will explain and show how to use the [Whale Alert API](https://docs.whale-alert.io/#introduction) to track transaction history data and to make your own analysis from differents blockchains, like Bitcoin, Ethereum, Ripple and others, for more information read the documentation [Whale Alert API](https://docs.whale-alert.io/#introduction).

In the implementation I will focus **On Chain Analysis** of the BTC blockchain transaction data to look deep dive into **the metric Inflow and Outflow of BTCs**:

- ```from exchange to unknown(wallet)```
- ```from exchange to exchange```
- ```from unknown to exchange```
- ```from unknown(wallet) to unknown(wallet)```

This metric shows a correlation with the price of BTC, because more BTCs flowing to the exchanges, there are a high probability that these BTCs can be sold in the market, i.e. a high strong BTC sales pressure making the price go down, and by the contrary, we expect the price go up, because a high flow of BTCs are going out from exchange to unknown(wallet):

In Summary for this article, I will describe how to build the framework(Using one python package avaliable) to get the data and to make the analysis:

- [Setting the environment to build the framework]()
- [Build the API using the Whale Alert framework to get BTC blockchain transaction data]().
- [Analysis the data, making plots to compare the Inflow and Outflow of BTCs and search one way to quantify a correlation with the price]().

**NOTE**: For this tutorial I will use the Linux Ubuntu 20 to do everything. If you are using Windows the commands will be similars and check on the internet to see how to make tutorial in Windows installed the framework to develop this API.


### 1 - Setting the environment to build the framework API.

First, you need to have the python and pip installed:

```bash
# if you do not have pip installed. 
# you can install it using the CLI - Install python 3
$ sudo apt install -y python3-pip

# packages and development tools to install
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev

# Ubuntu 20:
# # https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-20-04-server

# python version
$ python --version
Python 3.9.7

# pip version
$ pip -V          
pip 21.2.4 from ~/anaconda3/lib/python3.9/site-packages/pip (python 3.9)
```

I strong suggest to create python virtual environment to be a self-contained directory tree that includes a Python installation and number of additional packages(This is good practice when you are developing a project, to know more about see the article [A Guide to Python Good Practices](https://towardsdatascience.com/a-guide-to-python-good-practices-90598529da35)). Below I will the main steps to make this:

let's begin by installing the ```python3-venv```  package that provides the ```venv``` module

```bash
$ sudo apt install python3-venv
```

If the installation was sucessfully, we can now to create your new virtual environment:

```bash
# Here you can change the name of the project as you like :)
# I am called the project of 'api-blockchain-data'

$ python3 -m venv api-blockchain-data
```

## References

- [Bitcoin: A Peer-to-Peer Electronic Cash System](https://bitcoin.org/bitcoin.pdf)
- [The Bitcoin Standard: The Decentralized Alternative to Central Banking](https://www.resistance.money/research/library/to%20be%20organised%20better/The%20Bitcoin%20Standard.pdf)
- [The Scalability Trilemma in Blockchain](https://aakash-111.medium.com/the-scalability-trilemma-in-blockchain-75fb57f646df)
- [On Sound Money](https://medium.com/galaxy-digital-research/on-sound-money-afc0619697b3)
- [BITCOIN’S ON-CHAIN MARKET CYCLES](https://bitcoinmagazine.com/markets/bitcoins-on-chain-market-cycles)