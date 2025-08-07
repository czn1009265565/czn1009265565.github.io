# Spring Boot 事务管理

Spring Boot 提供了强大的事务管理支持，主要基于 Spring Framework 的事务抽象。

事务又可以分为声明式事务与编程式事务，主要区别如下:

| 特性	    | 声明式事务 (@Transactional)	  | 编程式事务 (TransactionTemplate/PlatformTransactionManager) |
|--------|--------------------------|--------------------------------------------------------|
| 实现方式	  | 基于AOP的注解配置	              | 通过编写代码显式控制                                             |
| 代码侵入性	 | 低（只需添加注解）	               | 高（需要编写事务控制代码）                                          |
| 灵活性	   | 相对固定                     | 	高度灵活                                                  |
| 可读性	   | 业务代码与事务代码分离，更清晰	         | 事务代码与业务代码混合                                            |
| 适用场景   | 	大多数常规业务场景	需要精细控制事务的特殊场景 |
| 异常处理	  | 通过注解属性配置	                | 在代码中直接处理                                               |

## 声明式事务
声明式事务 只需在方法或类上添加 `@Transactional` 注解

```java
@Transactional(
propagation = Propagation.REQUIRED,  // 传播行为
isolation = Isolation.DEFAULT,       // 隔离级别
timeout = 30,                        // 超时时间(秒)
readOnly = false,                    // 是否只读
rollbackFor = {SQLException.class},  // 指定触发回滚的异常
noRollbackFor = {NullPointerException.class} // 指定不触发回滚的异常
)
```

### 事务传播行为

- REQUIRED：如果当前没有事务，就新建一个事务；如果已经存在一个事务，就加入这个事务
- REQUIRES_NEW：新建事务，如果当前存在事务，把当前事务挂起
- SUPPORTS：支持当前事务，如果当前没有事务，就以非事务方式执行
- NOT_SUPPORTED：以非事务方式执行操作，如果当前存在事务，就把当前事务挂起
- MANDATORY：使用当前的事务，如果当前没有事务，就抛出异常
- NEVER：以非事务方式执行，如果当前存在事务，则抛出异常
- NESTED：如果当前存在事务，则在嵌套事务内执行；如果当前没有事务，则执行与 REQUIRED 类似的操作

### 隔离级别

- DEFAULT：使用底层数据库的默认隔离级别
- READ_UNCOMMITTED：读未提交
- READ_COMMITTED：读已提交
- REPEATABLE_READ：可重复读
- SERIALIZABLE：串行化


### readOnly
为什么只读操作也需要使用 `@Transactional(readOnly=true)`

1. 多次查询需要一致性视图
2. 避免连接泄露, 不使用事务时，每个Repository方法可能获取独立连接

### 实例

```java
@Service
public class BankService {
    @Autowired
    private AccountRepository accountRepository;
    @Transactional
    public void transfer(Long fromId, Long toId, BigDecimal amount) {
        // 扣减转出账户余额
        accountRepository.decreaseBalance(fromId, amount);
        // 增加转入账户余额
        accountRepository.increaseBalance(toId, amount);
    }
}
```

## 编程式事务

### 使用TransactionTemplate

```java
@Service
public class BankService {
    @Autowired
    private AccountRepository accountRepository;
    @Autowired
    private TransactionTemplate transactionTemplate;
    
    public void transfer(Long fromId, Long toId, BigDecimal amount) {
        transactionTemplate.execute(status -> {
            try {
                // 扣减转出账户余额
                accountRepository.decreaseBalance(fromId, amount);
                // 增加转入账户余额
                accountRepository.increaseBalance(toId, amount);
                // 执行成功，返回null表示无返回值
                return null;
            } catch (Exception e) {
                status.setRollbackOnly(); // 标记为回滚
                throw e; // 重新抛出异常
            }
        });
    }
}
```

### 使用PlatformTransactionManager

```java
@Service
public class BankService {
    
    @Autowired
    private AccountRepository accountRepository;
    
    @Autowired
    private PlatformTransactionManager transactionManager;
    
    public void transfer(Long fromId, Long toId, BigDecimal amount) {
        // 定义事务属性
        DefaultTransactionDefinition definition = new DefaultTransactionDefinition();
        definition.setPropagationBehavior(TransactionDefinition.PROPAGATION_REQUIRED);
        
        TransactionStatus status = transactionManager.getTransaction(definition);
        try {
            // 扣减转出账户余额
            accountRepository.decreaseBalance(fromId, amount);
            // 增加转入账户余额
            accountRepository.increaseBalance(toId, amount);
            // 手动提交
            transactionManager.commit(status);
        } catch (Exception e) {
            // 手动回滚
            transactionManager.rollback(status);
            throw e;
        }
    }
}
```

## 选择建议
1. 优先使用声明式事务：当业务逻辑简单，事务边界清晰时  
   - 优点：代码简洁，与业务逻辑解耦
   - 示例：简单的CRUD操作、单一事务边界的方法

2. 考虑编程式事务：当需要以下特性时  
   - 需要根据运行时条件决定是否提交/回滚
   - 需要更精细的事务控制（如多个独立事务块）
   - 需要捕获异常但不回滚事务
   - 示例：批量处理中的部分失败处理、复杂的事务流程