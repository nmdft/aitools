// AITools i18n routing
// Homepage (/) → English articles only
// /zh/ → Chinese articles only
// /en/ → redirect to /

'use strict';

// Disable default index generator — we replace it
hexo.config.index_generator.enable = false;

// English index (homepage) — only English posts
hexo.extend.generator.register('en_index', function(locals) {
  var posts = locals.posts.filter(function(p) { return p.lang !== 'zh'; }).sort('-date');
  return {
    path: 'index.html',
    layout: ['index'],
    data: {
      posts: posts,
      page: posts,
      __lang: 'en'
    }
  };
});

// Chinese index (/zh/) — only Chinese posts
hexo.extend.generator.register('zh_index', function(locals) {
  var posts = locals.posts.filter(function(p) { return p.lang === 'zh'; }).sort('-date');
    return {
      path: 'zh/index.html',
      layout: ['index'],
      data: {
        posts: posts,
        page: posts,
        title: 'AITools — 一人公司 AI 工具评测',
        subtitle: '独立创业者 AI 工具真实评测',
        description: '一人公司 AI 工具真实评测。我们帮你测试，你不用浪费时间和钱。',
        __lang: 'zh'
      }
    };
});

// Chinese post pages (/zh/slug/)
hexo.extend.generator.register('zh_posts', function(locals) {
  return locals.posts.filter(function(p) {
    return p.lang === 'zh';
  }).map(function(post) {
    var slug = post.slug.replace(/^zh-/, '');
    return {
      path: 'zh/' + slug + '/index.html',
      layout: ['post'],
      data: post
    };
  });
});

// /en/ → redirect to /
hexo.extend.generator.register('en_redirect', function() {
  return {
    path: 'en/index.html',
    layout: ['page'],
    data: {
      title: 'Redirecting...',
      content: '<script>window.location.href="/";</script>',
      __lang: 'en'
    }
  };
});
