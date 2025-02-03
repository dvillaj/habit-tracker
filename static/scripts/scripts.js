// static/js/scripts.js
document.addEventListener('DOMContentLoaded', function() {
    // Manejar el modal de borrado
    var deleteModal = document.getElementById('deleteModal');
    if (deleteModal) {
        deleteModal.addEventListener('show.bs.modal', function (event) {
            var button = event.relatedTarget;
            var habitId = button.getAttribute('data-habit-id');
            var habitName = button.getAttribute('data-habit-name');
            
            var form = deleteModal.querySelector('#deleteForm');
            form.action = `/habits/${habitId}/delete`;
            
            deleteModal.querySelector('#habitName').textContent = habitName;
        });
    }
});
