import React, { useEffect, useState } from 'react';
import { Card, Col, Row, Statistic, Table, Spin } from 'antd';
import { TeamOutlined, CarOutlined, ToolOutlined, WarningOutlined } from '@ant-design/icons';
import ReactECharts from 'echarts-for-react';
import { getStatistics } from '../../api/dashboard';

const Dashboard = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  useEffect(() => {
    setLoading(true);
    getStatistics()
      .then((res) => setData(res.data))
      .finally(() => setLoading(false));
  }, []);

  if (loading || !data) {
    return <div style={{ textAlign: 'center', padding: 100 }}><Spin size="large" /></div>;
  }

  const statCards = [
    { title: '整车数量', value: data.vehicle_count, icon: <CarOutlined />, color: '#1890ff' },
    { title: '零部件数量', value: data.part_count, icon: <ToolOutlined />, color: '#52c41a' },
    { title: '用户数量', value: data.user_count, icon: <TeamOutlined />, color: '#722ed1' },
    { title: '库存预警', value: data.low_stock_count, icon: <WarningOutlined />, color: '#faad14' },
  ];

  const categoryOption = {
    title: { text: '零部件分类统计', left: 'center' },
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      data: data.category_stats.map((item) => ({ name: item.category, value: item.count })),
      label: { show: true, formatter: '{b}: {c}' },
    }],
  };

  const lowStockColumns = [
    { title: '零件编号', dataIndex: 'part_code' },
    { title: '零件名称', dataIndex: 'part_name' },
    { title: '当前库存', dataIndex: 'stock_qty' },
    { title: '安全库存', dataIndex: 'safe_stock' },
  ];

  const vehicleColumns = [
    { title: '整车编号', dataIndex: 'vehicle_code' },
    { title: '整车名称', dataIndex: 'vehicle_name' },
    { title: '品牌', dataIndex: 'brand' },
  ];

  const partColumns = [
    { title: '零件编号', dataIndex: 'part_code' },
    { title: '零件名称', dataIndex: 'part_name' },
    { title: '分类', dataIndex: 'category' },
  ];

  return (
    <div style={{ padding: 24 }}>
      <h2 style={{ marginBottom: 24 }}>仪表盘</h2>
      <Row gutter={[16, 16]}>
        {statCards.map((item, i) => (
          <Col span={6} key={i}>
            <Card>
              <Statistic
                title={item.title}
                value={item.value}
                prefix={<span style={{ color: item.color, fontSize: 28 }}>{item.icon}</span>}
              />
            </Card>
          </Col>
        ))}
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
        <Col span={12}>
          <Card title="零部件分类分布">
            <ReactECharts option={categoryOption} style={{ height: 300 }} />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="库存预警 TOP 10">
            <Table
              columns={lowStockColumns}
              dataSource={data.low_stock_parts}
              rowKey="part_code"
              pagination={false}
              size="small"
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
        <Col span={12}>
          <Card title="最近新增整车">
            <Table
              columns={vehicleColumns}
              dataSource={data.recent_vehicles}
              rowKey="id"
              pagination={false}
              size="small"
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="最近新增零部件">
            <Table
              columns={partColumns}
              dataSource={data.recent_parts}
              rowKey="id"
              pagination={false}
              size="small"
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
