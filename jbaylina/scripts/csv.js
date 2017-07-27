const fs = require('fs');

exports.load = (file, cb) => {
  const records = [];
  fs.readFile(file, 'utf8', (err, data) => {
    if (err) {
      cb(err);
      return;
    }
    const lines = data.split('\n');
    const fields = lines[0].split(',');
    for (let i = 1; i < lines.length; i += 1) {
      if (lines[i] !== '') {
        const values = lines[i].split(',');
        const r = {};
        for (let j = 0; j < fields.length; j += 1) {
          if (typeof values[j] === 'string') {
            values[j] = values[j].replace(/"/g, '');
          }
          r[fields[j]] = values[j];
        }
        records.push(r);
      }
    }
    cb(null, records);
  });
};

exports.save = (file, fields, objs, cb) => {
  const lines = [];
  let i;
  let j;
  lines.push(fields.join('\t'));
  for (i = 0; i < objs.length; i += 1) {
    const record = [];
    for (j = 0; j < fields.length; j += 1) {
      record.push("'" + objs[i][fields[j]]);
    }
    lines.push(record.join('\t'));
  }
  const out = lines.join('\n');
  fs.writeFile(file, out, 'utf8', cb);
};
