const tradeGoods = [
  'grain','salt','iron','horses','wine','wood','amber','stone','fish','spices',
  'elephants','papyrus','cloth','wild_game','precious_metals','steppe_horses','cattle',
  'earthware','dye','fur','olive','leather','base_metals','woad','marble','honey',
  'incense','hemp','vegetables','gems','camel','glass','silk','dates','sugar','cedar',
  'myrrh','cinnabar','lapis','jade','fruits','silphium'
];

const lowCutoff = 9;
const depth = 100;

function generateBinaryTree(good, start, end, indent = 12) {
  const space = ' '.repeat(indent);
  const mid = Math.floor((start + end) / 2);
  if (start === end) return `${space}add = ${start}\n`;

  return (
    `${space}if = {\n` +
    `${space}    limit = { trade_good_surplus = { target = ${good} value <= ${mid} } }\n` +
    generateBinaryTree(good, start, mid, indent + 4) +
    `${space}}\n` +
    `${space}else = {\n` +
    generateBinaryTree(good, mid + 1, end, indent + 4) +
    `${space}}\n`
  );
}

let output = ``;

for (const good of tradeGoods) {
  output += `trade_good_surplus_${good} = {\n`;
  output += `    value = 0\n`;
  output += `    if = { limit = { trade_good_surplus = { target = ${good} value > 0 } }\n`;

  // Linear check for 1–9
  for (let i = 1; i <= lowCutoff; i++) {
    const keyword = i === 1 ? 'if' : 'else_if';
    output += `        ${keyword} = { limit = { trade_good_surplus = { target = ${good} value = { ${i} ${i} } } } add = ${i} }\n`;
  }

  // Fallback: binary search for 10–100
  output += `        else = {\n`;
  output += generateBinaryTree(good, lowCutoff + 1, depth, 12);
  output += `        }\n`;

  output += `    }\n`;
  output += `}\n\n`;
}

console.log(output.trim());
