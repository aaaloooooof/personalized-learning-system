<script setup>
import { computed, onMounted, reactive, ref } from 'vue'

import { getKnowledgeGraphData } from '../../api/graph'
import ConceptDrawer from './components/ConceptDrawer.vue'
import GraphCanvas from './components/GraphCanvas.vue'

const loading = ref(true)
const error = ref('')
const drawerVisible = ref(false)
const currentConceptId = ref('')
const sidebarCollapsed = ref(false)

const filters = reactive({
  mastered: true,
  learning: true,
  recommended: true,
})

const graphState = reactive({
  nodes: [],
  links: [],
})

const statusMetrics = computed(() => {
  const nodes = graphState.nodes

  return {
    mastered: nodes.filter((node) => Number(node.mastery_score || 0) >= 80).length,
    learning: nodes.filter((node) => {
      const score = Number(node.mastery_score || 0)
      return score >= 45 && score < 80
    }).length,
    recommended: nodes.filter((node) => Number(node.mastery_score || 0) < 45).length,
  }
})

const filteredGraphData = computed(() => {
  const allowNode = (node) => {
    const score = Number(node.mastery_score || 0)

    if (score >= 80) {
      return filters.mastered
    }

    if (score >= 45) {
      return filters.learning
    }

    return filters.recommended
  }

  const nodes = graphState.nodes.filter(allowNode)
  const visibleIds = new Set(nodes.map((node) => node.id))
  const links = graphState.links.filter(
    (link) => visibleIds.has(link.source) && visibleIds.has(link.target),
  )

  return {
    nodes,
    links,
  }
})

async function loadGraphData() {
  loading.value = true
  error.value = ''

  try {
    const graph = await getKnowledgeGraphData()
    graphState.nodes = graph.nodes
    graphState.links = graph.links
  } catch (requestError) {
    error.value = requestError.message || '知识图谱加载失败，请稍后重试。'
  } finally {
    loading.value = false
  }
}

function handleNodeClick(nodeId) {
  currentConceptId.value = nodeId
  drawerVisible.value = true
}

onMounted(async () => {
  await loadGraphData()
})
</script>

<template>
  <section class="graph-page">
    <header class="page-hero">
      <div>
        <p class="hero-kicker">Knowledge Graph</p>
        <h1>个性化学习知识图谱</h1>
        <p class="hero-copy">
          以学习路径、知识依赖和掌握程度为中心，构建一个可探索、可聚焦、可用于推荐的知识网络。
        </p>
      </div>
      <div class="hero-meta">
        <div class="hero-badge">
          <strong>{{ graphState.nodes.length }}</strong>
          <span>知识节点</span>
        </div>
        <div class="hero-badge">
          <strong>{{ graphState.links.length }}</strong>
          <span>依赖连接</span>
        </div>
      </div>
    </header>

    <div class="graph-layout">
      <aside class="control-rail" :class="{ 'control-rail--collapsed': sidebarCollapsed }">
        <button class="rail-button rail-button--wide" type="button" @click="sidebarCollapsed = !sidebarCollapsed">
          {{ sidebarCollapsed ? '展开面板' : '收起面板' }}
        </button>
        <button class="rail-button rail-button--soft" type="button" @click="loadGraphData">
          刷新图谱
        </button>

        <transition name="fade-slide">
          <div v-if="!sidebarCollapsed" class="rail-sections">
            <section class="rail-card">
              <h3>筛选条件</h3>
              <label class="checkbox-item">
                <input v-model="filters.mastered" type="checkbox" />
                <span>已掌握知识点</span>
                <strong>{{ statusMetrics.mastered }}</strong>
              </label>
              <label class="checkbox-item">
                <input v-model="filters.learning" type="checkbox" />
                <span>待学习知识点</span>
                <strong>{{ statusMetrics.learning }}</strong>
              </label>
              <label class="checkbox-item">
                <input v-model="filters.recommended" type="checkbox" />
                <span>重点推荐</span>
                <strong>{{ statusMetrics.recommended }}</strong>
              </label>
            </section>

            <section class="rail-card rail-card--soft">
              <h3>图谱提示</h3>
              <ul class="tips-list">
                <li>节点颜色越亮，掌握度越高。</li>
                <li>点击节点可查看资源、路径与前置知识。</li>
                <li>拖拽与缩放用于查看局部结构。</li>
              </ul>
            </section>
          </div>
        </transition>
      </aside>

      <main class="canvas-stage">
        <div v-if="loading" class="stage-state stage-state--loading">
          正在加载知识图谱，请稍候…
        </div>
        <div v-else-if="error" class="stage-state stage-state--error">
          {{ error }}
        </div>
        <GraphCanvas
          v-else
          :graph-data="filteredGraphData"
          @node-click="handleNodeClick"
        />
      </main>
    </div>

    <ConceptDrawer
      :concept-id="currentConceptId"
      :visible="drawerVisible"
      @close="drawerVisible = false"
    />
  </section>
</template>

<style scoped>
.graph-page {
  display: grid;
  gap: 24px;
}

.page-hero {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
  padding: 28px 30px;
  border: 1px solid rgba(168, 188, 214, 0.34);
  border-radius: 30px;
  background:
    radial-gradient(circle at top left, rgba(125, 211, 252, 0.18), transparent 30%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.86), rgba(241, 247, 255, 0.92));
  box-shadow:
    0 24px 64px rgba(29, 59, 115, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.78);
  backdrop-filter: blur(16px);
}

.hero-kicker {
  margin: 0 0 10px;
  color: #6480a8;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.page-hero h1 {
  margin: 0;
  font-size: clamp(2.2rem, 4.4vw, 3.5rem);
  line-height: 1.06;
  color: #10294d;
}

.hero-copy {
  max-width: 760px;
  margin: 12px 0 0;
  color: #667a97;
  line-height: 1.8;
}

.hero-meta {
  display: flex;
  gap: 12px;
}

.hero-badge {
  min-width: 112px;
  padding: 18px 16px;
  border-radius: 22px;
  text-align: center;
  background: rgba(247, 250, 255, 0.88);
  border: 1px solid rgba(168, 188, 214, 0.26);
}

.hero-badge strong {
  display: block;
  font-size: 28px;
  color: #143056;
}

.hero-badge span {
  color: #7084a1;
  font-size: 13px;
}

.graph-layout {
  display: grid;
  grid-template-columns: 240px minmax(0, 1fr);
  gap: 22px;
  align-items: start;
}

.control-rail {
  position: sticky;
  top: 24px;
  display: grid;
  gap: 16px;
}

.control-rail--collapsed {
  grid-template-columns: 1fr;
}

.rail-button {
  width: 100%;
  padding: 16px 18px;
  border: 1px solid rgba(115, 143, 185, 0.36);
  border-radius: 20px;
  color: #16315a;
  font-size: 18px;
  font-weight: 700;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(237, 243, 253, 0.88));
  box-shadow: 0 12px 30px rgba(24, 52, 93, 0.06);
  cursor: pointer;
}

.rail-button--soft {
  color: #35537a;
  font-size: 16px;
}

.rail-sections {
  display: grid;
  gap: 16px;
}

.rail-card {
  padding: 18px;
  border: 1px solid rgba(168, 188, 214, 0.3);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.78);
  box-shadow: 0 18px 38px rgba(18, 41, 80, 0.05);
  backdrop-filter: blur(12px);
}

.rail-card--soft {
  background: rgba(245, 249, 255, 0.92);
}

.rail-card h3 {
  margin: 0 0 14px;
  font-size: 18px;
  color: #18345d;
}

.checkbox-item {
  display: grid;
  grid-template-columns: 18px minmax(0, 1fr) auto;
  align-items: center;
  gap: 10px;
  padding: 12px 0;
  color: #2c4467;
  cursor: pointer;
}

.checkbox-item + .checkbox-item {
  border-top: 1px solid rgba(168, 188, 214, 0.18);
}

.checkbox-item input {
  width: 18px;
  height: 18px;
  accent-color: #598cf0;
}

.checkbox-item strong {
  color: #6d84a6;
  font-size: 13px;
}

.tips-list {
  margin: 0;
  padding-left: 18px;
  color: #6a7d99;
  line-height: 1.8;
}

.canvas-stage {
  min-width: 0;
}

.stage-state {
  display: grid;
  place-items: center;
  min-height: 720px;
  padding: 24px;
  border-radius: 32px;
  border: 1px solid rgba(168, 188, 214, 0.3);
  background: rgba(255, 255, 255, 0.82);
  color: #35537a;
  font-size: 18px;
  box-shadow: 0 22px 54px rgba(18, 41, 80, 0.06);
}

.stage-state--loading {
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.86), rgba(240, 246, 255, 0.92));
}

.stage-state--error {
  color: #aa5151;
  background:
    linear-gradient(180deg, rgba(255, 247, 247, 0.92), rgba(255, 237, 237, 0.96));
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.18s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

@media (max-width: 1120px) {
  .page-hero,
  .graph-layout {
    grid-template-columns: 1fr;
  }

  .page-hero {
    flex-direction: column;
  }

  .hero-meta {
    width: 100%;
  }

  .hero-badge {
    flex: 1;
  }

  .control-rail {
    position: static;
  }
}

@media (max-width: 640px) {
  .page-hero {
    padding: 22px;
  }

  .hero-meta {
    flex-direction: column;
  }

  .stage-state {
    min-height: 520px;
  }
}
</style>
