# Vue3 Pinia

Pinia 是 Vue 3 官方推荐的新一代状态管理库，它让你能够在组件之间共享和管理状态，
可以把 Pinia 想象成一个全局的数据仓库，所有组件都可以从这里获取数据或者更新数据。

## API速查

| API                       | 说明                    |
|---------------------------|-----------------------|
| defineStore(id, setup)	   | 组合式写法（Setup Store）	   |
| defineStore(id, options)	 | 选项式写法（Options Store）  |
| createPinia()	            | 创建 Pinia 实例           |
| useXxxStore()             | 	获取 Store 实例	         |
| storeToRefs(store)	       | 解构 State/Getter 保持响应式 |
| storeToRaw(store)	        | 获取原始非响应式对象            |

Store 实例内置属性与方法

| API             | 类型       | 说明                         |
|-----------------|----------|----------------------------|
| $id             | string   | Store 的唯一标识符               |
| $state          | object   | 完整 state 对象的引用（可直接读写）      |
| $patch(partial) | Function | 批量修改 state，支持对象合并或函数模式     |
| $reset()        | Function | 重置 state 到初始值（⚠️ 仅选项式可用）   |
| $subscribe(cb)  | Function | 订阅 state 变化（类似 watch，但更底层） |
| $onAction(cb)   | Function | 监听 action 的调用、结果与错误        |
| $dispose()      | Function | 销毁 store，移除所有订阅            |

## 安装与配置

### 安装 Pinia

```shell
npm install pinia
```

### 配置 Pinia

在入口文件 `main.js` 中注册 `Pinia`

```js
// main.js
import {createApp} from 'vue'
import {createPinia} from 'pinia'
import App from './App.vue'

// 创建 Pinia 实例
const pinia = createPinia()
// 创建 Vue 应用
const app = createApp(App)

// 使用 Pinia
app.use(pinia)
app.mount('#app')
```

## 创建 Store

Store 就是 Pinia 中的数据仓库

结构:

- state 定义存储的数据
- getters 基于 state 的计算属性
- actions 修改 state 的方法

### 定义 Store

新建 `src/stores/useCounter.js`

#### Options API

```js
import {defineStore} from 'pinia'

// 使用 defineStore 定义 store
// 第一个参数是 store 的唯一 ID
// 第二个参数是 store 的配置选项
export const useCounterStore = defineStore('counter', {
    // state: 定义 store 的状态数据
    state: () => ({
        count: 0,
        name: '我的计数器'
    }),

    // getters: 定义基于 state 的计算属性
    getters: {
        doubleCount: (state) => state.count * 2,
        // 使用 this 访问其他 getter
        doubleCountPlusOne() {
            return this.doubleCount + 1
        }
    },

    // actions: 定义修改 state 的方法
    actions: {
        increment() {
            this.count++
        },
        decrement() {
            this.count--
        },
        // 可以接收参数
        incrementBy(amount) {
            this.count += amount
        },
        // 异步 action
        async incrementAsync() {
            // 模拟异步操作
            await new Promise(resolve => setTimeout(resolve, 1000))
            this.count++
        }
    }
})
```

#### Composition API

```js
import {defineStore} from "pinia";
import {computed, ref} from "vue";

export const useCounterStore = defineStore('counter', () => {
    // state
    const count = ref(0)
    const name = ref('计数器')

    // getters
    const doubleCount = computed(() => count.value * 2)
    const doubleCountPlusOne = computed(() => doubleCount.value + 1)

    // actions
    function increment() {
        count.value++
    }

    function decrement() {
        count.value--
    }

    function incrementBy(amount) {
        count.value += amount
    }

    async function incrementAsync() {
        await new Promise(resolve => setTimeout(resolve, 1000))
        count.value++
    }

    function reset() {
        count.value = INITIAL_COUNT
        name.value = INITIAL_NAME
    }

    return {
        count,
        name,
        doubleCount,
        doubleCountPlusOne,
        increment,
        decrement,
        incrementBy,
        incrementAsync,
        reset
    }
})
```

### 组件中使用

`src/components/CounterComponent.vue`

```vue
<!-- CounterComponent.vue -->
<template>
  <div class="counter">
    <h3>{{ store.name }}</h3>
    <p>当前计数: {{ store.count }}</p>
    <p>双倍计数: {{ store.doubleCount }}</p>
    <p>双倍加一: {{ store.doubleCountPlusOne }}</p>

    <button @click="store.increment()">+1</button>
    <button @click="store.decrement()">-1</button>
    <button @click="store.incrementBy(5)">+5</button>
    <button @click="store.incrementAsync()">异步 +1</button>

    <button @click="store.reset()">重置</button>
  </div>
</template>

<script setup>
  import {useCounterStore} from '@/stores/useCounter'

  // 在 setup 中使用 store
  const store = useCounterStore()
</script>
```

### 响应式解构

```vue
<template>
  <div>
    <p>计数: {{ count }}</p>
    <p>名称: {{ name }}</p>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import {useCounterStore} from '@/stores/useCounter'

const store = useCounterStore()

// 使用 storeToRefs 保持响应式
const { count, name } = storeToRefs(store)

// 注意：直接解构会失去响应式！
// 错误写法：const { count, name } = store
</script>
```

## 数据持久化

对于需要持久化的数据，可以使用插件: `npm install pinia-plugin-persistedstate`

### 全局初始化

```js
// main.ts
import {createApp} from 'vue'
import {createPinia} from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import App from './App.vue'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const app = createApp(App)
app.use(pinia)
app.mount('#app')
```

### 自定义 Store

`stores/useUserStore.js`

```js
import {defineStore} from 'pinia'
import {ref} from 'vue'

export const useUserStore = defineStore('user', () => {
    // state
    const token = ref('')
    const userInfo = ref({})

    // actions
    function setToken(newToken) {
        token.value = newToken
    }

    function setUserInfo(info) {
        userInfo.value = info
    }

    function logout() {
        token.value = ''
        userInfo.value = {}
    }

    // 必须显式 return 所有需要暴露的 state 和 actions
    return {
        token,
        userInfo,
        setToken,
        setUserInfo,
        logout
    }
}, {
    // 持久化配置作为 defineStore 的第三个参数
    persist: true
})
```