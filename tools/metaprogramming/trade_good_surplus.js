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

let svalues = ``;
for (let i = 0; i < tradeGoods.length; i++) {
  svalues += `trade_good_surplus_${tradeGoods[i]} = {\n    value = 0\n    if = { limit = { trade_good_surplus = { target = ${tradeGoods[i]} value > 0 } }\n`;
  for (let j = 1; j <= depth; j++) {

    if (j % 10 === 0 && j < depth) {
      svalues += `        else_if = {\n            limit = { trade_good_surplus = { target = ${tradeGoods[i]} value < ${j + 10} } }\n`;
    }

    if (j >= 10 && j !== depth) {
      svalues += `    `;
    }
    svalues += `        `;
    if (j > 1 && (j % 10 !== 0 || j === depth)) {
      svalues += `else_`;
    }
    svalues += `if = { limit = { trade_good_surplus = { target = ${tradeGoods[i]} value ${j === depth ? `>= ${j}` : `= { ${j} ${j} }` } } } add = ${j} }\n`;

    if (j > 9 && j % 10 === 9) {
      svalues += `        }\n`;
    }
  }
  svalues += `    }\n}\n\n`;
}

console.log(svalues.trim());