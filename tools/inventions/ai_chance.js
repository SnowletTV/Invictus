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

function toStringFloat(percent) {
  return `0.${percent < 0.1 ? `0` : ``}${percent}`;
}

let script_values = ``;

for (let percent of percents) {
  if (percent === 100) {
    script_values += 
    `ai_invention_chance_${percent} = { ` +
      `value = 99999999 ` +
    `}\n`;
  } else {
    script_values += 
    `ai_invention_chance_${percent} = { ` +
      `value = num_inventions_to_choose_from_minus_1 ` +
      `divide = ${toStringFloat(100 - percent)} ` +
      `subtract = num_inventions_to_choose_from_minus_1 ` +
    `}\n`;
  }

  for (let target of percents) {
    if (percent >= target) {
      continue;
    }
    script_values += 
    `ai_invention_chance_from_${percent}_to_${target} = { ` +
      `value = ai_invention_chance_${target} ` +
      `divide = ai_invention_chance_${percent} ` +
    `}\n`;
  }
}

console.log(script_values);