/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import canStache from 'can-stache';
GGRC.Templates = GGRC.Templates || {};
GGRC.templates_path = '/static/templates';

let templates = require.context('./templates/', true, /\.stache/);

let prefix = './';
let postfix = '.stache';

templates.keys().forEach((key) => {
  let prefixPos = key.indexOf(prefix);
  let postfixPos = key.lastIndexOf(postfix);

  let newKey = key.slice(prefixPos + prefix.length, postfixPos);

  GGRC.Templates[newKey] = templates(key);

  let id = key.replace('./', `${GGRC.templates_path}/`);
  canStache.registerPartial(id, templates(key));
});
