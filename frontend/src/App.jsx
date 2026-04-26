import React from 'react';
import { RouterProvider } from 'react-router-dom';
import { Provider } from 'react-redux';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import store from './store';
import routes from './router/routes.jsx';

const App = () => (
  <Provider store={store}>
    <ConfigProvider locale={zhCN}>
      <RouterProvider router={routes} />
    </ConfigProvider>
  </Provider>
);

export default App;
