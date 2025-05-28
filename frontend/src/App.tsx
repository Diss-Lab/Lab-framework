/**
 * App.tsx
 * 使用日志管理组件
 * 功能：提供资源使用日志的录入和展示功能，包括设备和材料的使用记录
 */

import React, { useEffect, useState } from "react";
import axios from "axios";
import { Spin, Form, Select, Input, InputNumber, Checkbox, Button, Table, message, Space } from "antd";
import { UsageLog, ResourceType, ActionType } from "./types";

/**
 * 使用日志接口定义
 * @interface UsageLog
 * @property {number} id - 日志唯一标识
 * @property {number} user_id - 用户ID
 * @property {string} resource_type - 资源类型（equipment/material）
 * @property {number} resource_id - 资源ID
 * @property {string} action - 操作类型（start_use/end_use/consume/maintenance）
 * @property {number} quantity_used - 使用数量（可选）
 * @property {number} duration_minutes - 使用时长（分钟，可选）
 * @property {string} purpose - 使用目的（可选）
 * @property {string} notes - 备注信息（可选）
 * @property {string} issues_reported - 问题反馈（可选）
 * @property {string} project_name - 项目名称（可选）
 * @property {string} timestamp - 记录时间戳
 * @property {boolean} auto_recorded - 是否自动记录（可选）
 */
</edit>

<origin>
  const handleSubmit = async (values: any) => {
</origin>
<edit>
  const handleSubmit = async (values: Partial<UsageLog>) => {

// 常量定义
const API_BASE = "http://127.0.0.1:8000/api/logs/";
const RESOURCE_TYPES = {
  EQUIPMENT: "equipment",
  MATERIAL: "material"
} as const;

const ACTION_TYPES = {
  START_USE: "start_use",
  END_USE: "end_use",
  CONSUME: "consume",
  MAINTENANCE: "maintenance"
} as const;

const FORM_RULES = {
  resource_id: [{ required: true, message: "请输入资源ID" }],
  resource_type: [{ required: true, message: "请选择资源类型" }],
  action: [{ required: true, message: "请选择操作类型" }],
  quantity_used: [{ type: "number", min: 0, message: "数量必须大于0" }],
  duration_minutes: [{ type: "number", min: 0, message: "时长必须大于0" }]
};
/**
 * 使用日志管理主组件
 * @component App
 */
const App: React.FC = () => {
  const [form] = Form.useForm();
  const [logs, setLogs] = useState<UsageLog[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /** 用户认证token */
  const token = localStorage.getItem("access_token") || "";

  /**
   * token有效性检查
   * 副作用：当token不存在时设置错误信息
   */
  useEffect(() => {
    if (!token) {
      setError("未检测到登录信息，请先登录。");
    }
  }, [token]);

  /**
   * 获取日志列表
   * 副作用：组件加载时从API获取日志数据
   */
  useEffect(() => {
    if (!token) return;
    setLoading(true);
    axios
      .get(API_BASE, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setLogs(res.data);
        setError(null);
      })
      .catch((err) => {
        const errorMsg = err.response?.data?.detail || err.message;
        setError("获取日志失败: " + errorMsg);
        message.error("获取日志失败: " + errorMsg);
      })
      .finally(() => setLoading(false));
  }, [token]);

  /**
   * 处理表单提交
   * @param {React.FormEvent} e - 表单提交事件
   */
  const handleSubmit = async (values: any) => {
    if (!token) {
      message.error("未检测到登录信息，请先登录。");
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        API_BASE,
        values,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setLogs([response.data, ...logs]);
      form.resetFields();
      message.success("日志添加成功");
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || err.message;
      message.error("提交失败: " + errorMsg);
      setError("提交失败: " + errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Spin spinning={loading}>
      <div style={{ maxWidth: 900, margin: "40px auto", padding: 24, background: "#fff", borderRadius: 12, boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }}>
      <h2>📝 使用日志管理</h2>
      {/* 错误信息展示区域 */}
      {error && <div style={{ color: "red", marginBottom: 16 }}>{error}</div>}
      
      <Form
        form={form}
        onFinish={handleSubmit}
        layout="vertical"
        style={{ marginBottom: 32 }}
        initialValues={{
          resource_type: RESOURCE_TYPES.EQUIPMENT,
          action: ACTION_TYPES.START_USE,
          auto_recorded: false
        }}
      >
        <Form.Item name="resource_type" label="资源类型" rules={FORM_RULES.resource_type}>
          <Select>
            <Select.Option value={RESOURCE_TYPES.EQUIPMENT}>设备</Select.Option>
            <Select.Option value={RESOURCE_TYPES.MATERIAL}>材料</Select.Option>
          </Select>
        </Form.Item>
        
        {/* 资源ID输入框：必填字段 */}
        <Form.Item name="resource_id" label="资源ID" rules={FORM_RULES.resource_id}>
          <InputNumber min={1} style={{ width: '100%' }} />
        </Form.Item>
        
        {/* 操作类型选择：包含开始使用/结束使用/消耗/维护 */}
        <Form.Item name="action" label="操作类型" rules={FORM_RULES.action}>
          <Select>
            <Select.Option value={ACTION_TYPES.START_USE}>开始使用</Select.Option>
            <Select.Option value={ACTION_TYPES.END_USE}>结束使用</Select.Option>
            <Select.Option value={ACTION_TYPES.CONSUME}>消耗</Select.Option>
            <Select.Option value={ACTION_TYPES.MAINTENANCE}>维护</Select.Option>
          </Select>
        </Form.Item>
        
        {/* 数量输入框：用于记录使用或消耗的数量 */}
        <Form.Item name="quantity_used" label="数量" rules={FORM_RULES.quantity_used}>
          <InputNumber min={0} style={{ width: '100%' }} />
        </Form.Item>
        
        {/* 使用时长输入框：记录使用时间（分钟） */}
        <Form.Item name="duration_minutes" label="使用时长(分钟)" rules={FORM_RULES.duration_minutes}>
          <InputNumber min={0} style={{ width: '100%' }} />
        </Form.Item>
        
        {/* 使用目的输入框 */}
        <Form.Item name="purpose" label="目的">
          <Input />
        </Form.Item>
        
        {/* 备注信息输入框 */}
        <div>
          <label>备注：</label>
          <input value={form.notes} onChange={e => setForm(f => ({ ...f, notes: e.target.value }))} />
        </div>
        
        {/* 问题反馈输入框：记录使用过程中遇到的问题 */}
        <div>
          <label>问题反馈：</label>
          <input value={form.issues_reported} onChange={e => setForm(f => ({ ...f, issues_reported: e.target.value }))} />
        </div>
        
        {/* 项目名称输入框 */}
        <Form.Item name="project_name" label="项目名称">
          <Input />
        </Form.Item>
        
        {/* 自动记录复选框 */}
        <div>
          <label>
            <input type="checkbox" checked={form.auto_recorded} onChange={e => setForm(f => ({ ...f, auto_recorded: e.target.checked }))} />
            自动记录
          </label>
        </div>
        
        <Form.Item>
          <Space>
            <Button type="primary" htmlType="submit">
              添加日志
            </Button>
            <Button onClick={() => form.resetFields()}>
              重置
            </Button>
          </Space>
        </Form.Item>
      </Form>

      <h3>日志列表</h3>
      <Table
        dataSource={logs}
        rowKey="id"
        scroll={{ x: true }}
        columns={[
          { title: 'ID', dataIndex: 'id' },
          { title: '用户ID', dataIndex: 'user_id' },
          { title: '资源类型', dataIndex: 'resource_type' },
          { title: '资源ID', dataIndex: 'resource_id' },
          { title: '操作', dataIndex: 'action' },
          { title: '数量', dataIndex: 'quantity_used' },
          { title: '时长', dataIndex: 'duration_minutes' },
          { title: '目的', dataIndex: 'purpose' },
          { title: '备注', dataIndex: 'notes' },
          { title: '问题反馈', dataIndex: 'issues_reported' },
          { title: '项目', dataIndex: 'project_name' },
          { 
            title: '自动记录',
            dataIndex: 'auto_recorded',
            render: (value: boolean) => value ? '是' : '否'
          },
          { title: '时间', dataIndex: 'timestamp' }
        ]}
      />
        {/* 表格头部：定义所有列的标题 */}
        <thead>
          <tr>
            <th>ID</th>
            <th>用户ID</th>
            <th>资源类型</th>
            <th>资源ID</th>
            <th>操作</th>
            <th>数量</th>
            <th>时长</th>
            <th>目的</th>
            <th>备注</th>
            <th>问题反馈</th>
            <th>项目</th>
            <th>自动记录</th>
            <th>时间</th>
          </tr>
        </thead>
        {/* 表格主体：遍历日志数组并展示每条记录 */}
        <tbody>
          {logs.map(log => (
            <tr key={log.id}>
              <td>{log.id}</td>
              <td>{log.user_id}</td>
              <td>{log.resource_type}</td>
              <td>{log.resource_id}</td>
              <td>{log.action}</td>
              <td>{log.quantity_used ?? ""}</td>
              <td>{log.duration_minutes ?? ""}</td>
              <td>{log.purpose ?? ""}</td>
              <td>{log.notes ?? ""}</td>
              <td>{log.issues_reported ?? ""}</td>
              <td>{log.project_name ?? ""}</td>
              <td>{log.auto_recorded ? "是" : "否"}</td>
              <td>{log.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default App;