<template>
  <div class="case-background" id="user-profile">
    <h2 class="section-title">用户画像分析</h2>
    
    <div class="background-content">
      <!-- 用户画像知识 -->
      <div class="content-block">
        <h3>用户画像的定义</h3>
        <p>用户画像（User Persona）是对目标用户群体的一种抽象化、标签化的描述模型，通过收集和分析用户的人口统计学特征、行为习惯、消费偏好、使用场景、需求痛点等多维度数据，构建出具象化的目标用户形象。它是企业了解"用户是谁"、"用户在哪里"、"用户为什么购买"以及"用户如何购买"等核心问题的基础工具。</p>
        <p>从技术视角，用户画像是将海量、分散、多源异构的用户数据进行标签化处理后得到的特征集合，通常包含基础属性标签（如性别、年龄、地域）、行为特征标签（如购买频次、使用时长）、兴趣偏好标签（如内容偏好、审美取向）和价值评估标签（如生命周期价值、忠诚度）等多个维度。</p>
        <p>随着大数据和人工智能技术的发展，现代用户画像已经从静态描述模型向动态预测模型演进，从基于经验的定性分析转向基于数据的定量分析，能够更加精准地预测用户行为和需求变化，为企业的产品开发、精准营销和个性化服务提供数据支撑。</p>
      </div>
      
      <div class="content-block">
        <h3>用户画像的目的</h3>
        <p>构建用户画像的主要目的包括：</p>
        <ul class="challenge-list">
          <li><span class="highlight">精准识别目标用户</span> - 通过多维度标签刻画，清晰定义产品或服务的核心用户群体特征，避免目标用户定义模糊导致的资源浪费和策略偏离</li>
          <li><span class="highlight">深化用户理解</span> - 超越表面的人口统计学特征，深入洞察用户的行为模式、决策逻辑、情感需求和价值观念，实现对用户的立体化理解</li>
          <li><span class="highlight">指导产品开发</span> - 基于用户画像提供的具体用户特征和需求，开发更符合目标用户期望的产品功能和体验，提高产品的市场契合度</li>
          <li><span class="highlight">优化营销策略</span> - 针对不同用户画像群体，制定差异化的营销内容、渠道策略和传播方式，提高营销的精准度和转化效率</li>
          <li><span class="highlight">个性化用户体验</span> - 根据用户画像特征，为不同用户提供定制化的产品推荐、内容展示和服务流程，提升用户满意度和忠诚度</li>
          <li><span class="highlight">预测用户行为</span> - 通过对用户画像的历史行为分析，建立预测模型，预判用户的未来行为趋势和决策路径，实现主动式服务</li>
          <li><span class="highlight">细分市场定位</span> - 将广泛的市场细分为具有相似特征和需求的用户群体，针对性地制定差异化的产品策略和市场定位</li>
        </ul>
        <p>用户画像的根本目的是建立企业与用户之间的"共情桥梁"，使企业能够从用户视角思考问题，设计产品，制定策略，最终实现用户价值与企业价值的双赢。</p>
      </div>

      <!-- 用户画像操作 -->
      <div class="content-block">
        <h3>用户数据采集说明</h3>
        <p>在「0糖」新品上市项目中，我们通过多种渠道和方法采集了大量的用户信息，以便进行全面的用户画像分析：</p>
        <ul class="challenge-list">
          <li><span class="highlight">线上问卷调查</span>通过社交媒体平台、官方网站和电商平台发放了超过2万份问卷，收集了用户的人口统计学特征、购买习惯、饮料偏好等基础信息。</li>
          <li><span class="highlight">消费者焦点小组</span>组织了12场不同城市、不同年龄段的消费者焦点小组讨论，深入了解用户的消费动机、使用场景和情感需求。</li>
          <li><span class="highlight">社交媒体监测</span>利用社交监听工具分析了过去3个月内关于无糖饮料的超过50万条社交媒体讨论，提取用户关注点和情感倾向。</li>
          <li><span class="highlight">销售数据分析</span>分析了全国300多个城市的历史销售数据，识别不同区域、不同渠道的消费者购买模式和偏好差异。</li>
          <li><span class="highlight">产品体验测试</span>邀请了500名目标消费者参与产品盲测和包装评价，收集了直接的产品反馈数据。</li>
        </ul>
        
        <div class="data-file-section">
          <div class="file-card">
            <div class="file-icon">📊</div>
            <div class="file-info">
              <h4>用户画像数据集</h4>
              <p>包含人口统计学特征、购买行为、产品偏好、消费场景等多维度用户数据</p>
              <div class="file-actions">
                <button class="download-btn" @click="downloadDataFile">
                  <span>⬇️</span> 下载文件
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="content-block">
        <h3>AI协助用户画像分析</h3>
        <p>基于已收集的用户数据，您可以利用AI强大的分析能力，快速获取深度洞察：</p>
        
        <div class="ai-buttons">
          <button class="ai-assist-btn data-quality" @click="runAIDataQualityAnalysis">
            <div class="btn-icon">📊</div>
            <div class="btn-text">
              <span class="btn-title">AI数据质量分析</span>
              <span class="btn-desc">分析数据完整性、一致性和代表性，识别数据缺口与优化方向</span>
            </div>
          </button>
          
          <button class="ai-assist-btn user-persona" @click="runAIUserPersona">
            <div class="btn-icon">👤</div>
            <div class="btn-text">
              <span class="btn-title">AI用户画像</span>
              <span class="btn-desc">自动构建多维度用户画像，发现关键用户群体与行为模式</span>
            </div>
          </button>
        </div>
        
        <!-- 小试牛刀按钮 -->
        <div class="try-knowledge-btn-container">
          <button class="try-knowledge-btn" @click="showUserPersonaQuizModal = true">
            <span>⚔️</span> 小试牛刀
          </button>
        </div>
      </div>
      
      <!-- 交互式用户画像设计工具 -->
      <div class="content-block">
        <h3>交互式用户画像设计工具</h3>
        <p>通过回答以下问题，创建清晰、详细的用户画像，帮助您更好地理解目标受众并优化营销策略：</p>
        
        <div class="persona-form">
          <div class="form-section">
            <div class="form-group">
              <label>1. 目标用户的基本人口统计特征是什么？<span class="required">*</span></label>
              <div class="help-tooltip" @mouseenter="showTooltip('demographic')" @mouseleave="hideTooltip">
                <span>❓</span>
                <div class="tooltip-content" v-if="tooltips.demographic">
                  包括年龄范围、性别分布、教育水平、收入水平、职业类型、婚姻状况等基本特征
                </div>
              </div>
              <textarea v-model="personaData.demographic" placeholder="描述目标用户的年龄、性别、教育、收入等基本特征..." rows="4"></textarea>
            </div>
            
            <div class="form-group">
              <label>2. 目标用户的生活方式和价值观是怎样的？<span class="required">*</span></label>
              <div class="help-tooltip" @mouseenter="showTooltip('lifestyle')" @mouseleave="hideTooltip">
                <span>❓</span>
                <div class="tooltip-content" v-if="tooltips.lifestyle">
                  包括生活态度、消费观念、兴趣爱好、社交习惯、追求的生活品质等
                </div>
              </div>
              <textarea v-model="personaData.lifestyle" placeholder="描述目标用户的生活方式、价值观念、兴趣爱好等..." rows="4"></textarea>
            </div>
          </div>
          
          <div class="form-section">
            <div class="form-group">
              <label>3. 目标用户在饮料消费方面有哪些习惯和偏好？<span class="required">*</span></label>
              <div class="help-tooltip" @mouseenter="showTooltip('consumption')" @mouseleave="hideTooltip">
                <span>❓</span>
                <div class="tooltip-content" v-if="tooltips.consumption">
                  包括饮料购买频率、偏好口味、品牌忠诚度、价格敏感度、包装偏好等
                </div>
              </div>
              <textarea v-model="personaData.consumption" placeholder="描述目标用户的饮料消费习惯、口味偏好等..." rows="4"></textarea>
            </div>
            
            <div class="form-group">
              <label>4. 目标用户选择无糖饮料的主要动机是什么？<span class="required">*</span></label>
              <div class="checkbox-group">
                <div class="checkbox-item" v-for="(option, index) in motivationOptions" :key="index">
                  <input type="checkbox" :id="'motivation-' + index" v-model="personaData.motivation" :value="option">
                  <label :for="'motivation-' + index">{{ option }}</label>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="form-actions">
          <button class="generate-btn" @click="generatePersona" :disabled="!isFormValid">
            <span>🎯</span> 生成用户画像
          </button>
          <button class="reset-btn" @click="resetForm">
            <span>🔄</span> 重置表单
          </button>
        </div>
      </div>
      
      <!-- 用户画像结果展示 -->
      <div class="content-block highlight-block" v-if="showPersonaResult">
        <h3>「0糖」目标用户画像分析结果</h3>
        
        <div class="persona-card">
          <div class="persona-header">
            <div class="persona-avatar">👤</div>
            <div class="persona-title">健康生活追求者 - 张小萌</div>
          </div>
          
          <div class="persona-body">
            <div class="persona-section">
              <h4><span>📋</span> 基本信息</h4>
              <ul class="persona-list">
                <li><strong>年龄：</strong>28-35岁</li>
                <li><strong>职业：</strong>白领/专业人士</li>
                <li><strong>收入：</strong>月收入10000-20000元</li>
                <li><strong>教育：</strong>本科或以上学历</li>
                <li><strong>居住地：</strong>一二线城市</li>
              </ul>
            </div>
            
            <div class="persona-section">
              <h4><span>🧠</span> 心理特征</h4>
              <ul class="persona-list">
                <li><strong>价值观：</strong>注重健康、追求品质生活、愿意为健康支付溢价</li>
                <li><strong>痛点：</strong>忙碌工作压力大、担心健康问题、希望兼顾口感和健康</li>
                <li><strong>追求：</strong>平衡的生活方式、社交认同、自我健康管理</li>
              </ul>
            </div>
            
            <div class="persona-section">
              <h4><span>🛒</span> 消费行为</h4>
              <ul class="persona-list">
                <li><strong>购买频率：</strong>每周3-5次饮料消费</li>
                <li><strong>消费场景：</strong>办公室工作间隙、健身后补充、社交聚会</li>
                <li><strong>决策因素：</strong>健康成分 > 口感 > 品牌 > 价格</li>
                <li><strong>信息渠道：</strong>社交媒体、健康类APP、朋友推荐</li>
              </ul>
            </div>
          </div>
          
          <div class="ai-prompt-section">
            <h4>AI人物画像提示词</h4>
            <div class="prompt-box">
              <p class="prompt-content">{{ aiPrompt }}</p>
              <div class="prompt-actions">
                <button class="copy-btn" @click="copyPrompt">
                  <span>📋</span> 复制提示词
                </button>
                <button class="execute-btn" @click="executeAIDesign">
                  <span>🤖</span> AI一键设计
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 用户画像测验模态框 -->
    <div class="quiz-modal" v-if="showUserPersonaQuizModal">
      <!-- 模态框内容 -->
      <div class="quiz-content">
        <div class="quiz-header">
          <h3>用户画像知识小测验</h3>
          <button class="close-btn" @click="showUserPersonaQuizModal = false">×</button>
        </div>
        <div class="quiz-body">
          <div class="quiz-question" v-for="(question, index) in quizQuestions" :key="index">
            <p class="question-text">{{ index + 1 }}. {{ question.text }}</p>
            <div class="options">
              <div class="option" v-for="(option, optIndex) in question.options" :key="optIndex">
                <input type="radio" :id="'q' + index + 'opt' + optIndex" :name="'question' + index" :value="optIndex" v-model="userAnswers[index]">
                <label :for="'q' + index + 'opt' + optIndex">{{ option }}</label>
              </div>
            </div>
          </div>
        </div>
        <div class="quiz-footer">
          <button class="submit-btn" @click="submitQuiz">提交答案</button>
        </div>
      </div>
    </div>
    
    <!-- 测验结果模态框 -->
    <div class="result-modal" v-if="showQuizResultModal">
      <div class="result-content">
        <div class="result-header">
          <h3>测验结果</h3>
          <button class="close-btn" @click="showQuizResultModal = false">×</button>
        </div>
        <div class="result-body">
          <div class="score-display">
            <div class="score-circle">
              {{ quizScore }}/{{ quizQuestions.length }}
            </div>
            <p class="score-text">{{ getScoreMessage() }}</p>
          </div>
          <div class="correct-answers">
            <h4>正确答案与解析：</h4>
            <div class="answer-item" v-for="(question, index) in quizQuestions" :key="index">
              <p class="question"><strong>{{ index + 1 }}. {{ question.text }}</strong></p>
              <p class="answer" :class="{ 'correct': userAnswers[index] === question.correctAnswer, 'incorrect': userAnswers[index] !== question.correctAnswer }">
                您的答案：{{ question.options[userAnswers[index]] }}
                <span v-if="userAnswers[index] !== question.correctAnswer">
                  （正确答案：{{ question.options[question.correctAnswer] }}）
                </span>
              </p>
              <p class="explanation">{{ question.explanation }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// 提示气泡显示状态
const tooltips = ref({
  demographic: false,
  lifestyle: false,
  consumption: false,
  motivation: false,
  channels: false,
  painpoints: false
});

// 用户画像表单数据
const personaData = ref({
  demographic: '',
  lifestyle: '',
  consumption: '',
  motivation: [],
  channels: [],
  painpoints: []
});

// 动机选项
const motivationOptions = [
  '健康管理需求（减少糖分摄入）',
  '控制体重需求',
  '预防疾病（如糖尿病）',
  '个人口味偏好（喜欢低甜度）',
  '跟随健康生活潮流',
  '医生或营养师建议',
  '家人朋友影响'
];

// 媒体渠道选项
const channelOptions = [
  '社交媒体（微信、微博、小红书等）',
  '视频平台（抖音、B站等）',
  '线下超市/便利店',
  '电商平台',
  '朋友推荐',
  '传统媒体（电视、广播、平面媒体）',
  '户外广告'
];

// 小测验模态框显示状态
const showUserPersonaQuizModal = ref(false);
const showQuizResultModal = ref(false);

// 小测验问题
const quizQuestions = [
  {
    text: '用户画像最核心的作用是什么？',
    options: [
      '收集用户个人隐私信息',
      '帮助企业更好地理解目标用户，指导产品和营销决策',
      '统计用户数量进行销售预测',
      '为设计师提供灵感'
    ],
    correctAnswer: 1,
    explanation: '用户画像的核心作用是帮助企业更深入地理解目标用户的特征、需求和行为，从而指导产品开发和营销策略制定。'
  },
  {
    text: '以下哪项不属于用户画像的基础属性标签？',
    options: [
      '性别、年龄',
      '教育水平、收入',
      '地理位置',
      '公司股票代码'
    ],
    correctAnswer: 3,
    explanation: '用户画像的基础属性标签主要包括性别、年龄、教育水平、收入、地理位置等人口统计学特征，公司股票代码与用户个人特征无关。'
  },
  {
    text: '构建用户画像的数据来源可以包括：',
    options: [
      '仅限问卷调查',
      '仅限销售数据',
      '多渠道数据，包括问卷调查、行为数据、社交媒体数据等',
      '仅从竞争对手处获取'
    ],
    correctAnswer: 2,
    explanation: '有效的用户画像需要整合多渠道数据，包括但不限于问卷调查、用户行为数据、交易数据、社交媒体数据、客服互动记录等，以构建全面立体的用户形象。'
  },
  {
    text: '在用户画像构建过程中，"RFM模型"分析的三个维度是：',
    options: [
      '响应率、频率、货币价值',
      '最近购买时间、购买频率、购买金额',
      '研究、发现、管理',
      '风险、功能、市场'
    ],
    correctAnswer: 1,
    explanation: 'RFM模型是用户价值分析的经典方法，三个维度分别是Recency（最近购买时间）、Frequency（购买频率）和Monetary（购买金额），用于评估客户价值和忠诚度。'
  },
  {
    text: '为什么用户画像需要定期更新？',
    options: [
      '仅为了数据好看',
      '因为用户特征和行为模式会随时间变化',
      '只在产品升级时才需要更新',
      '用户画像一旦创建就永久有效'
    ],
    correctAnswer: 1,
    explanation: '用户特征、需求和行为模式会随着市场环境、产品演进和用户自身生命周期阶段的变化而改变，因此用户画像需要定期更新以保持其准确性和实用性。'
  }
];

// 小测验答案和得分
const userAnswers = ref(Array(quizQuestions.length).fill(null));
const quizScore = ref(0);

// 是否显示用户画像结果
const showPersonaResult = ref(false);

// 生成的AI提示词
const aiPrompt = ref('');

// 表单验证
const isFormValid = computed(() => {
  return personaData.value.demographic.trim() !== '' && 
         personaData.value.lifestyle.trim() !== '' && 
         personaData.value.consumption.trim() !== '' && 
         personaData.value.motivation.length > 0;
});

// 显示提示气泡
const showTooltip = (tooltipKey) => {
  tooltips.value[tooltipKey] = true;
};

// 隐藏提示气泡
const hideTooltip = () => {
  Object.keys(tooltips.value).forEach(key => {
    tooltips.value[key] = false;
  });
};

// 生成用户画像
const generatePersona = () => {
  if (!isFormValid.value) {
    alert('请填写所有必填项！');
    return;
  }
  
  // 生成AI提示词
  aiPrompt.value = `请为一款无糖饮料「0糖」创建详细的用户画像，目标用户具有以下特征：
  
- 人口统计特征：${personaData.value.demographic}
- 生活方式和价值观：${personaData.value.lifestyle}
- 饮料消费习惯：${personaData.value.consumption}
- 选择无糖饮料的动机：${personaData.value.motivation.join('、')}

请基于以上信息，生成一个完整的用户画像，包括：基本信息、心理特征、消费行为和营销洞察。同时提供5-8条针对这一用户群体的营销策略建议。`;

  // 显示结果
  showPersonaResult.value = true;
};

// 重置表单
const resetForm = () => {
  personaData.value = {
    demographic: '',
    lifestyle: '',
    consumption: '',
    motivation: [],
    channels: [],
    painpoints: []
  };
  showPersonaResult.value = false;
};

// 复制提示词
const copyPrompt = () => {
  navigator.clipboard.writeText(aiPrompt.value)
    .then(() => {
      alert('提示词已复制到剪贴板！');
    })
    .catch(err => {
      console.error('复制失败：', err);
      alert('复制失败，请手动复制。');
    });
};

// 执行AI提示词
const executeAIDesign = () => {
  alert('正在使用AI处理您的提示词，请稍候...');
  // 这里可以添加实际的AI接口调用
};

// 下载数据文件
const downloadDataFile = () => {
  alert('数据文件下载功能尚未实现');
};

// 运行AI数据质量分析
const runAIDataQualityAnalysis = () => {
  alert('AI数据质量分析功能尚未实现');
};

// 运行AI用户画像分析
const runAIUserPersona = () => {
  alert('AI用户画像分析功能尚未实现');
};

// 提交测验
const submitQuiz = () => {
  // 检查是否所有问题都已回答
  if (userAnswers.value.some(answer => answer === null)) {
    alert('请回答所有问题！');
    return;
  }
  
  // 计算得分
  quizScore.value = userAnswers.value.reduce((score, answer, index) => {
    return answer === quizQuestions[index].correctAnswer ? score + 1 : score;
  }, 0);
  
  // 显示结果
  showUserPersonaQuizModal.value = false;
  showQuizResultModal.value = true;
};

// 获取测验结果消息
const getScoreMessage = () => {
  if (quizScore.value === quizQuestions.length) {
    return '恭喜您全部答对！您对用户画像有很深的理解！';
  } else if (quizScore.value >= quizQuestions.length * 0.7) {
    return '不错！您对用户画像有很好的理解，继续努力！';
  } else {
    return '再接再厉！建议您再次回顾用户画像的相关知识。';
  }
};
</script>

<style scoped>
.case-background {
  margin-bottom: 60px;
}

.section-title {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin-bottom: 30px;
  position: relative;
  padding-bottom: 15px;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background-color: #c62828; /* 紫荆红 */
}

.background-content {
  display: flex;
  flex-direction: column;
}

.content-block {
  margin-bottom: 30px;
  background-color: #fff;
  border-radius: 8px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.content-block h3 {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 18px;
  color: #333;
  position: relative;
  padding-bottom: 10px;
}

.content-block h3::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 40px;
  height: 2px;
  background-color: #c62828; /* 紫荆红 */
}

.content-block p {
  font-size: 16px;
  line-height: 1.7;
  color: #444;
  margin-bottom: 15px;
}

.highlight-block {
  background-color: #f9f9f9;
  border-left: 4px solid #c62828;
}

.challenge-list {
  padding-left: 0;
  list-style-type: none;
  margin-bottom: 20px;
}

.challenge-list li {
  margin-bottom: 12px;
  line-height: 1.6;
  font-size: 15px;
  color: #444;
  padding-left: 25px;
  position: relative;
}

.highlight {
  color: #c62828;
  font-weight: 600;
  margin-right: 5px;
}

/* 保留原有的特殊样式 */
.data-file-section {
  margin-top: 25px;
}

.file-card {
  display: flex;
  align-items: center;
  background-color: #f1f2f6;
  border-radius: 8px;
  padding: 15px;
  border: 1px dashed #d1d8e0;
}

.file-icon {
  font-size: 24px;
  margin-right: 15px;
}

.file-info {
  flex: 1;
}

.file-info h4 {
  font-size: 16px;
  margin-bottom: 5px;
  color: #333;
}

.file-info p {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.file-actions {
  margin-top: 10px;
}

.download-btn {
  background-color: #f1f2f6;
  border: 1px solid #d1d8e0;
  border-radius: 4px;
  padding: 8px 12px;
  font-size: 14px;
  cursor: pointer;
  color: #333;
  display: inline-flex;
  align-items: center;
  transition: all 0.3s;
}

.download-btn:hover {
  background-color: #dfe4ea;
}

.download-btn span {
  margin-right: 5px;
}

.ai-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 15px;
  margin-top: 20px;
  margin-bottom: 20px;
}

.ai-assist-btn {
  display: flex;
  align-items: center;
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s;
}

.ai-assist-btn:hover {
  background-color: #edf2ff;
  border-color: #4a6fe3;
}

.ai-assist-btn.data-quality:hover {
  background-color: #e8f5e9;
  border-color: #4caf50;
}

.ai-assist-btn.user-persona:hover {
  background-color: #e3f2fd;
  border-color: #2196f3;
}

.btn-icon {
  font-size: 24px;
  margin-right: 15px;
}

.btn-text {
  flex: 1;
}

.btn-title {
  display: block;
  font-weight: 600;
  font-size: 16px;
  margin-bottom: 5px;
  color: #333;
}

.btn-desc {
  display: block;
  font-size: 14px;
  color: #666;
}

.try-knowledge-btn-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.try-knowledge-btn {
  background-color: #4a6fe3;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  font-size: 15px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: all 0.3s;
}

.try-knowledge-btn:hover {
  background-color: #3b5dd1;
}

.try-knowledge-btn span {
  margin-right: 8px;
}

.persona-form {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
  margin-top: 25px;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  margin-bottom: 20px;
  position: relative;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 15px;
  font-weight: 600;
  color: #333;
}

.required {
  color: #e74c3c;
  margin-left: 3px;
}

.help-tooltip {
  display: inline-block;
  position: relative;
  margin-left: 5px;
  cursor: help;
}

.help-tooltip span {
  font-size: 12px;
  background-color: #f1f2f6;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #4a6fe3;
}

.tooltip-content {
  position: absolute;
  top: 20px;
  left: 0;
  width: 250px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 8px 12px;
  font-size: 12px;
  color: #666;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
  z-index: 100;
}

textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
  resize: vertical;
}

.checkbox-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.checkbox-item {
  display: flex;
  align-items: center;
}

.checkbox-item input[type="checkbox"] {
  margin-right: 8px;
}

.form-actions {
  margin-top: 30px;
  display: flex;
  justify-content: center;
  gap: 15px;
}

.generate-btn, .reset-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 15px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: all 0.3s;
}

.generate-btn {
  background-color: #2ecc71;
  color: white;
}

.generate-btn:hover {
  background-color: #27ae60;
}

.generate-btn:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.reset-btn {
  background-color: #ecf0f1;
  color: #7f8c8d;
}

.reset-btn:hover {
  background-color: #bdc3c7;
}

.generate-btn span, .reset-btn span {
  margin-right: 8px;
}

.persona-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-top: 20px;
}

.persona-header {
  background-color: #4a6fe3;
  color: white;
  padding: 20px;
  display: flex;
  align-items: center;
}

.persona-avatar {
  font-size: 30px;
  margin-right: 15px;
  background-color: white;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4a6fe3;
}

.persona-title {
  font-size: 20px;
  font-weight: 600;
}

.persona-body {
  padding: 25px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 25px;
}

.persona-section h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  color: #333;
}

.persona-section h4 span {
  margin-right: 8px;
}

.persona-list {
  padding-left: 15px;
}

.persona-list li {
  margin-bottom: 8px;
  font-size: 14px;
  color: #555;
  line-height: 1.5;
}

.ai-prompt-section {
  margin-top: 30px;
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.ai-prompt-section h4 {
  font-size: 18px;
  margin-bottom: 15px;
  color: #333;
}

.prompt-box {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin-top: 15px;
}

.prompt-content {
  font-size: 14px;
  line-height: 1.6;
  color: #555;
  white-space: pre-line;
  margin-bottom: 15px;
}

.prompt-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.copy-btn, .execute-btn {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
}

.copy-btn {
  background-color: #f1f2f6;
  color: #333;
}

.execute-btn {
  background-color: #4a6fe3;
  color: white;
}

.copy-btn:hover {
  background-color: #dfe4ea;
}

.execute-btn:hover {
  background-color: #3b5dd1;
}

.copy-btn span, .execute-btn span {
  margin-right: 5px;
}

/* 弹窗样式 */
.quiz-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.quiz-content {
  background-color: white;
  border-radius: 10px;
  width: 90%;
  max-width: 700px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.quiz-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quiz-header h3 {
  margin: 0;
  font-size: 18px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
}

.quiz-body {
  padding: 20px;
}

.quiz-footer {
  padding: 15px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.quiz-question {
  margin-bottom: 25px;
}

.question-text {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #333;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.option {
  display: flex;
  align-items: center;
}

.option label {
  margin-left: 8px;
  font-size: 14px;
  color: #444;
}

.submit-btn {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  background-color: #4a6fe3;
  color: white;
  cursor: pointer;
}

.result-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.result-content {
  background-color: white;
  border-radius: 10px;
  width: 90%;
  max-width: 700px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.result-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.result-header h3 {
  margin: 0;
  font-size: 18px;
}

.result-body {
  padding: 20px;
}

.score-display {
  text-align: center;
  margin-bottom: 25px;
}

.score-circle {
  font-size: 48px;
  font-weight: 700;
  color: #4a6fe3;
}

.score-text {
  font-size: 18px;
  color: #333;
}

.correct-answers {
  margin-top: 20px;
}

.answer-item {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px dashed #ddd;
}

.question {
  font-weight: 600;
  font-size: 16px;
  margin-bottom: 10px;
  color: #333;
}

.answer {
  font-size: 14px;
  color: #555;
  margin: 5px 0;
}

.correct {
  color: #2ecc71;
  font-weight: 600;
}

.incorrect {
  color: #e74c3c;
  font-weight: 600;
}

.explanation {
  font-size: 14px;
  color: #666;
  margin-top: 8px;
  font-style: italic;
  background-color: #f9f9f9;
  padding: 8px;
  border-radius: 4px;
}
</style> 