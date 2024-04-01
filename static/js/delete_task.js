function deleteTask(taskId) {
    const csrftoken = document.querySelector('[name=csrf-token]').content;

    fetch('tasks/delete/' + taskId, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ task_id: taskId })
    })
    .then(response => response.json())
    .then(data => {
        if (data && data.success === true) {
            location.reload();
        } else {
            throw new Error('Failed to delete task');
        }
    })
    .catch(error => {
        console.error(error);
        alert('Failed to delete task');
    });
}
