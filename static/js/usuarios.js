document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById('userSearchInput');
    const tableRows = document.querySelectorAll('#userTable tbody tr');
    
    if(searchInput) {
        searchInput.addEventListener('keyup', function() {
            const query = this.value.toLowerCase().trim();
            tableRows.forEach(row => {
                const name = row.cells[1].textContent.toLowerCase();
                const email = row.cells[2].textContent.toLowerCase();
                row.style.display = (name.includes(query) || email.includes(query)) ? '' : 'none';
            });
        });
    }
});
