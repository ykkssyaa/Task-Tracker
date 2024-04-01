function updateStatus(taskId) {
    const newStatus = document.getElementById('select_status_' + taskId).value;
    const csrftoken = document.querySelector('[name=csrf-token]').content;

    fetch('/projects/update_status/' + taskId, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ status: newStatus })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to update status');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            //document.getElementById('status_' + taskId).innerText = newStatus;
            //alert("Статус успешно обновлён");
        } else {
            throw new Error('Failed to update status');
        }
    })
    .catch(error => {
        console.error(error);
        alert('Failed to update status');
    });
}
