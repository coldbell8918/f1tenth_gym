# 🧭 Semantic Map → Home-Tree → Patrol Node 생성 가이드

본 문서는 Active SLAM을 통해 수집된 데이터를 기반으로
Semantic Map 생성 → Room Segmentation → Home-Tree 생성 → Patrol Node 선정까지의 전체 과정을 설명합니다.

---

## 🧠 1. Semantic Map 생성

Active SLAM을 통해 저장된 데이터를 활용하여 Semantic Map을 생성합니다.

### ⚙️ 설정 파일 수정

`semantic_map/configs.py`에서 아래 항목들을 설정합니다:

* RGB 이미지 경로
* Depth 이미지 경로
* Pose 로그 경로
* 카메라 파라미터 (Intrinsic / Extrinsic 등)

```python id="x2p9ls"
# 예시
rgb_path = "your/path/to/rgb"
depth_path = "your/path/to/depth"
pose_path = "your/path/to/pose"
```

---

### 🤖 모델 선택

Semantic Map 생성에 사용할 모델을 선택합니다.

```python id="1j7d3k"
model_type: str = "yoloe"  # "sam3", "yoloe", "grounded_sam2" 중 택 1
```

선택 가능한 옵션:

* `"sam3"`
* `"yoloe"`
* `"grounded_sam2"`

📌 모델에 따라 정확도 및 처리 속도가 달라질 수 있습니다.

---

### ▶️ 실행

```bash id="sl8q2c"
python 1_main_semantic_map.py
```

📌 결과:

* Semantic Map 생성

---

## 🏠 2. Room Segmentation 및 Home-Tree 생성

생성된 Semantic Map을 기반으로 공간을 분할하고 Home-Tree 구조를 생성합니다.

---

### ⚙️ 설정 파일 수정

`room_segmentation/configs.py`에서 관련 파라미터를 설정합니다.

📌 예:

* segmentation threshold
* clustering 옵션
* 입력 Semantic Map 경로

---

### ▶️ 실행

```bash id="j3k91v"
python 2_room_segmentation.py
```

📌 결과:

* Room segmentation 완료
* 최종 `home-tree.json` 생성

---

## 🚓 3. Patrol Node 선정

Home-Tree를 기반으로 Patrol 수행에 필요한 주요 노드를 선택합니다.

---

### ⚙️ 설정 파일 수정

`patrol/configs.py`에서 다음과 같은 항목을 설정합니다:

* Patrol 전략
* 노드 선택 기준
* 입력 Home-Tree 경로

---

### ▶️ 실행

```bash id="k9s0dl"
python 3_main_patrol_node.py
```

📌 결과:

* Patrol에 사용될 주요 노드 리스트 생성

---

## 🧩 전체 파이프라인 요약

1. Semantic Map 생성
2. Room Segmentation 수행
3. Home-Tree 생성
4. Patrol Node 선정

---

## ⚠️ 주의 사항

* 모든 경로 설정은 **절대 경로 기준**으로 설정하는 것을 권장합니다.
* 입력 데이터(RGB, Depth, Pose)가 정확히 정렬되어 있어야 합니다.
* 모델 선택에 따라 GPU 사용 여부 및 성능 차이가 발생할 수 있습니다.
* 설정 파일(configs.py) 수정 후 저장 여부를 반드시 확인하세요.

---

## 📁 권장 디렉토리 구조

```id="m2v8zp"
project/
├── rgb/
├── depth/
├── pose/
├── semantic_map/
├── room_segmentation/
├── patrol/
└── home-tree.json
```

---

각 단계별 세부 옵션은 해당 디렉토리 내 `configs.py` 및 README를 참고하여 조정하세요.
