function getEditId() {
    const id = new URLSearchParams(window.location.search).get('id');
    return id === null ? null : Number(id);
}

// Пустое поле уходит на сервер как null — проверяет и отвечает сервер
function numberOrNull(id) {
    const value = document.getElementById(id).value.trim();
    return value === '' ? null : Number(value);
}

function readForm() {
    return {
        fullName: document.getElementById('fullName').value.trim(),
        group: document.getElementById('group').value.trim(),
        isuId: numberOrNull('isuId'),
        dormNumber: numberOrNull('dormNumber'),
        room: numberOrNull('room'),
        moveInDate: document.getElementById('moveInDate').value,
        isForeigner: document.getElementById('isForeigner').checked,
        notes: document.getElementById('notes').value.trim()
    };
}

function fillForm(student) {
    document.getElementById('fullName').value = student.fullName;
    document.getElementById('group').value = student.group;
    document.getElementById('isuId').value = student.isuId;
    document.getElementById('dormNumber').value = student.dormNumber;
    document.getElementById('room').value = student.room;
    document.getElementById('moveInDate').value = student.moveInDate;
    document.getElementById('isForeigner').checked = student.isForeigner;
    document.getElementById('notes').value = student.notes || '';
}

function showFormMessage(message, isError = false) {
    const box = document.getElementById('formMessage');
    box.textContent = message;
    box.classList.toggle('message-error', isError);
    box.hidden = !message;

    if (isError) {
        box.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

function clearFieldErrors() {
    document.querySelectorAll('.field-error').forEach(box => { box.textContent = ''; });
    document.querySelectorAll('.input-invalid').forEach(input => input.classList.remove('input-invalid'));
}

// Показывает ошибки сервера под полями; возвращает сообщения, для которых поля нет
function showFieldErrors(details) {
    const general = [];

    for (const [field, message] of Object.entries(details || {})) {
        const box = document.querySelector(`[data-error-for="${field}"]`);

        if (box) {
            box.textContent = message;
            document.getElementById(field)?.classList.add('input-invalid');
        } else {
            general.push(message);
        }
    }

    return general;
}

async function handleSave() {
    clearFieldErrors();

    const editId = getEditId();
    const saveButton = document.querySelector('.button-save');
    saveButton.disabled = true;
    showFormMessage('Сохранение...');

    try {
    const student = readForm();

    if (editId === null) {
        await addStudent(student);
    } else {
        delete student.isuId;
        await updateStudent(editId, student);
    }

    window.location.href = 'index.html';
    }catch (error) {
        const general = showFieldErrors(error.details);
        showFormMessage([error.message, ...general].join('\n'), true);
        saveButton.disabled = false;
    }
}

async function loadStudentForEdit() {
    const editId = getEditId();

    if (editId === null) {
        return;
    }

    if (!Number.isInteger(editId) || editId <= 0) {
        showFormMessage('Некорректный ID студента', true);
        return;
    }

    try {
    fillForm(await getStudentById(editId));
    document.getElementById('isuId').readOnly = true;
    } catch (error) {
        showFormMessage(error.message, true);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('formTitle').textContent =
        getEditId() === null ? 'Добавление студента' : 'Редактирование студента';

    document.getElementById('studentForm').addEventListener('submit', event => {
        event.preventDefault();
        handleSave();
    });

    loadStudentForEdit();
});