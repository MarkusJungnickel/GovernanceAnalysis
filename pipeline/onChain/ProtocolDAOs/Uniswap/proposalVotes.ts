import axios from "axios";
import fs from "fs";
import Web3 from "web3";
const provider =
  "https://patient-crimson-wave.quiknode.pro/97c31f01dc8e96ff9a2997208a4fd86a31b4fce8/";
const web3Provider = new Web3.providers.HttpProvider(provider);
const web3 = new Web3(provider);
const graph =
  "https://api.thegraph.com/subgraphs/name/ianlapham/governance-tracking";

async function getProposals() {
  fs.unlinkSync("./proposalVotes.csv");
  const proposal = `{
    proposals {
      forCount
      id
      againstCount
      votes {
        votes
        votesRaw
        id
        support
        voter {
          delegatedVotes
        }
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
        const votes = await getVotes(proposal.id);
        let count = 0;
        for (const vot of votes) {
          fs.appendFileSync("./proposalVotes.csv", vot.id + ",");
          count += 1;
        }
        console.log(count);
        fs.appendFileSync("./proposalVotes.csv", "\n");
      }
    })
    .catch((error) => {
      console.error(error);
    });
}

async function getVotes(id: any) {
  let returnValue: any[] = [];
  console.log("prop id: ", id);
  const votesQuery = `{votes(first: 1000, where: {proposal: "${id}"}) {
    id
    support
    votes
  }}`;
  await axios
    .post(graph, {
      query: votesQuery,
    })
    .then(async (res) => {
      const votes: any[] = res.data.data.votes;
      returnValue = votes;
      console.log(votes.length);
    })
    .catch((error) => {
      console.error(error);
    });
  return returnValue;
}

getProposals();
