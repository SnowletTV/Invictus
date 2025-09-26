function generateBinaryDistanceScript(min, max, indent = 0) {
  const space = ' '.repeat(indent);
  const mid = Math.floor((min + max) / 20) * 10; // round to nearest 10

  if (max - min <= 10) {
    return (
      space +
      `value = ${Math.max(0, min - 5)}\n`
    );
  }

  return (
    `${space}if = {\n` +
    `${space}    limit = { distance_from = { province = scope:target_province value <= ${mid} } }\n` +
    generateBinaryDistanceScript(min, mid, indent + 4) +
    `${space}}\n` +
    `${space}else = {\n` +
    generateBinaryDistanceScript(mid + 10, max, indent + 4) +
    `${space}}\n`
  );
}

// Usage
const minDistance = 10;
const maxDistance = 5000;
const scriptValue =
  `script_value = {\n` +
  generateBinaryDistanceScript(minDistance, maxDistance, 4) +
  `}\n`;

console.log(scriptValue);
