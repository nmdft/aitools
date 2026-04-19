// Newsletter CTA injection
// Post-processes generated HTML files to inject newsletter signup CTA

'use strict';

var fs = require('fs');
var path = require('path');

hexo.extend.filter.register('after_generate', function() {
  var publicDir = hexo.public_dir.toString().replace(/\/$/, '');

  setTimeout(function() {
    var enCTA = '<div style="background:#f8f9fa;border:1px solid #e9ecef;border-radius:8px;padding:20px 24px;margin:24px 0;text-align:center;">' +
      '<p style="margin:0 0 12px;font-size:16px;font-weight:600;color:#333;">📬 Get honest AI tool reviews in your inbox</p>' +
      '<p style="margin:0 0 16px;font-size:14px;color:#666;">No spam. No sponsored fluff. Just real tool reviews for solopreneurs, once a week.</p>' +
      '<form action="https://buttondown.com/api/emails/embed-subscribe/aitools" method="post" target="popupwindow" onsubmit="window.open(\'https://buttondown.com/aitools\',\'popupwindow\')" style="display:inline-flex;gap:8px;flex-wrap:wrap;justify-content:center;">' +
      '<input type="email" name="email" placeholder="your@email.com" style="padding:8px 12px;border:1px solid #ddd;border-radius:4px;font-size:14px;width:220px;" />' +
      '<button type="submit" style="padding:8px 20px;background:#2563eb;color:#fff;border:none;border-radius:4px;font-size:14px;font-weight:500;cursor:pointer;">Subscribe</button>' +
      '</form></div>';

    var zhCTA = '<div style="background:#f8f9fa;border:1px solid #e9ecef;border-radius:8px;padding:20px 24px;margin:24px 0;text-align:center;">' +
      '<p style="margin:0 0 12px;font-size:16px;font-weight:600;color:#333;">📬 每周收到真实的 AI 工具评测</p>' +
      '<p style="margin:0 0 16px;font-size:14px;color:#666;">没有广告、没有软文。每周一篇，独立创业者专属。</p>' +
      '<form action="https://buttondown.com/api/emails/embed-subscribe/aitools" method="post" target="popupwindow" onsubmit="window.open(\'https://buttondown.com/aitools\',\'popupwindow\')" style="display:inline-flex;gap:8px;flex-wrap:wrap;justify-content:center;">' +
      '<input type="email" name="email" placeholder="your@email.com" style="padding:8px 12px;border:1px solid #ddd;border-radius:4px;font-size:14px;width:220px;" />' +
      '<button type="submit" style="padding:8px 20px;background:#2563eb;color:#fff;border:none;border-radius:4px;font-size:14px;font-weight:500;cursor:pointer;">订阅</button>' +
      '</form></div>';

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
      if (relPath === 'index.html' || relPath === 'zh/index.html') return;
      if (relPath.indexOf('categories/') === 0 || relPath.indexOf('archives/') === 0 || relPath.indexOf('about/') === 0) return;

      var isZh = relPath.indexOf('zh/') === 0;
      var cta = isZh ? zhCTA : enCTA;

      if (html.indexOf('</article>') !== -1) {
        html = html.replace('</article>', '\n<hr>\n' + cta + '\n</article>');
        fs.writeFileSync(filePath, html, 'utf8');
        count++;
      }
    });

    hexo.log.info('Newsletter CTA: injected into ' + count + ' pages');
  }, 500);
});
