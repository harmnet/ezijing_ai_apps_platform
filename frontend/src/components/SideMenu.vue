<template>
  <div class="sidebar-container">
    <aside class="sidebar" :class="{ collapsed: isCollapsed }">
      <nav class="menu">
        <ul>
          <!-- AI对话 -->
          <li class="menu-item" :class="{ active: activePage === 'ai-chat' }">
            <div class="menu-group">
              <router-link to="/ai-chat" class="menu-link" @click="setActivePage('ai-chat')" 
                @mouseenter="showTooltip($event, 'AI对话')" @mouseleave="hideTooltip">
                <i class="ri-chat-3-line"></i>
                <span v-if="!isCollapsed" class="menu-text">AI对话</span>
              </router-link>
              <div v-if="!isCollapsed" class="submenu">
                <router-link to="/ai-chat" class="submenu-link" @click="setActivePage('ai-chat')">
                  常规对话
                </router-link>
              </div>
            </div>
          </li>
          
          <!-- 提示词工程 -->
          <li class="menu-item" :class="{ active: activePage === 'prompt-engineering' }">
            <router-link to="/prompt-engineering" class="menu-link" @click="setActivePage('prompt-engineering')"
              @mouseenter="showTooltip($event, '提示词工程')" @mouseleave="hideTooltip">
              <i class="ri-magic-line"></i>
              <span v-if="!isCollapsed" class="menu-text">提示词工程</span>
            </router-link>
          </li>

          <!-- 基础业务场景AI应用实战 -->
          <li class="menu-item" :class="{ active: activePage === 'practical-scenario' }">
            <router-link to="/practical-scenario" class="menu-link" @click="setActivePage('practical-scenario')"
              @mouseenter="showTooltip($event, '基础业务场景AI应用实战')" @mouseleave="hideTooltip">
              <i class="ri-briefcase-4-line"></i>
              <span v-if="!isCollapsed" class="menu-text">基础业务场景AI应用实战</span>
            </router-link>
          </li>
          
          <!-- 人工智能应用综合案例集 -->
          <li class="menu-item" :class="{ active: activePage === 'ai-case-studies' }">
            <router-link to="/ai-case-studies" class="menu-link" @click="setActivePage('ai-case-studies')"
              @mouseenter="showTooltip($event, '人工智能应用综合案例集')" @mouseleave="hideTooltip">
              <i class="ri-book-2-line"></i>
              <span v-if="!isCollapsed" class="menu-text">人工智能应用综合案例集</span>
            </router-link>
          </li>
          
          <!-- 企业岗位AI技能地图（原AI应用典型场景，顺序下移） -->
          <li class="menu-item" :class="{ active: activePage === 'ai-scenarios' }">
            <router-link to="/ai-scenarios" class="menu-link" @click="setActivePage('ai-scenarios')"
              @mouseenter="showTooltip($event, '企业岗位AI技能地图')" @mouseleave="hideTooltip">
              <i class="ri-lightbulb-line"></i>
              <span v-if="!isCollapsed" class="menu-text">企业岗位AI技能地图</span>
            </router-link>
          </li>
          
          <!-- 文本创作中心 -->
          <li class="menu-item" :class="{ active: activePage === 'text-creation' }">
            <router-link to="/text-creation" class="menu-link" @click="setActivePage('text-creation')"
              @mouseenter="showTooltip($event, '文本创作中心')" @mouseleave="hideTooltip">
              <i class="ri-file-text-line"></i>
              <span v-if="!isCollapsed" class="menu-text">文本创作中心</span>
            </router-link>
          </li>
          
          <!-- 图形创作中心 -->
          <li class="menu-item" :class="{ active: activePage === 'image-creation' }">
            <router-link to="/image-creation" class="menu-link" @click="setActivePage('image-creation')"
              @mouseenter="showTooltip($event, '图形创作中心')" @mouseleave="hideTooltip">
              <i class="ri-image-line"></i>
              <span v-if="!isCollapsed" class="menu-text">图形创作中心</span>
            </router-link>
          </li>
          
          <!-- 视频创作中心 -->
          <li class="menu-item" :class="{ active: activePage === 'video-creation' }">
            <router-link to="/video-creation" class="menu-link" @click="setActivePage('video-creation')"
              @mouseenter="showTooltip($event, '音视频创作中心')" @mouseleave="hideTooltip">
              <i class="ri-movie-line"></i>
              <span v-if="!isCollapsed" class="menu-text">音视频创作中心</span>
            </router-link>
          </li>
          
          <!-- 数字人中心 -->
          <li class="menu-item" :class="{ active: activePage === 'digital-human' }" v-if="false">
            <router-link to="/digital-human" class="menu-link" @click="setActivePage('digital-human')"
              @mouseenter="showTooltip($event, '数字人中心')" @mouseleave="hideTooltip">
              <i class="ri-user-smile-line"></i>
              <span v-if="!isCollapsed" class="menu-text">数字人中心</span>
            </router-link>
          </li>
          
          <!-- AI办公与教学中心 -->
          <li class="menu-item" :class="{ active: activePage === 'ai-office' }">
            <router-link to="/ai-office" class="menu-link" @click="setActivePage('ai-office')"
              @mouseenter="showTooltip($event, 'AI办公与教学中心')" @mouseleave="hideTooltip">
              <i class="ri-briefcase-line"></i>
              <span v-if="!isCollapsed" class="menu-text">AI办公与教学中心</span>
            </router-link>
          </li>
          
          <!-- 专业生产力提升中心 -->
          <li class="menu-item" :class="{ active: activePage === 'productivity-center' }">
            <router-link to="/productivity-center" class="menu-link" @click="setActivePage('productivity-center')"
              @mouseenter="showTooltip($event, '专业生产力提升中心')" @mouseleave="hideTooltip">
              <i class="ri-rocket-line"></i>
              <span v-if="!isCollapsed" class="menu-text">专业生产力提升中心</span>
            </router-link>
          </li>
          
          <!-- AI基础理论与教学 -->
          <li class="menu-item" :class="{ active: activePage === 'ai-theory' }">
            <router-link to="/ai-theory" class="menu-link" @click="setActivePage('ai-theory')"
              @mouseenter="showTooltip($event, 'AI基础理论与教学')" @mouseleave="hideTooltip">
              <i class="ri-book-open-line"></i>
              <span v-if="!isCollapsed" class="menu-text">AI基础理论与教学</span>
            </router-link>
          </li>
          
          <!-- AI应用案例智能设计 -->
          <li class="menu-item" :class="{ active: activePage === 'ai-app-design' }" v-if="false">
            <router-link to="/ai-app-design" class="menu-link" @click="setActivePage('ai-app-design')"
              @mouseenter="showTooltip($event, 'AI应用案例智能设计')" @mouseleave="hideTooltip">
              <i class="ri-apps-line"></i>
              <span v-if="!isCollapsed" class="menu-text">AI应用案例智能设计</span>
            </router-link>
          </li>
        </ul>
      </nav>
    </aside>
    
    <!-- 全局提示框 -->
    <div class="global-tooltip" ref="tooltip" v-show="tooltipVisible">{{ tooltipText }}</div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

export default {
  name: 'SideMenu',
  setup() {
    const router = useRouter();
    const route = useRoute();
    const isCollapsed = ref(true);
    const activePage = ref('ai-chat');
    const tooltip = ref(null);
    const tooltipVisible = ref(false);
    const tooltipText = ref('');

    // 初始化时根据当前路由设置激活菜单
    onMounted(() => {
      setActivePageByRoute(route);
      
      // 监听路由变化
      watch(() => route.path, (newPath) => {
        setActivePageByRoute(route);
      });
    });

    const setActivePage = (page) => {
      activePage.value = page;
    };

    // 根据当前路由路径设置激活菜单
    const setActivePageByRoute = (route) => {
      const path = route.path;
      
      // 检查路径前缀来判断应该激活哪个菜单项
      if (path.startsWith('/ai-chat')) {
        activePage.value = 'ai-chat';
      } else if (path.startsWith('/prompt-engineering')) {
        activePage.value = 'prompt-engineering';
      } else if (path.includes('/ai-scenarios/marketing-campaign') || 
                 path.includes('/ai-scenarios/customer-feedback') || 
                 path.includes('/ai-scenarios/product-requirement')) {
        // 这些特定的业务场景路径应该对应到"基础业务场景AI应用实战"菜单
        activePage.value = 'practical-scenario';
      } else if (path.startsWith('/ai-scenarios')) {
        activePage.value = 'ai-scenarios';
      } else if (path.startsWith('/text-creation')) {
        activePage.value = 'text-creation';
      } else if (path.startsWith('/image-creation')) {
        activePage.value = 'image-creation';
      } else if (path.startsWith('/video-creation')) {
        activePage.value = 'video-creation';
      } else if (path.startsWith('/digital-human')) {
        activePage.value = 'digital-human';
      } else if (path.startsWith('/ai-office')) {
        activePage.value = 'ai-office';
      } else if (path.startsWith('/ai-theory')) {
        activePage.value = 'ai-theory';
      } else if (path.startsWith('/ai-case-studies')) {
        activePage.value = 'ai-case-studies';
      } else if (path.startsWith('/ai-app-design')) {
        activePage.value = 'ai-app-design';
      } else if (path.startsWith('/practical-scenario')) {
        activePage.value = 'practical-scenario';
      } else if (path.startsWith('/productivity-center')) {
        activePage.value = 'productivity-center';
      }
    };

    const showTooltip = (event, text) => {
      if (!isCollapsed.value) return;
      
      tooltipText.value = text;
      tooltipVisible.value = true;
      
      // 下一帧计算位置
      setTimeout(() => {
        if (tooltip.value) {
          const rect = event.target.getBoundingClientRect();
          tooltip.value.style.top = `${rect.top + rect.height/2}px`;
          tooltip.value.style.left = `${rect.right + 10}px`;
        }
      }, 0);
    };

    const hideTooltip = () => {
      tooltipVisible.value = false;
    };

    return {
      isCollapsed,
      activePage,
      tooltip,
      tooltipVisible,
      tooltipText,
      setActivePage,
      setActivePageByRoute,
      showTooltip,
      hideTooltip
    };
  }
};
</script>

<style scoped>
:root {
  --primary-color: #ba003f;
  --hover-color: #d4185b;
  --active-color: #9e0035;
  --text-color: #333;
  --text-light: #666;
  --border-color: #eee;
  --bg-light: #f9f9f9;
  --transition-speed: 0.3s;
}

.sidebar-container {
  position: relative;
}

.sidebar {
  width: 250px;
  height: 100%;
  background-color: white;
  border-right: 1px solid #eee;
  transition: width 0.3s ease;
  overflow-x: hidden;
  overflow-y: auto;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.sidebar.collapsed {
  width: 70px;
}

.menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu-item {
  position: relative;
}

.menu-link {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  color: #333;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s;
}

.menu-link i:first-child {
  font-size: 18px;
  margin-right: 10px;
  min-width: 20px;
  text-align: center;
}

.menu-item.active > .menu-link {
  color: #ba003f;
  background-color: rgba(186, 0, 63, 0.1);
}

.menu-link:hover {
  background-color: #f9f9f9;
  color: #ba003f;
}

.menu-text {
  white-space: nowrap;
}

.global-tooltip {
  position: fixed;
  background-color: #333;
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 14px;
  white-space: nowrap;
  z-index: 10000;
  pointer-events: none;
  transform: translateY(-50%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.global-tooltip:before {
  content: '';
  position: absolute;
  top: 50%;
  right: 100%;
  margin-top: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: transparent #333 transparent transparent;
}

.menu-group {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.submenu {
  margin-left: 20px;
  margin-top: 5px;
  display: flex;
  flex-direction: column;
}

.submenu-link {
  color: var(--text-light);
  text-decoration: none;
  font-size: 0.85rem;
  padding: 5px 0;
  transition: color var(--transition-speed);
}

.submenu-link:hover,
.submenu-link.active {
  color: var(--primary-color);
}
</style> 