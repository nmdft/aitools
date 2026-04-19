// SEO: JSON-LD structured data injection
// Post-build script: runs after hexo generate to inject JSON-LD into HTML files

'use strict';

var fs = require('fs');
var path = require('path');

hexo.extend.filter.register('after_generate', function() {
  var siteUrl = hexo.config.url || 'https://aitools.nmdft.cn';
  var siteTitle = hexo.config.title || 'AITools';
  var publicDir = hexo.public_dir.toString().replace(/\/$/, '');

  // Use setTimeout to defer execution until after files are written
  setTimeout(function() {
    var posts = hexo.locals.get('posts');
    var postMap = {};
    posts.forEach(function(post) {
      if (post.path) {
        var key = post.path.replace(/^\//, '').replace(/\/$/, '');
        postMap[key] = post;
      }
    });

    var htmlFiles = [];
    function walkDir(dir) {
      try {
        fs.readdirSync(dir).forEach(function(entry) {
          var fullPath = path.join(dir, entry);
          try {
            var stat = fs.statSync(fullPath);
            if (stat.isDirectory()) walkDir(fullPath);
            else if (entry.endsWith('.html')) htmlFiles.push(fullPath);
          } catch(e) {}
        });
      } catch(e) {}
    }
    walkDir(publicDir);

    var injected = 0;
    htmlFiles.forEach(function(filePath) {
      var html;
      try { html = fs.readFileSync(filePath, 'utf8'); } catch(e) { return; }
      if (!html || html.indexOf('</head>') === -1) return;

      var relPath = path.relative(publicDir, filePath).replace(/\\/g, '/');
      var normalizedRel = relPath.replace(/\/index\.html$/, '');
      var isZh = relPath.indexOf('zh/') === 0;
      var lang = isZh ? 'zh' : 'en';

      var jsonLd = '';

      if (postMap[normalizedRel] && postMap[normalizedRel].title) {
        var post = postMap[normalizedRel];
        var url = siteUrl + '/' + relPath.replace(/index\.html$/, '');
        var articleLd = {
          '@context': 'https://schema.org',
          '@type': 'Review',
          headline: post.title,
          description: post.description || '',
          author: { '@type': 'Organization', name: 'AITools' },
          publisher: { '@type': 'Organization', name: 'AITools', url: siteUrl },
          datePublished: post.date ? post.date.toISOString() : '',
          dateModified: post.updated ? post.updated.toISOString() : (post.date ? post.date.toISOString() : ''),
          url: url,
          inLanguage: lang
        };

        var content2 = post._content || '';
        var rm = content2.match(/[Rr]ating[:\s]*(\d+(?:\.\d+)?)\s*\/\s*10/);
        var rc = content2.match(/评分[：:]\s*(\d+(?:\.\d+)?)\s*\/\s*10/);
        var score = rm ? parseFloat(rm[1]) : (rc ? parseFloat(rc[1]) : null);
        if (score) {
          articleLd.reviewRating = {
            '@type': 'Rating', ratingValue: score, bestRating: 10, worstRating: 0
          };
        }

        var toolName = extractToolName(post.title);
        if (toolName) {
          articleLd.itemReviewed = {
            '@type': 'SoftwareApplication', name: toolName,
            applicationCategory: 'BusinessApplication', operatingSystem: 'Web'
          };
        }

        jsonLd = '<script type="application/ld+json">' + JSON.stringify(articleLd) + '</script>';
        injected++;
      } else if (relPath === 'index.html') {
        var websiteLd = {
          '@context': 'https://schema.org', '@type': 'WebSite',
          name: siteTitle, url: siteUrl,
          description: 'Honest reviews of AI tools for solopreneurs.',
          publisher: { '@type': 'Organization', name: 'AITools' }
        };
        jsonLd = '<script type="application/ld+json">' + JSON.stringify(websiteLd) + '</script>';
        injected++;
      } else if (relPath === 'zh/index.html') {
        var zhLd = {
          '@context': 'https://schema.org', '@type': 'WebSite',
          name: siteTitle + ' — 一人公司 AI 工具评测', url: siteUrl,
          description: '独立创业者 AI 工具真实评测。',
          publisher: { '@type': 'Organization', name: 'AITools' }
        };
        jsonLd = '<script type="application/ld+json">' + JSON.stringify(zhLd) + '</script>';
        injected++;
      }

      if (jsonLd) {
        html = html.replace('</head>', jsonLd + '\n</head>');
        fs.writeFileSync(filePath, html, 'utf8');
      }
    });

    hexo.log.info('JSON-LD: injected into ' + injected + ' pages');
  }, 500);
});

function extractToolName(title) {
  var patterns = [
    /^(.+?)\s*(?:Review|评测|评价|测试)/i,
    /^(.+?)\s*(?:vs|VS)\s/i,
  ];
  for (var i = 0; i < patterns.length; i++) {
    var m = title.match(patterns[i]);
    if (m) return m[1].trim();
  }
  return null;
}
