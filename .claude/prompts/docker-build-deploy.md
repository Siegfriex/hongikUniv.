# MiriArt BE Docker 빌드·푸시·배포 프롬프트

> miriart-be 전용. 외부 AI 서비스는 별도 레포에서 관리.
> 배포 파라미터 SSOT: `docs/SSOT/miriarts_infra.md` §5.2

---

## 1. WSL에서 Docker 빌드·푸시

```bash
cd ~/projects-wsl/MiriArt/miriart-be

IMAGE="asia-northeast3-docker.pkg.dev/miriarts/miriart-images/miriart-be:latest"

# 빌드
docker build -t $IMAGE .

# 레지스트리 인증 (최초 1회)
gcloud auth configure-docker asia-northeast3-docker.pkg.dev --quiet

# 푸시
docker push $IMAGE
```

---

## 2. (선택) 로컬 컨테이너 실행 테스트

```bash
docker run --rm -p 8080:8080 \
  -e SPRING_PROFILES_ACTIVE=dev \
  -e SPRING_DATASOURCE_URL="jdbc:mysql://host.docker.internal:3306/miriart_dev?useSSL=false&characterEncoding=UTF-8&serverTimezone=Asia/Seoul" \
  $IMAGE
```

---

## 3. GCP Cloud Run 배포 (gcloud CLI)

```bash
PROJECT_ID="miriarts"
REGION="asia-northeast3"
IMAGE="asia-northeast3-docker.pkg.dev/miriarts/miriart-images/miriart-be:latest"
SA="miriart-be-runner@miriarts.iam.gserviceaccount.com"
INSTANCE="miriarts:asia-northeast3:miriart-mysql"

gcloud run deploy miriart-be \
  --image=$IMAGE \
  --region=$REGION \
  --platform=managed \
  --no-allow-unauthenticated \
  --service-account=$SA \
  --port=8080 \
  --memory=1Gi \
  --add-cloudsql-instances=$INSTANCE \
  --vpc-connector=miriart-connector \
  --vpc-egress=private-ranges-only \
  --set-secrets=SPRING_DATASOURCE_URL=miriart-db-url:latest,SPRING_DATASOURCE_USERNAME=miriart-db-username:latest,SPRING_DATASOURCE_PASSWORD=miriart-db-password:latest,SPRING_DATA_REDIS_HOST=miriart-redis-host:latest,JWT_ACCESS_SECRET=miriart-jwt-access-secret:latest,JWT_REFRESH_SECRET=miriart-jwt-refresh-secret:latest,GOOGLE_CLIENT_ID=miriart-google-client-id:latest,GOOGLE_CLIENT_SECRET=miriart-google-client-secret:latest,KAKAO_CLIENT_ID=miriart-kakao-client-id:latest,KAKAO_CLIENT_SECRET=miriart-kakao-client-secret:latest,FRONTEND_OAUTH_SUCCESS_URL=miriart-frontend-oauth-url:latest \
  --set-env-vars="SPRING_PROFILES_ACTIVE=prod,FASTAPI_INTERNAL_URL=https://miriart-ai-946560105497.asia-northeast3.run.app,GCS_BUCKET_NAME=miriart-bucket" \
  --project=$PROJECT_ID
```

---

## 4. 한 번에 하기 (빌드·푸시·배포)

WSL 배시 스크립트 사용:

```bash
cd ~/projects-wsl/MiriArt/miriart-be
./scripts/cloudrun-redeploy.sh
```

- `gcloud builds submit`으로 이미지 빌드·푸시 후, 이어서 `gcloud run deploy` 실행.
- 전제: `gcloud` 로그인, 프로젝트 `miriarts`, VPC 커넥터 `miriart-connector` 및 시크릿 존재.

---

## 5. GCP 콘솔에서 "풀 앤 디플로이"

1. [Cloud Run 콘솔](https://console.cloud.google.com/run?project=miriarts) → 리전 **asia-northeast3** 선택
2. 서비스 `miriart-be` 클릭
3. **"새 리비전 배포"** → 컨테이너 이미지 URL에 `asia-northeast3-docker.pkg.dev/miriarts/miriart-images/miriart-be:latest` 입력
4. 나머지 설정 유지 → **"배포"** 클릭
