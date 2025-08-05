let tradeGoods = [
  'grain',
  'salt',
  'iron',
  'horses',
  'wine',
  'wood',
  'amber',
  'stone',
  'fish',
  'spices',
  'elephants',
  'papyrus',
  'cloth',
  'wild_game',
  'precious_metals',
  'steppe_horses',
  'cattle',
  'earthware',
  'dye',
  'fur',
  'olive',
  'leather',
  'base_metals',
  'woad',
  'marble',
  'honey',
  'incense',
  'hemp',
  'vegetables',
  'gems',
  'camel',
  'glass',
  'silk',
  'dates',
  'sugar',
  'cedar',
  'myrrh',
  'cinnabar',
  'lapis',
  'jade',
  'fruits',
  'silphium',
];

let depth = 100;

let outgoing = `country_outgoing_trade_routes = {\n`;
for (let i = 0; i < tradeGoods.length; i++) {
  outgoing += `    if = { limit = { country_trade_good_exports = { target = ${tradeGoods[i]} value > 0 } }\n`;
  for (let j = 1; j <= depth; j++) {

    if (j % 10 === 0 && j < depth) {
      outgoing += `        else_if = {\n            limit = { country_trade_good_exports = { target = ${tradeGoods[i]} value < ${j + 10} } }\n`;
    }

    if (j >= 10 && j !== depth) {
      outgoing += `    `;
    }
    outgoing += `        `;
    if (j > 1 && (j % 10 !== 0 || j === depth)) {
      outgoing += `else_`;
    }
    outgoing += `if = { limit = { country_trade_good_exports = { target = ${tradeGoods[i]} value ${j === depth ? `>= ${j}` : `= { ${j} ${j} }` } } } add = ${j} }\n`;

    if (j > 9 && j % 10 === 9) {
      outgoing += `        }\n`;
    }
  }
  outgoing += `    }\n`;
}
outgoing += `}`;

incoming = `country_incoming_trade_routes = {\n`;
for (let i = 0; i < tradeGoods.length; i++) {
  incoming += `    if = { limit = { country_trade_good_imports = { target = ${tradeGoods[i]} value > 0 } }\n`;
  for (let j = 1; j <= depth; j++) {

    if (j % 10 === 0 && j < depth) {
      incoming += `        else_if = {\n            limit = { country_trade_good_imports = { target = ${tradeGoods[i]} value < ${j + 10} } }\n`;
    }

    if (j >= 10 && j !== depth) {
      incoming += `    `;
    }
    incoming += `        `;
    if (j > 1 && (j % 10 !== 0 || j === depth)) {
      incoming += `else_`;
    }
    incoming += `if = { limit = { country_trade_good_imports = { target = ${tradeGoods[i]} value ${j === depth ? `>= ${j}` : `= { ${j} ${j} }` } } } add = ${j} }\n`;

    if (j > 9 && j % 10 === 9) {
      incoming += `        }\n`;
    }
  }
  incoming += `    }\n`;
}
incoming += `}`;

console.log(outgoing + '\n\n' + incoming);