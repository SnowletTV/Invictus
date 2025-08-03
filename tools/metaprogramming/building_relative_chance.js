// Steps to generate script values for
let percents = [
  5,
  10,
  15,
  20,
  25,
  30,
  35,
  40,
  45,
  50,
  55,
  60,
  65,
  70,
  75,
  80,
  85,
  90,
  95,
  99,
  100
];

function roundFloat(value, precision) {
  return parseFloat(value.toFixed(precision));
}

// Number of buildings that the country can choose out from at the moment
// Hardcoded for simplicity and performance
const num_buildings_to_choose_from = 8;

function calculateValue(percent) {
  // For 100% just get some really big number to soft-guarantee the building getting chosen
  if (percent === 100) {
    return 99999999;
  }
  // Otherwise calculate the chance. It's a simple calculation where we have x elements of 1 weight each, and then we
  // need to make one of the elements of a certain weight that would become x percent of the new combined weight.
  return (num_buildings_to_choose_from - 1) / (1 - percent / 100) - (num_buildings_to_choose_from - 1);
}

let script_values = ``;

for (let percent of percents) {
  // Add the script value itself
  script_values += `brc_${percent} = ${roundFloat(calculateValue(percent), 4)}\n`;

  // Add the multipliers so we could upgrade this percent to any of the higher percents
  for (let target of percents) {
    if (percent >= target) {
      continue;
    }
    script_values += `brc_from_${percent}_to_${target} = ${roundFloat(calculateValue(target) / calculateValue(percent), 4)}\n`;
  }
}

console.log(script_values.trim());