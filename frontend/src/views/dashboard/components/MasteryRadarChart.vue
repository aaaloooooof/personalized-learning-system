<script setup>
import { computed } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => [],
  },
})

const size = 320
const center = size / 2
const levels = 4
const radius = 112

const normalizedItems = computed(() => {
  const fallback = [
    { label: '学习投入', value: 0 },
    { label: '内容完成', value: 0 },
    { label: '路径覆盖', value: 0 },
    { label: '测评表现', value: 0 },
    { label: '知识广度', value: 0 },
  ]

  return props.items.length ? props.items : fallback
})

const axisPoints = computed(() =>
  normalizedItems.value.map((item, index, array) => {
    const angle = ((Math.PI * 2) / array.length) * index - Math.PI / 2

    return {
      ...item,
      x: center + Math.cos(angle) * radius,
      y: center + Math.sin(angle) * radius,
      labelX: center + Math.cos(angle) * (radius + 26),
      labelY: center + Math.sin(angle) * (radius + 26),
      angle,
    }
  }),
)

const polygonLayers = computed(() =>
  Array.from({ length: levels }, (_, index) => {
    const factor = (index + 1) / levels

    return axisPoints.value
      .map((point) => {
        const x = center + Math.cos(point.angle) * radius * factor
        const y = center + Math.sin(point.angle) * radius * factor
        return `${x},${y}`
      })
      .join(' ')
  }),
)

const dataPolygon = computed(() =>
  axisPoints.value
    .map((point) => {
      const factor = Math.max(0, Math.min(100, Number(point.value) || 0)) / 100
      const x = center + Math.cos(point.angle) * radius * factor
      const y = center + Math.sin(point.angle) * radius * factor
      return `${x},${y}`
    })
    .join(' '),
)
</script>

<template>
  <section class="panel">
    <div class="panel-head">
      <div>
        <h3>能力素养雷达</h3>
        <p>基于学习记录、测评结果与路径覆盖的综合快照。</p>
      </div>
    </div>

    <div class="radar-shell">
      <svg :viewBox="`0 0 ${size} ${size}`" class="radar-svg" role="img" aria-label="能力素养雷达图">
        <polygon
          v-for="layer in polygonLayers"
          :key="layer"
          :points="layer"
          class="grid-layer"
        />

        <line
          v-for="point in axisPoints"
          :key="`${point.label}-axis`"
          :x1="center"
          :y1="center"
          :x2="point.x"
          :y2="point.y"
          class="axis-line"
        />

        <polygon :points="dataPolygon" class="data-area" />

        <circle
          v-for="point in axisPoints"
          :key="point.label"
          :cx="center + Math.cos(point.angle) * radius * ((Number(point.value) || 0) / 100)"
          :cy="center + Math.sin(point.angle) * radius * ((Number(point.value) || 0) / 100)"
          r="5"
          class="data-dot"
        />

        <text
          v-for="point in axisPoints"
          :key="`${point.label}-text`"
          :x="point.labelX"
          :y="point.labelY"
          class="axis-label"
          text-anchor="middle"
        >
          {{ point.label }}
        </text>
      </svg>
    </div>

    <ul class="legend">
      <li v-for="item in normalizedItems" :key="item.label">
        <span>{{ item.label }}</span>
        <strong>{{ Math.round(item.value) }}</strong>
      </li>
    </ul>
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

.radar-shell {
  display: flex;
  justify-content: center;
  padding: 18px 0 6px;
}

.radar-svg {
  width: min(100%, 320px);
  height: auto;
}

.grid-layer {
  fill: rgba(191, 219, 254, 0.14);
  stroke: rgba(148, 163, 184, 0.35);
  stroke-width: 1;
}

.axis-line {
  stroke: rgba(148, 163, 184, 0.4);
  stroke-width: 1;
}

.data-area {
  fill: rgba(37, 99, 235, 0.28);
  stroke: #2563eb;
  stroke-width: 2.5;
}

.data-dot {
  fill: #0f766e;
}

.axis-label {
  fill: #334155;
  font-size: 12px;
  font-weight: 600;
}

.legend {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin: 12px 0 0;
  padding: 0;
  list-style: none;
}

.legend li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  border-radius: 16px;
  background: rgba(248, 250, 252, 0.92);
}

.legend span {
  color: #64748b;
  font-size: 14px;
}

.legend strong {
  font-size: 18px;
  color: #0f172a;
}

@media (max-width: 640px) {
  .legend {
    grid-template-columns: 1fr;
  }
}
</style>
