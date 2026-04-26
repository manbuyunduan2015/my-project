import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { login as loginApi, getUserInfo as fetchUserInfo } from '../../api/auth';
import { setToken, setUserInfo, clearAuth } from '../../utils/auth';

export const login = createAsyncThunk('auth/login', async ({ username, password }) => {
  const res = await loginApi(username, password);
  const { token } = res.data;
  setToken(token);
  const userRes = await fetchUserInfo();
  const user = userRes.data;
  setUserInfo(user);
  return { token, user };
});

export const fetchUser = createAsyncThunk('auth/fetchUser', async () => {
  const res = await fetchUserInfo();
  return res.data;
});

const authSlice = createSlice({
  name: 'auth',
  initialState: {
    token: null,
    user: null,
    isAuthenticated: false,
    loading: false,
  },
  reducers: {
    logout: (state) => {
      clearAuth();
      state.token = null;
      state.user = null;
      state.isAuthenticated = false;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => { state.loading = true; })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false;
        state.token = action.payload.token;
        state.user = action.payload.user;
        state.isAuthenticated = true;
      })
      .addCase(login.rejected, (state) => { state.loading = false; })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.user = action.payload;
        state.isAuthenticated = true;
      });
  },
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;
