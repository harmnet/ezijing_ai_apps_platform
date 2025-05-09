// 添加研报大纲路由
const routes = [
  {
    path: '/text-creation',
    component: () => import('@/views/text-creation/index.vue'),
    meta: {
      title: '文本创作中心'
    },
    children: [
      // ... existing children routes ...
      
      // 添加研报大纲路由
      {
        path: 'report',
        component: () => import('@/views/text-creation/report/index.vue'),
        meta: {
          title: '智能研报大纲'
        }
      },
      
      // ... existing code ...
    ]
  }
] 