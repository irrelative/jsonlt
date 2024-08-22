const { Condition } = require('./schema');

function deepCopy(obj) {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  if (Array.isArray(obj)) {
    return obj.map(deepCopy);
  }

  const copy = {};
  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      copy[key] = deepCopy(obj[key]);
    }
  }
  return copy;
}

function renameTransformation(data, source, target) {
  if (source in data) {
    data[target] = data[source];
    delete data[source];
  }
  return data;
}

function reorderTransformation(data, order) {
  const reordered = {};
  for (const key of order) {
    if (key in data) {
      reordered[key] = data[key];
    }
  }
  return reordered;
}

function attributeToElementTransformation(data, source, target) {
  if (source in data) {
    data[target] = { [source]: data[source] };
    delete data[source];
  }
  return data;
}

function elementToAttributeTransformation(data, source, target) {
  const sourceParts = source.split('.');
  if (sourceParts.length === 2) {
    const [element, attribute] = sourceParts;
    if (element in data && typeof data[element] === 'object' && attribute in data[element]) {
      data[target] = data[element][attribute];
      delete data[element];
    }
  } else if (source in data && typeof data[source] === 'object') {
    data[target] = Object.values(data[source])[0];
    delete data[source];
  }
  return data;
}

function evaluateCondition(condition, data) {
  const ops = {
    eq: (a, b) => a === b,
    ne: (a, b) => a !== b,
    gt: (a, b) => a > b,
    lt: (a, b) => a < b,
    ge: (a, b) => a >= b,
    le: (a, b) => a <= b,
    and: (a, b) => a && b,
    or: (a, b) => a || b,
    not: a => !a
  };

  function resolveValue(value, data) {
    if (value instanceof Condition) {
      return evaluateCondition(value, data);
    } else if (typeof value === 'string') {
      const parts = value.split('.');
      let current = data;
      for (const part of parts) {
        if (typeof current === 'object' && part in current) {
          current = current[part];
        } else {
          const num = parseInt(value);
          return isNaN(num) ? value : num;
        }
      }
      return current;
    } else {
      return value;
    }
  }

  const left = resolveValue(condition.left, data);
  const right = condition.right !== undefined ? resolveValue(condition.right, data) : undefined;

  if (condition.operator === 'not') {
    return ops[condition.operator](left);
  } else {
    return ops[condition.operator](left, right);
  }
}

function conditionalTransformation(data, condition, trueTransformation, falseTransformation = null) {
  if (evaluateCondition(condition, data)) {
    return applyTransformation(data, trueTransformation);
  } else if (falseTransformation) {
    return applyTransformation(data, falseTransformation);
  }
  return data;
}

function mergeTransformation(data, sources, target) {
  function mergeRecursive(d) {
    const merged = {};
    const newD = {};
    for (const [key, value] of Object.entries(d)) {
      if (sources.includes(key)) {
        if (typeof value === 'object' && !Array.isArray(value)) {
          Object.assign(merged, value);
        } else {
          merged[key] = value;
        }
      } else {
        if (typeof value === 'object' && !Array.isArray(value)) {
          newD[key] = mergeRecursive(value);
        } else {
          newD[key] = value;
        }
      }
    }
    if (Object.keys(merged).length > 0) {
      newD[target] = merged;
    }
    return newD;
  }

  return mergeRecursive(data);
}

function splitTransformation(data, source, targets) {
  function splitRecursive(d) {
    if (source in d && typeof d[source] === 'object' && !Array.isArray(d[source])) {
      const sourceData = d[source];
      delete d[source];
      const sourceValues = Object.values(sourceData);
      targets.forEach((target, index) => {
        if (index < sourceValues.length) {
          d[target] = sourceValues[index];
        }
      });
    }
    for (const [key, value] of Object.entries(d)) {
      if (typeof value === 'object' && !Array.isArray(value)) {
        d[key] = splitRecursive(value);
      }
    }
    return d;
  }

  return splitRecursive(data);
}

function addElementTransformation(data, target, value) {
  data[target] = value;
  return data;
}

function removeElementTransformation(data, target) {
  if (target in data) {
    delete data[target];
  }
  return data;
}

function modifyTextTransformation(data, target, modification, replaceOld = null, replaceNew = null) {
  if (target in data && typeof data[target] === 'string') {
    switch (modification) {
      case 'uppercase':
        data[target] = data[target].toUpperCase();
        break;
      case 'lowercase':
        data[target] = data[target].toLowerCase();
        break;
      case 'capitalize':
        data[target] = data[target].charAt(0).toUpperCase() + data[target].slice(1);
        break;
      case 'title':
        data[target] = data[target].replace(/\w\S*/g, (txt) => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase());
        break;
      case 'strip':
        data[target] = data[target].trim();
        break;
      case 'replace':
        if (replaceOld !== null && replaceNew !== null) {
          data[target] = data[target].replace(new RegExp(replaceOld, 'g'), replaceNew);
        }
        break;
    }
  }
  return data;
}

function copyStructureTransformation(data, modifications) {
  const copiedData = deepCopy(data);
  for (const modification of modifications) {
    applyTransformation(copiedData, modification);
  }
  return copiedData;
}

function groupTransformation(data, source, target, groupBy) {
  if (source in data && Array.isArray(data[source])) {
    const grouped = {};
    for (const item of data[source]) {
      if (groupBy in item) {
        const key = item[groupBy];
        if (!(key in grouped)) {
          grouped[key] = [];
        }
        grouped[key].push(item);
      }
    }
    data[target] = grouped;
    delete data[source];
  }
  return data;
}

function concatTransformation(data, sources, target, delimiter = null) {
  const values = sources
    .filter(source => source in data)
    .map(source => String(data[source]));

  if (values.length > 0) {
    data[target] = delimiter !== null ? values.join(delimiter) : values.join('');
  }
  return data;
}

function applyPath(data, path, transformationFunc) {
  if (path === '.') {
    return transformationFunc(data);
  }

  const parts = path.split('.');
  let current = data;
  for (let i = 1; i < parts.length; i++) {
    const part = parts[i];
    if (part.endsWith('[]')) {
      const key = part.slice(0, -2);
      if (key in current && Array.isArray(current[key])) {
        current[key] = current[key].map(transformationFunc);
      }
      return data;
    } else if (part.endsWith(']')) {
      const [key, indexStr] = part.slice(0, -1).split('[');
      const index = parseInt(indexStr);
      if (key in current && Array.isArray(current[key]) && index >= 0 && index < current[key].length) {
        current[key][index] = transformationFunc(current[key][index]);
      }
      return data;
    } else if (i === parts.length - 1) {
      if (part in current) {
        current[part] = transformationFunc(current[part]);
      }
      return data;
    } else {
      if (!(part in current)) {
        current[part] = {};
      }
      current = current[part];
    }
  }

  return data;
}

function applyTransformation(data, transformation) {
  const path = transformation.path || '.';

  switch (transformation.type) {
    case 'rename':
      return applyPath(data, path, x => renameTransformation(x, transformation.source, transformation.target));
    case 'reorder':
      return applyPath(data, path, x => reorderTransformation(x, transformation.order));
    case 'attribute_to_element':
      return applyPath(data, path, x => attributeToElementTransformation(x, transformation.source, transformation.target));
    case 'element_to_attribute':
      return applyPath(data, path, x => elementToAttributeTransformation(x, transformation.source, transformation.target));
    case 'conditional':
      return applyPath(data, path, x => conditionalTransformation(x, new Condition(transformation.condition), transformation.true_transformation, transformation.false_transformation));
    case 'merge':
      return applyPath(data, path, x => mergeTransformation(x, transformation.sources, transformation.target));
    case 'split':
      return applyPath(data, path, x => splitTransformation(x, transformation.source, transformation.targets));
    case 'add':
      return applyPath(data, path, x => addElementTransformation(x, transformation.target, transformation.value));
    case 'remove':
      return applyPath(data, path, x => removeElementTransformation(x, transformation.target));
    case 'modify_text':
      return applyPath(data, path, x => modifyTextTransformation(x, transformation.target, transformation.modification, transformation.replace_old, transformation.replace_new));
    case 'copy_structure':
      return applyPath(data, path, x => copyStructureTransformation(x, transformation.modifications));
    case 'group':
      return applyPath(data, path, x => groupTransformation(x, transformation.source, transformation.target, transformation.group_by));
    case 'concat':
      return applyPath(data, path, x => concatTransformation(x, transformation.sources, transformation.target, transformation.delimiter));
    default:
      return data;
  }
}

function jsonltTransform(jsonData, jsonltConf) {
  let transformedData = deepCopy(jsonData);
  for (const transformation of jsonltConf.transformations) {
    transformedData = applyTransformation(transformedData, transformation);
  }
  return transformedData;
}

module.exports = {
  jsonltTransform
};
