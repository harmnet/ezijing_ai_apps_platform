// 基础提示语参考案例
export const promptExamples = [
  {
    title: "旅游攻略",
    description: "制作适合老年人的日本旅游攻略",
    task: "做一个从北京到日本的旅游攻略",
    audience: "爸妈",
    goal: "让他们在日本开心的玩20天",
    concern: "他们玩的累，腿和腰不太好",
    icon: "ri-map-pin-line"
  },
  {
    title: "学习计划",
    description: "为小学生制定高效学习计划",
    task: "制定一个小学五年级数学学习计划",
    audience: "注意力不集中的小学生",
    goal: "在三个月内提高数学成绩",
    concern: "孩子容易对枯燥的内容失去兴趣",
    icon: "ri-book-open-line"
  },
  {
    title: "健身计划",
    description: "为办公室工作者定制健身计划",
    task: "设计一套居家健身计划",
    audience: "长期久坐的上班族",
    goal: "改善体态，增强体质",
    concern: "没有健身器材，时间有限",
    icon: "ri-heart-pulse-line"
  },
  {
    title: "演讲稿",
    description: "撰写技术产品发布会演讲稿",
    task: "写一份新产品发布会的演讲稿",
    audience: "技术行业的投资者和媒体",
    goal: "展示产品创新点并吸引投资",
    concern: "听众对技术细节的理解有限",
    icon: "ri-mic-line"
  },
  {
    title: "食谱规划",
    description: "为糖尿病患者设计食谱",
    task: "设计一周的健康饮食食谱",
    audience: "糖尿病患者",
    goal: "控制血糖同时保证营养均衡",
    concern: "食材选择有限，口味不能太单调",
    icon: "ri-restaurant-line"
  },
  {
    title: "商业计划书",
    description: "编写创业项目商业计划书",
    task: "撰写一份人工智能创业项目的商业计划书",
    audience: "风险投资人",
    goal: "获得种子轮融资",
    concern: "市场竞争激烈，差异化不够明显",
    icon: "ri-briefcase-line"
  },
  {
    title: "育儿建议",
    description: "为新手父母提供育儿建议",
    task: "整理0-1岁婴儿科学喂养指南",
    audience: "第一次当父母的年轻夫妇",
    goal: "帮助他们科学喂养宝宝",
    concern: "他们工作忙，时间精力有限",
    icon: "ri-parent-line"
  },
  {
    title: "网站内容",
    description: "创建企业网站的核心内容",
    task: "为一家科技公司设计网站首页内容",
    audience: "潜在客户和合作伙伴",
    goal: "展示公司实力并促成合作",
    concern: "内容过于技术化会降低用户体验",
    icon: "ri-global-line"
  },
  {
    title: "教学课件",
    description: "设计高中物理教学课件",
    task: "制作高中物理力学单元的教学课件",
    audience: "对物理不感兴趣的高中生",
    goal: "通过生动的例子让学生理解物理概念",
    concern: "学生基础参差不齐，注意力容易分散",
    icon: "ri-presentation-line"
  },
  {
    title: "社交媒体策略",
    description: "规划品牌社交媒体营销策略",
    task: "设计化妆品品牌的社交媒体营销策略",
    audience: "18-25岁年轻女性",
    goal: "提高品牌知名度和产品销量",
    concern: "预算有限，市场竞争激烈",
    icon: "ri-share-line"
  }
];

// RTGO参考案例
export const rtgoPromptExamples = [
  {
    title: "小红书营销文案",
    description: "撰写吸引年轻消费群体的小红书营销文案",
    role: "一位拥有5年小红书内容运营经验的资深营销专家",
    task: "为一款新上市的保湿补水面膜写一篇小红书推广文案",
    goal: "吸引25-35岁的年轻女性消费者，提高产品试用率",
    objective: "800字以内，包含3-5张示意图位置标注，使用轻松有趣的语气，包含产品使用体验和效果对比",
    icon: "ri-shopping-bag-line"
  },
  {
    title: "技术博客文章",
    description: "撰写深入浅出的技术博客文章",
    role: "拥有10年开发经验的全栈工程师",
    task: "编写一篇关于前端框架性能优化的技术文章",
    goal: "帮助初中级开发者理解并应用性能优化技巧",
    objective: "2000字左右，包含代码示例、性能对比图表，使用通俗易懂的语言解释复杂概念",
    icon: "ri-code-line"
  },
  {
    title: "产品需求文档",
    description: "编写清晰详细的产品需求文档",
    role: "经验丰富的产品经理",
    task: "为一款移动端健康应用编写PRD文档",
    goal: "明确产品功能、用户流程和开发要求",
    objective: "包含用户故事、功能需求、交互设计、验收标准等，使用简洁专业的语言，配合流程图和原型图说明",
    icon: "ri-file-list-3-line"
  },
  {
    title: "教育课程方案",
    description: "设计K12数学在线教育课程方案",
    role: "有5年教学经验的数学教育专家",
    task: "设计一套针对初中生的数学思维训练课程",
    goal: "提升学生的数学思维能力和解题能力",
    objective: "设计10课时的课程大纲，每课时45分钟，包含教学目标、教学内容、教学方法、作业设计和教学资源",
    icon: "ri-book-open-line"
  },
  {
    title: "用户研究报告",
    description: "撰写详实的用户研究报告",
    role: "资深用户研究员",
    task: "分析电商平台的用户行为数据并撰写研究报告",
    goal: "发现用户痛点，为产品优化提供依据",
    objective: "包含研究方法、用户画像、行为分析、痛点总结和改进建议，使用专业术语但保持易读性，配合数据可视化图表",
    icon: "ri-user-search-line"
  },
  {
    title: "市场营销策略",
    description: "制定全方位的市场营销策略",
    role: "具有10年经验的市场营销总监",
    task: "为一款新上市的智能家居产品制定市场营销策略",
    goal: "在3个月内提升市场份额达到15%",
    objective: "包含市场分析、目标用户、竞品分析、营销渠道、推广方案和预算规划，策略要具体可执行，重点关注数字营销",
    icon: "ri-line-chart-line"
  },
  {
    title: "客户服务脚本",
    description: "编写专业的客户服务话术脚本",
    role: "资深客户服务培训师",
    task: "为电商平台的售后客服团队编写标准话术脚本",
    goal: "提升客户满意度和问题解决效率",
    objective: "覆盖常见场景如退款、换货、商品问题等，提供开场白、问题诊断、解决方案和结束语，语气友好专业，包含应对棘手情况的技巧",
    icon: "ri-customer-service-2-line"
  },
  {
    title: "数据分析报告",
    description: "编写专业的数据分析报告",
    role: "拥有统计学背景的数据分析师",
    task: "分析过去一年的销售数据并撰写分析报告",
    goal: "找出销售趋势和影响因素，为下一年销售策略提供依据",
    objective: "包含数据概览、趋势分析、相关性分析、异常点分析和建议，使用专业但易懂的语言，配合图表展示分析结果",
    icon: "ri-pie-chart-2-line"
  },
  {
    title: "社交媒体内容计划",
    description: "制定完整的社交媒体内容计划",
    role: "拥有丰富经验的社交媒体内容策划师",
    task: "为一家餐饮品牌制定为期一个月的社交媒体内容计划",
    goal: "提升品牌知名度和粉丝互动率",
    objective: "包含内容主题、发布频率、内容类型、创意方向和KPI指标，内容计划要有创意性和连贯性，适合目标平台的特性",
    icon: "ri-instagram-line"
  },
  {
    title: "企业培训方案",
    description: "设计企业员工技能培训方案",
    role: "专业的企业培训师",
    task: "为科技公司设计一套领导力培训课程",
    goal: "提升中层管理者的领导能力和团队管理技巧",
    objective: "设计3天的培训方案，包含培训目标、课程模块、教学方法、互动环节和效果评估，培训内容要实用性强，适合企业实际情况",
    icon: "ri-team-line"
  }
];

// CO-STAR参考案例
export const costarPromptExamples = [
  {
    title: "社交媒体营销",
    description: "为产品创建吸引年轻用户的社交媒体营销方案",
    context: "我们是一家推出新款智能手表的科技公司，产品具有健康监测和运动追踪功能",
    objective: "创建一套为期一个月的社交媒体营销方案，包括内容主题和发布时间表",
    style: "创新且具有视觉吸引力的内容，强调产品的科技感和生活方式属性",
    tone: "充满活力、鼓舞人心，偶尔使用幽默元素",
    audience: "18-35岁注重健康和科技的年轻专业人士",
    response: "一份分周的营销计划，包含具体的内容创意、发布平台和最佳发布时间",
    icon: "ri-instagram-line"
  },
  {
    title: "产品说明书",
    description: "编写用户友好的智能家居产品说明书",
    context: "我们刚推出一款智能家居中枢，可以连接和控制多种家用设备",
    objective: "创建一份既全面又易于理解的产品说明书",
    style: "清晰、直接，以任务为导向的指南",
    tone: "友好、耐心，避免技术术语，必要时提供解释",
    audience: "非技术背景的一般消费者，年龄在30-60岁之间",
    response: "一份分步骤的安装指南，常见问题解答，以及带图示的功能说明",
    icon: "ri-file-text-line"
  },
  {
    title: "企业演讲稿",
    description: "撰写CEO年度大会演讲稿",
    context: "公司刚经历了重大转型，并在过去一年取得了显著增长",
    objective: "撰写一份既能鼓舞士气又能传达公司愿景的演讲稿",
    style: "富有远见，战略性，包含具体故事和数据",
    tone: "自信、鼓舞人心、感谢与展望并重",
    audience: "公司全体员工，包括管理层和一线员工",
    response: "一份15分钟的演讲稿，包含开场、成就回顾、挑战分析、未来规划和鼓舞结尾",
    icon: "ri-presentation-line"
  },
  {
    title: "教育博客文章",
    description: "创作关于在线教育趋势的博客文章",
    context: "在线教育行业正在快速发展，尤其是疫情后混合式学习模式兴起",
    objective: "撰写一篇分析在线教育未来发展趋势的深度文章",
    style: "信息丰富，基于研究数据，同时富有洞察力",
    tone: "专业、思考性、略带乐观",
    audience: "教育工作者、学校管理者和教育科技公司",
    response: "一篇1500字的博客文章，包含数据支持、案例分析和实用建议",
    icon: "ri-article-line"
  },
  {
    title: "健康饮食指南",
    description: "编写针对办公室工作者的健康饮食指南",
    context: "长时间久坐的办公室工作者面临特殊的健康挑战",
    objective: "创建一份实用的健康饮食指南，帮助改善健康状况和工作效率",
    style: "实用、基于科学但不枯燥",
    tone: "鼓励性、支持性、不说教",
    audience: "25-45岁的办公室工作者，生活忙碌，关注健康",
    response: "一份包含一周食谱、简易食谱、零食建议和饮食习惯改善技巧的指南",
    icon: "ri-heart-pulse-line"
  },
  {
    title: "新闻通讯",
    description: "编写行业新闻简报通讯",
    context: "需要为金融科技行业专业人士提供每周行业动态",
    objective: "编写一份简洁但内容丰富的每周行业通讯",
    style: "信息密集、结构清晰、重点突出",
    tone: "专业、客观、简洁",
    audience: "金融和科技领域的专业人士，时间有限但需要掌握行业动态",
    response: "一份包含5-7条主要新闻，市场数据分析和一个专家观点的简报",
    icon: "ri-mail-line"
  },
  {
    title: "旅游目的地指南",
    description: "创作特色旅游目的地深度指南",
    context: "日本京都是一个兼具传统文化和现代元素的旅游胜地",
    objective: "创作一份能够展现京都独特魅力的旅行指南",
    style: "描述性、沉浸式、故事化",
    tone: "热情、好奇、带有文化敏感性",
    audience: "25-50岁的文化旅游爱好者，对历史和文化有浓厚兴趣",
    response: "一份包含历史背景、推荐景点、文化体验、美食推荐和实用贴士的旅行指南",
    icon: "ri-guide-line"
  },
  {
    title: "求职简历建议",
    description: "提供个性化简历优化建议",
    context: "竞争激烈的就业市场中，优秀的简历是求职者的关键工具",
    objective: "提供针对性的简历优化建议，提高求职成功率",
    style: "具体、实用、基于行业标准",
    tone: "专业、鼓励、建设性",
    audience: "应届毕业生和有1-3年工作经验的年轻专业人士",
    response: "一份包含简历结构、内容优化、关键词建议和常见错误分析的指南",
    icon: "ri-file-user-line"
  },
  {
    title: "产品评测",
    description: "撰写专业但用户友好的科技产品评测",
    context: "市场上新推出一款高端智能手机，消费者需要客观评价",
    objective: "撰写一篇全面但易于理解的产品评测",
    style: "详实、基于实际使用体验、结构化",
    tone: "客观、分析性、略带个人观点",
    audience: "对科技有兴趣但不一定有专业知识的普通消费者",
    response: "一篇包含外观设计、性能评测、摄像功能、电池续航和总体评价的评测文章",
    icon: "ri-smartphone-line"
  },
  {
    title: "环保生活指南",
    description: "创作实用的家庭环保生活指南",
    context: "越来越多的家庭希望通过日常生活习惯改变来减少环境影响",
    objective: "提供实用且可行的家庭环保生活建议",
    style: "实用、积极、注重细节",
    tone: "鼓励、不评判、重视渐进式改变",
    audience: "关注环保但无法做出激进生活方式改变的普通家庭",
    response: "一份包含节能、减废、环保购物、可持续饮食和低碳出行的分类指南",
    icon: "ri-plant-line"
  }
]; 