/**
 * API 模块统一导出
 */

export * from './types'
export * from './auth'
export * from './dashboard'
export * from './approval'
export * from './questions'
export * from './knowledge'

// 默认导出 request 实例
export { default as request } from '@/utils/request'
