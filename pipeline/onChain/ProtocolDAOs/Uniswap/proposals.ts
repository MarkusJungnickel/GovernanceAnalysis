import axios from "axios";
import fs from "fs";
import Web3 from "web3";
const provider =
  "https://mainnet.infura.io/v3/95e70ba790e649eeb37d25fc31e1662d";
const web3 = new Web3(provider);
const graph =
  "https://api.thegraph.com/subgraphs/name/ianlapham/governance-tracking";
async function isContract(address: string) {
  const code = await web3.eth.getCode(address);
  return code != "0x";
}

async function proposalList() {
  fs.unlinkSync("./proposals.csv");
  await getProposals(0);
}

async function getProposals(i: number): Promise<any> {
  let returnValue: any[] = [];
  const proposalsQuery = `{
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
      query: proposalsQuery,
    })
    .then(async (res) => {
      const proposals: any[] = res.data.data.proposals;
      console.log("prop length: ", proposals.length);
      for (const prop of proposals) {
        let votesAgainstShare = 0;
        let votesForShare = 0;
        let count = 0;
        let votes = await getVotes(prop.id);
        votes.forEach((vote: any) => {
          count += 1;
          if (vote.support == true) {
            votesForShare += parseInt(vote.votes.toString());
          } else {
            votesAgainstShare += parseInt(vote.votes.toString());
          }
        });
        console.log(count);
        fs.appendFileSync("./proposals.csv", prop.id + ","); // 0
        fs.appendFileSync("./proposals.csv", prop.id + ","); // 1
        fs.appendFileSync("./proposals.csv", prop.id + ","); // 2
        fs.appendFileSync("./proposals.csv", prop.id + ","); // 3
        fs.appendFileSync("./proposals.csv", prop.forCount + ","); // 4
        fs.appendFileSync("./proposals.csv", prop.againstCount + ","); // 5
        fs.appendFileSync("./proposals.csv", votesForShare + ","); // 6
        fs.appendFileSync("./proposals.csv", votesAgainstShare + ","); //7
        fs.appendFileSync("./proposals.csv", prop.id + ","); //8
        fs.appendFileSync("./proposals.csv", prop.id + ","); //9
        fs.appendFileSync("./proposals.csv", "\n");
      }
      returnValue = proposals;
    })
    .catch((error) => {
      console.error(error);
    });
  return returnValue;
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
proposalList();
