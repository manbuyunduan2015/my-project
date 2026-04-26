import request from './request';

export function login(username, password) {
  return request.post('/api/auth/login', { username, password });
}

export function getUserInfo() {
  return request.get('/api/auth/userinfo');
}

export function changePassword(oldPassword, newPassword) {
  return request.put('/api/auth/change-password', { old_password: oldPassword, new_password: newPassword });
}
