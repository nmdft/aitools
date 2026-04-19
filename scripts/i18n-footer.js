// i18n: Localize footer for Chinese pages
'use strict';

var fs = require('fs');
var path = require('path');

hexo.extend.filter.register('after_generate', function() {
  var publicDir = hexo.public_dir.toString().replace(/\/$/, '');

  setTimeout(function() {
    function walkDir(dir) {
      var files = [];
      try {
        fs.readdirSync(dir).forEach(function(entry) {
          var fullPath = path.join(dir, entry);
          try {
            var stat = fs.statSync(fullPath);
            if (stat.isDirectory()) files = files.concat(walkDir(fullPath));
            else if (entry.endsWith('.html')) files.push(fullPath);
          } catch(e) {}
        });
      } catch(e) {}
      return files;
    }

    var count = 0;
    walkDir(publicDir).forEach(function(filePath) {
      var html;
      try { html = fs.readFileSync(filePath, 'utf8'); } catch(e) { return; }
      if (!html) return;

      var relPath = path.relative(publicDir, filePath).replace(/\\/g, '/');
      if (relPath.indexOf('zh/') !== 0) return;

      var modified = false;

      // Replace footer text
      if (html.indexOf('Honest AI Tool Reviews for Solopreneurs') !== -1) {
        html = html.replace(/Honest AI Tool Reviews for Solopreneurs/g, '一人公司 AI 工具评测');
        modified = true;
      }

      // Set html lang
      if (html.indexOf('<html lang="en"') !== -1) {
        html = html.replace(/<html[^>]*lang="en"[^>]*>/, '<html lang="zh-CN">');
        modified = true;
      }

      if (modified) {
        fs.writeFileSync(filePath, html, 'utf8');
        count++;
      }
    });

    hexo.log.info('i18n footer: localized ' + count + ' Chinese pages');
  }, 500);
});
