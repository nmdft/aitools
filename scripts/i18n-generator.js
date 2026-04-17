// AITools i18n routing generator
// English posts: filename.md → /en/filename/
// Chinese posts: zh-filename.md → /zh/filename/

'use strict';

function stripZhPrefix(slug) {
  return slug.replace(/^zh-/, '');
}

// Post generator
hexo.extend.generator.register('post', function(locals) {
  return locals.posts.map(function(post) {
    var lang = post.lang || 'en';
    var slug = post.slug;
    if (lang === 'zh') {
      slug = stripZhPrefix(slug);
    }
    return {
      path: lang + '/' + slug + '/index.html',
      layout: ['post'],
      data: post
    };
  });
});

// Index generator
hexo.extend.generator.register('index', function(locals) {
  var perPage = hexo.config.per_page || 12;
  var allPosts = locals.posts.sort('-date').toArray();
  var enPosts = allPosts.filter(function(p) { return p.lang !== 'zh'; });
  var zhPosts = allPosts.filter(function(p) { return p.lang === 'zh'; });
  var result = [];

  function makePages(posts, base, lang) {
    var total = Math.max(1, Math.ceil(posts.length / perPage));
    for (var i = 0; i < total; i++) {
      var path = i === 0 ? base : base + 'page/' + (i + 1) + '/';
      result.push({
        path: path + 'index.html',
        layout: ['index'],
        data: {
          base: base,
          total: total,
          current: i + 1,
          current_url: path,
          posts: posts.slice(i * perPage, (i + 1) * perPage),
          prev: i > 0 ? (i === 1 ? base : base + 'page/' + i + '/') : 0,
          next: i < total - 1 ? base + 'page/' + (i + 2) + '/' : 0,
          __lang: lang
        }
      });
    }
  }

  makePages(enPosts, 'en/', 'en');
  makePages(zhPosts, 'zh/', 'zh');

  // Root → English
  result.push({
    path: 'index.html',
    layout: ['index'],
    data: {
      base: '',
      total: Math.max(1, Math.ceil(enPosts.length / perPage)),
      current: 1,
      current_url: '',
      posts: enPosts.slice(0, perPage),
      prev: 0,
      next: enPosts.length > perPage ? 'page/2/' : 0,
      __lang: 'en'
    }
  });

  return result;
});
