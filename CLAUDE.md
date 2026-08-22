# CLAUDE.md

ไฟล์นี้ให้คำแนะนำแก่ Claude Code (claude.ai/code) เมื่อทำงานกับโค้ดในโปรเจกต์นี้

## สถานะโปรเจกต์

**repo นี้ยังเป็น Obsidian vault สำหรับเอกสารล้วน** ไม่มี `package.json`, build tool, linter หรือ test runner — อย่าสมมติหรือคิดคำสั่ง build/lint/test ขึ้นเองสำหรับ repo นี้

🔴 **โค้ดแอปพลิเคชันมีอยู่แล้วตั้งแต่ 2026-08-22 แต่อยู่ใน repo แยก:**

- GitHub: <https://github.com/korakotcha06-dev/qr-order-app> (private)
- local: `/Users/korakotchangpan/Documents/ADT-AI/Classwork/qr-order-app`

คำสั่ง build/test/dev ทั้งหมดอยู่ใน `CLAUDE.md` ของ repo นั้น (`pnpm dev:all`, `pnpm migrate`, `pnpm seed`, `pnpm test`, `pnpm check:invariants`) · **เอกสารใน `docs/` ของ vault นี้ยังเป็น source of truth ของโค้ดนั้นอยู่** — โค้ดขัดกับเอกสารเมื่อไหร่ให้ทำตามเอกสาร แล้วบันทึกเหตุผลไว้ใน `docs/05-log/changelog.md`

สิ่งที่ build ไปแล้ว: schema เต็ม (24 ตาราง, INV-1..INV-10, RLS) + เส้นทาง dine-in (J1) ครบวง + NFR-11 PIN lock + หน้าจอแอดมิน A-00..A-07 + **ช่องทางเคาน์เตอร์ (J2/J3) ครบวง** = **23 จาก 23 หน้าจอ** — งานที่เหลือของ Phase 0 คือ deploy (R13/R14/R15) และการวัด NFR ที่ build ไปแล้ว · รายละเอียดพร้อมช่องว่างของเอกสารที่เจอตอนลงมือ อยู่ในบันทึก changelog วันที่ 2026-08-22

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
| **COULSON** (โควสัน) | `02-design` — architecture, DB schema, API design ต่อจาก backlog ที่ XAVIER ส่งมอบ | global |
| **SHURI** (ชูริ) | `02-design/01-prototypes` + frontend build (รายงานต่อ COULSON) | global |
| **BANNER** (แบนเนอร์) | backend/API/DB ของระบบสั่งอาหาร (รายงานต่อ COULSON) | global |
| **OKOYE** (โอโคเย) | `03-testing` — test plan/test result, ด่านสุดท้ายก่อน deploy (รายงานต่อ COULSON) | global |
| **JARVIS** (จาร์วิส) | ผู้ประสานงานข้ามทีมเมื่องานสเปน ≥2 แผนก | global |

ลำดับการส่งงาน: **XAVIER** ปิด backlog ใน `01-requirements` ก่อน → ส่งต่อ **COULSON** เริ่ม `02-design` → ทีม SHURI/BANNER ทำตาม scope ที่ COULSON แตกให้ → **OKOYE** เป็นด่านสุดท้ายก่อนขึ้นจริง

## Skill ของโปรเจกต์นี้

| Skill | ใช้เมื่อไหร่ | ที่อยู่ |
|-------|-------------|--------|
| `/product-backlog` | มี requirement ใหม่ที่ต้องแตกเป็น **user story + acceptance criteria + business rule + ลำดับความสำคัญ** ก่อนส่งเข้า `01-spec` / `02-plan` / `03-task` | `.claude/skills/product-backlog/SKILL.md` |
| `/feature-journey` | ต้องการ **Feature List** (ภาพลำดับชั้นของฟีเจอร์ทั้งระบบ แม็ปกับ US ID) หรือ **User Journey เป็น Mermaid diagram** (เส้นทางของ persona พร้อมจุดที่อารมณ์ตก) | `.claude/skills/feature-journey/SKILL.md` |

สอง skill นี้ทำคนละหน้าที่และใช้คู่กันได้: `/product-backlog` ให้ **รายการ story และลำดับ** ส่วน `/feature-journey` ให้ **ลำดับชั้น (มีอะไรบ้าง) และลำดับเวลา (เกิดอะไรขึ้นตามลำดับ)** ของ requirement ชุดเดียวกัน — ไม่ใช่อันใดอันหนึ่งแทนกัน
