import axios from "axios";
import fs from "fs";
import { exit } from "process";
import Web3 from "web3";
var gini = require("gini");
const provider =
  "https://mainnet.infura.io/v3/95e70ba790e649eeb37d25fc31e1662d";
const web3Provider = new Web3.providers.HttpProvider(provider);
const web3 = new Web3(provider);

async function memberList(): Promise<any> {
  // fs.unlinkSync("./shareTime.csv");
  fs.unlinkSync("./ids.csv");
  let count = 0;
  for (let block = 10861672; block < 15347898; block += 100000) {
    let lastId = "0x0000000000000000000000000000000000000000";
    let memberList: any[] = [];
    let cont = true;
    fs.appendFileSync("./shareTime.csv", block + ",");
    while (cont) {
      const members = `{
        tokenHolders(first: 1000, where: {id_gt: "${lastId}", tokenBalanceRaw_gt: "0"}, block: {number: ${block}}) {
          id
          tokenBalance
          tokenBalanceRaw
        }
      }`;
      await axios
        .post(
          "https://api.thegraph.com/subgraphs/name/ianlapham/governance-tracking",
          {
            query: members,
          }
        )
        .then(async (res) => {
          try {
            const members = res.data.data.tokenHolders;
            console.log("membr length", members.length);
            if (members.length <= 1) {
              cont = false;
            }
            for (const member of members) {
              count += 1;
              fs.appendFileSync("./shareTime.csv", member.tokenBalance + ",");
              fs.appendFileSync("./ids.csv", member.id + "\n");
              memberList.push(member.tokenBalance);
              lastId = member.id;
            }
            console.log(count);
          } catch (error) {
            console.log(error);
            console.log(count);
            exit(1);
          }
        })
        .catch((error) => {
          console.error(error);
        });
    }
    fs.appendFileSync("./shareTime.csv", "\n");
    fs.appendFileSync("./ids.csv", "\n");
    // const coefficients = getCos(memberList);
    // fs.appendFileSync("./gini.csv", block + ",");
    // fs.appendFileSync("./gini.csv", memberList.length + ",");
    // fs.appendFileSync("./gini.csv", coefficients[0] + ",");
    // fs.appendFileSync("./gini.csv", coefficients[1] + ",");
    // fs.appendFileSync("./gini.csv", "\n");
  }
}

memberList();
