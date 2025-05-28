/**
 * 类型定义文件
 */

/** 资源类型 */
export type ResourceType = 'equipment' | 'material';

/** 操作类型 */
export type ActionType = 'start_use' | 'end_use' | 'consume' | 'maintenance';

/** 使用日志接口 */
export interface UsageLog {
  id: number;
  user_id: number;
  resource_type: ResourceType;
  resource_id: number;
  action: ActionType;
  quantity_used?: number;
  duration_minutes?: number;
  purpose?: string;
  notes?: string;
  issues_reported?: string;
  project_name?: string;
  timestamp: string;
  auto_recorded?: boolean;
}

/** 表单数据接口 */
export interface LogFormData {
  resource_type: ResourceType;
  resource_id: string;
  action: ActionType;
  quantity_used: string;
  duration_minutes: string;
  purpose: string;
  notes: string;
  issues_reported: string;
  project_name: string;
  auto_recorded: boolean;
}

/** API 响应接口 */
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}
