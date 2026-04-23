import { createRouter, createWebHistory } from 'vue-router'

import AppLayout from '../layouts/AppLayout.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'dashboard',
          component: () => import('../views/dashboard/Index.vue'),
          meta: {
            title: '学习者仪表盘',
          },
        },
        {
          path: 'knowledge-graph',
          name: 'knowledge-graph',
          component: () => import('../views/knowledge-graph/Index.vue'),
          meta: {
            title: '知识图谱',
          },
        },
      ],
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/auth/Login.vue'),
      meta: {
        title: '登录',
      },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/auth/Register.vue'),
      meta: {
        title: '注册',
      },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFound.vue'),
      meta: {
        title: '页面不存在',
      },
    },
  ],
})

router.beforeEach((to, from, next) => {
  document.title = to.meta?.title ? `${to.meta.title} | 个性化学习系统` : '个性化学习系统'
  next()
})

export default router
