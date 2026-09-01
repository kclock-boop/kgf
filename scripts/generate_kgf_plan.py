from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "proposal" / "케이지에프_현장업무자동화_통합대시보드_자료실_구축계획서.pdf"
REGULAR_FONT = r"C:\Windows\Fonts\malgun.ttf"
BOLD_FONT = r"C:\Windows\Fonts\malgunbd.ttf"

NAVY = colors.HexColor("#102a43")
TEAL = colors.HexColor("#0f766e")
ORANGE = colors.HexColor("#d85b34")
PALE_TEAL = colors.HexColor("#e8f5f2")
PALE_ORANGE = colors.HexColor("#fff1eb")
INK = colors.HexColor("#243b53")
MUTED = colors.HexColor("#627d98")
LINE = colors.HexColor("#d9e2ec")
WHITE = colors.white


def p(text, style):
    return Paragraph(text, style)


def build_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title", parent=base["Normal"], fontName="MalgunBold", fontSize=24,
            leading=32, textColor=NAVY, alignment=TA_LEFT, spaceAfter=6,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle", parent=base["Normal"], fontName="Malgun", fontSize=11,
            leading=18, textColor=MUTED,
        ),
        "h1": ParagraphStyle(
            "H1", parent=base["Normal"], fontName="MalgunBold", fontSize=18,
            leading=25, textColor=NAVY, spaceBefore=4, spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Normal"], fontName="MalgunBold", fontSize=12,
            leading=18, textColor=TEAL, spaceBefore=7, spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["Normal"], fontName="Malgun", fontSize=9.2,
            leading=15, textColor=INK,
        ),
        "small": ParagraphStyle(
            "Small", parent=base["Normal"], fontName="Malgun", fontSize=7.6,
            leading=11, textColor=INK,
        ),
        "table_head": ParagraphStyle(
            "TableHead", parent=base["Normal"], fontName="MalgunBold", fontSize=8,
            leading=11, textColor=WHITE, alignment=TA_CENTER,
        ),
        "table_cell": ParagraphStyle(
            "TableCell", parent=base["Normal"], fontName="Malgun", fontSize=7.6,
            leading=11, textColor=INK,
        ),
        "callout": ParagraphStyle(
            "Callout", parent=base["Normal"], fontName="MalgunBold", fontSize=11,
            leading=18, textColor=NAVY,
        ),
        "caption": ParagraphStyle(
            "Caption", parent=base["Normal"], fontName="Malgun", fontSize=7.3,
            leading=10, textColor=MUTED,
        ),
    }


def band(text, styles, color=NAVY):
    table = Table([[p(text, styles["h2"])]], colWidths=[170 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE_TEAL),
        ("BOX", (0, 0), (-1, -1), 0.7, color),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def text_table(headers, rows, widths, styles, font_size=7.6):
    cell = styles["table_cell"].clone("cell")
    cell.fontSize = font_size
    head = styles["table_head"]
    data = [[p(h, head) for h in headers]]
    data += [[p(value, cell) for value in row] for row in rows]
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fbfd")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(20 * mm, 14 * mm, 190 * mm, 14 * mm)
    canvas.setFont("Malgun", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "(주)케이지에프 | 현장업무 자동화·통합대시보드·자료실 구축계획서 | PoC 기획안")
    canvas.drawRightString(190 * mm, 9 * mm, f"{doc.page}")
    canvas.restoreState()


def story(styles):
    items = []
    add = items.append

    add(Spacer(1, 27 * mm))
    add(p("현장업무 자동화·통합대시보드·자료실", styles["subtitle"]))
    add(p("구축 계획서", styles["title"]))
    add(Spacer(1, 4 * mm))
    add(p("생산·품질·시험/검사·계획 자료를 공용 기준으로 연결하고, 반복 보고 업무부터 안전하게 자동화하기 위한 KGF 맞춤 PoC 기획안", styles["subtitle"]))
    add(Spacer(1, 14 * mm))
    cover = Table([
        [p("PoC 초점", styles["small"]), p("공용 양식 · 자료실 · 이슈 상태관리 · 요약 대시보드 · 보고 초안", styles["body"])],
        [p("진단 기준", styles["small"]), p("사전 수준진단 26점 / Level 1", styles["body"])],
        [p("작성일", styles["small"]), p("2026. 09. 01.", styles["body"])],
    ], colWidths=[35 * mm, 135 * mm])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), PALE_ORANGE),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    add(cover)
    add(Spacer(1, 22 * mm))
    add(p("핵심 제안", styles["h2"]))
    add(p("“공용 자료실과 최소 데이터 기준을 먼저 만들고, 품질 이슈·생산계획 보고 중 하나를 선택해 대시보드와 보고 자동화를 제한된 범위에서 검증한다.”", styles["callout"]))
    add(PageBreak())

    add(p("1. 추진 개요", styles["h1"]))
    add(band("핵심 방향", styles))
    add(Spacer(1, 3 * mm))
    add(p("생산·품질·시험/검사·생산계획 관련 자료의 위치와 책임을 먼저 확인하고, 공용 양식과 분류체계를 정비한다. 그 다음 자료실, 이슈 상태관리, 대시보드, 보고 자동화를 작은 범위에서 순차적으로 검증한다.", styles["body"]))
    add(Spacer(1, 5 * mm))
    add(p("추진 배경", styles["h2"]))
    for text in [
        "생산·품질 부서는 집중 코칭 대상이며, 품질 데이터 보유 가능성이 확인됐다.",
        "사전 수준진단 26점 / Level 1에 따라 AI 사용 보안·데이터 관리·검증 기준이 선행돼야 한다.",
        "반복되는 자료 취합, 이슈 정리, 회의자료 작성은 PoC로 검증하기 적합한 후보 영역이다.",
        "실제 자료 위치, 시스템, 업무 채널은 현장 인터뷰와 샘플 양식 확인 후 확정한다.",
    ]:
        add(p(f"• {text}", styles["body"]))
    add(Spacer(1, 5 * mm))
    add(p("구축 목표", styles["h2"]))
    add(text_table(
        ["구분", "현재 확인·점검 범위", "PoC 목표", "기대효과"],
        [
            ["자료관리", "파일 위치·양식·책임자", "품질·시험·생산 자료의 공용 분류", "검색·재사용·검토 시간 단축"],
            ["이슈관리", "불량·조치·검토 흐름", "번호 기반 상태·조치이력", "누락 방지·원인 추적"],
            ["대시보드", "관리자 핵심 질문", "품질·계획·보고 요약 화면", "우선순위 판단 지원"],
            ["보고자동화", "반복 보고서 유형", "주간 보고·회의자료 초안", "취합·작성 시간 절감"],
            ["AI 사용기준", "입력 가능 정보·검토자", "보안 가이드와 검토 절차", "안전한 실무 활용"],
        ], [25 * mm, 47 * mm, 50 * mm, 48 * mm], styles
    ))
    add(Spacer(1, 7 * mm))
    add(p("현장 확인 원칙", styles["h2"]))
    add(p("메신저, 도면, 설비 로그 등 구체적인 현행 방식은 KGF에서 확인된 사실이 아니다. 본 계획서는 해당 항목을 확정 전제로 사용하지 않으며, 현장 확인 질문으로만 다룬다.", styles["body"]))
    add(PageBreak())

    add(p("2. 목표 시스템(To-Be)과 사용자 흐름", styles["h1"]))
    add(band("Data Room → 이슈 상태관리 → 통합 Dashboard → 주간 보고·회의자료 자동화", styles, TEAL))
    add(Spacer(1, 5 * mm))
    add(p("표준 업무 프로세스", styles["h2"]))
    flow = Table([[p("자료/이슈 등록", styles["small"]), p("담당자 확인", styles["small"]), p("원인·조치 입력", styles["small"]), p("검토 요청", styles["small"]), p("승인/보완", styles["small"]), p("이력·보고 반영", styles["small"]) ]], colWidths=[28 * mm] * 6)
    flow.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE_TEAL),
        ("BOX", (0, 0), (-1, -1), 0.8, TEAL),
        ("INNERGRID", (0, 0), (-1, -1), 0.6, TEAL),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    add(flow)
    add(Spacer(1, 8 * mm))
    add(p("상태값 초안", styles["h2"]))
    add(text_table(
        ["상태", "의미", "담당자 행동"],
        [
            ["등록", "자료 또는 이슈가 새로 접수됨", "기본정보·분류 입력"],
            ["확인", "담당 부서가 내용을 인지함", "담당자·기한 지정"],
            ["조치중", "원인 확인 또는 개선 활동 진행", "조치내용·증빙 추가"],
            ["검토대기", "조치 완료 후 검토 요청", "검토자 확인"],
            ["승인", "검토가 완료됨", "이력 확정"],
            ["보완요청", "추가 확인 또는 재조치 필요", "보완 사유·기한 기록"],
        ], [30 * mm, 75 * mm, 65 * mm], styles
    ))
    add(Spacer(1, 8 * mm))
    add(p("권한별 Dashboard", styles["h2"]))
    add(text_table(
        ["사용자", "주요 질문", "우선 화면"],
        [
            ["경영진", "이번 주 어떤 품질·납기 이슈를 먼저 봐야 하는가", "핵심 이슈·조치·지연 요약"],
            ["생산 관리자", "계획 대비 실적과 지연 사유는 무엇인가", "계획·실적·지연 현황"],
            ["품질 관리자", "반복 이슈와 미완료 조치는 무엇인가", "이슈·시정조치·검토대기"],
            ["실무 담당자", "내가 처리할 자료와 조치는 무엇인가", "내 할 일·등록·조치 입력"],
            ["데이터/보안", "어떤 자료가 AI에 사용됐고 검토됐는가", "마스킹·검토·권한 기록"],
        ], [27 * mm, 75 * mm, 68 * mm], styles
    ))
    add(PageBreak())

    add(p("3. Data Room과 대시보드 설계", styles["h1"]))
    add(p("자료실 분류체계", styles["h2"]))
    add(text_table(
        ["자료실", "우선 대상 자료", "현장 확인 후 확정할 사항"],
        [
            ["품질", "불량 이력, 시정조치, 클레임, 품질 기준", "불량 분류·승인 양식"],
            ["시험/검사", "시험성적서, 검사 결과, 판정 기록", "제품군별 필수 항목"],
            ["생산·계획", "생산계획, 실적, 납기 이슈", "계획 수립·변경 주기"],
            ["재고", "재고 현황, 부족·과다 이슈", "공유 가능 범위·기준"],
            ["R&D·기술", "시험 요약, 기술 검토 문서", "보안 등급·외부 반출 기준"],
            ["보고", "주간 보고, 회의자료, 승인본", "보관 주기·최종본 기준"],
        ], [30 * mm, 75 * mm, 65 * mm], styles
    ))
    add(Spacer(1, 7 * mm))
    add(p("핵심 메타데이터", styles["h2"]))
    add(p("이슈/자료번호, 제품군, 부서, 공정 또는 업무구분, 자료유형, 발생일, 등록자, 검토자, 상태, 원인분류, 조치내용, 기한, 보안등급, AI 입력 가능 여부, 파일명, 버전", styles["body"]))
    add(Spacer(1, 7 * mm))
    add(p("초기 Dashboard KPI", styles["h2"]))
    add(text_table(
        ["영역", "확인할 질문", "지표 예시"],
        [
            ["품질", "반복 이슈와 미완료 조치는 무엇인가", "이슈 건수, 반복 유형, 검토대기, 조치 리드타임"],
            ["생산·계획", "계획과 실제 운영의 차이는 무엇인가", "계획 대비 실적, 지연 건수, 지연 사유"],
            ["자료관리", "자료가 제때 등록·검토되는가", "자료 등록률, 미분류 자료, 최신 버전 비율"],
            ["교육·확산", "AI 훈련이 실제 업무에 적용되는가", "적용 과제 수, 검토 완료율, 보고 시간 절감"],
        ], [30 * mm, 72 * mm, 68 * mm], styles
    ))
    add(Spacer(1, 7 * mm))
    add(p("설계 원칙", styles["h2"]))
    for text in [
        "모든 자료는 번호와 기본 분류값으로 연결한다.",
        "파일명만이 아니라 제품군·유형·일자·상태로 검색 가능하게 설계한다.",
        "KPI 목표치와 실제 수치는 현장 데이터 확보 뒤 정한다.",
        "초기 화면은 경영진·관리자·실무자가 필요한 질문을 줄여 보여주는 방식으로 설계한다.",
    ]:
        add(p(f"• {text}", styles["body"]))
    add(PageBreak())

    add(p("4. 자동화 규칙·AI 사용기준·PoC 로드맵", styles["h1"]))
    add(p("우선 자동화 규칙", styles["h2"]))
    add(text_table(
        ["자동화 항목", "처리 규칙"],
        [
            ["상태 집계", "등록·확인·조치중·검토대기·승인·보완요청 상태를 자동 집계"],
            ["기한 표시", "검토 또는 조치 기한 경과 시 지연 후보로 표시"],
            ["자료 연결", "파일을 이슈/자료번호와 분류값에 연결"],
            ["보고 초안", "승인된 자료 기준으로 주간 요약·회의자료 초안 생성"],
            ["반복 이슈", "동일 제품군·유형·원인 키워드의 반복 후보 표시"],
        ], [40 * mm, 130 * mm], styles
    ))
    add(Spacer(1, 7 * mm))
    add(p("AI 사용기준", styles["h2"]))
    safety = Table([[p("AI는 판단을 대신하는 도구가 아니라, 마스킹된 자료의 요약·분류·초안 작성을 보조하는 도구로 먼저 사용한다. 민감정보·고객정보·단가·기술정보의 외부 입력 여부는 사내 기준과 담당자 검토를 거쳐 결정한다.", styles["body"])]], colWidths=[170 * mm])
    safety.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE_ORANGE),
        ("BOX", (0, 0), (-1, -1), 0.7, ORANGE),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    add(safety)
    add(Spacer(1, 7 * mm))
    add(p("6단계 PoC 로드맵", styles["h2"]))
    add(text_table(
        ["단계", "구축 내용", "핵심 산출물"],
        [
            ["1", "인터뷰·자료 현황 확인·보안 기준", "데이터맵, AI 사용 가이드 초안"],
            ["2", "자료실 분류체계와 공용 양식", "메타데이터 표준, 샘플 양식"],
            ["3", "이슈·조치 상태관리", "상태 흐름, 책임·기한 관리안"],
            ["4", "통합 대시보드 시안", "품질·계획·자료관리 화면"],
            ["5", "보고 자동화 실습", "주간 보고 또는 회의자료 초안"],
            ["6", "제한 파일럿·효과 점검", "결과보고, 확대 적용 제안"],
        ], [14 * mm, 78 * mm, 78 * mm], styles
    ))
    add(PageBreak())

    add(p("5. 기대효과와 최종 제안", styles["h1"]))
    add(p("기대효과와 초기 성공 기준", styles["h2"]))
    add(text_table(
        ["영역", "기대효과", "초기 성공 기준 예시"],
        [
            ["업무효율", "반복 취합·재입력·설명 작성 감소", "보고서 작성 시간 또는 준비 횟수 감소"],
            ["정확성", "최신 자료·검토 상태의 일원화", "원본 대조·검토 절차 준수"],
            ["가시성", "관리자가 우선 이슈를 빠르게 확인", "주간 핵심 이슈 목록의 정시 확인"],
            ["추적성", "자료·조치·승인 이력 연결", "이슈번호 기준 관련 자료 검색 가능"],
            ["데이터자산", "재사용 가능한 공용 데이터 축적", "공용 양식과 분류체계의 현장 적용"],
        ], [28 * mm, 72 * mm, 70 * mm], styles
    ))
    add(Spacer(1, 8 * mm))
    add(p("이번 회차에서 확보할 자료", styles["h2"]))
    for text in [
        "최근 품질 이력 또는 불량·시정조치 양식 1~2종",
        "시험/검사 결과 양식 또는 보고서 예시",
        "생산계획·실적 또는 재고 관련 보고 양식 1종",
        "주간 회의자료 또는 반복 보고서 예시",
        "현재 AI 사용·보안 관련 지침 또는 확인 가능한 담당자 정보",
    ]:
        add(p(f"• {text}", styles["body"]))
    add(Spacer(1, 10 * mm))
    add(band("최종 제안", styles, ORANGE))
    add(Spacer(1, 4 * mm))
    add(p("“케이지에프의 품질·생산·시험/검사·계획 관련 자료를 공용 분류체계로 연결하고, 이슈 상태와 검토 이력을 한 화면에서 확인하며, 검증 가능한 반복 보고 업무부터 자동화하는 PoC를 추진한다.”", styles["callout"]))
    add(Spacer(1, 8 * mm))
    add(p("초기 PoC는 공용 양식, 자료실 분류, 이슈 상태관리, 요약 대시보드, 보고 초안에 집중한다. 실제 시스템 연동, 이미지 분석, 고도화 AI 기능은 데이터 품질과 보안·검토 절차가 자리잡은 뒤 단계적으로 검토한다.", styles["body"]))
    return items


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdfmetrics.registerFont(TTFont("Malgun", REGULAR_FONT))
    pdfmetrics.registerFont(TTFont("MalgunBold", BOLD_FONT))
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=18 * mm, bottomMargin=21 * mm,
        title="케이지에프 현장업무 자동화·통합대시보드·자료실 구축계획서",
        author="KGF AI 훈련컨설팅",
    )
    doc.build(story(build_styles()), onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    main()
