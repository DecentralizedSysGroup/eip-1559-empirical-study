# open source repository for paper ``Empirical Analysis of EIP-1559``
This repository is an open source repository for the data and data collection related code for the paper ``Empirical Analysis of EIP-1559: Transaction Fees, Waiting Time, and Consensus Security``. This paper has been accepted by ACM CCS 2022 and you can find the paper [here](https://arxiv.org/abs/2201.05574).

In this archive we provide the raw data we collected (after compressing), the code for collecting and processing the data, and the processed data for further analysis.

## data

### ``rawdata``

The compressed raw data are stored in the ``rawdata`` folder. After unzip the archive file ``compressed.zip``, you can see several ``.txt`` file, each of which indicates the time of receipt of all transactions received by a particular full node within 15 days. For example, the file ``LA_[2021070100,2021071600)_compressed.txt`` means it is the dataset for the full node in LA with time interval from July 1, 2021 to July 16, 2021.

Each line of these files describes a transaction, the following is an example:

```
0x16d1f71ef96c9456dc465ee2ce4d106b0dda0d440380c1cdd053c9deb58d8284 1626418821.870
```

This line means that the node receives transaction ``0x16...`` at Unix timestamp ``1626418821.870``.

### ``blockdata``

The code ``waitingtime.py`` processes the raw data, which generates two files, one is the block information database, and the other is the detailed transaction waiting time table. These outputs are stored in the ``blockdata`` folder.

### ``MEVdata``

The code ``mev.py`` calls the Flashbots API to obtain data from Flashbots, and combines the data on the Blockchain to generate the source distribution of miner's revenue for each block. The output is saved in the folder ``MEVdata``.

### ``MEVfig``

The code ``mevpaint.py`` reads the distribution of miner's revenue from ``MEVdata`` and draws pictures and tables. These contents are saved in the ``MEVfig`` folder.
