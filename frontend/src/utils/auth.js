const TOKEN_KEY = 'access_token';
const USER_KEY = 'user_info';

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function removeToken() {
  localStorage.removeItem(TOKEN_KEY);
}

export function getUserInfo() {
  const data = localStorage.getItem(USER_KEY);
  return data ? JSON.parse(data) : null;
}

export function setUserInfo(info) {
  localStorage.setItem(USER_KEY, JSON.stringify(info));
}

export function removeUserInfo() {
  localStorage.removeItem(USER_KEY);
}

export function clearAuth() {
  removeToken();
  removeUserInfo();
}
