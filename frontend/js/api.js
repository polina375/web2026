const API_URL = 'http://127.0.0.1:5000/api/requests';

// Если активных фильтров больше этого числа — вместо GET используем QUERY с JSON-телом
const MAX_QUERY_PARAMS = 3;
const NUMERIC_FILTERS = ['isuId', 'dormNumber', 'room'];
const JSON_HEADERS = { 'Content-Type': 'application/json' };

async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, options);

        if (response.status === 204) {
            return null;
        }

        let data = null;
        try {
            data = await response.json();
        } catch (error) {
            data = null;
        }

        if (!response.ok) {
            const text = data?.error?.message || 'Неизвестная ошибка';
            const apiError = new Error(`Код ${response.status}: ${text}`);
            apiError.status = response.status;
            apiError.details = data?.error?.details || null;
            throw apiError;
        }

        return data;
    } catch (error) {
        if (error instanceof TypeError) {
            throw new Error('Не удалось подключиться. Проверьте, что Flask запущен');
        }
        throw error;
    }
}

function cleanFilters(filters) {
    return Object.fromEntries(
        Object.entries(filters).filter(
            ([, value]) => value !== '' && value !== null && value !== undefined
        )
    );
}

function getStudents(filters = {}) {
    const active = cleanFilters(filters);

    if (Object.keys(active).length > MAX_QUERY_PARAMS) {
        return queryStudents(active);
    }

    const query = new URLSearchParams(active).toString();
    return apiRequest(query ? `${API_URL}?${query}` : API_URL);
}

// QUERY /api/requests — фильтры в теле запроса, типы значений как ждёт сервер
function queryStudents(filters) {
    const body = {};

    for (const [key, value] of Object.entries(filters)) {
        if (NUMERIC_FILTERS.includes(key)) {
            body[key] = Number(value);
        } else if (key === 'isForeigner') {
            body[key] = value === true || value === 'true';
        } else {
            body[key] = value;
        }
    }

    return apiRequest(API_URL, {
        method: 'QUERY',
        headers: JSON_HEADERS,
        body: JSON.stringify(body)
    });
}

function getStudentById(id) {
    return apiRequest(`${API_URL}/${id}`);
}

function addStudent(student) {
    return apiRequest(API_URL, {
        method: 'POST',
        headers: JSON_HEADERS,
        body: JSON.stringify(student)
    });
}

function updateStudent(id, student) {
    return apiRequest(`${API_URL}/${id}`, {
        method: 'PATCH',
        headers: JSON_HEADERS,
        body: JSON.stringify(student)
    });
}

function deleteStudent(id) {
    return apiRequest(`${API_URL}/${id}`, { method: 'DELETE' });
}