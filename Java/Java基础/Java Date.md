# Java Date

### DateUtils

```
@Slf4j
public class DateUtils {
    /**
     * 字符串转Date
     * yyyy-MM-dd HH:mm:ss
     */
    public static Date string2Date(String dateString, String format) {
        if (StringUtils.isEmpty(dateString)) {
            return null;
        }
        DateFormat df = new SimpleDateFormat(format);
        Date d = null;
        try {
            d = df.parse(dateString);
        } catch (Exception e) {
            e.printStackTrace();
            log.error("日期转换错误[" + dateString + "][" + format + "]", e);
        }
        return d;
    }

    public static String date2String(Date date, String format) {
        SimpleDateFormat sdf = new SimpleDateFormat(format);

        return sdf.format(date);
    }

    public static Date timestamp2Date(long timestamp) {
        return new Date(timestamp);
    }

    /**
     * 毫秒数 13位长整型
     * @param date
     * @return
     */
    public static long date2Timestamp(Date date){
        return date.getTime();
    }

    public static void main(String[] args) {
        System.out.println(string2Date("2020/03/25 10:10:10","yyyy/MM/dd HH:mm:ss"));
        System.out.println(date2String(new Date(),"yyyy-MM-dd HH:mm:ss"));
        System.out.println(timestamp2Date(System.currentTimeMillis()));
        System.out.println(date2Timestamp(new Date()));
    }
}
```


### 时间线
静态方法调用`Instant.now()`给出当前的时刻，可以使用`equals`或者`compareTo`方法来比较两个Instant对象，因此也可以用作时间戳。
```
Instant start = Instant.now();
TimeUnit.SECONDS.sleep(1);
Instant end = Instant.now();
Duration duration = Duration.between(start,end);
System.out.println(duration.toMillis()); // 时间间隔，toMillis毫秒,toNanos纳秒,toMinutes分钟...
```


### 本地日期
构建localDate对象，可以使用`new`或者`of`静态方法
```
LocalDate today = LocalDate.now();
LocalDate future = LocalDate.of(2021,1,1);
System.out.println(today);
System.out.println(future);
```

日期计算,日期的加减，包括day,week,month,year
```
LocalDate today = LocalDate.now();
LocalDate nextDay = today.plusDays(1); // 加一天
LocalDate nextMonth = today.plusMonths(1); // 加一个月
LocalDate preYear = today.minusYears(1); // 减一年
System.out.println(today);
System.out.println(today.until(nextMonth, ChronoUnit.DAYS)); // 到下个月所需要的天数
```

### 本地时间
`LocalTime`用法与LocalDate类似。

### 时区时间
`ZonedDateTime`,具体时区id查看ZoneId源码
```
ZonedDateTime zonedDateTime = ZonedDateTime.of(LocalDate.now(), LocalTime.now(), ZoneId.of("Asia/Shanghai"));
System.out.println(zonedDateTime);
```

### 格式化和解析
`DateTimeFormatter`为我们提供了预定义的格式器，以及自定义格式器

```
ZonedDateTime zonedDateTime = ZonedDateTime.of(LocalDate.now(), LocalTime.now(), ZoneId.of("Asia/Shanghai"));
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
String s = formatter.format(zonedDateTime);
System.out.println(s);
System.out.println(formatter.parse(s));
```
**注意点 `yyyy-MM-dd HH:mm:ss`是24小时制时间，`yyyy-MM-dd hh:mm:ss`则是12小时制时间**


