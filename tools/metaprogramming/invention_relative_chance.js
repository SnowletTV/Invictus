const percents = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 99, 100];
const num_inventions_to_choose_from = 20;

function roundFloat(value, precision) {
  return parseFloat(value.toFixed(precision));
}

function calculateValue(percent) {
  return percent === 100
    ? 99999999
    : (num_inventions_to_choose_from - 1) / (1 - percent / 100) - (num_inventions_to_choose_from - 1);
}

const rawCache = {};
const roundedCache = {};
let output = ``;

// Cache all raw and rounded values
for (const percent of percents) {
  const raw = calculateValue(percent);
  rawCache[percent] = raw;
  roundedCache[percent] = roundFloat(raw, 4);
}

// Emit script values
for (const percent of percents) {
  output += `irc_${percent} = ${roundedCache[percent]}\n`;

  for (const target of percents) {
    if (target <= percent) continue;
    const ratio = roundFloat(rawCache[target] / rawCache[percent], 4);
    output += `irc_from_${percent}_to_${target} = ${ratio}\n`;
  }
}

console.log(output.trim());
