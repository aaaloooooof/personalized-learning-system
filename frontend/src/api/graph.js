import request from '../utils/request'

function normalizeList(payload) {
  if (Array.isArray(payload)) {
    return payload
  }

  if (Array.isArray(payload?.results)) {
    return payload.results
  }

  return []
}

export async function getKnowledgeGraphData(params = {}) {
  const payload = await request.get('/knowledge-points/', { params })
  const points = normalizeList(payload)

  // 后端知识点列表需要映射为图谱所需的 nodes / links 结构：
  // 1. nodes 中的 mastery_score 优先读取后端返回的 mastery_score，
  //    若当前接口尚未提供，则回退使用 weight * 100 近似映射。
  // 2. links 中的依赖关系优先读取 parent_concept_id，
  //    若当前接口尚未提供，则回退使用 prerequisite 字段表示父知识点。
  const nodes = points.map((point) => ({
    id: point.id,
    name: point.name,
    description: point.description,
    mastery_score:
      typeof point.mastery_score === 'number'
        ? point.mastery_score
        : Math.round(Number(point.weight || 0) * 100),
    status: point.status,
    weight: point.weight,
    category:
      typeof point.mastery_score === 'number'
        ? point.mastery_score >= 80
          ? 'mastered'
          : point.mastery_score >= 45
            ? 'learning'
            : 'recommended'
        : point.status || 'learning',
    parent_concept_id: point.parent_concept_id || point.prerequisite || null,
  }))

  const links = nodes
    .filter((node) => node.parent_concept_id)
    .map((node) => ({
      source: node.parent_concept_id,
      target: node.id,
      value: 'depends-on',
      parent_concept_id: node.parent_concept_id,
    }))

  return {
    nodes,
    links,
    raw: points,
  }
}

export async function getConceptDetails(conceptId) {
  const [concept, learningContents, pathNodes] = await Promise.all([
    request.get(`/knowledge-points/${conceptId}/`),
    request.get('/learning-contents/', {
      params: { knowledge_point: conceptId },
    }),
    request.get('/path-nodes/', {
      params: { knowledge_point: conceptId },
    }),
  ])

  return {
    concept,
    relatedContents: normalizeList(learningContents),
    relatedPaths: normalizeList(pathNodes),
  }
}
