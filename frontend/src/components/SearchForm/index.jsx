import React from 'react';
import { Form, Input, Button, Space } from 'antd';

const SearchForm = ({ onSearch, onReset, children }) => {
  const [form] = Form.useForm();

  const handleSearch = (values) => {
    onSearch(values);
  };

  const handleReset = () => {
    form.resetFields();
    onReset && onReset();
  };

  return (
    <Form form={form} layout="inline" onFinish={handleSearch} style={{ marginBottom: 16 }}>
      {children}
      <Form.Item>
        <Space>
          <Button type="primary" htmlType="submit">查询</Button>
          <Button onClick={handleReset}>重置</Button>
        </Space>
      </Form.Item>
    </Form>
  );
};

export default SearchForm;
