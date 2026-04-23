<script setup>
import { computed, ref, watch } from 'vue'

import { getConceptDetails } from '../../../api/graph'

const props = defineProps({
  conceptId: {
    type: [String, Number],
    default: '',
  },
  visible: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close'])

const loading = ref(false)
const error = ref('')
const detail = ref(null)

const masteryPercent = computed(() => {
  const raw = detail.value?.concept?.mastery_score

  if (typeof raw === 'number') {
    return Math.round(raw)
  }

  return Math.round(Number(detail.value?.concept?.weight || 0) * 100)
})

async function loadConceptDetails() {
  if (!props.conceptId || !props.visible) {
    return
  }

  loading.value = true
  error.value = ''

  try {
    detail.value = await getConceptDetails(props.conceptId)
  } catch (requestError) {
    error.value = requestError.message || '加载知识点详情失败。'
  } finally {
    loading.value = false
  }
}

watch(
  () => [props.conceptId, props.visible],
  async () => {
    if (!props.visible) {
      return
    }

    await loadConceptDetails()
  },
  { immediate: true },
)
</script>

<template>
  <transition name="drawer-fade">
    <div v-if="visible" class="drawer-overlay" @click.self="emit('close')">
      <aside class="drawer-panel">
        <div class="drawer-head">
          <div>
            <p class="drawer-kicker">Concept Insight</p>
            <h3>知识点详情</h3>
          </div>
          <button class="close-button" type="button" @click="emit('close')">关闭</button>
        </div>

        <div v-if="loading" class="drawer-body">
          <div class="skeleton skeleton-title" />
          <div class="skeleton skeleton-line" />
          <div class="skeleton skeleton-line" />
          <div class="skeleton skeleton-card" />
          <div class="skeleton skeleton-card" />
        </div>

        <div v-else-if="error" class="drawer-body">
          <div class="message message--error">{{ error }}</div>
        </div>

        <div v-else-if="detail" class="drawer-body">
          <section class="hero-card">
            <div>
              <span class="status-pill">{{ detail.concept.status || 'unknown' }}</span>
              <h4>{{ detail.concept.name }}</h4>
              <p>{{ detail.concept.description || '当前知识点暂无详细描述。' }}</p>
            </div>
            <div class="score-ring">
              <strong>{{ masteryPercent }}%</strong>
              <span>掌握度</span>
            </div>
          </section>

          <section class="meta-grid">
            <article class="meta-card">
              <span>前置知识</span>
              <strong>{{ detail.concept.prerequisite_name || '无' }}</strong>
            </article>
            <article class="meta-card">
              <span>权重</span>
              <strong>{{ detail.concept.weight ?? '--' }}</strong>
            </article>
            <article class="meta-card">
              <span>关联资源</span>
              <strong>{{ detail.relatedContents.length }}</strong>
            </article>
            <article class="meta-card">
              <span>关联路径</span>
              <strong>{{ detail.relatedPaths.length }}</strong>
            </article>
          </section>

          <section class="section-card">
            <div class="section-head">
              <h5>推荐学习资源</h5>
            </div>
            <ul v-if="detail.relatedContents.length" class="resource-list">
              <li v-for="content in detail.relatedContents" :key="content.id">
                <div>
                  <strong>{{ content.title }}</strong>
                  <p>{{ content.format }} · {{ content.duration }} 分钟</p>
                </div>
                <a :href="content.content_url" target="_blank" rel="noreferrer">查看</a>
              </li>
            </ul>
            <div v-else class="message">暂无资源数据。</div>
          </section>

          <section class="section-card">
            <div class="section-head">
              <h5>所在学习路径</h5>
            </div>
            <ul v-if="detail.relatedPaths.length" class="path-list">
              <li v-for="path in detail.relatedPaths" :key="path.id">
                <strong>{{ path.learning_path_name }}</strong>
                <span>Step {{ path.sort_order }}</span>
              </li>
            </ul>
            <div v-else class="message">该知识点暂未编入学习路径。</div>
          </section>
        </div>

        <div v-else class="drawer-body">
          <div class="message">请选择图谱中的知识点查看详情。</div>
        </div>
      </aside>
    </div>
  </transition>
</template>

<style scoped>
.drawer-overlay {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: flex;
  justify-content: flex-end;
  background: rgba(8, 15, 32, 0.18);
  backdrop-filter: blur(4px);
}

.drawer-panel {
  width: min(420px, 100%);
  height: 100%;
  padding: 24px;
  overflow-y: auto;
  border-left: 1px solid rgba(167, 186, 211, 0.32);
  background:
    linear-gradient(180deg, rgba(251, 253, 255, 0.96), rgba(239, 245, 255, 0.98));
  box-shadow: -24px 0 60px rgba(18, 41, 80, 0.14);
  backdrop-filter: blur(18px);
}

.drawer-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
}

.drawer-kicker {
  margin: 0 0 8px;
  color: #6581a9;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.drawer-head h3 {
  margin: 0;
  font-size: 26px;
  color: #143056;
}

.close-button {
  padding: 10px 14px;
  border: 0;
  border-radius: 999px;
  color: #35537a;
  background: rgba(220, 231, 247, 0.9);
  cursor: pointer;
}

.drawer-body {
  display: grid;
  gap: 16px;
}

.hero-card {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 16px;
  padding: 20px;
  border-radius: 24px;
  background:
    radial-gradient(circle at top left, rgba(125, 211, 252, 0.18), transparent 42%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.94), rgba(241, 246, 255, 0.94));
  border: 1px solid rgba(167, 186, 211, 0.28);
}

.status-pill {
  display: inline-flex;
  padding: 7px 11px;
  border-radius: 999px;
  color: #2d4c7e;
  font-size: 12px;
  font-weight: 700;
  background: rgba(215, 227, 247, 0.92);
}

.hero-card h4 {
  margin: 14px 0 10px;
  font-size: 22px;
  color: #143056;
}

.hero-card p {
  margin: 0;
  color: #6a7d99;
  line-height: 1.75;
}

.score-ring {
  display: grid;
  place-items: center;
  width: 102px;
  height: 102px;
  border-radius: 999px;
  color: #143056;
  background:
    radial-gradient(circle at center, rgba(255, 255, 255, 0.95) 42%, transparent 43%),
    conic-gradient(#7dd3fc 0deg, #7c9bf8 220deg, rgba(204, 219, 243, 0.6) 220deg);
}

.score-ring strong {
  font-size: 22px;
}

.score-ring span {
  font-size: 12px;
  color: #6a7d99;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.meta-card,
.section-card {
  padding: 18px;
  border-radius: 22px;
  border: 1px solid rgba(167, 186, 211, 0.24);
  background: rgba(255, 255, 255, 0.84);
}

.meta-card span {
  display: block;
  color: #6a7d99;
  font-size: 13px;
  margin-bottom: 8px;
}

.meta-card strong {
  color: #143056;
  font-size: 18px;
}

.section-head h5 {
  margin: 0;
  font-size: 18px;
  color: #143056;
}

.resource-list,
.path-list {
  display: grid;
  gap: 12px;
  margin: 14px 0 0;
  padding: 0;
  list-style: none;
}

.resource-list li,
.path-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 14px;
  border-radius: 16px;
  background: rgba(243, 247, 255, 0.92);
}

.resource-list strong,
.path-list strong {
  display: block;
  color: #18345d;
  margin-bottom: 4px;
}

.resource-list p,
.path-list span {
  margin: 0;
  color: #6a7d99;
  font-size: 13px;
}

.resource-list a {
  padding: 8px 12px;
  border-radius: 999px;
  color: #fff;
  background: linear-gradient(135deg, #5b8def, #4f46e5);
}

.message {
  padding: 14px 16px;
  border-radius: 16px;
  color: #607694;
  background: rgba(241, 246, 255, 0.92);
}

.message--error {
  color: #a34e4e;
  background: rgba(255, 232, 232, 0.92);
}

.skeleton {
  position: relative;
  overflow: hidden;
  border-radius: 18px;
  background: rgba(224, 233, 246, 0.7);
}

.skeleton::after {
  content: '';
  position: absolute;
  inset: 0;
  transform: translateX(-100%);
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.78), transparent);
  animation: shimmer 1.2s infinite;
}

.skeleton-title {
  height: 42px;
}

.skeleton-line {
  height: 18px;
}

.skeleton-card {
  height: 118px;
}

.drawer-fade-enter-active,
.drawer-fade-leave-active {
  transition: opacity 0.22s ease;
}

.drawer-fade-enter-active .drawer-panel,
.drawer-fade-leave-active .drawer-panel {
  transition: transform 0.22s ease;
}

.drawer-fade-enter-from,
.drawer-fade-leave-to {
  opacity: 0;
}

.drawer-fade-enter-from .drawer-panel,
.drawer-fade-leave-to .drawer-panel {
  transform: translateX(26px);
}

@keyframes shimmer {
  100% {
    transform: translateX(100%);
  }
}

@media (max-width: 640px) {
  .drawer-panel {
    padding: 18px;
  }

  .hero-card,
  .meta-grid {
    grid-template-columns: 1fr;
  }
}
</style>
