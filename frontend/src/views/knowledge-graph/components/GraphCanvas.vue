<script setup>
import { computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { GraphChart } from 'echarts/charts'
import { LegendComponent, TooltipComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, GraphChart, TooltipComponent, LegendComponent])

const props = defineProps({
  graphData: {
    type: Object,
    default: () => ({
      nodes: [],
      links: [],
    }),
  },
})

const emit = defineEmits(['node-click'])

const themeColors = {
  canvas: '#f8fbff',
  line: 'rgba(78, 114, 164, 0.28)',
  lineActive: 'rgba(45, 92, 163, 0.55)',
  high: '#7dd3fc',
  medium: '#7c9bf8',
  low: '#f59e7b',
  border: '#ffffff',
  text: '#143056',
  glow: 'rgba(125, 211, 252, 0.18)',
}

function getMasteryColor(score) {
  if (score >= 80) {
    return themeColors.high
  }

  if (score >= 45) {
    return themeColors.medium
  }

  return themeColors.low
}

const chartOption = computed(() => {
  const nodes = props.graphData.nodes.map((node) => {
    const mastery = Number(node.mastery_score || 0)

    return {
      ...node,
      symbolSize: Math.max(38, Math.min(82, 34 + mastery * 0.34)),
      draggable: true,
      value: mastery,
      itemStyle: {
        color: getMasteryColor(mastery),
        borderColor: themeColors.border,
        borderWidth: 2,
        shadowBlur: 18,
        shadowColor: themeColors.glow,
      },
      label: {
        show: true,
        color: themeColors.text,
        fontSize: 14,
        fontWeight: 600,
      },
      emphasis: {
        scale: 1.12,
        itemStyle: {
          shadowBlur: 30,
          shadowColor: 'rgba(57, 127, 255, 0.24)',
        },
      },
    }
  })

  const links = props.graphData.links.map((link) => ({
    ...link,
    lineStyle: {
      color: themeColors.line,
      width: 2,
      curveness: 0.16,
    },
  }))

  return {
    backgroundColor: 'transparent',
    animationDuration: 700,
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(14, 25, 48, 0.92)',
      borderWidth: 0,
      textStyle: {
        color: '#f8fafc',
      },
      formatter(params) {
        if (params.dataType === 'edge') {
          return `${params.data.source} -> ${params.data.target}`
        }

        return `
          <div style="min-width: 180px;">
            <div style="font-size: 14px; font-weight: 700; margin-bottom: 6px;">${params.data.name}</div>
            <div>掌握度：${Math.round(params.data.mastery_score || 0)}%</div>
            <div>状态：${params.data.status || 'unknown'}</div>
          </div>
        `
      },
    },
    legend: {
      bottom: 12,
      left: 'center',
      itemWidth: 12,
      itemHeight: 12,
      textStyle: {
        color: '#5b6b84',
      },
      data: ['已掌握', '学习中', '待强化'],
    },
    series: [
      {
        name: '知识图谱',
        type: 'graph',
        layout: 'force',
        roam: true,
        draggable: true,
        focusNodeAdjacency: true,
        data: nodes,
        links,
        categories: [
          { name: '已掌握' },
          { name: '学习中' },
          { name: '待强化' },
        ],
        force: {
          repulsion: 300,
          gravity: 0.08,
          edgeLength: [90, 170],
          friction: 0.12,
        },
        lineStyle: {
          color: themeColors.line,
          opacity: 0.92,
        },
        emphasis: {
          lineStyle: {
            color: themeColors.lineActive,
            width: 3,
          },
        },
      },
    ],
  }
})

function handleChartClick(params) {
  if (params?.dataType === 'node' && params?.data?.id) {
    emit('node-click', params.data.id)
  }
}
</script>

<template>
  <div class="graph-shell">
    <div class="graph-header">
      <div>
        <h3>图谱画布</h3>
        <p>拖拽节点、滚轮缩放，点击任一知识点查看详情。</p>
      </div>
      <div class="legend-pills">
        <span class="pill pill--high">高掌握</span>
        <span class="pill pill--mid">学习中</span>
        <span class="pill pill--low">待强化</span>
      </div>
    </div>

    <v-chart
      class="graph-chart"
      :option="chartOption"
      autoresize
      @click="handleChartClick"
    />
  </div>
</template>

<style scoped>
.graph-shell {
  height: 100%;
  min-height: 720px;
  padding: 20px;
  border: 1px solid rgba(167, 186, 211, 0.34);
  border-radius: 32px;
  background:
    radial-gradient(circle at top, rgba(255, 255, 255, 0.88), rgba(241, 246, 255, 0.92)),
    linear-gradient(180deg, rgba(245, 249, 255, 0.92), rgba(236, 244, 255, 0.94));
  box-shadow:
    0 24px 64px rgba(29, 59, 115, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(16px);
}

.graph-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;
}

.graph-header h3 {
  margin: 0;
  font-size: 22px;
  color: #16315a;
}

.graph-header p {
  margin: 8px 0 0;
  color: #6c7d96;
}

.legend-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.pill {
  padding: 8px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
}

.pill--high {
  color: #0f4f6a;
  background: rgba(125, 211, 252, 0.24);
}

.pill--mid {
  color: #2d4cb0;
  background: rgba(124, 155, 248, 0.2);
}

.pill--low {
  color: #9a4d34;
  background: rgba(245, 158, 123, 0.2);
}

.graph-chart {
  width: 100%;
  height: calc(100% - 76px);
  min-height: 620px;
  border-radius: 24px;
  background:
    radial-gradient(circle at center, rgba(255, 255, 255, 0.75), rgba(244, 248, 255, 0.4));
}

@media (max-width: 960px) {
  .graph-shell {
    min-height: 600px;
  }

  .graph-header {
    flex-direction: column;
  }

  .graph-chart {
    min-height: 520px;
  }
}
</style>
