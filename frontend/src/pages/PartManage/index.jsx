import React, { useEffect, useState } from 'react';
import { Card, Table, Button, Input, Modal, Form, Popconfirm, message, Space, Tag, InputNumber, Select } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { useSelector } from 'react-redux';
import { getPartsApi, createPartApi, updatePartApi, deletePartApi } from '../../api/part';
import { ROLE_ADMIN } from '../../utils/constants';

const PART_CATEGORIES = ['传动系统', '冷却系统', '制动系统', '悬挂系统', '点火系统', '照明系统', '电气系统', '行走系统', '过滤系统', '附件'];
const PART_SUPPLIERS = ['Bosch', 'GMB', 'Gates', 'Hella', 'KYB', 'Mahle', 'Mann', 'Michelin', 'NGK', 'Varta'];

const PartManage = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [modalOpen, setModalOpen] = useState(false);
  const [editId, setEditId] = useState(null);
  const [form] = Form.useForm();
  const { user } = useSelector((state) => state.auth);
  const isAdmin = user?.roles?.includes(ROLE_ADMIN);

  const fetchData = async (searchParams = {}) => {
    setLoading(true);
    try {
      const params = { page, page_size: pageSize, ...searchParams };
      const res = await getPartsApi(params);
      setData(res.data?.items || []);
      setTotal(res.data?.total || 0);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, [page, pageSize]);

  const handleSearch = (values) => { setPage(1); fetchData({ ...values, page: 1, page_size: pageSize }); };
  const handleReset = () => fetchData();

  const handleOpenModal = (record) => {
    setEditId(record?.id || null);
    if (record) {
      form.setFieldsValue(record);
    } else {
      form.resetFields();
    }
    setModalOpen(true);
  };

  const handleSubmit = async () => {
    const values = await form.validateFields();
    try {
      if (editId) {
        await updatePartApi(editId, values);
        message.success('更新成功');
      } else {
        await createPartApi(values);
        message.success('新增成功');
      }
      setModalOpen(false);
      fetchData();
    } catch (err) {
      message.error(err.message || '操作失败');
    }
  };

  const handleDelete = async (id) => {
    try {
      await deletePartApi(id);
      message.success('删除成功');
      fetchData();
    } catch (err) {
      message.error(err.message || '删除失败');
    }
  };

  const columns = [
    { title: '零件编号', dataIndex: 'part_code' },
    { title: '零件名称', dataIndex: 'part_name' },
    { title: '分类', dataIndex: 'category' },
    { title: '供应商', dataIndex: 'supplier' },
    { title: '单价', dataIndex: 'price', render: (v) => `¥${v}` },
    { title: '库存', dataIndex: 'stock_qty' },
    { title: '安全库存', dataIndex: 'safe_stock' },
    {
      title: '预警',
      dataIndex: 'low_stock',
      render: (low) => low ? <Tag color="red">库存不足</Tag> : <Tag color="green">正常</Tag>,
    },
    ...(isAdmin ? [{
      title: '操作',
      render: (_, record) => (
        <Space>
          <Button size="small" icon={<EditOutlined />} onClick={() => handleOpenModal(record)}>编辑</Button>
          <Popconfirm title="确定删除？" onConfirm={() => handleDelete(record.id)}>
            <Button size="small" danger icon={<DeleteOutlined />}>删除</Button>
          </Popconfirm>
        </Space>
      ),
    }] : []),
  ];

  return (
    <div style={{ padding: 24 }}>
      <Card title="零部件管理" extra={isAdmin && <Button type="primary" icon={<PlusOutlined />} onClick={() => handleOpenModal(null)}>新增零件</Button>}>
        <Form layout="inline" onFinish={handleSearch} style={{ marginBottom: 16 }}>
          <Form.Item name="part_code" label="零件编号"><Input placeholder="请输入编号" /></Form.Item>
          <Form.Item name="part_name" label="零件名称"><Input placeholder="请输入名称" /></Form.Item>
          <Form.Item name="category" label="分类">
            <Select allowClear placeholder="请选择分类" style={{ width: 150 }} options={PART_CATEGORIES.map(c => ({ label: c, value: c }))} />
          </Form.Item>
          <Form.Item name="supplier" label="供应商">
            <Select allowClear placeholder="请选择供应商" style={{ width: 150 }} options={PART_SUPPLIERS.map(s => ({ label: s, value: s }))} />
          </Form.Item>
          <Form.Item>
            <Space><Button type="primary" htmlType="submit">查询</Button><Button onClick={handleReset}>重置</Button></Space>
          </Form.Item>
        </Form>
        <Table
          columns={columns} dataSource={data} loading={loading} rowKey="id"
          pagination={{ current: page, pageSize, total, onChange: (p, ps) => { setPage(p); setPageSize(ps); } }}
        />
      </Card>
      <Modal title={editId ? '编辑零件' : '新增零件'} open={modalOpen} onOk={handleSubmit} onCancel={() => setModalOpen(false)} width={700}>
        <Form form={form} layout="vertical">
          <Form.Item name="part_code" label="零件编号" rules={[{ required: true }]}><Input disabled={!!editId} /></Form.Item>
          <Form.Item name="part_name" label="零件名称" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="category" label="分类">
            <Select allowClear placeholder="请选择分类" options={PART_CATEGORIES.map(c => ({ label: c, value: c }))} />
          </Form.Item>
          <Form.Item name="spec_model" label="规格型号"><Input /></Form.Item>
          <Form.Item name="material" label="材质"><Input /></Form.Item>
          <Form.Item name="supplier" label="供应商">
            <Select allowClear placeholder="请选择供应商" options={PART_SUPPLIERS.map(s => ({ label: s, value: s }))} />
          </Form.Item>
          <Form.Item name="unit" label="单位"><Input /></Form.Item>
          <Form.Item name="price" label="单价" rules={[{ required: true }]}><InputNumber min={0} precision={2} style={{ width: '100%' }} /></Form.Item>
          <Form.Item name="stock_qty" label="库存数量" rules={[{ required: true }]}><InputNumber min={0} style={{ width: '100%' }} /></Form.Item>
          <Form.Item name="safe_stock" label="安全库存" rules={[{ required: true }]}><InputNumber min={0} style={{ width: '100%' }} /></Form.Item>
          <Form.Item name="description" label="描述"><Input.TextArea rows={2} /></Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default PartManage;
