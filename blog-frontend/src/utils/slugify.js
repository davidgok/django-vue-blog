/**
 * 문자열을 URL에 적합한 슬러그 형태로 변환합니다.
 * 
 * @param {string} text - 변환할 텍스트
 * @param {string} prefix - 슬러그가 비어있을 경우 사용할 접두사 (기본값: 'item')
 * @returns {string} 변환된 슬러그 문자열
 */
export function slugify(text, prefix = 'item') {
    // 입력 유효성 검사
    if (!text || typeof text !== 'string' || text.trim() === '') {
        return `${prefix}-${Date.now()}`;
    }

    // 한글 -> 영문 변환 매핑 (옵션)
    const koreanMap = {
        '가': 'ga', '나': 'na', '다': 'da', '라': 'ra', '마': 'ma',
        '바': 'ba', '사': 'sa', '아': 'a', '자': 'ja', '차': 'cha',
        '카': 'ka', '타': 'ta', '파': 'pa', '하': 'ha'
    };

    // 슬러그 생성 전처리
    let processedText = text.trim();

    // 슬러그 변환 (공백 -> 하이픈, 소문자화, 특수문자 제거)
    let slug = processedText
        .toLowerCase()
        .replace(/\s+/g, '-')     // 공백을 하이픈으로 변환
        .replace(/[^\w-]+/g, '')  // 영문, 숫자, 하이픈이 아닌 문자 제거
        .replace(/--+/g, '-')     // 연속된 하이픈을 하나로 변환
        .replace(/^-+/, '')       // 시작 부분의 하이픈 제거
        .replace(/-+$/, '');      // 끝 부분의 하이픈 제거

    // 슬러그가 비어있는 경우 (한글만 있었던 경우 등) 처리
    if (!slug || slug.trim() === '') {
        // 원본 텍스트에서 첫 글자 가져오기 (영문 변환 시도)
        const firstChar = text.charAt(0);
        const transliterated = koreanMap[firstChar] || prefix.charAt(0);

        // 고유한 슬러그 생성
        const timestamp = Date.now();
        slug = `${transliterated}-${timestamp}`;

        // 영문자, 숫자, 하이픈만 남기고 제거
        slug = slug.replace(/[^\w-]+/g, '');
    }

    // 슬러그 길이 제한
    if (slug.length > 100) {
        slug = slug.substring(0, 100);
    }

    return slug;
}

/**
 * 텍스트를 주어진 길이로 잘라서 말줄임표를 추가합니다.
 * 
 * @param {string} text - 변환할 텍스트
 * @param {number} maxLength - 최대 길이 (기본값: 100)
 * @returns {string} 잘린 텍스트
 */
export function truncateText(text, maxLength = 100) {
    if (!text || text.length <= maxLength) {
        return text;
    }

    return text.substring(0, maxLength) + '...';
}

/**
 * 날짜를 형식화합니다.
 * 
 * @param {string|Date} date - 날짜 객체 또는 문자열
 * @param {string} format - 포맷 ('relative' 또는 'full')
 * @returns {string} 형식화된 날짜 문자열
 */
export function formatDate(date, format = 'full') {
    if (!date) return '';

    const dateObj = date instanceof Date ? date : new Date(date);

    if (format === 'relative') {
        const now = new Date();
        const diffMs = now - dateObj;
        const diffSec = Math.floor(diffMs / 1000);
        const diffMin = Math.floor(diffSec / 60);
        const diffHour = Math.floor(diffMin / 60);
        const diffDay = Math.floor(diffHour / 24);

        if (diffSec < 60) return '방금 전';
        if (diffMin < 60) return `${diffMin}분 전`;
        if (diffHour < 24) return `${diffHour}시간 전`;
        if (diffDay < 7) return `${diffDay}일 전`;
    }

    // 기본 날짜 포맷
    return dateObj.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

export default {
    slugify,
    truncateText,
    formatDate
}; 