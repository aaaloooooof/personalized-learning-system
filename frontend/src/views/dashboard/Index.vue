<script setup>
import { computed, onMounted, reactive } from 'vue'

import {
  fetchAssessmentResults,
  fetchKnowledgePoints,
  fetchLearners,
  fetchLearningPaths,
  fetchLearningRecords,
} from '../../api/dashboard'
import LearningPathTimeline from './components/LearningPathTimeline.vue'
import MasteryRadarChart from './components/MasteryRadarChart.vue'

const state = reactive({
  loading: true,
  error: '',
  learners: [],
  learningPaths: [],
  learningRecords: [],
  assessmentResults: [],
  knowledgePoints: [],
})

function normalizeList(payload) {
  if (Array.isArray(payload)) {
    return payload
  }

  if (Array.isArray(payload?.results)) {
    return payload.results
  }

  return []
}

const activeLearner = computed(() => state.learners[0] || null)

const summaryCards = computed(() => {
  const completedRecords = state.learningRecords.filter((item) => item.completed).length
  const avgScore = state.assessmentResults.length
    ? state.assessmentResults.reduce((sum, item) => sum + Number(item.score || 0), 0) /
      state.assessmentResults.length
    : 0

  return [
    {
      label: '学习者总数',
      value: state.learners.length,
      hint: '当前系统中已同步的学习者档案',
    },
    {
      label: '学习路径',
      value: state.learningPaths.length,
      hint: '已配置的路径总量',
    },
    {
      label: '已完成记录',
      value: completedRecords,
      hint: '学习记录中标记完成的内容数',
    },
    {
      label: '平均测评分',
      value: `${Math.round(avgScore)} 分`,
      hint: '来自当前接口可见的测评结果',
    },
  ]
})

const radarItems = computed(() => {
  const totalRecords = state.learningRecords.length
  const completedRecords = state.learningRecords.filter((item) => item.completed).length
  const avgProgress = totalRecords
    ? state.learningRecords.reduce((sum, item) => sum + Number(item.progress || 0), 0) / totalRecords
    : 0
  const avgAssessment = state.assessmentResults.length
    ? state.assessmentResults.reduce((sum, item) => sum + Number(item.score || 0), 0) /
      state.assessmentResults.length
    : 0
  const avgPathCoverage = state.learningPaths.length
    ? (state.learningPaths.filter((item) => (item.path_nodes || []).length > 0).length /
        state.learningPaths.length) *
      100
    : 0
  const knowledgeBreadth = Math.min(100, state.knowledgePoints.length * 10)

  return [
    {
      label: '学习投入',
      value: avgProgress,
    },
    {
      label: '内容完成',
      value: totalRecords ? (completedRecords / totalRecords) * 100 : 0,
    },
    {
      label: '路径覆盖',
      value: avgPathCoverage,
    },
    {
      label: '测评表现',
      value: avgAssessment,
    },
    {
      label: '知识广度',
      value: knowledgeBreadth,
    },
  ]
})

onMounted(async () => {
  state.loading = true
  state.error = ''

  try {
    const [learners, learningPaths, learningRecords, assessmentResults, knowledgePoints] =
      await Promise.all([
        fetchLearners(),
        fetchLearningPaths(),
        fetchLearningRecords(),
        fetchAssessmentResults(),
        fetchKnowledgePoints(),
      ])

    state.learners = normalizeList(learners)
    state.learningPaths = normalizeList(learningPaths)
    state.learningRecords = normalizeList(learningRecords)
    state.assessmentResults = normalizeList(assessmentResults)
    state.knowledgePoints = normalizeList(knowledgePoints)
  } catch (error) {
    state.error = error.message || '仪表盘加载失败，请稍后重试。'
  } finally {
    state.loading = false
  }
})
</script>

<template>
  <section class="dashboard-page">
    <header class="hero-card">
      <div class="hero-copy">
        <span class="eyebrow">Learner Dashboard</span>
        <h1>学习者仪表盘</h1>
        <p>
          聚合学习者、路径、学习记录与测评表现，用一个页面快速理解当前学习系统的运行状态。
        </p>
      </div>

      <div class="profile-card">
        <p class="profile-label">当前焦点学习者</p>
        <template v-if="activeLearner">
          <strong>{{ activeLearner.user_username }}</strong>
          <span>{{ activeLearner.user_email || '暂无邮箱信息' }}</span>
          <small>
            学习风格：{{ activeLearner.learning_style }} · 综合得分：{{ activeLearner.total_score }}
          </small>
        </template>
        <template v-else>
          <strong>暂无学习者数据</strong>
          <span>后端接口已连接，等待业务数据进入系统。</span>
        </template>
      </div>
    </header>

    <div v-if="loading" class="state-card state-card--loading">
      仪表盘数据加载中，请稍候…
    </div>

    <div v-else-if="error" class="state-card state-card--error">
      {{ error }}
    </div>

    <template v-else>
      <section class="stats-grid">
        <article v-for="card in summaryCards" :key="card.label" class="stat-card">
          <span>{{ card.label }}</span>
          <strong>{{ card.value }}</strong>
          <small>{{ card.hint }}</small>
        </article>
      </section>

      <section class="content-grid">
        <MasteryRadarChart :items="radarItems" />
        <LearningPathTimeline :items="state.learningPaths" />
      </section>

      <section class="detail-grid">
        <article class="detail-card">
          <div class="detail-head">
            <h2>近期学习记录</h2>
            <span>{{ state.learningRecords.length }} 条</span>
          </div>
          <ul v-if="state.learningRecords.length" class="detail-list">
            <li v-for="record in state.learningRecords.slice(0, 6)" :key="record.id">
              <div>
                <strong>{{ record.learning_content_title }}</strong>
                <p>{{ record.learner_username }}</p>
              </div>
              <span class="badge">{{ Math.round(record.progress) }}%</span>
            </li>
          </ul>
          <div v-else class="empty-block">暂无学习记录。</div>
        </article>

        <article class="detail-card">
          <div class="detail-head">
            <h2>测评结果概览</h2>
            <span>{{ state.assessmentResults.length }} 条</span>
          </div>
          <ul v-if="state.assessmentResults.length" class="detail-list">
            <li v-for="result in state.assessmentResults.slice(0, 6)" :key="result.id">
              <div>
                <strong>{{ result.assessment_title }}</strong>
                <p>{{ result.learner_username }}</p>
              </div>
              <span
                class="badge"
                :class="{ 'badge--success': result.passed, 'badge--muted': !result.passed }"
              >
                {{ Math.round(result.score) }} 分
              </span>
            </li>
          </ul>
          <div v-else class="empty-block">暂无测评结果。</div>
        </article>
      </section>
    </template>
  </section>
</template>

<style scoped>
.dashboard-page {
  display: grid;
  gap: 22px;
}

.hero-card {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 18px;
  padding: 28px;
  border-radius: 32px;
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(148, 163, 184, 0.22);
  box-shadow: 0 20px 48px rgba(15, 23, 42, 0.06);
}

.eyebrow {
  display: inline-flex;
  padding: 8px 12px;
  border-radius: 999px;
  color: #2563eb;
  background: rgba(219, 234, 254, 0.92);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.hero-copy h1 {
  margin: 16px 0 12px;
  font-size: clamp(2.2rem, 5vw, 3.4rem);
  line-height: 1.05;
}

.hero-copy p {
  margin: 0;
  max-width: 52rem;
  color: #64748b;
  line-height: 1.8;
}

.profile-card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 10px;
  padding: 22px;
  border-radius: 24px;
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(15, 118, 110, 0.12));
}

.profile-label {
  margin: 0;
  color: #0f766e;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.profile-card strong {
  font-size: 24px;
}

.profile-card span,
.profile-card small {
  color: #475569;
}

.state-card {
  padding: 18px 20px;
  border-radius: 18px;
  font-weight: 500;
}

.state-card--loading {
  color: #0f766e;
  background: rgba(204, 251, 241, 0.8);
}

.state-card--error {
  color: #b91c1c;
  background: rgba(254, 226, 226, 0.86);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.stat-card {
  display: grid;
  gap: 10px;
  padding: 22px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.stat-card span {
  color: #64748b;
  font-size: 14px;
}

.stat-card strong {
  font-size: 34px;
  color: #0f172a;
}

.stat-card small {
  color: #94a3b8;
  line-height: 1.6;
}

.content-grid {
  display: grid;
  grid-template-columns: 0.9fr 1.1fr;
  gap: 18px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.detail-card {
  padding: 24px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(148, 163, 184, 0.22);
  box-shadow: 0 16px 40px rgba(15, 23, 42, 0.05);
}

.detail-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}

.detail-head h2 {
  margin: 0;
  font-size: 20px;
}

.detail-head span {
  padding: 6px 10px;
  border-radius: 999px;
  color: #2563eb;
  font-size: 12px;
  background: rgba(219, 234, 254, 0.92);
}

.detail-list {
  display: grid;
  gap: 12px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.detail-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding: 14px 16px;
  border-radius: 18px;
  background: rgba(248, 250, 252, 0.92);
}

.detail-list strong {
  display: block;
  margin-bottom: 6px;
}

.detail-list p {
  margin: 0;
  color: #64748b;
  font-size: 14px;
}

.badge {
  white-space: nowrap;
  padding: 8px 12px;
  border-radius: 999px;
  color: #1d4ed8;
  background: rgba(219, 234, 254, 0.92);
}

.badge--success {
  color: #047857;
  background: rgba(209, 250, 229, 0.95);
}

.badge--muted {
  color: #92400e;
  background: rgba(254, 243, 199, 0.95);
}

.empty-block {
  padding: 18px;
  border-radius: 18px;
  color: #64748b;
  background: rgba(248, 250, 252, 0.92);
}

@media (max-width: 1080px) {
  .hero-card,
  .content-grid,
  .detail-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .hero-card,
  .detail-card {
    padding: 20px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .detail-list li {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
