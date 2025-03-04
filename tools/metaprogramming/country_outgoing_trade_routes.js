
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
let script_value = `country_outgoing_trade_routes = {\n`;
for (let i = 0; i < tradeGoods.length; i++) {
  script_value += `    if = { limit = { country_trade_good_exports = { target = ${tradeGoods[i]} value > 0 } }\n`;
  for (let j = 1; j <= depth; j++) {
    script_value += `        `;
    if (j > 1) {
      script_value += `else_`;
    }
    script_value += `if = { limit = { country_trade_good_exports = { target = ${tradeGoods[i]} value ${j === depth ? `>= ${j}` : `= { ${j} ${j} }` } } } add = ${j} }\n`;
  }
  script_value += `    }\n`;
}
script_value += `}`;

console.log(script_value);