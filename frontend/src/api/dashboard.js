import request from '../utils/request'

export function fetchLearners() {
  return request.get('/learners/')
}

export function fetchLearningPaths() {
  return request.get('/learning-paths/')
}

export function fetchLearningRecords() {
  return request.get('/learning-records/')
}

export function fetchAssessmentResults() {
  return request.get('/assessment-results/')
}

export function fetchKnowledgePoints() {
  return request.get('/knowledge-points/')
}
