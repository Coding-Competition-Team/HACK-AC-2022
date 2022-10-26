const readline = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout,
});

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

flag = "ACSI{REDACTED}"

function main() {
  console.log("I just love adding 1 to any integer...")
  readline.question("Give me an integer!\n> ", async input => {
    // in case the integer is too big... shld be all good :)
    if (input.length <= 16) {
      // small enough
      input = parseInt(input);
      result = input + 1;

      console.log(`And the answer is... ${result}!!`);
      console.log(`${input} + 1 = ${result}`);
      await sleep(3000);

      if (input === result) {
        console.log("wait...");
        await sleep(3000);
        console.log(`Today ends my +1 career. Here's the flag: ${flag}`);
      } else {
        console.log("Yes, that's right. I applaud my excellent math.");
      }
    } else {
      // it's too big! i can't handle it!
      console.log("It's too big... I can't handle it :(");
    }
    readline.close();
  });
}

main();
