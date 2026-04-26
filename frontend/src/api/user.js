import request from './request';

export function getUsersApi(params) {
  return request.get('/api/users', { params });
}

export function createUserApi(data) {
  return request.post('/api/users', data);
}

export function updateUserApi(id, data) {
  return request.put(`/api/users/${id}`, data);
}

export function deleteUserApi(id) {
  return request.delete(`/api/users/${id}`);
}

export function updateUserStatusApi(id, status) {
  return request.put(`/api/users/${id}/status`, { status });
}
