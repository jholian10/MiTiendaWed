document.getElementById('file_input').onchange = function(e) {
    let reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('preview').src = e.target.result;
        document.getElementById('preview').style.display = 'block';
        document.getElementById('msg').style.display = 'none';
    }
    reader.readAsDataURL(this.files[0]);
};
