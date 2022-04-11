# open source repository for paper ``Empirical Analysis of EIP-1559``

This repository holds the data and code used for the paper ``Empirical Analysis of EIP-1559: Transaction Fees, Waiting Time, and Consensus Security``. This paper has been accepted by ACM CCS 2022 and you can find the paper [here](https://arxiv.org/abs/2201.05574).


## Summary

Yuxuan: please finish the following summary.

- Waiting time (Section 5.3): File X contains data used for waiting time analysis.
- Network spikes (Table 4): File X contains data for Table 4.
- Miner's revenue (Fig 11 & 12): File X contains data for Fig 11 & 12.

## Reproducing results from the raw data

In this archival, we provide the raw data we collected (after compressing), the code for collecting and processing the data, and the processed data for further analysis.

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

To reproduce the data, you can use the following command.

```bash
./mev.py --data
```

When executing the `--data` command, `mev.py` will call the Flashbots API, combining data from Ethereum full nodes (via `web3_api.py`) to generate MEV raw data. This data will be saved in the `MEVdata` folder.

### ``MEVfig``

The code ``mev.py`` reads the distribution of miner's revenue from ``MEVdata`` and draws pictures and tables. These contents are saved in the ``MEVfig`` folder.

In `MEVfig`, you can find figure 11 and figure 12 of our paper. To reproduce the figure, you can use the following command.

```bash
./mev.py --csv;
./mev.py --img
```

When executing the `--csv` command, `mev.py` will read the MEV raw data in the `MEVdata` folder and output a table `MEVfig/MEVdata.csv` with all the data. When executing the `--img` command, `mev.py` will use the file `MEVfig/MEVdata.csv` to draw all the figures.
