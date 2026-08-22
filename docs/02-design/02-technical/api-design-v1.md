# API Design v1 — ระบบสั่งอาหารด้วย QR Code (Phase 0)

> **สถานะ: DRAFT (ร่าง API contract ของ Phase 0)**
> ต้นทาง: [[../../01-requirements/01-spec/product-backlog-v1|Product Backlog v1]] (Business Rule ข้อ 1-23), [[../../01-requirements/01-spec/ux-requirements-v1|UX Requirements v1]] (โดยเฉพาะหัวข้อ 5 Error/Empty/Edge States และหัวข้อ 6 Content & Tone)
> จัดทำโดย: COULSON (Web PM & Architect) — วันที่ 2026-08-15
> เอกสารพี่น้อง: [[architecture-v1|Architecture v1]] · [[data-model-v1|Data Model v1]]

> 🔴 **แก้ไข 2026-08-20** — เปลี่ยนชื่อตามที่ตัดสินใน [[data-model-v1|Data Model v1]] §9.4 · `table_session` → `visit_session` · `shop_table` → `service_point` **เปลี่ยนเฉพาะชื่อ ไม่มีตรรกะข้อไหนเปลี่ยน** · คำว่า "โต๊ะ" ในเนื้อความคงไว้เพราะเป็นคำเรียกของร้านกาแฟ ซึ่งอยู่ที่ `shop.service_point_label`

กลับไปที่ [[index|02-technical]]

---

## 1. ข้อตกลงร่วม (Conventions)

| หัวข้อ | ข้อตกลง |
|---|---|
| Base path | `/api/v1` (implement เป็น Next.js Route Handler) |
| Format | JSON เท่านั้น · `Content-Type: application/json` |
| เงิน | ทุก field เป็น **integer หน่วยสตางค์** ชื่อลงท้าย `_satang` — client เป็นผู้แปลงเป็นบาทตอนแสดงผล |
| เวลา | ISO-8601 พร้อม offset (`2026-08-15T14:03:22+07:00`) |
| การเขียนที่ไม่ idempotent โดยธรรมชาติ | ต้องส่ง header `Idempotency-Key` (UUID จาก client) — ใช้กับ `POST /orders`, `POST /counter-orders`, `POST /bills/{id}/payment` |
| การอัปเดตที่แข่งกันได้ | ใช้ **conditional update**: ส่งสถานะ/เวอร์ชันที่ client เชื่อว่าเป็นจริงมาด้วย (`expected_status`, `expected_version`, `expected_total_satang`) → ไม่ตรงคืน `409` พร้อมสถานะปัจจุบัน **ห้ามเขียนทับเงียบ ๆ** |
| Pagination | cursor-based (`?cursor=&limit=`) เฉพาะรายการประวัติ — คิวหน้าร้านไม่ต้องแบ่งหน้า |
| ภาษาข้อความ | `message_th` เป็นข้อความที่แสดงต่อผู้ใช้จริง **ห้ามมีศัพท์เทคนิค** (UX §6) · `code` เป็นภาษาอังกฤษสำหรับ log/dev |

### 1.1 ตัวตนของผู้เรียก 3 แบบ

| ผู้เรียก | ได้สิทธิ์มาอย่างไร | ขอบเขต |
|---|---|---|
| **guest** | cookie `cs_token` (JWT, HttpOnly/Secure/SameSite=Lax) ที่เซิร์ฟเวอร์ออกให้ตอนสแกน QR · claims `{ sid, tsid?, tid?, ch, exp }` **ไม่มีข้อมูลส่วนบุคคล** (BR ข้อ 14) | อ่าน/เขียนได้เฉพาะตะกร้าและออเดอร์ของ session/โต๊ะตัวเอง |
| **staff** | Supabase Auth JWT, `role='staff'` (BR ข้อ 9) | ทุกออเดอร์/บิล/โต๊ะ + toggle ของหมด |
| **admin** | Supabase Auth JWT, `role='admin'` | staff ทั้งหมด + จัดการเมนู/option/โต๊ะ/QR |

**สิทธิ์ที่ guest ไม่มีเด็ดขาด:** ยกเลิกออเดอร์ (BR ข้อ 5), เปลี่ยนสถานะออเดอร์, ปิดบิล, ยืนยันการชำระเงิน, มาร์กสินค้าหมด, เห็นข้อมูลของโต๊ะอื่น

### 1.2 ซองข้อความ error มาตรฐาน

```jsonc
{
  "error": {
    "code": "ITEM_UNAVAILABLE_AT_CONFIRM",
    "message_th": "ลาเต้ (เย็น) เพิ่งหมดพอดี จึงไม่ได้ส่งเข้าครัว รายการอื่นส่งเรียบร้อยแล้ว",
    "next_action": "เลือกเครื่องดื่มอื่นแทน หรือกดเรียกพนักงาน",   // UX §6: error ต้องบอกว่าทำอะไรต่อได้เสมอ
    "details": { "rejected_item_ids": ["…"] }
  }
}
```

---

## 2. Endpoint ฝั่งลูกค้า (guest)

### 2.1 จุดเข้าจาก QR — **ไม่ใช่ API แต่เป็นหน้าเว็บ**

```
GET  https://<domain>/t/{code}    → หน้าเมนู dine-in   (US-01)
GET  https://<domain>/c/{code}    → หน้าเมนู takeaway  (US-28)
```

🔴 **ตั้งใจให้ URL ใน QR เป็นหน้าเมนูโดยตรง ไม่ใช่ endpoint ที่ redirect** — UX-01 กำหนด "0 หน้ากลาง" การทำ `/scan?code=…` แล้ว redirect ไป `/menu` คือหน้ากลางที่มองไม่เห็นแต่กินเวลาจริงบนเน็ตช้า route นี้ทำ 3 อย่างในการ request เดียว: resolve QR → สร้าง/เข้าร่วม session + ตั้ง cookie → server-render เมนูส่งกลับ

**กรณีที่ resolve ไม่ผ่าน** (ตาม UX §5 แถว "สแกน QR ไม่ติด"):

| สถานการณ์ | HTTP | code | `message_th` |
|---|---|---|---|
| ไม่พบ `code` | 404 | `QR_NOT_FOUND` | "ไม่พบข้อมูลโต๊ะจาก QR นี้ กรุณาแจ้งพนักงานเพื่อสั่งอาหาร" |
| QR ถูกปิดใช้งาน | 410 | `QR_INACTIVE` | "QR นี้เลิกใช้งานแล้ว กรุณาแจ้งพนักงาน" |
| โต๊ะถูกปลดระวาง (US-42) | 410 | `TABLE_RETIRED` | "โต๊ะนี้ไม่เปิดให้บริการแล้ว กรุณาแจ้งพนักงาน" |
| ร้านปิดรับออเดอร์ (เตรียมทาง US-26) | 200 | — | แสดงหน้า "ร้านปิดรับออเดอร์แล้ว" แทนเมนู ไม่มีปุ่มสั่ง (UX §5) |

ทุกกรณี error ต้องแสดง **ทางออกที่ไม่ใช่การงมเอง** (UX principle ข้อ 3): ข้อความบอกให้แจ้งพนักงาน → พนักงานคีย์แทนผ่าน US-30

### 2.2 เมนูและตะกร้า

| Method | Path | ผู้เรียก | Input | Output | หมายเหตุ |
|---|---|---|---|---|---|
| `GET` | `/api/v1/menu` | guest/staff | — | หมวดหมู่ + สินค้า + option group ที่ผูกกับแต่ละสินค้า + `is_available` | cache ได้ (ISR) revalidate ทันทีที่แอดมินแก้ (US-23 AC) · **ซ่อน option group ที่ `hide_when_empty` และไม่มี value ที่ available เลย** (US-35 AC) |
| `GET` | `/api/v1/cart` | guest | — | ตะกร้าปัจจุบัน + ยอดรวม | dine-in = ตะกร้าของโต๊ะ (แชร์) · counter = ตะกร้าของ session |
| `POST` | `/api/v1/cart/items` | guest | `{product_id, qty, option_value_ids[]}` | `{cart_item, cart_total_satang}` | **atomic upsert** ดู §5.1 |
| `PATCH` | `/api/v1/cart/items/{id}` | guest | `{qty, expected_version}` | `{cart_item}` \| 409 | ตั้งจำนวนแบบระบุค่า (จากปุ่ม +/-) |
| `DELETE` | `/api/v1/cart/items/{id}` | guest | — | 204 | idempotent — ลบซ้ำก็คืน 204 |

**กฎ authorization:** ทุก endpoint ตรวจว่า `cart_id` ที่ถูกแตะ เป็นของ `tsid`/`sid` ใน token เท่านั้น — ห้ามรับ `cart_id` จาก body

### 2.3 ยืนยันออเดอร์และติดตามสถานะ

| Method | Path | ผู้เรียก | Input | Output |
|---|---|---|---|---|
| `POST` | `/api/v1/orders` | guest | header `Idempotency-Key` · body `{}` (ยืนยันทั้งตะกร้า) | `201 {order, rejected_items[], payment_instruction}` |
| `GET` | `/api/v1/orders` | guest | — | ออเดอร์ทุกรอบของ session/โต๊ะ + สถานะปัจจุบัน (US-05, US-06) |
| `GET` | `/api/v1/bill/summary` | guest | — | ทุกออเดอร์ของรอบนี้ + ยอดรวมสุทธิ + ข้อความว่าต้องจ่ายที่ไหน (US-07) |

**`payment_instruction` ในผลลัพธ์ — บังคับให้ต่างกันตามช่องทาง (UX-07 / UX-08):**

```jsonc
// dine-in (BR ข้อ 3)
{ "kind": "pay_later_at_counter",
  "message_th": "ส่งออเดอร์เข้าครัวแล้ว ชำระเงินที่เคาน์เตอร์ตอนจะกลับได้เลย" }

// takeaway (BR ข้อ 12) — ต้องไม่ทำให้เข้าใจผิดว่าออเดอร์เข้าครัวแล้ว
{ "kind": "prepay_required",
  "message_th": "กรุณาชำระเงินที่เคาน์เตอร์ก่อน ทางร้านจะเริ่มทำเครื่องดื่มหลังได้รับเงินแล้ว" }
```
UX-08 ตั้งเกณฑ์ ≥95% ของผู้ทดสอบต้องเข้าใจว่ายังไม่เข้าครัว — ข้อความนี้จึงเป็นส่วนหนึ่งของ API contract ไม่ใช่ copy ที่ frontend คิดเอง เพื่อให้ทุกจอพูดตรงกัน

---

## 3. Endpoint ฝั่งพนักงาน (staff)

| Method | Path | Input | Output / ผล | US |
|---|---|---|---|---|
| `GET` | `/api/v1/staff/orders` | `?status=&channel=` | คิวออเดอร์ที่ยังไม่จบ + `placed_at` + `status_changed_at` + ป้าย channel/origin | US-13, UX-10 |
| `POST` | `/api/v1/staff/orders/{id}/status` | `{expected_status, to_status}` | 200 `{order}` \| 409 | US-14 · §5.4 |
| `POST` | `/api/v1/staff/orders/{id}/cancel` | `{reason}` **บังคับ** | 200 · เขียน `order_status_event` | US-20 · BR ข้อ 5 |
| `POST` | `/api/v1/staff/order-items/{id}/cancel` | `{reason}` **บังคับ** | 200 · คำนวณยอดบิลใหม่ทันที | US-20 |
| `POST` | `/api/v1/staff/orders/{id}/handover` | — | `ready → completed` (เฉพาะ channel=counter) | US-30 "รอเสิร์ฟ" → ส่งมอบ |
| `POST` | `/api/v1/staff/products/{id}/availability` | `{is_available}` | 200 · เมนูลูกค้าอัปเดตทันทีผ่าน realtime | US-16 |
| `POST` | `/api/v1/staff/option-values/{id}/availability` | `{is_available}` | 200 | US-36 · BR ข้อ 4 (ระดับตัวเลือก) |
| `GET` | `/api/v1/staff/tables` | — | โต๊ะทั้งหมด + สถานะจาก `table_status_v` + ยอดค้างต่อโต๊ะ | US-18 · BR ข้อ 11 |
| `GET` | `/api/v1/staff/bills/{id}` | — | ทุกออเดอร์ของบิล + ยอดรวมสุทธิ | US-18 |
| `POST` | `/api/v1/staff/bills/{id}/close` | `{expected_total_satang, method, force?}` | 200 · ปิดบิล + ปิด visit_session + โต๊ะกลับเป็นว่าง \| 409 | US-19 · §5.3 |
| `POST` | `/api/v1/staff/bills/{id}/payment` | `Idempotency-Key` · `{method, amount_satang}` | 200 · counter: `awaiting_payment → queued` | US-29 · §5.5 |
| `POST` | `/api/v1/staff/counter-orders` | `Idempotency-Key` · `{items[], method, amount_satang}` | `201 {order}` สถานะ `queued` ทันที | US-30 · §4.2 |

**หมายเหตุ US-19 (`close`):** ไม่มี endpoint ใดในระบบที่เขียนสถานะโต๊ะได้ — โต๊ะกลับเป็น "ว่าง" เป็น **ผลข้างเคียง**ของการปิด `visit_session` ในทรานแซกชันนี้เท่านั้น (BR ข้อ 11)

**หมายเหตุ US-30 (`counter-orders`):** สร้างออเดอร์ + `payment` + เลื่อนสถานะเป็น `queued` **ในทรานแซกชันเดียว** ตาม AC ที่ระบุว่ารับเงินเป็นส่วนหนึ่งของขั้นตอนเดียวกัน ไม่ใช่ 2 ขั้นแบบ US-28/US-29 · แคชเชียร์เรียกซ้ำต่อเนื่องได้ (คิว walk-in) โดยแต่ละครั้งเป็นคนละ `Idempotency-Key` → ออเดอร์แยกกันไม่ปน

---

## 4. Endpoint ฝั่งแอดมิน (admin)

| Method | Path | หมายเหตุ | US |
|---|---|---|---|
| `POST/PATCH` | `/api/v1/admin/categories[/{id}]` | soft delete เท่านั้น (`DELETE` = set `deleted_at`) | US-23 |
| `POST/PATCH` | `/api/v1/admin/products[/{id}]` | แก้แล้วมีผลกับเมนูลูกค้าทันที (revalidate cache) | US-23 |
| `POST/PATCH` | `/api/v1/admin/option-groups[/{id}]` | ตั้ง `default_option_value_id`, `source_type`, `hide_when_empty` | US-35, US-43 |
| `POST/PATCH` | `/api/v1/admin/option-values[/{id}]` | เพิ่ม/แก้/ลบเมล็ดพิเศษใช้ endpoint ชุดนี้ **ไม่มีระบบจัดการแยก** | US-36 |
| `PUT` | `/api/v1/admin/products/{id}/option-groups` | ผูก/ถอดกลุ่มตัวเลือกของสินค้ารายตัว | US-43 AC ข้อ 4 |
| `POST` | `/api/v1/admin/tables` | สร้างโต๊ะ **+ สร้าง QR ในทรานแซกชันเดียวกัน** | US-42 + US-24 |
| `PATCH` | `/api/v1/admin/tables/{id}` | แก้ `display_name` / `zone_id` / `sort_order` — **ไม่แตะ `id` และไม่แตะ QR** | US-42 |
| `POST` | `/api/v1/admin/tables/{id}/retire` | soft delete · 409 ถ้ามีบิลเปิดค้าง | US-42 · §5.6 |
| `GET` | `/api/v1/admin/tables/{id}/qr.png` | เรนเดอร์ QR จาก `qr_code.code` ตอนดาวน์โหลด | US-24 |
| `POST/PATCH` | `/api/v1/admin/zones[/{id}]` | โซนของผังอย่างง่าย | US-42 |

🔴 **ไม่มี endpoint `POST /tables/{id}/qr/regenerate`** — ตั้งใจไม่มี ตาม BR ข้อ 10 (QR static ตลอดอายุร้าน) การมี endpoint นี้คือการเปิดช่องให้ QR ที่พิมพ์ติดโต๊ะไปแล้วพังโดยไม่ตั้งใจ

🔴 **ไม่มี endpoint ที่เขียนสถานะโต๊ะ** — ตาม BR ข้อ 11

---

## 5. จุดที่ต้องจัดการ concurrency / race condition โดยเฉพาะ

หัวข้อนี้คือแกนหลักของเอกสาร — 6 จุดนี้คือที่ที่ระบบจะพังเงียบ ๆ ถ้าออกแบบผิด

### 5.1 หลายคนเพิ่มของเข้าตะกร้าโต๊ะเดียวกันพร้อมกัน (BR ข้อ 2 · UX-06)

**ปัญหา:** ถ้า API เป็น `PUT /cart` ที่รับตะกร้าทั้งใบ อุปกรณ์ B จะเขียนทับของที่อุปกรณ์ A เพิ่งเพิ่ม → รายการหาย = ทำเครื่องดื่มขาดที่หน้าร้าน

**การออกแบบ:**
1. **ไม่มี endpoint ที่เขียนตะกร้าทั้งใบ** — มีเฉพาะ `POST /cart/items`, `PATCH /cart/items/{id}`, `DELETE /cart/items/{id}`
2. การเพิ่มของเป็น **operation ที่สลับลำดับกันได้ (commutative)**:
```sql
INSERT INTO cart_item (cart_id, product_id, qty, line_signature, added_by_session_id)
VALUES ($1, $2, $3, $4, $5)
ON CONFLICT (cart_id, line_signature)
DO UPDATE SET qty = cart_item.qty + EXCLUDED.qty,
              version = cart_item.version + 1,
              updated_at = now()
RETURNING *;
```
   สองเครื่องกด "ลาเต้เย็น หวาน 50%" พร้อมกัน → ได้ qty=2 เสมอ ไม่มี lost update และไม่ต้องล็อกอะไร
3. **การตั้งจำนวนแบบระบุค่า** (ปุ่ม +/- ที่ส่งค่าใหม่) เป็น operation ที่ไม่ commutative → ใช้ optimistic concurrency:
```sql
UPDATE cart_item SET qty=$1, version=version+1
WHERE id=$2 AND version=$3;   -- 0 rows → 409
```
   → `409 CART_ITEM_VERSION_CONFLICT` พร้อมค่าปัจจุบัน → client รีเฟรชแล้วให้ผู้ใช้เห็นค่าจริง **ห้าม retry อัตโนมัติเงียบ ๆ** เพราะเจตนาของผู้ใช้อาจเปลี่ยนไปแล้ว
4. **ลบรายการ** idempotent — ลบสิ่งที่ถูกลบไปแล้วคืน 204 ไม่ใช่ 404 (สองคนกดลบพร้อมกันไม่ควรเห็น error)
5. ทุกการเปลี่ยนแปลง broadcast ผ่าน realtime → อุปกรณ์อื่นในโต๊ะเห็นภายใน ≤5 วิ (UX-06)

> **ประเด็นที่ยังต้องให้ Touch ตัดสิน:** ตะกร้าแชร์แปลว่า **ใครก็ลบรายการของคนอื่นได้** — เป็นผลตรงจาก BR ข้อ 2 (ตะกร้าต่อโต๊ะ ไม่ใช่ต่อคน) ค่าที่ใช้ไปก่อนคือ แสดงป้าย "เพิ่มโดยอุปกรณ์อื่น" (ไม่ระบุตัวตน ตาม BR ข้อ 14) เพื่อลดการลบผิด แต่ไม่บล็อก

### 5.2 ยืนยันออเดอร์ชนกับการมาร์กของหมด (BR ข้อ 4) 🔴

**กฎที่ห้ามผิด: reject เฉพาะรายการนั้น ไม่ปฏิเสธทั้งออเดอร์** และต้องครอบคลุม **ทั้งระดับสินค้าและระดับ option value** (เมล็ดพิเศษหมด)

**ลำดับใน `POST /api/v1/orders` — ทรานแซกชันเดียว:**
1. `SELECT ... FOR UPDATE` บน `visit_session` (กันชนกับการปิดบิล — §5.3)
2. ตรวจ `Idempotency-Key` ซ้ำ → ถ้าเคยสำเร็จแล้ว คืนผลเดิม (กัน double-submit ตาม UX §5)
3. อ่าน `cart_item` ทั้งหมด แล้ว **ตรวจ availability ใหม่ ณ วินาทีนี้** (ไม่เชื่อค่าที่ client เห็นตอนกดเพิ่มลงตะกร้า):
   - `product.is_available = false` → รายการนั้น `rejected_unavailable`
   - มี `option_value.is_available = false` อยู่ในรายการนั้น → รายการนั้น `rejected_unavailable`
4. ถ้ามีรายการที่ผ่านอย่างน้อย 1 → สร้าง `orders` + `order_item` (snapshot ชื่อ/ราคา/ตัวเลือก) และเปิด `visit_session` ถ้ายังไม่มี (BR ข้อ 11)
5. ถ้า **ทุกรายการถูก reject** → ไม่สร้างออเดอร์ คืน `409 ALL_ITEMS_UNAVAILABLE`
6. ล้าง cart_item ที่ถูกส่งไปแล้ว **แต่คงรายการที่ถูก reject ไว้ในตะกร้า** เพื่อให้ลูกค้าเห็นว่าอะไรไม่ผ่านและเลือกใหม่ได้ทันที

**Response (บางส่วนสำเร็จ) — HTTP `201` ไม่ใช่ error:**
```jsonc
{
  "order": { "id": "…", "sequence_no": 2, "status": "queued", "placed_at": "…" },
  "accepted_items": [ { "name": "อเมริกาโน่ (เย็น)", "qty": 1 } ],
  "rejected_items": [
    { "name": "ลาเต้ (เย็น)", "qty": 1,
      "reason_code": "PRODUCT_UNAVAILABLE",
      "message_th": "ลาเต้ (เย็น) เพิ่งหมดพอดี จึงไม่ได้ส่งเข้าครัว" },
    { "name": "ดริป — เอธิโอเปีย เยิร์กาเชฟ", "qty": 1,
      "reason_code": "OPTION_UNAVAILABLE",
      "message_th": "เมล็ดเอธิโอเปีย เยิร์กาเชฟ หมดพอดี รายการนี้จึงไม่ได้ส่งเข้าครัว" }
  ],
  "partial": true,
  "payment_instruction": { "kind": "pay_later_at_counter", "message_th": "…" }
}
```
**เหตุผลที่คืน 201 ไม่ใช่ 207/409:** ออเดอร์ถูกสร้างสำเร็จจริง การใช้ status code ที่เป็น error จะทำให้ client library ทั่วไปตีความว่าล้มเหลวแล้วอาจ retry → สั่งซ้ำ · client อ่าน `partial` เพื่อแสดง UI แจ้งเตือน

### 5.3 ปิดบิลชนกับการสั่งเพิ่ม (US-19 vs US-06) 🔴 **ความเสียหายเป็นเงินจริง**

**ปัญหา:** แคชเชียร์เปิดหน้าสรุปยอดโต๊ะ 5 เห็น 250 บาท · ระหว่างนั้นลูกค้ากดสั่งลาเต้เพิ่ม · แคชเชียร์กดปิดบิล → **เก็บเงินขาด 70 บาท และออเดอร์ที่เพิ่งสั่งกลายเป็นออเดอร์ของบิลที่ปิดไปแล้ว**

**การออกแบบ — ทั้งสอง path ล็อกแถวเดียวกัน:**
```sql
-- ทั้ง POST /orders และ POST /bills/{id}/close เริ่มด้วยบรรทัดนี้
SELECT * FROM visit_session WHERE id = $1 FOR UPDATE;
```
| ใครชนะ | ผลของอีกฝ่าย |
|---|---|
| **ปิดบิลชนะ** | `POST /orders` คืน `409 SESSION_CLOSED` · `message_th`: "บิลของโต๊ะนี้ถูกปิดไปแล้ว หากต้องการสั่งเพิ่ม กรุณาแจ้งพนักงาน" · **รายการในตะกร้าไม่ถูกลบทิ้ง** (UX §5 แถวเน็ตหลุด: ห้ามทำให้ตะกร้าหาย) |
| **สั่งเพิ่มชนะ** | `close` คืน `409 BILL_CHANGED` พร้อม `{ current_total_satang, new_orders[] }` → หน้าจอแคชเชียร์แสดงยอดใหม่ + รายการที่เพิ่งเข้ามา และให้กดยืนยันอีกครั้ง |

`POST /bills/{id}/close` จึง **บังคับส่ง `expected_total_satang`** — เป็นการยืนยันว่า "ฉันกำลังจะเก็บเงินตามยอดที่ฉันเห็นอยู่" ถ้ายอดจริงเปลี่ยนไปแล้วระบบต้องไม่ยอมปิดเงียบ ๆ

`force: true` มีไว้สำหรับกรณีตามหัวข้อ 8 ข้อ 2 (ปิดบิลทั้งที่ยังมีออเดอร์ค้างทำ) **ไม่ใช่** สำหรับข้ามการตรวจยอด — ยอดไม่ตรงต้องกดยืนยันใหม่เสมอ

### 5.4 พนักงาน 2 เครื่องกดเปลี่ยนสถานะออเดอร์เดียวกัน (US-14)

```sql
UPDATE orders SET status=$1, status_changed_at=now()
WHERE id=$2 AND status=$3;   -- $3 = expected_status
```
| ผล | การตอบกลับ |
|---|---|
| 1 row | 200 + เขียน `order_status_event` |
| 0 row แต่สถานะปัจจุบัน = `to_status` แล้ว | **200 (no-op)** — สองคนกด "เสร็จแล้ว" พร้อมกันไม่ควรเห็น error ในสภาพหน้าร้านจริง |
| 0 row และสถานะไปไกลกว่า/ผิด transition | `409 ORDER_STATUS_CONFLICT` + สถานะปัจจุบัน · `message_th`: "ออเดอร์นี้ถูกอัปเดตเป็น 'เสร็จแล้ว' โดยอีกเครื่องหนึ่ง" |

transition ที่ผิดกฎตาม [[data-model-v1|Data Model v1]] §4.1 คืน `422 ILLEGAL_TRANSITION` (ไม่ใช่ 409 — เป็นคนละเรื่อง: 409 = แข่งกัน, 422 = ขอสิ่งที่ผิดกฎ)

### 5.5 ยืนยันรับเงินซ้ำ / กดปุ่มรัวตอนยุ่ง (US-29)

- `Idempotency-Key` บังคับ → กดซ้ำภายใน key เดิมคืนผลเดิม ไม่สร้าง `payment` แถวที่สอง
- conditional update: `UPDATE bill SET paid_at=now(), status='paid' WHERE id=$1 AND status='awaiting_payment'` → 0 row + จ่ายแล้ว = 200 no-op · 0 row + บิล voided = `409 BILL_VOIDED`
- ออเดอร์เลื่อนไป `queued` **ในทรานแซกชันเดียวกับการบันทึก payment** — ห้ามแยกเป็น 2 request เพราะถ้า request ที่สองล้ม ลูกค้าจ่ายเงินแล้วแต่ออเดอร์ไม่เข้าคิว (INV-3)

### 5.6 ปลดระวางโต๊ะชนกับบิลที่เปิดค้าง (US-42)

```sql
UPDATE service_point SET retired_at = now()
WHERE id = $1
  AND retired_at IS NULL
  AND NOT EXISTS (
    SELECT 1 FROM visit_session
    WHERE table_id = $1 AND status = 'open');
```
0 row → `409 TABLE_HAS_OPEN_BILL` · `message_th`: "โต๊ะนี้ยังมีบิลที่เปิดค้างอยู่ กรุณาปิดบิลก่อนจึงจะปลดระวางได้" (US-42 AC)

การแก้ `display_name` ใช้กฎเดียวกันหรือไม่? **ไม่** — US-42 AC บอกว่า "ห้ามลบหรือแก้ไขโต๊ะที่ยังมีบิลเปิดค้าง" แต่การแก้ชื่อระหว่างมีลูกค้านั่งอยู่ไม่ทำให้ข้อมูลเสียหาย (QR ผูกกับ id) ค่าที่ใช้ไปก่อนคือ **อนุญาตให้แก้ชื่อได้เสมอ แต่บล็อกการปลดระวาง** — ดูหัวข้อ 8 ข้อ 3

---

## 6. Realtime (ไม่ใช่ REST แต่เป็นส่วนหนึ่งของ contract)

| ช่อง | ผู้ subscribe | เนื้อหา | US/UX |
|---|---|---|---|
| `cart:{visit_session_id}` | guest (dine-in) | `cart_item` เปลี่ยน | UX-06 ≤5 วิ |
| `orders:{visit_session_id}` / `orders:{customer_session_id}` | guest | `orders.status` เปลี่ยน | US-05, UX-04 ≤5 วิ |
| `station:orders` | staff | ออเดอร์ใหม่ + สถานะเปลี่ยน + ออเดอร์ `awaiting_payment` | US-13, US-15 |
| `menu:availability` | ทุกคน | `product.is_available`, `option_value.is_available` | US-16, US-36 |

**บังคับสำหรับทุก client (จาก [[architecture-v1|Architecture v1]] §3.3):** ถ้าไม่ได้รับ event หรือ connection ไม่อยู่ในสถานะ `SUBSCRIBED` เกิน 10 วินาที → สลับไป polling `GET` ทุก 5 วินาทีอัตโนมัติ **และแสดงป้ายบอกผู้ใช้** ห้าม degrade เงียบ ๆ (จอสถานีคือ single point of failure ตาม persona P4)

---

## 7. Error Contract — จับคู่กับ UX Requirements หัวข้อ 5

| กรณีใน UX §5 | HTTP | `code` | `message_th` (ตัวอย่าง) | `next_action` |
|---|---|---|---|---|
| สแกน QR ไม่ติด/ไม่ทำงาน | 404/410 | `QR_NOT_FOUND` \| `QR_INACTIVE` \| `TABLE_RETIRED` | "ไม่พบข้อมูลโต๊ะจาก QR นี้" | "แจ้งพนักงานเพื่อสั่งอาหารได้เลย" (fallback US-30) |
| เมนูสินค้าหมด | 200 | — | สินค้าแสดง label "หมดชั่วคราว" ปุ่มปิดใช้งาน **ไม่ซ่อนหาย** | "เลือกเมนูอื่นได้ตามปกติ" |
| ตัวเลือกหมด (เมล็ดพิเศษ) | 200 | — | ตัวเลือกนั้นปิด · ถ้าไม่เหลือเลย **ซ่อนทั้งกลุ่ม** (US-35 AC) | — |
| ร้านปิดรับออเดอร์ | 200 | `SHOP_CLOSED` | "ร้านปิดรับออเดอร์แล้ว" แทนทั้งหน้าเมนู | ไม่มีปุ่มสั่ง |
| ตะกร้าว่าง | 200 | — | empty state ไม่ใช่หน้าเปล่า | ปุ่มกลับไปหน้าเมนู |
| เน็ตหลุดกลางกดยืนยัน | — | (client-side) | "การเชื่อมต่อขาดหาย **ยังไม่ได้ส่งออเดอร์**" | ปุ่มลองส่งใหม่ · **ตะกร้าต้องไม่หาย** · retry ใช้ `Idempotency-Key` เดิม |
| กดยืนยันซ้ำ (double-submit) | 200 | — | คืนผลเดิมจาก idempotency ไม่สร้างออเดอร์ซ้ำ | client ปิดปุ่มทันทีหลังกดครั้งแรก |
| ของหมดตอนกดยืนยันพอดี | **201** | `partial: true` + `rejected_items[]` | "ลาเต้ (เย็น) เพิ่งหมดพอดี รายการอื่นส่งเรียบร้อยแล้ว" | "เลือกเครื่องดื่มอื่นแทน หรือกดเรียกพนักงาน" |
| ของหมดทุกรายการ | 409 | `ALL_ITEMS_UNAVAILABLE` | "รายการที่เลือกไว้หมดทั้งหมดพอดี ยังไม่ได้ส่งออเดอร์" | "เลือกเมนูใหม่ หรือแจ้งพนักงาน" |
| จ่ายเงินไม่สำเร็จ (เคาน์เตอร์) | 200 | — | ออเดอร์ค้าง `awaiting_payment` **ไม่เข้าครัว** | แคชเชียร์ยกเลิกด้วย US-20 |
| สั่งเพิ่มหลังบิลปิด | 409 | `SESSION_CLOSED` | "บิลของโต๊ะนี้ถูกปิดไปแล้ว" | "แจ้งพนักงานเพื่อเปิดรอบใหม่" |
| ปิดบิลแต่ยอดเปลี่ยน | 409 | `BILL_CHANGED` | "มีออเดอร์เข้ามาใหม่ ยอดรวมเปลี่ยนเป็น X บาท" | "ตรวจสอบรายการใหม่แล้วกดยืนยันอีกครั้ง" |
| ตั้งจำนวนชนกัน | 409 | `CART_ITEM_VERSION_CONFLICT` | "มีคนในโต๊ะแก้รายการนี้พอดี" | "ตรวจจำนวนล่าสุดแล้วลองใหม่" |
| เปลี่ยนสถานะชนกัน | 409 | `ORDER_STATUS_CONFLICT` | "ออเดอร์นี้ถูกอัปเดตโดยอีกเครื่องหนึ่งแล้ว" | — |
| ปลดระวางโต๊ะที่มีบิลค้าง | 409 | `TABLE_HAS_OPEN_BILL` | "โต๊ะนี้ยังมีบิลเปิดค้างอยู่" | "ปิดบิลก่อนจึงจะปลดระวางได้" |
| ลูกค้าพยายามยกเลิกออเดอร์เอง | 403 | `FORBIDDEN_FOR_GUEST` | "การยกเลิกต้องทำผ่านพนักงาน" (BR ข้อ 5) | "กดเรียกพนักงาน" |

**กฎการเขียนข้อความ (UX §6):** ห้ามใช้คำว่า session / checkout / submit / error code ในข้อความที่ลูกค้าเห็น · ทุก error ต้องมี `next_action` เสมอ — ห้ามมีหน้าจอที่บอกแค่ว่าผิดพลาดแล้วจบ

---

## 8. ประเด็นที่ต้องกลับไปถาม XAVIER/Touch

| # | ประเด็น | ทำไมถึงตอบเองไม่ได้ | ค่าที่ใช้ไปก่อน |
|---|---|---|---|
| 1 | **ตะกร้าแชร์ = ใครก็ลบรายการของคนอื่นได้** — BR ข้อ 2 บอกว่าแชร์ตะกร้าต่อโต๊ะ แต่ไม่ได้บอกว่าลบของคนอื่นได้ไหม | เป็นการตัดสินใจเชิงประสบการณ์ ไม่ใช่เชิงเทคนิค | ลบได้ทุกคน + แสดงป้าย "เพิ่มโดยอุปกรณ์อื่น" (ไม่ระบุตัวตน ตาม BR ข้อ 14) |
| 2 | **ปิดบิลตอนยังมีเครื่องดื่มค้างทำ** ต้องบล็อกหรือแค่เตือน (ซ้ำกับ [[architecture-v1|Architecture v1]] §8 ข้อ 5) | กระทบทั้ง flow เงินและลำดับงานหน้าร้าน | เตือน + ต้องส่ง `force: true` ยืนยันอีกชั้น · ออเดอร์ที่ค้าง auto-complete |
| 3 | **แก้ชื่อโต๊ะระหว่างมีบิลเปิดค้างได้ไหม** — US-42 AC เขียนรวมว่า "ห้ามลบหรือแก้ไขโต๊ะที่มีบิลเปิดค้าง" แต่การแก้ชื่อไม่ทำให้ข้อมูลเสียหายเลย (QR ผูกกับ id) | ต้องรู้ว่า AC ตั้งใจครอบคลุมการแก้ชื่อด้วยจริงหรือหมายถึงการปลดระวางเป็นหลัก | อนุญาตแก้ชื่อ · บล็อกเฉพาะการปลดระวาง — **ถ้า XAVIER ยืนยันว่าต้องบล็อกทั้งคู่ เปลี่ยนได้ในบรรทัดเดียว** |
| 4 | **rate limit ของ guest** — QR ทางกายภาพคือ credential (ความเสี่ยง R6) ใครถ่ายรูป QR ไปก็สั่งของเข้าโต๊ะคนอื่นได้ | เกณฑ์ที่เหมาะสมขึ้นกับปริมาณลูกค้าจริงของร้านซึ่งยังไม่เปิด | จำกัด ~30 คำขอเขียน/นาที/session · ยืนยันออเดอร์ ~5 ครั้ง/นาที/session · เกินแล้วคืน 429 พร้อมข้อความสุภาพ ไม่ล็อกถาวร |
| 5 | **ต้องมี endpoint ให้พนักงานคีย์ออเดอร์ dine-in แทนลูกค้าไหม** — US-30 ครอบคลุมเฉพาะช่องทางเคาน์เตอร์ แต่ UX principle ข้อ 3 + persona P3 (ป้าน้อย) บอกว่าทุก flow ต้องมีทางออกให้พนักงานช่วย ซึ่งฝั่งโต๊ะยังไม่มี | เป็นการเพิ่มสโคปเกิน backlog — ต้องให้ XAVIER เปิด story ใหม่ ไม่ใช่ COULSON เพิ่มเอง | **ไม่ทำใน Phase 0** ตามสโคปที่ backlog กำหนด · fallback ปัจจุบันคือพนักงานเดินไปกดบนมือถือของลูกค้า/สั่งผ่านช่องทางเคาน์เตอร์แทน — **flag ไว้ว่าเป็นช่องว่างจริงของ journey J3** |

---

ส่งงาน — COULSON → ทัช (งาน / ผลลัพธ์ / ค้าง-เสี่ยง / skill ที่ใช้)

**งาน:** ออกแบบ API contract ของ Phase 0 แยกตาม 3 surface พร้อมกฎ authorization, การจัดการ race condition ที่กระทบเงินและออเดอร์โดยตรง และ error contract ที่ตรงกับ UX Requirements หัวข้อ 5

**ผลลัพธ์:** `docs/02-design/02-technical/api-design-v1.md` — endpoint ครบทั้ง guest / staff / admin พร้อม input-output-สิทธิ์, **6 จุด race condition ที่ออกแบบวิธีแก้ไว้เป็นรูปธรรมระดับ SQL** (ตะกร้าแชร์แบบ commutative upsert, ยืนยันออเดอร์ชนของหมดที่ reject รายรายการ, ปิดบิลชนสั่งเพิ่มด้วย `expected_total` + row lock, เปลี่ยนสถานะชนกัน, ยืนยันรับเงินซ้ำ, ปลดระวางโต๊ะชนบิลเปิด), ช่อง realtime 4 ช่องพร้อมกฎ fallback, และตาราง error contract 16 กรณีที่จับคู่กับ UX §5 ทีละแถวพร้อมข้อความไทยที่ไม่มีศัพท์เทคนิค

**ค้าง/เสี่ยง:** จุดที่เสี่ยงที่สุดคือ **§5.3 ปิดบิลชนกับการสั่งเพิ่ม** เพราะพลาดแล้วคือเก็บเงินขาดจริง — วิธีแก้คือบังคับให้แคชเชียร์ส่ง `expected_total_satang` มาด้วยทุกครั้ง ยอดไม่ตรงคือ 409 พร้อมรายการใหม่ ห้ามปิดเงียบ ๆ · จุดที่สองคือ **§5.2 ต้องคืน HTTP 201 ไม่ใช่ error เมื่อสำเร็จบางส่วน** เพราะถ้าใช้ status code ที่เป็น error client อาจ retry แล้วเกิดออเดอร์ซ้ำ · **5 ประเด็นที่ต้องกลับไปถาม** โดยข้อที่ควรให้ XAVIER ดูเป็นอันดับแรกคือข้อ 5: UX principle ข้อ 3 และ persona ป้าน้อยเรียกร้องว่าทุก flow ต้องมีทางให้พนักงานช่วยสั่งแทน แต่ **backlog มี US-30 เฉพาะช่องทางเคาน์เตอร์ ไม่มีของช่องทางโต๊ะ** — เป็นช่องว่างจริงของ journey J3 ที่ COULSON ไม่ควรอุดเองด้วยการเพิ่มสโคป

**skill ที่ใช้:** scrutinize (ไล่หา seam ที่สองคนทำงานพร้อมกันแล้วเงินหรือออเดอร์จะเพี้ยน แทนที่จะไล่แค่รายการ endpoint — เป็นที่มาของหัวข้อ 5 ทั้งหมด และของการเลือก HTTP status ที่ไม่ทำให้ client retry จนเกิดออเดอร์ซ้ำ), management-talk (เขียน error contract เป็นข้อความที่ลูกค้าอ่านเข้าใจจริงตาม UX §6 ไม่ใช่ code ดิบ และแยกประเด็นที่ต้องให้ Touch/XAVIER ตัดสินออกจาก default ที่เดินงานต่อได้)
