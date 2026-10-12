function showListMessage(message, isError = false) {
    const box = document.getElementById('listMessage');
    box.textContent = message;
    box.classList.toggle('message-error', isError);
    box.hidden = !message;
}

function readFilters() {
    return {
        fullName: document.getElementById('filterFullName').value.trim(),
        group: document.getElementById('filterGroup').value.trim(),
        isuId: document.getElementById('filterIsuId').value,
        dormNumber: document.getElementById('filterDormNumber').value,
        room: document.getElementById('filterRoom').value,
        moveInDate: document.getElementById('filterMoveInDate').value,
        isForeigner: document.getElementById('filterForeigner').value
    };
}

async function renderTable(filters = {}) {
    const tbody = document.getElementById('studentsBody');
    tbody.innerHTML = '';
    showListMessage('Загрузка...');

    try {
        const students = await getStudents(filters);
        showListMessage('');

        if (students.length === 0) {
            showListMessage('Студенты не найдены');
            return;
        }

        for (const student of students) {
            const row = document.createElement('tr');

            const fullNameCell = document.createElement('td');
            fullNameCell.textContent = student.fullName;

            const groupCell = document.createElement('td');
            groupCell.textContent = student.group;

            const dormCell = document.createElement('td');
            dormCell.textContent = student.dormNumber;

            const roomCell = document.createElement('td');
            roomCell.textContent = student.room;

            const actionsCell = document.createElement('td');

           const viewButton = createActionButton('Просмотр', () => goToView(student.isuId));
           const editButton = createActionButton('Редактировать', () => goToEdit(student.isuId));
           const deleteButton = createActionButton('Удалить', () => handleDelete(student.isuId))

            actionsCell.append(viewButton, editButton, deleteButton);
            row.append(fullNameCell, groupCell, dormCell, roomCell, actionsCell);
            tbody.appendChild(row);
        }
    } catch (error) {
        showListMessage(error.message, true);
    }
}

function createActionButton(text, handler) {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = text;
    button.addEventListener('click', handler);
    return button;
}

function applyFilters() {
    renderTable(readFilters());
}

function resetFilters() {
    document.getElementById('filtersForm').reset();
    renderTable();
}

function goToAdd() {
    window.location.href = 'form.html';
}

function goToEdit(id) {
    window.location.href = `form.html?id=${id}`;
}

function goToView(id) {
    window.location.href = `student.html?id=${id}`;
}

async function handleDelete(id) {
    if (!confirm('Точно удалить этого студента?')) {
        return;
    }

    try {
        await deleteStudent(id);
        await renderTable(readFilters());
    } catch (error) {
        showListMessage(error.message, true);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('filtersForm').addEventListener('submit', event => {
        event.preventDefault();
        applyFilters();
    });

    document.getElementById('resetFilters').addEventListener('click', resetFilters);
    renderTable();
});