# Governance Analysis

## Pipeline

The pipline contains the TypeScript scripts that are used to querey the smart contracts and the subgraphs. Running the scripts will produce csv files, which can then be analysed. The subgraph queries were posted using Axios and the smart contract calls are run through web3.js.

## Analysis

The analysis contains python scripts used to analyse the data stored in the csv files. The scripts rely on a variety of libraries including Matplot, Seaborn and NetworkX.
