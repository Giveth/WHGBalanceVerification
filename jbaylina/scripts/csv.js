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
    cb(null, records);
  });
};
