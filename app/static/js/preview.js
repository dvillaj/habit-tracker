
document.getElementById('icon').addEventListener('change', function(e) {
    const preview = document.getElementById('preview-container');
    const previewContainer = document.getElementById('icon-preview');
    
    if (this.files && this.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            preview.innerHTML = `<img src="${e.target.result}" class="img-fluid">`;
            previewContainer.style.display = 'block';
        }
        
        reader.readAsDataURL(this.files[0]);
    } else {
        previewContainer.style.display = 'none';
        preview.innerHTML = '';
    }
});