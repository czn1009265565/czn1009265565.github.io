# Java Date

## Date
java.util 包提供了 Date 类来封装当前的日期和时间。

基本API:  
```java
public class DateTest {
    public static void main(String[] args) {
        // 实例化对象
        Date now = new Date();
        Date date = new Date(System.currentTimeMillis());

        // 获取时间戳
        long timestamp = now.getTime();

        // 日期比较
        boolean before = date.before(now);
        boolean after = date.after(now);
    }
}
```

## DateFormat
java.text.DateFormat 是日期/时间格式化子类的抽象类，
通过这个类可以完成日期和文本之间的转换，也就是可以在Date对象与String对象之间进行来回转换。

字符串格式:  
- y	年
- M	月
- d	日
- H	时
- m	分
- s	秒

```java
public class DateFormatTest {
    public static void main(String[] args) {
        // 初始化格式
        DateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        // 日期时间格式化字符串
        Date now = new Date();
        String dateValue = format.format(now);

        // 字符串解析为Date对象
        try {
            Date date = format.parse("2024-01-01 00:00:00");
        } catch (ParseException e) {
            e.printStackTrace();
        }
    }
}
```

## Calendar
在Java中，Calendar是一个用于处理日期和时间的类。
它提供了许多方法来获取和设置日期、时间以及执行日期和时间的计算操作。
使用Calendar类，可以执行各种常见的日期和时间操作，如获取当前日期和时间、计算两个日期之间的差异、添加或减去指定数量的年、月、日、小时、分钟等等。

```java
public class CalendarTest {
    public static void main(String[] args) {
        // 初始化
        Calendar calendar = Calendar.getInstance();
        // Date转Calendar
        Calendar instance = Calendar.getInstance();
        instance.setTime(new Date());
        // Calendar转Date
        Date date = instance.getTime();

        // 获取年月日
        int year = calendar.get(Calendar.YEAR);
        int month = calendar.get(Calendar.MONTH);
        int day = calendar.get(Calendar.DAY_OF_MONTH);
        System.out.printf("%s年%s月%s日%n", year, month, day);

        // 设置年月日
        calendar.set(Calendar.YEAR, 2024);
        calendar.set(Calendar.MONTH, 1);
        calendar.set(Calendar.DAY_OF_MONTH, 1);
        System.out.println(calendar);

        // 时间计算
        calendar.add(Calendar.YEAR, 1);
        calendar.add(Calendar.YEAR, -1);
    }
}
```

## Java8日期类
- LocalDate  日期/年月日
- LocalTime  时间/时分秒
- LocalDateTime  日期时间/年月日时分秒

这里以LocalDate为例，LocalTime、LocalDateTime用法类似

```
public class LocalDateTest {
    public static void main(String[] args) {
        
        // 初始化
        LocalDate localDate = LocalDate.now();
        LocalDate future = LocalDate.of(2024,1,1);

        // 获取年月日
        int year = localDate.getYear();
        int month = localDate.getMonth().getValue();
        int day = localDate.getDayOfMonth();
        System.out.printf("%s年%s月%s日%n", year, month, day);

        // 日期计算
        LocalDate tomorrow = localDate.plus(1, ChronoUnit.DAYS);
        LocalDate yesterday = localDate.plus(-1, ChronoUnit.DAYS);
        // 日期比较
        boolean equals = localDate.equals(future);
        boolean before = localDate.isBefore(future);
        boolean after = localDate.isAfter(future);

        // 获取详情
        // 获取所在月份的天数
        int dayOfMonth = localDate.getDayOfMonth();
        // 获取所在周的天数
        int dayOfWeek = localDate.getDayOfWeek().getValue();
        // 获取所在年的天数
        int dayOfYear = localDate.getDayOfYear();
        // 获取所在月份的第一天
        LocalDate firstDayOfMonth = localDate.with(TemporalAdjusters.firstDayOfMonth());
        // 获取所在月份下个月的第一天
        LocalDate firstDayOfNextMonth = localDate.with(TemporalAdjusters.firstDayOfNextMonth());
        // 获取所在月份的最后一天
        LocalDate lastDayOfMonth = localDate.with(TemporalAdjusters.lastDayOfMonth());
    }
}
```

日期时间格式化和解析，`DateTimeFormatter`为我们提供了预定义的格式器，以及自定义格式器

```
public class LocalDateTimeTest {
    public static void main(String[] args) {
        LocalDateTime localDateTime = LocalDateTime.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

        // 格式化字符串
        String formattedDateTime = localDateTime.format(formatter);
        LocalDateTime parsedDateTime = LocalDateTime.parse("2024-01-01 12:30:00", formatter);
    }
}
```


