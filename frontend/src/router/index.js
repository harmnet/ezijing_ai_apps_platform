import { createRouter, createWebHistory } from 'vue-router';
import Layout from '../views/Layout.vue';
import HomePage from '../views/HomePage.vue';

// 路由配置
const routes = [
  {
    path: '/',
    component: Layout,
    children: [
      {
        path: '',
        name: 'HomePage',
        component: () => import('../views/AIChat.vue')
      },
      {
        path: 'ai-chat',
        name: 'AIChat',
        component: () => import('../views/AIChat.vue')
      },
      {
        path: 'prompt-engineering',
        name: 'PromptEngineering',
        component: () => import('../views/prompt-engineering/index.vue')
      },
      {
        path: 'ai-scenarios',
        name: 'AIScenarios',
        component: () => import('../views/ai-scenarios/index.vue'),
        children: [
          {
            path: '',
            name: 'AIScenariosList',
            component: () => import('../views/ai-scenarios/ScenariosList.vue')
          },
          {
            path: 'hr',
            name: 'HRScenarios',
            component: () => import('../views/ai-scenarios/HRScenarios.vue')
          },
          {
            path: 'marketing',
            name: 'MarketingScenarios',
            component: () => import('../views/ai-scenarios/MarketingScenarios.vue')
          },
          {
            path: 'admin',
            name: 'AdminScenarios',
            component: () => import('../views/ai-scenarios/AdminScenarios.vue')
          },
          {
            path: 'operation',
            name: 'OperationScenarios',
            component: () => import('../views/ai-scenarios/OperationScenarios.vue')
          },
          {
            path: 'product',
            name: 'ProductScenarios',
            component: () => import('../views/ai-scenarios/ProductScenarios.vue')
          }
        ]
      },
      {
        path: 'text-creation',
        name: 'TextCreation',
        component: () => import('../views/text-creation/index.vue'),
        children: [
          // 营销创作路由
          {
            path: 'marketing/ad-slogan',
            name: 'AdSlogan',
            component: () => import('../views/text-creation/marketing/AdSlogan.vue')
          },
          {
            path: 'marketing/copywriting-generator',
            name: 'CopywritingGenerator',
            component: () => import('../views/text-creation/marketing/CopywritingGenerator.vue')
          },
          // 新媒体内容创作路由
          {
            path: 'new-media/wechat',
            name: 'WechatArticle',
            component: () => import('../views/text-creation/new-media/WechatArticle.vue')
          },
          {
            path: 'new-media/weibo',
            name: 'WeiboArticle',
            component: () => import('../views/text-creation/new-media/WeiboArticle.vue')
          },
          {
            path: 'new-media/xiaohongshu',
            name: 'XiaohongshuArticle',
            component: () => import('../views/text-creation/new-media/XiaohongshuArticle.vue')
          },
          {
            path: 'new-media/short-video',
            name: 'ShortVideoScript',
            component: () => import('../views/text-creation/new-media/ShortVideoScript.vue')
          },
          {
            path: 'new-media/livestream',
            name: 'LivestreamScript',
            component: () => import('../views/text-creation/new-media/LivestreamScript.vue')
          },
          // 文案创作路由
          {
            path: 'copywriting/document-structure',
            name: 'DocumentStructure',
            component: () => import('../views/text-creation/copywriting/DocumentStructure.vue')
          },
          {
            path: 'copywriting/longform',
            name: 'Longform',
            component: () => import('../views/text-creation/copywriting/Longform.vue')
          },
          {
            path: 'copywriting/poetry',
            name: 'Poetry',
            component: () => import('../views/text-creation/copywriting/Poetry.vue')
          },
          // 文本修订路由
          {
            path: 'revision/proofreading',
            name: 'Proofreading',
            component: () => import('../views/text-creation/revision/Proofreading.vue')
          },
          {
            path: 'revision/refinement',
            name: 'Refinement',
            component: () => import('../views/text-creation/revision/Refinement.vue')
          },
          {
            path: 'revision/summary',
            name: 'Summary',
            component: () => import('../views/text-creation/revision/Summary.vue')
          },
          // 学术文案路由
          {
            path: 'academic/paper-abstract',
            name: 'PaperAbstract',
            component: () => import('../views/text-creation/academic/PaperAbstract.vue')
          },
          {
            path: 'academic/report-summary',
            name: 'ReportSummary',
            component: () => import('../views/text-creation/academic/ReportSummary.vue')
          },
          {
            path: 'academic/search',
            name: 'AcademicSearch',
            component: () => import('../views/text-creation/academic/AcademicSearch.vue')
          },
          {
            path: 'academic/plagiarism',
            name: 'PlagiarismCheck',
            component: () => import('../views/text-creation/academic/PlagiarismCheck.vue')
          },
          {
            path: 'academic/translation',
            name: 'Translation',
            component: () => import('../views/text-creation/academic/Translation.vue')
          },
          // 添加合同检查路由，注释掉原位置
          /*{
            path: 'legal/contract-check',
            component: () => import('../views/text-creation/legal/ContractCheck.vue'),
            name: 'ContractCheck',
            meta: {
              title: '合同检查',
              icon: 'ri-file-search-line',
              affix: false,
              roles: ['admin', 'user', 'visitor'],
            },
          }*/
        ]
      },
      {
        path: 'image-creation',
        name: 'ImageCreation',
        component: () => import('../views/image-creation/index.vue'),
        children: [
          {
            path: 'online-design',
            name: 'OnlineDesign',
            component: () => import('../views/image-creation/OnlineDesign.vue')
          },
          {
            path: 'text-to-image',
            name: 'TextToImage',
            component: () => import('../views/image-creation/TextToImage.vue')
          },
          {
            path: 'image-to-image',
            name: 'ImagetoImage',
            component: () => import('../views/image-creation/ImagetoImage.vue')
          },
          {
            path: 'image-redraw',
            name: 'ImageRedraw',
            component: () => import('../views/image-creation/ImageRedraw.vue')
          },
          /* 暂时注释掉不存在的组件
          {
            path: 'image-editing',
            name: 'ImageEditing',
            component: () => import('../views/image-creation/ImageEditing.vue')
          },
          {
            path: 'image-enhancement',
            name: 'ImageEnhancement',
            component: () => import('../views/image-creation/ImageEnhancement.vue')
          }
          */
        ]
      },
      {
        path: 'video-creation',
        name: 'VideoCreation',
        component: () => import('../views/video-creation/index.vue'),
        children: [
          {
            path: 'text-to-video',
            name: 'TextToVideo',
            component: () => import('../views/video-creation/TextToVideo.vue')
          },
          {
            path: 'image-to-video',
            name: 'ImageToVideo',
            component: () => import('../views/video-creation/ImageToVideo.vue')
          }
        ]
      },
      {
        path: 'digital-human',
        name: 'DigitalHuman',
        children: [
          {
            path: '',
            name: 'DigitalHumanFunctionalList',
            component: () => import('../views/digital-human/FunctionalList.vue')
          },
          {
            path: 'ppt-video',
            name: 'DigitalHumanPPTVideo',
            component: () => import('../views/digital-human/PPTVideo.vue')
          }
        ]
      },
      {
        path: 'ai-office',
        name: 'AIOfficeSuite',
        component: () => import('../views/ai-office/index.vue'),
        children: [
          {
            path: 'ppt',
            name: 'AIPPT',
            component: () => import('../views/ai-office/AIPPT.vue')
          },
          {
            path: 'integration-test',
            name: 'IntegrationTest',
            component: () => import('../views/ai-office/IntegrationTest.vue')
          },
          {
            path: 'meeting-minutes',
            name: 'MeetingMinutes',
            component: () => import('../views/ai-office/MeetingMinutes.vue')
          },
          // 添加招聘JD生成路由
          {
            path: 'jd-maker',
            component: () => import('../views/ai-office/JDMaker.vue'),
            name: 'JDMaker',
            meta: {
              title: 'AI招聘JD生成',
              icon: 'ri-file-list-3-line',
              affix: false,
              roles: ['admin', 'user', 'visitor'],
            },
          },
          // 添加简历优化路由
          {
            path: 'cv-optimize',
            component: () => import('../views/ai-office/CVOptimize.vue'),
            name: 'CVOptimize',
            meta: {
              title: 'AI简历优化',
              icon: 'ri-file-text-line',
              affix: false,
              roles: ['admin', 'user', 'visitor'],
            },
          },
          // 添加合同检查路由
          {
            path: 'legal/contract-check',
            component: () => import('../views/ai-office/legal/ContractCheck.vue'),
            name: 'ContractCheck',
            meta: {
              title: '合同检查',
              icon: 'ri-file-search-line',
              affix: false,
              roles: ['admin', 'user', 'visitor'],
            },
          },
          // 添加数据分析路由
          {
            path: 'data-analysis',
            component: () => import('../views/ai-office/DataAnaysis.vue'),
            name: 'DataAnalysis',
            meta: {
              title: 'AI数据分析',
              icon: 'ri-bar-chart-line',
              affix: false,
              roles: ['admin', 'user', 'visitor'],
            },
          }
        ]
      },
      {
        path: 'ai-theory',
        name: 'AITheory',
        component: () => import('../views/Study.vue')
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/:catchAll(.*)',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue')
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router; 