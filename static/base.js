document.querySelectorAll('.sortable').forEach(th => th.addEventListener('click', () => {
    const table = th.closest('table');
    const tbody = table.querySelector('tbody');
    const headerIndex = Array.from(th.parentNode.children).indexOf(th);
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const sortDirection = th.dataset.sortDirection || 'asc';
    const newRows = rows.sort((a, b) => {
        const aValue = a.children[headerIndex].textContent.trim();
        const bValue = b.children[headerIndex].textContent.trim();
        return aValue.localeCompare(bValue, undefined, { sensitivity: 'base' }) * (sortDirection === 'asc' ? 1 : -1);
    });
    newRows.forEach(row => tbody.appendChild(row));
    th.dataset.sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
}));