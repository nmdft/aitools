// AITools i18n routing
// Chinese posts: zh-filename.md → /zh/filename/
// English posts use default permalink (en/:title/ via frontmatter)
// Root shows all posts (default)
// /en/ and /zh/ are static redirect pages

'use strict';

function stripZhPrefix(slug) {
  return slug.replace(/^zh-/, '');
}

// Chinese post generator
hexo.extend.generator.register('zh_posts', function(locals) {
  var zhPosts = locals.posts.filter(function(p) { return p.lang === 'zh'; });
  return zhPosts.map(function(post) {
    return {
      path: 'zh/' + stripZhPrefix(post.slug) + '/index.html',
      layout: ['post'],
      data: post
    };
  });
});

// Language landing pages
hexo.extend.generator.register('lang_landing', function(locals) {
  return [
    {
      path: 'en/index.html',
      layout: ['page'],
      data: {
        title: 'AITools — AI Tools for Solopreneurs',
        content: '<div class="lang-landing"><h1>AITools — AI Tools for Solopreneurs</h1><p>Honest reviews of AI tools for one-person businesses.</p><p><a href="/">Browse all articles →</a></p></div>',
        __lang: 'en'
      }
    },
    {
      path: 'zh/index.html',
      layout: ['page'],
      data: {
        title: 'AITools — 一人公司 AI 工具评测',
        content: '<div class="lang-landing"><h1>AITools — 一人公司 AI 工具评测</h1><p>面向一人公司的 AI 工具真实评测。</p><p><a href="/">浏览所有文章 →</a></p></div>',
        __lang: 'zh'
      }
    }
  ];
});
