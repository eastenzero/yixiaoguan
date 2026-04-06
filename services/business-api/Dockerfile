FROM eclipse-temurin:21-jre-alpine
LABEL maintainer="yixiaoguan-team"

WORKDIR /app

# 使用预构建 jar（不在容器内 Maven 构建，节省资源）
COPY ruoyi-admin/target/ruoyi-admin.jar app.jar

RUN mkdir -p logs uploadPath

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
