## Whale Alert API

In this API I will focus in analysis data from different blockchain's (BTC, ETH and etc) to look for insights in the crypto market.

### TODO's

- Analysis the flow of transactions (In principle this have a high correction with the price):
    - [x] from exchange to unknown wallet
    - [x] from exchange to exchange
    - [x] from unknown wallet to exchange
    - [x] from unknown wallet to unknown wallet

    NOTE: Here we are using the package ```notify2``` ( a package to display desktop notifications on Linux)
          [notify2 API documentation](https://notify2.readthedocs.io/en/latest/) to install ```pip install notify2``` to nofity the high value moved in one transaction by whale.


- Storage information to analysis the market and to search for standard or metrics to evaluate the ecosystem.
    - transaction (example):
        ```bash
        blockchain: ethereum
        symbol: ETH
        id: 1640685299
        transaction_type: transfer
        hash: 13ea6b3dc2f6bce12f40f4aa48462d308f7cd63906407767ea31a2aa7ae438d1
        from: {'address': '3c047b9dfa4fd8f812f264f1611b959a4dd980f8', 'owner_type': 'unknown', 'owner': ''}
        to: {'address': 'aa344f7b0f781c18f6fba768d5b85f46722b5955', 'owner_type': 'unknown', 'owner': ''}
        timestamp: 1625244742
        amount: 600
        amount_usd: 1264570.1
        transaction_count: 1
      ```
## Resource

- [Whale Alert API Documentation](https://docs.whale-alert.io/?_ga=2.18753593.1286745348.1624886898-1875508501.1610310849#introduction)
- [Whale Alert GitHub](https://github.com/stuianna/whaleAlert)
