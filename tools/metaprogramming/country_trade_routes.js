const tradeGoods = [
  'grain', 'salt', 'iron', 'horses', 'wine', 'wood', 'amber', 'stone', 'fish', 'spices',
  'elephants', 'papyrus', 'cloth', 'wild_game', 'precious_metals', 'steppe_horses', 'cattle',
  'earthware', 'dye', 'fur', 'olive', 'leather', 'base_metals', 'woad', 'marble', 'honey',
  'incense', 'hemp', 'vegetables', 'gems', 'camel', 'glass', 'silk', 'dates', 'sugar', 'cedar',
  'myrrh', 'cinnabar', 'lapis', 'jade', 'fruits', 'silphium'
];

const depth = 100;
const cutoff = 9; // cutoff for linear evaluation

function generateBinaryTree(start, end, good, type, indent = 12) {
  const space = ' '.repeat(indent);
  const mid = Math.floor((start + end) / 2);
  if (start === end) return `${space}add = ${start}\n`;

  return (
    `${space}if = {\n` +
    `${space}    limit = { country_trade_good_${type} = { target = ${good} value <= ${mid} } }\n` +
    generateBinaryTree(start, mid, good, type, indent + 4) +
    `${space}}\n` +
    `${space}else = {\n` +
    generateBinaryTree(mid + 1, end, good, type, indent + 4) +
    `${space}}\n`
  );
}

function generateTradeTree(type, funcName) {
  let out = `${funcName} = {\n    value = 0\n`;

  for (const good of tradeGoods) {
    out += `    if = { limit = { country_trade_good_${type} = { target = ${good} value > 0 } }\n`;

    // Fast early linear check for 1–9
    for (let i = 1; i <= cutoff; i++) {
      const keyword = i === 1 ? 'if' : 'else_if';
      out += `        ${keyword} = { limit = { country_trade_good_${type} = { target = ${good} value = { ${i} ${i} } } } add = ${i} }\n`;
    }

    // Fallback to binary tree from 10–100
    out += `        else = {\n`;
    out += generateBinaryTree(cutoff + 1, depth, good, type, 12);
    out += `        }\n`;

    out += `    }\n`;
  }

  out += `}`;
  return out;
}

const outgoing = generateTradeTree("exports", "country_outgoing_trade_routes");
const incoming = generateTradeTree("imports", "country_incoming_trade_routes");

console.log(outgoing + '\n\n' + incoming);
