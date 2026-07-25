/* ═══════════════════════════════════════════════════════
   AI Tools Hub - Internationalization (i18n) Engine
   多语言翻译引擎 — 支持 5 种语言
   ═══════════════════════════════════════════════════════ */

window.I18N = (function() {
  'use strict';

  // ── Translations ──────────────────────────────────────────
  const TRANSLATIONS = {
    en: { name: 'English', native: 'English', flag: '🇺🇸' },
    'zh-CN': { name: 'Chinese', native: '简体中文', flag: '🇨🇳' },
    ja: { name: 'Japanese', native: '日本語', flag: '🇯🇵' },
    ko: { name: 'Korean', native: '한국어', flag: '🇰🇷' },
    es: { name: 'Spanish', native: 'Español', flag: '🇪🇸' },
  };

  // UI Strings
  const STRINGS = {
    en: {
      // Navigation
      'nav.home': 'Home',
      'nav.categories': 'Categories',
      'nav.tools': 'AI Tools',
      'nav.videos': 'Videos',
      'nav.about': 'About',
      'nav.rss': 'RSS',
      'nav.search': 'Search',
      'nav.language': 'Language',

      // Hero
      'hero.badge': '🚀 AI Tools Hub v2.0 — Your Ultimate AI Tools Guide',
      'hero.title1': 'AI Tools Hub',
      'hero.subtitle': 'Your ultimate guide to AI tools, tutorials, reviews and resources — AI工具资源站',
      'hero.start': 'Start Exploring',
      'hero.tools': 'Online AI Tools',
      'hero.stats.reviews': 'AI Tool Reviews',
      'hero.stats.categories': 'Categories',
      'hero.stats.tags': 'Tags',
      'hero.stats.tutorials': 'Tutorials',
      'hero.trust.updated': 'Regularly Updated',
      'hero.trust.seo': 'SEO Optimized',
      'hero.trust.bilingual': 'Bilingual',
      'hero.trust.data': 'Data Driven',

      // Features
      'features.title': '🤖 Why Choose AI Tools Hub',
      'features.desc': 'We curate the most practical AI tools with in-depth reviews and tutorials',
      'features.reviews': 'In-depth Reviews',
      'features.reviews.desc': 'Every AI tool is thoroughly tested across features, pricing, and performance',
      'features.tutorials': 'Hands-on Tutorials',
      'features.tutorials.desc': 'Step-by-step guides from beginner to expert level',
      'features.tools': 'Online AI Tools',
      'features.tools.desc': 'Free online tools for image processing, color extraction and more',
      'features.updates': 'Regular Updates',
      'features.updates.desc': 'Stay current with the latest AI industry developments',
      'features.compare': 'Side-by-side Comparisons',
      'features.compare.desc': 'Detailed comparisons to help you choose the right tool',
      'features.bilingual': 'Bilingual Content',
      'features.bilingual.desc': 'All content available in both English and Chinese',

      // Tools Section
      'tools.title': '⚡ Online AI Toolbox',
      'tools.desc': 'Free online AI tools, no registration required',

      // Videos Section
      'videos.title': '🎬 AI Video Tutorials',
      'videos.desc': 'Curated AI tutorials — learn by watching',
      'videos.view_all': 'View All Video Tutorials →',

      // Categories
      'categories.title': '📂 Browse Categories',
      'categories.desc': 'Explore AI tool reviews and tutorials by category',

      // Featured
      'featured.title': '🔥 Featured Content',
      'featured.desc': 'Most popular in-depth AI tool reviews',
      'latest.title': '📰 Latest Articles',
      'latest.view_all': 'Browse All Articles →',

      // Tags
      'tags.title': '🏷️ Popular Tags',
      'tags.desc': 'Browse AI tools content by tag',

      // CTA
      'cta.title': '🚀 Ready to Explore the AI World?',
      'cta.desc': 'Browse our AI tools library — from ChatGPT to Midjourney, from video generation to coding',
      'cta.learn': 'Learn More',
      'cta.rss': 'Subscribe RSS',

      // Tools page
      'tools.page.title': '⚡ Online AI Toolbox',
      'tools.page.desc': 'Free online AI tools — image processing, color extraction, QR code generation and more',
      'tools.image_filter': '🎨 Image Filter',
      'tools.image_filter.desc': 'Apply filters and effects to your images',
      'tools.palette': '🌈 Color Palette',
      'tools.palette.desc': 'Extract color schemes from images',
      'tools.qr': '📱 QR Code Generator',
      'tools.qr.desc': 'Generate QR codes instantly',
      'tools.prompt': '💬 Prompt Builder',
      'tools.prompt.desc': 'AI prompt template builder',
      'tools.bg_remove': '✂️ Background Removal',
      'tools.bg_remove.desc': 'Remove image backgrounds online',
      'tools.tts': '🔊 Text to Speech',
      'tools.tts.desc': 'AI voice synthesis demo',
      'tools.img_gen': '🎨 AI Image Generator',
      'tools.img_gen.desc': 'AI-powered abstract art generation',
      'tools.video': '🎬 AI Video Studio',
      'tools.video.desc': 'Video info and frame capture',
      'tools.ppt': '📊 AI Slide Creator',
      'tools.ppt.desc': 'Create HTML presentations',
      'tools.office': '📝 Office Suite',
      'tools.office.desc': 'Text analysis and statistics',
      'tools.design': '🎯 Design Studio',
      'tools.design.desc': 'Color scheme designer',
      'tools.automation': '⚙️ Automation Hub',
      'tools.automation.desc': 'Task management and timer',

      // Videos page
      'videos.page.title': '🎬 AI Tool Video Tutorials',
      'videos.page.desc': 'Curated AI tool tutorials, in-depth reviews and industry insights',
      'videos.all': 'All',
      'videos.chatgpt': '🤖 ChatGPT',
      'videos.image': '🎨 AI Image',
      'videos.video': '🎬 AI Video',
      'videos.coding': '💻 AI Coding',
      'videos.tutorial': '📚 Tutorial',

      // Footer
      'footer.quick_links': 'Quick Links',
      'footer.popular_cats': 'Popular Categories',
      'footer.popular_tags': 'Popular Tags',
      'footer.about': 'About Us',
      'footer.rss': 'RSS Subscribe',
      'footer.rights': 'All rights reserved.',
      'footer.privacy': 'Privacy Policy',
      'footer.home': 'Home',
      'footer.tools': 'AI Tools',
      'footer.videos': 'Video Tutorials',

      // Search
      'search.placeholder': 'Search articles...',
      'search.close': 'Close search',

      // Common
      'common.loading': 'Loading...',
      'common.error': 'Error',
      'common.submit': 'Submit',
      'common.cancel': 'Cancel',
      'common.download': 'Download',
      'common.reset': 'Reset',
      'common.copy': 'Copy',
      'common.generate': 'Generate',
      'common.play': 'Play',
      'common.pause': 'Pause',
      'common.stop': 'Stop',
    },

    'zh-CN': {
      'nav.home': '首页',
      'nav.categories': '分类',
      'nav.tools': 'AI工具',
      'nav.videos': '视频',
      'nav.about': '关于',
      'nav.rss': 'RSS',
      'nav.search': '搜索',
      'nav.language': '语言',

      'hero.badge': '🚀 AI Tools Hub v2.0 — 你的AI工具终极指南',
      'hero.title1': 'AI Tools Hub',
      'hero.subtitle': '你的AI工具终极指南 — 评测、教程、对比与资源',
      'hero.start': '开始探索',
      'hero.tools': '在线AI工具',
      'hero.stats.reviews': 'AI工具评测',
      'hero.stats.categories': '分类',
      'hero.stats.tags': '标签',
      'hero.stats.tutorials': '教程',
      'hero.trust.updated': '持续更新',
      'hero.trust.seo': 'SEO优化',
      'hero.trust.bilingual': '中英双语',
      'hero.trust.data': '数据驱动',

      'features.title': '🤖 为什么选择 AI Tools Hub',
      'features.desc': '我们为你精选最实用的AI工具，提供深度评测与实战教程',
      'features.reviews': '深度评测',
      'features.reviews.desc': '每款AI工具都经过实际测试，从功能、定价、性能多维度评估',
      'features.tutorials': '实战教程',
      'features.tutorials.desc': '从入门到精通，step-by-step 教程帮你快速掌握AI工具',
      'features.tools': '在线AI工具',
      'features.tools.desc': '免费在线使用AI图片处理、调色板提取等实用工具',
      'features.updates': '持续更新',
      'features.updates.desc': '紧跟AI行业最新动态，每日更新新工具和教程',
      'features.compare': '横向对比',
      'features.compare.desc': '同类AI工具详细对比，帮你选择最适合的工具',
      'features.bilingual': '中英双语',
      'features.bilingual.desc': '所有内容支持中英文，服务全球用户',

      'tools.title': '⚡ 在线AI工具箱',
      'tools.desc': '免费使用在线AI工具，无需注册',

      'videos.title': '🎬 AI工具视频教程',
      'videos.desc': '精选AI工具使用教程，边看边学',
      'videos.view_all': '浏览全部视频教程 →',

      'categories.title': '📂 浏览分类',
      'categories.desc': '按类别探索AI工具评测与教程',

      'featured.title': '🔥 精选内容',
      'featured.desc': '最受欢迎的AI工具深度评测',
      'latest.title': '📰 最新文章',
      'latest.view_all': '浏览全部文章 →',

      'tags.title': '🏷️ 热门标签',
      'tags.desc': '按标签浏览AI工具内容',

      'cta.title': '🚀 准备好探索AI世界了吗?',
      'cta.desc': '浏览我们的AI工具库，从ChatGPT到Midjourney，从视频生成到代码编程，一应俱全',
      'cta.learn': '了解更多',
      'cta.rss': '订阅RSS',

      'tools.page.title': '⚡ 在线AI工具箱',
      'tools.page.desc': '免费使用在线AI工具 — 图片处理、颜色提取、QR码生成等',
      'tools.image_filter': '🎨 图片滤镜',
      'tools.image_filter.desc': '在线图片滤镜与特效处理',
      'tools.palette': '🌈 颜色提取',
      'tools.palette.desc': '从图片提取配色方案',
      'tools.qr': '📱 QR码生成',
      'tools.qr.desc': '快速生成二维码',
      'tools.prompt': '💬 Prompt构建',
      'tools.prompt.desc': 'AI提示词模板工具',
      'tools.bg_remove': '✂️ 背景去除',
      'tools.bg_remove.desc': '在线图片背景去除',
      'tools.tts': '🔊 文字转语音',
      'tools.tts.desc': 'AI语音合成演示',
      'tools.img_gen': '🎨 AI图片生成',
      'tools.img_gen.desc': 'AI智能抽象艺术生成',
      'tools.video': '🎬 视频工坊',
      'tools.video.desc': '视频信息查看和帧捕获',
      'tools.ppt': '📊 AI幻灯片',
      'tools.ppt.desc': '创建HTML演示文稿',
      'tools.office': '📝 办公套件',
      'tools.office.desc': '文本分析与统计',
      'tools.design': '🎯 设计工坊',
      'tools.design.desc': '配色方案设计器',
      'tools.automation': '⚙️ 自动化',
      'tools.automation.desc': '任务管理和计时器',

      'videos.page.title': '🎬 AI工具视频教程',
      'videos.page.desc': '精选AI工具使用教程、深度评测与行业洞察',
      'videos.all': '全部',
      'videos.chatgpt': '🤖 ChatGPT',
      'videos.image': '🎨 AI图像',
      'videos.video': '🎬 AI视频',
      'videos.coding': '💻 AI编程',
      'videos.tutorial': '📚 教程',

      'footer.quick_links': '快速链接',
      'footer.popular_cats': '热门分类',
      'footer.popular_tags': '热门标签',
      'footer.about': '关于我们',
      'footer.rss': 'RSS订阅',
      'footer.rights': '版权所有。',
      'footer.privacy': '隐私政策',
      'footer.home': '首页',
      'footer.tools': 'AI工具',
      'footer.videos': '视频教程',

      'search.placeholder': '搜索文章...',
      'search.close': '关闭搜索',

      'common.loading': '加载中...',
      'common.error': '错误',
      'common.submit': '提交',
      'common.cancel': '取消',
      'common.download': '下载',
      'common.reset': '重置',
      'common.copy': '复制',
      'common.generate': '生成',
      'common.play': '播放',
      'common.pause': '暂停',
      'common.stop': '停止',
    },

    ja: {
      'nav.home': 'ホーム',
      'nav.categories': 'カテゴリー',
      'nav.tools': 'AIツール',
      'nav.videos': 'ビデオ',
      'nav.about': 'について',
      'nav.rss': 'RSS',
      'nav.search': '検索',
      'nav.language': '言語',

      'hero.badge': '🚀 AI Tools Hub v2.0 — 究極のAIツールガイド',
      'hero.title1': 'AI Tools Hub',
      'hero.subtitle': 'AIツールの究極ガイド — レビュー、チュートリアル、比較、リソース',
      'hero.start': '探索を始める',
      'hero.tools': 'オンラインAIツール',
      'hero.stats.reviews': 'AIツールレビュー',
      'hero.stats.categories': 'カテゴリー',
      'hero.stats.tags': 'タグ',
      'hero.stats.tutorials': 'チュートリアル',

      'features.title': '🤖 AI Tools Hubを選ぶ理由',
      'features.desc': '厳選されたAIツールの詳細レビューと実践的なチュートリアル',
      'features.reviews': '詳細レビュー',
      'features.reviews.desc': 'すべてのAIツールを機能、価格、パフォーマンスで徹底評価',
      'features.tutorials': '実践チュートリアル',
      'features.tutorials.desc': '初心者からエキスパートまで、ステップバイステップで学習',
      'features.tools': 'オンラインAIツール',
      'features.tools.desc': '画像処理、カラー抽出など無料オンラインツール',
      'features.updates': '定期更新',
      'features.updates.desc': '最新のAI業界動向に常に対応',
      'features.compare': '比較分析',
      'features.compare.desc': '類似AIツールの詳細比較で最適な選択を支援',
      'features.bilingual': '多言語対応',
      'features.bilingual.desc': '全コンテンツが多言語で利用可能',

      'tools.title': '⚡ オンラインAIツールボックス',
      'tools.desc': '登録不要で使える無料オンラインAIツール',
      'videos.title': '🎬 AIビデオチュートリアル',
      'videos.desc': '厳選AIチュートリアル — 見て学ぶ',
      'videos.view_all': 'すべてのビデオを見る →',

      'categories.title': '📂 カテゴリーを探す',
      'categories.desc': 'カテゴリー別にAIツールを探索',
      'featured.title': '🔥 おすすめコンテンツ',
      'featured.desc': '最も人気のあるAIツール詳細レビュー',
      'latest.title': '📰 最新記事',
      'latest.view_all': 'すべての記事を見る →',
      'tags.title': '🏷️ 人気タグ',
      'tags.desc': 'タグ別にAIツールコンテンツを閲覧',

      'cta.title': '🚀 AIの世界を探索する準備はできましたか？',
      'cta.desc': 'ChatGPTからMidjourney、動画生成からコーディングまで',
      'cta.learn': 'もっと詳しく',
      'cta.rss': 'RSS購読',

      'tools.page.title': '⚡ オンラインAIツールボックス',
      'tools.page.desc': '無料オンラインAIツール — 画像処理、カラー抽出、QRコード生成など',
      'tools.image_filter': '🎨 画像フィルター',
      'tools.image_filter.desc': '画像にフィルターと効果を適用',
      'tools.palette': '🌈 カラーパレット',
      'tools.palette.desc': '画像から配色を抽出',
      'tools.qr': '📱 QRコード生成',
      'tools.qr.desc': 'QRコードを即座に生成',
      'tools.prompt': '💬 プロンプトビルダー',
      'tools.prompt.desc': 'AIプロンプトテンプレート',
      'tools.bg_remove': '✂️ 背景除去',
      'tools.bg_remove.desc': '画像の背景をオンラインで除去',
      'tools.tts': '🔊 音声合成',
      'tools.tts.desc': 'AI音声合成デモ',
      'tools.img_gen': '🎨 AI画像生成',
      'tools.img_gen.desc': 'AIによる抽象アート生成',
      'tools.video': '🎬 ビデオスタジオ',
      'tools.video.desc': '動画情報とフレームキャプチャ',
      'tools.ppt': '📊 AIスライド',
      'tools.ppt.desc': 'HTMLプレゼンテーション作成',
      'tools.office': '📝 オフィススイート',
      'tools.office.desc': 'テキスト分析と統計',
      'tools.design': '🎯 デザインスタジオ',
      'tools.design.desc': 'カラースキームデザイナー',
      'tools.automation': '⚙️ 自動化',
      'tools.automation.desc': 'タスク管理とタイマー',

      'videos.page.title': '🎬 AIツールビデオチュートリアル',
      'videos.page.desc': '厳選AIツールチュートリアル、詳細レビューと業界インサイト',
      'videos.all': 'すべて',
      'videos.chatgpt': '🤖 ChatGPT',
      'videos.image': '🎨 AI画像',
      'videos.video': '🎬 AI動画',
      'videos.coding': '💻 AIコーディング',
      'videos.tutorial': '📚 チュートリアル',

      'footer.quick_links': 'クイックリンク',
      'footer.popular_cats': '人気カテゴリー',
      'footer.popular_tags': '人気タグ',
      'footer.about': '私たちについて',
      'footer.rss': 'RSS購読',
      'footer.rights': 'All rights reserved.',
      'footer.privacy': 'プライバシーポリシー',
      'footer.home': 'ホーム',
      'footer.tools': 'AIツール',
      'footer.videos': 'ビデオチュートリアル',

      'search.placeholder': '記事を検索...',
      'search.close': '検索を閉じる',

      'common.loading': '読み込み中...',
      'common.error': 'エラー',
      'common.submit': '送信',
      'common.cancel': 'キャンセル',
      'common.download': 'ダウンロード',
      'common.reset': 'リセット',
      'common.copy': 'コピー',
      'common.generate': '生成',
      'common.play': '再生',
      'common.pause': '一時停止',
      'common.stop': '停止',
    },

    ko: {
      'nav.home': '홈',
      'nav.categories': '카테고리',
      'nav.tools': 'AI 도구',
      'nav.videos': '비디오',
      'nav.about': '소개',
      'nav.rss': 'RSS',
      'nav.search': '검색',
      'nav.language': '언어',

      'hero.badge': '🚀 AI Tools Hub v2.0 — 궁극의 AI 도구 가이드',
      'hero.title1': 'AI Tools Hub',
      'hero.subtitle': 'AI 도구의 궁극적인 가이드 — 리뷰, 튜토리얼, 비교, 리소스',
      'hero.start': '탐험 시작',
      'hero.tools': '온라인 AI 도구',
      'hero.stats.reviews': 'AI 도구 리뷰',
      'hero.stats.categories': '카테고리',
      'hero.stats.tags': '태그',
      'hero.stats.tutorials': '튜토리얼',

      'features.title': '🤖 AI Tools Hub를 선택해야 하는 이유',
      'features.desc': '실용적인 AI 도구를 선별하여 심층 리뷰와 튜토리얼 제공',
      'features.reviews': '심층 리뷰',
      'features.reviews.desc': '모든 AI 도구를 기능, 가격, 성능으로 철저히 테스트',
      'features.tutorials': '실습 튜토리얼',
      'features.tutorials.desc': '초보자부터 전문가까지 단계별 가이드',
      'features.tools': '온라인 AI 도구',
      'features.tools.desc': '이미지 처리, 색상 추출 등 무료 온라인 도구',
      'features.updates': '정기 업데이트',
      'features.updates.desc': '최신 AI 산업 동향을 지속적으로 반영',
      'features.compare': '비교 분석',
      'features.compare.desc': '유사 AI 도구 상세 비교로 최적 선택 지원',
      'features.bilingual': '다국어 지원',
      'features.bilingual.desc': '모든 콘텐츠 다국어 지원',

      'tools.title': '⚡ 온라인 AI 도구 모음',
      'tools.desc': '회원가입 없이 무료로 사용하는 온라인 AI 도구',
      'videos.title': '🎬 AI 비디오 튜토리얼',
      'videos.desc': '선별된 AI 튜토리얼 — 보면서 배우기',
      'videos.view_all': '모든 비디오 보기 →',

      'categories.title': '📂 카테고리 탐색',
      'categories.desc': '카테고리별 AI 도구 리뷰 및 튜토리얼',
      'featured.title': '🔥 추천 콘텐츠',
      'featured.desc': '가장 인기 있는 AI 도구 심층 리뷰',
      'latest.title': '📰 최신 기사',
      'latest.view_all': '모든 기사 보기 →',
      'tags.title': '🏷️ 인기 태그',
      'tags.desc': '태그별 AI 도구 콘텐츠 탐색',

      'cta.title': '🚀 AI 세계를 탐험할 준비가 되셨나요?',
      'cta.desc': 'ChatGPT부터 Midjourney까지, 비디오 생성부터 코딩까지',
      'cta.learn': '더 알아보기',
      'cta.rss': 'RSS 구독',

      'tools.page.title': '⚡ 온라인 AI 도구 모음',
      'tools.page.desc': '무료 온라인 AI 도구 — 이미지 처리, 색상 추출, QR 코드 생성 등',
      'tools.image_filter': '🎨 이미지 필터',
      'tools.image_filter.desc': '이미지에 필터와 효과 적용',
      'tools.palette': '🌈 색상 팔레트',
      'tools.palette.desc': '이미지에서 색상 구성표 추출',
      'tools.qr': '📱 QR 코드 생성',
      'tools.qr.desc': 'QR 코드 즉시 생성',
      'tools.prompt': '💬 프롬프트 빌더',
      'tools.prompt.desc': 'AI 프롬프트 템플릿 도구',
      'tools.bg_remove': '✂️ 배경 제거',
      'tools.bg_remove.desc': '온라인 이미지 배경 제거',
      'tools.tts': '🔊 텍스트 음성 변환',
      'tools.tts.desc': 'AI 음성 합성 데모',
      'tools.img_gen': '🎨 AI 이미지 생성',
      'tools.img_gen.desc': 'AI 추상 아트 생성',
      'tools.video': '🎬 비디오 스튜디오',
      'tools.video.desc': '동영상 정보 및 프레임 캡처',
      'tools.ppt': '📊 AI 슬라이드',
      'tools.ppt.desc': 'HTML 프레젠테이션 생성',
      'tools.office': '📝 오피스 제품군',
      'tools.office.desc': '텍스트 분석 및 통계',
      'tools.design': '🎯 디자인 스튜디오',
      'tools.design.desc': '색상 구성표 디자이너',
      'tools.automation': '⚙️ 자동화',
      'tools.automation.desc': '작업 관리 및 타이머',

      'videos.page.title': '🎬 AI 도구 비디오 튜토리얼',
      'videos.page.desc': '선별된 AI 도구 튜토리얼, 심층 리뷰 및 업계 인사이트',
      'videos.all': '전체',
      'videos.chatgpt': '🤖 ChatGPT',
      'videos.image': '🎨 AI 이미지',
      'videos.video': '🎬 AI 비디오',
      'videos.coding': '💻 AI 코딩',
      'videos.tutorial': '📚 튜토리얼',

      'footer.quick_links': '빠른 링크',
      'footer.popular_cats': '인기 카테고리',
      'footer.popular_tags': '인기 태그',
      'footer.about': '소개',
      'footer.rss': 'RSS 구독',
      'footer.rights': 'All rights reserved.',
      'footer.privacy': '개인정보처리방침',
      'footer.home': '홈',
      'footer.tools': 'AI 도구',
      'footer.videos': '비디오 튜토리얼',

      'search.placeholder': '기사 검색...',
      'search.close': '검색 닫기',

      'common.loading': '로딩 중...',
      'common.error': '오류',
      'common.submit': '제출',
      'common.cancel': '취소',
      'common.download': '다운로드',
      'common.reset': '초기화',
      'common.copy': '복사',
      'common.generate': '생성',
      'common.play': '재생',
      'common.pause': '일시정지',
      'common.stop': '정지',
    },

    es: {
      'nav.home': 'Inicio',
      'nav.categories': 'Categorías',
      'nav.tools': 'Herramientas IA',
      'nav.videos': 'Videos',
      'nav.about': 'Acerca de',
      'nav.rss': 'RSS',
      'nav.search': 'Buscar',
      'nav.language': 'Idioma',

      'hero.badge': '🚀 AI Tools Hub v2.0 — Tu Guía Definitiva de Herramientas IA',
      'hero.title1': 'AI Tools Hub',
      'hero.subtitle': 'Tu guía definitiva de herramientas IA — reseñas, tutoriales, comparaciones y recursos',
      'hero.start': 'Comenzar a Explorar',
      'hero.tools': 'Herramientas IA Online',
      'hero.stats.reviews': 'Reseñas de IA',
      'hero.stats.categories': 'Categorías',
      'hero.stats.tags': 'Etiquetas',
      'hero.stats.tutorials': 'Tutoriales',

      'features.title': '🤖 ¿Por Qué Elegir AI Tools Hub?',
      'features.desc': 'Seleccionamos las herramientas IA más prácticas con reseñas profundas y tutoriales',
      'features.reviews': 'Reseñas Profundas',
      'features.reviews.desc': 'Cada herramienta IA es probada minuciosamente en características, precio y rendimiento',
      'features.tutorials': 'Tutoriales Prácticos',
      'features.tutorials.desc': 'Guías paso a paso desde principiante hasta experto',
      'features.tools': 'Herramientas IA Online',
      'features.tools.desc': 'Herramientas gratuitas online para procesamiento de imágenes y más',
      'features.updates': 'Actualizaciones Regulares',
      'features.updates.desc': 'Mantente al día con los últimos avances en IA',
      'features.compare': 'Comparativas',
      'features.compare.desc': 'Comparaciones detalladas para ayudarte a elegir la herramienta adecuada',
      'features.bilingual': 'Contenido Bilingüe',
      'features.bilingual.desc': 'Todo el contenido disponible en múltiples idiomas',

      'tools.title': '⚡ Caja de Herramientas IA Online',
      'tools.desc': 'Herramientas IA gratuitas online, sin necesidad de registro',
      'videos.title': '🎬 Tutoriales en Video de IA',
      'videos.desc': 'Tutoriales de IA seleccionados — aprende viendo',
      'videos.view_all': 'Ver Todos los Videos →',

      'categories.title': '📂 Explorar Categorías',
      'categories.desc': 'Explora reseñas y tutoriales de herramientas IA por categoría',
      'featured.title': '🔥 Contenido Destacado',
      'featured.desc': 'Las reseñas más populares de herramientas IA',
      'latest.title': '📰 Últimos Artículos',
      'latest.view_all': 'Ver Todos los Artículos →',
      'tags.title': '🏷️ Etiquetas Populares',
      'tags.desc': 'Explora contenido de herramientas IA por etiqueta',

      'cta.title': '🚀 ¿Listo para Explorar el Mundo de la IA?',
      'cta.desc': 'Explora nuestra biblioteca de herramientas IA — de ChatGPT a Midjourney',
      'cta.learn': 'Saber Más',
      'cta.rss': 'Suscribirse RSS',

      'tools.page.title': '⚡ Caja de Herramientas IA Online',
      'tools.page.desc': 'Herramientas IA gratuitas — procesamiento de imágenes, extracción de color, generación de QR y más',
      'tools.image_filter': '🎨 Filtro de Imagen',
      'tools.image_filter.desc': 'Aplica filtros y efectos a tus imágenes',
      'tools.palette': '🌈 Paleta de Colores',
      'tools.palette.desc': 'Extrae esquemas de color de imágenes',
      'tools.qr': '📱 Generador QR',
      'tools.qr.desc': 'Genera códigos QR al instante',
      'tools.prompt': '💬 Constructor de Prompts',
      'tools.prompt.desc': 'Plantillas de prompts para IA',
      'tools.bg_remove': '✂️ Eliminar Fondo',
      'tools.bg_remove.desc': 'Elimina fondos de imágenes online',
      'tools.tts': '🔊 Texto a Voz',
      'tools.tts.desc': 'Demo de síntesis de voz IA',
      'tools.img_gen': '🎨 Generador de Imágenes IA',
      'tools.img_gen.desc': 'Generación de arte abstracto con IA',
      'tools.video': '🎬 Estudio de Video',
      'tools.video.desc': 'Información de video y captura de fotogramas',
      'tools.ppt': '📊 Creador de Diapositivas',
      'tools.ppt.desc': 'Crea presentaciones HTML',
      'tools.office': '📝 Suite de Oficina',
      'tools.office.desc': 'Análisis y estadísticas de texto',
      'tools.design': '🎯 Estudio de Diseño',
      'tools.design.desc': 'Diseñador de esquemas de color',
      'tools.automation': '⚙️ Centro de Automatización',
      'tools.automation.desc': 'Gestión de tareas y temporizador',

      'videos.page.title': '🎬 Tutoriales en Video de Herramientas IA',
      'videos.page.desc': 'Tutoriales seleccionados, reseñas profundas y perspectivas de la industria',
      'videos.all': 'Todos',
      'videos.chatgpt': '🤖 ChatGPT',
      'videos.image': '🎨 Imagen IA',
      'videos.video': '🎬 Video IA',
      'videos.coding': '💻 Programación IA',
      'videos.tutorial': '📚 Tutorial',

      'footer.quick_links': 'Enlaces Rápidos',
      'footer.popular_cats': 'Categorías Populares',
      'footer.popular_tags': 'Etiquetas Populares',
      'footer.about': 'Sobre Nosotros',
      'footer.rss': 'Suscribirse RSS',
      'footer.rights': 'All rights reserved.',
      'footer.privacy': 'Política de Privacidad',
      'footer.home': 'Inicio',
      'footer.tools': 'Herramientas IA',
      'footer.videos': 'Tutoriales en Video',

      'search.placeholder': 'Buscar artículos...',
      'search.close': 'Cerrar búsqueda',

      'common.loading': 'Cargando...',
      'common.error': 'Error',
      'common.submit': 'Enviar',
      'common.cancel': 'Cancelar',
      'common.download': 'Descargar',
      'common.reset': 'Restablecer',
      'common.copy': 'Copiar',
      'common.generate': 'Generar',
      'common.play': 'Reproducir',
      'common.pause': 'Pausa',
      'common.stop': 'Detener',
    },
  };

  // ── State ─────────────────────────────────────────────────
  let currentLang = document.documentElement.lang === 'zh-CN' ? 'zh-CN' : 'en';
  const supportedLangs = Object.keys(STRINGS);

  // ── Init ───────────────────────────────────────────────────
  function init() {
    // URL is the source of truth: /zh/ is Chinese, root paths are English.
    applyLang(currentLang);
  }

  // ── Get supported language list ────────────────────────────
  function getLanguages() {
    return supportedLangs.map(code => ({
      code,
      name: TRANSLATIONS[code]?.name || code,
      native: TRANSLATIONS[code]?.native || code,
      flag: TRANSLATIONS[code]?.flag || '🌐',
    }));
  }

  // ── Translate a single key ─────────────────────────────────
  function t(key, lang) {
    const l = lang || currentLang;
    return STRINGS[l]?.[key] || STRINGS['en']?.[key] || key;
  }

  // ── Apply language to the page ─────────────────────────────
  function applyLang(lang) {
    if (!STRINGS[lang]) lang = 'en';
    currentLang = lang;
    localStorage.setItem('aiToolsLang', lang);
    document.documentElement.lang = lang === 'zh-CN' ? 'zh-Hans' : lang;

    // Page-specific bilingual content. Templates expose both variants through
    // data-en/data-zh so article and archive content can switch without reload.
    document.querySelectorAll('[data-en][data-zh]').forEach(el => {
      const value = lang === 'zh-CN' ? el.getAttribute('data-zh') : el.getAttribute('data-en');
      if (value === null) return;
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
        el.setAttribute('placeholder', value);
      } else {
        el.textContent = value;
      }
    });

    // Update all data-i18n elements
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      const translation = t(key, lang);
      if (translation && translation !== key) {
        // Preserve HTML, only update text content
        if (el.hasAttribute('data-i18n-html')) {
          el.innerHTML = translation;
        } else if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
          el.setAttribute('placeholder', translation);
        } else if (el.tagName === 'META') {
          el.setAttribute('content', translation);
        } else {
          el.textContent = translation;
        }
      }
    });

    // Update language switcher display
    document.querySelectorAll('[data-i18n-lang]').forEach(el => {
      const langCode = el.getAttribute('data-i18n-lang');
      const tr = TRANSLATIONS[langCode];
      if (tr) {
        const show = langCode === lang;
        el.style.display = show ? '' : 'none';
      }
    });

    // Update current language display
    document.querySelectorAll('[data-i18n-current]').forEach(el => {
      const tr = TRANSLATIONS[lang];
      if (tr) {
        const showFlag = el.hasAttribute('data-i18n-show-flag');
        el.textContent = showFlag ? `${tr.flag} ${tr.native}` : tr.native;
      }
    });

    // Dispatch event for other scripts
    document.dispatchEvent(new CustomEvent('i18nChanged', { detail: { lang } }));

    return lang;
  }

  // ── Public API ─────────────────────────────────────────────
  return {
    init,
    t,
    applyLang,
    getLanguages,
    getCurrentLang: () => currentLang,
  };
})();

// Auto-initialize
document.addEventListener('DOMContentLoaded', () => window.I18N.init());
