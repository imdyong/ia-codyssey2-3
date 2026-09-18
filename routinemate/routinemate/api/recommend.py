"""
Vercel Serverless Function (Python)
POST /api/recommend
Body: { "goal": str, "minutes": str, "condition": str }
Response: { "routine": str }

환경 변수 ANTHROPIC_API_KEY 가 Vercel 프로젝트 설정에 등록되어 있어야 합니다.
"""

from http.server import BaseHTTPRequestHandler
import json
import os

from anthropic import Anthropic


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length) if content_length else b"{}"
            payload = json.loads(raw_body or b"{}")
        except (ValueError, json.JSONDecodeError):
            self._send_json(400, {"error": "잘못된 요청 형식입니다."})
            return

        goal = (payload.get("goal") or "").strip()
        minutes = (payload.get("minutes") or "").strip()
        condition = (payload.get("condition") or "").strip()

        # 서버 측 필수값 검증 (빈 입력 실패 처리)
        if not goal or not minutes or not condition:
            self._send_json(400, {"error": "goal, minutes, condition은 필수입니다."})
            return

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            self._send_json(500, {"error": "서버에 API 키가 설정되어 있지 않습니다."})
            return

        prompt = (
            f"사용자의 목표: {goal}\n"
            f"오늘 사용 가능한 시간: {minutes}분\n"
            f"오늘 컨디션: {condition}\n\n"
            "위 정보를 바탕으로, 사용자가 오늘 바로 실천할 수 있는 아주 구체적인 "
            "미니 루틴 하나를 한국어로 제안해줘. 다음 형식을 지켜줘:\n"
            "1) 루틴 이름 (한 줄)\n"
            "2) 실행 순서 (2~4단계, 각 단계는 한 문장)\n"
            "3) 오늘 컨디션을 고려한 한 줄 응원 메시지\n"
            "전체 200자 내외로 간결하게 작성하고, 불필요한 서론 없이 바로 결과만 제시해줘."
        )

        try:
            client = Anthropic(api_key=api_key)
            message = client.messages.create(
                model="claude-3-5-haiku-latest",
                max_tokens=400,
                messages=[{"role": "user", "content": prompt}],
            )
            routine_text = "".join(
                block.text for block in message.content if block.type == "text"
            ).strip()

            if not routine_text:
                self._send_json(502, {"error": "AI 응답이 비어있습니다."})
                return

            self._send_json(200, {"routine": routine_text})

        except Exception:
            # 업스트림 AI API 오류 처리 (4xx/5xx 포함)
            self._send_json(502, {"error": "AI 응답 생성 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."})

    def _send_json(self, status_code, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
