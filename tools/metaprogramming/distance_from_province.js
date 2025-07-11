let depth = 5;
let script_value = `distance_from_province = {\n`;
for (let k = 1; k <= depth; k++) {
  script_value += `    `;
  if (k === depth) {
    script_value +=
    `else = {\n`;
  } else {
    if (k > 1) {
      script_value +=
      `else_`;
    }
    script_value +=
    `if = { limit = { distance_from = { province = scope:target_province value <= ` + (k * 1000) + ` } }\n`;
  }

  for (let i = 1; i <= 10; i++) {
    script_value += `        `;
    if (i === 10) {
      script_value +=
      `else = {\n`;
    } else {
      if (i > 1) {
        script_value +=
        `else_`;
      }
      script_value +=
      `if = { limit = { distance_from = { province = scope:target_province value <= ` + ((k - 1) * 1000 + i * 100) + ` } }\n`;
    }
    
    for (let j = 1; j <= 10; j++) {
      let distance = ((k - 1) * 1000 + (i - 1) * 100 + j * 10);

      script_value += `            `;
      if (j === 10) {
        script_value +=
        `else = {` + checkIfBelowOrAboveFive(distance) + `            }\n`;
      } else {
        if (j > 1) {
          script_value +=
          `else_`;
        }
        script_value +=
        `if = { limit = { distance_from = { province = scope:target_province value <= ` + distance + ` } }` + checkIfBelowOrAboveFive(distance) + `            }\n`;
      }
    }

    script_value +=
    `        }\n`;
  }
  script_value += `    }\n`;
}
script_value += `}\n`;

console.log(script_value);

function checkIfBelowOrAboveFive(value) {
  return `\n                if = { limit = { distance_from = { province = scope:target_province value <= ` + (value - 5) + ` } } value = ` + (value - 5) + ` }\n                else = { value = ` + value + ` }\n`;
}