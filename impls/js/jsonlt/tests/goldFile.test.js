const fs = require('fs');
const path = require('path');
const { transform } = require('../src/index');
const { evaluateCondition } = require('../src/xform');

function findTestfilesFolder() {
  let currentDir = __dirname;
  while (true) {
    if (fs.existsSync(path.join(currentDir, 'testfiles'))) {
      return path.join(currentDir, 'testfiles');
    }
    const parentDir = path.dirname(currentDir);
    if (parentDir === currentDir) {
      throw new Error("Could not find 'testfiles' folder");
    }
    currentDir = parentDir;
  }
}

describe('JSON file tests', () => {
  const testFolder = findTestfilesFolder();
  const jsonFiles = fs.readdirSync(testFolder).filter(file => file.endsWith('.json'));

  test.each(jsonFiles)('%s', (filename) => {
    const filePath = path.join(testFolder, filename);
    const testCase = JSON.parse(fs.readFileSync(filePath, 'utf8'));

    const inputData = testCase.input;
    const jsonltConf = testCase.jsonlt;
    const expectedOutput = testCase.output;

    const result = transform(inputData, jsonltConf);

    expect(result).toEqual(expectedOutput);
  });

  test('At least one test file was found', () => {
    expect(jsonFiles.length).toBeGreaterThan(0);
  });
});

describe('evaluateCondition', () => {
  test('not operator works correctly', () => {
    const data = { age: 25 };
    const condition = {
      operator: 'not',
      left: {
        operator: 'lt',
        left: 'age',
        right: 18
      }
    };
    expect(evaluateCondition(condition, data)).toBe(true);

    const falseCondition = {
      operator: 'not',
      left: {
        operator: 'gt',
        left: 'age',
        right: 18
      }
    };
    expect(evaluateCondition(falseCondition, data)).toBe(false);
  });
});
