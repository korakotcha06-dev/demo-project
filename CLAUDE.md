# CLAUDE.md

ไฟล์นี้ให้คำแนะนำแก่ Claude Code (claude.ai/code) เมื่อทำงานกับโค้ดในโปรเจกต์นี้

## สถานะโปรเจกต์

**repo นี้ยังเป็น Obsidian vault สำหรับเอกสารล้วน** ไม่มี `package.json`, build tool, linter หรือ test runner — อย่าสมมติหรือคิดคำสั่ง build/lint/test ขึ้นเองสำหรับ repo นี้

🔴 **โค้ดแอปพลิเคชันมีอยู่แล้วตั้งแต่ 2026-08-22 แต่อยู่ใน repo แยก:**

- GitHub: <https://github.com/korakotcha06-dev/qr-order-app> (private)
- local: `/Users/korakotchangpan/Documents/ADT-AI/Classwork/qr-order-app`
- 🔴 **branch: `feat/unified-shell` — ยังไม่ merge เข้า `main`** (2026-08-23)
  งานทั้งหมดของวันที่ 2026-08-23 อยู่บน branch นี้ · ใครเปิด `main` จะไม่เห็นอะไรเลย
  (เปลือกเดียวรวมพนักงาน+แอดมิน · รวมหน้าเมนู/หมวด/ตัวเลือก · ป้าย QR · พร้อมเพย์ · ฯลฯ)

**vault เอกสารนี้เองก็อยู่บน branch เหมือนกัน** — `claude/app-web-design-phase-6178f6`
ที่ <https://github.com/korakotcha06-dev/demo-project.git> ไม่ใช่ `main`

🔴 **การแยกสองรีโปเป็นการตัดสินใจที่ Touch เคาะแล้ว (2026-08-23) — อย่าเสนอให้รวมอีก**
เหตุผลและตัวเลขที่ใช้ตัดสินอยู่ใน `docs/05-log/changelog.md` วันที่ 2026-08-23
สรุป: vault เป็นงานส่งของ bootcamp ที่ถูกตรวจ และประกาศตัวเองว่าเป็นเอกสารล้วน
เอาโค้ดที่ต้อง deploy มาปนจะพังทั้งสองฝั่ง · ต้นทุนคือ commit สองที่ ซึ่งยอมรับแล้ว

คำสั่ง build/test/dev ทั้งหมดอยู่ใน `CLAUDE.md` ของ repo นั้น (`pnpm dev:all`, `pnpm migrate`, `pnpm seed`, `pnpm test`, `pnpm check:invariants`) · **เอกสารใน `docs/` ของ vault นี้ยังเป็น source of truth ของโค้ดนั้นอยู่** — โค้ดขัดกับเอกสารเมื่อไหร่ให้ทำตามเอกสาร แล้วบันทึกเหตุผลไว้ใน `docs/05-log/changelog.md`

สิ่งที่ build ไปแล้ว: schema เต็ม (24 ตาราง, INV-1..INV-10, RLS) + เส้นทาง dine-in (J1) ครบวง + NFR-11 PIN lock + หน้าจอแอดมิน A-00..A-07 (A-02+A-03+A-04+A-05 รวมเป็น `/admin/menu` · A-06+A-07 รวมเป็น `/admin/tables`) + **ช่องทางเคาน์เตอร์ (J2/J3) ครบวง** + **A-08 เปิด/ปิด VAT ได้เองเมื่อจดทะเบียน** = **24 หน้าจอ** (23 ตามเอกสาร + A-08) — งานที่เหลือของ Phase 0 คือ deploy (R13/R14/R15) และการวัด NFR ที่ build ไปแล้ว · รายละเอียดพร้อมช่องว่างของเอกสารที่เจอตอนลงมือ อยู่ในบันทึก changelog วันที่ 2026-08-22

## โจทย์ของโปรเจกต์ (Product brief)

ผู้ประกอบการที่เป็นเจ้าของโปรเจกต์นี้กำลังจะเปิดร้านกาแฟ และต้องการ **ระบบสั่งอาหาร/เครื่องดื่มด้วย QR code**: ลูกค้าสแกน QR code ที่โต๊ะแล้วสั่งเองได้โดยไม่ต้องให้พนักงานมารับออเดอร์ นี่คือโจทย์ตั้งต้นที่อยู่เบื้องหลัง `docs/01-requirements` — ให้ถือว่าเป็นต้นทาง (source of truth) เวลาเขียนสเปค แผนงาน หรืองานย่อยในโฟลเดอร์นั้น เว้นแต่จะมีเอกสารในโฟลเดอร์นั้นที่เขียนทับความต้องการนี้ไว้แล้ว

## โครงสร้างเอกสาร (Documentation architecture)

โปรเจกต์นี้เป็น Obsidian vault (`.obsidian/`) ที่ใช้ pipeline แบบ SDLC ตายตัวภายใต้ `docs/` โดยผลลัพธ์ของแต่ละขั้นตอนจะถูกส่งต่อไปยังขั้นตอนถัดไป แต่ละโฟลเดอร์จะมี `index.md` ของตัวเองที่อธิบายจุดประสงค์และลิงก์ไปยังโฟลเดอร์ก่อนหน้า/ถัดไปด้วย Obsidian wikilink (`[[../path/index|label]]`) — **ห้ามทำลิงก์เหล่านี้ขาด และต้องอัปเดตทุกครั้งที่เพิ่มหรือย้ายเอกสาร**

ลำดับ pipeline:

1. **`01-requirements`** — จะสร้างอะไร
   - `01-spec` — ข้อกำหนดฟีเจอร์, user stories, กฎทางธุรกิจ, ขอบเขตงาน (ต้นทางของความต้องการ)
   - `02-plan` — roadmap, phase/milestone, ลำดับความสำคัญ
   - `03-task` — งานย่อยที่แตกออกมาจากแผนให้ลงมือทำได้จริง
2. **`02-design`** — หน้าตาเป็นอย่างไรและสร้างอย่างไร ต่อยอดจาก requirements
   - `01-prototypes` — wireframe/mockup, user flow, design system เบื้องต้น
   - `02-technical` — architecture, database schema, API design, การเลือกเทคโนโลยี/ไลบรารี
3. **`03-testing`** — การตรวจสอบ ต่อยอดจาก design
   - `01-test-plan` — test case/scenario, test data, ขอบเขตการทดสอบ
   - `02-test-result` — ผล pass/fail, บั๊กที่พบ, สถานะการแก้ไข
4. **`04-retrospectives`** — บทเรียนที่ได้แต่ละ phase/sprint โดยอ้างอิงจาก `03-testing/02-test-result` และ `05-log`
5. **`05-log`** — changelog และ decision log แบบเรียงตามลำดับเวลา ใช้อ้างอิงใน retrospectives
6. **`00-archived`** — เอกสารที่เลิกใช้แล้ว **ห้ามลบเอกสารทิ้งเด็ดขาด** — ให้ย้ายเวอร์ชันเก่าหรือแผนที่ยกเลิกมาเก็บไว้ที่นี่แทน เพื่อรักษาประวัติไว้

เมื่อจะเพิ่มเอกสารใหม่ ให้วางในโฟลเดอร์ที่ตรงกับขั้นตอนนั้น ๆ (ข้อมูลระดับสเปคให้ไปอยู่ใน `01-spec` ไม่ใช่ `02-plan` เป็นต้น) และทำตามการอ้างอิงต้นทาง/ปลายทางที่ประกาศไว้ใน `index.md` ของโฟลเดอร์นั้นอยู่แล้ว

## ข้อตกลงในการทำงาน (Conventions)

- เอกสารเขียนเป็นภาษาไทย ให้ใช้ภาษาเดียวกันเมื่อเพิ่มเนื้อหาในเอกสารที่มีอยู่
- ไฟล์ตั้งค่าเฉพาะของ Obsidian (`.obsidian/app.json`, `appearance.json`, `core-plugins.json`) เป็นการตั้งค่า vault ไม่ใช่การตั้งค่าแอปพลิเคชัน — อย่าไปแก้ไข เว้นแต่ผู้ใช้จะขอให้เปลี่ยนพฤติกรรมของ vault

## ทีม Agent สำหรับโปรเจกต์นี้

โปรเจกต์นี้อยู่ในสเตจ `01-requirements` ยังไม่มีโค้ด ทีม agent ที่ใช้ได้มีทั้งแบบ project-scoped (เฉพาะโปรเจกต์นี้) และแบบ global (ของบริษัท ใช้ได้ทุกโปรเจกต์):

| Agent | สเตจที่รับผิดชอบ | ที่อยู่ |
|-------|------------------|--------|
| **XAVIER** (เอ็กซาเวียร์) | `01-requirements` — วิเคราะห์ requirement, เขียน user story/business rule, จัดลำดับ product backlog (P0/P1/P2 + MoSCoW) | `.claude/agents/xavier.md` (project) |
| **PEGGY** (เพ็กกี้) | `01-requirements` — Feature List (feature → sub-feature → capability แม็ปกับ US ID) และ User Journey เป็น **Mermaid diagram** · ทำงานคู่กับ XAVIER แต่คนละมุม: XAVIER เขียน story/กฎ/ลำดับ · PEGGY ทำมุมมองลำดับชั้นและมุมมองเส้นทางของ persona | `.claude/agents/peggy.md` (project) |
| **VISION** (วิชั่น) | `02-design/02-technical` — **High-Level Architecture เชิง conceptual** (logical component, trust boundary, data flow ตาม user journey) **ห้ามผูกกับเทคโนโลยี/vendor ใด ๆ** · เป็น peer ของ COULSON ไม่ใช่ลูกทีม · ส่งต่อโมเดล conceptual ให้ COULSON เลือก stack จริง | `.claude/agents/vision.md` (project) |
| **COULSON** (โควสัน) | `02-design` — architecture ที่ผูกกับ stack จริง, DB schema, API design ต่อจาก backlog ที่ XAVIER ส่งมอบ **และ** conceptual model ที่ VISION ส่งมอบ | global |
| **SHURI** (ชูริ) | `02-design/01-prototypes` + frontend build (รายงานต่อ COULSON) | global |
| **BANNER** (แบนเนอร์) | backend/API/DB ของระบบสั่งอาหาร (รายงานต่อ COULSON) | global |
| **OKOYE** (โอโคเย) | `03-testing` — **Test Analyst & QA Lead** เจ้าของทั้ง `01-test-plan` (AC testability audit, test case, test data, RTM, UAT, เกณฑ์ผ่าน-ไม่ผ่าน) และ `02-test-result` (ผลจริง, bug log, GO/NO-GO) · ด่านสุดท้ายก่อนขึ้นจริง | `.claude/agents/okoye.md` (project — **override ตัว global**) |
| **JARVIS** (จาร์วิส) | ผู้ประสานงานข้ามทีมเมื่องานสเปน ≥2 แผนก | global |

ลำดับการส่งงาน: **XAVIER** + **PEGGY** ปิด requirements ใน `01-requirements` ก่อน → **VISION** ทำ conceptual High-Level Architecture (ไม่ผูก stack) → ส่งต่อ **COULSON** ทำ `02-design` ที่ผูกกับ stack จริง → ทีม SHURI/BANNER ทำตาม scope ที่ COULSON แตกให้ → **OKOYE** เป็นด่านสุดท้ายก่อนขึ้นจริง

**ข้อควรระวังเรื่องความเป็นเจ้าของเอกสาร:**

- **OKOYE ตัว project override ตัว global โดยตั้งใจ** — ตัว global เป็น pre-deploy web QA checklist runner สำหรับเว็บไซต์ลูกค้า TNM ซึ่งเป็นคนละบทบาทกับ test analyst ที่ทำงานในไปป์ไลน์เอกสารแบบนี้
- **AC เป็นของ XAVIER ไม่ใช่ OKOYE** — OKOYE เจอ AC ที่วัดผลไม่ได้ ให้เขียนเป็น *ข้อเสนอ* ลงหัวข้อ 6 ของ `01-spec/acceptance-criteria-v1.md` แล้วส่งคืน XAVIER/Touch เคาะ **ห้ามแก้เอง** (กติกาเดียวกับ PEGGY)
- 🔴 **agent global `design-syncer` ประกาศว่ารับงาน "สร้าง test plan / เขียน acceptance criteria" ด้วย — ชนกับ OKOYE และ XAVIER โดยตรง** · ในโปรเจกต์นี้ `03-testing` เป็นของ **OKOYE** และ AC เป็นของ **XAVIER** อย่าเรียก `design-syncer` มาทำสองชั้นนี้ ไม่งั้นจะมีสอง agent เขียนทับกัน
- **VISION กับ COULSON แบ่งกันด้วยระดับ ไม่ใช่ด้วยโฟลเดอร์** — ทั้งคู่เขียนลง `02-design/02-technical` แต่คนละไฟล์: VISION เขียนเฉพาะ `high-level-architecture-conceptual-*.md` (ห้ามมีชื่อเทคโนโลยี/vendor แม้แต่คำเดียว) ส่วน `architecture-v1.md` / `data-model-v1.md` / `api-design-v1.md` เป็นของ COULSON เท่านั้น **VISION ห้ามแก้ไฟล์ของ COULSON และ COULSON ห้ามแก้ไฟล์ของ VISION** — ถ้า COULSON เลือก stack ที่ขัดกับ capability ที่ VISION ระบุไว้ ต้อง flag กลับ ไม่ใช่แก้เอกสารของอีกฝ่ายเงียบ ๆ

## Skill ของโปรเจกต์นี้

| Skill | ใช้เมื่อไหร่ | ที่อยู่ |
|-------|-------------|--------|
| `/product-backlog` | มี requirement ใหม่ที่ต้องแตกเป็น **user story + acceptance criteria + business rule + ลำดับความสำคัญ** ก่อนส่งเข้า `01-spec` / `02-plan` / `03-task` | `.claude/skills/product-backlog/SKILL.md` |
| `/feature-journey` | ต้องการ **Feature List** (ภาพลำดับชั้นของฟีเจอร์ทั้งระบบ แม็ปกับ US ID) หรือ **User Journey เป็น Mermaid diagram** (เส้นทางของ persona พร้อมจุดที่อารมณ์ตก) | `.claude/skills/feature-journey/SKILL.md` |
| `/high-level-architecture` | ต้องการสร้าง/ปรับปรุง **High-Level Architecture เชิง conceptual** — logical component, trust boundary, data flow ตาม user journey — **ห้ามผูกกับเทคโนโลยี/vendor** ใช้ก่อน COULSON เลือก stack จริง | `.claude/skills/high-level-architecture/SKILL.md` |
| `/test-design` | ต้องแปลง requirement เป็น **AC testability audit → test case → test data → traceability matrix → test plan → UAT scenario** · ใช้ตอนที่ยัง**ไม่มี**ระบบให้ทดสอบก็ได้ | `.claude/skills/test-design/SKILL.md` |
| `/test-run` | **มีระบบจริงให้ทดสอบแล้ว** — รันเคส บันทึกผล `PASS`/`FAIL`/`BLOCKED`/`DEGRADED` เขียน bug log และตัดสิน **GO / NO-GO** | `.claude/skills/test-run/SKILL.md` |

สอง skill แรกทำคนละหน้าที่และใช้คู่กันได้: `/product-backlog` ให้ **รายการ story และลำดับ** ส่วน `/feature-journey` ให้ **ลำดับชั้น (มีอะไรบ้าง) และลำดับเวลา (เกิดอะไรขึ้นตามลำดับ)** ของ requirement ชุดเดียวกัน — ไม่ใช่อันใดอันหนึ่งแทนกัน

`/high-level-architecture` กิน input จาก `/product-backlog` และ `/feature-journey` แล้วส่งต่อให้ COULSON เลือก stack จริง — **ห้ามใช้แทน** การเขียน `architecture-v1.md` ของ COULSON และห้าม COULSON ใช้ skill นี้เพื่อ "รีบข้าม" ไปเขียนเอกสารที่ผูกกับ stack ทันที

`/test-design` กับ `/test-run` ก็แยกกันด้วยเหตุผลเดียวกัน — คนละเวลาและคนละโฟลเดอร์ปลายทาง (`01-test-plan` vs `02-test-result`) · **`/test-design` ห้ามแตะ `02-test-result` และ `/test-run` ห้ามแก้ test case ให้เข้ากับพฤติกรรมของระบบที่ผิด**
