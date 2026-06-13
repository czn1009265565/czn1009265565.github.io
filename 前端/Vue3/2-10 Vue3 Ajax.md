# Vue3 Ajax
Vue 版本推荐使用 axios 来完成 ajax 请求

```shell
npm install axios
```

## Request 工具类

utils/request.js
```js
import axios from 'axios';
import { ElMessage } from 'element-plus';
import router from '@/router';

// 1. 创建实例
const service = axios.create({
    // 配置读取 .env .env.development .env.production
    baseURL: import.meta.env.VITE_API_BASE_URL,
    timeout: 15000,
});

// 2. 防重复请求池
const pendingMap = new Map();

const getRequestKey = (config) => {
    return [config.method, config.url, JSON.stringify(config.params), JSON.stringify(config.data)].join('&');
};

// 3. 请求拦截器
service.interceptors.request.use(
    (config) => {
        // TODO 用户状态实现
        const token = 'Token'
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        // 处理重复请求：如果存在相同key的请求，取消前一个
        const key = getRequestKey(config);
        if (pendingMap.has(key)) {
            pendingMap.get(key).abort();
        }
        const controller = new AbortController();
        config.signal = controller.signal;
        pendingMap.set(key, controller);

        return config;
    },
    (error) => Promise.reject(error)
);

// 4. 响应拦截器
service.interceptors.response.use(
    (response) => {
        // 请求完成，清理 Map
        const key = getRequestKey(response.config);
        pendingMap.delete(key);

        const res = response.data;

        // 核心：根据后端规范判断业务状态码，直接解包返回 data
        // 假设后端格式为 { code: 200, data: {}, message: '' }
        if (res.code === 200 || res.code === 0) {
            return res.data;
        }

        // 业务逻辑错误提示
        ElMessage.error(res.message || '请求失败');
        return Promise.reject(new Error(res.message || 'Error'));
    },
    (error) => {
        if (error.config) {
            pendingMap.delete(getRequestKey(error.config));
        }

        // 被取消的请求不弹提示
        if (axios.isCancel(error)) {
            console.warn('重复请求已取消:', error.message);
            return Promise.reject(error);
        }

        // HTTP 状态码统一处理
        if (error.response) {
            const status = error.response.status;
            const msgMap = {
                401: '登录已过期，请重新登录',
                403: '拒绝访问',
                404: '请求资源不存在',
                500: '服务器内部错误',
            };

            ElMessage.error(msgMap[status] || error.message);

            // 401 自动跳转登录
            if (status === 401) {
                // TODO logout
                router.push('/login');
            }
        } else if (error.message.includes('timeout')) {
            ElMessage.error('网络请求超时，请稍后重试');
        } else if (error.message.includes('Network Error')) {
            ElMessage.error('网络异常，请检查网络连接');
        }

        return Promise.reject(error);
    }
);

export default service;
```

## API 模块化

api/user.js
```js
import request from '@/utils/request';

/**
 * 用户登录
 * @param {{ username: string, password: string }} params - 登录参数
 * @returns {Promise<string>} 返回 Token 字符串
 */
export const login = (params) => {
    return request.post('/auth/login', params);
};

/**
 * 获取当前用户信息
 * @returns {Promise<{id: number, username: string, avatar: string}>}
 */
export const getUserList = () => {
    return request.get('/user/list');
};
```

## Vue组件使用

views/UserList.vue

```vue
<template>
  <div class="user-list">
    <h1>用户列表</h1>
    <div class="user-grid">
      <div v-for="user in users" :key="user.id" class="user-card">
        <h3>{{ user.name }}</h3>
        <p>{{ user.email }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted} from 'vue'
import {getUserList} from '@/api/user'

// 初始值必须是空数组，保证 v-for 首次渲染不报错
const users = ref([])

// 封装获取数据的方法
const fetchUsers = async () => {
  try {
    const res = await getUserList()
    users.value = res
  } catch (error) {
    console.error('获取用户列表失败:', error)
  }
}

// 在组件挂载后调用
onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.user-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
}

.user-card {
  padding: 1.5rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.user-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
</style>
```
