const percents = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 99, 100];
const num_buildings_to_choose_from = 8;

function calculateValue(percent) {
  return percent === 100
    ? 99999999
    : (num_buildings_to_choose_from - 1) / (1 - percent / 100) - (num_buildings_to_choose_from - 1);
}

function roundFloat(value, precision) {
  return parseFloat(value.toFixed(precision));
}

const rawCache = {};
const roundedCache = {};
let script = ``;

for (const p of percents) {
  const raw = calculateValue(p);
  rawCache[p] = raw;
  roundedCache[p] = roundFloat(raw, 4);
}

for (const percent of percents) {
  script += `brc_${percent} = ${roundedCache[percent]}\n`;

  for (const target of percents) {
    if (target <= percent) continue;
    const ratio = roundFloat(rawCache[target] / rawCache[percent], 4);
    script += `brc_from_${percent}_to_${target} = ${ratio}\n`;
  }
}

console.log(script.trim());
