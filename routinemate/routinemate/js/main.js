// ---------- 모바일 네비게이션 토글 ----------
const navBar = document.querySelector('.nav-bar');
const navToggle = document.getElementById('navToggle');

navToggle.addEventListener('click', () => {
  navBar.classList.toggle('open');
});

document.querySelectorAll('.nav-links a').forEach((link) => {
  link.addEventListener('click', () => navBar.classList.remove('open'));
});

// ---------- AI 루틴 추천 폼 ----------
const form = document.getElementById('routineForm');
const statusMsg = document.getElementById('statusMsg');
const resultBox = document.getElementById('resultBox');
const resultContent = document.getElementById('resultContent');
const submitBtn = document.getElementById('submitBtn');

const REQUEST_TIMEOUT_MS = 15000;

function setStatus(text, type) {
  statusMsg.textContent = text;
  statusMsg.className = 'status-msg' + (type ? ' ' + type : '');
}

function withTimeout(promise, ms) {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error('TIMEOUT')), ms)
  );
  return Promise.race([promise, timeout]);
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const goal = document.getElementById('goal').value.trim();
  const minutes = document.getElementById('minutes').value;
  const condition = document.getElementById('condition').value;

  // 1) 빈 입력 처리
  if (!goal || !minutes || !condition) {
    setStatus('목표, 시간, 컨디션을 모두 입력해주세요.', 'error');
    resultBox.hidden = true;
    return;
  }

  submitBtn.disabled = true;
  resultBox.hidden = true;
  setStatus('AI가 오늘의 루틴을 만들고 있어요...', 'loading');

  try {
    const response = await withTimeout(
      fetch('/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ goal, minutes, condition }),
      }),
      REQUEST_TIMEOUT_MS
    );

    // 2) API 오류(4xx/5xx) 처리
    if (!response.ok) {
      setStatus('루틴을 불러오는 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.', 'error');
      return;
    }

    const data = await response.json();

    if (!data.routine) {
      setStatus('추천 결과를 받지 못했습니다. 다시 시도해주세요.', 'error');
      return;
    }

    setStatus('', '');
    resultContent.textContent = data.routine;
    resultBox.hidden = false;
  } catch (err) {
    // 3) 지연/타임아웃 처리
    if (err.message === 'TIMEOUT') {
      setStatus('응답이 지연되고 있습니다. 잠시 후 다시 시도해주세요.', 'error');
    } else {
      setStatus('네트워크 오류가 발생했습니다. 연결 상태를 확인해주세요.', 'error');
    }
  } finally {
    submitBtn.disabled = false;
  }
});
