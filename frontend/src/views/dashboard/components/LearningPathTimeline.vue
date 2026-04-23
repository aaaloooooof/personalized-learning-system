<script setup>
const props = defineProps({
  items: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <section class="panel">
    <div class="panel-head">
      <div>
        <h3>学习路径时间轴</h3>
        <p>展示当前可见学习路径及其节点分布，帮助学习者把握推进节奏。</p>
      </div>
    </div>

    <div v-if="items.length" class="timeline">
      <article v-for="path in items" :key="path.id" class="timeline-item">
        <div class="timeline-dot" />
        <div class="timeline-content">
          <div class="timeline-top">
            <h4>{{ path.name }}</h4>
            <span class="status">{{ path.status || 'unknown' }}</span>
          </div>
          <p>{{ path.description || '该学习路径暂未配置说明。' }}</p>
          <ul class="nodes">
            <li v-for="node in path.path_nodes || []" :key="node.id">
              <strong>Step {{ node.sort_order }}</strong>
              <span>{{ node.knowledge_point_name }}</span>
            </li>
          </ul>
        </div>
      </article>
    </div>

    <div v-else class="empty-state">
      暂无学习路径数据，后端接入完成后这里会自动渲染时间轴。
    </div>
  </section>
</template>

<style scoped>
.panel {
  padding: 24px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(148, 163, 184, 0.22);
  box-shadow: 0 16px 40px rgba(15, 23, 42, 0.05);
}

.panel-head h3 {
  margin: 0;
  font-size: 20px;
}

.panel-head p {
  margin: 8px 0 0;
  color: #64748b;
}

.timeline {
  position: relative;
  margin-top: 20px;
  display: grid;
  gap: 18px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 11px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(180deg, rgba(37, 99, 235, 0.4), rgba(15, 118, 110, 0.18));
}

.timeline-item {
  position: relative;
  display: grid;
  grid-template-columns: 24px minmax(0, 1fr);
  gap: 16px;
}

.timeline-dot {
  position: relative;
  z-index: 1;
  width: 24px;
  height: 24px;
  margin-top: 10px;
  border-radius: 999px;
  background: linear-gradient(135deg, #2563eb, #0f766e);
  box-shadow: 0 0 0 6px rgba(219, 234, 254, 0.9);
}

.timeline-content {
  padding: 18px;
  border-radius: 22px;
  background: rgba(248, 250, 252, 0.92);
}

.timeline-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.timeline-top h4 {
  margin: 0;
  font-size: 18px;
}

.status {
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 12px;
  text-transform: capitalize;
  color: #2563eb;
  background: rgba(219, 234, 254, 0.9);
}

.timeline-content p {
  margin: 10px 0 0;
  color: #64748b;
  line-height: 1.7;
}

.nodes {
  display: grid;
  gap: 10px;
  margin: 16px 0 0;
  padding: 0;
  list-style: none;
}

.nodes li {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  padding: 10px 12px;
  border-radius: 14px;
  background: #fff;
}

.nodes strong {
  color: #0f172a;
  font-size: 13px;
}

.nodes span {
  color: #475569;
  font-size: 14px;
}

.empty-state {
  margin-top: 18px;
  padding: 20px;
  border-radius: 18px;
  color: #64748b;
  background: rgba(248, 250, 252, 0.92);
}
</style>
