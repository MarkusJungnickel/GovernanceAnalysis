import axios from "axios";
import fs from "fs";
import Web3 from "web3";
const provider =
  "https://patient-crimson-wave.quiknode.pro/97c31f01dc8e96ff9a2997208a4fd86a31b4fce8/";
const web3Provider = new Web3.providers.HttpProvider(provider);
const web3 = new Web3(provider);
const graph = "https://api.thegraph.com/subgraphs/name/aave/governance-v2";

async function getProposals() {
  // fs.unlinkSync("./proposalVotes.csv");
  const proposal = `{
    proposals(skip: 0, first: 1000) {
      id
      govContract
      state
      creator
      totalCurrentVoters
      currentYesVote
      currentNoVote
      totalVotingSupply
      winner
      startBlock
      votes{
        id
        votingPower
        support
      }
      
    }
  }`;
  await axios
    .post(graph, {
      query: proposal,
    })
    .then(async (res) => {
      const proposals = res.data.data.proposals;
      //writeProposalSummary(proposals);
      for (const proposal of proposals) {
        fs.appendFileSync("./proposalVotes.csv", proposal.id + ",");
        const votes = proposal.votes;
        for (const vot of votes) {
          fs.appendFileSync("./proposalVotes.csv", vot.id + ",");
        }
        fs.appendFileSync("./proposalVotes.csv", "\n");
      }
    })
    .catch((error) => {
      console.error(error);
    });
}

getProposals();
