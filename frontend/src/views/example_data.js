// 微信公众号文章模块参考案例数据

const wechatArticleExamples = [
  { 
    title: '农业科技', 
    desc: '智慧农业新趋势', 
    icon: 'ri-seedling-line', 
    articleType: 'industry', 
    writingStyle: 'professional' 
  },
  { 
    title: '冰雪产业', 
    desc: '冬奥带动冰雪经济', 
    icon: 'ri-snowy-line', 
    articleType: 'industry', 
    writingStyle: 'analytical' 
  },
  { 
    title: '交通出行', 
    desc: '智能交通新时代', 
    icon: 'ri-train-line', 
    articleType: 'knowledge', 
    writingStyle: 'professional' 
  },
  { 
    title: '新能源车', 
    desc: '电动未来已来临', 
    icon: 'ri-battery-charge-line', 
    articleType: 'opinion', 
    writingStyle: 'analytical' 
  },
  { 
    title: '金融科技', 
    desc: '数字金融新变革', 
    icon: 'ri-bank-line', 
    articleType: 'industry', 
    writingStyle: 'professional' 
  },
  { 
    title: '云计算', 
    desc: '云端科技新体验', 
    icon: 'ri-cloud-line', 
    articleType: 'knowledge', 
    writingStyle: 'professional' 
  },
  { 
    title: '健康医疗', 
    desc: '智慧医疗新未来', 
    icon: 'ri-heart-pulse-line', 
    articleType: 'tutorial', 
    writingStyle: 'conversational' 
  },
  { 
    title: '游戏产业', 
    desc: '元宇宙与游戏融合', 
    icon: 'ri-gamepad-line', 
    articleType: 'opinion', 
    writingStyle: 'humorous' 
  },
  { 
    title: '房地产', 
    desc: '智慧地产新模式', 
    icon: 'ri-building-line', 
    articleType: 'case', 
    writingStyle: 'analytical' 
  },
  { 
    title: '在线教育', 
    desc: '数字化学习革命', 
    icon: 'ri-book-line', 
    articleType: 'knowledge', 
    writingStyle: 'inspirational' 
  }
];

// 微博文章模块参考案例数据
const weiboArticleExamples = [
  { 
    icon: 'ri-briefcase-line', 
    title: '职场感悟', 
    desc: '分享工作中的感悟和经验',
    type: '生活日常',
    weiboType: 'lifestyle',
    writingStyle: 'emotional'
  },
  { 
    icon: 'ri-shopping-bag-line', 
    title: '好物推荐', 
    desc: '推荐最近使用的好产品',
    type: '产品测评',
    weiboType: 'review',
    writingStyle: 'casual'
  },
  { 
    icon: 'ri-film-line', 
    title: '影视评论', 
    desc: '分享观影感受和推荐',
    type: '热点话题',
    weiboType: 'trending',
    writingStyle: 'emotional'
  },
  { 
    icon: 'ri-football-line', 
    title: '体育热点', 
    desc: '体育赛事相关评论',
    type: '提问互动',
    weiboType: 'question',
    writingStyle: 'humorous'
  },
  { 
    icon: 'ri-book-open-line', 
    title: '读书心得', 
    desc: '分享阅读体验和推荐',
    type: '生活日常',
    weiboType: 'lifestyle',
    writingStyle: 'professional'
  },
  { 
    icon: 'ri-restaurant-line', 
    title: '美食分享', 
    desc: '推荐美食和餐厅体验',
    type: '生活日常',
    weiboType: 'lifestyle',
    writingStyle: 'casual'
  },
  { 
    icon: 'ri-rocket-line', 
    title: '科技动态', 
    desc: '最新科技产品和行业动态',
    type: '热点话题',
    weiboType: 'trending',
    writingStyle: 'professional'
  },
  { 
    icon: 'ri-emotion-laugh-line', 
    title: '日常段子', 
    desc: '幽默有趣的生活小故事',
    type: '幽默段子',
    weiboType: 'humor',
    writingStyle: 'humorous'
  },
  { 
    icon: 'ri-map-pin-line', 
    title: '旅行记录', 
    desc: '旅行经历和景点推荐',
    type: '生活日常',
    weiboType: 'lifestyle',
    writingStyle: 'emotional'
  },
  { 
    icon: 'ri-question-line', 
    title: '育儿问答', 
    desc: '育儿经验和问题互动',
    type: '提问互动',
    weiboType: 'question',
    writingStyle: 'conversational'
  }
];

// 小红书笔记模块参考案例数据
const xiaohongshuArticleExamples = [
  { 
    title: '这款面霜真的绝了', 
    desc: '适合敏感肌和干燥肌的保湿面霜，质地轻薄但很滋润，使用后皮肤屏障有明显改善',
    type: '护肤测评', 
    icon: 'ri-lotion-line',
    noteType: 'product-review',
    noteTitle: '这款面霜真的绝了！敏感肌救星✨',
    productName: 'XXX舒缓修复面霜',
    writingStyle: 'enthusiastic',
    includeEmoji: true,
    includeRating: true,
    includeProsCons: true
  },
  { 
    title: '隐藏在巷子里的神级小吃', 
    desc: '探访藏在老城区小巷里的网红美食店，特色小吃和招牌菜品的味道体验',
    type: '美食探店', 
    icon: 'ri-restaurant-line',
    noteType: 'food',
    noteTitle: '隐藏在巷子里的神级小吃！排队两小时值得吗？',
    writingStyle: 'humorous',
    includeEmoji: true,
    includeRating: true,
    includeHashtags: true,
    includeImageDesc: true
  },
  { 
    title: '三亚度假攻略', 
    desc: '三亚三天两晚深度游攻略，包含景点、酒店、美食推荐和实用小贴士',
    type: '旅游攻略', 
    icon: 'ri-suitcase-line',
    noteType: 'travel',
    noteTitle: '三亚度假攻略｜看这一篇就够了',
    writingStyle: 'informative',
    includeEmoji: true,
    includeProsCons: false,
    includeHashtags: true,
    includeTips: true,
    includeImageDesc: true
  },
  { 
    title: '提升生活品质的10个小物件', 
    desc: '分享近期入手的提升生活品质和幸福感的小物件，包括厨房用品和居家好物',
    type: '好物分享', 
    icon: 'ri-gift-line',
    noteType: 'lifestyle',
    noteTitle: '提升生活品质的10个小物件',
    writingStyle: 'friendly',
    includeEmoji: true,
    includeHashtags: true,
    includeImageDesc: true
  },
  { 
    title: '春季穿搭指南', 
    desc: '适合春季的5套日常穿搭分享，包含单品推荐和搭配技巧',
    type: '穿搭分享', 
    icon: 'ri-t-shirt-line',
    noteType: 'fashion',
    noteTitle: '春季穿搭指南｜5套百搭Look',
    writingStyle: 'enthusiastic',
    includeEmoji: true,
    includeHashtags: true,
    includeImageDesc: true
  },
  { 
    title: '15分钟居家燃脂运动', 
    desc: '适合没有健身器材的居家运动方案，每天15分钟高效燃脂',
    type: '健身分享', 
    icon: 'ri-run-line',
    noteType: 'lifestyle',
    noteTitle: '15分钟居家燃脂运动｜无需器械',
    writingStyle: 'professional',
    includeEmoji: true,
    includeTips: true,
    includeHashtags: true
  },
  { 
    title: '日常妆容分享', 
    desc: '适合职场女性的快速日常妆容教程，突出重点部位，提升精神面貌',
    type: '美妆教程', 
    icon: 'ri-paint-brush-line',
    noteType: 'lifestyle',
    noteTitle: '上班族日常妆容分享｜5分钟搞定',
    writingStyle: 'friendly',
    includeEmoji: true,
    includeHashtags: true,
    includeImageDesc: true
  },
  { 
    title: '这本书改变了我的思考方式', 
    desc: '分享一本关于心理学的书籍读后感，以及对日常生活的启发和应用',
    type: '读书笔记', 
    icon: 'ri-book-open-line',
    noteType: 'lifestyle',
    noteTitle: '这本书改变了我的思考方式｜读书笔记',
    writingStyle: 'informative',
    includeEmoji: true,
    includeHashtags: true,
    includeProsCons: false
  },
  { 
    title: '最新数码产品测评', 
    desc: '全面测试新款旗舰手机的性能、拍照、续航等关键特性，帮助你决定是否值得购买',
    type: '数码科技', 
    icon: 'ri-smartphone-line',
    noteType: 'product-review',
    noteTitle: '最新旗舰手机深度测评｜值不值得买？',
    productName: 'XX旗舰手机',
    writingStyle: 'professional',
    includeEmoji: true,
    includeRating: true,
    includeProsCons: true,
    includeHashtags: true
  },
  { 
    title: '超简单的家居DIY改造', 
    desc: '用简单的材料和工具，将家中的旧物改造成实用又美观的装饰品',
    type: 'DIY手工', 
    icon: 'ri-tools-line',
    noteType: 'lifestyle',
    noteTitle: '超简单的家居DIY改造｜旧物改造新生',
    writingStyle: 'friendly',
    includeEmoji: true,
    includeHashtags: true,
    includeImageDesc: true,
    includeTips: true
  }
];

// 短视频脚本模块参考案例数据
const shortVideoScriptExamples = [
  {
    id: 'douyin-tutorial',
    title: '手机摄影技巧',
    desc: '抖音风格教程',
    platform: 'douyin',
    category: 'tutorial',
    icon: 'ri-camera-line',
    topic: '如何用手机拍出专业级照片',
    audience: '摄影爱好者，18-35岁年轻人',
    keywords: '手机摄影,构图技巧,光线利用,后期处理',
    style: '教学型',
    duration: '30-60秒'
  },
  {
    id: 'bilibili-knowledge',
    title: '历史冷知识',
    desc: 'B站科普视频',
    platform: 'bilibili',
    category: 'knowledge',
    icon: 'ri-time-line',
    topic: '鲜为人知的历史趣闻：古代人如何计时？',
    audience: '历史爱好者，学生，知识分子',
    keywords: '历史知识,日晷,水钟,计时工具,古代科技',
    style: '干货型',
    duration: '2-5分钟'
  },
  {
    id: 'xiaohongshu-review',
    title: '美妆新品评测',
    desc: '小红书测评视频',
    platform: 'xiaohongshu',
    category: 'review',
    icon: 'ri-palette-line',
    topic: '平价替代大牌？这5款国货粉底实测对比',
    audience: '美妆爱好者，女性，18-30岁',
    keywords: '美妆测评,国货粉底,性价比,使用感受,持久度',
    style: '教学型',
    duration: '1-2分钟'
  },
  {
    id: 'kuaishou-comedy',
    title: '烦恼日常',
    desc: '搞笑吐槽视频',
    platform: 'kuaishou',
    category: 'comedy',
    icon: 'ri-emotion-laugh-line',
    topic: '当代年轻人的居家烦恼',
    audience: '年轻上班族，20-35岁',
    keywords: '生活吐槽,搞笑,日常烦恼,居家生活,反差感',
    style: '幽默型',
    duration: '15-30秒'
  },
  {
    id: 'weibo-vlog',
    title: '美食Vlog',
    desc: '美食日常记录',
    platform: 'weibo',
    category: 'vlog',
    icon: 'ri-restaurant-line',
    topic: '跟我一起做简单美味的家常菜',
    audience: '家庭煮夫煮妇，美食爱好者',
    keywords: '美食vlog,家常菜,简单料理,烹饪技巧,食材搭配',
    style: '故事型',
    duration: '1-2分钟'
  },
  {
    id: 'wechat-story',
    title: '职场成长故事',
    desc: '视频号成长分享',
    platform: 'wechat',
    category: 'story',
    icon: 'ri-briefcase-line',
    topic: '从菜鸟到主管：我的5年职场蜕变之路',
    audience: '职场新人，求职者，职场人士',
    keywords: '职场成长,经验分享,职业发展,工作技巧,自我提升',
    style: '情感型',
    duration: '2-5分钟'
  }
];

// 直播脚本模块参考案例数据
const livestreamScriptExamples = [
  {
    id: 'douyin-shopping',
    title: '化妆品带货',
    desc: '抖音电商直播',
    platform: 'douyin',
    category: 'shopping',
    icon: 'ri-shopping-cart-line',
    topic: '春季必备护肤品推荐',
    audience: '女性，18-35岁，美妆爱好者',
    keywords: '护肤,春季焕新,保湿,美白,抗氧化',
    style: '热情活力',
    duration: '30-90分钟',
    products: '五款国产高性价比护肤品'
  },
  {
    id: 'bilibili-gaming',
    title: '游戏攻略',
    desc: 'B站游戏直播',
    platform: 'bilibili',
    category: 'gaming',
    icon: 'ri-gamepad-line',
    topic: '《原神》新版本攻略与队伍搭配',
    audience: '游戏玩家，原神爱好者',
    keywords: '原神,游戏攻略,角色展示,装备选择,技巧分享',
    style: '轻松对话型',
    duration: '1.5-3小时'
  },
  {
    id: 'taobao-makeup',
    title: '彩妆教程',
    desc: '淘宝美妆直播',
    platform: 'taobao',
    category: 'makeup',
    icon: 'ri-palette-line',
    topic: '手把手教你日常通勤妆容',
    audience: '上班族女性，初学者化妆爱好者',
    keywords: '日常妆容,通勤妆,底妆技巧,眼妆教程,唇妆选择',
    style: '专业知识型',
    duration: '30-90分钟',
    products: '平价彩妆产品推荐'
  },
  {
    id: 'kuaishou-cooking',
    title: '家常菜教学',
    desc: '快手美食直播',
    platform: 'kuaishou',
    category: 'cooking',
    icon: 'ri-restaurant-line',
    topic: '15分钟快手家常菜',
    audience: '家庭主妇/夫，上班族，烹饪爱好者',
    keywords: '快手菜,简单烹饪,家常菜谱,食材处理,烹饪技巧',
    style: '幽默风趣',
    duration: '30-90分钟'
  },
  {
    id: 'xiaohongshu-fitness',
    title: '居家健身',
    desc: '小红书健身直播',
    platform: 'xiaohongshu',
    category: 'fitness',
    icon: 'ri-run-line',
    topic: '零基础居家健身指南',
    audience: '健身新手，想要保持健康的上班族',
    keywords: '居家健身,无器械训练,核心锻炼,燃脂运动,健康生活',
    style: '专业知识型',
    duration: '30-90分钟'
  },
  {
    id: 'jd-knowledge',
    title: '数码科普',
    desc: '京东知识直播',
    platform: 'jd',
    category: 'knowledge',
    icon: 'ri-lightbulb-line',
    topic: '手机选购指南：如何选到性价比最高的手机',
    audience: '数码爱好者，手机换新需求人群',
    keywords: '手机选购,数码科普,性价比,参数解读,使用建议',
    style: '专业知识型',
    duration: '30-90分钟',
    products: '各价位段推荐手机型号'
  }
];

// 文档结构模块参考案例数据
const documentStructureExamples = [
  {
    title: '商业计划书',
    desc: '适合创业融资',
    icon: 'ri-briefcase-line',
    data: {
      documentType: 'business',
      documentTitle: '零碳科技创业商业计划书',
      documentPurpose: '为零碳科技公司的创业项目寻求投资融资，展示公司的商业模式、市场机会和盈利潜力',
      targetAudience: '潜在投资者、风险投资公司',
      documentLength: 'medium',
      keyPoints: '- 环保科技创新解决方案\n- 目标市场规模和增长趋势\n- 产品技术优势和专利保护\n- 营销策略和销售渠道\n- 财务预测和投资回报分析\n- 管理团队背景',
      additionalNotes: '需要包含详细的财务模型和市场分析数据'
    }
  },
  {
    title: '研究报告',
    desc: '适合学术研究',
    icon: 'ri-book-open-line',
    data: {
      documentType: 'research',
      documentTitle: '5G技术对远程医疗发展的影响研究',
      documentPurpose: '分析5G技术为远程医疗带来的机遇与挑战，并提出应用建议',
      targetAudience: '医疗信息化管理人员、医院管理者、政策制定者',
      documentLength: 'long',
      keyPoints: '- 当前远程医疗技术现状\n- 5G技术关键特性分析\n- 5G对医疗图像传输的改进\n- 实时远程手术可能性\n- 患者监控设备创新\n- 案例研究与实践经验\n- 实施挑战与建议',
      additionalNotes: '需要包含国内外多个成功案例分析'
    }
  },
  {
    title: '白皮书',
    desc: '适合技术产品',
    icon: 'ri-file-paper-2-line',
    data: {
      documentType: 'whitepaper',
      documentTitle: '企业级区块链解决方案白皮书',
      documentPurpose: '介绍我司区块链技术在企业应用中的创新方案，解释技术原理和应用场景',
      targetAudience: '企业CTO、IT决策者、技术采购负责人',
      documentLength: 'comprehensive',
      keyPoints: '- 区块链技术概述和发展趋势\n- 传统系统面临的挑战\n- 我司区块链方案架构\n- 安全性和隐私保护设计\n- 性能优化与扩展性\n- 应用场景示例\n- 实施路径与ROI分析',
      additionalNotes: '强调我们的方案与竞争对手的差异化优势'
    }
  },
  {
    title: '操作手册',
    desc: '适合技术指导',
    icon: 'ri-book-read-line',
    data: {
      documentType: 'handbook',
      documentTitle: '企业数据安全管理操作手册',
      documentPurpose: '为企业IT管理人员提供数据安全管理的标准操作流程和最佳实践指南',
      targetAudience: 'IT管理员、系统管理员、信息安全专员',
      documentLength: 'medium',
      keyPoints: '- 数据分类与敏感度标记\n- 访问控制策略制定\n- 数据加密标准与实施\n- 备份与恢复流程\n- 安全事件响应流程\n- 员工安全意识培训\n- 合规审计检查要点',
      additionalNotes: '需要包含详细的操作截图和步骤说明'
    }
  },
  {
    title: '项目提案',
    desc: '适合项目申请',
    icon: 'ri-projector-line',
    data: {
      documentType: 'proposal',
      documentTitle: '智慧城市交通系统改造项目提案',
      documentPurpose: '向市政部门申请智慧交通系统改造项目，展示技术方案和实施计划',
      targetAudience: '城市规划者、交通管理部门负责人、政府决策者',
      documentLength: 'medium',
      keyPoints: '- 当前交通系统痛点分析\n- 智慧交通系统架构设计\n- 人工智能交通预测模型\n- 实时数据监控与分析\n- 分阶段实施计划\n- 投资回报与社会效益\n- 案例城市成功经验',
      additionalNotes: '需要强调方案的可扩展性和与现有系统的兼容性'
    }
  },
  {
    title: '市场调研',
    desc: '适合市场分析',
    icon: 'ri-line-chart-line',
    data: {
      documentType: 'research',
      documentTitle: '2023年中国电动汽车市场调研报告',
      documentPurpose: '分析中国电动汽车市场现状、消费者偏好和未来趋势，为产品策略提供依据',
      targetAudience: '汽车制造企业高管、产品经理、投资分析师',
      documentLength: 'long',
      keyPoints: '- 中国电动汽车市场规模与增长\n- 消费者购买决策因素分析\n- 充电基础设施现状评估\n- 主要竞争对手产品对比\n- 政策支持与监管趋势\n- 技术发展路线图\n- 未来五年市场预测',
      additionalNotes: '需要包含大量图表和数据可视化'
    }
  },
  {
    title: '培训课程',
    desc: '适合教育培训',
    icon: 'ri-mental-health-line',
    data: {
      documentType: 'handbook',
      documentTitle: '数据分析师入门到精通培训课程',
      documentPurpose: '设计一套完整的数据分析培训课程，涵盖基础知识到高级应用',
      targetAudience: '职场新人、转行人士、在职提升者',
      documentLength: 'comprehensive',
      keyPoints: '- 数据分析基础概念\n- Excel高级数据处理\n- SQL数据库查询\n- Python数据分析库应用\n- 数据可视化技巧\n- 统计学原理与应用\n- 商业智能工具实战\n- 真实项目案例实践',
      additionalNotes: '每个模块需要包含练习和测验'
    }
  },
  {
    title: '产品规划',
    desc: '适合产品开发',
    icon: 'ri-rocket-line',
    data: {
      documentType: 'proposal',
      documentTitle: '智能家居中央控制系统产品规划',
      documentPurpose: '制定智能家居中央控制系统的产品路线图和开发计划',
      targetAudience: '产品开发团队、工程师、公司高管',
      documentLength: 'medium',
      keyPoints: '- 市场需求与机会分析\n- 核心功能定义\n- 技术架构设计\n- 用户体验设计原则\n- 开发里程碑规划\n- 上市策略\n- 后续迭代方向',
      additionalNotes: '需要关注与其他智能家居产品的互操作性'
    }
  },
  {
    title: '营销策略',
    desc: '适合品牌推广',
    icon: 'ri-advertisement-line',
    data: {
      documentType: 'marketing',
      documentTitle: '新品牌市场营销全渠道策略',
      documentPurpose: '为新上市的消费品牌制定全面的市场营销策略和执行计划',
      targetAudience: '营销团队、品牌经理、社交媒体专员',
      documentLength: 'medium',
      keyPoints: '- 目标受众画像分析\n- 品牌定位与核心信息\n- 社交媒体营销策略\n- 内容营销计划\n- KOL合作方案\n- 线下活动规划\n- 营销效果评估框架',
      additionalNotes: '需包含竞品分析和差异化战略'
    }
  },
  {
    title: '战略规划',
    desc: '适合企业发展',
    icon: 'ri-pie-chart-line',
    data: {
      documentType: 'business',
      documentTitle: '五年企业战略发展规划',
      documentPurpose: '制定公司未来五年的战略目标、业务发展方向和实施路径',
      targetAudience: '公司董事会、高管团队、投资人',
      documentLength: 'long',
      keyPoints: '- 行业趋势与市场机会\n- 企业核心竞争力分析\n- 战略目标与关键绩效指标\n- 业务扩展规划\n- 人才发展战略\n- 风险管理框架\n- 资源配置与财务规划',
      additionalNotes: '需要包含多种情景分析和应对策略'
    }
  }
];

// 长文生成模块参考案例数据
const longformExamples = [
  { id: 'academic1', title: '人工智能在教育领域的应用前景', type: '学术论文', icon: 'ri-article-line' },
  { id: 'report1', title: '2023年全球经济发展趋势报告', type: '商业报告', icon: 'ri-bar-chart-line' },
  { id: 'review1', title: '文学作品分析：《百年孤独》的叙事结构', type: '文学评论', icon: 'ri-book-open-line' },
  { id: 'research1', title: '气候变化对生物多样性的影响研究', type: '研究论文', icon: 'ri-leaf-line' },
  { id: 'tech1', title: '区块链技术在供应链管理中的应用', type: '技术分析', icon: 'ri-link-m-line' },
  { id: 'medical1', title: '新冠疫情后的全球公共卫生体系建设', type: '医学论文', icon: 'ri-heart-pulse-line' },
  { id: 'history1', title: '丝绸之路与东西方文化交流', type: '历史研究', icon: 'ri-road-map-line' },
  { id: 'philosophy1', title: '东西方哲学思想比较研究', type: '哲学论文', icon: 'ri-mind-map-line' },
  { id: 'marketing1', title: '社交媒体时代的品牌营销策略', type: '营销分析', icon: 'ri-advertisement-line' },
  { id: 'psychology1', title: '童年创伤对成人心理健康的长期影响', type: '心理学研究', icon: 'ri-psychotherapy-line' }
];

// 长文生成模块参考案例数据模板
const longformExampleData = {
  'academic1': {
    noteType: 'product-review',
    noteTitle: '人工智能在教育领域的应用前景',
    targetAudience: '教育工作者、教育技术研究人员、政策制定者',
    description: '探讨人工智能技术在教育领域的当前应用状况、潜在发展方向及可能带来的教育变革',
    writingStyle: 'professional',
    contentType: 'informative',
    articleLength: 'long',
    citationStandard: 'apa',
    includeAbstract: true,
    includeTableOfContents: true,
    includeIntroduction: true,
    includeMethodology: true,
    includeLiteratureReview: true,
    includeAnalysis: true,
    includeReferences: true
  },
  'report1': {
    noteType: 'lifestyle',
    noteTitle: '2023年全球经济发展趋势报告',
    targetAudience: '企业决策者、投资者、经济学研究人员',
    description: '分析2023年全球经济形势、主要经济体表现、新兴市场变化及未来发展预测',
    writingStyle: 'professional',
    contentType: 'informative',
    articleLength: 'long',
    citationStandard: 'mla',
    includeAbstract: true,
    includeTableOfContents: true,
    includeIntroduction: true,
    includeAnalysis: true,
    includeConclusion: true
  },
  'review1': {
    noteType: 'travel',
    noteTitle: '文学作品分析：《百年孤独》的叙事结构',
    targetAudience: '文学爱好者、文学研究者、大学生',
    description: '分析加西亚·马尔克斯《百年孤独》中的叙事手法、时间结构及魔幻现实主义表现',
    writingStyle: 'professional',
    contentType: 'argumentative',
    articleLength: 'medium',
    citationStandard: 'mla',
    includeAbstract: false,
    includeIntroduction: true,
    includeLiteratureReview: true,
    includeAnalysis: true,
    includeConclusion: true,
    includeReferences: true
  },
  'research1': {
    noteType: 'lifestyle',
    noteTitle: '气候变化对生物多样性的影响研究',
    targetAudience: '环保工作者、生物学研究人员、政策制定者',
    description: '研究全球气候变化对不同生态系统中生物多样性的影响、应对策略及未来挑战',
    writingStyle: 'professional',
    contentType: 'informative',
    articleLength: 'long',
    citationStandard: 'apa',
    includeAbstract: true,
    includeTableOfContents: true,
    includeIntroduction: true,
    includeMethodology: true,
    includeResults: true,
    includeAnalysis: true,
    includeConclusion: true,
    includeReferences: true
  },
  'tech1': {
    noteType: 'fashion',
    noteTitle: '区块链技术在供应链管理中的应用',
    targetAudience: '企业技术主管、供应链管理人员、IT从业者',
    description: '探讨区块链技术如何改善供应链透明度、追溯性和效率，分析实施案例和未来发展',
    writingStyle: 'professional',
    contentType: 'informative',
    articleLength: 'medium',
    citationStandard: 'harvard',
    includeAbstract: true,
    includeIntroduction: true,
    includeAnalysis: true,
    includeConclusion: true
  },
  'medical1': {
    noteType: 'beauty',
    noteTitle: '新冠疫情后的全球公共卫生体系建设',
    targetAudience: '公共卫生专业人士、政策制定者、医疗工作者',
    description: '分析新冠疫情暴露的全球公共卫生体系问题、各国应对措施及未来体系建设方向',
    writingStyle: 'professional',
    contentType: 'argumentative',
    articleLength: 'long',
    citationStandard: 'apa',
    includeAbstract: true,
    includeTableOfContents: true,
    includeIntroduction: true,
    includeLiteratureReview: true,
    includeAnalysis: true,
    includeConclusion: true,
    includeReferences: true
  },
  'history1': {
    noteType: 'travel',
    noteTitle: '丝绸之路与东西方文化交流',
    targetAudience: '历史爱好者、文化研究学者、大学生',
    description: '考察丝绸之路的历史发展、贸易路线及其对东西方文化、艺术、宗教等方面的影响',
    writingStyle: 'professional',
    contentType: 'narrative',
    articleLength: 'long',
    citationStandard: 'chicago',
    includeAbstract: true,
    includeIntroduction: true,
    includeAnalysis: true,
    includeConclusion: true,
    includeReferences: true
  },
  'philosophy1': {
    noteType: 'lifestyle',
    noteTitle: '东西方哲学思想比较研究',
    targetAudience: '哲学研究者、文化爱好者、大学生',
    description: '比较分析东西方主要哲学流派的核心思想、价值观念和世界观差异及其文化根源',
    writingStyle: 'professional',
    contentType: 'argumentative',
    articleLength: 'long',
    citationStandard: 'mla',
    includeAbstract: true,
    includeTableOfContents: true,
    includeIntroduction: true,
    includeLiteratureReview: true,
    includeAnalysis: true,
    includeConclusion: true,
    includeReferences: true
  },
  'marketing1': {
    noteType: 'product-review',
    noteTitle: '社交媒体时代的品牌营销策略',
    targetAudience: '市场营销人员、品牌管理者、企业决策者',
    description: '分析社交媒体环境下品牌营销的新特点、成功案例及有效策略',
    writingStyle: 'professional',
    contentType: 'informative',
    articleLength: 'medium',
    citationStandard: 'apa',
    includeAbstract: true,
    includeIntroduction: true,
    includeAnalysis: true,
    includeConclusion: true
  },
  'psychology1': {
    noteType: 'lifestyle',
    noteTitle: '童年创伤对成人心理健康的长期影响',
    targetAudience: '心理健康工作者、社会工作者、心理学研究人员',
    description: '研究童年期创伤经历对成人心理健康状况的影响机制、表现形式及干预策略',
    writingStyle: 'professional',
    contentType: 'informative',
    articleLength: 'long',
    citationStandard: 'apa',
    includeAbstract: true,
    includeTableOfContents: true,
    includeIntroduction: true,
    includeMethodology: true,
    includeResults: true,
    includeAnalysis: true,
    includeConclusion: true,
    includeReferences: true
  }
};

// 诗歌创作模块参考案例数据
const poetryExamples = [
  { id: 'modern1', title: '城市夜景', type: '现代诗', icon: 'ri-book-open-line' },
  { id: 'classical1', title: '月下思乡', type: '古典诗', icon: 'ri-book-read-line' },
  { id: 'free1', title: '生命的意义', type: '自由诗', icon: 'ri-quill-pen-line' },
  { id: 'song1', title: '雨巷情思', type: '宋词', icon: 'ri-ink-bottle-line' },
  { id: 'tang1', title: '秋日山水', type: '唐诗', icon: 'ri-mountains-line' },
  { id: 'haiku1', title: '夏日蝉鸣', type: '俳句', icon: 'ri-leaf-line' },
  { id: 'landscape1', title: '田园黄昏', type: '山水诗', icon: 'ri-sun-foggy-line' },
  { id: 'love1', title: '思念情人', type: '爱情诗', icon: 'ri-heart-line' },
  { id: 'philosophical1', title: '生死沉思', type: '哲理诗', icon: 'ri-mind-map-line' },
  { id: 'seasonal1', title: '春天的脚步', type: '季节诗', icon: 'ri-seedling-line' }
];

const poetryExampleData = {
  'modern1': {
    noteType: 'modern-poem',
    noteTitle: '城市夜景',
    targetAudience: 'emotional',
    description: '描述现代城市的夜晚景象，霓虹灯与孤独人影的交织',
    keywords: '霓虹灯,高楼,寂寞,城市,夜晚'
  },
  'classical1': {
    noteType: 'classical-poem',
    noteTitle: '月下思乡',
    targetAudience: 'emotional',
    description: '游子在异乡赏月，触景生情，思念故乡和亲人',
    keywords: '明月,思乡,游子,离愁,夜色'
  },
  'free1': {
    noteType: 'free-verse',
    noteTitle: '生命的意义',
    targetAudience: 'philosophical',
    description: '探讨人生存在的价值和意义，表达对生命本质的思考',
    keywords: '生命,存在,哲思,意义,时间'
  },
  'song1': {
    noteType: 'song-ci',
    noteTitle: '雨巷情思',
    targetAudience: 'romantic',
    description: '雨中漫步的情人，打着油纸伞，在青石板路上留下足迹与思念',
    keywords: '油纸伞,雨巷,青石,思念,丁香'
  },
  'tang1': {
    noteType: 'tang-poem',
    noteTitle: '秋日山水',
    targetAudience: 'landscape',
    description: '秋天山间的景色，红叶、流水与远山的和谐画面',
    keywords: '秋山,红叶,流水,远眺,晚霞'
  },
  'haiku1': {
    noteType: 'haiku',
    noteTitle: '夏日蝉鸣',
    targetAudience: 'landscape',
    description: '夏日午后，蝉在树上鸣叫，表达夏天的炎热与生机',
    keywords: '蝉鸣,夏日,树荫,炎热,静谧'
  },
  'landscape1': {
    noteType: 'classical-poem',
    noteTitle: '田园黄昏',
    targetAudience: 'landscape',
    description: '黄昏时分的农村景象，炊烟袅袅，牧童归家',
    keywords: '炊烟,黄昏,田园,牧童,归家'
  },
  'love1': {
    noteType: 'modern-poem',
    noteTitle: '思念爱人',
    targetAudience: 'romantic',
    description: '描述对远方恋人的思念之情，以及相思带来的甜蜜与痛苦',
    keywords: '思念,距离,情书,等待,相思'
  },
  'philosophical1': {
    noteType: 'free-verse',
    noteTitle: '生死沉思',
    targetAudience: 'philosophical',
    description: '对生死问题的哲学思考，探讨存在的本质与意义',
    keywords: '生死,哲思,时间,永恒,灵魂'
  },
  'seasonal1': {
    noteType: 'modern-poem',
    noteTitle: '春天的脚步',
    targetAudience: 'landscape',
    description: '描述春天来临时大地复苏的景象与生机',
    keywords: '春天,新芽,花开,生机,鸟鸣'
  }
};

export { 
  wechatArticleExamples, // 03 公众号文章 
  weiboArticleExamples, // 04 微博文章  
  xiaohongshuArticleExamples, // 05 小红书笔记
  shortVideoScriptExamples, // 06 短视频脚本
  livestreamScriptExamples, // 07 直播脚本
  documentStructureExamples, // 08 文档结构
  longformExamples, // 09 长文生成
  longformExampleData, 
  poetryExamples, // 10 诗歌创作
  poetryExampleData 
};
