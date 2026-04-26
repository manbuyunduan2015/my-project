import React, { useEffect, useState } from 'react';
import { Card, Table } from 'antd';
import { getRolesApi } from '../../api/role';

const RoleManage = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([]);

  useEffect(() => {
    setLoading(true);
    getRolesApi().then((res) => setData(res.data || [])).finally(() => setLoading(false));
  }, []);

  const columns = [
    { title: '角色名称', dataIndex: 'role_name' },
    { title: '角色描述', dataIndex: 'role_desc' },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Card title="角色管理">
        <Table columns={columns} dataSource={data} loading={loading} rowKey="id" pagination={false} />
      </Card>
    </div>
  );
};

export default RoleManage;
