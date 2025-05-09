import { createRouter, createWebHistory } from 'vue-router';
import Layout from '../views/Layout.vue';
import HomePage from '../views/HomePage.vue';
import FinanceManager from '../views/ai-scenarios/FinanceManager.vue'
import SalesManager from '../views/ai-scenarios/SalesManager.vue'
import InternalAuditor from '../views/ai-scenarios/InternalAuditor.vue'
import MarketingManager from '../views/ai-scenarios/MarketingManager.vue'
import RequirementsEngineer from '../views/ai-scenarios/RequirementsEngineer.vue'
import TalentDevelopmentSpecialist from '../views/ai-scenarios/TalentDevelopmentSpecialist.vue'
import AfterSalesEngineer from '../views/ai-scenarios/AfterSalesEngineer.vue'
import CustomerManager from '../views/ai-scenarios/CustomerManager.vue'
import PracticalScenario from '../views/PracticalScenario.vue';
import MarketingCampaign from '../views/ai-scenarios/MarketingCampaign.vue'
import CustomerFeedback from '../views/ai-scenarios/CustomerFeedback.vue'
import BaiduDigitalHuman from '../views/digital-human/BaiduDigitalHuman.vue'
import DigitalHumanVideoCreation from '../views/digital-human/VideoCreation.vue'
import DigitalHumanFunctionalList from '../views/digital-human/FunctionalList.vue'
import BaiduDigitalHumanAdvanceNew from '../views/digital-human/BaiduDigitalHumanAdvanceNew.vue'

// 路由配置
const routes = [
  {
    path: '/',
    component: Layout,
    children: [
      {
        path: '',
        name: 'HomePage',
        component: HomePage
      },
      {
        path: 'ai-chat',
        name: 'AIChat',
        component: () => import('../views/AIChat.vue')
      },
      {
        path: 'prepare-study',
        name: 'PrepareStudy',
        component: () => import('../views/PrepareStudy.vue'),
        meta: {
          title: '准备篇：人工智能应用技能入门',
          icon: 'ri-book-read-line'
        }
      },
      {
        path: 'increase-efficiency',
        name: 'IncreaseEfficiency',
        component: () => import('../views/IncreaseEfficiency.vue'),
        meta: {
          title: '效率飞跃篇：AI应用效率倍增',
          icon: 'ri-rocket-line'
        }
      },
      {
        path: '/prompt-engineering',
        name: 'PromptEngineering',
        component: () => import('../views/text-creation/prompt-engineering/index.vue'),
        meta: {
          title: '提示词工程助手',
          icon: 'mdi-file-document-edit-outline'
        }
      },
      {
        path: '/prompt-case',
        name: 'PromptCase',
        component: () => import('../views/PromptCase.vue'),
        meta: {
          title: '提示词工程案例学习',
          icon: 'ri-book-mark-line'
        }
      },
      {
        path: 'practical-scenario',
        name: 'PracticalScenario',
        component: PracticalScenario,
        meta: {
          title: 'AI场景实践',
          icon: 'ri-file-list-3-line'
        }
      },
      {
        path: 'ai-case-studies',
        name: 'AICaseStudies',
        component: () => import('../views/ai-case-studies/index.vue'),
        children: [
          {
            path: '',
            name: 'CaseStudiesList',
            component: () => import('../views/ai-case-studies/CaseStudiesList.vue'),
            meta: {
              title: '人工智能应用综合案例集',
              icon: 'ri-book-mark-line'
            }
          },
          {
            path: 'marketing',
            name: 'MarketingCase',
            component: () => import('../views/ai-case-studies/MarketingCase.vue'),
            meta: {
              title: 'AI市场营销综合应用案例',
              icon: 'ri-advertisement-line'
            }
          }
        ]
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
            path: 'sales-manager',
            name: 'SalesManager',
            component: SalesManager,
            meta: {
              title: '销售经理详情页',
            },
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
          },
          {
            path: 'marketing-manager',
            name: 'marketing-manager',
            component: MarketingManager,
            meta: {
              title: '市场经理详情页',
            },
          },
          {
            path: 'purchasing-manager',
            name: 'purchasing-manager',
            component: () => import('@/views/ai-scenarios/PurchasingManager.vue'),
            meta: {
              title: '采购经理详情页',
            },
          },
          {
            path: 'logistics-manager',
            name: 'logistics-manager',
            component: () => import('@/views/ai-scenarios/LogisticsManager.vue'),
            meta: {
              title: '物流经理详情页',
            },
          },
          {
            path: 'inventory-specialist',
            name: 'inventory-specialist',
            component: () => import('@/views/ai-scenarios/InventorySpecialist.vue'),
            meta: {
              title: '库存管理专员详情页',
            },
          },
          {
            path: 'product-manager',
            name: 'product-manager',
            component: () => import('@/views/ai-scenarios/ProductManager.vue'),
            meta: {
              title: '产品经理详情页',
            },
          },
          {
            path: 'requirements-engineer',
            name: 'RequirementsEngineer',
            component: RequirementsEngineer,
            meta: {
              title: '需求工程师详情页'
            }
          },
          {
            path: 'finance-manager',
            name: 'FinanceManager',
            component: FinanceManager,
            meta: {
              title: '财务经理详情页'
            }
          },
          {
            path: 'internal-auditor',
            name: 'InternalAuditor',
            component: InternalAuditor,
            meta: {
              title: '内部审计师详情页'
            }
          },
          {
            path: 'development-engineer',
            name: 'development-engineer',
            component: () => import('@/views/ai-scenarios/DevelopmentEngineer.vue'),
            meta: {
              title: '研发工程师详情页',
            },
          },
          {
            path: 'test-engineer',
            name: 'test-engineer',
            component: () => import('@/views/ai-scenarios/TestEngineer.vue'),
            meta: {
              title: '测试工程师详情页',
            },
          },
          {
            path: 'ui-design-engineer',
            name: 'ui-design-engineer',
            component: () => import('@/views/ai-scenarios/UIDesignEngineer.vue'),
            meta: {
              title: 'UI设计工程师详情页',
            },
          },
          {
            path: 'legal-compliance-manager',
            name: 'LegalComplianceManager',
            component: () => import('../views/ai-scenarios/LegalComplianceManager.vue'),
            meta: {
              title: '法务合规经理详情页',
              icon: 'ri-shield-check-line'
            }
          },
          {
            path: 'admin-specialist',
            name: 'AdminSpecialist',
            component: () => import('../views/ai-scenarios/AdminSpecialist.vue'),
            meta: {
              title: '行政专员详情页',
              icon: 'ri-briefcase-4-line'
            }
          },
          {
            path: 'recruitment-manager',
            name: 'RecruitmentManager',
            component: () => import('../views/ai-scenarios/RecruitmentManager.vue'),
            meta: {
              title: '人才招聘经理详情页',
              icon: 'ri-user-search-line'
            }
          },
          {
            path: 'customer-manager',
            name: 'customer-manager',
            component: CustomerManager,
            meta: {
              title: '客户经理详情页',
            },
          },
          {
            path: 'after-sales-engineer',
            name: 'after-sales-engineer',
            component: AfterSalesEngineer,
            meta: {
              title: '售后工程师详情页',
            },
          },
          {
            path: 'talent-development-specialist',
            name: 'talent-development-specialist',
            component: TalentDevelopmentSpecialist,
            meta: {
              title: '人才培养专员详情页',
            },
          },
          {
            path: 'marketing-campaign',
            name: 'marketing-campaign',
            component: MarketingCampaign,
            meta: {
              title: '市场活动策划场景',
            },
          },
          {
            path: 'customer-feedback',
            name: 'customer-feedback',
            component: CustomerFeedback,
            meta: {
              title: '产品方案编写场景',
            },
          },
          {
            path: 'product-requirement',
            name: 'product-requirement',
            component: () => import('@/views/ai-scenarios/ProductRequirement.vue'),
            meta: {
              title: '产品需求分析与规划场景',
            },
          },
          {
            path: 'training-material',
            name: 'training-material',
            component: () => import(/* webpackChunkName: "training-material" */ '../views/ai-scenarios/Placeholder.vue'),
            meta: {
              title: '培训材料开发场景',
            },
          },
          {
            path: 'financial-report',
            name: 'financial-report',
            component: () => import(/* webpackChunkName: "financial-report" */ '../views/ai-scenarios/Placeholder.vue'),
            meta: {
              title: '财务报告解读与决策支持场景',
            },
          },
          {
            path: 'dev-documentation',
            name: 'dev-documentation',
            component: () => import(/* webpackChunkName: "dev-documentation" */ '../views/ai-scenarios/Placeholder.vue'),
            meta: {
              title: '研发文档撰写与管理场景',
            },
          },
          {
            path: 'multilingual-content',
            name: 'multilingual-content',
            component: () => import(/* webpackChunkName: "multilingual-content" */ '../views/ai-scenarios/Placeholder.vue'),
            meta: {
              title: '多语言内容本地化场景',
            },
          },
          {
            path: 'brand-design',
            name: 'brand-design',
            component: () => import(/* webpackChunkName: "brand-design" */ '../views/ai-scenarios/Placeholder.vue'),
            meta: {
              title: '品牌形象视觉设计场景',
            },
          },
          {
            path: 'brand-visual-design',
            name: 'brand-visual-design',
            component: () => import('../views/ai-scenarios/BrandVisualDesign.vue'),
            meta: {
              title: '产品需求分析与规划',
            },
          },
          {
            path: 'recruitment',
            name: 'recruitment',
            component: () => import(/* webpackChunkName: "recruitment" */ '../views/ai-scenarios/Placeholder.vue'),
            meta: {
              title: '招聘流程自动化场景',
            },
          },
          {
            path: 'knowledge-base',
            name: 'knowledge-base',
            component: () => import(/* webpackChunkName: "knowledge-base" */ '../views/ai-scenarios/Placeholder.vue'),
            meta: {
              title: '企业知识库构建与优化场景',
            },
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
            name: 'PaperOutline',
            component: () => import('../views/text-creation/academic/ReportSummary.vue')
          },
          {
            path: 'academic/paper-history',
            name: 'PaperHistory',
            component: () => import('../views/text-creation/academic/PaperHistory.vue')
          },
          {
            path: 'academic/search',
            name: 'AcademicSearch',
            component: () => import('../views/text-creation/academic/AcademicSearch.vue'),
            meta: {
              title: '学术搜索'
            }
          },
          {
            path: 'academic/plagiarism',
            name: 'PlagiarismCheck',
            component: () => import('../views/text-creation/academic/PlagiarismCheck.vue')
          },
          {
            path: 'academic/translation',
            name: 'Translation',
            component: () => import('../views/text-creation/academic/Translation.vue'),
            meta: {
              title: '学术搜索'
            }
          },
          // 添加智能研报大纲路由
          {
            path: 'academic/report-outline',
            name: 'ReportOutline',
            component: () => import('../views/text-creation/report/index.vue')
          },
          // 添加大纲生成研报路由
          {
            path: 'academic/outline-to-report',
            name: 'OutlineToReport',
            component: () => import('../views/text-creation/report/index.vue')
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
            path: 'intelligent-design',
            name: 'IntelligentDesign',
            component: () => import('../views/image-creation/IntelligentDesign.vue')
          },
          {
            path: 'image-to-painter',
            name: 'ImageToPainter',
            component: () => import('../views/image-creation/ImageToPainter.vue')
          },
          {
            path: 'image-to-design',
            name: 'ImageToDesign',
            component: () => import('../views/image-creation/ImageToDesign.vue')
          },
          {
            path: 'image-matting',
            name: 'ImageMatting',
            component: () => import('../views/image-creation/ImageMatting.vue')
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
        component: () => import('../views/digital-human/index.vue'),
        children: [
          {
            path: '',
            name: 'DigitalHumanList',
            component: DigitalHumanFunctionalList,
            meta: {
              title: 'AI数字人功能列表',
              icon: 'ri-robot-line'
            }
          },
          {
            path: 'video-creation',
            name: 'DigitalHumanVideoCreation',
            component: DigitalHumanVideoCreation,
            meta: {
              title: 'AI数字人视频制作',
              icon: 'ri-user-voice-line'
            }
          },
          {
            path: 'ppt-video',
            name: 'DigitalHumanPPTVideo',
            component: () => import('../views/digital-human/PPTVideo.vue'),
            meta: {
              title: 'AI数字人微课制作',
              icon: 'ri-presentation-line'
            }
          },
          {
            path: 'advance-video',
            name: 'BaiduDigitalHumanAdvance',
            component: BaiduDigitalHumanAdvanceNew,
            meta: {
              title: 'AI数字人高级视频',
              icon: 'ri-robot-line'
            }
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
          },
          // 添加AI知识库问答路由
          {
            path: 'knowledge-qa',
            component: () => import('../views/ai-office/KnowledgeQA.vue'),
            name: 'KnowledgeQA',
            meta: {
              title: 'AI知识库问答',
              icon: 'ri-question-answer-line',
              affix: false,
              roles: ['admin', 'user', 'visitor'],
            },
          }
        ]
      },
      {
        path: 'productivity-center',
        name: 'ProductivityCenter',
        component: () => import('../views/productivity-center/index.vue'),
        meta: {
          title: '专业生产力提升中心',
          icon: 'ri-rocket-line'
        }
      },
      {
        path: 'ai-theory',
        name: 'AITheory',
        component: () => import('../views/Study.vue')
      },
      {
        path: 'ai-app-design',
        name: 'AIAppDesign',
        component: () => import('../views/ai-app-design/index.vue'),
        children: [
          {
            path: '',
            name: 'AppDesignList',
            component: () => import('../views/ai-app-design/AppDesignList.vue'),
            meta: {
              title: 'AI应用案例智能设计',
              icon: 'ri-layout-masonry-line'
            }
          },
          {
            path: 'case-edit/:id',
            name: 'AppCaseEdit',
            component: () => import('../views/ai-app-design/AppCaseEdit.vue'),
            meta: {
              title: '编辑AI应用案例',
              icon: 'ri-edit-box-line'
            }
          }
        ]
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