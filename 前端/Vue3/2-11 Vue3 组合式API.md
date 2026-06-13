# Vue3 组合式API

Vue 3 的组合式 API（Composition API） 是 Vue 3 引入的一套全新的组件编写方式。
核心目的是解决复杂组件的逻辑复用和代码组织问题，并提供更好的 TypeScript 支持。

## 响应式系统
使用 ref 和  将数据变成响应式对象，底层通过 `Proxy` 拦截 `get、set、deleteProperty` 等操作，
并在读取时收集依赖（跟踪），在修改时触发更新（通知）

### Options API
通过 `data()` 选项返回一个普通对象，
Vue 在底层将其劫持并代理到组件实例（this）上。
开发者无需关心底层是基本类型还是对象，统一通过 `this.xxx` 访问和修改

```vue
<!-- Options API -->
<script>
export default {
  data() {
    return {
      count: 0,               // 基本类型
      user: { name: 'Alice' } // 对象类型
    }
  },
  methods: {
    updateData() {
      // 统一通过 this 访问，无需区分类型
      this.count++
      this.user.name = 'Bob'
    }
  }
}
</script>
```

### Composition API

显式调用 `ref()` 或 `reactive()` 创建响应式数据。
最大的差异在于: `ref` 在 `JS` 逻辑中必须通过 `.value` 访问和修改，而在 `<template>` 中会自动解包；`reactive` 则直接操作对象属性

```vue
<!-- Composition API -->
<script setup>
import { ref, reactive } from 'vue'

// 推荐: 统一使用 ref
const count = ref(0)
const user = ref({ name: 'Alice' })

// 备选: 使用 reactive 处理深层对象
// const user = reactive({ name: 'Alice' })

function updateData() {
  // ⚠️ JS 中操作 ref 必须加 .value
  count.value++
  user.value.name = 'Bob' 
  
  // 如果上面用的是 reactive，则直接 user.name = 'Bob'
}
</script>

<template>
  <!-- 模板中 ref 自动解包，不需要 .value -->
  <p>{{ count }} - {{ user.name }}</p>
</template>
```

## 计算属性与侦听器

### Options API

- 计算属性在 `Options API` 中是配置对象，支持 `get/set`
- `watch` 必须通过字符串路径（如 'user.name'）或数据对象来指定侦听源

```vue
<!-- Options API -->
<script>
export default {
  data() {
    return { firstName: '张', lastName: '三', log: '' }
  },
  computed: {
    // 配置项形式
    fullName() {
      return this.firstName + this.lastName
    }
  },
  watch: {
    // ⚠️ 必须使用字符串路径指定侦听源
    fullName: {
      handler(newVal, oldVal) {
        this.log = `名字从 ${oldVal} 变成了 ${newVal}`
      },
      immediate: true // 初始立即执行一次
    }
  }
}
</script>
```

### Composition API

- 计算属性在 `Composition API` 中是 `computed()` 函数，接收一个 `getter` 函数，返回一个只读的 ref（也可传入对象实现可写）
- `watch()` 直接接收响应式变量或 `getter` 函数作为侦听源，支持同时侦听多个源（数组）。此外还新增了 `watchEffect()` 用于自动收集依赖

```vue
<!-- Composition API -->
<script setup>
import { ref, computed, watch, watchEffect } from 'vue'

const firstName = ref('张')
const lastName = ref('三')
const log = ref('')

// 函数形式，返回一个只读的 ref
const fullName = computed(() => firstName.value + lastName.value)

// 直接传入 computed 返回的 ref 变量作为侦听源
watch(fullName, (newVal, oldVal) => {
  log.value = `名字从 ${oldVal} 变成了 ${newVal}`
}, { immediate: true })

// 进阶: 使用 watchEffect 自动追踪依赖（无需手动指定 fullName）
watchEffect(() => {
  log.value = `当前全名是: ${fullName.value}`
})
</script>
```

## 生命周期钩子
生命周期钩子是 Vue 组件从创建到销毁过程中特定时间点自动执行的回调函数

### Options API

生命周期是组件实例的固定配置项（如 mounted）。
每个钩子只能定义一次，所有挂载逻辑必须挤在一个函数里。`beforeCreate` 和 `created` 用于初始化数据。

```vue
<!-- Options API -->
<script>
export default {
  data() { return { timer: null } },
  // 所有挂载逻辑必须写在一个 mounted 里，容易臃肿
  mounted() {
    console.log('1. 请求初始数据')
    this.fetchData()
    
    console.log('2. 初始化定时器')
    this.timer = setInterval(() => {}, 1000)
    
    console.log('3. 绑定全局事件')
    window.addEventListener('resize', this.handleResize)
  },
  unmounted() {
    clearInterval(this.timer)
    window.removeEventListener('resize', this.handleResize)
  },
  methods: {
    fetchData() {},
    handleResize() {}
  }
}
</script>
```

### Composition API
生命周期是 `onXxx()` 函数。
同一个钩子可以被多次调用，逻辑可以分散甚至抽离到外部函数中。
`setup()` 函数本身替代了 `beforeCreate` 和 `created`

```vue
<!-- Composition API -->
<script setup>
  import { onMounted, onUnmounted } from 'vue'

  // 可以多次调用 onMounted，按功能拆分，极其清晰
  onMounted(() => {
    console.log('1. 请求初始数据')
    fetchData()
  })

  let timer = null
  onMounted(() => {
    console.log('2. 初始化定时器')
    timer = setInterval(() => {}, 1000)
  })

  function handleResize() {}
  onMounted(() => {
    console.log('3. 绑定全局事件')
    window.addEventListener('resize', handleResize)
  })

  // 清理逻辑也可以紧跟在注册逻辑之后（或者统一放在 onUnmounted）
  onUnmounted(() => {
    clearInterval(timer)
    window.removeEventListener('resize', handleResize)
  })

  function fetchData() {}
</script>
```

## 组件通信
- Props & Emits: Options API 使用组件选项对象配置。Composition API（特指 <script setup>）使用编译器宏 `defineProps` 和 `defineEmits`，无需 `import`，且对 `TypeScript` 泛型支持极佳
- Provide / Inject: Options API 中，如果 `provide` 的是响应式数据，Vue 2 需要特殊处理，Vue 3 虽然支持但写法依然受限。Composition API 使用 `provide() / inject()` 函数，直接传递 `ref` 即可让后代组件获得响应式数据

### Options API

```vue
<!-- Options API -->
<script>
export default {
  // 1. Props 配置
  props: {
    title: { type: String, required: true }
  },
  // 2. Emits 配置
  emits: ['update'],
  // 3. Provide 配置 (如果是响应式数据，Vue2 中需要写函数)
  provide() {
    return {
      theme: 'dark' // ⚠️ 这里传递普通字符串，后代修改不会触发响应
    }
  },
  methods: {
    handleClick() {
      this.$emit('update', 'new title')
    }
  }
}
</script>
```

### Composition API

```vue
<!-- Composition API (<script setup>) -->
<script setup>
import { ref, provide, inject } from 'vue'

// 1. Props: 使用编译器宏，支持 TS 泛型
const props = defineProps<{
  title: string
}>()

// 2. Emits: 使用编译器宏
const emit = defineEmits<{
  (e: 'update', value: string): void
}>()

// 3. Provide: 直接传递 ref，后代组件自动获得响应式能力！
const theme = ref('dark')
provide('theme', theme) 

function handleClick() {
  emit('update', 'new title')
}

// 4. Inject: 后代组件注入
// const injectedTheme = inject('theme', ref('light'))
</script>
```


## 模板引用与 DOM 访问
- Options API: 在模板中使用 ref="xxx"，在 JS 中通过 `this.$refs.xxx` 访问。必须在 `mounted` 之后才能获取到 DOM 节点
- Composition API: 在 `<script setup>` 中，声明一个与模板 `ref` 属性同名的 `ref` 变量。在 `onMounted` 之后，通过该变量的 `.value` 即可访问 `DOM` 节点或子组件实例

### Options API

```vue
<!-- Options API -->
<template>
  <input ref="myInput" type="text" />
</template>

<script>
export default {
  mounted() {
    // 通过 this.$refs 访问
    this.$refs.myInput.focus()
  }
}
</script>
```

### Composition API

```vue
<!-- Composition API -->
<template>
  <!-- 模板中的 ref 属性名 -->
  <input ref="inputRef" type="text" />
</template>

<script setup>
import { ref, onMounted } from 'vue'

// ⚠️ 变量名必须与模板中的 ref 属性名完全一致
const inputRef = ref(null)

onMounted(() => {
  // 通过 .value 访问 DOM 节点
  inputRef.value.focus()
})
</script>
```
