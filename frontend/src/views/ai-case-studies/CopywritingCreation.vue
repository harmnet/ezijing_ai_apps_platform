<template>
  <div class="case-background" id="copywriting-creation">
    <h2 class="section-title">广告语与营销文案创作</h2>
    
    <div class="background-content">
      <!-- 广告语与文案基础知识 -->
      <div class="content-block">
        <h3>广告语与营销文案的定义</h3>
        <p>广告语（Slogan）是一种简短、醒目、易记的文字表达，用于传达品牌核心理念或产品核心卖点，是品牌传播的关键元素。优秀的广告语能够在短短几个字中凝练品牌精神，激发消费者共鸣，并长期留存于消费者心智中。</p>
        <p>营销文案（Marketing Copywriting）则是面向目标受众，围绕产品或服务特点、消费者需求和行业背景，创作的具有说服力和吸引力的文字内容。它的目的是通过精准的语言触发消费者情感共鸣，引导特定行为，如品牌认同、产品购买等。</p>
        <p>在数字营销时代，广告语与营销文案已经从传统的平面媒体扩展到社交媒体、短视频、电商平台等多元渠道，呈现出内容形式多样化、传播渠道碎片化、创作节奏快速化的特点。</p>
      </div>
      
      <div class="content-block">
        <h3>「0糖」系列文案创作要点</h3>
        <p>基于前期的市场调研、用户画像分析和营销策划，「0糖」系列的广告语与文案创作应遵循以下要点：</p>
        <ul class="challenge-list">
          <li><span class="highlight">产品核心价值突出</span> - 强调"零糖不减甜感"的核心卖点，突显产品在口感和健康平衡上的创新</li>
          <li><span class="highlight">目标用户情感共鸣</span> - 围绕25-35岁健康生活追求者的需求痛点，设计能引发情感共鸣的文案内容</li>
          <li><span class="highlight">场景化表达</span> - 结合办公、健身、社交等核心消费场景，塑造产品使用的具体情境</li>
          <li><span class="highlight">品牌调性统一</span> - 保持积极、健康、时尚的品牌语调，避免过度营销和夸张表达</li>
          <li><span class="highlight">渠道特性适配</span> - 针对不同传播渠道（如社交媒体、电商平台、线下广告等）的特性，调整文案长度和表达方式</li>
          <li><span class="highlight">行动召唤明确</span> - 在文案结尾设置清晰的行动召唤（Call to Action），引导消费者进行下一步行动</li>
        </ul>
      </div>
      
      <!-- 广告语展示与创意 -->
      <div class="content-block highlight-block">
        <h3>「0糖」系列广告语创意案例</h3>
        <p>以下是根据产品特性和目标用户需求设计的一组广告语创意案例，展示了不同角度和表达方式的可能性：</p>
        
        <div class="slogan-showcase">
          <div class="slogan-card" v-for="(slogan, index) in sloganShowcases" :key="index" @click="copySloganToClipboard(slogan.text)">
            <div class="slogan-content">
              <div class="slogan-text">{{ slogan.text }}</div>
              <div class="slogan-description">{{ slogan.description }}</div>
            </div>
            <div class="slogan-tag">{{ slogan.tag }}</div>
            <div class="copy-hint">点击复制</div>
          </div>
        </div>
        
        <div class="ai-tool-tip">
          <div class="tip-icon">💡</div>
          <div class="tip-content">
            <p>想要创作更多针对性广告语？试试<a @click="navigateTo('广告语创作', '/text-creation/marketing/ad-slogan')" class="tool-link">AI广告语创作</a>工具，只需输入产品信息和目标受众，即可生成多组创意广告语。</p>
          </div>
        </div>
      </div>
      
      <!-- AI辅助文案创作工具 -->
      <div class="content-block">
        <h3>AI辅助文案创作</h3>
        <p>现代营销文案创作已经可以借助AI工具显著提升效率和创意水平。针对「0糖」系列的不同营销场景，紫荆AI平台提供了多种专业文案创作工具：</p>
        
        <div class="tools-section">
          <div class="tools-category">
            <h4>核心文案创作工具</h4>
            <div class="tool-cards">
              <div class="tool-card" @click="navigateTo('广告语创作', '/text-creation/marketing/ad-slogan')">
                <div class="tool-icon">✏️</div>
                <div class="tool-info">
                  <h5>广告语创作</h5>
                  <p>生成简洁有力的品牌或产品广告语，传达核心价值主张</p>
                </div>
                <div class="tool-action">使用</div>
              </div>
              <div class="tool-card" @click="navigateTo('营销文案创作', '/text-creation/marketing/copywriting-generator')">
                <div class="tool-icon">📝</div>
                <div class="tool-info">
                  <h5>营销文案创作</h5>
                  <p>为产品详情页、宣传材料等创建专业营销文案</p>
                </div>
                <div class="tool-action">使用</div>
              </div>
              <div class="tool-card" @click="navigateTo('文章润色', '/text-creation/revision/refinement')">
                <div class="tool-icon">✨</div>
                <div class="tool-info">
                  <h5>文案润色优化</h5>
                  <p>提升文案表达力、感染力和说服力，完善语言表达</p>
                </div>
                <div class="tool-action">使用</div>
              </div>
            </div>
          </div>
          
          <div class="tools-category">
            <h4>平台化文案工具</h4>
            <div class="tool-cards">
              <div class="tool-card" @click="navigateTo('小红书笔记创作', '/text-creation/new-media/xiaohongshu')">
                <div class="tool-icon">📔</div>
                <div class="tool-info">
                  <h5>小红书笔记创作</h5>
                  <p>创建适合小红书平台的种草笔记，引发用户兴趣与互动</p>
                </div>
                <div class="tool-action">使用</div>
              </div>
              <div class="tool-card" @click="navigateTo('微博文章创作', '/text-creation/new-media/weibo')">
                <div class="tool-icon">📱</div>
                <div class="tool-info">
                  <h5>微博文案创作</h5>
                  <p>生成简短有趣的微博内容，提高社交媒体传播效果</p>
                </div>
                <div class="tool-action">使用</div>
              </div>
              <div class="tool-card" @click="navigateTo('公众号创作', '/text-creation/new-media/wechat')">
                <div class="tool-icon">📰</div>
                <div class="tool-info">
                  <h5>公众号文章创作</h5>
                  <p>撰写专业深度的公众号文章，建立品牌专业形象</p>
                </div>
                <div class="tool-action">使用</div>
              </div>
            </div>
          </div>
          
          <div class="tools-category">
            <h4>视频文案工具</h4>
            <div class="tool-cards">
              <div class="tool-card" @click="navigateTo('短视频脚本创作', '/text-creation/new-media/short-video')">
                <div class="tool-icon">🎬</div>
                <div class="tool-info">
                  <h5>短视频脚本创作</h5>
                  <p>为抖音、快手等平台创建吸引人的短视频文案脚本</p>
                </div>
                <div class="tool-action">使用</div>
              </div>
              <div class="tool-card" @click="navigateTo('直播脚本创作', '/text-creation/new-media/livestream')">
                <div class="tool-icon">📺</div>
                <div class="tool-info">
                  <h5>直播脚本创作</h5>
                  <p>设计产品直播话术和流程脚本，提升直播带货效果</p>
                </div>
                <div class="tool-action">使用</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 文案实战案例展示 -->
      <div class="content-block">
        <h3>「0糖」系列典型文案案例</h3>
        <p>针对不同营销场景和传播渠道，以下是「0糖」系列的典型文案案例，展示了如何将产品卖点融入不同类型的文案创作中：</p>
        
        <div class="copywriting-tabs">
          <div class="tab-header">
            <div 
              v-for="(tab, index) in copywritingTabs" 
              :key="index" 
              :class="['tab-item', { active: activeTabIndex === index }]"
              @click="activeTabIndex = index"
            >
              {{ tab.title }}
            </div>
          </div>
          
          <div class="tab-content">
            <div class="content-item" v-if="activeTabIndex === 0">
              <div class="content-header">
                <div class="content-title">「0糖」电商详情页文案</div>
                <div class="content-actions">
                  <button class="action-btn" @click="navigateTo('营销文案创作', '/text-creation/marketing/copywriting-generator')">
                    <span>✏️</span> 创建类似文案
                  </button>
                  <button class="copy-btn" @click="copyContent(copywritingTabs[0].content)">
                    <span>📋</span> 复制文案
                  </button>
                </div>
              </div>
              <div class="copywriting-preview e-commerce">
                <div class="product-headline">【「0糖」气泡果茶 · 甜味不减 · 热量全无】</div>
                <div class="product-subheadline">突破性甜感平衡技术，告别"健康无味"的刻板印象</div>
                <div class="product-description">
                  <p>✓ <strong>零糖零热量</strong>：特殊甜味剂配方，带来纯正甜感，热量接近于0</p>
                  <p>✓ <strong>真实果味</strong>：采用100%真实水果提取物，口感饱满不寡淡</p>
                  <p>✓ <strong>轻盈气泡</strong>：精调碳酸度，带来清爽口感，适合全天饮用</p>
                  <p>✓ <strong>健康配方</strong>：无防腐剂，无色素，无反式脂肪，呵护全家健康</p>
                </div>
                <div class="product-scenarios">
                  <div class="scenario-title">适合场景</div>
                  <div class="scenarios-list">
                    <div class="scenario-item">
                      <span class="scenario-icon">💼</span>
                      <span>办公提神</span>
                    </div>
                    <div class="scenario-item">
                      <span class="scenario-icon">🏋️‍♀️</span>
                      <span>运动补给</span>
                    </div>
                    <div class="scenario-item">
                      <span class="scenario-icon">🎬</span>
                      <span>休闲娱乐</span>
                    </div>
                    <div class="scenario-item">
                      <span class="scenario-icon">🥂</span>
                      <span>社交聚会</span>
                    </div>
                  </div>
                </div>
                <div class="cta-section">
                  <div class="product-price"><span class="price-unit">¥</span>9.9<span class="price-unit">/瓶</span></div>
                  <button class="cta-button">立即购买，享受健康甜蜜</button>
                </div>
              </div>
            </div>
            
            <div class="content-item" v-if="activeTabIndex === 1">
              <div class="content-header">
                <div class="content-title">「0糖」小红书种草笔记</div>
                <div class="content-actions">
                  <button class="action-btn" @click="navigateTo('小红书笔记创作', '/text-creation/new-media/xiaohongshu')">
                    <span>✏️</span> 创建类似文案
                  </button>
                  <button class="copy-btn" @click="copyContent(copywritingTabs[1].content)">
                    <span>📋</span> 复制文案
                  </button>
                </div>
              </div>
              <div class="copywriting-preview xiaohongshu">
                <div class="xiaohongshu-title">✨无糖饮料真香实测！这款「0糖」气泡果茶让我戒糖不再难！</div>
                <div class="xiaohongshu-content">
                  <p>之前减脂期最痛苦的就是不能喝甜饮了！市面上的无糖饮料要么太寡淡要么有怪味，直到发现了这款「0糖」气泡果茶，真的是无糖饮料界的天花板了吧！🌟</p>
                  <p>👉 口感测评：</p>
                  <p>首先是开盖那一刻，果香味就扑面而来，一点也不输含糖饮料！喝下去有细腻的气泡感，甜度刚刚好，完全感受不到代糖的怪味，尤其是蜜桃乌龙这个味道简直绝了！真的做到了"零糖不减甜感"！</p>
                  <p>👉 成分党的分析：</p>
                  <p>配料表超级干净，无色素、无防腐剂，用的是新一代甜味剂，比阿斯巴甜健康很多。一整瓶热量只有3大卡，对减肥人群太友好了！</p>
                  <p>👉 使用场景：</p>
                  <p>最近健身完都会来一瓶，解渴又解馋！办公室常备，下午犯困来一瓶提神醒脑！朋友聚会也可以带上，再也不用喝可乐被朋友嘲笑长小肚子了😂</p>
                  <p>🔍 真实体验：已经连续喝了两周，完全没有反弹，现在已经不想碰普通饮料了，真的是戒糖路上的神助攻！</p>
                  <p>#无糖饮料 #减肥日记 #0糖生活 #健康饮品 #测评</p>
                </div>
              </div>
            </div>
            
            <div class="content-item" v-if="activeTabIndex === 2">
              <div class="content-header">
                <div class="content-title">「0糖」短视频脚本</div>
                <div class="content-actions">
                  <button class="action-btn" @click="navigateTo('短视频脚本创作', '/text-creation/new-media/short-video')">
                    <span>✏️</span> 创建类似文案
                  </button>
                  <button class="copy-btn" @click="copyContent(copywritingTabs[2].content)">
                    <span>📋</span> 复制文案
                  </button>
                </div>
              </div>
              <div class="copywriting-preview video-script">
                <div class="script-scene-title">【「0糖挑战」短视频脚本】</div>
                <div class="script-scene">
                  <div class="scene-heading">场景1：街头采访（5秒）</div>
                  <div class="scene-desc">
                    <p><strong>旁白：</strong>"如果让你选择健康和美味，你会选哪一个？"</p>
                    <p><strong>画面：</strong>快速剪辑不同路人做选择的画面，有人选健康，有人选美味，表情纠结</p>
                  </div>
                </div>
                <div class="script-scene">
                  <div class="scene-heading">场景2：对比测试（8秒）</div>
                  <div class="scene-desc">
                    <p><strong>旁白：</strong>"无糖饮料=无味道？今天我们来打破这个刻板印象！"</p>
                    <p><strong>画面：</strong>主持人手持两杯外观完全相同的饮料，一杯是普通含糖饮料，一杯是「0糖」气泡果茶</p>
                  </div>
                </div>
                <div class="script-scene">
                  <div class="scene-heading">场景3：盲测环节（10秒）</div>
                  <div class="scene-desc">
                    <p><strong>旁白：</strong>"我们邀请了10位挑剔的吃货，进行蒙眼品尝测试..."</p>
                    <p><strong>画面：</strong>参与者蒙眼品尝两种饮料，表情由怀疑到惊讶</p>
                    <p><strong>参与者：</strong>"这个甜度刚刚好！""哇，这个气泡感超赞！""我猜这个是高糖的那杯？"</p>
                  </div>
                </div>
                <div class="script-scene">
                  <div class="scene-heading">场景4：揭晓真相（7秒）</div>
                  <div class="scene-desc">
                    <p><strong>旁白：</strong>"当8位参与者都认为「0糖」是含糖饮料时..."</p>
                    <p><strong>画面：</strong>主持人揭示真相，参与者摘下眼罩，表情震惊</p>
                    <p><strong>字幕动效：</strong>"零糖不减甜感，才是真正的双赢"</p>
                  </div>
                </div>
                <div class="script-scene">
                  <div class="scene-heading">场景5：产品展示（5秒）</div>
                  <div class="scene-desc">
                    <p><strong>旁白：</strong>"「0糖」气泡果茶，健康与美味的双重享受！"</p>
                    <p><strong>画面：</strong>产品多角度展示，特写零糖零卡路里标签，并展示多种饮用场景</p>
                    <p><strong>行动号召：</strong>"扫码立即体验，参与#0糖挑战#"</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 互动式文案生成器 -->
      <div class="content-block">
        <h3>「0糖」系列文案生成器</h3>
        <p>尝试使用下方简易工具，快速生成「0糖」系列的广告语或营销文案。选择文案类型和核心卖点，AI将为您定制专属文案。</p>
        
        <div class="copywriting-generator">
          <div class="generator-form">
            <div class="form-group">
              <label>选择文案类型 <span class="required">*</span></label>
              <div class="radio-group">
                <div class="radio-item" v-for="(type, index) in contentTypes" :key="index">
                  <input type="radio" :id="'type-' + index" v-model="selectedContentType" :value="type">
                  <label :for="'type-' + index">{{ type }}</label>
                </div>
              </div>
            </div>
            
            <div class="form-group">
              <label>核心产品卖点 <span class="required">*</span></label>
              <div class="checkbox-group">
                <div class="checkbox-item" v-for="(point, index) in sellingPoints" :key="index">
                  <input type="checkbox" :id="'point-' + index" v-model="selectedSellingPoints" :value="point">
                  <label :for="'point-' + index">{{ point }}</label>
                </div>
              </div>
            </div>
            
            <div class="form-group">
              <label>目标受众 <span class="required">*</span></label>
              <div class="radio-group">
                <div class="radio-item" v-for="(audience, index) in targetAudiences" :key="index">
                  <input type="radio" :id="'audience-' + index" v-model="selectedAudience" :value="audience">
                  <label :for="'audience-' + index">{{ audience }}</label>
                </div>
              </div>
            </div>
            
            <div class="form-group">
              <label>传播场景 <span class="required">*</span></label>
              <div class="radio-group">
                <div class="radio-item" v-for="(scenario, index) in scenarios" :key="index">
                  <input type="radio" :id="'scenario-' + index" v-model="selectedScenario" :value="scenario">
                  <label :for="'scenario-' + index">{{ scenario }}</label>
                </div>
              </div>
            </div>
            
            <div class="form-group">
              <label>品牌语调 <span class="required">*</span></label>
              <div class="radio-group">
                <div class="radio-item" v-for="(tone, index) in tones" :key="index">
                  <input type="radio" :id="'tone-' + index" v-model="selectedTone" :value="tone">
                  <label :for="'tone-' + index">{{ tone }}</label>
                </div>
              </div>
            </div>
          </div>
          
          <div class="form-actions">
            <button class="reset-btn" @click="resetForm">
              <span>🔄</span> 重置
            </button>
            <button class="generate-btn" @click="generateCopywriting" :disabled="!isFormValid">
              <span>✨</span> 生成文案
            </button>
          </div>
          
          <!-- 生成的文案结果 -->
          <div class="generator-result" v-if="showGeneratedContent">
            <h4>AI生成的「0糖」{{ selectedContentType }}</h4>
            <div class="result-content">
              <div v-if="generatedContent" v-html="formattedGeneratedContent"></div>
              <div v-else class="loading-content">
                <div class="loading-spinner"></div>
                <p>正在创作中，请稍候...</p>
              </div>
            </div>
            
            <div class="result-actions" v-if="generatedContent">
              <button class="copy-btn" @click="copyContent(generatedContent)">
                <span>📋</span> 复制文案
              </button>
              <button class="regenerate-btn" @click="generateCopywriting">
                <span>🔄</span> 重新生成
              </button>
              <button class="advanced-btn" @click="goToAdvancedTool">
                <span>⚙️</span> 使用高级工具
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 视觉与文案结合 -->
      <div class="content-block">
        <h3>视觉与文案结合</h3>
        <p>优秀的营销传播不仅需要有力的文案，还需要配合吸引人的视觉元素。紫荆AI平台提供多种工具，帮助您将文案与视觉内容无缝结合：</p>
        
        <div class="visual-copywriting">
          <div class="visual-item">
            <div class="visual-preview">
              <div class="preview-placeholder">
                <span>文案配图</span>
              </div>
            </div>
            <div class="visual-description">
              <h4>AI文生图</h4>
              <p>将文案概念转化为视觉图像，为社交媒体、广告创建匹配的视觉内容</p>
              <button class="tool-btn" @click="navigateTo('文生图', '/image-creation/text-to-image')">
                使用文生图工具
              </button>
            </div>
          </div>
          
          <div class="visual-item">
            <div class="visual-preview">
              <div class="preview-placeholder">
                <span>营销视频</span>
              </div>
            </div>
            <div class="visual-description">
              <h4>AI文生视频</h4>
              <p>基于文案脚本自动生成短视频内容，快速创建营销视频</p>
              <button class="tool-btn" @click="navigateTo('文生视频', '/video-creation/text-to-video')">
                使用文生视频工具
              </button>
            </div>
          </div>
          
          <div class="visual-item">
            <div class="visual-preview">
              <div class="preview-placeholder">
                <span>数字人讲解</span>
              </div>
            </div>
            <div class="visual-description">
              <h4>数字人视频</h4>
              <p>让AI数字人演绎您的营销文案，创建专业的产品介绍视频</p>
              <button class="tool-btn" @click="navigateTo('数字人视频制作', '/digital-human/video-creation')">
                使用数字人工具
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 文案效果评估 -->
      <div class="content-block">
        <h3>文案效果评估</h3>
        <p>优秀的广告语与营销文案应具备以下特质，可用作评估文案质量的标准：</p>
        
        <div class="evaluation-checklist">
          <div class="checklist-item">
            <div class="check-icon">✓</div>
            <div class="check-content">
              <h4>简明性（Simplicity）</h4>
              <p>内容简洁明了，容易理解和记忆，避免复杂晦涩的表达</p>
            </div>
          </div>
          <div class="checklist-item">
            <div class="check-icon">✓</div>
            <div class="check-content">
              <h4>相关性（Relevance）</h4>
              <p>与目标受众的需求、痛点和价值观高度相关，能引发共鸣</p>
            </div>
          </div>
          <div class="checklist-item">
            <div class="check-icon">✓</div>
            <div class="check-content">
              <h4>独特性（Uniqueness）</h4>
              <p>展现品牌或产品的独特卖点，区别于竞争对手</p>
            </div>
          </div>
          <div class="checklist-item">
            <div class="check-icon">✓</div>
            <div class="check-content">
              <h4>可信度（Credibility）</h4>
              <p>内容真实可信，避免夸大其词或做出无法兑现的承诺</p>
            </div>
          </div>
          <div class="checklist-item">
            <div class="check-icon">✓</div>
            <div class="check-content">
              <h4>情感性（Emotion）</h4>
              <p>能够触动目标受众的情感，建立情感连接</p>
            </div>
          </div>
          <div class="checklist-item">
            <div class="check-icon">✓</div>
            <div class="check-content">
              <h4>行动导向（Action-oriented）</h4>
              <p>鼓励受众采取特定行动，如购买、分享或了解更多</p>
            </div>
          </div>
        </div>
        
        <div class="ai-analysis-tip">
          <div class="tip-icon">💡</div>
          <div class="tip-content">
            <h4>AI辅助文案评估</h4>
            <p>使用<a @click="navigateTo('文章润色', '/text-creation/revision/refinement')" class="tool-link">文章润色</a>工具，可以自动评估和优化您的文案质量，提升表达效果。</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template> 