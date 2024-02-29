## PostGis
本文主要记录 PostGis中的空间地理的使用

个人觉得初学者首先要区分 geomtery(平面坐标系)和geography(地理坐标系 经纬度)

### 添加PostGIS扩展
1. 加载 PostGIS 扩展 `CREATE EXTENSION postgis;`
2. 查看postgis版本 `SELECT postgis_full_version();`

### 简单查询

```sql
-- 创建城市表
CREATE TABLE cities (id int4 primary key, name varchar(50), geom geometry(POINT,4326));
-- 简单查询
SELECT id, ST_AsText(geom), ST_AsEwkt(geom), ST_X(geom), ST_Y(geom) FROM cities;
 id |          st_astext           |               st_asewkt                |    st_x     |   st_y
----+------------------------------+----------------------------------------+-------------+-----------
  1 | POINT(-0.1257 51.508)        | SRID=4326;POINT(-0.1257 51.508)        |     -0.1257 |    51.508
  2 | POINT(-81.233 42.983)        | SRID=4326;POINT(-81.233 42.983)        |     -81.233 |    42.983
  3 | POINT(27.91162491 -33.01529) | SRID=4326;POINT(27.91162491 -33.01529) | 27.91162491 | -33.01529
```

### Geomtery
### 创建测试表

```sql
CREATE TABLE geometries (name varchar, geom geometry);

INSERT INTO geometries VALUES
  ('Point', 'POINT(0 0)'),
  ('LineString', 'LINESTRING(0 0, 1 1, 2 1, 2 2)'),
  ('Polygon', 'POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'),
  ('PolygonWithHole', 'POLYGON((0 0, 10 0, 10 10, 0 10, 0 0),(1 1, 1 2, 2 2, 2 1, 1 1))'),
  ('Collection', 'GEOMETRYCOLLECTION(POINT(2 0),POLYGON((0 0, 1 0, 1 1, 0 1, 0 0)))');

SELECT name, ST_AsText(geom) FROM geometries;
```


### Geography
#### 创建测试表

```sql
CREATE TABLE airports (
    code VARCHAR(3),
    geog GEOGRAPHY(Point),
    area GEOGRAPHY(Polygon)
  );

INSERT INTO airports
  VALUES ('LAX', 'POINT(-118.4079 33.9434)');
INSERT INTO airports
  VALUES ('CDG', 'POINT(2.5559 49.0083)');
INSERT INTO airports
  VALUES ('KEF', 'POINT(-22.6056 63.9850)');
```

1. ST_GeometryFromText(text) return geometry

#### 基本函数
1. ST_AsText(geography) return text

    ```sql
    SELECT code,ST_AsText(geog) FROM airports;
    ```

2. ST_GeographyFromText(text) return geography

    ```sql
    SELECT ST_GeographyFromText('POINT(-118.4079 33.9434)') as geog;
    ```

3. ST_AsBinary(geography) return bytea
4. ST_GeogFromWKB(bytea) return geography
5. ST_AsSVG(geography) return geography
6. ST_AsGML(geography) return text
7. ST_AsKML(geography) return text
8. ST_AsGeoJson(geography) return GeoJson

    ```sql
    SELECT code,ST_AsGeoJson(geog) FROM airports;
    ```

9. ST_Distance(geography, geography) return double(单位米)

    ```sql
    SELECT ST_Distance(
      ST_GeographyFromText('POINT(-118.4079 33.9434)'), -- Los Angeles (LAX)
      ST_GeographyFromText('POINT(2.5559 49.0083)')     -- Paris (CDG)
      ) as distance;
    ```

10. ST_DWithin(geography, geography, float8) return boolean

    ```sql
    -- 查询在POINT(-118.4080 33.9435)附近100米以内的机场数据
    SELECT code,geog FROM airports WHERE ST_DWithin(geog, ST_GeographyFromText('POINT(-118.4080 33.9435)'), 100);
    ```

11. ST_Area(geography) return double 计算多边形面积(单位平方米)

    ```sql
    SELECT code,geog,ST_Area(area) FROM airports;
    ```

12. ST_Length(geography) return double 计算LineString长度(单位米)
  
    ```sql
    SELECT ST_Length(ST_GeographyFromText('LINESTRING(-118.4079 33.9434, -118.4080 33.9435)')) as length
    ```

13. ST_Covers(geography, geography) return boolean
14. ST_CoveredBy(geography, geography) return boolean
15. ST_Intersects(geography, geography) return boolean,判断是否相交包括(点对点,点对线,点对面,线对线,线对面,面对面)
16. ST_Buffer(geography, float8) return geography
17. ST_Intersection(geography, geography) return geography 返回重叠区域
18. ST_Contains(geometry, geometry) 第一个面数据包含第二个面数据


### 类型相互转换

#### geometry 转 geography

将geometry转换为geography，首先需要将geometry投影到EPSG:4326(WGS84)，然后再将其转换为geography。`ST_Transform(geometry, srid)`函数能将坐标转换为地理坐标，`Geography(geometry)`函数能将geometry转换为geography。

```sql
SELECT name, Geography(ST_Transform(geom,4326)) FROM geometries;

-- 当数据没有设置srid时,默认为4326,直接转换即可
SELECT name, Geography(geom) FROM geometries;
SELECT name, geom::geography FROM geometries;
```

### geography 转 geometry
将geography转换为geometry方便使用geometry函数

```sql
SELECT code,ST_X(Geometry(geog)) as longitude,ST_Y(Geometry(geog)) as latitude FROM airports;
SELECT code,ST_X(geog::geometry) as longitude,ST_Y(geog::geometry) as latitude FROM airports;
```


